"""Authentication and API key management endpoints."""

import logging
from datetime import datetime
from typing import Any

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Header, Request, Response, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
import jwt

from api.auth.api_keys import api_key_manager
from api.auth.users import fastapi_users, jwt_authentication, User
from api.dependencies import get_current_user
from api.dependencies.plan_enforcement import require_api_key_limit
from api.config import settings
from api.database.async_mongodb import async_mongodb_adapter
from api.auth.database import MongoDBUserDatabase
from api.auth.users import UserManager

get_current_active_user = fastapi_users.current_user(active=True)

logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer()


class TokenRefreshResponse(BaseModel):
    """Response model for token refresh."""

    access_token: str = Field(..., description="New JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class CreateAPIKeyRequest(BaseModel):
    """Request model for creating API key."""

    name: str = Field(..., min_length=1, max_length=100, description="API key name")
    description: str | None = Field(default=None, max_length=500, description="API key description")
    expires_at: datetime | None = Field(default=None, description="Expiration date (optional)")


class APIKeyResponse(BaseModel):
    """Response model for API key."""

    api_key: str = Field(..., description="API key (only shown once)")
    api_key_id: str = Field(..., description="API key ID")
    key_prefix: str = Field(..., description="Key prefix for display")
    created_at: str = Field(..., description="Creation timestamp")
    expires_at: str | None = Field(default=None, description="Expiration timestamp")


class APIKeyListResponse(BaseModel):
    """Response model for API key list."""

    api_keys: list[dict[str, Any]] = Field(..., description="List of API keys")


class RotateAPIKeyRequest(BaseModel):
    """Request model for rotating API key."""

    grace_period_hours: int = Field(default=24, ge=1, le=168, description="Grace period in hours (1-168, default: 24)")


async def check_api_key_limit_for_user(
    current_user_dict: dict[str, Any] = Depends(get_current_user),
) -> User:
    """Check API key limit and return User object.
    
    Uses cookie-based auth via get_current_user, then fetches User object.
    """
    from api.dependencies.plan_enforcement import require_api_key_limit
    
    await require_api_key_limit(current_user_dict)
    
    user_id = current_user_dict.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )
    
    await async_mongodb_adapter.connect()
    db = async_mongodb_adapter.get_database()
    collection = db.users
    user_db = MongoDBUserDatabase(collection)
    user_manager = UserManager(user_db)
    
    user = await user_manager.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive",
        )
    
    return user


@router.post("/api-keys", response_model=APIKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    request: CreateAPIKeyRequest,
    current_user: User = Depends(check_api_key_limit_for_user),
) -> APIKeyResponse:
    """Create new API key.

    Requires JWT token from OAuth login.
    Checks API key limit based on user's plan.
    """
    user_id = str(current_user.id)

    try:
        organization_id = str(current_user.organization_id) if current_user.organization_id else None
        result = await api_key_manager.create_api_key(
            user_id=user_id,
            name=request.name,
            description=request.description,
            organization_id=organization_id,
            expires_at=request.expires_at,
        )

        return APIKeyResponse(
            api_key=result["api_key"],
            api_key_id=result["api_key_id"],
            key_prefix=result["key_prefix"],
            created_at=result["created_at"],
            expires_at=result.get("expires_at"),
        )
    except Exception as e:
        logger.error("Error creating API key: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create API key",
        ) from e


