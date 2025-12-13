"""Organization-level rate limiting middleware."""

import logging
from typing import Any

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from api.database.redis_client import get_redis_client
from api.dependencies.auth import get_current_user

logger = logging.getLogger(__name__)

DEFAULT_ORGANIZATION_RATE_LIMIT = 1000
DEFAULT_RATE_LIMIT_WINDOW = 60


class OrganizationRateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for organization-level rate limiting.

    Prevents DDoS attacks and ensures fair resource distribution across team members.
    """

    def __init__(
        self,
        app: Any,
        limit: int = DEFAULT_ORGANIZATION_RATE_LIMIT,
        window_seconds: int = DEFAULT_RATE_LIMIT_WINDOW,
    ):
        """Initialize organization rate limit middleware.

        Args:
            app: FastAPI application
            limit: Request limit per window (default: 1000 requests per minute)
            window_seconds: Time window in seconds (default: 60 seconds)
        """
        super().__init__(app)
        self.limit = limit
        self.window_seconds = window_seconds
        self._redis_client = None

    async def _get_redis_client(self):
        """Get Redis client for rate limiting.

        Returns:
            Redis client or None if not configured
        """
        if self._redis_client is None:
            try:
                self._redis_client = await get_redis_client()
            except Exception as e:
                logger.debug("Redis not available for rate limiting: %s", e)
                self._redis_client = None
        return self._redis_client

    async def _check_rate_limit(
        self,
        organization_id: str,
        endpoint: str,
    ) -> bool:
        """Check if organization has exceeded rate limit.

        Args:
            organization_id: Organization ID
            endpoint: API endpoint

        Returns:
            True if within limit, False if exceeded
        """
        redis_client = await self._get_redis_client()
        if not redis_client:
            return True

        key = f"rate_limit:org:{organization_id}:{endpoint}"

        try:
            current = await redis_client.get(key)
            if current and int(current) >= self.limit:
                return False

            pipe = redis_client.pipeline()
            pipe.incr(key)
            pipe.expire(key, self.window_seconds)
            await pipe.execute()
            return True
        except Exception as e:
            logger.warning("Rate limit check failed: %s", e)
            return True

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        """Process request with organization rate limiting.

        Args:
            request: FastAPI request
            call_next: Next middleware/handler

        Returns:
            Response

        Raises:
            HTTPException: If rate limit exceeded
        """
        if request.url.path.startswith("/health") or request.url.path.startswith("/docs"):
            return await call_next(request)

        try:
            user_info = getattr(request.state, "user_info", None)
            if not user_info:
                return await call_next(request)

            organization_id = user_info.get("organization_id")
            if not organization_id:
                return await call_next(request)

            allowed = await self._check_rate_limit(str(organization_id), request.url.path)
            if not allowed:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Organization rate limit exceeded: {self.limit} requests per {self.window_seconds} seconds",
                    headers={"Retry-After": str(self.window_seconds)},
                )

        except HTTPException:
            raise
        except Exception as e:
            logger.warning("Rate limit middleware error: %s", e)

        return await call_next(request)

