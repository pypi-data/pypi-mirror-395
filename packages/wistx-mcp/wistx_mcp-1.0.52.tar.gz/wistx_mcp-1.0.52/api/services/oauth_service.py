"""OAuth token management service for GitHub integration."""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from typing import Any, Optional
from bson import ObjectId

from api.database.mongodb import mongodb_manager
from api.services.indexing_service import indexing_service
from api.exceptions import DatabaseError

logger = logging.getLogger(__name__)


class OAuthService:
    """Service for managing OAuth tokens."""

    async def store_github_token(
        self,
        user_id: str,
        access_token: str,
        refresh_token: Optional[str] = None,
        expires_in: Optional[int] = None,
        scope: str = "repo",
    ) -> None:
        """Store GitHub OAuth token for user.

        Args:
            user_id: User ID
            access_token: OAuth access token
            refresh_token: OAuth refresh token (if available)
            expires_in: Token expiration time in seconds
            scope: Token scopes
        """
        expires_at = None
        if expires_in:
            expires_at = datetime.utcnow() + timedelta(seconds=expires_in)

        from api.services.token_encryption_service import TokenEncryptionService

        encrypted_access_token = TokenEncryptionService.encrypt_token(access_token, user_id)
        encrypted_refresh_token = None
        if refresh_token:
            encrypted_refresh_token = TokenEncryptionService.encrypt_token(refresh_token, user_id)

        token_data = {
            "access_token": encrypted_access_token,
            "refresh_token": encrypted_refresh_token,
            "token_type": "bearer",
            "expires_at": expires_at,
            "scope": scope,
            "organizations": [],
            "selected_organizations": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        def update_user_sync():
            db = mongodb_manager.get_database()
            collection = db.users
            collection.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$set": {
                        "github_oauth_token": token_data,
                        "github_connected": True,
                        "updated_at": datetime.utcnow(),
                    }
                },
            )
        
        loop = asyncio.get_event_loop()
        try:
            await asyncio.wait_for(
                loop.run_in_executor(ThreadPoolExecutor(max_workers=1), update_user_sync),
                timeout=3.0
            )
        except asyncio.TimeoutError:
            logger.error("store_github_token: MongoDB update timed out for user: %s", user_id)
            raise DatabaseError(
                message=f"Database update timeout for user: {user_id}",
                user_message="Database operation timed out. Please try again.",
                error_code="DATABASE_TIMEOUT",
                details={"user_id": user_id, "operation": "store_github_token"}
            )

        logger.info("Stored GitHub OAuth token for user: %s", user_id)

    async def get_github_token(self, user_id: str) -> Optional[str]:
        """Get decrypted GitHub OAuth token for user.

        Args:
            user_id: User ID

        Returns:
            Decrypted access token or None
        """
        logger.info("get_github_token: Starting token fetch for user: %s", user_id)
        
        def find_user_sync():
            logger.info("get_github_token: Starting synchronous MongoDB query")
            try:
                db = mongodb_manager.get_database()
                collection = db.users
                user = collection.find_one({"_id": ObjectId(user_id)})
                logger.info("get_github_token: Synchronous MongoDB query completed: user=%s", "found" if user else "None")
                return user
            except Exception as e:
                logger.error("get_github_token: Failed to fetch user synchronously: %s", e, exc_info=True)
                raise
        
        loop = asyncio.get_event_loop()
        try:
            user = await asyncio.wait_for(
                loop.run_in_executor(ThreadPoolExecutor(max_workers=1), find_user_sync),
                timeout=3.0
            )
        except asyncio.TimeoutError:
            logger.error("get_github_token: MongoDB query timed out after 3 seconds for user: %s", user_id)
            return None
        except Exception as e:
            logger.error("get_github_token: Error during MongoDB query: %s", e, exc_info=True)
            return None
        
        if not user or "github_oauth_token" not in user:
            logger.debug("get_github_token: User has no GitHub token: %s", user_id)
            return None

        token_data = user["github_oauth_token"]

        if token_data.get("expires_at"):
            expires_at = token_data["expires_at"]
            if isinstance(expires_at, str):
                try:
                    expires_at = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
                except ValueError:
                    logger.warning("Invalid expires_at format for user %s: %s", user_id, expires_at)
                    expires_at = None
            elif isinstance(expires_at, datetime):
                pass
            else:
                logger.warning("Invalid expires_at type for user %s: %s", user_id, type(expires_at))
                expires_at = None

            if expires_at and expires_at < datetime.utcnow():
                logger.warning("GitHub OAuth token expired for user: %s", user_id)
                return None

        encrypted_token = token_data["access_token"]
        try:
            from api.services.token_encryption_service import TokenEncryptionService

            decrypted_token = TokenEncryptionService.decrypt_token(encrypted_token, user_id)
            logger.info("get_github_token: Successfully decrypted token for user: %s", user_id)
            return decrypted_token
        except ValueError:
            logger.warning(
                "Failed to decrypt token with new method, trying legacy method for user %s",
                user_id
            )
            try:
                decrypted_token = indexing_service._decrypt_token_legacy(encrypted_token)
                logger.info("get_github_token: Successfully decrypted token with legacy method for user: %s", user_id)
                return decrypted_token
            except Exception as e:
                logger.error("Error decrypting GitHub token (legacy) for user %s: %s", user_id, e)
                return None
        except Exception as e:
            logger.error("Error decrypting GitHub token for user %s: %s", user_id, e)
            return None

    async def revoke_github_token(self, user_id: str) -> None:
        """Revoke GitHub OAuth token for user.

        Args:
            user_id: User ID
        """
        def update_user_sync():
            db = mongodb_manager.get_database()
            collection = db.users
            collection.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$unset": {"github_oauth_token": ""},
                    "$set": {
                        "github_connected": False,
                        "updated_at": datetime.utcnow(),
                    },
                },
            )
        
        loop = asyncio.get_event_loop()
        try:
            await asyncio.wait_for(
                loop.run_in_executor(ThreadPoolExecutor(max_workers=1), update_user_sync),
                timeout=3.0
            )
        except asyncio.TimeoutError:
            logger.error("revoke_github_token: MongoDB update timed out for user: %s", user_id)
            raise DatabaseError(
                message=f"Database update timeout for user: {user_id}",
                user_message="Database operation timed out. Please try again.",
                error_code="DATABASE_TIMEOUT",
                details={"user_id": user_id, "operation": "revoke_github_token"}
            )

        logger.info("Revoked GitHub OAuth token for user: %s", user_id)

    async def has_github_token(self, user_id: str) -> bool:
        """Check if user has GitHub OAuth token.

        Args:
            user_id: User ID

        Returns:
            True if user has valid token
        """
        token = await self.get_github_token(user_id)
        return token is not None

    async def get_github_organizations(self, user_id: str) -> list[dict[str, Any]]:
        """Get user's GitHub organizations from stored token data.

        Args:
            user_id: User ID

        Returns:
            List of organization dictionaries
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
            logger.error("get_github_organizations: MongoDB query timed out for user: %s", user_id)
            return []
        
        if not user or "github_oauth_token" not in user:
            return []

        token_data = user["github_oauth_token"]
        return token_data.get("organizations", [])

    async def update_github_organizations(
        self,
        user_id: str,
        organizations: list[dict[str, Any]],
    ) -> None:
        """Update stored GitHub organizations for user.

        Args:
            user_id: User ID
            organizations: List of organization dictionaries
        """
        def update_user_sync():
            db = mongodb_manager.get_database()
            collection = db.users
            collection.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$set": {
                        "github_oauth_token.organizations": organizations,
                        "github_oauth_token.updated_at": datetime.utcnow(),
                        "updated_at": datetime.utcnow(),
                    }
                },
            )
        
        loop = asyncio.get_event_loop()
        try:
            await asyncio.wait_for(
                loop.run_in_executor(ThreadPoolExecutor(max_workers=1), update_user_sync),
                timeout=3.0
            )
        except asyncio.TimeoutError:
            logger.error("update_github_organizations: MongoDB update timed out for user: %s", user_id)
            raise DatabaseError(
                message=f"Database update timeout for user: {user_id}",
                user_message="Database operation timed out. Please try again.",
                error_code="DATABASE_TIMEOUT",
                details={"user_id": user_id, "operation": "update_github_organizations"}
            )

        logger.info("Updated GitHub organizations for user: %s (%d orgs)", user_id, len(organizations))

    async def select_github_organizations(
        self,
        user_id: str,
        organization_logins: list[str],
    ) -> None:
        """Select which GitHub organizations to grant access.

        Args:
            user_id: User ID
            organization_logins: List of organization login names to select
        """
        def update_user_sync():
            db = mongodb_manager.get_database()
            collection = db.users
            collection.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$set": {
                        "github_oauth_token.selected_organizations": organization_logins,
                        "github_oauth_token.updated_at": datetime.utcnow(),
                        "updated_at": datetime.utcnow(),
                    }
                },
            )
        
        loop = asyncio.get_event_loop()
        try:
            await asyncio.wait_for(
                loop.run_in_executor(ThreadPoolExecutor(max_workers=1), update_user_sync),
                timeout=3.0
            )
        except asyncio.TimeoutError:
            logger.error("select_github_organizations: MongoDB update timed out for user: %s", user_id)
            raise DatabaseError(
                message=f"Database update timeout for user: {user_id}",
                user_message="Database operation timed out. Please try again.",
                error_code="DATABASE_TIMEOUT",
                details={"user_id": user_id, "operation": "select_github_organizations"}
            )

        logger.info(
            "Selected GitHub organizations for user: %s (%s)",
            user_id,
            ", ".join(organization_logins),
        )

    async def get_selected_organizations(self, user_id: str) -> list[str]:
        """Get selected organization logins for user.

        Args:
            user_id: User ID

        Returns:
            List of selected organization login names
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
            logger.error("get_selected_organizations: MongoDB query timed out for user: %s", user_id)
            return []
        
        if not user or "github_oauth_token" not in user:
            return []

        token_data = user["github_oauth_token"]
        return token_data.get("selected_organizations", [])


oauth_service = OAuthService()

