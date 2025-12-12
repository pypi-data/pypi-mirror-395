"""Package metadata cache - cache package metadata to reduce API calls."""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any

logger = logging.getLogger(__name__)


class PackageMetadataCache:
    """In-memory cache for package metadata."""

    def __init__(self, ttl_hours: int = 24):
        """Initialize package metadata cache.

        Args:
            ttl_hours: Time-to-live in hours (default: 24)
        """
        self.cache: dict[str, dict[str, Any]] = {}
        self.ttl = timedelta(hours=ttl_hours)
        self.lock = asyncio.Lock()

    async def get(self, registry: str, package_name: str) -> dict[str, Any] | None:
        """Get cached package metadata.

        Args:
            registry: Registry name
            package_name: Package name

        Returns:
            Cached metadata or None if not found or expired
        """
        cache_key = f"{registry}:{package_name}"

        async with self.lock:
            if cache_key not in self.cache:
                return None

            cached_data = self.cache[cache_key]
            cached_at = cached_data.get("cached_at")

            if cached_at:
                age = datetime.utcnow() - cached_at
                if age > self.ttl:
                    del self.cache[cache_key]
                    return None

            return cached_data.get("metadata")

    async def set(self, registry: str, package_name: str, metadata: dict[str, Any]) -> None:
        """Cache package metadata.

        Args:
            registry: Registry name
            package_name: Package name
            metadata: Package metadata dictionary
        """
        cache_key = f"{registry}:{package_name}"

        async with self.lock:
            self.cache[cache_key] = {
                "metadata": metadata,
                "cached_at": datetime.utcnow(),
            }

    async def clear(self) -> None:
        """Clear all cached data."""
        async with self.lock:
            self.cache.clear()

    async def clear_expired(self) -> None:
        """Clear expired cache entries."""
        async with self.lock:
            now = datetime.utcnow()
            expired_keys = [
                key
                for key, data in self.cache.items()
                if data.get("cached_at") and (now - data["cached_at"]) > self.ttl
            ]
            for key in expired_keys:
                del self.cache[key]

    async def size(self) -> int:
        """Get cache size.

        Returns:
            Number of cached entries
        """
        async with self.lock:
            return len(self.cache)


_global_cache: PackageMetadataCache | None = None


def get_cache() -> PackageMetadataCache:
    """Get global package metadata cache instance.

    Returns:
        Global cache instance
    """
    global _global_cache
    if _global_cache is None:
        _global_cache = PackageMetadataCache()
    return _global_cache

