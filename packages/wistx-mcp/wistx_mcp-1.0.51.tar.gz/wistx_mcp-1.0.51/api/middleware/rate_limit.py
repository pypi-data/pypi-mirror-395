"""Rate limiting middleware for FastAPI with Redis and plan-based limits."""

import logging
import time
from collections import defaultdict, deque
from typing import Any, Callable

from fastapi import Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from api.config import settings
from api.database.redis_client import get_redis_manager, RedisCircuitBreakerOpenError
from api.services.plan_service import plan_service
from api.utils.client_ip import get_real_client_ip

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware with Redis support and plan-based limits.

    Supports both in-memory (single instance) and Redis-based (distributed) rate limiting.
    Uses plan-based limits from plan_service.
    """

    def __init__(self, app: ASGIApp, requests_per_minute: int | None = None):
        """Initialize rate limiting middleware.

        Args:
            app: ASGI application
            requests_per_minute: Default requests per minute (fallback if plan not found)
        """
        super().__init__(app)
        default_limit = requests_per_minute or settings.rate_limit_requests_per_minute
        if settings.debug:
            self.default_requests_per_minute = max(default_limit, 300)
        else:
            self.default_requests_per_minute = default_limit
        self.window_seconds = 60
        self.request_times: dict[str, deque[float]] = defaultdict(self._create_deque)
        self.redis_manager = None
        self.use_redis = False

    @staticmethod
    def _create_deque() -> deque[float]:
        """Create a new deque for rate limiting."""
        return deque()

    def _get_client_id(self, request: Request) -> str:
        """Get client identifier for rate limiting.

        Args:
            request: FastAPI request object

        Returns:
            Client identifier (user_id if available, otherwise IP or API key)
        """
        user_info = getattr(request.state, "user_info", None)
        if user_info and user_info.get("user_id"):
            return f"user:{user_info['user_id']}"

        client_ip = get_real_client_ip(request)

        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            api_key = auth_header.replace("Bearer ", "")
            return f"api_key:{api_key[:16]}"

        return f"ip:{client_ip}"

    def _get_plan_limit(self, request: Request) -> int:
        """Get rate limit for user's plan.

        Args:
            request: FastAPI request object

        Returns:
            Requests per minute limit
        """
        user_info = getattr(request.state, "user_info", None)
        if user_info:
            plan = user_info.get("plan", "professional")
            plan_limits = plan_service.get_plan_limits(plan)
            if plan_limits:
                return plan_limits.requests_per_minute

        return self.default_requests_per_minute

    def _is_rate_limited_in_memory(self, client_id: str, limit: int) -> bool:
        """Check if client is rate limited (in-memory).

        Args:
            client_id: Client identifier
            limit: Requests per minute limit

        Returns:
            True if rate limited, False otherwise
        """
        now = time.time()
        window_start = now - self.window_seconds

        request_times = self.request_times[client_id]

        while request_times and request_times[0] < window_start:
            request_times.popleft()

        if len(request_times) >= limit:
            return True

        request_times.append(now)
        return False

    async def _ensure_redis_manager(self) -> None:
        """Ensure Redis manager is initialized."""
        if self.redis_manager is None:
            self.redis_manager = await get_redis_manager()
            self.use_redis = self.redis_manager is not None

    async def _is_rate_limited_redis(self, client_id: str, limit: int) -> bool:
        """Check if client is rate limited (Redis).

        Args:
            client_id: Client identifier
            limit: Requests per minute limit

        Returns:
            True if rate limited, False otherwise
        """
        await self._ensure_redis_manager()

        if not self.redis_manager:
            return False

        try:
            key = f"rate_limit:{client_id}"
            now = time.time()
            window_start = now - self.window_seconds

            async def _check_rate_limit(client: Any) -> bool:
                pipe = client.pipeline()
                pipe.zremrangebyscore(key, 0, window_start)
                pipe.zcard(key)
                pipe.zadd(key, {str(now): now})
                pipe.expire(key, self.window_seconds + 10)

                results = await pipe.execute()
                current_count = results[1] if len(results) > 1 else 0

                return current_count >= limit

            return await self.redis_manager.execute(_check_rate_limit)
        except RedisCircuitBreakerOpenError:
            logger.warning("Redis circuit breaker open, falling back to in-memory rate limiting")
            return self._is_rate_limited_in_memory(client_id, limit)
        except Exception as e:
            logger.warning("Redis rate limit check failed: %s. Falling back to in-memory.", e)
            return self._is_rate_limited_in_memory(client_id, limit)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with rate limiting.

        Args:
            request: FastAPI request object
            call_next: Next middleware/handler

        Returns:
            Response object

        Raises:
            HTTPException: If rate limit exceeded
        """
        # Skip rate limiting only if explicitly disabled via DISABLE_RATE_LIMIT env var
        # Note: This is decoupled from DEBUG mode to ensure rate limiting stays enabled
        # in production even if DEBUG is accidentally left on
        if settings.disable_rate_limit:
            logger.debug("Rate limiting explicitly disabled via DISABLE_RATE_LIMIT")
            return await call_next(request)

        if (
            request.url.path.startswith("/health")
            or request.url.path.startswith("/docs")
            or request.url.path.startswith("/auth/")
            or request.url.path.startswith("/v1/auth/sync")
            or request.method == "OPTIONS"
        ):
            return await call_next(request)

        client_id = self._get_client_id(request)
        limit = self._get_plan_limit(request)

        is_limited = False
        if self.use_redis:
            is_limited = await self._is_rate_limited_redis(client_id, limit)
        else:
            is_limited = self._is_rate_limited_in_memory(client_id, limit)

        if is_limited:
            logger.warning(
                "Rate limit exceeded for client: %s (limit: %d/min) | Path: %s",
                client_id,
                limit,
                request.url.path,
            )

            from api.models.audit_log import AuditEventType, AuditLogSeverity
            from api.services.audit_log_service import audit_log_service

            user_info = getattr(request.state, "user_info", None)
            ip_address = request.client.host if request.client else None
            user_agent = request.headers.get("user-agent")
            request_id = getattr(request.state, "request_id", None)

            audit_log_service.log_event(
                event_type=AuditEventType.RATE_LIMIT_EXCEEDED,
                severity=AuditLogSeverity.MEDIUM,
                message=f"Rate limit exceeded for {client_id}: {limit} req/min",
                success=False,
                user_id=user_info.get("user_id") if user_info else None,
                api_key_id=user_info.get("api_key_id") if user_info else None,
                organization_id=user_info.get("organization_id") if user_info else None,
                ip_address=ip_address,
                user_agent=user_agent,
                request_id=request_id,
                endpoint=request.url.path,
                method=request.method,
                status_code=429,
                details={
                    "client_id": client_id,
                    "limit": limit,
                    "path": request.url.path,
                },
                compliance_tags=["PCI-DSS-10", "SOC2"],
            )

            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": f"Rate limit exceeded. Maximum {limit} requests per minute.",
                        "details": {
                            "limit": limit,
                            "window_seconds": self.window_seconds,
                        },
                    }
                },
                headers={
                    "X-RateLimit-Limit": str(limit),
                    "X-RateLimit-Window": str(self.window_seconds),
                    "Retry-After": str(self.window_seconds),
                },
            )

        response = await call_next(request)

        remaining = limit
        if self.use_redis and self.redis_manager:
            try:
                key = f"rate_limit:{client_id}"

                async def _get_count(client: Any) -> int:
                    return await client.zcard(key)

                count = await self.redis_manager.execute(_get_count)
                remaining = max(0, limit - count)
            except Exception:
                remaining = limit - 1
        else:
            remaining = max(0, limit - len(self.request_times[client_id]))

        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Window"] = str(self.window_seconds)

        return response
