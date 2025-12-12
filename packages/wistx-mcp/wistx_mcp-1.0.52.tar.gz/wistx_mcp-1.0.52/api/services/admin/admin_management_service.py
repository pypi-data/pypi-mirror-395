"""Admin management service."""

import logging
from datetime import datetime
from typing import Any

from bson import ObjectId

from api.database.mongodb import mongodb_manager
from api.models.admin.rbac import (
    AdminInfoResponse,
    AdminListResponse,
    AdminPermissionsUpdateRequest,
    AdminRoleUpdateRequest,
    ADMIN_ROLES,
)
from api.models.audit_log import AuditEventType, AuditLogSeverity
from api.services.audit_log_service import audit_log_service
from api.exceptions import NotFoundError, ValidationError, AuthorizationError

logger = logging.getLogger(__name__)


class AdminManagementService:
    """Service for managing admins."""

    async def list_admins(
        self,
        limit: int = 50,
        offset: int = 0,
        role: str | None = None,
        status: str | None = None,
        show_internal_only: bool = False,
    ) -> AdminListResponse:
        """List all admins.

        Args:
            limit: Maximum number of results
            offset: Result offset
            role: Filter by role
            status: Filter by status
            show_internal_only: If True, show only @wistx.ai users

        Returns:
            Admin list response
        """
        from api.auth.admin import ADMIN_DOMAIN

        db = mongodb_manager.get_database()
        collection = db.users

        if show_internal_only:
            filter_query: dict[str, Any] = {
                "email": {"$regex": f".*{ADMIN_DOMAIN.replace('@', '')}$", "$options": "i"}
            }
        else:
            filter_query: dict[str, Any] = {
                "$or": [
                    {"admin_role": {"$exists": True, "$ne": None}},
                    {"is_super_admin": True},
                ]
            }

        if role:
            filter_query["admin_role"] = role

        if status:
            filter_query["admin_status"] = status

        cursor = collection.find(filter_query).sort("created_at", -1).skip(offset).limit(limit)

        admins = []
        for doc in cursor:
            invited_by_email = None
            if doc.get("admin_invited_by"):
                invited_by_doc = db.users.find_one({"_id": doc["admin_invited_by"]})
                invited_by_email = invited_by_doc.get("email") if invited_by_doc else None

            admins.append(
                AdminInfoResponse(
                    user_id=str(doc["_id"]),
                    email=doc.get("email", ""),
                    full_name=doc.get("full_name"),
                    admin_role=doc.get("admin_role"),
                    admin_permissions=doc.get("admin_permissions", []),
                    is_super_admin=doc.get("is_super_admin", False),
                    admin_status=doc.get("admin_status"),
                    admin_invited_by=str(doc["admin_invited_by"]) if doc.get("admin_invited_by") else None,
                    admin_invited_at=doc.get("admin_invited_at"),
                    created_at=doc.get("created_at"),
                )
            )

        total = collection.count_documents(filter_query)

        return AdminListResponse(
            admins=admins,
            total=total,
            limit=limit,
            offset=offset,
        )

    async def get_admin(self, user_id: str) -> AdminInfoResponse:
        """Get admin by user ID.

        Args:
            user_id: User ID

        Returns:
            Admin info response

        Raises:
            ValueError: If admin not found
        """
        db = mongodb_manager.get_database()
        collection = db.users

        doc = collection.find_one({"_id": ObjectId(user_id)})
        if not doc:
            raise NotFoundError(
                message=f"User not found: {user_id}",
                user_message="User not found",
                error_code="USER_NOT_FOUND",
                details={"user_id": user_id}
            )

        admin_role = doc.get("admin_role")
        is_super_admin = doc.get("is_super_admin", False)

        if not admin_role and not is_super_admin:
            raise AuthorizationError(
                message=f"User {user_id} is not an admin",
                user_message="User is not an admin",
                error_code="NOT_AN_ADMIN",
                details={"user_id": user_id}
            )

        invited_by_email = None
        if doc.get("admin_invited_by"):
            invited_by_doc = db.users.find_one({"_id": doc["admin_invited_by"]})
            invited_by_email = invited_by_doc.get("email") if invited_by_doc else None

        return AdminInfoResponse(
            user_id=str(doc["_id"]),
            email=doc.get("email", ""),
            full_name=doc.get("full_name"),
            admin_role=admin_role,
            admin_permissions=doc.get("admin_permissions", []),
            is_super_admin=is_super_admin,
            admin_status=doc.get("admin_status"),
            admin_invited_by=str(doc["admin_invited_by"]) if doc.get("admin_invited_by") else None,
            admin_invited_at=doc.get("admin_invited_at"),
            created_at=doc.get("created_at"),
        )

    async def update_admin_role(
        self, user_id: str, request: AdminRoleUpdateRequest, updated_by: str, admin_email: str
    ) -> AdminInfoResponse:
        """Update admin role.

        Args:
            user_id: User ID
            request: Role update request
            updated_by: Admin user ID updating role
            admin_email: Admin email updating role

        Returns:
            Updated admin info response

        Raises:
            ValueError: If admin not found
        """
        db = mongodb_manager.get_database()
        collection = db.users

        doc = collection.find_one({"_id": ObjectId(user_id)})
        if not doc:
            raise NotFoundError(
                message=f"User not found: {user_id}",
                user_message="User not found",
                error_code="USER_NOT_FOUND",
                details={"user_id": user_id}
            )

        if doc.get("is_super_admin"):
            raise ValidationError(
                message="Cannot change role of super admin",
                user_message="Cannot change the role of a super admin",
                error_code="CANNOT_CHANGE_SUPER_ADMIN_ROLE",
                details={"user_id": user_id}
            )

        old_role = doc.get("admin_role")
        role_permissions = ADMIN_ROLES.get(request.role, [])

        collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "admin_role": request.role,
                    "admin_permissions": role_permissions,
                    "plan": "enterprise",
                    "updated_at": datetime.utcnow(),
                }
            },
        )

        logger.info("Admin role updated for user %s: %s -> %s by %s", user_id, old_role, request.role, admin_email)

        audit_log_service.log_event(
            event_type=AuditEventType.ROLE_ASSIGNED,
            severity=AuditLogSeverity.HIGH,
            message=f"Admin role updated for user {user_id}: {old_role} -> {request.role}",
            success=True,
            user_id=updated_by,
            endpoint=f"/admin/admins/{user_id}/role",
            method="PATCH",
            status_code=200,
            details={
                "target_user_id": user_id,
                "target_user_email": doc.get("email"),
                "old_role": old_role,
                "new_role": request.role,
                "admin_email": admin_email,
            },
            compliance_tags=["SOC2", "PCI-DSS-10"],
        )

        return await self.get_admin(user_id)

    async def update_admin_permissions(
        self, user_id: str, request: AdminPermissionsUpdateRequest, updated_by: str, admin_email: str
    ) -> AdminInfoResponse:
        """Update admin permissions.

        Args:
            user_id: User ID
            request: Permissions update request
            updated_by: Admin user ID updating permissions
            admin_email: Admin email updating permissions

        Returns:
            Updated admin info response

        Raises:
            ValueError: If admin not found
        """
        db = mongodb_manager.get_database()
        collection = db.users

        doc = collection.find_one({"_id": ObjectId(user_id)})
        if not doc:
            raise NotFoundError(
                message=f"User not found: {user_id}",
                user_message="User not found",
                error_code="USER_NOT_FOUND",
                details={"user_id": user_id}
            )

        if doc.get("is_super_admin"):
            raise ValidationError(
                message="Cannot change permissions of super admin",
                user_message="Cannot change the permissions of a super admin",
                error_code="CANNOT_CHANGE_SUPER_ADMIN_PERMISSIONS",
                details={"user_id": user_id}
            )

        old_permissions = doc.get("admin_permissions", [])

        collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "admin_permissions": request.permissions,
                    "plan": "enterprise",
                    "updated_at": datetime.utcnow(),
                }
            },
        )

        logger.info("Admin permissions updated for user %s by %s", user_id, admin_email)

        audit_log_service.log_event(
            event_type=AuditEventType.PERMISSION_CHANGED,
            severity=AuditLogSeverity.HIGH,
            message=f"Admin permissions updated for user {user_id}",
            success=True,
            user_id=updated_by,
            endpoint=f"/admin/admins/{user_id}/permissions",
            method="PATCH",
            status_code=200,
            details={
                "target_user_id": user_id,
                "target_user_email": doc.get("email"),
                "old_permissions": old_permissions,
                "new_permissions": request.permissions,
                "admin_email": admin_email,
            },
            compliance_tags=["SOC2", "PCI-DSS-10"],
        )

        return await self.get_admin(user_id)

    async def suspend_admin(self, user_id: str, suspended_by: str, admin_email: str) -> AdminInfoResponse:
        """Suspend admin.

        Args:
            user_id: User ID
            suspended_by: Admin user ID suspending admin
            admin_email: Admin email suspending admin

        Returns:
            Updated admin info response

        Raises:
            ValueError: If admin not found
        """
        db = mongodb_manager.get_database()
        collection = db.users

        doc = collection.find_one({"_id": ObjectId(user_id)})
        if not doc:
            raise ValueError(f"User not found: {user_id}")

        if doc.get("is_super_admin"):
            raise ValueError("Cannot suspend super admin")

        collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "admin_status": "suspended",
                    "updated_at": datetime.utcnow(),
                }
            },
        )

        logger.warning("Admin suspended: %s by %s", user_id, admin_email)

        audit_log_service.log_event(
            event_type=AuditEventType.ROLE_REVOKED,
            severity=AuditLogSeverity.CRITICAL,
            message=f"Admin suspended: {user_id}",
            success=True,
            user_id=suspended_by,
            endpoint=f"/admin/admins/{user_id}/suspend",
            method="POST",
            status_code=200,
            details={
                "target_user_id": user_id,
                "target_user_email": doc.get("email"),
                "admin_email": admin_email,
            },
            compliance_tags=["SOC2", "PCI-DSS-10"],
        )

        return await self.get_admin(user_id)

    async def activate_admin(self, user_id: str, activated_by: str, admin_email: str) -> AdminInfoResponse:
        """Activate suspended admin.

        Args:
            user_id: User ID
            activated_by: Admin user ID activating admin
            admin_email: Admin email activating admin

        Returns:
            Updated admin info response

        Raises:
            ValueError: If admin not found
        """
        db = mongodb_manager.get_database()
        collection = db.users

        doc = collection.find_one({"_id": ObjectId(user_id)})
        if not doc:
            raise ValueError(f"User not found: {user_id}")

        collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "admin_status": "active",
                    "updated_at": datetime.utcnow(),
                }
            },
        )

        logger.info("Admin activated: %s by %s", user_id, admin_email)

        audit_log_service.log_event(
            event_type=AuditEventType.ROLE_ASSIGNED,
            severity=AuditLogSeverity.MEDIUM,
            message=f"Admin activated: {user_id}",
            success=True,
            user_id=activated_by,
            endpoint=f"/admin/admins/{user_id}/activate",
            method="POST",
            status_code=200,
            details={
                "target_user_id": user_id,
                "target_user_email": doc.get("email"),
                "admin_email": admin_email,
            },
            compliance_tags=["SOC2", "PCI-DSS-10"],
        )

        return await self.get_admin(user_id)

    async def remove_admin(self, user_id: str, removed_by: str, admin_email: str) -> None:
        """Remove admin (super admin only).

        Args:
            user_id: User ID
            removed_by: Super admin user ID removing admin
            admin_email: Super admin email removing admin

        Raises:
            ValueError: If admin not found or is super admin
        """
        db = mongodb_manager.get_database()
        collection = db.users

        doc = collection.find_one({"_id": ObjectId(user_id)})
        if not doc:
            raise ValueError(f"User not found: {user_id}")

        if doc.get("is_super_admin"):
            raise ValueError("Cannot remove super admin")

        collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "admin_role": None,
                    "admin_permissions": [],
                    "admin_status": None,
                    "admin_invited_by": None,
                    "admin_invited_at": None,
                    "updated_at": datetime.utcnow(),
                },
                "$unset": {
                    "is_super_admin": "",
                },
            },
        )

        logger.warning("Admin removed: %s by %s", user_id, admin_email)

        audit_log_service.log_event(
            event_type=AuditEventType.ROLE_REVOKED,
            severity=AuditLogSeverity.CRITICAL,
            message=f"Admin removed: {user_id}",
            success=True,
            user_id=removed_by,
            endpoint=f"/admin/admins/{user_id}",
            method="DELETE",
            status_code=204,
            details={
                "target_user_id": user_id,
                "target_user_email": doc.get("email"),
                "admin_email": admin_email,
            },
            compliance_tags=["SOC2", "PCI-DSS-10"],
        )


admin_management_service = AdminManagementService()

