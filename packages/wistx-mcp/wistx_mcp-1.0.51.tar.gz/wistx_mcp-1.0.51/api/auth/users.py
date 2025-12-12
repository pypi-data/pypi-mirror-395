"""User models and OAuth authentication setup."""

import logging
from typing import Optional

from bson import ObjectId
from fastapi import Depends, Request
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend
from fastapi_users.manager import BaseUserManager
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.clients.github import GitHubOAuth2
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import Field, ConfigDict

from api.config import settings
from api.database.async_mongodb import async_mongodb_adapter
from api.auth.database import MongoDBUserDatabase

logger = logging.getLogger(__name__)


class OAuthAccount:
    """OAuth account wrapper that provides attribute access to dict data."""

    def __init__(self, data: dict):
        """Initialize OAuth account from dictionary."""
        self._data = data

    @property
    def oauth_name(self) -> str:
        """Get OAuth provider name."""
        return self._data.get("oauth_name", "")

    @property
    def account_id(self) -> str:
        """Get OAuth account ID."""
        return self._data.get("account_id", "")

    @property
    def account_email(self) -> str:
        """Get OAuth account email."""
        return self._data.get("account_email", "")

    @property
    def access_token(self) -> str:
        """Get access token."""
        return self._data.get("access_token", "")

    @property
    def expires_at(self) -> int | None:
        """Get expiration timestamp."""
        return self._data.get("expires_at")

    @property
    def refresh_token(self) -> str | None:
        """Get refresh token."""
        return self._data.get("refresh_token")

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return self._data.copy()

    def __getattr__(self, name: str):
        """Allow access to other dict keys as attributes."""
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


