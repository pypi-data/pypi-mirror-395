"""Performance caching for tool discovery and recommendations."""

import logging
import time
from collections import OrderedDict
from typing import Any

logger = logging.getLogger(__name__)


class LRUCache:
    """LRU cache implementation for tool data caching."""

    def __init__(self, max_size: int = 100, ttl_seconds: int = 300):
        """Initialize LRU cache.

        Args:
            max_size: Maximum number of items in cache
            ttl_seconds: Time-to-live in seconds for cache entries
        """
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache: OrderedDict[str, tuple[Any, float]] = OrderedDict()

    def get(self, key: str) -> Any | None:
        """Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found or expired
        """
        if key not in self.cache:
            return None

        value, timestamp = self.cache[key]
        if time.time() - timestamp > self.ttl_seconds:
            del self.cache[key]
            return None

        self.cache.move_to_end(key)
        return value

    def set(self, key: str, value: Any) -> None:
        """Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)

        self.cache[key] = (value, time.time())

    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()

    def size(self) -> int:
        """Get current cache size.

        Returns:
            Number of items in cache
        """
        return len(self.cache)


class ToolDiscoveryCache:
    """Cache for tool discovery operations."""

    def __init__(self):
        """Initialize tool discovery cache."""
        self.tools_cache = LRUCache(max_size=10, ttl_seconds=60)
        self.categories_cache = LRUCache(max_size=20, ttl_seconds=300)
        self.recommendations_cache = LRUCache(max_size=100, ttl_seconds=60)

    def get_tools(self, category: str | None = None) -> list[dict[str, Any]] | None:
        """Get cached tools.

        Args:
            category: Optional category filter

        Returns:
            Cached tools or None
        """
        cache_key = f"tools:{category or 'all'}"
        return self.tools_cache.get(cache_key)

    def set_tools(self, tools: list[dict[str, Any]], category: str | None = None) -> None:
        """Cache tools.

        Args:
            tools: Tools to cache
            category: Optional category filter
        """
        cache_key = f"tools:{category or 'all'}"
        self.tools_cache.set(cache_key, tools)

    def get_categories(self) -> dict[str, Any] | None:
        """Get cached categories.

        Returns:
            Cached categories or None
        """
        return self.categories_cache.get("categories")

    def set_categories(self, categories: dict[str, Any]) -> None:
        """Cache categories.

        Args:
            categories: Categories to cache
        """
        self.categories_cache.set("categories", categories)

    def get_recommendations(
        self,
        query: str | None = None,
        current_tool: str | None = None,
        category: str | None = None,
    ) -> list[dict[str, Any]] | None:
        """Get cached recommendations.

        Args:
            query: Search query
            current_tool: Current tool name
            category: Category filter

        Returns:
            Cached recommendations or None
        """
        cache_key = f"recommendations:{query or ''}:{current_tool or ''}:{category or ''}"
        return self.recommendations_cache.get(cache_key)

    def set_recommendations(
        self,
        recommendations: list[dict[str, Any]],
        query: str | None = None,
        current_tool: str | None = None,
        category: str | None = None,
    ) -> None:
        """Cache recommendations.

        Args:
            recommendations: Recommendations to cache
            query: Search query
            current_tool: Current tool name
            category: Category filter
        """
        cache_key = f"recommendations:{query or ''}:{current_tool or ''}:{category or ''}"
        self.recommendations_cache.set(cache_key, recommendations)


_tool_discovery_cache: ToolDiscoveryCache | None = None


def get_tool_discovery_cache() -> ToolDiscoveryCache:
    """Get global tool discovery cache instance.

    Returns:
        ToolDiscoveryCache instance
    """
    global _tool_discovery_cache
    if _tool_discovery_cache is None:
        _tool_discovery_cache = ToolDiscoveryCache()
    return _tool_discovery_cache

