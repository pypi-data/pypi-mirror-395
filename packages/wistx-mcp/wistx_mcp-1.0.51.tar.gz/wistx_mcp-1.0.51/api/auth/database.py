"""MongoDB database adapter for FastAPI-Users."""

import logging
from typing import Optional, TYPE_CHECKING

from bson import ObjectId
from fastapi_users.db.base import BaseUserDatabase
from motor.motor_asyncio import AsyncIOMotorCollection

if TYPE_CHECKING:
    from api.auth.users import User

logger = logging.getLogger(__name__)


class MongoDBUserDatabase(BaseUserDatabase["User", ObjectId]):
    """MongoDB user database adapter for FastAPI-Users."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initialize MongoDB user database.

        Args:
            collection: Motor collection instance
        """
        self.collection = collection

    async def get(self, id: ObjectId | str) -> Optional["User"]:
        """Get user by ID.

        Args:
            id: User ID (ObjectId or string)

        Returns:
            User instance or None
        """
        from api.auth.users import User

        if isinstance(id, str):
            try:
                id = ObjectId(id)
            except Exception:
                logger.warning("Invalid user ID format: %s", id)
                return None

        user_dict = await self.collection.find_one({"_id": id})
        if user_dict:
            return User.from_dict(user_dict)
        return None

    async def get_by_email(self, email: str) -> Optional["User"]:
        """Get user by email.

        Args:
            email: User email

        Returns:
            User instance or None
        """
        from api.auth.users import User

        user_dict = await self.collection.find_one({"email": email})
        if user_dict:
            return User.from_dict(user_dict)
        return None

    async def get_by_oauth_account(self, oauth: str, account_id: str) -> Optional["User"]:
        """Get user by OAuth account.

        Args:
            oauth: OAuth provider name
            account_id: OAuth account ID (will be normalized to string)

        Returns:
            User instance or None
        """
        from api.auth.users import User

        account_id_str = str(account_id)
        
        user_dict = await self.collection.find_one(
            {"oauth_accounts": {"$elemMatch": {"oauth_name": oauth, "account_id": account_id_str}}}
        )
        
        if not user_dict and account_id_str.isdigit():
            try:
                account_id_int = int(account_id_str)
                max_mongodb_int = 9223372036854775807
                min_mongodb_int = -9223372036854775808
                
                if min_mongodb_int <= account_id_int <= max_mongodb_int:
                    user_dict = await self.collection.find_one(
                        {"oauth_accounts": {"$elemMatch": {"oauth_name": oauth, "account_id": account_id_int}}}
                    )
                else:
                    logger.debug(
                        "Account ID %s exceeds MongoDB integer range, skipping integer query",
                        account_id_str,
                    )
            except (ValueError, TypeError, OverflowError) as e:
                logger.debug("Could not convert account_id to integer: %s", e)
                pass
        
        if user_dict:
            return User.from_dict(user_dict)
        return None

    async def create(self, user: "User") -> "User":
        """Create new user.

        Args:
            user: User instance or dict

        Returns:
            Created User instance

        Raises:
            ValueError: If admin signup is not allowed
        """
        from api.auth.users import User
        from api.auth.admin import (
            can_signup_as_admin,
            is_internal_admin_domain,
            has_first_admin_signed_up,
        )
        from api.database.mongodb import mongodb_manager
        from datetime import datetime

        if isinstance(user, dict):
            user_dict = user.copy()
        else:
            user_dict = user.to_dict()

        email = user_dict.get("email", "")
        can_signup, error_msg = can_signup_as_admin(email)

        if not can_signup:
            raise ValueError(error_msg or "Admin signup not allowed")

        if "_id" not in user_dict:
            user_dict["_id"] = ObjectId()

        if is_internal_admin_domain(email) and not has_first_admin_signed_up():
            user_dict["is_super_admin"] = True
            user_dict["admin_role"] = "super_admin"
            user_dict["admin_status"] = "active"
            user_dict["admin_permissions"] = ["*"]
            user_dict["admin_invited_at"] = datetime.utcnow()
            user_dict["plan"] = "enterprise"
        elif is_internal_admin_domain(email) and has_first_admin_signed_up():
            db = mongodb_manager.get_database()
            pending_invitation = db.admin_invitations.find_one(
                {
                    "email": email.lower(),
                    "status": "pending",
                    "expires_at": {"$gt": datetime.utcnow()},
                }
            )

            if pending_invitation:
                role_permissions = pending_invitation.get("permissions", [])
                if not role_permissions:
                    from api.models.admin.rbac import ADMIN_ROLES
                    role_permissions = ADMIN_ROLES.get(pending_invitation.get("role", "admin"), [])

                user_dict["admin_role"] = pending_invitation.get("role", "admin")
                user_dict["admin_permissions"] = role_permissions
                user_dict["admin_status"] = "active"
                user_dict["admin_invited_by"] = pending_invitation["invited_by"]
                user_dict["admin_invited_at"] = datetime.utcnow()
                user_dict["plan"] = "enterprise"

                db.admin_invitations.update_one(
                    {"_id": pending_invitation["_id"]},
                    {
                        "$set": {
                            "status": "accepted",
                            "accepted_at": datetime.utcnow(),
                            "accepted_by": user_dict["_id"],
                            "updated_at": datetime.utcnow(),
                        }
                    },
                )

                logger.info("Admin invitation auto-accepted during signup for %s", email)

        await self.collection.insert_one(user_dict)
        return User.from_dict(user_dict)

    async def update(self, user: "User") -> "User":
        """Update user.

        Args:
            user: User instance

        Returns:
            Updated User instance
        """
        user_dict = user.to_dict()
        user_id = user_dict.pop("_id")
        await self.collection.update_one({"_id": user_id}, {"$set": user_dict})
        return user

    async def delete(self, user: "User") -> None:
        """Delete user.

        Args:
            user: User instance
        """
        await self.collection.delete_one({"_id": user.id})

    async def add_oauth_account(self, user: "User", oauth_account: dict) -> "User":
        """Add OAuth account to user.

        Args:
            user: User instance
            oauth_account: OAuth account dictionary

        Returns:
            Updated User instance
        """
        from api.auth.users import User

        user_dict = user.to_dict()
        oauth_accounts = user_dict.get("oauth_accounts", [])
        
        existing_index = None
        for i, account in enumerate(oauth_accounts):
            account_dict = account if isinstance(account, dict) else account.to_dict()
            if (
                account_dict.get("oauth_name") == oauth_account.get("oauth_name")
                and account_dict.get("account_id") == oauth_account.get("account_id")
            ):
                existing_index = i
                break

        if existing_index is not None:
            oauth_accounts[existing_index] = oauth_account
        else:
            oauth_accounts.append(oauth_account)

        user_dict["oauth_accounts"] = oauth_accounts
        user_id = user_dict.pop("_id")
        await self.collection.update_one(
            {"_id": user_id},
            {"$set": {"oauth_accounts": oauth_accounts}},
        )
        return User.from_dict({**user_dict, "_id": user_id})

    async def update_oauth_account(
        self, user: "User", oauth_account: "OAuthAccount", update_dict: dict
    ) -> "User":
        """Update OAuth account for user.

        Args:
            user: User instance
            oauth_account: Existing OAuth account object
            update_dict: Dictionary with updates to apply

        Returns:
            Updated User instance
        """
        from api.auth.users import User, OAuthAccount

        user_dict = user.to_dict()
        oauth_accounts = user_dict.get("oauth_accounts", [])
        
        oauth_account_dict = oauth_account.to_dict() if isinstance(oauth_account, OAuthAccount) else oauth_account
        updated_account = {**oauth_account_dict, **update_dict}
        
        existing_index = None
        for i, account in enumerate(oauth_accounts):
            account_dict = account if isinstance(account, dict) else account.to_dict()
            if (
                account_dict.get("oauth_name") == oauth_account_dict.get("oauth_name")
                and account_dict.get("account_id") == oauth_account_dict.get("account_id")
            ):
                existing_index = i
                break

        if existing_index is not None:
            oauth_accounts[existing_index] = updated_account
        else:
            oauth_accounts.append(updated_account)

        user_dict["oauth_accounts"] = oauth_accounts
        user_id = user_dict.pop("_id")
        await self.collection.update_one(
            {"_id": user_id},
            {"$set": {"oauth_accounts": oauth_accounts}},
        )
        return User.from_dict({**user_dict, "_id": user_id})

