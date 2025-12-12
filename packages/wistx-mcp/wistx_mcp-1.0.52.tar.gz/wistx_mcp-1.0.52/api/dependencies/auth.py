"""Authentication dependencies."""

import logging
from typing import Annotated, Any

from fastapi import Depends, Header, HTTPException, Request, status

from api.auth.api_keys import get_user_from_api_key

logger = logging.getLogger(__name__)


async def get_api_key(
    authorization: Annotated[str | None, Header()] = None,
) -> str:
    """Extract API key from Authorization header.

    Args:
        authorization: Authorization header value

    Returns:
        API key string

    Raises:
        HTTPException: If authorization header is invalid
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header. Expected 'Bearer {api_key}'",
        )
    api_key = authorization.replace("Bearer ", "").strip()
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required",
        )
    return api_key


async def get_current_user(
    request: Request,
    authorization: Annotated[str | None, Header()] = None,
) -> dict[str, Any]:
    """Extract user information from cookie, JWT token, or API key.

    First checks request.state.user_info (set by AuthenticationMiddleware),
    which handles both cookie-based and header-based JWT tokens.
    Falls back to API key validation if needed.

    Args:
        request: FastAPI request object
        authorization: Authorization header value (for API keys or fallback)

    Returns:
        Dictionary with user_id, organization_id, plan, rate_limits, etc.

    Raises:
        HTTPException: If authentication is invalid or missing
    """
    logger.info(
        "get_current_user called: path=%s, has_user_info=%s, has_cookie=%s, has_auth_header=%s",
        request.url.path,
        bool(getattr(request.state, "user_info", None)),
        bool(request.cookies.get("auth_token")),
        bool(authorization),
    )
    
    user_info = getattr(request.state, "user_info", None)
    if user_info:
        logger.info("get_current_user: Returning user_info from request.state")
        return user_info

    cookie_token = request.cookies.get("auth_token")
    if cookie_token:
        logger.info("get_current_user: Cookie token found, attempting validation")
        logger.debug("get_current_user: Cookie token found, attempting validation")
        try:
            import asyncio
            from api.auth.users import jwt_authentication
            from api.database.async_mongodb import async_mongodb_adapter
            from api.auth.database import MongoDBUserDatabase
            from api.auth.users import UserManager
            from api.database.mongodb import mongodb_manager
            from api.auth.admin import get_admin_info
            from bson import ObjectId

            async def validate_token_with_timeout():
                logger.info("get_current_user: Starting async MongoDB connect for JWT validation")
                await async_mongodb_adapter.connect()
                logger.info("get_current_user: Async MongoDB adapter connected successfully")
                db = async_mongodb_adapter.get_database()
                collection = db.users
                user_db = MongoDBUserDatabase(collection)
                user_manager = UserManager(user_db)

                strategy = jwt_authentication.get_strategy()
                logger.info("get_current_user: Calling strategy.read_token() for JWT validation")
                user = await strategy.read_token(cookie_token, user_manager)
                logger.info("get_current_user: strategy.read_token() completed: user=%s", "found" if user else "None")
                return user
            
            try:
                logger.info("get_current_user: Starting token validation with 5s timeout")
                user = await asyncio.wait_for(validate_token_with_timeout(), timeout=5.0)
                logger.info("get_current_user: Token validation completed")
            except asyncio.TimeoutError:
                logger.error(
                    "get_current_user: MongoDB token validation timed out after 5 seconds. Path: %s",
                    request.url.path,
                )
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Authentication service temporarily unavailable",
                )
            if user:
                email = getattr(user, "email", "")
                
                from concurrent.futures import ThreadPoolExecutor
                
                def get_user_doc_sync():
                    logger.info("get_current_user: Starting synchronous MongoDB query for user_doc")
                    try:
                        sync_db = mongodb_manager.get_database()
                        user_doc = sync_db.users.find_one({"_id": ObjectId(str(user.id))})
                        logger.info("get_current_user: Synchronous MongoDB query completed: user_doc=%s", "found" if user_doc else "None")
                        return user_doc
                    except Exception as e:
                        logger.warning("get_current_user: Failed to fetch user doc synchronously: %s", e, exc_info=True)
                        return None
                
                loop = asyncio.get_event_loop()
                try:
                    logger.info("get_current_user: Starting executor for synchronous MongoDB query (3s timeout)")
                    user_doc = await asyncio.wait_for(
                        loop.run_in_executor(ThreadPoolExecutor(max_workers=1), get_user_doc_sync),
                        timeout=3.0
                    )
                    logger.info("get_current_user: Executor completed")
                except asyncio.TimeoutError:
                    logger.warning("get_current_user: Synchronous MongoDB query timed out after 3 seconds")
                    user_doc = None
                except Exception as e:
                    logger.error("get_current_user: Error during synchronous user_doc fetch: %s", e, exc_info=True)
                    user_doc = None
                
                logger.info("get_current_user: Building user_info dictionary")
                admin_info = {}
                if user_doc:
                    admin_info = get_admin_info(user_doc)
                else:
                    from api.auth.admin import is_internal_admin_domain
                    admin_info = {
                        "is_admin": is_internal_admin_domain(email),
                        "admin_role": None,
                        "admin_permissions": [],
                        "is_super_admin": False,
                        "admin_status": None,
                    }

                organization_id = None
                organization_role = None
                if user_doc:
                    organization_id = str(user_doc.get("organization_id")) if user_doc.get("organization_id") else None
                    if organization_id:
                        from bson import ObjectId
                        member = sync_db.organization_members.find_one(
                            {
                                "organization_id": ObjectId(organization_id),
                                "user_id": ObjectId(str(user.id)),
                                "status": "active",
                            }
                        )
                        if member:
                            organization_role = member.get("role")

                user_info = {
                    "user_id": str(user.id),
                    "email": email,
                    "plan": getattr(user, "plan", "professional"),
                    "rate_limits": getattr(user, "limits", {}),
                    "organization_id": organization_id,
                    "organization_role": organization_role,
                    **admin_info,
                }
                logger.info("get_current_user: Successfully constructed user_info from cookie token")
                return user_info
            else:
                logger.warning(
                    "get_current_user: JWT token validation returned None (token may be expired or invalid). Path: %s, Token length: %d",
                    request.url.path,
                    len(cookie_token) if cookie_token else 0,
                )
        except HTTPException:
            raise
        except Exception as e:
            logger.warning("get_current_user: Cookie token validation failed with unexpected error: %s", e, exc_info=True)

    logger.info(
        "get_current_user: No cookie token or validation failed. Checking Authorization header: has_header=%s",
        bool(authorization),
    )
    
    if not authorization or not authorization.startswith("Bearer "):
        logger.warning(
            "get_current_user: No authentication found. Raising HTTPException. Path: %s",
            request.url.path,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    
    logger.info("get_current_user: Authorization header found, attempting API key validation")

    api_key_value = authorization.replace("Bearer ", "").strip()
    logger.info("get_current_user: Attempting API key validation")
    user_info = await get_user_from_api_key(api_key_value)

    if not user_info:
        logger.warning("get_current_user: API key validation failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    
    logger.info("get_current_user: API key validation successful")
    return user_info


async def get_current_user_for_request(request: Request) -> dict[str, Any]:
    """Get current user from request state (for middleware).

    Args:
        request: FastAPI request object

    Returns:
        Dictionary with user info or None
    """
    return getattr(request.state, "user_info", None)


async def require_admin(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Require admin access.

    Checks if the current user has admin privileges using RBAC system.

    Args:
        current_user: Current authenticated user from get_current_user dependency

    Returns:
        Dictionary with user info (guaranteed to have is_admin=True)

    Raises:
        HTTPException: If user is not an admin (403 Forbidden)
    """
    from api.auth.rbac import check_admin_access

    has_access, error_msg = check_admin_access(current_user)

    if not has_access:
        logger.warning(
            "Admin access denied for user %s (email: %s): %s",
            current_user.get("user_id"),
            current_user.get("email"),
            error_msg,
        )

        from api.models.audit_log import AuditEventType, AuditLogSeverity
        from api.services.audit_log_service import audit_log_service

        audit_log_service.log_event(
            event_type=AuditEventType.AUTHORIZATION_DENIED,
            severity=AuditLogSeverity.HIGH,
            message=f"Admin access denied for user {current_user.get('user_id')}: {error_msg}",
            success=False,
            user_id=current_user.get("user_id"),
            api_key_id=current_user.get("api_key_id"),
            organization_id=current_user.get("organization_id"),
            details={
                "reason": error_msg or "Admin access required",
                "user_email": current_user.get("email"),
                "user_plan": current_user.get("plan"),
                "admin_role": current_user.get("admin_role"),
                "admin_status": current_user.get("admin_status"),
            },
            compliance_tags=["PCI-DSS-10", "SOC2"],
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error_msg or "Admin access required",
        )

    return current_user


