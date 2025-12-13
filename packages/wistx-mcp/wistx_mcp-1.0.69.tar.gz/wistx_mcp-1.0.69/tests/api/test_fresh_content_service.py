"""Unit tests for fresh content service."""

import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

from api.services.fresh_content_service import (
    FreshContentService,
    FreshContentCache,
    GitHubRateLimiter,
    FreshnessInfo,
    FileContent,
)


class TestFreshContentCache:
    """Tests for FreshContentCache."""

    @pytest.mark.asyncio
    async def test_cache_set_and_get(self):
        """Test basic cache set and get operations."""
        cache = FreshContentCache(ttl_seconds=60)
        
        await cache.set("test_key", {"data": "value"})
        result = await cache.get("test_key")
        
        assert result == {"data": "value"}

    @pytest.mark.asyncio
    async def test_cache_expiration(self):
        """Test cache entry expiration."""
        cache = FreshContentCache(ttl_seconds=0)  # Immediate expiration
        
        await cache.set("test_key", {"data": "value"})
        result = await cache.get("test_key")
        
        assert result is None

    @pytest.mark.asyncio
    async def test_cache_invalidation(self):
        """Test cache invalidation by prefix."""
        cache = FreshContentCache(ttl_seconds=60)
        
        await cache.set("repo:owner/name:file1", "content1")
        await cache.set("repo:owner/name:file2", "content2")
        await cache.set("other:key", "content3")
        
        await cache.invalidate("repo:owner/name")
        
        assert await cache.get("repo:owner/name:file1") is None
        assert await cache.get("repo:owner/name:file2") is None
        assert await cache.get("other:key") == "content3"


class TestGitHubRateLimiter:
    """Tests for GitHubRateLimiter."""

    @pytest.mark.asyncio
    async def test_acquire_token(self):
        """Test acquiring a rate limit token."""
        limiter = GitHubRateLimiter(requests_per_minute=60, burst_limit=10)
        
        result = await limiter.acquire()
        
        assert result is True

    @pytest.mark.asyncio
    async def test_burst_limit(self):
        """Test burst limit enforcement."""
        limiter = GitHubRateLimiter(requests_per_minute=60, burst_limit=2)
        
        # Acquire all burst tokens
        assert await limiter.acquire() is True
        assert await limiter.acquire() is True
        # Third should fail
        assert await limiter.acquire() is False

    def test_update_from_headers(self):
        """Test updating rate limit from GitHub headers."""
        limiter = GitHubRateLimiter()
        
        limiter.update_from_headers({
            "x-ratelimit-remaining": "100",
            "x-ratelimit-reset": "1700000000",
        })
        
        assert limiter._rate_limit_remaining == 100
        assert limiter._rate_limit_reset == 1700000000.0


class TestFreshContentService:
    """Tests for FreshContentService."""

    @pytest.fixture
    def service(self):
        """Create a fresh content service instance."""
        return FreshContentService(
            cache_ttl_seconds=60,
            max_concurrent_requests=5,
            request_timeout=10.0,
        )

    def test_parse_repo_url_github(self, service):
        """Test parsing GitHub repository URL."""
        result = service._parse_repo_url("https://github.com/owner/repo")
        
        assert result == {"owner": "owner", "name": "repo"}

    def test_parse_repo_url_with_git_suffix(self, service):
        """Test parsing repository URL with .git suffix."""
        result = service._parse_repo_url("https://github.com/owner/repo.git")
        
        assert result == {"owner": "owner", "name": "repo"}

    def test_parse_repo_url_invalid(self, service):
        """Test parsing invalid repository URL."""
        result = service._parse_repo_url("invalid-url")
        
        assert result is None

    @pytest.mark.asyncio
    async def test_check_repository_freshness_no_token(self, service):
        """Test freshness check when no token is available."""
        with patch.object(service, "_get_github_token", return_value=None), \
             patch("api.services.fresh_content_service.settings") as mock_settings:
            mock_settings.github_internal_token = None
            
            result = await service.check_repository_freshness(
                repo_url="https://github.com/owner/repo",
                branch="main",
                indexed_commit_sha="abc123",
                user_id="user123",
            )
            
            assert result.freshness_check_error == "No GitHub token available"

    @pytest.mark.asyncio
    async def test_enrich_search_results_empty(self, service):
        """Test enriching empty search results."""
        results, freshness = await service.enrich_search_results_with_freshness(
            results=[],
            user_id="user123",
        )
        
        assert results == []
        assert isinstance(freshness, FreshnessInfo)


class TestFreshnessInfo:
    """Tests for FreshnessInfo dataclass."""

    def test_to_dict(self):
        """Test converting FreshnessInfo to dictionary."""
        info = FreshnessInfo(
            index_last_updated=datetime(2024, 1, 1, 12, 0, 0),
            latest_commit_sha="abc123",
            indexed_commit_sha="def456",
            commits_behind=5,
            stale_files=["file1.py", "file2.py"],
            fresh_content_fetched=True,
            freshness_check_performed=True,
        )
        
        result = info.to_dict()
        
        assert result["index_last_updated"] == "2024-01-01T12:00:00"
        assert result["latest_commit_sha"] == "abc123"
        assert result["commits_behind"] == 5
        assert result["stale_files_count"] == 2
        assert result["fresh_content_fetched"] is True

