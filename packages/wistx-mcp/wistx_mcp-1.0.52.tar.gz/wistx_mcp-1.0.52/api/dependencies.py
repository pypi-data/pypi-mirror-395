"""Shared dependencies."""

import logging
from typing import Annotated, Any

from fastapi import Header, HTTPException, Request, status, Depends

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
    """Extract user information from JWT token or API key.

    First checks request.state.user_info (set by AuthenticationMiddleware for JWT tokens),
    then falls back to API key validation.

    Args:
        request: FastAPI request object
        authorization: Authorization header value

    Returns:
        Dictionary with user_id, organization_id, plan, rate_limits, etc.

    Raises:
        HTTPException: If authentication is invalid or missing
    """
    user_info = getattr(request.state, "user_info", None)
    if user_info:
        return user_info

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header. Expected 'Bearer {token}'",
        )

    api_key_value = authorization.replace("Bearer ", "").strip()
    user_info = await get_user_from_api_key(api_key_value)

    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return user_info


async def get_current_user_for_request(request: Request) -> dict[str, Any]:
    """Get current user from request state (for middleware).

    Args:
        request: FastAPI request object

    Returns:
        Dictionary with user info or None
    """
    return getattr(request.state, "user_info", None)

