"""Documentation crawler for multi-page documentation sites.

Implements industry-leading crawling capabilities:
- Sitemap.xml parsing for complete site discovery
- Intelligent link following within documentation domain
- Parallel crawling with rate limiting
- Content deduplication
- Pattern-based filtering
- Checkpointing for resume capability
- Incremental updates via content hashing
"""

import asyncio
import hashlib
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Optional
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

try:
    from crawl4ai import AsyncWebCrawler
    CRAWL4AI_AVAILABLE = True
except ImportError:
    CRAWL4AI_AVAILABLE = False
    AsyncWebCrawler = None

logger = logging.getLogger(__name__)


class DocumentationCheckpointManager:
    """Manages checkpoints for documentation crawling and indexing.

    Enables:
    - Resume interrupted crawls
    - Skip unchanged pages (incremental updates)
    - Track crawl progress
    """

    def __init__(self):
        """Initialize checkpoint manager."""
        self._db = None

    def _get_db(self):
        """Get MongoDB database connection."""
        if self._db is None:
            from api.database.mongodb import mongodb_manager
            self._db = mongodb_manager.get_database()
        return self._db

    def save_page_checkpoint(
        self,
        resource_id: str,
        page_url: str,
        content_hash: str,
        articles_created: int = 0,
        status: str = "completed",
        error: str | None = None,
    ) -> None:
        """Save checkpoint for a crawled page.

        Args:
            resource_id: Resource ID
            page_url: Page URL
            content_hash: Content hash for change detection
            articles_created: Number of articles created from this page
            status: Processing status
            error: Error message if failed
        """
        db = self._get_db()
        collection = db.indexed_documentation_pages

        checkpoint = {
            "resource_id": resource_id,
            "page_url": page_url,
            "content_hash": content_hash,
            "articles_created": articles_created,
            "status": status,
            "error": error,
            "processed_at": datetime.utcnow(),
        }

        collection.update_one(
            {"resource_id": resource_id, "page_url": page_url},
            {"$set": checkpoint},
            upsert=True,
        )

    def get_page_checkpoint(
        self,
        resource_id: str,
        page_url: str,
    ) -> dict[str, Any] | None:
        """Get checkpoint for a page.

        Args:
            resource_id: Resource ID
            page_url: Page URL

        Returns:
            Checkpoint data or None
        """
        db = self._get_db()
        collection = db.indexed_documentation_pages

        return collection.find_one({
            "resource_id": resource_id,
            "page_url": page_url,
        })

    def get_all_checkpoints(
        self,
        resource_id: str,
    ) -> list[dict[str, Any]]:
        """Get all checkpoints for a resource.

        Args:
            resource_id: Resource ID

        Returns:
            List of checkpoint data
        """
        db = self._get_db()
        collection = db.indexed_documentation_pages

        return list(collection.find({"resource_id": resource_id}))

    def is_page_unchanged(
        self,
        resource_id: str,
        page_url: str,
        content_hash: str,
    ) -> bool:
        """Check if page content is unchanged.

        Args:
            resource_id: Resource ID
            page_url: Page URL
            content_hash: Current content hash

        Returns:
            True if page is unchanged
        """
        checkpoint = self.get_page_checkpoint(resource_id, page_url)
        if not checkpoint:
            return False

        return (
            checkpoint.get("content_hash") == content_hash
            and checkpoint.get("status") == "completed"
        )

    def clear_checkpoints(self, resource_id: str) -> int:
        """Clear all checkpoints for a resource.

        Args:
            resource_id: Resource ID

        Returns:
            Number of checkpoints deleted
        """
        db = self._get_db()
        collection = db.indexed_documentation_pages

        result = collection.delete_many({"resource_id": resource_id})
        return result.deleted_count

    def get_crawl_progress(self, resource_id: str) -> dict[str, Any]:
        """Get crawl progress for a resource.

        Args:
            resource_id: Resource ID

        Returns:
            Progress data
        """
        checkpoints = self.get_all_checkpoints(resource_id)

        total = len(checkpoints)
        completed = sum(1 for c in checkpoints if c.get("status") == "completed")
        failed = sum(1 for c in checkpoints if c.get("status") == "failed")
        articles = sum(c.get("articles_created", 0) for c in checkpoints)

        return {
            "total_pages": total,
            "completed_pages": completed,
            "failed_pages": failed,
            "total_articles": articles,
            "progress_percent": (completed / total * 100) if total > 0 else 0,
        }


# Singleton checkpoint manager
checkpoint_manager = DocumentationCheckpointManager()


