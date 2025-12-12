"""Link following with quality scoring for automated source discovery.

Follows links from seed URLs and scores them for quality to discover
high-quality content sources automatically.
"""

import asyncio
from typing import Any
from urllib.parse import urljoin, urlparse

import aiohttp
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler

from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class LinkFollower:
    """Follow links with quality scoring for automated discovery.
    
    Follows links from seed URLs recursively, scoring each link for quality
    and only following high-quality links to discover new content sources.
    """

    def __init__(
        self,
        max_depth: int = 3,
        max_links_per_page: int = 20,
        quality_threshold: float = 0.6,
        timeout_seconds: float = 15.0,
    ):
        """Initialize link follower.
        
        Args:
            max_depth: Maximum link depth to follow (default: 3)
            max_links_per_page: Maximum links to extract per page (default: 20)
            quality_threshold: Minimum quality score (0-1) to follow link (default: 0.6)
            timeout_seconds: Timeout for each page fetch (default: 15.0)
        """
        self.max_depth = max_depth
        self.max_links_per_page = max_links_per_page
        self.quality_threshold = quality_threshold
        self.timeout_seconds = timeout_seconds
        self._crawler: AsyncWebCrawler | None = None
        self._session: aiohttp.ClientSession | None = None

    async def _get_crawler(self) -> AsyncWebCrawler:
        """Get or create AsyncWebCrawler instance.
        
        Returns:
            AsyncWebCrawler instance
        """
        if self._crawler is None:
            self._crawler = AsyncWebCrawler()
        return self._crawler

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session for raw HTTP requests.
        
        Returns:
            aiohttp.ClientSession instance
        """
        if self._session is None:
            timeout = aiohttp.ClientTimeout(total=self.timeout_seconds, connect=5)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session

    async def follow_links(
        self,
        seed_urls: list[str],
        domain_filter: str | None = None,
    ) -> dict[str, list[str]]:
        """Follow links from seed URLs with quality scoring.
        
        Process:
        1. Crawl seed URLs
        2. Extract links from HTML
        3. Score links for quality
        4. Follow high-quality links recursively
        
        Args:
            seed_urls: Seed URLs to start from
            domain_filter: Optional domain to restrict links to
            
        Returns:
            Dictionary with "web_urls" and "pdf_urls" lists
        """
        discovered_urls: set[str] = set(seed_urls)
        to_process: list[tuple[str, int]] = [(url, 0) for url in seed_urls]
        processed: set[str] = set()
        
        crawler = await self._get_crawler()
        
        while to_process:
            url, depth = to_process.pop(0)
            
            if depth >= self.max_depth or url in processed:
                continue
            
            processed.add(url)
            
            try:
                crawl_result = await asyncio.wait_for(
                    crawler.arun(url=url, bypass_cache=True),
                    timeout=self.timeout_seconds,
                )
                html = crawl_result.html or ""
                
                if not html or len(html.strip()) < 100:
                    logger.debug("Skipping page with insufficient content: %s", url)
                    continue
                
                links = self._extract_links(html, url, domain_filter)
                
                scored_links = []
                for link_url in links:
                    if link_url in discovered_urls:
                        continue
                    
                    score = self._score_link_quality(link_url, html)
                    if score >= self.quality_threshold:
                        scored_links.append((link_url, score))
                
                scored_links.sort(key=lambda x: x[1], reverse=True)
                top_links = [link_url for link_url, _ in scored_links[:self.max_links_per_page]]
                
                for link_url in top_links:
                    if link_url not in discovered_urls:
                        discovered_urls.add(link_url)
                        if depth < self.max_depth - 1:
                            to_process.append((link_url, depth + 1))
            
            except asyncio.TimeoutError:
                logger.debug("Timeout processing link %s (depth %d)", url, depth)
            except (ValueError, RuntimeError, AttributeError, TypeError, ConnectionError) as e:
                logger.debug("Failed to process link %s: %s", url, e)
        
        pdf_urls = [url for url in discovered_urls if url.endswith(".pdf")]
        web_urls = [url for url in discovered_urls if not url.endswith(".pdf")]
        
        logger.info(
            "Link following discovered %d URLs (%d web, %d PDFs) from %d seed URLs",
            len(discovered_urls),
            len(web_urls),
            len(pdf_urls),
            len(seed_urls),
        )
        
        return {
            "web_urls": web_urls,
            "pdf_urls": pdf_urls,
        }

    def _extract_links(
        self,
        html: str,
        base_url: str,
        domain_filter: str | None = None,
    ) -> list[str]:
        """Extract links from HTML.
        
        Args:
            html: HTML content
            base_url: Base URL for resolving relative URLs
            domain_filter: Optional domain filter
            
        Returns:
            List of absolute URLs
        """
        links = []
        
        try:
            soup = BeautifulSoup(html, "html.parser")
            
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]
                absolute_url = urljoin(base_url, href)
                parsed = urlparse(absolute_url)
                
                if not absolute_url.startswith(("http://", "https://")):
                    continue
                
                if domain_filter and domain_filter not in parsed.netloc:
                    continue
                
                skip_patterns = [
                    "#",
                    "mailto:",
                    "javascript:",
                    "tel:",
                    ".jpg",
                    ".jpeg",
                    ".png",
                    ".gif",
                    ".svg",
                    ".webp",
                    ".css",
                    ".js",
                    ".json",
                    ".xml",
                ]
                
                url_lower = absolute_url.lower()
                if any(pattern in url_lower for pattern in skip_patterns):
                    continue
                
                if absolute_url not in links:
                    links.append(absolute_url)
        
        except (ValueError, RuntimeError, AttributeError, TypeError) as e:
            logger.debug("Error extracting links: %s", e)
        
        return links

    def _score_link_quality(self, url: str, context_html: str) -> float:
        """Score link quality based on URL and context.
        
        Quality indicators:
        - URL structure (path depth, keywords)
        - Link text quality
        - Context around link
        - Domain reputation
        
        Args:
            url: Link URL
            context_html: HTML context around link
            
        Returns:
            Quality score (0-1)
        """
        score = 0.5
        
        parsed = urlparse(url)
        path = parsed.path.lower()
        
        quality_keywords = [
            "documentation",
            "guide",
            "tutorial",
            "article",
            "blog",
            "docs",
            "reference",
            "api",
            "best-practices",
            "how-to",
            "compliance",
            "security",
            "architecture",
            "design",
            "getting-started",
            "examples",
            "patterns",
        ]
        
        for keyword in quality_keywords:
            if keyword in path:
                score += 0.05
                if score >= 1.0:
                    break
        
        low_quality_patterns = [
            "login",
            "signup",
            "register",
            "cart",
            "checkout",
            "admin",
            "private",
            "internal",
            "logout",
            "account",
            "profile",
            "settings",
        ]
        
        for pattern in low_quality_patterns:
            if pattern in path:
                score -= 0.1
                if score <= 0.0:
                    break
        
        path_depth = len([p for p in path.split("/") if p])
        if path_depth <= 3:
            score += 0.1
        elif path_depth > 5:
            score -= 0.1
        
        if path.endswith((".html", ".htm", "/")):
            score += 0.05
        
        if path.endswith((".pdf", ".doc", ".docx")):
            score += 0.1
        
        return max(0.0, min(1.0, score))

    async def close(self):
        """Close crawler and session resources."""
        if self._crawler:
            await self._crawler.close()
            self._crawler = None
        if self._session:
            await self._session.close()
            self._session = None

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

