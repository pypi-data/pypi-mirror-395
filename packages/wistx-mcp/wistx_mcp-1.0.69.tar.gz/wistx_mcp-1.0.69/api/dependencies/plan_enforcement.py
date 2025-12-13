"""Plan enforcement dependencies for FastAPI."""

import logging
from typing import Annotated, Any

from fastapi import Depends, HTTPException, status

from api.dependencies import get_current_user
from api.services.exceptions import OrganizationQuotaExceededError, QuotaExceededError
from api.services.quota_service import quota_service
from api.services.plan_service import plan_service
from api.models.v1_responses import ErrorResponse

logger = logging.getLogger(__name__)


async def require_query_quota(
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
) -> dict[str, Any]:
    """Dependency that checks query quota before allowing request.

    Usage:
        @router.post("/endpoint")
        async def my_endpoint(
            user: dict = Depends(require_query_quota)
        ):
            # User has quota, proceed
    """
    user_id = current_user.get("user_id")
    plan = current_user.get("plan", "professional")
    is_admin = current_user.get("is_admin", False)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    if is_admin:
        return current_user

    try:
        await quota_service.check_query_quota(user_id, plan)
    except QuotaExceededError as e:
        from api.services.exceptions import OrganizationQuotaExceededError

        if isinstance(e, OrganizationQuotaExceededError):
            error_response = ErrorResponse(
                error={
                    "code": "ORGANIZATION_QUOTA_EXCEEDED",
                    "message": str(e),
                    "details": {
                        "limit_type": e.limit_type,
                        "current": e.current,
                        "limit": e.limit,
                        "organization_id": e.organization_id,
                        "member_breakdown": e.member_breakdown,
                        "upgrade_url": "/billing",
                    },
                },
            )
        else:
            error_response = ErrorResponse(
                error={
                    "code": "QUOTA_EXCEEDED",
                    "message": str(e),
                    "details": {
                        "limit_type": e.limit_type,
                        "current": e.current,
                        "limit": e.limit,
                        "upgrade_url": "/billing",
                    },
                },
            )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=error_response.model_dump(),
        ) from e

    return current_user


def require_indexing_quota(estimated_storage_mb: float = 0.0):
    """Dependency factory that checks indexing quota before allowing request.

    Usage:
        @router.post("/indexing/repositories")
        async def index_repo(
            request: IndexRequest,
            user: dict = Depends(require_indexing_quota(estimated_storage_mb=10.0))
        ):
            # User has indexing quota, proceed
    """
    async def dependency(
        current_user: Annotated[dict[str, Any], Depends(get_current_user)],
    ) -> dict[str, Any]:
        user_id = current_user.get("user_id")
        plan = current_user.get("plan", "professional")
        is_admin = current_user.get("is_admin", False)

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found",
            )

        if is_admin:
            return current_user

        try:
            await quota_service.check_indexing_quota(
                user_id=user_id,
                plan=plan,
                estimated_storage_mb=estimated_storage_mb,
            )
        except QuotaExceededError as e:
            from api.services.exceptions import OrganizationQuotaExceededError

            if isinstance(e, OrganizationQuotaExceededError):
                error_response = ErrorResponse(
                    error={
                        "code": "ORGANIZATION_QUOTA_EXCEEDED",
                        "message": str(e),
                        "details": {
                            "limit_type": e.limit_type,
                            "current": e.current,
                            "limit": e.limit,
                            "organization_id": e.organization_id,
                            "member_breakdown": e.member_breakdown,
                            "upgrade_url": "/billing",
                        },
                    },
                )
            else:
                error_response = ErrorResponse(
                    error={
                        "code": "QUOTA_EXCEEDED",
                        "message": str(e),
                        "details": {
                            "limit_type": e.limit_type,
                            "current": e.current,
                            "limit": e.limit,
                            "upgrade_url": "/billing",
                        },
                    },
                )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=error_response.model_dump(),
            ) from e

        return current_user

    return dependency


