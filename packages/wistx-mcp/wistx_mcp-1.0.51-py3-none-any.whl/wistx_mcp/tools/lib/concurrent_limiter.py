"""Concurrent request limiting for MCP tool calls with TTL-based cleanup.

Supports both Redis-based distributed concurrent limiting and in-memory semaphores.
Uses Redis for global limits across instances, local semaphores for per-instance throttling.
"""

import asyncio
import logging
import time
from typing import Any, Optional

from wistx_mcp.tools.lib.constants import (
    MAX_CONCURRENT_TOOLS,
    CONCURRENT_LIMITER_TIMEOUT_SECONDS,
)

logger = logging.getLogger(__name__)

SEMAPHORE_TTL_SECONDS = 300


class SemaphoreEntry:
    """Semaphore entry with TTL tracking."""

    def __init__(self, semaphore: asyncio.Semaphore):
        """Initialize semaphore entry.

        Args:
            semaphore: Semaphore instance
        """
        self.semaphore = semaphore
        self.last_access: float = time.time()
        self.acquired_count: int = 0

    def is_expired(self, now: float) -> bool:
        """Check if entry is expired.

        Args:
            now: Current timestamp

        Returns:
            True if expired and not in use
        """
        if self.acquired_count > 0:
            return False
        return (now - self.last_access) > SEMAPHORE_TTL_SECONDS

    def update_access(self) -> None:
        """Update last access time."""
        self.last_access = time.time()


class ConcurrentLimiter:
    """Limits concurrent tool executions per user with TTL-based cleanup.

    Supports both Redis-based distributed limiting and in-memory semaphores.
    Uses Redis for global limits, local semaphores for per-instance throttling.
    """

    def __init__(
        self,
        max_concurrent: int = MAX_CONCURRENT_TOOLS,
        cleanup_interval: float = 60.0,
    ):
        """Initialize concurrent limiter.

        Args:
            max_concurrent: Maximum concurrent executions per user
            cleanup_interval: Background cleanup interval in seconds
        """
        self.max_concurrent = max_concurrent
        self.semaphores: dict[str, SemaphoreEntry] = {}
        self.lock = asyncio.Lock()
        self._cleanup_task: Optional[asyncio.Task] = None
        self._running = False
        self._cleanup_interval = cleanup_interval
        self._distributed_limiter: Optional[Any] = None

    async def start(self) -> None:
        """Start background cleanup task."""
        from wistx_mcp.tools.lib.distributed_concurrent_limiter import (
            get_distributed_concurrent_limiter,
        )

        self._distributed_limiter = await get_distributed_concurrent_limiter(
            max_concurrent=self.max_concurrent,
        )

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
        """Background task to clean up expired semaphores."""
        while self._running:
            try:
                await asyncio.sleep(self._cleanup_interval)
                await self._cleanup_expired()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Error in concurrent limiter cleanup: %s", e, exc_info=True)

    async def _cleanup_expired(self) -> None:
        """Clean up expired semaphore entries."""
        now = time.time()
        expired_keys = [
            key
            for key, entry in self.semaphores.items()
            if entry.is_expired(now)
        ]

        async with self.lock:
            for key in expired_keys:
                del self.semaphores[key]

        if expired_keys:
            logger.debug(
                "Cleaned up %d expired semaphore entries",
                len(expired_keys),
            )

    async def acquire(self, user_id: str) -> None:
        """Acquire a slot for concurrent execution.

        Checks Redis global limit first, then uses local semaphore for per-instance throttling.

        Args:
            user_id: User identifier

        Raises:
            ValueError: If maximum concurrent executions exceeded
        """
        if self._distributed_limiter:
            try:
                acquired = await self._distributed_limiter.acquire(user_id)
                if not acquired:
                    raise ValueError(
                        f"Maximum concurrent executions ({self.max_concurrent}) exceeded globally. "
                        "Please wait for current operations to complete."
                    )
            except ValueError:
                raise
            except Exception as e:
                logger.warning(
                    "Distributed concurrent limit check failed, using local only: %s",
                    e,
                )

        async with self.lock:
            if user_id not in self.semaphores:
                self.semaphores[user_id] = SemaphoreEntry(
                    asyncio.Semaphore(self.max_concurrent)
                )

            entry = self.semaphores[user_id]
            entry.update_access()
            entry.acquired_count += 1

        try:
            await asyncio.wait_for(
                entry.semaphore.acquire(),
                timeout=CONCURRENT_LIMITER_TIMEOUT_SECONDS,
            )
        except asyncio.TimeoutError:
            async with self.lock:
                if user_id in self.semaphores:
                    self.semaphores[user_id].acquired_count -= 1
            if self._distributed_limiter:
                try:
                    await self._distributed_limiter.release(user_id)
                except Exception:
                    pass
            raise ValueError(
                f"Maximum concurrent executions ({self.max_concurrent}) exceeded for user. "
                "Please wait for current operations to complete."
            )

    async def release(self, user_id: str) -> None:
        """Release a slot after execution completes.

        Releases both Redis global counter and local semaphore.

        Args:
            user_id: User identifier
        """
        if self._distributed_limiter:
            try:
                await self._distributed_limiter.release(user_id)
            except Exception as e:
                logger.warning("Distributed concurrent limit release failed: %s", e)

        async with self.lock:
            if user_id in self.semaphores:
                entry = self.semaphores[user_id]
                entry.semaphore.release()
                entry.acquired_count -= 1
                entry.update_access()

                if entry.acquired_count == 0 and entry.is_expired(time.time()):
                    del self.semaphores[user_id]


_global_concurrent_limiter: Optional[ConcurrentLimiter] = None


async def get_concurrent_limiter(
    max_concurrent: int = MAX_CONCURRENT_TOOLS,
) -> ConcurrentLimiter:
    """Get global concurrent limiter instance.

    Args:
        max_concurrent: Maximum concurrent executions per user

    Returns:
        ConcurrentLimiter instance
    """
    global _global_concurrent_limiter

    if _global_concurrent_limiter is None:
        _global_concurrent_limiter = ConcurrentLimiter(max_concurrent=max_concurrent)
        await _global_concurrent_limiter.start()

    return _global_concurrent_limiter