async def require_permission(
    permission: str,
    current_user: dict[str, Any] = Depends(require_admin),
) -> dict[str, Any]:
    """Require specific permission.

    Args:
        permission: Required permission name
        current_user: Current admin user from require_admin dependency

    Returns:
        Dictionary with user info (guaranteed to have permission)

    Raises:
        HTTPException: If user doesn't have permission (403 Forbidden)
    """
    from api.auth.rbac import get_user_permissions, has_permission

    is_super_admin = current_user.get("is_super_admin", False)
    user_permissions = get_user_permissions(current_user)

    if not has_permission(user_permissions, permission, is_super_admin):
        logger.warning(
            "Permission denied for user %s (email: %s): required %s",
            current_user.get("user_id"),
            current_user.get("email"),
            permission,
        )

        from api.models.audit_log import AuditEventType, AuditLogSeverity
        from api.services.audit_log_service import audit_log_service

        audit_log_service.log_event(
            event_type=AuditEventType.AUTHORIZATION_DENIED,
            severity=AuditLogSeverity.HIGH,
            message=f"Permission denied for user {current_user.get('user_id')}: {permission}",
            success=False,
            user_id=current_user.get("user_id"),
            api_key_id=current_user.get("api_key_id"),
            organization_id=current_user.get("organization_id"),
            details={
                "reason": f"Permission required: {permission}",
                "user_email": current_user.get("email"),
                "user_permissions": user_permissions,
                "admin_role": current_user.get("admin_role"),
            },
            compliance_tags=["PCI-DSS-10", "SOC2"],
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission required: {permission}",
        )

    return current_user