class User:
    """User model implementing UserProtocol for FastAPI-Users v15."""

    def __init__(
        self,
        id: ObjectId,
        email: str,
        hashed_password: str = "",
        is_active: bool = True,
        is_superuser: bool = False,
        is_verified: bool = False,
        organization_id: Optional[ObjectId] = None,
        plan: str = "professional",
        oauth_accounts: Optional[list[dict | OAuthAccount]] = None,
        github_oauth_token: Optional[dict] = None,
        full_name: Optional[str] = None,
        role: Optional[str] = None,
        organization_name: Optional[str] = None,
        referral_source: Optional[str] = None,
        profile_completed: bool = False,
    ):
        """Initialize user."""
        self.id = id
        self.email = email
        self.hashed_password = hashed_password
        self.is_active = is_active
        self.is_superuser = is_superuser
        self.is_verified = is_verified
        self.organization_id = organization_id
        self.plan = plan
        oauth_accounts_raw = oauth_accounts or []
        self.oauth_accounts = [
            account if isinstance(account, OAuthAccount) else OAuthAccount(account)
            for account in oauth_accounts_raw
        ]
        self.github_oauth_token = github_oauth_token
        self.full_name = full_name
        self.role = role
        self.organization_name = organization_name
        self.referral_source = referral_source
        self.profile_completed = profile_completed

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Create user from dictionary."""
        return cls(
            id=data.get("_id", data.get("id")),
            email=data["email"],
            hashed_password=data.get("hashed_password", ""),
            is_active=data.get("is_active", True),
            is_superuser=data.get("is_superuser", False),
            is_verified=data.get("is_verified", False),
            organization_id=data.get("organization_id"),
            plan=data.get("plan", "professional"),
            oauth_accounts=data.get("oauth_accounts", []),
            github_oauth_token=data.get("github_oauth_token"),
            full_name=data.get("full_name"),
            role=data.get("role"),
            organization_name=data.get("organization_name"),
            referral_source=data.get("referral_source"),
            profile_completed=data.get("profile_completed", False),
        )

    def to_dict(self) -> dict:
        """Convert user to dictionary."""
        result = {
            "_id": self.id,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "is_verified": self.is_verified,
            "profile_completed": self.profile_completed,
        }
        if self.organization_id:
            result["organization_id"] = self.organization_id
        if self.plan:
            result["plan"] = self.plan
        if self.oauth_accounts:
            result["oauth_accounts"] = [
                account.to_dict() if isinstance(account, OAuthAccount) else account
                for account in self.oauth_accounts
            ]
        if self.github_oauth_token:
            result["github_oauth_token"] = self.github_oauth_token
        if self.full_name:
            result["full_name"] = self.full_name
        if self.role:
            result["role"] = self.role
        if self.organization_name:
            result["organization_name"] = self.organization_name
        if self.referral_source:
            result["referral_source"] = self.referral_source
        return result


class UserManager(BaseUserManager[User, ObjectId]):
    """Custom user manager."""

    def __init__(self, user_db: MongoDBUserDatabase):
        """Initialize user manager.

        Args:
            user_db: MongoDB user database
        """
        from fastapi_users.password import PasswordHelper

        super().__init__(user_db, PasswordHelper())

    def parse_id(self, value: str | ObjectId) -> ObjectId:
        """Parse user ID from string or ObjectId.

        Args:
            value: User ID as string or ObjectId

        Returns:
            ObjectId instance

        Raises:
            ValueError: If value cannot be converted to ObjectId
        """
        if isinstance(value, ObjectId):
            return value
        try:
            return ObjectId(value)
        except Exception as e:
            raise ValueError(f"Invalid user ID format: {value}") from e

    async def on_after_register(self, user: User, request: Request | None = None) -> None:
        """Called after user registration.
        
        Signup flow order:
        1. OAuth Authentication (Google/GitHub) - creates account (this hook)
        2. Profile Completion - required (user must complete profile) - welcome email sent here
        3. GitHub Repository Connection - optional, last step (can be done later)
        
        Note: Welcome email is sent after profile completion, not during registration.
        """
        logger.info("User %s has registered - profile completion required", user.id)

    async def on_after_update(
        self,
        user: User,
        update_dict: dict,
        request: Request | None = None,
    ) -> None:
        """Called after user update."""
        logger.info("User %s has been updated", user.id)


async def get_user_db() -> MongoDBUserDatabase:
    """Get MongoDB user database adapter.

    Yields:
        MongoDBUserDatabase instance
    """
    await async_mongodb_adapter.connect()
    db: AsyncIOMotorDatabase = async_mongodb_adapter.get_database()
    collection = db.users
    yield MongoDBUserDatabase(collection)


async def get_user_manager(user_db: MongoDBUserDatabase = Depends(get_user_db)) -> UserManager:
    """Get user manager instance.

    Args:
        user_db: MongoDB user database

    Yields:
        UserManager instance
    """
    yield UserManager(user_db)


def get_jwt_authentication() -> AuthenticationBackend:
    """Get JWT authentication backend.

    Returns:
        AuthenticationBackend instance
    """
    bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
    jwt_strategy = JWTStrategy(
        secret=settings.secret_key,
        lifetime_seconds=settings.access_token_expire_minutes * 60,
    )
    return AuthenticationBackend(
        name="jwt",
        transport=bearer_transport,
        get_strategy=lambda: jwt_strategy,
    )


jwt_authentication = get_jwt_authentication()


def get_google_oauth_client() -> GoogleOAuth2:
    """Get Google OAuth client.

    Returns:
        GoogleOAuth2 instance
    """
    return GoogleOAuth2(
        client_id=settings.google_oauth_client_id,
        client_secret=settings.google_oauth_client_secret,
    )


def get_github_oauth_client() -> GitHubOAuth2:
    """Get GitHub OAuth client.

    Returns:
        GitHubOAuth2 instance
    """
    return GitHubOAuth2(
        client_id=settings.github_oauth_client_id,
        client_secret=settings.github_oauth_client_secret,
    )


google_oauth_client = get_google_oauth_client()
github_oauth_client = get_github_oauth_client()


fastapi_users = FastAPIUsers[User, ObjectId](
    get_user_manager,
    [jwt_authentication],
)