@router.get("/api-keys", response_model=APIKeyListResponse)
async def list_api_keys(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIKeyListResponse:
    """List all API keys for current user."""
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    try:
        keys = await api_key_manager.list_api_keys(user_id=user_id)
        return APIKeyListResponse(api_keys=keys)
    except Exception as e:
        logger.error("Error listing API keys: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list API keys",
        ) from e


@router.post("/api-keys/{api_key_id}/rotate", response_model=APIKeyResponse, status_code=status.HTTP_200_OK)
async def rotate_api_key(
    api_key_id: str,
    request: RotateAPIKeyRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIKeyResponse:
    """Rotate API key with grace period.

    Creates a new API key and allows the old key to work during grace period.
    Sends in-app notification to user about the rotation.
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    try:
        result = await api_key_manager.rotate_api_key(
            user_id=user_id,
            key_id=api_key_id,
            grace_period_hours=request.grace_period_hours,
        )

        return APIKeyResponse(
            api_key=result["api_key"],
            api_key_id=result["api_key_id"],
            key_prefix=result["key_prefix"],
            created_at=result["created_at"],
            expires_at=result.get("expires_at"),
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error rotating API key: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to rotate API key",
        ) from e


@router.delete("/api-keys/{api_key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_api_key(
    api_key_id: str,
    request: Request,
    current_user: dict[str, Any] = Depends(get_current_user),
    reason: str | None = None,
) -> Response:
    """Revoke API key."""
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    try:
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")

        success = await api_key_manager.revoke_api_key(
            api_key_id=api_key_id,
            user_id=user_id,
            reason=reason,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API key not found or access denied",
            )
        
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error revoking API key: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to revoke API key",
        ) from e


async def get_user_from_expired_token(
    request: Request,
    authorization: str | None = Header(None),
) -> User:
    """Get user from JWT token, allowing expired tokens for refresh.
    
    Checks both Authorization header and httpOnly cookie for token.
    
    Args:
        request: FastAPI Request object
        authorization: Authorization header value
        
    Returns:
        User object
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    from api.utils.cookies import get_auth_token_from_cookie
    
    token = None
    
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "").strip()
    else:
        cookie_token = get_auth_token_from_cookie(request)
        if cookie_token:
            token = cookie_token
    
    if not token:
        logger.warning("No token provided for refresh (checked header and cookie)")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token required",
        )
    
    token_parts = token.split(".")
    if len(token_parts) != 3:
        logger.warning("Invalid token format for refresh: token has %d segments (expected 3), token length: %d", len(token_parts), len(token))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
        )
    
    try:
        decoded = jwt.decode(
            token,
            settings.secret_key,
            algorithms=["HS256"],
            options={"verify_exp": False, "verify_aud": False},
        )
        
        exp_timestamp = decoded.get("exp")
        if exp_timestamp:
            import time
            token_age_seconds = time.time() - exp_timestamp
            max_refresh_window_seconds = settings.jwt_refresh_window_days * 24 * 60 * 60
            
            if token_age_seconds > max_refresh_window_seconds:
                logger.warning(
                    "Token refresh attempted after window expired: age=%.0f days, max=%d days",
                    token_age_seconds / (24 * 60 * 60),
                    settings.jwt_refresh_window_days,
                )
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token too old to refresh. Please re-authenticate.",
                )
        
        user_id = decoded.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID",
            )
        
        await async_mongodb_adapter.connect()
        db = async_mongodb_adapter.get_database()
        collection = db.users
        user_db = MongoDBUserDatabase(collection)
        user_manager = UserManager(user_db)
        
        user = await user_manager.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is inactive",
            )
        
        return user
    except jwt.InvalidTokenError as e:
        logger.warning("Invalid token for refresh: %s", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from e
    except Exception as e:
        logger.error("Error getting user from expired token: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to validate token",
        ) from e


@router.post("/refresh")
async def refresh_token(
    request: Request,
    response: Response,
    current_user: User = Depends(get_user_from_expired_token),
) -> dict[str, str] | TokenRefreshResponse:
    """Refresh JWT access token.

    Generates a new JWT token for the authenticated user.
    Sets token in httpOnly cookie if possible, otherwise returns in response body.
    Allows expired tokens (within reasonable time) for refresh.
    """
    try:
        jwt_strategy = jwt_authentication.get_strategy()
        new_token = await jwt_strategy.write_token(current_user)

        if not new_token or not isinstance(new_token, str):
            logger.error("Invalid token generated for user: %s", current_user.id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate token",
            )

        from api.models.audit_log import AuditEventType, AuditLogSeverity
        from api.services.audit_log_service import audit_log_service
        from api.utils.cookies import set_auth_cookie_safe

        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")

        cookie_success, fallback_token = set_auth_cookie_safe(
            response, new_token, fallback_to_header=True
        )

        audit_log_service.log_event(
            event_type=AuditEventType.TOKEN_REFRESHED,
            severity=AuditLogSeverity.LOW,
            message=f"Token refreshed for user {current_user.id}",
            success=True,
            user_id=str(current_user.id),
            organization_id=str(current_user.organization_id) if current_user.organization_id else None,
            ip_address=ip_address,
            user_agent=user_agent,
            endpoint="/v1/auth/refresh",
            method="POST",
            details={
                "auth_method": "jwt",
                "cookie_set": cookie_success,
                "token_size": len(new_token),
            },
            compliance_tags=["PCI-DSS-10", "SOC2"],
        )

        logger.info(
            "Token refreshed for user: %s (cookie_set: %s, token_size: %d)",
            current_user.id,
            cookie_success,
            len(new_token),
        )

        if cookie_success:
            return {"status": "success", "message": "Token refreshed"}
        else:
            if not fallback_token:
                logger.error("Cookie setting failed and no fallback token available")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to set authentication cookie",
                )
            return TokenRefreshResponse(
                access_token=fallback_token,
                token_type="bearer",
            )
    except HTTPException:
        raise
    except ValueError as e:
        logger.error("Token validation error during refresh: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token validation failed",
        ) from e
    except Exception as e:
        logger.error("Error refreshing token: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to refresh token",
        ) from e