def require_permission_factory(permission: str):
    """Factory function to create a dependency that requires a specific permission.
    
    Args:
        permission: Required permission name
        
    Returns:
        Dependency function that checks for the specified permission
    """
    async def dependency(
        current_user: dict[str, Any] = Depends(require_admin),
    ) -> dict[str, Any]:
        return await require_permission(permission, current_user)
    
    return dependency


async def require_super_admin(
    current_user: dict[str, Any] = Depends(require_admin),
) -> dict[str, Any]:
    """Require super admin access.

    Args:
        current_user: Current admin user from require_admin dependency

    Returns:
        Dictionary with user info (guaranteed to be super admin)

    Raises:
        HTTPException: If user is not super admin (403 Forbidden)
    """
    is_super_admin = current_user.get("is_super_admin", False)

    if not is_super_admin:
        logger.warning(
            "Super admin access denied for user %s (email: %s)",
            current_user.get("user_id"),
            current_user.get("email"),
        )

        from api.models.audit_log import AuditEventType, AuditLogSeverity
        from api.services.audit_log_service import audit_log_service

        audit_log_service.log_event(
            event_type=AuditEventType.AUTHORIZATION_DENIED,
            severity=AuditLogSeverity.CRITICAL,
            message=f"Super admin access denied for user {current_user.get('user_id')}",
            success=False,
            user_id=current_user.get("user_id"),
            api_key_id=current_user.get("api_key_id"),
            organization_id=current_user.get("organization_id"),
            details={
                "reason": "Super admin access required",
                "user_email": current_user.get("email"),
                "admin_role": current_user.get("admin_role"),
            },
            compliance_tags=["PCI-DSS-10", "SOC2"],
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super admin access required",
        )

    return current_user

