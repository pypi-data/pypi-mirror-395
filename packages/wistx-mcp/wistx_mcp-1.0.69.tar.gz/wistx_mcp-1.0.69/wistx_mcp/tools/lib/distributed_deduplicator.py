"""Distributed request deduplication using Redis for Cloud Run horizontal scaling."""

import hashlib
import json
import logging
import time
from typing import Any, Optional

from wistx_mcp.tools.lib.constants import REQUEST_DEDUPLICATION_TTL_SECONDS

logger = logging.getLogger(__name__)


async def get_redis_client():
    """Get Redis client for distributed deduplication.

    Reuses the same Redis client from distributed_rate_limiter.

    Returns:
        Redis client instance or None if Redis not configured
    """
    from wistx_mcp.tools.lib.distributed_rate_limiter import get_redis_client as get_rate_limiter_redis

    return await get_rate_limiter_redis()


class DistributedRequestDeduplicator:
    """Distributed request deduplicator using Redis for Cloud Run scaling.

    Stores request results in Redis with TTL-based expiration.
    All instances share the same cache.
    """

    def __init__(self, ttl_seconds: int = REQUEST_DEDUPLICATION_TTL_SECONDS):
        """Initialize distributed request deduplicator.

        Args:
            ttl_seconds: Time-to-live for cached results in seconds
        """
        self.ttl_seconds = ttl_seconds
        self._redis_client: Optional[Any] = None

    async def _ensure_redis_client(self) -> Optional[Any]:
        """Ensure Redis client is initialized.

        Returns:
            Redis client or None if not available
        """
        if self._redis_client is None:
            self._redis_client = await get_redis_client()
        return self._redis_client

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

    def _serialize_result(self, result: Any) -> str:
        """Serialize result for Redis storage.

        Args:
            result: Result to serialize (list[TextContent])

        Returns:
            JSON string representation
        """
        try:
            if isinstance(result, list):
                serialized = []
                for item in result:
                    if hasattr(item, "model_dump"):
                        serialized.append(item.model_dump())
                    elif hasattr(item, "dict"):
                        serialized.append(item.dict())
                    elif isinstance(item, dict):
                        serialized.append(item)
                    else:
                        serialized.append({"type": "text", "text": str(item)})
                return json.dumps(serialized)
            elif hasattr(result, "model_dump"):
                return json.dumps(result.model_dump())
            elif hasattr(result, "dict"):
                return json.dumps(result.dict())
            else:
                return json.dumps(result, default=str)
        except Exception as e:
            logger.warning("Failed to serialize result: %s", e)
            return json.dumps({"error": "serialization_failed"})

    def _deserialize_result(self, data: str) -> Any:
        """Deserialize result from Redis storage.

        Args:
            data: JSON string representation

        Returns:
            Deserialized result
        """
        try:
            from mcp.types import TextContent

            parsed = json.loads(data)
            if isinstance(parsed, list):
                result = []
                for item in parsed:
                    if isinstance(item, dict) and "type" in item:
                        result.append(TextContent(**item))
                    else:
                        result.append(item)
                return result
            return parsed
        except Exception as e:
            logger.warning("Failed to deserialize result: %s", e)
            return None

    async def check_duplicate(
        self,
        request_id: str,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> Optional[Any]:
        """Check if request is duplicate and return cached result if available.

        Args:
            request_id: Request ID
            tool_name: Tool name
            arguments: Tool arguments

        Returns:
            Cached result if duplicate, None otherwise
        """
        redis_client = await self._ensure_redis_client()
        if not redis_client:
            return None

        request_hash = self._generate_hash(request_id, tool_name, arguments)
        key = f"dedup:{request_hash}"

        try:
            cached_data = await redis_client.get(key)
            if cached_data:
                logger.debug(
                    "Duplicate request detected (distributed): %s",
                    request_hash[:16],
                )
                return self._deserialize_result(cached_data)
            return None
        except Exception as e:
            logger.debug("Redis deduplication check failed: %s", e)
            return None

    async def store_result(
        self,
        request_id: str,
        tool_name: str,
        arguments: dict[str, Any],
        result: Any,
    ) -> None:
        """Store request result for deduplication.

        Args:
            request_id: Request ID
            tool_name: Tool name
            arguments: Tool arguments
            result: Tool execution result
        """
        redis_client = await self._ensure_redis_client()
        if not redis_client:
            return

        request_hash = self._generate_hash(request_id, tool_name, arguments)
        key = f"dedup:{request_hash}"

        try:
            serialized_result = self._serialize_result(result)
            await redis_client.setex(key, self.ttl_seconds, serialized_result)
        except Exception as e:
            logger.debug("Redis deduplication store failed: %s", e)

    async def clear_cache(self) -> None:
        """Clear all cached results (for testing/debugging).

        Note: This clears ALL deduplication cache entries.
        """
        redis_client = await self._ensure_redis_client()
        if not redis_client:
            return

        try:
            keys = await redis_client.keys("dedup:*")
            if keys:
                await redis_client.delete(*keys)
                logger.info("Cleared %d deduplication cache entries", len(keys))
        except Exception as e:
            logger.warning("Failed to clear deduplication cache: %s", e)


_global_distributed_deduplicator: Optional[DistributedRequestDeduplicator] = None


async def get_distributed_deduplicator(
    ttl_seconds: int = REQUEST_DEDUPLICATION_TTL_SECONDS,
) -> Optional[DistributedRequestDeduplicator]:
    """Get global distributed deduplicator instance.

    Args:
        ttl_seconds: Time-to-live for cached results

    Returns:
        DistributedRequestDeduplicator instance or None if Redis not configured
    """
    global _global_distributed_deduplicator

    if _global_distributed_deduplicator is None:
        _global_distributed_deduplicator = DistributedRequestDeduplicator(
            ttl_seconds=ttl_seconds,
        )

    return _global_distributed_deduplicator




