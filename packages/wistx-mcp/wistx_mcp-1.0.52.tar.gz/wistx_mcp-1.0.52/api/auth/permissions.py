"""Permission checks for API access."""

import logging
from typing import Any

from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


def check_permission(user_info: dict[str, Any], required_permission: str) -> bool:
    """Check if user has required permission.

    Args:
        user_info: User information dictionary
        required_permission: Required permission name

    Returns:
        True if user has permission, False otherwise

    Raises:
        HTTPException: If permission check fails
    """
    plan = user_info.get("plan", "professional")
    scopes = user_info.get("scopes", [])

    if required_permission in scopes:
        return True

    plan_permissions = {
        "professional": ["read"],
        "team": ["read", "write"],
        "enterprise": ["read", "write", "admin", "billing"],
    }

    user_permissions = plan_permissions.get(plan, ["read"])

    if required_permission in user_permissions:
        return True

    logger.warning(
        "Permission denied: user %s (plan: %s) attempted %s",
        user_info.get("user_id"),
        plan,
        required_permission,
    )

    from api.models.audit_log import AuditEventType, AuditLogSeverity
    from api.services.audit_log_service import audit_log_service

    audit_log_service.log_event(
        event_type=AuditEventType.AUTHORIZATION_DENIED,
        severity=AuditLogSeverity.HIGH,
        message=f"Permission denied: user {user_info.get('user_id')} (plan: {plan}) attempted {required_permission}",
        success=False,
        user_id=user_info.get("user_id"),
        api_key_id=user_info.get("api_key_id"),
        organization_id=user_info.get("organization_id"),
        details={
            "required_permission": required_permission,
            "user_plan": plan,
            "user_scopes": user_info.get("scopes", []),
        },
        compliance_tags=["PCI-DSS-10", "SOC2"],
    )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={
            "error": {
                "code": "PERMISSION_DENIED",
                "message": f"Permission '{required_permission}' required. Current plan: {plan}",
            }
        },
    )


def require_permission(required_permission: str):
    """Decorator to require permission for endpoint.

    Args:
        required_permission: Required permission name

    Returns:
        Decorator function
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            user_info = kwargs.get("current_user")
            if not user_info:
                for arg in args:
                    if isinstance(arg, dict) and "user_id" in arg:
                        user_info = arg
                        break

            if not user_info:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required",
                )

            check_permission(user_info, required_permission)
            return await func(*args, **kwargs)

        return wrapper

    return decorator
