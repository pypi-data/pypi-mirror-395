"""Distributed concurrent request limiting using Redis for Cloud Run horizontal scaling."""

import logging
import time
import uuid
from typing import Any, Optional

from wistx_mcp.tools.lib.constants import (
    MAX_CONCURRENT_TOOLS,
    CONCURRENT_LIMITER_TIMEOUT_SECONDS,
)

logger = logging.getLogger(__name__)


async def get_redis_client():
    """Get Redis client for distributed concurrent limiting.

    Reuses the same Redis client from distributed_rate_limiter.

    Returns:
        Redis client instance or None if Redis not configured
    """
    from wistx_mcp.tools.lib.distributed_rate_limiter import get_redis_client as get_rate_limiter_redis

    return await get_rate_limiter_redis()


class DistributedConcurrentLimiter:
    """Distributed concurrent request limiter using Redis for Cloud Run scaling.

    Tracks concurrent requests per user globally across all instances.
    Uses Redis atomic counters (INCR/DECR) for thread-safe operations.
    """

    def __init__(self, max_concurrent: int = MAX_CONCURRENT_TOOLS):
        """Initialize distributed concurrent limiter.

        Args:
            max_concurrent: Maximum concurrent executions per user globally
        """
        self.max_concurrent = max_concurrent
        self._redis_client: Optional[Any] = None
        self._instance_id = str(uuid.uuid4())[:8]

    async def _ensure_redis_client(self) -> Optional[Any]:
        """Ensure Redis client is initialized.

        Returns:
            Redis client or None if not available
        """
        if self._redis_client is None:
            self._redis_client = await get_redis_client()
        return self._redis_client

    async def acquire(self, user_id: str) -> bool:
        """Acquire a slot for concurrent execution.

        Uses Redis Lua script for atomic check-and-increment operation.

        Args:
            user_id: User identifier

        Returns:
            True if slot acquired, False if limit exceeded
        """
        redis_client = await self._ensure_redis_client()
        if not redis_client:
            return True

        key = f"concurrent:{user_id}"

        lua_script = """
        local key = KEYS[1]
        local max_concurrent = tonumber(ARGV[1])
        local ttl = tonumber(ARGV[2])
        
        local current = redis.call('GET', key)
        if current == false then
            current = 0
        else
            current = tonumber(current)
        end
        
        if current >= max_concurrent then
            return 0
        end
        
        redis.call('INCR', key)
        redis.call('EXPIRE', key, ttl)
        return 1
        """

        try:
            result = await redis_client.eval(
                lua_script,
                1,
                key,
                str(self.max_concurrent),
                "300",
            )

            if result == 0:
                logger.warning(
                    "Concurrent limit exceeded for %s: %d/%d (distributed)",
                    user_id[:16],
                    await self.get_current_count(user_id),
                    self.max_concurrent,
                )
                return False

            return True

        except Exception as e:
            logger.debug(
                "Redis concurrent limit check failed: %s. Allowing request (fail-open).",
                e,
            )
            return True

    async def release(self, user_id: str) -> None:
        """Release a slot after execution completes.

        Uses Redis atomic DECR to decrement counter.

        Args:
            user_id: User identifier
        """
        redis_client = await self._ensure_redis_client()
        if not redis_client:
            return

        key = f"concurrent:{user_id}"

        try:
            count = await redis_client.decr(key)
            if count <= 0:
                await redis_client.delete(key)
        except Exception as e:
            logger.debug("Redis concurrent limit release failed: %s", e)

    async def get_current_count(self, user_id: str) -> int:
        """Get current concurrent count for a user.

        Args:
            user_id: User identifier

        Returns:
            Current concurrent count
        """
        redis_client = await self._ensure_redis_client()
        if not redis_client:
            return 0

        key = f"concurrent:{user_id}"

        try:
            count = await redis_client.get(key)
            return int(count) if count else 0
        except Exception as e:
            logger.debug("Redis get concurrent count failed: %s", e)
            return 0


_global_distributed_concurrent_limiter: Optional[DistributedConcurrentLimiter] = None


async def get_distributed_concurrent_limiter(
    max_concurrent: int = MAX_CONCURRENT_TOOLS,
) -> Optional[DistributedConcurrentLimiter]:
    """Get global distributed concurrent limiter instance.

    Args:
        max_concurrent: Maximum concurrent executions per user globally

    Returns:
        DistributedConcurrentLimiter instance or None if Redis not configured
    """
    global _global_distributed_concurrent_limiter

    if _global_distributed_concurrent_limiter is None:
        _global_distributed_concurrent_limiter = DistributedConcurrentLimiter(
            max_concurrent=max_concurrent,
        )

    return _global_distributed_concurrent_limiter

