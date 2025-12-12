"""Admin invitation service."""

import logging
import secrets
import uuid
from datetime import datetime, timedelta
from typing import Any, Optional

from bson import ObjectId

from api.database.mongodb import mongodb_manager
from api.models.admin.rbac import (
    AdminInvitationAcceptRequest,
    AdminInvitationCreateRequest,
    AdminInvitationListResponse,
    AdminInvitationResponse,
    ADMIN_ROLES,
    VALID_ADMIN_ROLES,
)
from api.models.audit_log import AuditEventType, AuditLogSeverity
from api.services.audit_log_service import audit_log_service
from api.exceptions import ValidationError, NotFoundError

logger = logging.getLogger(__name__)


class AdminInvitationService:
    """Service for managing admin invitations."""

    def __init__(self):
        """Initialize invitation service."""
        self.db = mongodb_manager.get_database()
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        """Ensure admin_invitations collection exists with indexes."""
        collection_name = "admin_invitations"
        if collection_name not in self.db.list_collection_names():
            self.db.create_collection(collection_name)
            logger.info("Created collection: %s", collection_name)

        collection = self.db[collection_name]

        indexes = [
            [("token", 1)],
            [("email", 1)],
            [("status", 1), ("expires_at", 1)],
            [("invited_by", 1), ("created_at", -1)],
            [("created_at", -1)],
        ]

        existing_indexes = collection.list_indexes()
        existing_index_names = [idx["name"] for idx in existing_indexes]

        for index_spec in indexes:
            index_name = "_".join([f"{field}_{direction}" for field, direction in index_spec])
            if index_name not in existing_index_names:
                try:
                    collection.create_index(index_spec, name=index_name, background=True)
                    logger.debug("Created index: %s", index_name)
                except Exception as e:
                    logger.warning("Failed to create index %s: %s", index_name, e)

    def _generate_invitation_token(self) -> str:
        """Generate secure invitation token.

        Returns:
            Secure token string
        """
        return f"wistx_inv_{uuid.uuid4().hex}_{secrets.token_urlsafe(16)}"

    async def create_invitation(
        self, request: AdminInvitationCreateRequest, invited_by: str, admin_email: str
    ) -> AdminInvitationResponse:
        """Create admin invitation.

        Args:
            request: Invitation creation request
            invited_by: Admin user ID who is creating invitation
            admin_email: Admin email who is creating invitation

        Returns:
            Created invitation response

        Raises:
            ValueError: If email already has pending invitation or is already admin
        """
        collection = self.db.admin_invitations
        users_collection = self.db.users

        email_lower = request.email.lower()

        existing_user = users_collection.find_one({"email": email_lower})
        if existing_user:
            admin_role = existing_user.get("admin_role")
            admin_status = existing_user.get("admin_status")
            if admin_role and admin_status == "active":
                raise ValidationError(
                    message=f"User {request.email} is already an admin",
                    user_message=f"User {request.email} is already an admin",
                    error_code="USER_ALREADY_ADMIN",
                    details={"email": request.email}
                )

        existing_invitation = collection.find_one(
            {
                "email": email_lower,
                "status": "pending",
                "expires_at": {"$gt": datetime.utcnow()},
            }
        )

        if existing_invitation:
            raise ValidationError(
                message=f"Pending invitation already exists for {request.email}",
                user_message=f"Pending invitation already exists for {request.email}",
                error_code="PENDING_INVITATION_EXISTS",
                details={"email": request.email}
            )

        token = self._generate_invitation_token()
        expires_at = datetime.utcnow() + timedelta(days=request.expires_in_days)

        role_permissions = ADMIN_ROLES.get(request.role, [])
        final_permissions = request.permissions or role_permissions

        invitation_doc = {
            "email": email_lower,
            "invited_by": ObjectId(invited_by),
            "role": request.role,
            "permissions": final_permissions,
            "token": token,
            "expires_at": expires_at,
            "accepted_at": None,
            "accepted_by": None,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        result = collection.insert_one(invitation_doc)
        invitation_id = str(result.inserted_id)

        logger.info("Admin invitation created for %s by %s", request.email, admin_email)

        try:
            from api.services.email import email_service
            from api.config import settings
            from datetime import datetime

            frontend_url = (
                settings.oauth_frontend_redirect_url_prod.replace("/auth/callback/{provider}", "")
                if not settings.debug
                else settings.oauth_frontend_redirect_url_dev.replace("/auth/callback/{provider}", "")
            )
            invitation_url = f"{frontend_url}/admin/invitations/accept?token={token}"

            permissions_str = ", ".join(final_permissions) if final_permissions else "None"

            await email_service.send_template(
                template_name="admin_invitation",
                to=request.email,
                subject=f"Admin Invitation - {request.role} Role",
                context={
                    "invited_by_name": admin_email.split("@")[0] if admin_email else "Admin",
                    "role": request.role,
                    "permissions": permissions_str,
                    "expires_at": expires_at.strftime("%B %d, %Y at %I:%M %p UTC"),
                    "invitation_url": invitation_url,
                    "invited_email": request.email,
                    "current_year": datetime.now().year,
                },
                tags=["admin_invitation", "admin"],
            )
            logger.info("Admin invitation email sent to %s", request.email)
        except Exception as e:
            logger.warning("Failed to send admin invitation email to %s: %s", request.email, e)

        audit_log_service.log_event(
            event_type=AuditEventType.ROLE_ASSIGNED,
            severity=AuditLogSeverity.MEDIUM,
            message=f"Admin invitation created for {request.email} with role {request.role}",
            success=True,
            user_id=invited_by,
            endpoint="/admin/invitations",
            method="POST",
            status_code=201,
            details={
                "invitation_id": invitation_id,
                "invited_email": request.email,
                "role": request.role,
                "permissions": final_permissions,
                "expires_at": expires_at.isoformat(),
                "admin_email": admin_email,
            },
            compliance_tags=["SOC2", "PCI-DSS-10"],
        )

        return AdminInvitationResponse(
            invitation_id=invitation_id,
            email=request.email,
            role=request.role,
            permissions=final_permissions,
            token=token,
            expires_at=expires_at,
            status="pending",
            invited_by=invited_by,
            invited_by_email=admin_email,
            accepted_at=None,
            accepted_by=None,
            created_at=invitation_doc["created_at"],
            updated_at=invitation_doc["updated_at"],
        )

    async def list_invitations(
        self, limit: int = 50, offset: int = 0, status: Optional[str] = None
    ) -> AdminInvitationListResponse:
        """List admin invitations.

        Args:
            limit: Maximum number of results
            offset: Result offset
            status: Filter by status

        Returns:
            Invitation list response
        """
        collection = self.db.admin_invitations

        filter_query: dict[str, Any] = {}
        if status:
            filter_query["status"] = status

        cursor = collection.find(filter_query).sort("created_at", -1).skip(offset).limit(limit)

        invitations = []
        for doc in cursor:
            invited_by_doc = self.db.users.find_one({"_id": doc["invited_by"]})
            invited_by_email = invited_by_doc.get("email") if invited_by_doc else None

            accepted_by_email = None
            if doc.get("accepted_by"):
                accepted_by_doc = self.db.users.find_one({"_id": doc["accepted_by"]})
                accepted_by_email = accepted_by_doc.get("email") if accepted_by_doc else None

            invitations.append(
                AdminInvitationResponse(
                    invitation_id=str(doc["_id"]),
                    email=doc["email"],
                    role=doc["role"],
                    permissions=doc.get("permissions", []),
                    token=doc["token"],
                    expires_at=doc["expires_at"],
                    status=doc["status"],
                    invited_by=str(doc["invited_by"]),
                    invited_by_email=invited_by_email,
                    accepted_at=doc.get("accepted_at"),
                    accepted_by=str(doc["accepted_by"]) if doc.get("accepted_by") else None,
                    created_at=doc["created_at"],
                    updated_at=doc.get("updated_at", doc["created_at"]),
                )
            )

        total = collection.count_documents(filter_query)

        return AdminInvitationListResponse(
            invitations=invitations,
            total=total,
            limit=limit,
            offset=offset,
        )

    async def get_invitation(self, invitation_id: str) -> AdminInvitationResponse:
        """Get invitation by ID.

        Args:
            invitation_id: Invitation ID

        Returns:
            Invitation response

        Raises:
            ValueError: If invitation not found
        """
        collection = self.db.admin_invitations

        doc = collection.find_one({"_id": ObjectId(invitation_id)})
        if not doc:
            raise ValueError(f"Invitation not found: {invitation_id}")

        invited_by_doc = self.db.users.find_one({"_id": doc["invited_by"]})
        invited_by_email = invited_by_doc.get("email") if invited_by_doc else None

        accepted_by_email = None
        if doc.get("accepted_by"):
            accepted_by_doc = self.db.users.find_one({"_id": doc["accepted_by"]})
            accepted_by_email = accepted_by_doc.get("email") if accepted_by_doc else None

        return AdminInvitationResponse(
            invitation_id=str(doc["_id"]),
            email=doc["email"],
            role=doc["role"],
            permissions=doc.get("permissions", []),
            token=doc["token"],
            expires_at=doc["expires_at"],
            status=doc["status"],
            invited_by=str(doc["invited_by"]),
            invited_by_email=invited_by_email,
            accepted_at=doc.get("accepted_at"),
            accepted_by=str(doc["accepted_by"]) if doc.get("accepted_by") else None,
            created_at=doc["created_at"],
            updated_at=doc.get("updated_at", doc["created_at"]),
        )

    async def get_invitation_by_token(self, token: str) -> AdminInvitationResponse:
        """Get invitation by token.

        Args:
            token: Invitation token

        Returns:
            Invitation response

        Raises:
            ValueError: If invitation not found or expired
        """
        collection = self.db.admin_invitations

        doc = collection.find_one({"token": token})
        if not doc:
            raise ValidationError(
                message="Invalid invitation token",
                user_message="Invalid invitation token. Please check your invitation link.",
                error_code="INVALID_INVITATION_TOKEN",
                details={"token_prefix": token[:8] if token else None}
            )

        if doc["status"] != "pending":
            raise ValidationError(
                message=f"Invitation status is {doc['status']}, cannot be accepted",
                user_message=f"Invitation status is {doc['status']}, cannot be accepted",
                error_code="INVITATION_NOT_PENDING",
                details={"status": doc["status"]}
            )

        if doc["expires_at"] < datetime.utcnow():
            collection.update_one({"_id": doc["_id"]}, {"$set": {"status": "expired", "updated_at": datetime.utcnow()}})
            raise ValidationError(
                message="Invitation has expired",
                user_message="This invitation has expired. Please request a new invitation.",
                error_code="INVITATION_EXPIRED",
                details={"expires_at": doc["expires_at"].isoformat() if doc.get("expires_at") else None}
            )

        invited_by_doc = self.db.users.find_one({"_id": doc["invited_by"]})
        invited_by_email = invited_by_doc.get("email") if invited_by_doc else None

        return AdminInvitationResponse(
            invitation_id=str(doc["_id"]),
            email=doc["email"],
            role=doc["role"],
            permissions=doc.get("permissions", []),
            token=doc["token"],
            expires_at=doc["expires_at"],
            status=doc["status"],
            invited_by=str(doc["invited_by"]),
            invited_by_email=invited_by_email,
            accepted_at=doc.get("accepted_at"),
            accepted_by=str(doc["accepted_by"]) if doc.get("accepted_by") else None,
            created_at=doc["created_at"],
            updated_at=doc.get("updated_at", doc["created_at"]),
        )

    async def accept_invitation(self, token: str, user_id: str) -> AdminInvitationResponse:
        """Accept admin invitation.

        Args:
            token: Invitation token
            user_id: User ID accepting invitation

        Returns:
            Updated invitation response

        Raises:
            ValueError: If invitation not found, expired, or email mismatch
        """
        collection = self.db.admin_invitations
        users_collection = self.db.users

        invitation = await self.get_invitation_by_token(token)

        user_doc = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user_doc:
            raise ValueError(f"User not found: {user_id}")

        user_email = user_doc.get("email", "").lower()
        if user_email != invitation.email.lower():
            raise ValueError(f"Invitation email ({invitation.email}) does not match user email ({user_email})")

        if user_doc.get("admin_role") and user_doc.get("admin_status") == "active":
            raise ValueError("User is already an admin")

        role_permissions = ADMIN_ROLES.get(invitation.role, [])
        final_permissions = invitation.permissions or role_permissions

        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "admin_role": invitation.role,
                    "admin_permissions": final_permissions,
                    "admin_status": "active",
                    "admin_invited_by": ObjectId(invitation.invited_by),
                    "admin_invited_at": datetime.utcnow(),
                    "plan": "enterprise",
                    "updated_at": datetime.utcnow(),
                }
            },
        )

        collection.update_one(
            {"_id": ObjectId(invitation.invitation_id)},
            {
                "$set": {
                    "status": "accepted",
                    "accepted_at": datetime.utcnow(),
                    "accepted_by": ObjectId(user_id),
                    "updated_at": datetime.utcnow(),
                }
            },
        )

        logger.info("Admin invitation accepted by user %s (%s)", user_id, user_email)

        audit_log_service.log_event(
            event_type=AuditEventType.ROLE_ASSIGNED,
            severity=AuditLogSeverity.MEDIUM,
            message=f"Admin invitation accepted by {user_email} with role {invitation.role}",
            success=True,
            user_id=user_id,
            endpoint="/admin/invitations/accept",
            method="POST",
            status_code=200,
            details={
                "invitation_id": invitation.invitation_id,
                "role": invitation.role,
                "permissions": final_permissions,
                "invited_by": invitation.invited_by,
            },
            compliance_tags=["SOC2", "PCI-DSS-10"],
        )

        return await self.get_invitation(invitation.invitation_id)

    async def revoke_invitation(self, invitation_id: str, revoked_by: str, admin_email: str) -> None:
        """Revoke admin invitation.

        Args:
            invitation_id: Invitation ID
            revoked_by: Admin user ID revoking invitation
            admin_email: Admin email revoking invitation

        Raises:
            ValueError: If invitation not found or already accepted
        """
        collection = self.db.admin_invitations

        doc = collection.find_one({"_id": ObjectId(invitation_id)})
        if not doc:
            raise ValueError(f"Invitation not found: {invitation_id}")

        if doc["status"] == "accepted":
            raise ValueError("Cannot revoke accepted invitation")

        collection.update_one(
            {"_id": ObjectId(invitation_id)},
            {
                "$set": {
                    "status": "revoked",
                    "updated_at": datetime.utcnow(),
                }
            },
        )

        logger.info("Admin invitation revoked: %s by %s", invitation_id, admin_email)

        audit_log_service.log_event(
            event_type=AuditEventType.ROLE_REVOKED,
            severity=AuditLogSeverity.MEDIUM,
            message=f"Admin invitation revoked for {doc['email']}",
            success=True,
            user_id=revoked_by,
            endpoint=f"/admin/invitations/{invitation_id}",
            method="DELETE",
            status_code=200,
            details={
                "invitation_id": invitation_id,
                "invited_email": doc["email"],
                "admin_email": admin_email,
            },
            compliance_tags=["SOC2", "PCI-DSS-10"],
        )


admin_invitation_service = AdminInvitationService()

