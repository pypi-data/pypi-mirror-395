"""Fresh Content Service - Fetch fresh content from GitHub at query time.

This service enables real-time content freshness checking and retrieval
for search results, ensuring users get up-to-date information even when
the index is stale.

Production Features:
- Rate limiting to respect GitHub API limits
- Caching to avoid redundant API calls
- Graceful degradation on failures
- Concurrent request limiting
- OAuth token management
- Freshness metadata tracking
"""

import asyncio
import base64
import hashlib
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Optional
from urllib.parse import urlparse

import httpx

from api.config import settings
from api.database.mongodb import mongodb_manager

logger = logging.getLogger(__name__)


@dataclass
class FreshnessInfo:
    """Freshness metadata for search results."""
    
    index_last_updated: Optional[datetime] = None
    latest_commit_sha: Optional[str] = None
    indexed_commit_sha: Optional[str] = None
    commits_behind: int = 0
    stale_files: list[str] = field(default_factory=list)
    fresh_files: list[str] = field(default_factory=list)
    fresh_content_fetched: bool = False
    freshness_check_performed: bool = False
    freshness_check_error: Optional[str] = None
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "index_last_updated": self.index_last_updated.isoformat() if self.index_last_updated else None,
            "latest_commit_sha": self.latest_commit_sha,
            "indexed_commit_sha": self.indexed_commit_sha,
            "commits_behind": self.commits_behind,
            "stale_files_count": len(self.stale_files),
            "stale_files": self.stale_files[:10],  # Limit for response size
            "fresh_content_fetched": self.fresh_content_fetched,
            "freshness_check_performed": self.freshness_check_performed,
            "freshness_check_error": self.freshness_check_error,
        }


@dataclass
class FileContent:
    """Content fetched from GitHub."""
    
    file_path: str
    content: str
    sha: str
    size: int
    encoding: str
    content_hash: str
    fetched_at: datetime = field(default_factory=datetime.utcnow)
    is_stale: bool = False
    previous_hash: Optional[str] = None


