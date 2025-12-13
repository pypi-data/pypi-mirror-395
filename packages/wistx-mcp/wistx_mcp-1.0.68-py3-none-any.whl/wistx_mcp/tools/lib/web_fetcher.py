"""Web Fetcher - On-demand URL content fetching using Crawl4AI.

Provides a simple interface for fetching web content with:
- JavaScript rendering support
- LLM-ready markdown output
- Retry and timeout handling
- Content validation
"""

import asyncio
import logging
from typing import Any
from urllib.parse import urlparse

from crawl4ai import AsyncWebCrawler

logger = logging.getLogger(__name__)


class WebFetcher:
    """Fetches web content on-demand using Crawl4AI.
    
    Designed for research orchestrator to fetch URLs discovered during
    on-demand knowledge research.
    """
    
    def __init__(
        self,
        timeout_seconds: float = 30.0,
        bypass_cache: bool = True,
        use_markdown: bool = True,
    ):
        """Initialize web fetcher.
        
        Args:
            timeout_seconds: Request timeout
            bypass_cache: Bypass Crawl4AI cache
            use_markdown: Output as markdown (vs raw HTML)
        """
        self.timeout_seconds = timeout_seconds
        self.bypass_cache = bypass_cache
        self.use_markdown = use_markdown
        self._crawler: AsyncWebCrawler | None = None
    
    async def _get_crawler(self) -> AsyncWebCrawler:
        """Get or create AsyncWebCrawler instance."""
        if self._crawler is None:
            self._crawler = AsyncWebCrawler()
        return self._crawler
    
    async def close(self) -> None:
        """Close the crawler instance."""
        if self._crawler:
            try:
                await self._crawler.close()
            except Exception as e:
                logger.debug("Error closing crawler: %s", e)
            self._crawler = None
    
    async def fetch_url(
        self,
        url: str,
        extract_metadata: bool = True,
    ) -> dict[str, Any] | None:
        """Fetch content from a URL.
        
        Args:
            url: URL to fetch
            extract_metadata: Include metadata in response
            
        Returns:
            Dictionary with content and metadata, or None if failed
        """
        try:
            # Validate URL
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                logger.warning("Invalid URL: %s", url)
                return None
            
            crawler = await self._get_crawler()
            
            # Fetch with timeout
            result = await asyncio.wait_for(
                crawler.arun(
                    url=url,
                    bypass_cache=self.bypass_cache,
                ),
                timeout=self.timeout_seconds,
            )
            
            if not result or not result.success:
                logger.warning("Failed to fetch %s: %s", url, getattr(result, 'error_message', 'Unknown error'))
                return None
            
            # Get content
            content = result.markdown if self.use_markdown else result.html
            if not content or len(content.strip()) < 100:
                logger.warning("Empty or minimal content from %s", url)
                return None
            
            response = {
                "url": url,
                "content": content,
                "content_type": "markdown" if self.use_markdown else "html",
            }
            
            # Extract metadata
            if extract_metadata:
                response["metadata"] = {
                    "title": getattr(result, 'title', None) or self._extract_title(content),
                    "links_count": len(result.links.get("internal", [])) + len(result.links.get("external", [])) if result.links else 0,
                    "content_length": len(content),
                }
            
            return response
            
        except asyncio.TimeoutError:
            logger.warning("Timeout fetching %s", url)
            return None
        except Exception as e:
            logger.error("Error fetching %s: %s", url, e)
            return None
    
    def _extract_title(self, content: str) -> str | None:
        """Extract title from markdown content."""
        if not content:
            return None
        
        # Look for first H1
        for line in content.split("\n")[:20]:
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
        
        return None
    
    async def fetch_multiple(
        self,
        urls: list[str],
        max_concurrent: int = 5,
    ) -> list[dict[str, Any]]:
        """Fetch multiple URLs concurrently.
        
        Args:
            urls: List of URLs to fetch
            max_concurrent: Maximum concurrent requests
            
        Returns:
            List of successful fetch results
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def fetch_with_semaphore(url: str) -> dict[str, Any] | None:
            async with semaphore:
                return await self.fetch_url(url)
        
        tasks = [fetch_with_semaphore(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return [r for r in results if isinstance(r, dict)]

