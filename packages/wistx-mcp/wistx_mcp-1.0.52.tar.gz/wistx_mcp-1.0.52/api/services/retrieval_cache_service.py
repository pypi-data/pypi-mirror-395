"""Retrieval Cache Service.

Implements caching for the retrieval pipeline:
1. Query embedding cache - avoid regenerating embeddings for repeated queries
2. Search result cache - cache hot query results
3. BM25 corpus stats cache - avoid recalculating corpus statistics

Uses Redis for distributed caching with TTL-based expiration.
Falls back to in-memory LRU cache if Redis is unavailable.
"""

import hashlib
import json
import logging
import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class CacheStats:
    """Cache statistics."""
    hits: int = 0
    misses: int = 0
    size: int = 0
    
    @property
    def hit_rate(self) -> float:
        """Calculate hit rate."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


class LRUCache:
    """Simple LRU cache implementation for fallback."""
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        """Initialize LRU cache.
        
        Args:
            max_size: Maximum number of items
            default_ttl: Default TTL in seconds
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: OrderedDict[str, tuple[Any, float]] = OrderedDict()
        self._stats = CacheStats()
    
    def get(self, key: str) -> Any | None:
        """Get item from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        if key not in self._cache:
            self._stats.misses += 1
            return None
        
        value, expiry = self._cache[key]
        
        # Check expiry
        if time.time() > expiry:
            del self._cache[key]
            self._stats.misses += 1
            return None
        
        # Move to end (most recently used)
        self._cache.move_to_end(key)
        self._stats.hits += 1
        return value
    
    def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Set item in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: TTL in seconds (default: default_ttl)
        """
        ttl = ttl or self.default_ttl
        expiry = time.time() + ttl
        
        # Remove oldest if at capacity
        while len(self._cache) >= self.max_size:
            self._cache.popitem(last=False)
        
        self._cache[key] = (value, expiry)
        self._stats.size = len(self._cache)
    
    def delete(self, key: str) -> bool:
        """Delete item from cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if deleted, False if not found
        """
        if key in self._cache:
            del self._cache[key]
            self._stats.size = len(self._cache)
            return True
        return False
    
    def clear(self) -> None:
        """Clear all items from cache."""
        self._cache.clear()
        self._stats.size = 0
    
    @property
    def stats(self) -> CacheStats:
        """Get cache statistics."""
        return self._stats


