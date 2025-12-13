"""Distributed tool cache using Redis for horizontal scaling."""

import json
import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


class DistributedToolCache:
    """Distributed cache for tool definitions, recommendations, and analytics."""

    def __init__(self, redis_client=None, ttl: int = 3600):
        """Initialize distributed tool cache.
        
        Args:
            redis_client: Redis client instance
            ttl: Time-to-live for cache entries in seconds
        """
        self.redis_client = redis_client
        self.ttl = ttl
        self.local_cache = {}
        self.cache_prefix = "wistx:tool:"

    def set_tool_definitions(self, tools: list[dict[str, Any]]) -> bool:
        """Cache tool definitions.
        
        Args:
            tools: List of tool definitions
            
        Returns:
            True if successful
        """
        try:
            key = f"{self.cache_prefix}definitions"
            value = json.dumps(tools)
            
            if self.redis_client:
                self.redis_client.setex(key, self.ttl, value)
            
            self.local_cache[key] = (value, time.time() + self.ttl)
            logger.info(f"Cached {len(tools)} tool definitions")
            return True
        except Exception as e:
            logger.error(f"Error caching tool definitions: {e}", exc_info=True)
            return False

    def get_tool_definitions(self) -> list[dict[str, Any]] | None:
        """Get cached tool definitions.
        
        Returns:
            List of tool definitions or None if not cached
        """
        try:
            key = f"{self.cache_prefix}definitions"
            
            # Try Redis first
            if self.redis_client:
                value = self.redis_client.get(key)
                if value:
                    return json.loads(value)
            
            # Try local cache
            if key in self.local_cache:
                value, expiry = self.local_cache[key]
                if time.time() < expiry:
                    return json.loads(value)
                else:
                    del self.local_cache[key]
            
            return None
        except Exception as e:
            logger.error(f"Error retrieving tool definitions: {e}", exc_info=True)
            return None

    def set_recommendations(self, query: str, recommendations: list[dict[str, Any]]) -> bool:
        """Cache tool recommendations for a query.
        
        Args:
            query: Search query
            recommendations: List of recommendations
            
        Returns:
            True if successful
        """
        try:
            key = f"{self.cache_prefix}recommendations:{query.lower()}"
            value = json.dumps(recommendations)
            
            if self.redis_client:
                self.redis_client.setex(key, self.ttl, value)
            
            self.local_cache[key] = (value, time.time() + self.ttl)
            logger.info(f"Cached recommendations for query: {query}")
            return True
        except Exception as e:
            logger.error(f"Error caching recommendations: {e}", exc_info=True)
            return False

    def get_recommendations(self, query: str) -> list[dict[str, Any]] | None:
        """Get cached recommendations for a query.
        
        Args:
            query: Search query
            
        Returns:
            List of recommendations or None if not cached
        """
        try:
            key = f"{self.cache_prefix}recommendations:{query.lower()}"
            
            if self.redis_client:
                value = self.redis_client.get(key)
                if value:
                    return json.loads(value)
            
            if key in self.local_cache:
                value, expiry = self.local_cache[key]
                if time.time() < expiry:
                    return json.loads(value)
                else:
                    del self.local_cache[key]
            
            return None
        except Exception as e:
            logger.error(f"Error retrieving recommendations: {e}", exc_info=True)
            return None

    def set_analytics(self, analytics_data: dict[str, Any]) -> bool:
        """Cache analytics data.
        
        Args:
            analytics_data: Analytics data to cache
            
        Returns:
            True if successful
        """
        try:
            key = f"{self.cache_prefix}analytics"
            value = json.dumps(analytics_data)
            
            if self.redis_client:
                self.redis_client.setex(key, self.ttl, value)
            
            self.local_cache[key] = (value, time.time() + self.ttl)
            logger.info("Cached analytics data")
            return True
        except Exception as e:
            logger.error(f"Error caching analytics: {e}", exc_info=True)
            return False

    def get_analytics(self) -> dict[str, Any] | None:
        """Get cached analytics data.
        
        Returns:
            Analytics data or None if not cached
        """
        try:
            key = f"{self.cache_prefix}analytics"
            
            if self.redis_client:
                value = self.redis_client.get(key)
                if value:
                    return json.loads(value)
            
            if key in self.local_cache:
                value, expiry = self.local_cache[key]
                if time.time() < expiry:
                    return json.loads(value)
                else:
                    del self.local_cache[key]
            
            return None
        except Exception as e:
            logger.error(f"Error retrieving analytics: {e}", exc_info=True)
            return None

    def invalidate_all(self) -> bool:
        """Invalidate all cache entries.
        
        Returns:
            True if successful
        """
        try:
            if self.redis_client:
                pattern = f"{self.cache_prefix}*"
                keys = self.redis_client.keys(pattern)
                if keys:
                    self.redis_client.delete(*keys)
            
            self.local_cache.clear()
            logger.info("Invalidated all cache entries")
            return True
        except Exception as e:
            logger.error(f"Error invalidating cache: {e}", exc_info=True)
            return False

    def get_cache_stats(self) -> dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        try:
            redis_size = 0
            if self.redis_client:
                pattern = f"{self.cache_prefix}*"
                keys = self.redis_client.keys(pattern)
                redis_size = len(keys) if keys else 0
            
            return {
                "local_cache_size": len(self.local_cache),
                "redis_cache_size": redis_size,
                "ttl": self.ttl,
                "redis_enabled": self.redis_client is not None,
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}", exc_info=True)
            return {"error": str(e)}

    def cleanup_expired(self) -> int:
        """Clean up expired local cache entries.
        
        Returns:
            Number of entries cleaned up
        """
        current_time = time.time()
        expired_keys = [
            key for key, (_, expiry) in self.local_cache.items()
            if current_time >= expiry
        ]
        
        for key in expired_keys:
            del self.local_cache[key]
        
        if expired_keys:
            logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
        
        return len(expired_keys)

