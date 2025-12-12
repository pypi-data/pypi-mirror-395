"""URL discovery caching for reducing redundant work."""

import hashlib
import time
from typing import Any

from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class URLCache:
    """Simple in-memory cache for URL discovery results.
    
    Caches discovered URLs to avoid redundant discovery work.
    Uses TTL-based expiration for cache entries.
    """

    def __init__(self, default_ttl_seconds: int = 86400):
        """Initialize URL cache.
        
        Args:
            default_ttl_seconds: Default TTL for cache entries in seconds (default: 24 hours)
        """
        self._cache: dict[str, tuple[dict[str, list[str]], float]] = {}
        self.default_ttl = default_ttl_seconds

    def _generate_key(self, domain: str, subdomain: str | None = None, **kwargs: Any) -> str:
        """Generate cache key from parameters.
        
        Args:
            domain: Domain name
            subdomain: Optional subdomain
            **kwargs: Additional parameters for cache key
            
        Returns:
            Cache key string
        """
        key_parts = [domain]
        if subdomain:
            key_parts.append(subdomain)
        
        if kwargs:
            sorted_kwargs = sorted(kwargs.items())
            kwargs_str = "_".join(f"{k}:{v}" for k, v in sorted_kwargs)
            key_parts.append(kwargs_str)
        
        key_string = "_".join(key_parts)
        return hashlib.sha256(key_string.encode()).hexdigest()

    def get(
        self,
        domain: str,
        subdomain: str | None = None,
        **kwargs: Any,
    ) -> dict[str, list[str]] | None:
        """Get cached URLs for domain/subdomain.
        
        Args:
            domain: Domain name
            subdomain: Optional subdomain
            **kwargs: Additional parameters for cache key
            
        Returns:
            Cached URLs dictionary or None if not found/expired
        """
        cache_key = self._generate_key(domain, subdomain, **kwargs)
        
        if cache_key not in self._cache:
            return None
        
        cached_data, expiry_time = self._cache[cache_key]
        
        if time.time() > expiry_time:
            del self._cache[cache_key]
            logger.debug("Cache expired for key: %s", cache_key[:16])
            return None
        
        logger.debug("Cache hit for key: %s", cache_key[:16])
        return cached_data

    def set(
        self,
        domain: str,
        urls: dict[str, list[str]],
        subdomain: str | None = None,
        ttl_seconds: int | None = None,
        **kwargs: Any,
    ) -> None:
        """Cache URLs for domain/subdomain.
        
        Args:
            domain: Domain name
            urls: URLs dictionary to cache
            subdomain: Optional subdomain
            ttl_seconds: TTL in seconds (default: self.default_ttl)
            **kwargs: Additional parameters for cache key
        """
        cache_key = self._generate_key(domain, subdomain, **kwargs)
        ttl = ttl_seconds or self.default_ttl
        expiry_time = time.time() + ttl
        
        self._cache[cache_key] = (urls, expiry_time)
        logger.debug("Cached URLs for key: %s (TTL: %d seconds)", cache_key[:16], ttl)

    def clear(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()
        logger.info("URL cache cleared")

    def cleanup_expired(self) -> int:
        """Remove expired cache entries.
        
        Returns:
            Number of entries removed
        """
        current_time = time.time()
        expired_keys = [
            key for key, (_, expiry_time) in self._cache.items()
            if current_time > expiry_time
        ]
        
        for key in expired_keys:
            del self._cache[key]
        
        if expired_keys:
            logger.debug("Cleaned up %d expired cache entries", len(expired_keys))
        
        return len(expired_keys)

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        current_time = time.time()
        expired_count = sum(
            1 for _, expiry_time in self._cache.values()
            if current_time > expiry_time
        )
        
        return {
            "total_entries": len(self._cache),
            "active_entries": len(self._cache) - expired_count,
            "expired_entries": expired_count,
        }


url_cache = URLCache()