@dataclass
class CrawledPage:
    """Represents a crawled documentation page."""

    url: str
    title: str
    content: str
    markdown: str
    content_hash: str
    crawled_at: datetime
    links: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CrawlConfig:
    """Configuration for documentation crawling."""

    max_pages: int = 100
    max_depth: int = 5
    rate_limit_delay: float = 1.0
    parallel_requests: int = 5
    include_patterns: list[str] = field(default_factory=list)
    exclude_patterns: list[str] = field(default_factory=list)
    follow_external_links: bool = False
    respect_robots_txt: bool = True
    timeout_seconds: float = 30.0


class DocumentationCrawler:
    """Crawl multi-page documentation sites.

    Features:
    - Sitemap.xml parsing for complete site discovery
    - Link following within domain
    - Parallel crawling with configurable concurrency
    - Content deduplication via hashing
    - Pattern-based URL filtering
    - Progress callbacks for activity logging
    """

    def __init__(self, config: CrawlConfig | None = None):
        """Initialize documentation crawler.

        Args:
            config: Crawl configuration (uses defaults if not provided)
        """
        self.config = config or CrawlConfig()
        self.visited_urls: set[str] = set()
        self.content_hashes: set[str] = set()
        self.url_queue: asyncio.Queue = asyncio.Queue()
        self.results: list[CrawledPage] = []
        self._semaphore: asyncio.Semaphore | None = None

    def _normalize_url(self, url: str) -> str:
        """Normalize URL for deduplication.

        Args:
            url: URL to normalize

        Returns:
            Normalized URL string
        """
        parsed = urlparse(url)
        # Remove fragment and trailing slashes
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path.rstrip('/')}"
        if parsed.query:
            normalized += f"?{parsed.query}"
        return normalized

    def _is_valid_url(self, url: str, base_domain: str) -> bool:
        """Check if URL should be crawled.

        Args:
            url: URL to check
            base_domain: Base domain to restrict crawling to

        Returns:
            True if URL should be crawled
        """
        try:
            parsed = urlparse(url)

            # Must be HTTP(S)
            if parsed.scheme not in ("http", "https"):
                return False

            # Check domain restriction
            if not self.config.follow_external_links:
                if parsed.netloc != base_domain:
                    return False

            # Check exclude patterns
            for pattern in self.config.exclude_patterns:
                if re.search(pattern, url):
                    return False

            # Check include patterns (if specified, URL must match at least one)
            if self.config.include_patterns:
                if not any(re.search(p, url) for p in self.config.include_patterns):
                    return False

            # Skip common non-documentation URLs
            skip_extensions = (
                ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
                ".css", ".js", ".woff", ".woff2", ".ttf", ".eot",
                ".pdf", ".zip", ".tar", ".gz", ".mp4", ".webm",
            )
            if any(parsed.path.lower().endswith(ext) for ext in skip_extensions):
                return False

            return True

        except Exception:
            return False

    def _compute_content_hash(self, content: str) -> str:
        """Compute hash for content deduplication.

        Args:
            content: Content to hash

        Returns:
            SHA256 hash string
        """
        # Normalize whitespace for better deduplication
        normalized = " ".join(content.split())
        return hashlib.sha256(normalized.encode()).hexdigest()

    async def _fetch_sitemap(self, base_url: str) -> list[str]:
        """Fetch and parse sitemap.xml.

        Args:
            base_url: Base URL of the documentation site

        Returns:
            List of URLs from sitemap
        """
        sitemap_urls = []
        parsed = urlparse(base_url)
        sitemap_url = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"

        try:
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.get(sitemap_url)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "xml")

                    # Handle sitemap index
                    sitemap_tags = soup.find_all("sitemap")
                    if sitemap_tags:
                        for sitemap in sitemap_tags:
                            loc = sitemap.find("loc")
                            if loc:
                                nested_urls = await self._fetch_nested_sitemap(loc.text)
                                sitemap_urls.extend(nested_urls)

                    # Handle regular sitemap
                    url_tags = soup.find_all("url")
                    for url_tag in url_tags:
                        loc = url_tag.find("loc")
                        if loc:
                            sitemap_urls.append(loc.text)

                    logger.info("Found %d URLs in sitemap for %s", len(sitemap_urls), base_url)
                else:
                    logger.debug("No sitemap found at %s (status: %d)", sitemap_url, response.status_code)

        except Exception as e:
            logger.debug("Error fetching sitemap: %s", e)

        return sitemap_urls

    async def _fetch_nested_sitemap(self, sitemap_url: str) -> list[str]:
        """Fetch nested sitemap URLs.

        Args:
            sitemap_url: URL of the nested sitemap

        Returns:
            List of URLs from nested sitemap
        """
        urls = []
        try:
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.get(sitemap_url)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "xml")
                    for url_tag in soup.find_all("url"):
                        loc = url_tag.find("loc")
                        if loc:
                            urls.append(loc.text)
        except Exception as e:
            logger.debug("Error fetching nested sitemap %s: %s", sitemap_url, e)

        return urls


    def _extract_links(self, html: str, base_url: str) -> list[str]:
        """Extract links from HTML content.

        Args:
            html: HTML content
            base_url: Base URL for resolving relative links

        Returns:
            List of absolute URLs
        """
        links = []
        try:
            soup = BeautifulSoup(html, "html.parser")

            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]

                # Skip anchors and javascript
                if href.startswith("#") or href.startswith("javascript:"):
                    continue

                # Resolve relative URLs
                absolute_url = urljoin(base_url, href)
                links.append(self._normalize_url(absolute_url))

        except Exception as e:
            logger.debug("Error extracting links: %s", e)

        return list(set(links))

    async def _crawl_page(
        self,
        url: str,
        crawler: Any,
        base_domain: str,
    ) -> CrawledPage | None:
        """Crawl a single page.

        Args:
            url: URL to crawl
            crawler: AsyncWebCrawler instance
            base_domain: Base domain for link filtering

        Returns:
            CrawledPage or None if failed
        """
        if not self._semaphore:
            self._semaphore = asyncio.Semaphore(self.config.parallel_requests)

        async with self._semaphore:
            try:
                # Rate limiting
                await asyncio.sleep(self.config.rate_limit_delay)

                result = await crawler.arun(url=url, bypass_cache=True)

                markdown = result.markdown or ""
                html = result.html or ""

                if not markdown and not html:
                    logger.debug("No content from %s", url)
                    return None

                content = markdown if markdown else html
                content_hash = self._compute_content_hash(content)

                # Check for duplicate content
                if content_hash in self.content_hashes:
                    logger.debug("Duplicate content detected for %s", url)
                    return None

                self.content_hashes.add(content_hash)

                # Extract title
                title = url.split("/")[-1] or "Documentation"
                if html:
                    soup = BeautifulSoup(html, "html.parser")
                    title_tag = soup.find("title")
                    if title_tag:
                        title = title_tag.text.strip()
                    else:
                        h1_tag = soup.find("h1")
                        if h1_tag:
                            title = h1_tag.text.strip()

                # Extract links for further crawling
                links = self._extract_links(html, url) if html else []
                valid_links = [
                    link for link in links
                    if self._is_valid_url(link, base_domain) and link not in self.visited_urls
                ]

                return CrawledPage(
                    url=url,
                    title=title,
                    content=content,
                    markdown=markdown,
                    content_hash=content_hash,
                    crawled_at=datetime.utcnow(),
                    links=valid_links,
                )

            except Exception as e:
                logger.warning("Error crawling %s: %s", url, e)
                return None

    async def crawl(
        self,
        start_url: str,
        activity_callback: Callable[[str, str, dict[str, Any] | None], None] | None = None,
    ) -> list[CrawledPage]:
        """Crawl a documentation site starting from the given URL.

        Args:
            start_url: Starting URL for crawling
            activity_callback: Optional callback for progress logging

        Returns:
            List of CrawledPage objects
        """
        if not CRAWL4AI_AVAILABLE:
            logger.error("crawl4ai not available, cannot crawl documentation")
            return []

        # Reset state
        self.visited_urls = set()
        self.content_hashes = set()
        self.results = []

        parsed = urlparse(start_url)
        base_domain = parsed.netloc

        if activity_callback:
            activity_callback("CRAWL_STARTED", f"Starting crawl of {start_url}", {"url": start_url})

        # Try to get URLs from sitemap first
        sitemap_urls = await self._fetch_sitemap(start_url)

        if sitemap_urls:
            if activity_callback:
                activity_callback(
                    "SITEMAP_FOUND",
                    f"Found {len(sitemap_urls)} URLs in sitemap",
                    {"sitemap_urls": len(sitemap_urls)},
                )

            # Filter sitemap URLs
            urls_to_crawl = [
                url for url in sitemap_urls
                if self._is_valid_url(url, base_domain)
            ][:self.config.max_pages]
        else:
            # Start with the initial URL and discover via links
            urls_to_crawl = [start_url]

        async with AsyncWebCrawler() as crawler:
            depth = 0

            while urls_to_crawl and len(self.results) < self.config.max_pages and depth < self.config.max_depth:
                # Filter out already visited URLs
                urls_to_crawl = [url for url in urls_to_crawl if url not in self.visited_urls]

                if not urls_to_crawl:
                    break

                if activity_callback:
                    activity_callback(
                        "CRAWLING_BATCH",
                        f"Crawling batch of {len(urls_to_crawl)} URLs (depth {depth})",
                        {"batch_size": len(urls_to_crawl), "depth": depth},
                    )

                # Mark URLs as visited
                for url in urls_to_crawl:
                    self.visited_urls.add(url)

                # Crawl in parallel
                tasks = [
                    self._crawl_page(url, crawler, base_domain)
                    for url in urls_to_crawl[:self.config.parallel_requests * 2]
                ]

                pages = await asyncio.gather(*tasks)

                # Collect results and new URLs
                new_urls = []
                for page in pages:
                    if page:
                        self.results.append(page)
                        new_urls.extend(page.links)

                        if activity_callback:
                            activity_callback(
                                "PAGE_CRAWLED",
                                f"Crawled: {page.title}",
                                {"url": page.url, "title": page.title, "total_pages": len(self.results)},
                            )

                # Prepare next batch
                urls_to_crawl = list(set(new_urls))
                depth += 1

        if activity_callback:
            activity_callback(
                "CRAWL_COMPLETE",
                f"Completed crawling {len(self.results)} pages",
                {"total_pages": len(self.results)},
            )

        logger.info("Crawled %d pages from %s", len(self.results), start_url)
        return self.results

    async def crawl_incremental(
        self,
        start_url: str,
        resource_id: str,
        activity_callback: Callable[[str, str, dict[str, Any] | None], None] | None = None,
    ) -> tuple[list[CrawledPage], list[CrawledPage]]:
        """Crawl with incremental update support.

        Skips pages that haven't changed since last crawl.

        Args:
            start_url: Starting URL for crawling
            resource_id: Resource ID for checkpoint lookup
            activity_callback: Optional callback for progress logging

        Returns:
            Tuple of (new_or_changed_pages, unchanged_pages)
        """
        if not CRAWL4AI_AVAILABLE:
            logger.error("crawl4ai not available, cannot crawl documentation")
            return [], []

        # Reset state
        self.visited_urls = set()
        self.content_hashes = set()
        self.results = []

        new_or_changed: list[CrawledPage] = []
        unchanged: list[CrawledPage] = []

        parsed = urlparse(start_url)
        base_domain = parsed.netloc

        if activity_callback:
            activity_callback(
                "INCREMENTAL_CRAWL_STARTED",
                f"Starting incremental crawl of {start_url}",
                {"url": start_url, "resource_id": resource_id},
            )

        # Get existing checkpoints
        existing_checkpoints = {
            cp["page_url"]: cp
            for cp in checkpoint_manager.get_all_checkpoints(resource_id)
        }

        if existing_checkpoints:
            activity_callback(
                "CHECKPOINTS_LOADED",
                f"Found {len(existing_checkpoints)} existing page checkpoints",
                {"checkpoint_count": len(existing_checkpoints)},
            ) if activity_callback else None

        # Get URLs to crawl
        sitemap_urls = await self._fetch_sitemap(start_url)

        if sitemap_urls:
            urls_to_crawl = [
                url for url in sitemap_urls
                if self._is_valid_url(url, base_domain)
            ][:self.config.max_pages]
        else:
            urls_to_crawl = [start_url]

        async with AsyncWebCrawler() as crawler:
            depth = 0

            while urls_to_crawl and len(self.results) < self.config.max_pages and depth < self.config.max_depth:
                urls_to_crawl = [url for url in urls_to_crawl if url not in self.visited_urls]

                if not urls_to_crawl:
                    break

                for url in urls_to_crawl:
                    self.visited_urls.add(url)

                tasks = [
                    self._crawl_page(url, crawler, base_domain)
                    for url in urls_to_crawl[:self.config.parallel_requests * 2]
                ]

                pages = await asyncio.gather(*tasks)

                new_urls = []
                for page in pages:
                    if page:
                        self.results.append(page)
                        new_urls.extend(page.links)

                        # Check if page is unchanged
                        if checkpoint_manager.is_page_unchanged(
                            resource_id, page.url, page.content_hash
                        ):
                            unchanged.append(page)
                            if activity_callback:
                                activity_callback(
                                    "PAGE_UNCHANGED",
                                    f"Skipping unchanged: {page.title}",
                                    {"url": page.url, "title": page.title},
                                )
                        else:
                            new_or_changed.append(page)
                            if activity_callback:
                                activity_callback(
                                    "PAGE_CHANGED",
                                    f"Processing changed: {page.title}",
                                    {"url": page.url, "title": page.title},
                                )

                urls_to_crawl = list(set(new_urls))
                depth += 1

        if activity_callback:
            activity_callback(
                "INCREMENTAL_CRAWL_COMPLETE",
                f"Crawled {len(self.results)} pages: {len(new_or_changed)} changed, {len(unchanged)} unchanged",
                {
                    "total_pages": len(self.results),
                    "changed_pages": len(new_or_changed),
                    "unchanged_pages": len(unchanged),
                },
            )

        logger.info(
            "Incremental crawl of %s: %d total, %d changed, %d unchanged",
            start_url, len(self.results), len(new_or_changed), len(unchanged),
        )

        return new_or_changed, unchanged


# Singleton instance with default config
documentation_crawler = DocumentationCrawler()