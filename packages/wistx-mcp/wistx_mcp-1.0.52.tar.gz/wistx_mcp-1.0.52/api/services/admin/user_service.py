"""Admin user management service."""

import logging
from datetime import datetime
from typing import Any, Optional

from bson import ObjectId

from api.database.mongodb import mongodb_manager
from api.models.admin.user_management import (
    AdminUserResponse,
    UserListQuery,
    UserListResponse,
    UserStatsResponse,
    UserSuspendRequest,
    UserUpdateRequest,
)
from api.auth.admin import is_internal_admin
from api.models.audit_log import AuditEventType, AuditLogSeverity
from api.services.audit_log_service import audit_log_service

logger = logging.getLogger(__name__)


class AdminUserService:
    """Service for admin user management operations."""

    async def list_users(self, query: UserListQuery) -> UserListResponse:
        """List users with filters and pagination.

        Args:
            query: Query parameters

        Returns:
            User list response
        """
        db = mongodb_manager.get_database()
        collection = db.users

        filter_query: dict[str, Any] = {}

        if query.search:
            search_term = query.search.lower()
            or_conditions = [
                {"email": {"$regex": search_term, "$options": "i"}},
                {"full_name": {"$regex": search_term, "$options": "i"}},
            ]
            if ObjectId.is_valid(query.search):
                or_conditions.append({"_id": ObjectId(query.search)})
            filter_query["$or"] = or_conditions

        if query.plan:
            filter_query["plan"] = query.plan

        if query.is_active is not None:
            filter_query["is_active"] = query.is_active

        if query.is_verified is not None:
            filter_query["is_verified"] = query.is_verified

        if query.profile_completed is not None:
            filter_query["profile_completed"] = query.profile_completed

        if query.organization_id:
            filter_query["organization_id"] = ObjectId(query.organization_id)

        if query.start_date or query.end_date:
            filter_query["created_at"] = {}
            if query.start_date:
                filter_query["created_at"]["$gte"] = query.start_date
            if query.end_date:
                filter_query["created_at"]["$lte"] = query.end_date

        sort_direction = -1 if query.sort_order == "desc" else 1
        sort_field = query.sort_by if query.sort_by in ["created_at", "email", "plan", "updated_at"] else "created_at"

        cursor = (
            collection.find(filter_query)
            .sort(sort_field, sort_direction)
            .skip(query.offset)
            .limit(query.limit)
        )

        users = []
        for user_doc in cursor:
            users.append(await self._user_doc_to_admin_response(user_doc))

        total = collection.count_documents(filter_query)

        return UserListResponse(
            users=users,
            total=total,
            limit=query.limit,
            offset=query.offset,
        )

    async def get_user(self, user_id: str) -> AdminUserResponse:
        """Get user details.

        Args:
            user_id: User ID

        Returns:
            Admin user response

        Raises:
            ValueError: If user not found
        """
        db = mongodb_manager.get_database()
        collection = db.users

        from api.exceptions import NotFoundError
        
        user_doc = collection.find_one({"_id": ObjectId(user_id)})
        if not user_doc:
            raise NotFoundError(
                message=f"User not found: {user_id}",
                user_message="User not found",
                error_code="USER_NOT_FOUND",
                details={"user_id": user_id}
            )

        return await self._user_doc_to_admin_response(user_doc)

    async def update_user(
        self, user_id: str, updates: UserUpdateRequest, admin_user_info: dict[str, Any] | None = None
    ) -> AdminUserResponse:
        """Update user.

        Args:
            user_id: User ID
            updates: Update data
            admin_user_info: Admin user information for audit logging

        Returns:
            Updated admin user response

        Raises:
            ValueError: If user not found
        """
        db = mongodb_manager.get_database()
        collection = db.users

        from api.exceptions import NotFoundError
        
        user_doc = collection.find_one({"_id": ObjectId(user_id)})
        if not user_doc:
            raise NotFoundError(
                message=f"User not found: {user_id}",
                user_message="User not found",
                error_code="USER_NOT_FOUND",
                details={"user_id": user_id}
            )

        old_plan = user_doc.get("plan")
        old_is_active = user_doc.get("is_active", True)
        old_is_verified = user_doc.get("is_verified", False)
        old_role = user_doc.get("role")
        old_full_name = user_doc.get("full_name")
        old_org_id = str(user_doc.get("organization_id")) if user_doc.get("organization_id") else None

        update_data: dict[str, Any] = {"updated_at": datetime.utcnow()}
        changes: list[str] = []

        if updates.plan is not None and updates.plan != old_plan:
            update_data["plan"] = updates.plan
            changes.append(f"plan: {old_plan} -> {updates.plan}")

        if updates.is_active is not None and updates.is_active != old_is_active:
            update_data["is_active"] = updates.is_active
            changes.append(f"is_active: {old_is_active} -> {updates.is_active}")

        if updates.is_verified is not None and updates.is_verified != old_is_verified:
            update_data["is_verified"] = updates.is_verified
            changes.append(f"is_verified: {old_is_verified} -> {updates.is_verified}")

        if updates.full_name is not None and updates.full_name != old_full_name:
            update_data["full_name"] = updates.full_name
            changes.append("full_name updated")

        if updates.role is not None and updates.role != old_role:
            update_data["role"] = updates.role
            changes.append(f"role: {old_role} -> {updates.role}")

        if updates.organization_name is not None:
            update_data["organization_name"] = updates.organization_name
            changes.append("organization_name updated")

        if updates.organization_id is not None:
            new_org_id = updates.organization_id if updates.organization_id else None
            if str(new_org_id) != old_org_id:
                update_data["organization_id"] = ObjectId(updates.organization_id) if updates.organization_id else None
                changes.append(f"organization_id: {old_org_id} -> {new_org_id}")

        collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})

        logger.info("User %s updated by admin", user_id)

        if admin_user_info and changes:
            plan_changed = any("plan:" in change for change in changes)
            event_type = AuditEventType.PLAN_CHANGED if plan_changed else AuditEventType.DATA_MODIFIED

            audit_log_service.log_event(
                event_type=event_type,
                severity=AuditLogSeverity.MEDIUM if plan_changed else AuditLogSeverity.LOW,
                message=f"Admin updated user {user_id}: {', '.join(changes)}",
                success=True,
                user_id=admin_user_info.get("user_id"),
                api_key_id=admin_user_info.get("api_key_id"),
                organization_id=admin_user_info.get("organization_id"),
                endpoint=f"/admin/users/{user_id}",
                method="PATCH",
                status_code=200,
                details={
                    "target_user_id": user_id,
                    "target_user_email": user_doc.get("email"),
                    "changes": changes,
                    "admin_email": admin_user_info.get("email"),
                },
                compliance_tags=["SOC2", "PCI-DSS-10"],
            )

        return await self.get_user(user_id)

    async def suspend_user(
        self, user_id: str, request: UserSuspendRequest, admin_user_info: dict[str, Any] | None = None
    ) -> AdminUserResponse:
        """Suspend user.

        Args:
            user_id: User ID
            request: Suspend request
            admin_user_info: Admin user information for audit logging

        Returns:
            Updated admin user response

        Raises:
            ValueError: If user not found
        """
        db = mongodb_manager.get_database()
        collection = db.users

        from api.exceptions import NotFoundError
        
        user_doc = collection.find_one({"_id": ObjectId(user_id)})
        if not user_doc:
            raise NotFoundError(
                message=f"User not found: {user_id}",
                user_message="User not found",
                error_code="USER_NOT_FOUND",
                details={"user_id": user_id}
            )

        collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "is_active": False,
                    "updated_at": datetime.utcnow(),
                    "suspended_at": datetime.utcnow(),
                    "suspension_reason": request.reason,
                }
            },
        )

        logger.info("User %s suspended by admin: %s", user_id, request.reason)

        if admin_user_info:
            audit_log_service.log_event(
                event_type=AuditEventType.ROLE_REVOKED,
                severity=AuditLogSeverity.HIGH,
                message=f"Admin suspended user {user_id}: {request.reason}",
                success=True,
                user_id=admin_user_info.get("user_id"),
                api_key_id=admin_user_info.get("api_key_id"),
                organization_id=admin_user_info.get("organization_id"),
                endpoint=f"/admin/users/{user_id}/suspend",
                method="POST",
                status_code=200,
                details={
                    "target_user_id": user_id,
                    "target_user_email": user_doc.get("email"),
                    "suspension_reason": request.reason,
                    "admin_email": admin_user_info.get("email"),
                },
                compliance_tags=["SOC2", "PCI-DSS-10"],
            )

        return await self.get_user(user_id)

    async def activate_user(
        self, user_id: str, admin_user_info: dict[str, Any] | None = None
    ) -> AdminUserResponse:
        """Activate suspended user.

        Args:
            user_id: User ID
            admin_user_info: Admin user information for audit logging

        Returns:
            Updated admin user response

        Raises:
            ValueError: If user not found
        """
        db = mongodb_manager.get_database()
        collection = db.users

        from api.exceptions import NotFoundError
        
        user_doc = collection.find_one({"_id": ObjectId(user_id)})
        if not user_doc:
            raise NotFoundError(
                message=f"User not found: {user_id}",
                user_message="User not found",
                error_code="USER_NOT_FOUND",
                details={"user_id": user_id}
            )

        collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "is_active": True,
                    "updated_at": datetime.utcnow(),
                },
                "$unset": {
                    "suspended_at": "",
                    "suspension_reason": "",
                },
            },
        )

        logger.info("User %s activated by admin", user_id)

        if admin_user_info:
            audit_log_service.log_event(
                event_type=AuditEventType.ROLE_ASSIGNED,
                severity=AuditLogSeverity.MEDIUM,
                message=f"Admin activated user {user_id}",
                success=True,
                user_id=admin_user_info.get("user_id"),
                api_key_id=admin_user_info.get("api_key_id"),
                organization_id=admin_user_info.get("organization_id"),
                endpoint=f"/admin/users/{user_id}/activate",
                method="POST",
                status_code=200,
                details={
                    "target_user_id": user_id,
                    "target_user_email": user_doc.get("email"),
                    "admin_email": admin_user_info.get("email"),
                },
                compliance_tags=["SOC2", "PCI-DSS-10"],
            )

        return await self.get_user(user_id)

    async def delete_user(self, user_id: str, admin_user_info: dict[str, Any] | None = None) -> None:
        """Delete user permanently.

        Args:
            user_id: User ID
            admin_user_info: Admin user information for audit logging

        Raises:
            ValueError: If user not found
        """
        db = mongodb_manager.get_database()
        collection = db.users

        from api.exceptions import NotFoundError
        
        user_doc = collection.find_one({"_id": ObjectId(user_id)})
        if not user_doc:
            raise NotFoundError(
                message=f"User not found: {user_id}",
                user_message="User not found",
                error_code="USER_NOT_FOUND",
                details={"user_id": user_id}
            )

        user_email = user_doc.get("email")
        user_plan = user_doc.get("plan")
        user_org_id = str(user_doc.get("organization_id")) if user_doc.get("organization_id") else None

        collection.delete_one({"_id": ObjectId(user_id)})

        logger.warning("User %s deleted by admin", user_id)

        if admin_user_info:
            audit_log_service.log_event(
                event_type=AuditEventType.DATA_DELETED,
                severity=AuditLogSeverity.CRITICAL,
                message=f"Admin deleted user {user_id} ({user_email})",
                success=True,
                user_id=admin_user_info.get("user_id"),
                api_key_id=admin_user_info.get("api_key_id"),
                organization_id=admin_user_info.get("organization_id"),
                endpoint=f"/admin/users/{user_id}",
                method="DELETE",
                status_code=204,
                details={
                    "target_user_id": user_id,
                    "target_user_email": user_email,
                    "target_user_plan": user_plan,
                    "target_user_organization_id": user_org_id,
                    "admin_email": admin_user_info.get("email"),
                },
                compliance_tags=["SOC2", "PCI-DSS-10", "GDPR"],
            )

    async def get_user_stats(self, user_id: str) -> UserStatsResponse:
        """Get user statistics.

        Args:
            user_id: User ID

        Returns:
            User statistics response

        Raises:
            ValueError: If user not found
        """
        db = mongodb_manager.get_database()

        user_doc = db.users.find_one({"_id": ObjectId(user_id)})
        if not user_doc:
            raise ValueError(f"User not found: {user_id}")

        usage_cursor = db.api_usage.find({"user_id": ObjectId(user_id)})
        total_api_requests = usage_cursor.count()

        query_count = db.api_usage.count_documents(
            {"user_id": ObjectId(user_id), "operation_type": "query"}
        )

        indexing_count = db.api_usage.count_documents(
            {"user_id": ObjectId(user_id), "operation_type": "index"}
        )

        resources_cursor = db.indexed_resources.find({"user_id": ObjectId(user_id)})
        storage_mb = sum(resource.get("storage_mb", 0.0) for resource in resources_cursor)

        api_keys_count = db.api_keys.count_documents({"user_id": ObjectId(user_id)})
        active_api_keys_count = db.api_keys.count_documents(
            {"user_id": ObjectId(user_id), "is_active": True}
        )

        return UserStatsResponse(
            user_id=user_id,
            total_api_requests=total_api_requests,
            total_queries=query_count,
            total_indexing_operations=indexing_count,
            storage_mb=storage_mb,
            api_keys_count=api_keys_count,
            active_api_keys_count=active_api_keys_count,
        )

    async def _user_doc_to_admin_response(self, user_doc: dict) -> AdminUserResponse:
        """Convert user document to admin response.

        Args:
            user_doc: User document from MongoDB

        Returns:
            Admin user response
        """
        from api.services.oauth_service import oauth_service

        user_id = str(user_doc["_id"])
        email = user_doc.get("email", "")
        is_admin = is_internal_admin(email)
        github_connected = await oauth_service.has_github_token(user_id)

        organization_id = None
        if user_doc.get("organization_id"):
            organization_id = str(user_doc["organization_id"])

        last_active_doc = mongodb_manager.get_database().api_usage.find_one(
            {"user_id": ObjectId(user_id)}, sort=[("timestamp", -1)]
        )
        last_active_at = last_active_doc.get("timestamp") if last_active_doc else None

        return AdminUserResponse(
            user_id=user_id,
            email=email,
            full_name=user_doc.get("full_name"),
            role=user_doc.get("role"),
            organization_name=user_doc.get("organization_name"),
            organization_id=organization_id,
            plan=user_doc.get("plan", "professional"),
            is_active=user_doc.get("is_active", True),
            is_verified=user_doc.get("is_verified", False),
            is_admin=is_admin,
            profile_completed=user_doc.get("profile_completed", False),
            github_connected=github_connected,
            created_at=user_doc.get("created_at"),
            updated_at=user_doc.get("updated_at"),
            last_active_at=last_active_at,
        )


admin_user_service = AdminUserService()

