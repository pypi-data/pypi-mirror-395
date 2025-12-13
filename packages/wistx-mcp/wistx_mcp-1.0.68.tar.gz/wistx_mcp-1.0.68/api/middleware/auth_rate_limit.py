"""Rate limiting specifically for authentication endpoints."""

import logging
import time
from typing import Callable
from collections import defaultdict, deque

from fastapi import Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

from api.database.redis_client import get_redis_manager
from api.utils.client_ip import get_real_client_ip

logger = logging.getLogger(__name__)


class AuthRateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting for authentication endpoints with exponential backoff."""

    def __init__(self, app, max_attempts: int = 5, window_minutes: int = 15):
        """Initialize auth rate limiter.

        Args:
            app: ASGI application
            max_attempts: Maximum failed attempts per window
            window_minutes: Time window in minutes
        """
        super().__init__(app)
        self.max_attempts = max_attempts
        self.window_seconds = window_minutes * 60
        self._failed_attempts: dict[str, deque[float]] = defaultdict(deque)
        self._redis_manager = None

    def _get_client_id(self, request: Request) -> str:
        """Get client identifier for rate limiting.

        Args:
            request: FastAPI request

        Returns:
            Client ID (IP address or user identifier)
        """
        user_info = getattr(request.state, "user_info", None)
        if user_info and "user_id" in user_info:
            return f"user:{user_info['user_id']}"

        ip = get_real_client_ip(request)
        return f"ip:{ip}"

    async def _check_rate_limit_redis(self, client_id: str) -> tuple[bool, int]:
        """Check rate limit using Redis.

        Args:
            client_id: Client identifier

        Returns:
            Tuple of (is_limited, retry_after_seconds)
        """
        try:
            redis_manager = await get_redis_manager()
            if not redis_manager:
                return self._check_rate_limit_memory(client_id)

            redis_client = await redis_manager.get_client()
            if not redis_client:
                return self._check_rate_limit_memory(client_id)

            key = f"auth_rate_limit:{client_id}"
            now = time.time()

            await redis_client.zremrangebyscore(
                key, 0, now - self.window_seconds
            )

            count = await redis_client.zcard(key)

            if count >= self.max_attempts:
                oldest = await redis_client.zrange(key, 0, 0, withscores=True)
                if oldest:
                    retry_after = int(self.window_seconds - (now - oldest[0][1]))
                    return True, max(0, retry_after)
                return True, self.window_seconds

            await redis_client.zadd(key, {str(now): now})
            await redis_client.expire(key, self.window_seconds)

            return False, 0

        except Exception as e:
            logger.warning("Redis rate limit check failed, using memory: %s", e)
            return self._check_rate_limit_memory(client_id)

    def _check_rate_limit_memory(self, client_id: str) -> tuple[bool, int]:
        """Check rate limit using in-memory storage.

        Args:
            client_id: Client identifier

        Returns:
            Tuple of (is_limited, retry_after_seconds)
        """
        now = time.time()
        attempts = self._failed_attempts[client_id]

        while attempts and attempts[0] < now - self.window_seconds:
            attempts.popleft()

        if len(attempts) >= self.max_attempts:
            retry_after = int(self.window_seconds - (now - attempts[0]))
            return True, max(0, retry_after)

        attempts.append(now)
        return False, 0

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with auth rate limiting.

        Args:
            request: FastAPI request
            call_next: Next middleware/handler

        Returns:
            Response object

        Raises:
            HTTPException: If rate limit exceeded
        """
        auth_paths = [
            "/auth/jwt/login",
            "/auth/jwt/register",
            "/auth/google/callback",
            "/auth/github/callback",
            "/v1/auth/api-keys",
        ]

        if not any(request.url.path.startswith(path) for path in auth_paths):
            return await call_next(request)

        client_id = self._get_client_id(request)
        is_limited, retry_after = await self._check_rate_limit_redis(client_id)

        if is_limited:
            logger.warning(
                "Auth rate limit exceeded for %s (retry after %d seconds)",
                client_id[:20],
                retry_after
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Too many authentication attempts",
                    "retry_after": retry_after,
                    "message": f"Please try again in {retry_after} seconds"
                },
                headers={"Retry-After": str(retry_after)}
            )

        response = await call_next(request)

        if response.status_code in (401, 403):
            await self._record_failed_attempt(client_id)

        return response

    async def _record_failed_attempt(self, client_id: str) -> None:
        """Record a failed authentication attempt.

        Args:
            client_id: Client identifier
        """
        try:
            redis_manager = await get_redis_manager()
            if redis_manager:
                redis_client = await redis_manager.get_client()
                if redis_client:
                    key = f"auth_rate_limit:{client_id}"
                    now = time.time()
                    await redis_client.zadd(key, {str(now): now})
                    await redis_client.expire(key, self.window_seconds)
                    return

            now = time.time()
            attempts = self._failed_attempts[client_id]
            attempts.append(now)

            while attempts and attempts[0] < now - self.window_seconds:
                attempts.popleft()

        except Exception as e:
            logger.error("Failed to record auth attempt: %s", e)

