"""Plan enforcement utilities for MCP tools."""

import functools
import logging
import sys
from typing import Any, Callable, TypeVar

from wistx_mcp.tools.lib.auth_context import get_auth_context

logger = logging.getLogger(__name__)

# Patch sys.exit to prevent api.config from exiting the MCP server
_original_sys_exit = sys.exit

def _mcp_safe_exit(code: int = 0) -> None:
    """MCP-safe sys.exit that raises SystemExit instead of exiting."""
    raise SystemExit(code)

try:
    sys.exit = _mcp_safe_exit
    from api.services.quota_service import quota_service, QuotaExceededError
    API_AVAILABLE = True
except (ImportError, SystemExit, Exception):
    API_AVAILABLE = False
    quota_service = None
    QuotaExceededError = Exception
finally:
    sys.exit = _original_sys_exit

T = TypeVar("T")


def require_query_quota(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator to check query quota before executing MCP tool.

    Usage:
        @require_query_quota
        async def my_tool(query: str, api_key: str) -> dict:
            # Quota checked, proceed
            pass
    """
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        auth_ctx = get_auth_context()

        if auth_ctx and API_AVAILABLE and quota_service:
            user_id = auth_ctx.get_user_id()
            if user_id:
                try:
                    plan = "professional"
                    if auth_ctx.user_info:
                        plan = auth_ctx.user_info.get("plan", "professional")

                    await quota_service.check_query_quota(user_id, plan)

                    try:
                        from api.services.usage_tracker import usage_tracker
                        from api.models.usage import APIUsageRequest
                        import secrets

                        api_key_id = ""
                        if auth_ctx.user_info:
                            api_key_id = auth_ctx.user_info.get("api_key_id", "")

                        usage_request = APIUsageRequest(
                            request_id=f"mcp_{secrets.token_hex(12)}",
                            user_id=user_id,
                            api_key_id=api_key_id,
                            organization_id=auth_ctx.user_info.get("organization_id") if auth_ctx.user_info else None,
                            plan=plan,
                            endpoint=f"mcp/{func.__name__}",
                            method="MCP",
                            operation_type="query",
                            operation_details={"tool": func.__name__},
                            status_code=200,
                            success=True,
                        )
                        await usage_tracker.track_request(usage_request)
                    except Exception as e:
                        logger.warning("Failed to track MCP tool usage: %s", e)

                except QuotaExceededError as e:
                    logger.warning("Quota exceeded for user %s: %s", user_id, e)
                    raise RuntimeError(f"Quota exceeded: {e}") from e
                except Exception as e:
                    logger.warning("Failed to check quota (continuing): %s", e)
        elif not API_AVAILABLE:
            logger.debug("API module not available, skipping quota check")

        return await func(*args, **kwargs)

    return wrapper


def require_plan_feature(feature_name: str):
    """Decorator factory that requires a specific plan feature.

    Usage:
        @require_plan_feature("sso")
        async def configure_sso(api_key: str) -> dict:
            # SSO feature checked, proceed
            pass
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            auth_ctx = get_auth_context()

            if not auth_ctx:
                raise ValueError("Authentication required")

            user_id = auth_ctx.get_user_id()
            if not user_id:
                raise ValueError("User ID not found")

            plan_id = auth_ctx.user_info.get("plan", "professional") if auth_ctx.user_info else "professional"

            if not API_AVAILABLE:
                logger.warning("API module not available, cannot check plan features. Allowing access.")
                return await func(*args, **kwargs)

            try:
                from api.services.plan_service import plan_service

                plan_features = plan_service.get_plan_features(plan_id)
                if not plan_features:
                    raise RuntimeError("Plan features not found")

                feature_value = getattr(plan_features, feature_name, False)
                if not feature_value:
                    raise ValueError(
                        f"Feature '{feature_name}' is not available on {plan_id} plan. "
                        f"Please upgrade to a plan that includes this feature."
                    )
            except ImportError:
                logger.warning("API module not available, cannot check plan features. Allowing access.")
                return await func(*args, **kwargs)

            return await func(*args, **kwargs)

        return wrapper

    return decorator


def require_minimum_plan(minimum_plan: str):
    """Decorator factory that requires a minimum plan level.

    Usage:
        @require_minimum_plan("team")
        async def advanced_feature(api_key: str) -> dict:
            # Team+ plan required, proceed
            pass
    """
    plan_hierarchy = {"professional": 1, "team": 2, "enterprise": 3}

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            auth_ctx = get_auth_context()

            if not auth_ctx:
                raise ValueError("Authentication required")

            user_plan = auth_ctx.user_info.get("plan", "professional") if auth_ctx.user_info else "professional"
            user_level = plan_hierarchy.get(user_plan, 0)
            required_level = plan_hierarchy.get(minimum_plan, 999)

            if user_level < required_level:
                raise ValueError(
                    f"This feature requires {minimum_plan} plan or higher. "
                    f"Your current plan: {user_plan}. Please upgrade."
                )

            return await func(*args, **kwargs)

        return wrapper

    return decorator

