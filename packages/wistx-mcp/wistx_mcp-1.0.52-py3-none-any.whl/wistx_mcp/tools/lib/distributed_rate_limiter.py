"""Distributed rate limiting using Redis (Google Memorystore) for Cloud Run horizontal scaling."""

import asyncio
import logging
import time
from typing import Any, Optional

from wistx_mcp.tools.lib.constants import (
    MAX_RATE_LIMIT_CALLS,
    RATE_LIMIT_WINDOW_SECONDS,
)

logger = logging.getLogger(__name__)

_redis_client: Optional[Any] = None
_redis_lock = asyncio.Lock()


async def get_redis_client():
    """Get Redis client for distributed rate limiting.

    Returns:
        Redis client instance or None if Redis not configured
    """
    global _redis_client

    if _redis_client is not None:
        return _redis_client

    async with _redis_lock:
        if _redis_client is not None:
            return _redis_client

        from wistx_mcp.config import settings

        if not settings.memorystore_enabled and not settings.redis_url:
            logger.debug("Distributed rate limiting disabled (no Redis/Memorystore configured)")
            return None

        try:
            import redis.asyncio as redis

            socket_connect_timeout = 5
            socket_timeout = 5

            if settings.redis_url:
                _redis_client = redis.from_url(
                    settings.redis_url,
                    encoding="utf-8",
                    decode_responses=True,
                    socket_connect_timeout=socket_connect_timeout,
                    socket_timeout=socket_timeout,
                )
                logger.info("Redis client initialized from REDIS_URL for distributed rate limiting")
            elif settings.memorystore_host:
                socket_connect_timeout = 10
                socket_timeout = 10
                
                _redis_client = redis.Redis(
                    host=settings.memorystore_host,
                    port=settings.memorystore_port,
                    encoding="utf-8",
                    decode_responses=True,
                    socket_connect_timeout=socket_connect_timeout,
                    socket_timeout=socket_timeout,
                    socket_keepalive=True,
                    socket_keepalive_options={
                        1: 1,
                        3: 10,
                        4: 1,
                    },
                    health_check_interval=30,
                    retry_on_timeout=True,
                    single_connection_client=False,
                )
                logger.info(
                    "Redis client initialized for Memorystore at %s:%d (connect_timeout=%d, socket_timeout=%d)",
                    settings.memorystore_host,
                    settings.memorystore_port,
                    socket_connect_timeout,
                    socket_timeout,
                )
            else:
                logger.warning("Memorystore enabled but host not configured")
                return None

            max_connect_retries = 3
            connect_retry_delay = 2.0
            
            for attempt in range(max_connect_retries):
                try:
                    await asyncio.wait_for(
                        _redis_client.ping(),
                        timeout=socket_connect_timeout + 5,
                    )
                    break
                except Exception as e:
                    if attempt < max_connect_retries - 1:
                        logger.debug(
                            "Redis connection attempt %d/%d failed, retrying in %.1fs: %s",
                            attempt + 1,
                            max_connect_retries,
                            connect_retry_delay,
                            e,
                        )
                        await asyncio.sleep(connect_retry_delay)
                        connect_retry_delay *= 1.5
                    else:
                        raise
            logger.info("Successfully connected to Redis/Memorystore for distributed rate limiting")

            try:
                from wistx_mcp.tools.lib.resource_manager import get_resource_manager

                resource_manager = await get_resource_manager()
                resource_manager.register_redis_client(_redis_client)
            except Exception as e:
                logger.debug("Could not register Redis client with resource manager: %s", e)

            return _redis_client

        except ImportError:
            logger.warning(
                "redis package not installed. Install with: pip install redis. "
                "Falling back to in-memory rate limiting."
            )
            return None
        except Exception as e:
            logger.debug(
                "Failed to connect to Redis/Memorystore: %s. Falling back to in-memory rate limiting.",
                e,
            )
            return None


