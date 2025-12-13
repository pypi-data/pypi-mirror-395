"""Rate limiting for MCP tool calls with TTL-based cleanup and distributed Redis support."""

import asyncio
import logging
import time
from typing import Optional

from wistx_mcp.tools.lib.constants import (
    RATE_LIMITER_MAX_IDENTIFIERS,
    MAX_RATE_LIMIT_CALLS,
    RATE_LIMIT_WINDOW_SECONDS,
)

logger = logging.getLogger(__name__)


class RateLimitEntry:
    """Individual rate limit entry with TTL."""

    def __init__(self, max_calls: int, window_seconds: int):
        """Initialize rate limit entry.

        Args:
            max_calls: Maximum calls allowed
            window_seconds: Time window in seconds
        """
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.calls: list[float] = []
        self.last_access: float = time.time()

    def is_expired(self, now: float) -> bool:
        """Check if entry is expired.

        Args:
            now: Current timestamp

        Returns:
            True if expired
        """
        return (now - self.last_access) > (self.window_seconds * 2)

    def cleanup_old_calls(self, now: float) -> None:
        """Remove calls outside the time window.

        Args:
            now: Current timestamp
        """
        window_start = now - self.window_seconds
        self.calls = [call_time for call_time in self.calls if call_time > window_start]

    def check_and_record(self, now: float) -> bool:
        """Check rate limit and record call.

        Args:
            now: Current timestamp

        Returns:
            True if allowed, False if rate limited
        """
        self.last_access = now
        self.cleanup_old_calls(now)

        if len(self.calls) >= self.max_calls:
            return False

        self.calls.append(now)
        return True


