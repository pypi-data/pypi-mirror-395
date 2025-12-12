"""Admin authentication helpers."""

import logging
from typing import Optional

from api.database.mongodb import mongodb_manager
from api.auth.rbac import check_admin_access, get_user_permissions

logger = logging.getLogger(__name__)

ADMIN_DOMAIN = "@wistx.ai"
ADMIN_API_KEY_PREFIX = "wistx_admin_"


def is_internal_admin_domain(email: str | None) -> bool:
    """Check if email is from internal admin domain.

    Args:
        email: User email address

    Returns:
        True if email is from admin domain, False otherwise
    """
    if not email:
        return False
    return email.lower().endswith(ADMIN_DOMAIN.lower())


def is_admin_api_key(api_key: str) -> bool:
    """Check if API key is an admin API key.

    Args:
        api_key: API key string

    Returns:
        True if API key has admin prefix, False otherwise
    """
    if not api_key:
        return False
    return api_key.startswith(ADMIN_API_KEY_PREFIX)


def has_first_admin_signed_up() -> bool:
    """Check if first @wistx.ai admin has already signed up.

    Returns:
        True if first admin exists, False otherwise
    """
    db = mongodb_manager.get_database()
    collection = db.users

    first_admin = collection.find_one(
        {
            "email": {"$regex": f".*{ADMIN_DOMAIN.replace('@', '')}$", "$options": "i"},
            "$or": [
                {"is_super_admin": True},
                {"admin_role": {"$exists": True, "$ne": None}},
            ],
        }
    )

    return first_admin is not None


def can_signup_as_admin(email: str) -> tuple[bool, str | None]:
    """Check if email can sign up as admin.

    Args:
        email: User email address

    Returns:
        Tuple of (can_signup, error_message)
    """
    if not is_internal_admin_domain(email):
        return True, None

    if not has_first_admin_signed_up():
        return True, None

    from datetime import datetime

    db = mongodb_manager.get_database()
    invitation_collection = db.admin_invitations

    pending_invitation = invitation_collection.find_one(
        {
            "email": email.lower(),
            "status": "pending",
            "expires_at": {"$gt": datetime.utcnow()},
        }
    )

    if pending_invitation:
        return True, None

    return False, "Admin invitation required. Please contact an existing admin to receive an invitation."


def get_admin_info(user_doc: dict) -> dict:
    """Get admin information from user document.

    Args:
        user_doc: User document from MongoDB

    Returns:
        Dictionary with admin information
    """
    email = user_doc.get("email", "")
    admin_role = user_doc.get("admin_role")
    admin_permissions = user_doc.get("admin_permissions", [])
    is_super_admin = user_doc.get("is_super_admin", False)
    admin_status = user_doc.get("admin_status")
    admin_invited_by = user_doc.get("admin_invited_by")
    admin_invited_at = user_doc.get("admin_invited_at")

    is_admin = False

    if admin_role and admin_status == "active":
        is_admin = True
    elif is_super_admin:
        is_admin = True
    elif is_internal_admin_domain(email) and has_first_admin_signed_up():
        is_admin = False
    elif is_internal_admin_domain(email):
        is_admin = True

    return {
        "is_admin": is_admin,
        "admin_role": admin_role,
        "admin_permissions": admin_permissions,
        "is_super_admin": is_super_admin,
        "admin_status": admin_status,
        "admin_invited_by": str(admin_invited_by) if admin_invited_by else None,
        "admin_invited_at": admin_invited_at,
    }


def is_internal_admin(email: str | None) -> bool:
    """Check if email is from internal admin domain (backward compatibility).

    Args:
        email: User email address

    Returns:
        True if email is from admin domain, False otherwise
    """
    return is_internal_admin_domain(email)

