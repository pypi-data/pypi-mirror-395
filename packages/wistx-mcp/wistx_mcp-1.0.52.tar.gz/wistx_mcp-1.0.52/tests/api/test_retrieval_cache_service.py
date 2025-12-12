"""Unit tests for RetrievalCacheService.

Tests caching for query embeddings and search results.
"""

import pytest
import time
from unittest.mock import AsyncMock, MagicMock, patch

from api.services.retrieval_cache_service import (
    RetrievalCacheService,
    CacheEntry,
    CacheStats,
)


class TestRetrievalCacheService:
    """Tests for RetrievalCacheService."""

    @pytest.fixture
    def service(self):
        """Create cache service instance."""
        return RetrievalCacheService(
            embedding_ttl_seconds=300,
            result_ttl_seconds=60,
            max_cache_size=100,
        )

    @pytest.fixture
    def sample_embedding(self):
        """Sample embedding vector."""
        return [0.1] * 768

    @pytest.fixture
    def sample_results(self):
        """Sample search results."""
        return [
            {"chunk_id": "chunk-1", "content": "Test content 1", "score": 0.9},
            {"chunk_id": "chunk-2", "content": "Test content 2", "score": 0.8},
        ]

    def test_cache_entry_creation(self):
        """Test CacheEntry dataclass creation."""
        entry = CacheEntry(
            key="test-key",
            value={"data": "value"},
            created_at=time.time(),
            ttl_seconds=60,
        )
        
        assert entry.key == "test-key"
        assert entry.value["data"] == "value"
        assert entry.ttl_seconds == 60

    def test_cache_entry_is_expired_false(self):
        """Test CacheEntry.is_expired when not expired."""
        entry = CacheEntry(
            key="test-key",
            value="test",
            created_at=time.time(),
            ttl_seconds=60,
        )
        
        assert entry.is_expired() is False

    def test_cache_entry_is_expired_true(self):
        """Test CacheEntry.is_expired when expired."""
        entry = CacheEntry(
            key="test-key",
            value="test",
            created_at=time.time() - 120,  # 2 minutes ago
            ttl_seconds=60,  # 1 minute TTL
        )
        
        assert entry.is_expired() is True

    def test_cache_stats_defaults(self):
        """Test CacheStats default values."""
        stats = CacheStats()
        
        assert stats.hits == 0
        assert stats.misses == 0
        assert stats.evictions == 0
        assert stats.size == 0

    def test_cache_stats_hit_rate(self):
        """Test CacheStats hit rate calculation."""
        stats = CacheStats(hits=70, misses=30, evictions=5, size=50)
        
        hit_rate = stats.hit_rate()
        assert hit_rate == 0.7  # 70 / (70 + 30)

    def test_cache_stats_hit_rate_zero_requests(self):
        """Test CacheStats hit rate with zero requests."""
        stats = CacheStats()
        
        hit_rate = stats.hit_rate()
        assert hit_rate == 0.0

    def test_generate_cache_key(self, service):
        """Test cache key generation."""
        key1 = service._generate_cache_key("embedding", "test query", "user-123")
        key2 = service._generate_cache_key("embedding", "test query", "user-123")
        key3 = service._generate_cache_key("embedding", "different query", "user-123")
        
        # Same inputs should produce same key
        assert key1 == key2
        # Different inputs should produce different keys
        assert key1 != key3

    def test_generate_cache_key_includes_prefix(self, service):
        """Test cache key includes type prefix."""
        embedding_key = service._generate_cache_key("embedding", "query", "user")
        result_key = service._generate_cache_key("result", "query", "user")
        
        assert embedding_key != result_key

    @pytest.mark.asyncio
    async def test_get_embedding_cache_miss(self, service):
        """Test getting embedding from empty cache."""
        result = await service.get_embedding("unknown query", "user-123")
        
        assert result is None

    @pytest.mark.asyncio
    async def test_set_and_get_embedding(self, service, sample_embedding):
        """Test setting and getting embedding from cache."""
        query = "kubernetes deployment"
        user_id = "user-123"
        
        await service.set_embedding(query, user_id, sample_embedding)
        result = await service.get_embedding(query, user_id)
        
        assert result is not None
        assert len(result) == len(sample_embedding)

    @pytest.mark.asyncio
    async def test_get_results_cache_miss(self, service):
        """Test getting results from empty cache."""
        result = await service.get_results("unknown query", "user-123")
        
        assert result is None

    @pytest.mark.asyncio
    async def test_set_and_get_results(self, service, sample_results):
        """Test setting and getting results from cache."""
        query = "kubernetes deployment"
        user_id = "user-123"
        
        await service.set_results(query, user_id, sample_results)
        result = await service.get_results(query, user_id)
        
        assert result is not None
        assert len(result) == len(sample_results)

    @pytest.mark.asyncio
    async def test_cache_invalidation_by_user(self, service, sample_embedding):
        """Test cache invalidation for a specific user."""
        user_id = "user-123"
        
        await service.set_embedding("query1", user_id, sample_embedding)
        await service.set_embedding("query2", user_id, sample_embedding)
        
        # Invalidate user's cache
        await service.invalidate_user_cache(user_id)
        
        # Cache should be empty for user
        result1 = await service.get_embedding("query1", user_id)
        result2 = await service.get_embedding("query2", user_id)
        
        assert result1 is None
        assert result2 is None

    @pytest.mark.asyncio
    async def test_get_stats(self, service, sample_embedding):
        """Test getting cache statistics."""
        # Generate some cache activity
        await service.get_embedding("miss-query", "user-123")  # Miss
        await service.set_embedding("query", "user-123", sample_embedding)
        await service.get_embedding("query", "user-123")  # Hit
        
        stats = await service.get_stats()
        
        assert stats.misses >= 1
        assert stats.hits >= 1

    @pytest.mark.asyncio
    async def test_clear_all(self, service, sample_embedding, sample_results):
        """Test clearing entire cache."""
        await service.set_embedding("query", "user-123", sample_embedding)
        await service.set_results("query", "user-123", sample_results)
        
        await service.clear_all()
        
        embedding = await service.get_embedding("query", "user-123")
        results = await service.get_results("query", "user-123")
        
        assert embedding is None
        assert results is None

