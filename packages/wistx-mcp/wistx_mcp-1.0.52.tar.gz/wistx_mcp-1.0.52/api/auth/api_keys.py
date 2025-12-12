"""API key management and verification."""

import hashlib
import hmac
import logging
import secrets
from datetime import datetime, timedelta
from typing import Any, Optional

from bson import ObjectId
from fastapi import HTTPException, status

from api.config import settings
from api.database.mongodb import mongodb_manager
from api.auth.admin import is_internal_admin, is_admin_api_key

logger = logging.getLogger(__name__)


class APIKeyManager:
    """Production-ready API key management."""

    @staticmethod
    def generate_api_key(prefix: str = "wistx") -> tuple[str, str]:
        """Generate secure API key.

        Args:
            prefix: Key prefix (default: "wistx")

        Returns:
            Tuple of (full_key, key_hash)
        """
        random_bytes = secrets.token_bytes(32)
        key = f"{prefix}_{random_bytes.hex()}"
        key_hash = APIKeyManager.hash_api_key(key)
        return key, key_hash

    @staticmethod
    def hash_api_key(api_key: str) -> str:
        """Hash API key with pepper for secure storage.

        Uses HMAC-SHA256 with a secret pepper to prevent rainbow table attacks.
        The pepper is stored in environment variables and not in the database,
        providing an additional layer of security even if the database is compromised.

        Args:
            api_key: API key string

        Returns:
            HMAC-SHA256 hash of the key with pepper
        """
        # Use HMAC with pepper for secure hashing
        # This is more secure than simple SHA256 as it:
        # 1. Prevents rainbow table attacks (pepper is secret)
        # 2. Provides constant-time comparison safety
        # 3. Is the industry standard for keyed hashing
        return hmac.new(
            key=settings.api_key_pepper.encode(),
            msg=api_key.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

    async def create_api_key(
        self,
        user_id: str,
        name: str,
        description: Optional[str] = None,
        organization_id: Optional[str] = None,
        expires_at: Optional[datetime] = None,
    ) -> dict[str, Any]:
        """Create new API key for user.

        Args:
            user_id: User ID
            name: Key name
            description: Key description
            organization_id: Organization ID (optional)
            expires_at: Expiration date (optional)

        Returns:
            Dictionary with api_key, api_key_id, and metadata
        """
        db = mongodb_manager.get_database()
        collection = db.api_keys

        api_key, key_hash = self.generate_api_key()
        key_prefix = api_key[:16]

        user_doc = db.users.find_one({"_id": ObjectId(user_id)})
        if not user_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        plan = user_doc.get("plan", "professional")
        rate_limits = user_doc.get("limits", {})

        api_key_doc = {
            "key_hash": key_hash,
            "key_prefix": key_prefix,
            "user_id": ObjectId(user_id),
            "organization_id": ObjectId(organization_id) if organization_id else None,
            "name": name,
            "description": description,
            "environment": "production",
            "plan": plan,
            "rate_limits": rate_limits,
            "scopes": None,
            "allowed_models": None,
            "ip_whitelist": None,
            "referrer_whitelist": None,
            "is_active": True,
            "is_test_key": False,
            "usage_count": 0,
            "last_used_at": None,
            "last_used_ip": None,
            "last_used_endpoint": None,
            "created_at": datetime.utcnow(),
            "expires_at": expires_at,
            "revoked_at": None,
            "revoked_reason": None,
            "rotated_from": None,
            "rotated_to": None,
            "rotated_at": None,
            "grace_period_end": None,
            "replaced_by": None,
            "created_by": ObjectId(user_id),
            "notes": description,
        }

        result = collection.insert_one(api_key_doc)
        api_key_id = str(result.inserted_id)

        logger.info("Created API key for user %s: %s", user_id, key_prefix)

        from api.models.audit_log import AuditEventType, AuditLogSeverity
        from api.services.audit_log_service import audit_log_service

        audit_log_service.log_event(
            event_type=AuditEventType.API_KEY_CREATED,
            severity=AuditLogSeverity.MEDIUM,
            message=f"API key created: {key_prefix} for user {user_id}",
            success=True,
            user_id=user_id,
            api_key_id=api_key_id,
            organization_id=organization_id,
            details={
                "key_prefix": key_prefix,
                "name": name,
                "expires_at": expires_at.isoformat() if expires_at else None,
            },
            compliance_tags=["PCI-DSS-10", "SOC2"],
        )

        return {
            "api_key": api_key,
            "api_key_id": api_key_id,
            "key_prefix": key_prefix,
            "created_at": api_key_doc["created_at"].isoformat(),
            "expires_at": expires_at.isoformat() if expires_at else None,
        }

    async def verify_api_key(self, api_key: str) -> Optional[dict[str, Any]]:
        """Verify API key and return user info.

        Args:
            api_key: API key string

        Returns:
            Dictionary with user info if valid, None otherwise
        """
        is_admin_key = is_admin_api_key(api_key)

        key_hash = self.hash_api_key(api_key)
        db = mongodb_manager.get_database()
        collection = db.api_keys

        api_key_doc = collection.find_one(
            {
                "key_hash": key_hash,
                "is_active": True,
            }
        )

        if not api_key_doc:
            rotated_key = collection.find_one({
                "key_hash": key_hash,
                "rotated_at": {"$exists": True},
                "grace_period_end": {"$gt": datetime.utcnow()},
            })
            if rotated_key:
                replacement_id = rotated_key.get("replaced_by")
                if replacement_id:
                    replacement = collection.find_one({"_id": replacement_id, "is_active": True})
                    if replacement:
                        api_key_doc = replacement
                        logger.info("Using rotated key replacement for user %s", str(replacement.get("user_id")))
            else:
                return None

        if not api_key_doc:
            return None

        if api_key_doc.get("revoked_at"):
            return None

        expires_at = api_key_doc.get("expires_at")
        if expires_at and expires_at < datetime.utcnow():
            return None

        grace_period_end = api_key_doc.get("grace_period_end")
        if grace_period_end and datetime.utcnow() > grace_period_end:
            return None

        organization_id = str(api_key_doc["organization_id"]) if api_key_doc.get("organization_id") else None

        if organization_id:
            org = db.organizations.find_one({"_id": ObjectId(organization_id)})
            if not org:
                logger.warning("Organization not found for API key: %s", organization_id)
                return None

            user_id = str(api_key_doc["user_id"])
            user_doc = db.users.find_one({"_id": api_key_doc["user_id"]})
            if not user_doc:
                logger.warning("User not found for API key: %s", user_id)
                return None

            plan_id = org.get("plan_id", "team")
            from api.services.plan_service import plan_service

            plan = plan_service.get_plan(plan_id)
            rate_limits = plan.limits.requests_per_minute if plan else 60
            email = user_doc.get("email", "")

            from api.auth.admin import get_admin_info

            admin_info = get_admin_info(user_doc)
            if is_admin_key:
                admin_info["is_admin"] = True
                admin_info["is_super_admin"] = True

            organization_role = None
            member = db.organization_members.find_one(
                {
                    "organization_id": ObjectId(organization_id),
                    "user_id": api_key_doc["user_id"],
                    "status": "active",
                }
            )
            if member:
                organization_role = member.get("role")

            return {
                "user_id": user_id,
                "email": email,
                "organization_id": organization_id,
                "organization_role": organization_role,
                "api_key_id": str(api_key_doc["_id"]),
                "plan": plan_id,
                "rate_limits": rate_limits,
                "scopes": api_key_doc.get("scopes"),
                "allowed_models": api_key_doc.get("allowed_models"),
                **admin_info,
            }

        user_id = str(api_key_doc["user_id"])

        user_doc = db.users.find_one({"_id": api_key_doc["user_id"]})
        if not user_doc:
            logger.warning("User not found for API key: %s", user_id)
            return None

        plan = api_key_doc.get("plan", user_doc.get("plan", "professional"))
        rate_limits = api_key_doc.get("rate_limits", user_doc.get("limits", {}))
        email = user_doc.get("email", "")

        from api.auth.admin import get_admin_info

        admin_info = get_admin_info(user_doc)
        if is_admin_key:
            admin_info["is_admin"] = True
            admin_info["is_super_admin"] = True

        return {
            "user_id": user_id,
            "email": email,
            "organization_id": organization_id,
            "api_key_id": str(api_key_doc["_id"]),
            "plan": plan,
            "rate_limits": rate_limits,
            "scopes": api_key_doc.get("scopes"),
            "allowed_models": api_key_doc.get("allowed_models"),
            **admin_info,
        }

    async def revoke_api_key(
        self,
        api_key_id: str,
        user_id: str,
        reason: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> bool:
        """Revoke API key.

        Args:
            api_key_id: API key ID
            user_id: User ID (for authorization)
            reason: Revocation reason

        Returns:
            True if revoked, False otherwise
        """
        db = mongodb_manager.get_database()
        collection = db.api_keys

        result = collection.update_one(
            {
                "_id": ObjectId(api_key_id),
                "user_id": ObjectId(user_id),
            },
            {
                "$set": {
                    "is_active": False,
                    "revoked_at": datetime.utcnow(),
                    "revoked_reason": reason,
                }
            },
        )

        if result.modified_count > 0:
            logger.info("Revoked API key %s for user %s", api_key_id, user_id)

            from api.models.audit_log import AuditEventType, AuditLogSeverity
            from api.services.audit_log_service import audit_log_service

            api_key_doc = collection.find_one({"_id": ObjectId(api_key_id)})
            organization_id = str(api_key_doc["organization_id"]) if api_key_doc.get("organization_id") else None

            audit_log_service.log_event(
                event_type=AuditEventType.API_KEY_DELETED,
                severity=AuditLogSeverity.HIGH,
                message=f"API key revoked: {api_key_id} for user {user_id}",
                success=True,
                user_id=user_id,
                api_key_id=api_key_id,
                organization_id=organization_id,
                ip_address=ip_address,
                user_agent=user_agent,
                details={
                    "reason": reason,
                    "key_prefix": api_key_doc.get("key_prefix") if api_key_doc else None,
                },
                compliance_tags=["PCI-DSS-10", "SOC2"],
            )

            return True

        return False

    async def list_api_keys(self, user_id: str) -> list[dict[str, Any]]:
        """List all API keys for user.

        Args:
            user_id: User ID

        Returns:
            List of API key dictionaries
        """
        db = mongodb_manager.get_database()
        collection = db.api_keys

        cursor = collection.find(
            {"user_id": ObjectId(user_id)},
            {
                "key_hash": 0,
            },
        ).sort("created_at", -1)

        keys = []
        for doc in cursor:
            keys.append({
                "api_key_id": str(doc["_id"]),
                "key_prefix": doc.get("key_prefix"),
                "name": doc.get("name"),
                "description": doc.get("description"),
                "is_active": doc.get("is_active", False),
                "created_at": doc.get("created_at").isoformat() if doc.get("created_at") else None,
                "expires_at": doc.get("expires_at").isoformat() if doc.get("expires_at") else None,
                "last_used_at": doc.get("last_used_at").isoformat() if doc.get("last_used_at") else None,
                "usage_count": doc.get("usage_count", 0),
            })

        return keys

    async def rotate_api_key(
        self,
        user_id: str,
        key_id: str,
        grace_period_hours: int = 24,
    ) -> dict[str, Any]:
        """Rotate API key with grace period.

        Args:
            user_id: User ID
            key_id: Current API key ID
            grace_period_hours: Hours to allow old key to work (default: 24)

        Returns:
            Dictionary with new api_key, api_key_id, and metadata

        Raises:
            HTTPException: If key not found or unauthorized
        """
        db = mongodb_manager.get_database()
        collection = db.api_keys

        current_key = collection.find_one({"_id": ObjectId(key_id), "user_id": ObjectId(user_id)})
        if not current_key:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API key not found",
            )

        if not current_key.get("is_active"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot rotate inactive API key",
            )

        new_key_doc = await self.create_api_key(
            user_id=user_id,
            name=current_key.get("name", "Rotated Key"),
            description=current_key.get("description"),
            organization_id=str(current_key["organization_id"]) if current_key.get("organization_id") else None,
            expires_at=current_key.get("expires_at"),
        )

        grace_period_end = datetime.utcnow() + timedelta(hours=grace_period_hours)

        collection.update_one(
            {"_id": ObjectId(key_id)},
            {
                "$set": {
                    "rotated_at": datetime.utcnow(),
                    "grace_period_end": grace_period_end,
                    "replaced_by": ObjectId(new_key_doc["api_key_id"]),
                }
            },
        )

        logger.info("Rotated API key %s for user %s, grace period until %s", key_id, user_id, grace_period_end)

        from api.models.audit_log import AuditEventType, AuditLogSeverity
        from api.services.audit_log_service import audit_log_service

        audit_log_service.log_event(
            event_type=AuditEventType.API_KEY_ROTATED,
            severity=AuditLogSeverity.MEDIUM,
            message=f"API key rotated: {key_id} for user {user_id}",
            success=True,
            user_id=user_id,
            api_key_id=key_id,
            organization_id=str(current_key["organization_id"]) if current_key.get("organization_id") else None,
            details={
                "old_key_prefix": current_key.get("key_prefix"),
                "new_key_prefix": new_key_doc.get("key_prefix"),
                "grace_period_hours": grace_period_hours,
                "grace_period_end": grace_period_end.isoformat(),
            },
            compliance_tags=["PCI-DSS-10", "SOC2"],
        )

        try:
            from api.services.alert_service import AlertService, AlertChannel

            alert_service = AlertService()
            await alert_service.create_alert(
                budget_id=None,
                user_id=user_id,
                alert_type="api_key_rotation",
                message=f"Your API key '{current_key.get('name', 'Unnamed')}' has been rotated. The old key will work for {grace_period_hours} more hours.",
                utilization_percent=0.0,
                channels=[AlertChannel.IN_APP],
            )
        except Exception as e:
            logger.warning("Failed to send rotation notification: %s", e)

        return new_key_doc

    async def create_organization_api_key(
        self,
        organization_id: str,
        name: str,
        created_by: str,
        description: Optional[str] = None,
        expires_at: Optional[datetime] = None,
    ) -> dict[str, Any]:
        """Create API key for organization.

        **CRITICAL**: Only Team and Enterprise plans can create organization API keys.
        Organization API keys are shared across all team members.

        Args:
            organization_id: Organization ID
            name: Key name
            created_by: User ID who created the key (must be org admin/owner)
            description: Key description
            expires_at: Expiration date (optional)

        Returns:
            Dictionary with api_key, api_key_id, and metadata

        Raises:
            HTTPException: If organization not found, plan doesn't support org keys, or limit exceeded
        """
        from api.services.organization_service import organization_service
        from api.services.plan_service import plan_service

        org = await organization_service.get_organization(organization_id)
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found",
            )

        plan_id = org.plan_id
        if plan_id not in ["team", "enterprise"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Organization API keys require Team or Enterprise plan. Current plan: {plan_id}",
            )

        plan = plan_service.get_plan(plan_id)
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Plan configuration error",
            )

        db = mongodb_manager.get_database()
        collection = db.api_keys

        existing_count = collection.count_documents(
            {
                "organization_id": ObjectId(organization_id),
                "is_active": True,
                "revoked_at": None,
            }
        )

        if existing_count >= plan.limits.max_api_keys:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Organization API key limit exceeded. Maximum {plan.limits.max_api_keys} keys allowed for {plan_id} plan.",
            )

        api_key, key_hash = self.generate_api_key()
        key_prefix = api_key[:16]

        created_by_user = db.users.find_one({"_id": ObjectId(created_by)})
        if not created_by_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        member = db.organization_members.find_one(
            {
                "organization_id": ObjectId(organization_id),
                "user_id": ObjectId(created_by),
                "status": "active",
            }
        )
        if not member or member.get("role") not in ["owner", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only organization owners and admins can create API keys",
            )

        api_key_doc = {
            "key_hash": key_hash,
            "key_prefix": key_prefix,
            "user_id": ObjectId(created_by),
            "organization_id": ObjectId(organization_id),
            "name": name,
            "description": description,
            "environment": "production",
            "plan": plan_id,
            "rate_limits": plan.limits.requests_per_minute,
            "scopes": None,
            "allowed_models": None,
            "ip_whitelist": None,
            "referrer_whitelist": None,
            "is_active": True,
            "is_test_key": False,
            "usage_count": 0,
            "last_used_at": None,
            "last_used_ip": None,
            "last_used_endpoint": None,
            "created_at": datetime.utcnow(),
            "expires_at": expires_at,
            "revoked_at": None,
            "revoked_reason": None,
            "rotated_from": None,
            "rotated_to": None,
            "rotated_at": None,
            "grace_period_end": None,
            "replaced_by": None,
            "created_by": ObjectId(created_by),
            "notes": description,
        }

        result = collection.insert_one(api_key_doc)
        api_key_id = str(result.inserted_id)

        logger.info("Created organization API key for org %s: %s", organization_id, key_prefix)

        from api.models.audit_log import AuditEventType, AuditLogSeverity
        from api.services.audit_log_service import audit_log_service

        audit_log_service.log_event(
            event_type=AuditEventType.ORGANIZATION_API_KEY_CREATED,
            severity=AuditLogSeverity.MEDIUM,
            message=f"Organization API key created: {key_prefix} for organization {organization_id}",
            success=True,
            user_id=created_by,
            api_key_id=api_key_id,
            organization_id=organization_id,
            details={
                "key_prefix": key_prefix,
                "name": name,
                "expires_at": expires_at.isoformat() if expires_at else None,
            },
            compliance_tags=["PCI-DSS-10", "SOC2"],
        )

        return {
            "api_key": api_key,
            "api_key_id": api_key_id,
            "key_prefix": key_prefix,
            "created_at": api_key_doc["created_at"].isoformat(),
            "expires_at": expires_at.isoformat() if expires_at else None,
        }

    async def list_organization_api_keys(
        self,
        organization_id: str,
        user_id: str,
    ) -> list[dict[str, Any]]:
        """List all API keys for organization.

        **CRITICAL**: Only organization members can list organization API keys.

        Args:
            organization_id: Organization ID
            user_id: User ID (for authorization check)

        Returns:
            List of API key dictionaries

        Raises:
            HTTPException: If user is not organization member
        """
        db = mongodb_manager.get_database()
        collection = db.api_keys

        member = db.organization_members.find_one(
            {
                "organization_id": ObjectId(organization_id),
                "user_id": ObjectId(user_id),
                "status": "active",
            }
        )
        if not member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this organization",
            )

        cursor = collection.find(
            {
                "organization_id": ObjectId(organization_id),
                "is_active": True,
            },
            {
                "key_hash": 0,
            },
        ).sort("created_at", -1)

        keys = []
        for doc in cursor:
            keys.append({
                "api_key_id": str(doc["_id"]),
                "key_prefix": doc.get("key_prefix"),
                "name": doc.get("name"),
                "description": doc.get("description"),
                "is_active": doc.get("is_active", False),
                "created_at": doc.get("created_at").isoformat() if doc.get("created_at") else None,
                "expires_at": doc.get("expires_at").isoformat() if doc.get("expires_at") else None,
                "last_used_at": doc.get("last_used_at").isoformat() if doc.get("last_used_at") else None,
                "usage_count": doc.get("usage_count", 0),
                "created_by": str(doc.get("created_by", "")),
            })

        return keys

    async def revoke_organization_api_key(
        self,
        organization_id: str,
        api_key_id: str,
        user_id: str,
        reason: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> bool:
        """Revoke organization API key.

        **CRITICAL**: Only organization admins and owners can revoke organization API keys.

        Args:
            organization_id: Organization ID
            api_key_id: API key ID
            user_id: User ID (for authorization)
            reason: Revocation reason
            ip_address: IP address of requester
            user_agent: User agent of requester

        Returns:
            True if revoked, False otherwise

        Raises:
            HTTPException: If user is not organization admin/owner
        """
        db = mongodb_manager.get_database()
        collection = db.api_keys

        member = db.organization_members.find_one(
            {
                "organization_id": ObjectId(organization_id),
                "user_id": ObjectId(user_id),
                "status": "active",
            }
        )
        if not member or member.get("role") not in ["owner", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only organization owners and admins can revoke API keys",
            )

        result = collection.update_one(
            {
                "_id": ObjectId(api_key_id),
                "organization_id": ObjectId(organization_id),
            },
            {
                "$set": {
                    "is_active": False,
                    "revoked_at": datetime.utcnow(),
                    "revoked_reason": reason,
                }
            },
        )

        if result.modified_count > 0:
            logger.info("Revoked organization API key %s for org %s", api_key_id, organization_id)

            from api.models.audit_log import AuditEventType, AuditLogSeverity
            from api.services.audit_log_service import audit_log_service

            api_key_doc = collection.find_one({"_id": ObjectId(api_key_id)})

            audit_log_service.log_event(
                event_type=AuditEventType.ORGANIZATION_API_KEY_DELETED,
                severity=AuditLogSeverity.HIGH,
                message=f"Organization API key revoked: {api_key_id} for organization {organization_id}",
                success=True,
                user_id=user_id,
                api_key_id=api_key_id,
                organization_id=organization_id,
                ip_address=ip_address,
                user_agent=user_agent,
                details={
                    "reason": reason,
                    "key_prefix": api_key_doc.get("key_prefix") if api_key_doc else None,
                },
                compliance_tags=["PCI-DSS-10", "SOC2"],
            )

            return True

        return False

    async def verify_organization_api_key(
        self,
        api_key: str,
        user_id: Optional[str] = None,
    ) -> Optional[dict[str, Any]]:
        """Verify organization API key and check user membership.

        Args:
            api_key: API key string
            user_id: Optional user ID to verify membership (if provided)

        Returns:
            Dictionary with organization info if valid, None otherwise
        """
        key_hash = self.hash_api_key(api_key)
        db = mongodb_manager.get_database()
        collection = db.api_keys

        api_key_doc = collection.find_one(
            {
                "key_hash": key_hash,
                "is_active": True,
                "organization_id": {"$ne": None},
            }
        )

        if not api_key_doc:
            return None

        if api_key_doc.get("revoked_at"):
            return None

        expires_at = api_key_doc.get("expires_at")
        if expires_at and expires_at < datetime.utcnow():
            return None

        organization_id = str(api_key_doc["organization_id"])

        if user_id:
            member = db.organization_members.find_one(
                {
                    "organization_id": ObjectId(organization_id),
                    "user_id": ObjectId(user_id),
                    "status": "active",
                }
            )
            if not member:
                logger.warning("User %s is not a member of organization %s", user_id, organization_id)
                return None

        org = db.organizations.find_one({"_id": ObjectId(organization_id)})
        if not org:
            logger.warning("Organization not found for API key: %s", organization_id)
            return None

        plan_id = org.get("plan_id", "team")
        from api.services.plan_service import plan_service

        plan = plan_service.get_plan(plan_id)
        rate_limits = plan.limits.requests_per_minute if plan else 60

        return {
            "organization_id": organization_id,
            "api_key_id": str(api_key_doc["_id"]),
            "plan": plan_id,
            "rate_limits": rate_limits,
            "scopes": api_key_doc.get("scopes"),
            "allowed_models": api_key_doc.get("allowed_models"),
        }


api_key_manager = APIKeyManager()


async def verify_api_key(api_key: str) -> bool:
    """Verify API key (legacy function for compatibility).

    Args:
        api_key: API key string

    Returns:
        True if valid, False otherwise
    """
    result = await api_key_manager.verify_api_key(api_key)
    return result is not None


async def get_user_from_api_key(api_key: str) -> Optional[dict[str, Any]]:
    """Get user information from API key.

    Args:
        api_key: API key string

    Returns:
        Dictionary with user info if valid, None otherwise
    """
    return await api_key_manager.verify_api_key(api_key)