class DistributedRateLimiter:
    """Distributed rate limiter using Redis sorted sets for Cloud Run horizontal scaling.

    Uses Redis sorted sets (ZSET) for efficient time-window queries.
    All instances share the same rate limit counters.
    """

    def __init__(
        self,
        max_calls: int = MAX_RATE_LIMIT_CALLS,
        window_seconds: int = RATE_LIMIT_WINDOW_SECONDS,
    ):
        """Initialize distributed rate limiter.

        Args:
            max_calls: Maximum number of calls per window
            window_seconds: Time window in seconds
        """
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self._redis_client: Optional[Any] = None

    async def _ensure_redis_client(self) -> Optional[Any]:
        """Ensure Redis client is initialized.

        Returns:
            Redis client or None if not available
        """
        if self._redis_client is None:
            self._redis_client = await get_redis_client()
        return self._redis_client

    async def check_rate_limit(self, identifier: str) -> bool:
        """Check if rate limit allows the call using Redis sorted sets.

        Args:
            identifier: Unique identifier (user_id:tool_hash)

        Returns:
            True if allowed, False if rate limited
        """
        redis_client = await self._ensure_redis_client()
        if not redis_client:
            return True

        try:
            key = f"rate_limit:{identifier}"
            now = time.time()
            window_start = now - self.window_seconds

            pipe = redis_client.pipeline()
            pipe.zremrangebyscore(key, 0, window_start)
            pipe.zcard(key)
            pipe.expire(key, self.window_seconds + 10)

            results = await pipe.execute()
            current_count = results[1] if len(results) > 1 else 0

            if current_count >= self.max_calls:
                logger.warning(
                    "Rate limit exceeded for %s: %d calls in %d seconds (distributed)",
                    identifier[:16],
                    current_count,
                    self.window_seconds,
                )
                return False

            await redis_client.zadd(key, {str(now): now})
            return True

        except Exception as e:
            logger.debug(
                "Redis rate limit check failed: %s. Allowing request (fail-open).",
                e,
            )
            return True

    async def get_remaining_calls(self, identifier: str) -> int:
        """Get remaining calls for an identifier.

        Args:
            identifier: Identifier to check

        Returns:
            Number of remaining calls
        """
        redis_client = await self._ensure_redis_client()
        if not redis_client:
            return self.max_calls

        try:
            key = f"rate_limit:{identifier}"
            now = time.time()
            window_start = now - self.window_seconds

            await redis_client.zremrangebyscore(key, 0, window_start)
            current_count = await redis_client.zcard(key)

            return max(0, self.max_calls - current_count)

        except Exception as e:
            logger.debug("Redis get_remaining_calls failed: %s", e)
            return self.max_calls

    async def reset(self, identifier: str) -> None:
        """Reset rate limit for an identifier.

        Args:
            identifier: Identifier to reset
        """
        redis_client = await self._ensure_redis_client()
        if not redis_client:
            return

        try:
            key = f"rate_limit:{identifier}"
            await redis_client.delete(key)
        except Exception as e:
            logger.debug("Redis reset failed: %s", e)

    async def close(self) -> None:
        """Close Redis connection."""
        if self._redis_client:
            try:
                await self._redis_client.aclose()
            except Exception as e:
                logger.warning("Error closing Redis client: %s", e)
            finally:
                self._redis_client = None


_global_distributed_rate_limiter: Optional[DistributedRateLimiter] = None


async def get_distributed_rate_limiter(
    max_calls: int = MAX_RATE_LIMIT_CALLS,
    window_seconds: int = RATE_LIMIT_WINDOW_SECONDS,
) -> Optional[DistributedRateLimiter]:
    """Get global distributed rate limiter instance.

    Args:
        max_calls: Maximum calls per window
        window_seconds: Time window in seconds

    Returns:
        DistributedRateLimiter instance or None if Redis not configured
    """
    global _global_distributed_rate_limiter

    if _global_distributed_rate_limiter is None:
        _global_distributed_rate_limiter = DistributedRateLimiter(
            max_calls=max_calls,
            window_seconds=window_seconds,
        )

    return _global_distributed_rate_limiter