def require_plan_feature(feature_name: str):
    """Dependency factory that requires a specific plan feature.

    Usage:
        @router.post("/sso/configure")
        async def configure_sso(
            user: dict = Depends(require_plan_feature("sso"))
        ):
            # User has SSO feature, proceed
    """
    async def dependency(
        current_user: Annotated[dict[str, Any], Depends(get_current_user)],
    ) -> dict[str, Any]:
        plan_id = current_user.get("plan", "professional")
        is_admin = current_user.get("is_admin", False)

        if is_admin:
            return current_user

        plan_features = plan_service.get_plan_features(plan_id)

        if not plan_features:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Plan features not found",
            )

        feature_value = getattr(plan_features, feature_name, False)

        if not feature_value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": {
                        "code": "FEATURE_NOT_AVAILABLE",
                        "message": f"Feature '{feature_name}' is not available on your plan",
                        "details": {
                            "current_plan": plan_id,
                            "required_feature": feature_name,
                            "upgrade_url": "/billing",
                        },
                    }
                },
            )

        return current_user

    return dependency


def require_minimum_plan(minimum_plan: str):
    """Dependency factory that requires a minimum plan level.

    Plan hierarchy: professional < team < enterprise

    Usage:
        @router.post("/advanced/feature")
        async def advanced_feature(
            user: dict = Depends(require_minimum_plan("team"))
        ):
            # User has Team+ plan, proceed
    """
    plan_hierarchy = {
        "professional": 1,
        "team": 2,
        "enterprise": 3,
    }

    async def dependency(
        current_user: Annotated[dict[str, Any], Depends(get_current_user)],
    ) -> dict[str, Any]:
        user_plan = current_user.get("plan", "professional")
        is_admin = current_user.get("is_admin", False)

        if is_admin:
            return current_user

        user_level = plan_hierarchy.get(user_plan, 0)
        required_level = plan_hierarchy.get(minimum_plan, 999)

        if user_level < required_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": {
                        "code": "PLAN_UPGRADE_REQUIRED",
                        "message": f"This feature requires {minimum_plan} plan or higher",
                        "details": {
                            "current_plan": user_plan,
                            "required_plan": minimum_plan,
                            "upgrade_url": "/billing",
                        },
                    }
                },
            )

        return current_user

    return dependency


async def require_api_key_limit(
    current_user: Annotated[dict[str, Any] | Any, Depends(get_current_user)],
) -> dict[str, Any]:
    """Dependency that checks API key limit before allowing creation.

    Usage:
        @router.post("/api-keys")
        async def create_api_key(
            user: dict = Depends(require_api_key_limit)
        ):
            # User hasn't exceeded API key limit, proceed
    """
    if hasattr(current_user, "id"):
        user_id = str(current_user.id)
        plan = getattr(current_user, "plan", "professional")
    else:
        user_id = current_user.get("user_id") if isinstance(current_user, dict) else None
        plan = current_user.get("plan", "professional") if isinstance(current_user, dict) else "professional"

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    plan_limits = plan_service.get_plan_limits(plan)
    if not plan_limits:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Plan limits not found",
        )

    from api.database.mongodb import mongodb_manager
    from bson import ObjectId

    db = mongodb_manager.get_database()
    current_key_count = db.api_keys.count_documents(
        {"user_id": ObjectId(user_id), "revoked": False}
    )

    if current_key_count >= plan_limits.max_api_keys:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": {
                    "code": "API_KEY_LIMIT_EXCEEDED",
                    "message": f"API key limit exceeded. Current: {current_key_count}, Limit: {plan_limits.max_api_keys}",
                    "details": {
                        "current": current_key_count,
                        "limit": plan_limits.max_api_keys,
                        "upgrade_url": "/billing",
                    },
                }
            },
        )

    return current_user


async def require_custom_compliance_access(
    current_user: Annotated[dict[str, Any], Depends(get_current_user)],
) -> dict[str, Any]:
    """Dependency that checks if user has access to custom compliance controls.

    Usage:
        @router.post("/compliance/custom-controls/upload")
        async def upload_custom_controls(
            user: dict = Depends(require_custom_compliance_access)
        ):
            # User has access, proceed
    """
    plan_id = current_user.get("plan", "professional")
    is_admin = current_user.get("is_admin", False)

    if is_admin:
        return current_user

    plan_hierarchy = {
        "professional": 1,
        "team": 2,
        "enterprise": 3,
    }
    user_level = plan_hierarchy.get(plan_id, 0)
    required_level = plan_hierarchy.get("professional", 1)

    if user_level < required_level:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": {
                    "code": "PLAN_UPGRADE_REQUIRED",
                    "message": "Custom compliance controls require Professional plan or higher. Upgrade to Professional ($99/month) or Team ($999/month) for more features.",
                    "details": {
                        "current_plan": plan_id,
                        "required_plan": "professional",
                        "upgrade_url": "/billing",
                    },
                }
            },
        )

    return current_user

