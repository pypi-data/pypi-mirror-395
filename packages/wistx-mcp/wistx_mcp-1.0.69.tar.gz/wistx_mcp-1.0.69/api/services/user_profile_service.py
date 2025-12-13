"""User profile management service."""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Optional

from bson import ObjectId

from api.database.mongodb import mongodb_manager
from api.models.user_profile import (
    ProfileCompletionRequest,
    ProfileUpdateRequest,
    UserProfileResponse,
    ProfileCompletionStatusResponse,
)
from api.auth.admin import get_admin_info
from api.exceptions import DatabaseError, NotFoundError, ValidationError

logger = logging.getLogger(__name__)


class UserProfileService:
    """Service for managing user profiles."""

    REQUIRED_FIELDS = ["full_name", "role", "referral_source"]

    async def complete_profile(
        self, user_id: str, profile_data: ProfileCompletionRequest
    ) -> UserProfileResponse:
        """Complete user profile during signup.

        Args:
            user_id: User ID
            profile_data: Profile completion data

        Returns:
            Updated user profile

        Raises:
            ValueError: If user not found or profile already completed
        """
        def find_user_sync():
            db = mongodb_manager.get_database()
            collection = db.users
            return collection.find_one({"_id": ObjectId(user_id)})
        
        loop = asyncio.get_event_loop()
        try:
            user = await asyncio.wait_for(
                loop.run_in_executor(ThreadPoolExecutor(max_workers=1), find_user_sync),
                timeout=3.0
            )
        except asyncio.TimeoutError:
            logger.error("complete_profile: MongoDB query timed out for user: %s", user_id)
            raise DatabaseError(
                message=f"Database query timeout for user: {user_id}",
                user_message="Database operation timed out. Please try again.",
                error_code="DATABASE_TIMEOUT",
                details={"user_id": user_id, "operation": "complete_profile"}
            )
        
        if not user:
            raise NotFoundError(
                message=f"User not found: {user_id}",
                user_message="User not found",
                error_code="USER_NOT_FOUND",
                details={"user_id": user_id}
            )

        if user.get("profile_completed", False):
            logger.warning("Profile already completed for user: %s", user_id)
            raise ValidationError(
                message="Profile already completed",
                user_message="Your profile has already been completed",
                error_code="PROFILE_ALREADY_COMPLETED",
                details={"user_id": user_id}
            )

        update_data = {
            "full_name": profile_data.full_name,
            "role": profile_data.role,
            "organization_name": profile_data.organization_name,
            "referral_source": profile_data.referral_source,
            "profile_completed": True,
            "onboarding_completed": True,
            "updated_at": datetime.utcnow(),
        }

        def update_user_sync():
            db = mongodb_manager.get_database()
            collection = db.users
            collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
        
        try:
            await asyncio.wait_for(
                loop.run_in_executor(ThreadPoolExecutor(max_workers=1), update_user_sync),
                timeout=3.0
            )
        except asyncio.TimeoutError:
            logger.error("complete_profile: MongoDB update timed out for user: %s", user_id)
            raise DatabaseError(
                message=f"Database update timeout for user: {user_id}",
                user_message="Database operation timed out. Please try again.",
                error_code="DATABASE_TIMEOUT",
                details={"user_id": user_id, "operation": "complete_profile_update"}
            )

        logger.info("Profile completed for user: %s", user_id)

        profile = await self.get_profile(user_id)

        if user.get("email"):
            try:
                from api.services.email import email_service
                from api.config import settings

                dashboard_url = "https://wistx.ai/dashboard"

                user_name = profile.full_name or user.get("email", "").split("@")[0] or "there"

                response = await email_service.send_template(
                    template_name="welcome",
                    to=user.get("email"),
                    subject="Welcome to WISTX! Let's get started",
                    context={
                        "user_name": user_name,
                        "user_email": user.get("email"),
                        "dashboard_url": dashboard_url,
                        "current_year": datetime.now().year,
                    },
                    tags=["welcome", "signup"],
                )
                
                if response.success:
                    logger.info("Welcome email sent successfully to %s (provider: %s)", user.get("email"), response.provider.value)
                else:
                    logger.error(
                        "Failed to send welcome email to %s: %s (provider: %s)",
                        user.get("email"),
                        response.error,
                        response.provider.value if response.provider else "unknown",
                    )
            except Exception as e:
                logger.error("Exception sending welcome email to %s: %s", user.get("email"), e, exc_info=True)

        return profile

    async def get_profile(self, user_id: str) -> UserProfileResponse:
        """Get user profile.

        Args:
            user_id: User ID

        Returns:
            User profile

        Raises:
            ValueError: If user not found
        """
        logger.info("get_profile: Starting profile fetch for user: %s", user_id)
        
        def find_user_sync():
            logger.info("get_profile: Starting synchronous MongoDB query for user")
            try:
                db = mongodb_manager.get_database()
                collection = db.users
                user = collection.find_one({"_id": ObjectId(user_id)})
                logger.info("get_profile: Synchronous MongoDB query completed: user=%s", "found" if user else "None")
                return user
            except Exception as e:
                logger.error("get_profile: Failed to fetch user synchronously: %s", e, exc_info=True)
                raise
        
        loop = asyncio.get_event_loop()
        try:
            user = await asyncio.wait_for(
                loop.run_in_executor(ThreadPoolExecutor(max_workers=1), find_user_sync),
                timeout=3.0
            )
        except asyncio.TimeoutError:
            logger.error("get_profile: MongoDB query timed out after 3 seconds for user: %s", user_id)
            raise DatabaseError(
                message=f"Database query timeout for user: {user_id}",
                user_message="Database operation timed out. Please try again.",
                error_code="DATABASE_TIMEOUT",
                details={"user_id": user_id, "operation": "get_profile"}
            )
        except Exception as e:
            logger.error("get_profile: Error during MongoDB query: %s", e, exc_info=True)
            raise DatabaseError(
                message=f"Failed to fetch user: {user_id}",
                user_message="Failed to retrieve profile. Please try again later.",
                error_code="DATABASE_ERROR",
                details={"user_id": user_id, "error": str(e)}
            ) from e
        
        if not user:
            raise NotFoundError(
                message=f"User not found: {user_id}",
                user_message="User not found",
                error_code="USER_NOT_FOUND",
                details={"user_id": user_id}
            )

        organization_id = None
        organization_role = None
        if user.get("organization_id"):
            organization_id = str(user["organization_id"])
            
            def find_member_sync():
                db = mongodb_manager.get_database()
                member = db.organization_members.find_one(
                    {
                        "organization_id": ObjectId(organization_id),
                        "user_id": ObjectId(user_id),
                        "status": "active",
                    }
                )
                return member.get("role") if member else None
            
            loop = asyncio.get_event_loop()
            try:
                member_role = await asyncio.wait_for(
                    loop.run_in_executor(ThreadPoolExecutor(max_workers=1), find_member_sync),
                    timeout=2.0
                )
                if member_role:
                    organization_role = member_role
            except (asyncio.TimeoutError, Exception) as e:
                logger.warning("get_profile: Failed to fetch organization role for user %s: %s", user_id, e)

        from api.services.oauth_service import oauth_service

        logger.info("get_profile: Checking GitHub token status for user: %s", user_id)
        github_connected = await oauth_service.has_github_token(user_id)
        logger.info("get_profile: GitHub token check completed: connected=%s", github_connected)
        
        email = user["email"]
        admin_info = get_admin_info(user)

        logger.info("get_profile: Successfully constructed profile response for user: %s", user_id)
        return UserProfileResponse(
            user_id=str(user["_id"]),
            email=email,
            full_name=user.get("full_name"),
            role=user.get("role"),
            organization_name=user.get("organization_name"),
            organization_id=organization_id,
            organization_role=organization_role,
            referral_source=user.get("referral_source"),
            profile_completed=user.get("profile_completed", False),
            github_connected=github_connected,
            plan=user.get("plan", "professional"),
            is_verified=user.get("is_verified", False),
            is_admin=admin_info["is_admin"],
            is_super_admin=admin_info["is_super_admin"],
            admin_role=admin_info.get("admin_role"),
            admin_status=admin_info.get("admin_status"),
            created_at=user.get("created_at"),
            updated_at=user.get("updated_at"),
        )

    async def update_profile(
        self, user_id: str, updates: ProfileUpdateRequest
    ) -> UserProfileResponse:
        """Update user profile.

        Args:
            user_id: User ID
            updates: Profile update data

        Returns:
            Updated user profile

        Raises:
            ValueError: If user not found
        """
        def find_user_sync():
            db = mongodb_manager.get_database()
            collection = db.users
            return collection.find_one({"_id": ObjectId(user_id)})
        
        loop = asyncio.get_event_loop()
        try:
            user = await asyncio.wait_for(
                loop.run_in_executor(ThreadPoolExecutor(max_workers=1), find_user_sync),
                timeout=3.0
            )
        except asyncio.TimeoutError:
            logger.error("update_profile: MongoDB query timed out for user: %s", user_id)
            raise ValueError(f"Database query timeout for user: {user_id}")
        
        if not user:
            raise ValueError(f"User not found: {user_id}")

        update_data: dict[str, any] = {"updated_at": datetime.utcnow()}

        if updates.full_name is not None:
            update_data["full_name"] = updates.full_name
        if updates.role is not None:
            update_data["role"] = updates.role
        if updates.organization_name is not None:
            update_data["organization_name"] = updates.organization_name
        if updates.referral_source is not None:
            update_data["referral_source"] = updates.referral_source

        if update_data:
            def update_user_sync():
                db = mongodb_manager.get_database()
                collection = db.users
                collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
            
            try:
                await asyncio.wait_for(
                    loop.run_in_executor(ThreadPoolExecutor(max_workers=1), update_user_sync),
                    timeout=3.0
                )
            except asyncio.TimeoutError:
                logger.error("update_profile: MongoDB update timed out for user: %s", user_id)
                raise ValueError(f"Database update timeout for user: {user_id}")
            
            logger.info("Profile updated for user: %s", user_id)

        profile = await self.get_profile(user_id)

        if profile.profile_completed:
            required_fields_present = all(
                [
                    profile.full_name,
                    profile.role,
                    profile.referral_source,
                ]
            )
            if not required_fields_present:
                def update_completion_sync():
                    db = mongodb_manager.get_database()
                    collection = db.users
                    collection.update_one(
                        {"_id": ObjectId(user_id)}, {"$set": {"profile_completed": False}}
                    )
                
                try:
                    await asyncio.wait_for(
                        loop.run_in_executor(ThreadPoolExecutor(max_workers=1), update_completion_sync),
                        timeout=3.0
                    )
                except asyncio.TimeoutError:
                    logger.warning("update_profile: Failed to update profile_completed flag (timeout)")
                
                profile.profile_completed = False

        return profile

    async def check_completion_status(self, user_id: str) -> ProfileCompletionStatusResponse:
        """Check profile completion status.

        Args:
            user_id: User ID

        Returns:
            Profile completion status

        Raises:
            ValueError: If user not found
        """
        def find_user_sync():
            db = mongodb_manager.get_database()
            collection = db.users
            return collection.find_one({"_id": ObjectId(user_id)})
        
        loop = asyncio.get_event_loop()
        try:
            user = await asyncio.wait_for(
                loop.run_in_executor(ThreadPoolExecutor(max_workers=1), find_user_sync),
                timeout=3.0
            )
        except asyncio.TimeoutError:
            logger.error("check_completion_status: MongoDB query timed out for user: %s", user_id)
            raise ValueError(f"Database query timeout for user: {user_id}")
        
        if not user:
            raise ValueError(f"User not found: {user_id}")

        missing_fields: list[str] = []
        completed_fields: list[str] = ["email"]

        for field in self.REQUIRED_FIELDS:
            if not user.get(field):
                missing_fields.append(field)
            else:
                completed_fields.append(field)

        if user.get("organization_name"):
            completed_fields.append("organization_name")

        profile_completed = len(missing_fields) == 0 and user.get("profile_completed", False)

        return ProfileCompletionStatusResponse(
            profile_completed=profile_completed,
            missing_fields=missing_fields,
            completed_fields=completed_fields,
        )


user_profile_service = UserProfileService()