class RateLimiter:
    """Rate limiter with TTL-based cleanup and proper isolation."""

    def __init__(
        self,
        max_calls: int = MAX_RATE_LIMIT_CALLS,
        window_seconds: int = RATE_LIMIT_WINDOW_SECONDS,
        max_identifiers: int = RATE_LIMITER_MAX_IDENTIFIERS,
        cleanup_interval: float = 60.0,
    ):
        """Initialize rate limiter.

        Args:
            max_calls: Maximum number of calls per window
            window_seconds: Time window in seconds
            max_identifiers: Maximum number of tracked identifiers
            cleanup_interval: Background cleanup interval in seconds
        """
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.max_identifiers = max_identifiers
        self.entries: dict[str, RateLimitEntry] = {}
        self.lock = asyncio.Lock()
        self._cleanup_task: Optional[asyncio.Task] = None
        self._cleanup_interval = cleanup_interval
        self._running = False

    async def start(self) -> None:
        """Start background cleanup task."""
        if not self._running:
            self._running = True
            self._cleanup_task = asyncio.create_task(self._background_cleanup())

    async def stop(self) -> None:
        """Stop background cleanup task."""
        self._running = False
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass

    async def _background_cleanup(self) -> None:
        """Background task to clean up expired entries."""
        while self._running:
            try:
                await asyncio.sleep(self._cleanup_interval)
                await self._cleanup_expired()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Error in rate limiter cleanup: %s", e, exc_info=True)

    async def check_rate_limit(self, identifier: str) -> bool:
        """Check if rate limit allows the call.

        Args:
            identifier: Unique identifier (user_id, api_key hash, etc.)

        Returns:
            True if allowed, False if rate limited
        """
        async with self.lock:
            now = time.time()

            await self._cleanup_expired(now)

            if len(self.entries) >= self.max_identifiers:
                await self._evict_oldest(now)
            
            memory_usage_mb = self._get_memory_usage_mb()
            if memory_usage_mb > 100:
                logger.warning("Rate limiter memory usage high: %.2f MB, evicting oldest entries", memory_usage_mb)
                await self._evict_oldest(now)

            if identifier not in self.entries:
                self.entries[identifier] = RateLimitEntry(
                    max_calls=self.max_calls,
                    window_seconds=self.window_seconds,
                )

            entry = self.entries[identifier]
            allowed = entry.check_and_record(now)

            if not allowed:
                logger.warning(
                    "Rate limit exceeded for %s: %d calls in %d seconds",
                    identifier[:8],
                    len(entry.calls),
                    self.window_seconds,
                )

            return allowed

    async def _cleanup_expired(self, now: Optional[float] = None) -> None:
        """Clean up expired entries.

        Args:
            now: Current timestamp (generated if not provided)
        """
        if now is None:
            now = time.time()

        expired_keys = [
            key for key, entry in self.entries.items()
            if entry.is_expired(now)
        ]

        for key in expired_keys:
            del self.entries[key]

        if expired_keys:
            logger.debug("Cleaned up %d expired rate limit entries", len(expired_keys))

    async def _evict_oldest(self, now: float) -> None:
        """Evict oldest entries when limit reached.

        Args:
            now: Current timestamp
        """
        if len(self.entries) < self.max_identifiers:
            return

        sorted_entries = sorted(
            self.entries.items(),
            key=lambda x: x[1].last_access,
        )

        evict_count = max(100, len(sorted_entries) // 10)
        for key, _ in sorted_entries[:evict_count]:
            del self.entries[key]

        logger.debug("Evicted %d rate limit entries (limit: %d)", evict_count, self.max_identifiers)
    
    def _get_memory_usage_mb(self) -> float:
        """Get approximate memory usage in MB.
        
        Returns:
            Memory usage in MB
        """
        import sys
        total_size = sys.getsizeof(self.entries)
        for key, entry in self.entries.items():
            total_size += sys.getsizeof(key)
            total_size += sys.getsizeof(entry)
            total_size += sys.getsizeof(entry.calls)
            for call_time in entry.calls:
                total_size += sys.getsizeof(call_time)
        return total_size / (1024 * 1024)

    async def reset(self, identifier: str) -> None:
        """Reset rate limit for an identifier.

        Args:
            identifier: Identifier to reset
        """
        async with self.lock:
            if identifier in self.entries:
                del self.entries[identifier]

    def get_remaining_calls(self, identifier: str) -> int:
        """Get remaining calls for an identifier.

        Args:
            identifier: Identifier to check

        Returns:
            Number of remaining calls
        """
        if identifier not in self.entries:
            return self.max_calls

        entry = self.entries[identifier]
        now = time.time()
        entry.cleanup_old_calls(now)

        return max(0, self.max_calls - len(entry.calls))


_global_rate_limiter: Optional[RateLimiter] = None


async def get_rate_limiter(
    max_calls: int = MAX_RATE_LIMIT_CALLS,
    window_seconds: int = RATE_LIMIT_WINDOW_SECONDS,
) -> RateLimiter:
    """Get global rate limiter instance.

    Automatically uses distributed Redis rate limiting if configured,
    otherwise falls back to in-memory rate limiting.

    Args:
        max_calls: Maximum calls per window
        window_seconds: Time window in seconds

    Returns:
        RateLimiter instance (in-memory) or HybridRateLimiter (with Redis fallback)
    """
    from wistx_mcp.config import settings
    from wistx_mcp.tools.lib.distributed_rate_limiter import (
        get_distributed_rate_limiter,
    )

    distributed_limiter = await get_distributed_rate_limiter(
        max_calls=max_calls,
        window_seconds=window_seconds,
    )

    if distributed_limiter:
        return HybridRateLimiter(
            distributed_limiter=distributed_limiter,
            in_memory_limiter=None,
            max_calls=max_calls,
            window_seconds=window_seconds,
        )

    global _global_rate_limiter

    if _global_rate_limiter is None:
        _global_rate_limiter = RateLimiter(
            max_calls=max_calls,
            window_seconds=window_seconds,
        )
        await _global_rate_limiter.start()

    return _global_rate_limiter


class HybridRateLimiter:
    """Hybrid rate limiter that uses Redis when available, falls back to in-memory.

    Provides same interface as RateLimiter but uses distributed Redis for Cloud Run scaling.
    """

    def __init__(
        self,
        distributed_limiter,
        in_memory_limiter: Optional[RateLimiter],
        max_calls: int,
        window_seconds: int,
    ):
        """Initialize hybrid rate limiter.

        Args:
            distributed_limiter: DistributedRateLimiter instance
            in_memory_limiter: In-memory RateLimiter instance (for fallback)
            max_calls: Maximum calls per window
            window_seconds: Time window in seconds
        """
        self.distributed_limiter = distributed_limiter
        self.in_memory_limiter = in_memory_limiter
        self.max_calls = max_calls
        self.window_seconds = window_seconds

    async def start(self) -> None:
        """Start rate limiter (no-op for hybrid, distributed doesn't need start)."""
        if self.in_memory_limiter:
            await self.in_memory_limiter.start()

    async def stop(self) -> None:
        """Stop rate limiter."""
        if self.in_memory_limiter:
            await self.in_memory_limiter.stop()
        if self.distributed_limiter:
            await self.distributed_limiter.close()

    async def check_rate_limit(self, identifier: str) -> bool:
        """Check if rate limit allows the call.

        Uses distributed Redis limiter, falls back to in-memory if Redis fails.

        Args:
            identifier: Unique identifier (user_id, api_key hash, etc.)

        Returns:
            True if allowed, False if rate limited
        """
        if self.distributed_limiter:
            try:
                return await self.distributed_limiter.check_rate_limit(identifier)
            except Exception as e:
                logger.warning(
                    "Distributed rate limit check failed, falling back to in-memory: %s",
                    e,
                )
                if self.in_memory_limiter:
                    return await self.in_memory_limiter.check_rate_limit(identifier)

        if self.in_memory_limiter:
            return await self.in_memory_limiter.check_rate_limit(identifier)

        return True

    async def reset(self, identifier: str) -> None:
        """Reset rate limit for an identifier.

        Args:
            identifier: Identifier to reset
        """
        if self.distributed_limiter:
            try:
                await self.distributed_limiter.reset(identifier)
            except Exception as e:
                logger.warning("Distributed rate limit reset failed: %s", e)

        if self.in_memory_limiter:
            await self.in_memory_limiter.reset(identifier)

    def get_remaining_calls(self, identifier: str) -> int:
        """Get remaining calls for an identifier.

        Args:
            identifier: Identifier to check

        Returns:
            Number of remaining calls
        """
        if self.in_memory_limiter:
            return self.in_memory_limiter.get_remaining_calls(identifier)
        return self.max_calls
