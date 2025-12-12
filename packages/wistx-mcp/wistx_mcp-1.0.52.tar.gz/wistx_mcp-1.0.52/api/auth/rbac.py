"""RBAC permission checking utilities."""

import logging
from typing import Any

from api.models.admin.rbac import ADMIN_ROLES, VALID_PERMISSIONS

logger = logging.getLogger(__name__)


def get_role_permissions(role: str | None) -> list[str]:
    """Get permissions for a role.

    Args:
        role: Admin role name

    Returns:
        List of permissions for the role
    """
    if not role:
        return []

    if role == "super_admin":
        return ["*"]

    return ADMIN_ROLES.get(role, [])


def has_permission(
    user_permissions: list[str], required_permission: str, is_super_admin: bool = False
) -> bool:
    """Check if user has required permission.

    Args:
        user_permissions: List of user permissions
        required_permission: Required permission name
        is_super_admin: Whether user is super admin

    Returns:
        True if user has permission, False otherwise
    """
    if is_super_admin:
        return True

    if "*" in user_permissions:
        return True

    if required_permission in user_permissions:
        return True

    return False


def check_admin_access(user_info: dict[str, Any]) -> tuple[bool, str | None]:
    """Check if user has admin access.

    Args:
        user_info: User information dictionary

    Returns:
        Tuple of (has_access, error_message)
    """
    is_admin = user_info.get("is_admin", False)
    admin_role = user_info.get("admin_role")
    is_super_admin = user_info.get("is_super_admin", False)
    admin_status = user_info.get("admin_status")

    if not is_admin:
        return False, "User is not an admin"

    if admin_status == "suspended":
        return False, "Admin account is suspended"

    if admin_status == "invited" and not admin_role:
        return False, "Admin invitation not yet accepted"

    if admin_role and admin_status != "active":
        return False, f"Admin account status is {admin_status}"

    return True, None


def get_user_permissions(user_info: dict[str, Any]) -> list[str]:
    """Get user's effective permissions.

    Args:
        user_info: User information dictionary

    Returns:
        List of permissions
    """
    is_super_admin = user_info.get("is_super_admin", False)
    admin_role = user_info.get("admin_role")
    admin_permissions = user_info.get("admin_permissions", [])

    if is_super_admin:
        return ["*"]

    if admin_role:
        role_perms = get_role_permissions(admin_role)
        combined_perms = list(set(role_perms + admin_permissions))
        return combined_perms

    return admin_permissions