@router.get("/sync")
async def sync_auth_token(
    request: Request,
    response: Response,
    token: str | None = None,
) -> dict[str, str]:
    """Sync authentication token from OAuth callback (development only).
    
    This endpoint is used in development to exchange a temporary token
    from the OAuth callback for a cookie that works with the proxy.
    
    Args:
        token: Temporary JWT token from OAuth callback (dev only)
        
    Returns:
        Success message
    """
    from api.config import settings
    from api.utils.cookies import set_auth_cookie_safe
    
    if not settings.debug:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is only available in development",
        )
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token parameter is required",
        )
    
    if len(token) > 4096:
        logger.warning("Token length exceeds maximum size: %d", len(token))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token format",
        )
    
    try:
        from api.database.async_mongodb import async_mongodb_adapter
        await async_mongodb_adapter.connect()
        db = async_mongodb_adapter.get_database()
        collection = db.users
        user_db = MongoDBUserDatabase(collection)
        user_manager = UserManager(user_db)
        
        strategy = jwt_authentication.get_strategy()
        user = await strategy.read_token(token, user_manager)
        
        if not user:
            logger.warning(
                "Invalid token provided to sync endpoint: token_length=%d",
                len(token),
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )
        
        cookie_success, _ = set_auth_cookie_safe(
            response, token, fallback_to_header=False
        )
        
        if not cookie_success:
            logger.error("Failed to set cookie in sync endpoint for user: %s", user.id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to set authentication cookie",
            )
        
        from api.models.audit_log import AuditEventType, AuditLogSeverity
        from api.services.audit_log_service import audit_log_service
        
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        
        audit_log_service.log_event(
            event_type=AuditEventType.AUTHENTICATION_SUCCESS,
            severity=AuditLogSeverity.LOW,
            message=f"Token synced for user {user.id} (dev mode)",
            success=True,
            user_id=str(user.id),
            organization_id=str(user.organization_id) if user.organization_id else None,
            ip_address=ip_address,
            user_agent=user_agent,
            endpoint="/v1/auth/sync",
            method="GET",
            details={
                "auth_method": "oauth_sync",
                "cookie_set": cookie_success,
                "dev_mode": True,
            },
            compliance_tags=["PCI-DSS-10", "SOC2"],
        )
        
        logger.info(
            "Token synced successfully for user: %s (cookie_set: %s)",
            user.id,
            cookie_success,
        )
        
        return {"status": "success", "message": "Authentication token synced"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error syncing token: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to sync authentication token",
        ) from e


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, str]:
    """Logout user and clear authentication cookie.
    
    Clears the authentication cookie and optionally revokes tokens.
    
    Args:
        request: FastAPI Request object
        response: FastAPI Response object
        current_user: Current authenticated user
        
    Returns:
        Success status
    """
    from api.models.audit_log import AuditEventType, AuditLogSeverity
    from api.services.audit_log_service import audit_log_service
    from api.utils.cookies import clear_auth_cookie, REFRESH_COOKIE_NAME
    
    clear_auth_cookie(response)
    clear_auth_cookie(response, cookie_name=REFRESH_COOKIE_NAME)
    
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    
    audit_log_service.log_event(
        event_type=AuditEventType.AUTHENTICATION_LOGOUT,
        severity=AuditLogSeverity.LOW,
        message=f"User {current_user.get('user_id')} logged out",
        success=True,
        user_id=current_user.get("user_id"),
        organization_id=current_user.get("organization_id"),
        ip_address=ip_address,
        user_agent=user_agent,
        endpoint="/v1/auth/logout",
        method="POST",
        compliance_tags=["PCI-DSS-10", "SOC2"],
    )
    
    logger.info("User logged out: %s", current_user.get("user_id"))
    
    return {"status": "success", "message": "Logged out successfully"}