class RetrievalCacheService:
    """Caching service for retrieval pipeline.
    
    Provides caching for:
    - Query embeddings
    - Search results
    - BM25 corpus statistics
    """
    
    # Cache key prefixes
    EMBEDDING_PREFIX = "emb:"
    SEARCH_PREFIX = "search:"
    CORPUS_PREFIX = "corpus:"
    
    # Default TTLs (in seconds)
    EMBEDDING_TTL = 86400      # 24 hours
    SEARCH_TTL = 300           # 5 minutes
    CORPUS_TTL = 3600          # 1 hour
    
    def __init__(
        self,
        redis_client: Any | None = None,
        max_memory_cache_size: int = 1000,
    ):
        """Initialize cache service.
        
        Args:
            redis_client: Optional Redis client
            max_memory_cache_size: Max size for in-memory fallback cache
        """
        self.redis = redis_client
        self._memory_cache = LRUCache(max_size=max_memory_cache_size)
        self._use_redis = redis_client is not None
    
    def _get_cache(self) -> LRUCache | Any:
        """Get the active cache backend."""
        return self.redis if self._use_redis else self._memory_cache
    
    def _make_key(self, prefix: str, *parts: str) -> str:
        """Create a cache key from parts.

        Args:
            prefix: Key prefix
            *parts: Key parts to hash

        Returns:
            Cache key string
        """
        content = ":".join(str(p) for p in parts)
        hash_val = hashlib.sha256(content.encode()).hexdigest()[:16]
        return f"{prefix}{hash_val}"

    # Embedding cache methods

    def get_embedding(self, query: str) -> list[float] | None:
        """Get cached query embedding.

        Args:
            query: Query string

        Returns:
            Cached embedding or None
        """
        key = self._make_key(self.EMBEDDING_PREFIX, query)

        if self._use_redis:
            try:
                data = self.redis.get(key)
                if data:
                    return json.loads(data)
            except Exception as e:
                logger.warning("Redis get failed: %s", e)

        return self._memory_cache.get(key)

    def set_embedding(self, query: str, embedding: list[float]) -> None:
        """Cache query embedding.

        Args:
            query: Query string
            embedding: Embedding vector
        """
        key = self._make_key(self.EMBEDDING_PREFIX, query)

        if self._use_redis:
            try:
                self.redis.setex(key, self.EMBEDDING_TTL, json.dumps(embedding))
                return
            except Exception as e:
                logger.warning("Redis set failed: %s", e)

        self._memory_cache.set(key, embedding, self.EMBEDDING_TTL)

    # Search result cache methods

    def get_search_results(
        self,
        query: str,
        user_id: str,
        search_type: str = "hybrid",
    ) -> list[dict[str, Any]] | None:
        """Get cached search results.

        Args:
            query: Search query
            user_id: User ID
            search_type: Type of search (hybrid, semantic, bm25)

        Returns:
            Cached results or None
        """
        key = self._make_key(self.SEARCH_PREFIX, query, user_id, search_type)

        if self._use_redis:
            try:
                data = self.redis.get(key)
                if data:
                    return json.loads(data)
            except Exception as e:
                logger.warning("Redis get failed: %s", e)

        return self._memory_cache.get(key)

    def set_search_results(
        self,
        query: str,
        user_id: str,
        results: list[dict[str, Any]],
        search_type: str = "hybrid",
        ttl: int | None = None,
    ) -> None:
        """Cache search results.

        Args:
            query: Search query
            user_id: User ID
            results: Search results to cache
            search_type: Type of search
            ttl: Optional custom TTL
        """
        key = self._make_key(self.SEARCH_PREFIX, query, user_id, search_type)
        ttl = ttl or self.SEARCH_TTL

        if self._use_redis:
            try:
                self.redis.setex(key, ttl, json.dumps(results))
                return
            except Exception as e:
                logger.warning("Redis set failed: %s", e)

        self._memory_cache.set(key, results, ttl)

    # Corpus stats cache methods

    def get_corpus_stats(self, user_id: str) -> dict[str, Any] | None:
        """Get cached BM25 corpus statistics.

        Args:
            user_id: User ID

        Returns:
            Cached stats or None
        """
        key = self._make_key(self.CORPUS_PREFIX, user_id)

        if self._use_redis:
            try:
                data = self.redis.get(key)
                if data:
                    return json.loads(data)
            except Exception as e:
                logger.warning("Redis get failed: %s", e)

        return self._memory_cache.get(key)

    def set_corpus_stats(self, user_id: str, stats: dict[str, Any]) -> None:
        """Cache BM25 corpus statistics.

        Args:
            user_id: User ID
            stats: Corpus statistics
        """
        key = self._make_key(self.CORPUS_PREFIX, user_id)

        if self._use_redis:
            try:
                self.redis.setex(key, self.CORPUS_TTL, json.dumps(stats))
                return
            except Exception as e:
                logger.warning("Redis set failed: %s", e)

        self._memory_cache.set(key, stats, self.CORPUS_TTL)

    def invalidate_user_cache(self, user_id: str) -> None:
        """Invalidate all cache entries for a user.

        Called when user's KB is updated.

        Args:
            user_id: User ID
        """
        # For memory cache, we can't easily invalidate by pattern
        # Just invalidate corpus stats
        corpus_key = self._make_key(self.CORPUS_PREFIX, user_id)

        if self._use_redis:
            try:
                # Delete corpus stats
                self.redis.delete(corpus_key)
                # Delete search results by pattern (if supported)
                pattern = f"{self.SEARCH_PREFIX}*{user_id}*"
                keys = self.redis.keys(pattern)
                if keys:
                    self.redis.delete(*keys)
            except Exception as e:
                logger.warning("Redis invalidation failed: %s", e)
        else:
            self._memory_cache.delete(corpus_key)

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics.

        Returns:
            Dictionary with cache stats
        """
        if self._use_redis:
            try:
                info = self.redis.info("stats")
                return {
                    "backend": "redis",
                    "hits": info.get("keyspace_hits", 0),
                    "misses": info.get("keyspace_misses", 0),
                }
            except Exception:
                pass

        stats = self._memory_cache.stats
        return {
            "backend": "memory",
            "hits": stats.hits,
            "misses": stats.misses,
            "size": stats.size,
            "hit_rate": stats.hit_rate,
        }

