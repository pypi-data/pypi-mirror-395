"""Waitlist middleware to block auth routes when waitlist is enabled."""

import logging
from typing import Callable

from fastapi import Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

from api.config import settings

logger = logging.getLogger(__name__)


class WaitlistMiddleware(BaseHTTPMiddleware):
    """Middleware to block auth routes when waitlist mode is enabled."""

    def __init__(self, app):
        """Initialize waitlist middleware.

        Args:
            app: ASGI application
        """
        super().__init__(app)
        self.blocked_paths = {
            "/auth/",
            "/v1/auth/",
        }
        self.allowed_paths = {
            "/v1/waitlist/",
            "/health",
            "/docs",
            "/redoc",
            "/openapi.json",
        }
        # Auth paths that should be allowed for already-authenticated users
        # These endpoints are needed to maintain existing sessions
        self.authenticated_user_allowed_paths = {
            "/v1/auth/refresh",
            "/v1/auth/logout",
            "/v1/auth/me",
            "/v1/auth/sync",
            "/auth/refresh",
            "/auth/logout",
            "/auth/me",
            "/auth/sync",
        }

    def _is_authenticated(self, request: Request) -> bool:
        """Check if the request is from an authenticated user.

        Args:
            request: FastAPI request object

        Returns:
            True if user is authenticated, False otherwise
        """
        # Check if auth middleware has set the user_info on request state
        # Note: AuthenticationMiddleware sets request.state.user_info, not request.state.user
        return hasattr(request.state, "user_info") and request.state.user_info is not None

    def _is_blocked_path(self, request: Request) -> bool:
        """Check if path should be blocked when waitlist is enabled.

        Args:
            request: FastAPI request object

        Returns:
            True if path should be blocked, False otherwise
        """
        if not settings.enable_waitlist:
            return False

        path = request.url.path

        if any(path.startswith(allowed) for allowed in self.allowed_paths):
            return False

        # Allow authenticated users to access session management endpoints
        # (refresh, logout, me, sync) even when waitlist is enabled
        if self._is_authenticated(request):
            if any(path.startswith(allowed) for allowed in self.authenticated_user_allowed_paths):
                logger.debug(
                    "Allowing authenticated user to access: path=%s",
                    path,
                )
                return False

        return any(path.startswith(blocked) for blocked in self.blocked_paths)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and block auth routes if waitlist is enabled.

        Args:
            request: FastAPI request object
            call_next: Next middleware/handler

        Returns:
            Response object

        Raises:
            HTTPException: If waitlist is enabled and trying to access auth routes
        """
        if self._is_blocked_path(request):
            logger.info(
                "Blocked auth route access: path=%s (waitlist enabled, user not authenticated)",
                request.url.path,
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "waitlist_enabled",
                    "message": "Access is currently limited. Please join the waitlist to be notified when access is available.",
                },
            )

        return await call_next(request)

