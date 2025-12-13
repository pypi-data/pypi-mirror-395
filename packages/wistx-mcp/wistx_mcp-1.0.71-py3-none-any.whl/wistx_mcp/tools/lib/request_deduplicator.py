"""Request deduplication for idempotent operations with TTL-based cache and background cleanup.

Supports both Redis-based distributed deduplication and in-memory fallback.
"""

import asyncio
import hashlib
import json
import logging
import time
from collections import OrderedDict
from typing import Any, Optional

from wistx_mcp.tools.lib.constants import (
    REQUEST_DEDUPLICATION_TTL_SECONDS,
    MAX_CACHE_SIZE,
)

logger = logging.getLogger(__name__)


class RequestDeduplicator:
    """Deduplicates requests with TTL-based cache and background cleanup.

    Supports both Redis-based distributed deduplication and in-memory fallback.
    Automatically uses Redis if configured, otherwise uses in-memory cache.
    """

    def __init__(
        self,
        ttl_seconds: int = REQUEST_DEDUPLICATION_TTL_SECONDS,
        max_cache_size: int = MAX_CACHE_SIZE,
        cleanup_interval: float = 30.0,
    ):
        """Initialize request deduplicator.

        Args:
            ttl_seconds: Time-to-live for request hashes (default: 5 minutes)
            max_cache_size: Maximum number of cached requests (default: 10000)
            cleanup_interval: Background cleanup interval in seconds
        """
        self.ttl_seconds = ttl_seconds
        self.max_cache_size = max_cache_size
        self.cleanup_interval = cleanup_interval
        self.request_cache: OrderedDict[str, tuple[Any, float]] = OrderedDict()
        self.lock = asyncio.Lock()
        self._cleanup_task: Optional[asyncio.Task] = None
        self._running = False
        self._distributed_deduplicator: Optional[Any] = None

    async def start(self) -> None:
        """Start background cleanup task."""
        from wistx_mcp.tools.lib.distributed_deduplicator import (
            get_distributed_deduplicator,
        )

        self._distributed_deduplicator = await get_distributed_deduplicator(
            ttl_seconds=self.ttl_seconds,
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
        """Background task to clean up expired entries."""
        while self._running:
            try:
                await asyncio.sleep(self.cleanup_interval)
                await self._cleanup_expired()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Error in deduplicator cleanup: %s", e, exc_info=True)

    def _generate_hash(
        self,
        request_id: str,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> str:
        """Generate hash for request deduplication.

        Args:
            request_id: Request ID
            tool_name: Tool name
            arguments: Tool arguments

        Returns:
            SHA256 hash of request
        """
        normalized_args = json.dumps(arguments, sort_keys=True)
        hash_input = f"{request_id}:{tool_name}:{normalized_args}"
        return hashlib.sha256(hash_input.encode()).hexdigest()

    async def check_duplicate(
        self,
        request_id: str,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> Optional[Any]:
        """Check if request is duplicate and return cached result if available.

        Uses Redis-based distributed deduplication if available, otherwise falls back to in-memory.

        Args:
            request_id: Request ID
            tool_name: Tool name
            arguments: Tool arguments

        Returns:
            Cached result if duplicate, None otherwise
        """
        if self._distributed_deduplicator:
            try:
                cached_result = await self._distributed_deduplicator.check_duplicate(
                    request_id, tool_name, arguments
                )
                if cached_result is not None:
                    return cached_result
            except Exception as e:
                logger.warning(
                    "Distributed deduplication check failed, falling back to in-memory: %s",
                    e,
                )

        request_hash = self._generate_hash(request_id, tool_name, arguments)

        async with self.lock:
            await self._cleanup_expired()
            await self._enforce_cache_limit()

            if request_hash in self.request_cache:
                cached_result, timestamp = self.request_cache[request_hash]
                age = time.time() - timestamp

                if age < self.ttl_seconds:
                    self.request_cache.move_to_end(request_hash)
                    logger.debug(
                        "Duplicate request detected (in-memory): %s (age: %.1fs)",
                        request_hash[:16],
                        age,
                    )
                    return cached_result
                else:
                    del self.request_cache[request_hash]

            return None

    async def store_result(
        self,
        request_id: str,
        tool_name: str,
        arguments: dict[str, Any],
        result: Any,
    ) -> None:
        """Store request result for deduplication.

        Uses Redis-based distributed deduplication if available, also stores in-memory for fallback.

        Args:
            request_id: Request ID
            tool_name: Tool name
            arguments: Tool arguments
            result: Tool execution result
        """
        if self._distributed_deduplicator:
            try:
                await self._distributed_deduplicator.store_result(
                    request_id, tool_name, arguments, result
                )
            except Exception as e:
                logger.warning(
                    "Distributed deduplication store failed, using in-memory only: %s",
                    e,
                )

        request_hash = self._generate_hash(request_id, tool_name, arguments)

        async with self.lock:
            await self._cleanup_expired()
            await self._enforce_cache_limit()

            self.request_cache[request_hash] = (result, time.time())
            self.request_cache.move_to_end(request_hash)

    async def _cleanup_expired(self) -> None:
        """Remove expired entries from cache."""
        now = time.time()
        expired_keys = [
            key
            for key, (_, timestamp) in self.request_cache.items()
            if now - timestamp >= self.ttl_seconds
        ]

        for key in expired_keys:
            del self.request_cache[key]

        if expired_keys:
            logger.debug(
                "Cleaned up %d expired request cache entries",
                len(expired_keys),
            )

    async def _enforce_cache_limit(self) -> None:
        """Enforce maximum cache size using LRU eviction."""
        while len(self.request_cache) > self.max_cache_size:
            self.request_cache.popitem(last=False)
            logger.debug(
                "Evicted entry from request cache (limit: %d)",
                self.max_cache_size,
            )


_global_deduplicator: Optional[RequestDeduplicator] = None


async def get_request_deduplicator(
    ttl_seconds: int = REQUEST_DEDUPLICATION_TTL_SECONDS,
) -> RequestDeduplicator:
    """Get global request deduplicator instance.

    Args:
        ttl_seconds: Time-to-live for request hashes

    Returns:
        RequestDeduplicator instance
    """
    global _global_deduplicator

    if _global_deduplicator is None:
        _global_deduplicator = RequestDeduplicator(ttl_seconds=ttl_seconds)
        await _global_deduplicator.start()

    return _global_deduplicator