class FreshContentCache:
    """In-memory cache for fresh content with TTL."""
    
    def __init__(self, ttl_seconds: int = 300, max_size: int = 1000):
        """Initialize cache.
        
        Args:
            ttl_seconds: Time-to-live for cache entries (default: 5 minutes)
            max_size: Maximum number of entries
        """
        self._cache: dict[str, tuple[Any, float]] = {}
        self._ttl = ttl_seconds
        self._max_size = max_size
        self._lock = asyncio.Lock()
    
    async def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired."""
        async with self._lock:
            if key in self._cache:
                value, timestamp = self._cache[key]
                if time.time() - timestamp < self._ttl:
                    return value
                del self._cache[key]
            return None
    
    async def set(self, key: str, value: Any) -> None:
        """Set cache value with TTL."""
        async with self._lock:
            # Evict oldest entries if cache is full
            if len(self._cache) >= self._max_size:
                oldest_key = min(self._cache, key=lambda k: self._cache[k][1])
                del self._cache[oldest_key]
            self._cache[key] = (value, time.time())
    
    async def invalidate(self, key_prefix: str) -> None:
        """Invalidate all entries matching prefix."""
        async with self._lock:
            keys_to_delete = [k for k in self._cache if k.startswith(key_prefix)]
            for key in keys_to_delete:
                del self._cache[key]


class GitHubRateLimiter:
    """Rate limiter for GitHub API calls."""
    
    def __init__(
        self,
        requests_per_minute: int = 30,
        burst_limit: int = 10,
    ):
        """Initialize rate limiter.
        
        Args:
            requests_per_minute: Maximum requests per minute
            burst_limit: Maximum burst requests
        """
        self._requests_per_minute = requests_per_minute
        self._burst_limit = burst_limit
        self._tokens = float(burst_limit)
        self._last_update = time.time()
        self._lock = asyncio.Lock()
        self._rate_limit_remaining: Optional[int] = None
        self._rate_limit_reset: Optional[float] = None
    
    async def acquire(self) -> bool:
        """Acquire a token for making a request.
        
        Returns:
            True if request can proceed, False if rate limited
        """
        async with self._lock:
            now = time.time()
            
            # Check GitHub's rate limit header
            if self._rate_limit_remaining is not None and self._rate_limit_remaining <= 5:
                if self._rate_limit_reset and now < self._rate_limit_reset:
                    wait_time = self._rate_limit_reset - now
                    logger.warning(
                        "GitHub rate limit nearly exhausted, waiting %.1fs",
                        wait_time,
                    )
                    return False

            # Token bucket algorithm
            time_passed = now - self._last_update
            self._tokens = min(
                self._burst_limit,
                self._tokens + time_passed * (self._requests_per_minute / 60.0),
            )
            self._last_update = now

            if self._tokens >= 1:
                self._tokens -= 1
                return True
            return False

    def update_from_headers(self, headers: dict[str, str]) -> None:
        """Update rate limit info from GitHub response headers."""
        if "x-ratelimit-remaining" in headers:
            self._rate_limit_remaining = int(headers["x-ratelimit-remaining"])
        if "x-ratelimit-reset" in headers:
            self._rate_limit_reset = float(headers["x-ratelimit-reset"])


class FreshContentService:
    """Service for fetching fresh content from GitHub.

    This service provides query-time content freshness checking and retrieval,
    enabling users to get up-to-date results even when the search index is stale.
    """

    def __init__(
        self,
        cache_ttl_seconds: int = 300,
        max_concurrent_requests: int = 5,
        request_timeout: float = 10.0,
        max_stale_minutes: int = 60,
    ):
        """Initialize fresh content service.

        Args:
            cache_ttl_seconds: Cache TTL in seconds (default: 5 minutes)
            max_concurrent_requests: Maximum concurrent GitHub API requests
            request_timeout: Request timeout in seconds
            max_stale_minutes: Default threshold for considering content stale
        """
        self._cache = FreshContentCache(ttl_seconds=cache_ttl_seconds)
        self._rate_limiter = GitHubRateLimiter()
        self._semaphore = asyncio.Semaphore(max_concurrent_requests)
        self._timeout = request_timeout
        self._max_stale_minutes = max_stale_minutes
        self._http_client: Optional[httpx.AsyncClient] = None

    async def _get_http_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._http_client is None or self._http_client.is_closed:
            self._http_client = httpx.AsyncClient(
                timeout=httpx.Timeout(self._timeout),
                limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
            )
        return self._http_client

    async def close(self) -> None:
        """Close HTTP client."""
        if self._http_client and not self._http_client.is_closed:
            await self._http_client.aclose()

    async def _get_github_token(self, user_id: str) -> Optional[str]:
        """Get GitHub OAuth token for user.

        Args:
            user_id: User ID

        Returns:
            Decrypted OAuth token or None
        """
        try:
            from api.services.oauth_service import oauth_service
            return await oauth_service.get_github_token(user_id)
        except Exception as e:
            logger.warning("Error getting OAuth token for user %s: %s", user_id, e)
            return None

    async def check_repository_freshness(
        self,
        repo_url: str,
        branch: str,
        indexed_commit_sha: Optional[str],
        user_id: str,
    ) -> FreshnessInfo:
        """Check if repository has new commits since last index.

        Args:
            repo_url: Repository URL
            branch: Branch name
            indexed_commit_sha: SHA of commit when index was last updated
            user_id: User ID for OAuth token

        Returns:
            FreshnessInfo with comparison results
        """
        freshness = FreshnessInfo(indexed_commit_sha=indexed_commit_sha)

        # Check cache first
        cache_key = f"repo_freshness:{repo_url}:{branch}"
        cached = await self._cache.get(cache_key)
        if cached:
            return cached

        try:
            # Parse repository URL
            repo_info = self._parse_repo_url(repo_url)
            if not repo_info:
                freshness.freshness_check_error = "Invalid repository URL"
                return freshness

            # Get GitHub token
            token = await self._get_github_token(user_id)
            if not token:
                token = settings.github_internal_token

            if not token:
                freshness.freshness_check_error = "No GitHub token available"
                return freshness

            # Check rate limit
            if not await self._rate_limiter.acquire():
                freshness.freshness_check_error = "Rate limited"
                return freshness

            # Fetch latest commit
            async with self._semaphore:
                client = await self._get_http_client()
                headers = {"Authorization": f"token {token}"}

                url = f"https://api.github.com/repos/{repo_info['owner']}/{repo_info['name']}/commits/{branch}"
                response = await client.get(url, headers=headers)

                self._rate_limiter.update_from_headers(dict(response.headers))

                if response.status_code == 200:
                    data = response.json()
                    freshness.latest_commit_sha = data.get("sha")
                    freshness.freshness_check_performed = True

                    # Compare commits
                    if indexed_commit_sha and freshness.latest_commit_sha:
                        if indexed_commit_sha != freshness.latest_commit_sha:
                            # Get commit count difference
                            compare_url = (
                                f"https://api.github.com/repos/{repo_info['owner']}/"
                                f"{repo_info['name']}/compare/{indexed_commit_sha}...{freshness.latest_commit_sha}"
                            )
                            compare_response = await client.get(compare_url, headers=headers)
                            if compare_response.status_code == 200:
                                compare_data = compare_response.json()
                                freshness.commits_behind = compare_data.get("ahead_by", 0)

                                # Get list of changed files
                                for file_info in compare_data.get("files", [])[:50]:
                                    freshness.stale_files.append(file_info.get("filename", ""))
                else:
                    freshness.freshness_check_error = f"GitHub API error: {response.status_code}"

            # Cache the result
            await self._cache.set(cache_key, freshness)

        except Exception as e:
            logger.error("Error checking repository freshness: %s", e, exc_info=True)
            freshness.freshness_check_error = str(e)

        return freshness

    async def fetch_fresh_file_content(
        self,
        repo_url: str,
        file_path: str,
        branch: str,
        user_id: str,
        indexed_hash: Optional[str] = None,
    ) -> Optional[FileContent]:
        """Fetch fresh file content from GitHub.

        Args:
            repo_url: Repository URL
            file_path: File path within repository
            branch: Branch name
            user_id: User ID for OAuth token
            indexed_hash: Hash of previously indexed content (for change detection)

        Returns:
            FileContent if successful, None otherwise
        """
        # Check cache first
        cache_key = f"file_content:{repo_url}:{branch}:{file_path}"
        cached = await self._cache.get(cache_key)
        if cached:
            return cached

        try:
            repo_info = self._parse_repo_url(repo_url)
            if not repo_info:
                logger.warning("Invalid repository URL: %s", repo_url)
                return None

            token = await self._get_github_token(user_id)
            if not token:
                token = settings.github_internal_token

            if not token:
                logger.warning("No GitHub token available for fresh content fetch")
                return None

            if not await self._rate_limiter.acquire():
                logger.warning("Rate limited, skipping fresh content fetch for %s", file_path)
                return None

            async with self._semaphore:
                client = await self._get_http_client()
                headers = {"Authorization": f"token {token}"}

                url = (
                    f"https://api.github.com/repos/{repo_info['owner']}/"
                    f"{repo_info['name']}/contents/{file_path}?ref={branch}"
                )

                response = await client.get(url, headers=headers)
                self._rate_limiter.update_from_headers(dict(response.headers))

                if response.status_code == 200:
                    data = response.json()

                    # Decode content
                    content = ""
                    if data.get("encoding") == "base64" and data.get("content"):
                        content = base64.b64decode(data["content"]).decode("utf-8", errors="ignore")

                    # Calculate content hash
                    content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

                    file_content = FileContent(
                        file_path=file_path,
                        content=content,
                        sha=data.get("sha", ""),
                        size=data.get("size", 0),
                        encoding=data.get("encoding", ""),
                        content_hash=content_hash,
                        is_stale=indexed_hash is not None and indexed_hash != content_hash,
                        previous_hash=indexed_hash,
                    )

                    # Cache the result
                    await self._cache.set(cache_key, file_content)

                    return file_content
                else:
                    logger.warning(
                        "Failed to fetch file content: %s/%s (status: %d)",
                        repo_url,
                        file_path,
                        response.status_code,
                    )
                    return None

        except Exception as e:
            logger.error("Error fetching fresh file content: %s", e, exc_info=True)
            return None

    async def enrich_search_results_with_freshness(
        self,
        results: list[dict[str, Any]],
        user_id: str,
        include_fresh_content: bool = False,
        max_stale_minutes: Optional[int] = None,
        max_files_to_check: int = 10,
    ) -> tuple[list[dict[str, Any]], FreshnessInfo]:
        """Enrich search results with freshness information.

        This method:
        1. Checks if indexed content is stale
        2. Optionally fetches fresh content for stale files
        3. Returns enriched results with freshness metadata

        Args:
            results: Search results from vector search
            user_id: User ID for OAuth token
            include_fresh_content: Whether to fetch fresh content for stale files
            max_stale_minutes: Consider stale if older than this (default: service default)
            max_files_to_check: Maximum files to check for freshness

        Returns:
            Tuple of (enriched_results, freshness_info)
        """
        if not results:
            return results, FreshnessInfo()

        stale_minutes = max_stale_minutes or self._max_stale_minutes
        freshness_info = FreshnessInfo()
        enriched_results = []

        # Group results by repository
        repos_to_check: dict[str, list[dict[str, Any]]] = {}
        for result in results:
            repo_url = result.get("repository_url") or result.get("repo_url")
            if repo_url:
                if repo_url not in repos_to_check:
                    repos_to_check[repo_url] = []
                repos_to_check[repo_url].append(result)

        # Check freshness for each repository
        files_checked = 0
        for repo_url, repo_results in repos_to_check.items():
            if files_checked >= max_files_to_check:
                break

            # Get repository info from first result
            first_result = repo_results[0]
            branch = first_result.get("branch", "main")
            indexed_commit = first_result.get("commit_sha")
            indexed_at = first_result.get("analyzed_at") or first_result.get("last_updated")

            # Check if index is stale based on time
            is_time_stale = False
            if indexed_at:
                if isinstance(indexed_at, str):
                    try:
                        indexed_at = datetime.fromisoformat(indexed_at.replace("Z", "+00:00"))
                    except ValueError:
                        indexed_at = None
                if indexed_at:
                    freshness_info.index_last_updated = indexed_at
                    age_minutes = (datetime.utcnow() - indexed_at.replace(tzinfo=None)).total_seconds() / 60
                    is_time_stale = age_minutes > stale_minutes

            # Check repository for new commits
            repo_freshness = await self.check_repository_freshness(
                repo_url=repo_url,
                branch=branch,
                indexed_commit_sha=indexed_commit,
                user_id=user_id,
            )

            # Update aggregated freshness info
            if repo_freshness.freshness_check_performed:
                freshness_info.freshness_check_performed = True
                freshness_info.latest_commit_sha = repo_freshness.latest_commit_sha
                freshness_info.indexed_commit_sha = repo_freshness.indexed_commit_sha
                freshness_info.commits_behind = max(
                    freshness_info.commits_behind,
                    repo_freshness.commits_behind,
                )

            if repo_freshness.freshness_check_error:
                freshness_info.freshness_check_error = repo_freshness.freshness_check_error

            # Process results for this repository
            for result in repo_results:
                enriched_result = dict(result)
                file_path = result.get("source_file") or result.get("file_path", "")

                # Check if this specific file changed
                file_is_stale = file_path in repo_freshness.stale_files

                if file_is_stale or (is_time_stale and include_fresh_content):
                    freshness_info.stale_files.append(file_path)

                    # Optionally fetch fresh content
                    if include_fresh_content and files_checked < max_files_to_check:
                        indexed_hash = result.get("source_hash") or result.get("metadata", {}).get("file_hash")
                        fresh_content = await self.fetch_fresh_file_content(
                            repo_url=repo_url,
                            file_path=file_path,
                            branch=branch,
                            user_id=user_id,
                            indexed_hash=indexed_hash,
                        )

                        if fresh_content:
                            enriched_result["fresh_content"] = {
                                "content": fresh_content.content[:10000],  # Limit content size
                                "content_hash": fresh_content.content_hash,
                                "is_changed": fresh_content.is_stale,
                                "fetched_at": fresh_content.fetched_at.isoformat(),
                            }
                            freshness_info.fresh_content_fetched = True
                            freshness_info.fresh_files.append(file_path)

                        files_checked += 1
                else:
                    freshness_info.fresh_files.append(file_path)

                enriched_result["freshness"] = {
                    "is_stale": file_is_stale or is_time_stale,
                    "indexed_commit": indexed_commit,
                    "latest_commit": repo_freshness.latest_commit_sha,
                }

                enriched_results.append(enriched_result)

        # Add results without repository info as-is
        for result in results:
            repo_url = result.get("repository_url") or result.get("repo_url")
            if not repo_url:
                enriched_results.append(dict(result))

        return enriched_results, freshness_info

    def _parse_repo_url(self, repo_url: str) -> Optional[dict[str, str]]:
        """Parse GitHub repository URL.

        Args:
            repo_url: Repository URL

        Returns:
            Dictionary with owner and name, or None if invalid
        """
        try:
            parsed = urlparse(repo_url)
            path_parts = parsed.path.strip("/").split("/")

            if len(path_parts) >= 2:
                return {
                    "owner": path_parts[0],
                    "name": path_parts[1].replace(".git", ""),
                }
            return None
        except Exception:
            return None


# Singleton instance
fresh_content_service = FreshContentService()

