"""Automated source discovery from trusted domains.

Uses sitemap discovery to automatically find URLs from trusted domains.
Leverages existing Crawl4AI infrastructure for web content.
Supports RSS/Atom feed discovery for automated content discovery.
"""

import asyncio
import re
from typing import Any
from xml.etree import ElementTree as ET
from urllib.parse import urljoin, urlparse

import aiohttp
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler

from ..utils.logger import setup_logger
from ..utils.url_cache import url_cache
from ..utils.config import settings
from .link_follower import LinkFollower

logger = setup_logger(__name__)


class SourceDiscovery:
    """Automatically discovers sources from trusted domains.
    
    Uses raw HTTP requests for sitemaps (XML), Crawl4AI for web content.
    Separates PDFs from web pages for different processing pipelines.
    """

    def __init__(self):
        """Initialize source discovery."""
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
            timeout = aiohttp.ClientTimeout(
                total=settings.sitemap_fetch_timeout_seconds,
                connect=10
            )
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session

    async def discover_from_domain(
        self,
        domain: str,
        discovery_mode: str,
        path_patterns: list[str],
        content_types: list[str] | None = None,
        enable_rss_discovery: bool = False,
        max_rss_feeds: int = 50,
        enable_link_following: bool = False,
        link_following_depth: int = 2,
        max_links_per_page: int = 20,
        link_quality_threshold: float = 0.6,
        max_sitemap_depth: int | None = None,
    ) -> dict[str, list[str]]:
        """Discover URLs from a domain.
        
        Args:
            domain: Domain to discover (e.g., "aws.amazon.com")
            discovery_mode: Discovery mode ("sitemap", "search", "crawl")
            path_patterns: Path patterns to match
            content_types: Content types to include (optional)
            enable_rss_discovery: Enable RSS/Atom feed discovery (default: False)
            max_rss_feeds: Maximum number of feeds to process (default: 50)
            enable_link_following: Enable link following with quality scoring (default: False)
            link_following_depth: Maximum depth for link following (default: 2)
            max_links_per_page: Maximum links to extract per page (default: 20)
            link_quality_threshold: Minimum quality score to follow link (default: 0.6)
            max_sitemap_depth: Maximum recursion depth for nested sitemaps (None = use default 3, 0 = no recursion)
            
        Returns:
            Dictionary with "web_urls" and "pdf_urls" lists
        """
        if discovery_mode == "sitemap":
            result = await self._discover_from_sitemap(domain, path_patterns, content_types, max_sitemap_depth=max_sitemap_depth)
        elif discovery_mode == "search":
            result = await self._discover_from_search(domain, path_patterns)
        elif discovery_mode == "crawl":
            result = await self._discover_from_crawl(domain, path_patterns, content_types)
        else:
            logger.warning("Unknown discovery mode: %s", discovery_mode)
            result = {"web_urls": [], "pdf_urls": []}
        
        if enable_rss_discovery:
            try:
                seed_urls = [f"https://{domain}", f"https://www.{domain}"]
                rss_result = await self._discover_from_rss_feeds(seed_urls, max_feeds=max_rss_feeds)
                result["web_urls"].extend(rss_result["web_urls"])
                result["pdf_urls"].extend(rss_result["pdf_urls"])
                logger.info(
                    "RSS discovery added %d web URLs and %d PDF URLs from %s",
                    len(rss_result["web_urls"]),
                    len(rss_result["pdf_urls"]),
                    domain,
                )
            except (ValueError, RuntimeError, AttributeError, TypeError, ConnectionError) as e:
                logger.warning("RSS discovery failed for %s: %s", domain, e)
        
        if enable_link_following:
            try:
                seed_urls = result["web_urls"][:10]
                if seed_urls:
                    async with LinkFollower(
                        max_depth=link_following_depth,
                        max_links_per_page=max_links_per_page,
                        quality_threshold=link_quality_threshold,
                    ) as link_follower:
                        link_result = await link_follower.follow_links(seed_urls, domain_filter=domain)
                        result["web_urls"].extend(link_result["web_urls"])
                        result["pdf_urls"].extend(link_result["pdf_urls"])
                        logger.info(
                            "Link following added %d web URLs and %d PDF URLs from %s",
                            len(link_result["web_urls"]),
                            len(link_result["pdf_urls"]),
                            domain,
                        )
            except (ValueError, RuntimeError, AttributeError, TypeError, ConnectionError) as e:
                logger.warning("Link following failed for %s: %s", domain, e)
        
        result["web_urls"] = list(set(result["web_urls"]))
        result["pdf_urls"] = list(set(result["pdf_urls"]))
        
        return result

    async def _discover_from_sitemap(
        self,
        domain: str,
        path_patterns: list[str],
        content_types: list[str] | None = None,
        max_sitemap_depth: int | None = None,
    ) -> dict[str, list[str]]:
        """Discover URLs from sitemap.xml using raw HTTP requests.
        
        Uses raw HTTP for sitemaps (XML), not Crawl4AI, for better reliability.
        Recursively fetches nested sitemaps from sitemap indexes.
        Separates PDFs from web pages for different processing pipelines.
        
        Args:
            domain: Domain to discover
            path_patterns: Path patterns to match
            content_types: Content types to include (optional)
            max_sitemap_depth: Maximum recursion depth for nested sitemaps (None = use default 3, 0 = no recursion)
            
        Returns:
            Dictionary with "web_urls" and "pdf_urls" lists
        """
        sitemap_urls = [
            f"https://{domain}/sitemap.xml",
            f"https://{domain}/sitemap_index.xml",
            f"https://www.{domain}/sitemap.xml",
            f"https://www.{domain}/sitemap_index.xml",
        ]

        discovered_urls: list[str] = []
        session = await self._get_session()
        processed_sitemaps: set[str] = set()
        max_depth = max_sitemap_depth if max_sitemap_depth is not None else 3
        
        if max_depth == 0:
            logger.info("Deep crawling disabled: limiting sitemap discovery to top-level sitemaps only")

        async def fetch_sitemap_recursive(sitemap_url: str, depth: int = 0) -> list[str]:
            """Recursively fetch sitemap and nested sitemaps.
            
            Args:
                sitemap_url: URL of sitemap to fetch
                depth: Current recursion depth
                
            Returns:
                List of discovered URLs
            """
            if depth > max_depth or sitemap_url in processed_sitemaps:
                return []

            processed_sitemaps.add(sitemap_url)
            urls: list[str] = []

            try:
                logger.debug("Fetching sitemap (depth %d): %s", depth, sitemap_url)

                async with session.get(sitemap_url, headers={"User-Agent": "Mozilla/5.0"}) as response:
                    if response.status != 200:
                        logger.debug("Sitemap returned status %d: %s", response.status, sitemap_url)
                        return []

                    content_type = response.headers.get("Content-Type", "").lower()
                    if "xml" not in content_type and "text" not in content_type:
                        logger.debug("Unexpected content type %s for sitemap: %s", content_type, sitemap_url)
                        return []

                    sitemap_content = await response.text()

                    if not sitemap_content or len(sitemap_content.strip()) < 50:
                        logger.debug("Empty or too short sitemap content: %s", sitemap_url)
                        return []

                    parsed_urls = self._parse_sitemap_xml(sitemap_content, sitemap_url)

                    if not parsed_urls:
                        logger.debug("No URLs found in sitemap: %s", sitemap_url)
                        return []

                    logger.info("Found %d URLs in sitemap: %s", len(parsed_urls), sitemap_url)

                    nested_sitemaps: list[str] = []
                    content_urls: list[str] = []

                    for url in parsed_urls:
                        url_lower = url.lower()
                        if "sitemap" in url_lower and (url_lower.endswith(".xml") or "sitemap" in url_lower):
                            nested_sitemaps.append(url)
                        else:
                            content_urls.append(url)

                    if nested_sitemaps:
                        logger.debug("Found %d nested sitemaps, fetching recursively...", len(nested_sitemaps))
                        for nested_url in nested_sitemaps:
                            nested_urls = await fetch_sitemap_recursive(nested_url, depth + 1)
                            urls.extend(nested_urls)

                    urls.extend(content_urls)

            except (asyncio.TimeoutError, aiohttp.ServerTimeoutError) as e:
                logger.warning("Timeout fetching sitemap %s (depth %d): %s", sitemap_url, depth, e)
                return []
            except aiohttp.ClientError as e:
                logger.debug("HTTP error fetching sitemap %s: %s", sitemap_url, e)
                return []
            except (ValueError, RuntimeError, AttributeError, TypeError, ConnectionError) as e:
                logger.debug("Error processing sitemap %s: %s", sitemap_url, e)
                return []

            return urls

        try:
            for sitemap_url in sitemap_urls:
                try:
                    urls = await fetch_sitemap_recursive(sitemap_url)
                    discovered_urls.extend(urls)
                except Exception as e:
                    logger.warning("Error fetching sitemap %s: %s", sitemap_url, e)
                    continue
        except Exception as e:
            logger.error("Error during sitemap discovery for domain %s: %s", domain, e)
            return {"web_urls": [], "pdf_urls": []}

        discovered_urls = list(set(discovered_urls))

        filtered_urls = self._filter_urls(discovered_urls, path_patterns, content_types)

        pdf_urls = [url for url in filtered_urls if url.endswith(".pdf")]
        web_urls = [url for url in filtered_urls if not url.endswith(".pdf")]

        logger.info(
            "Discovered %d URLs from %s (%d web, %d PDFs) after filtering",
            len(filtered_urls),
            domain,
            len(web_urls),
            len(pdf_urls),
        )

        return {
            "web_urls": web_urls,
            "pdf_urls": pdf_urls,
        }

    def _parse_sitemap_xml(self, sitemap_content: str, base_url: str) -> list[str]:
        """Parse sitemap XML to extract URLs.
        
        Handles both regular sitemaps and sitemap indexes.
        Includes fallback regex extraction for malformed XML.
        
        Args:
            sitemap_content: XML content of sitemap
            base_url: Base URL for resolving relative URLs
            
        Returns:
            List of discovered URLs
        """
        urls: list[str] = []

        sitemap_content_clean = self._clean_xml_content(sitemap_content)

        try:
            root = ET.fromstring(sitemap_content_clean)

            sitemap_ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"

            if root.tag.endswith("sitemapindex"):
                sitemap_refs = root.findall(f".//{sitemap_ns}sitemap/{sitemap_ns}loc")
                sitemap_refs.extend(root.findall(f".//{sitemap_ns}loc"))
                for ref in sitemap_refs:
                    if ref.text:
                        nested_url = urljoin(base_url, ref.text.strip())
                        logger.debug("Found nested sitemap: %s", nested_url)
                        urls.append(nested_url)

            elif root.tag.endswith("urlset"):
                url_elements = root.findall(f".//{sitemap_ns}url/{sitemap_ns}loc")
                url_elements.extend(root.findall(f".//{sitemap_ns}loc"))
                for elem in url_elements:
                    if elem.text:
                        url = urljoin(base_url, elem.text.strip())
                        urls.append(url)

        except ET.ParseError as e:
            logger.debug("XML parsing failed, trying regex fallback: %s", e)
            urls.extend(self._extract_urls_regex(sitemap_content, base_url))
        except (ValueError, RuntimeError, AttributeError, TypeError) as e:
            logger.debug("Error parsing sitemap, trying regex fallback: %s", e)
            urls.extend(self._extract_urls_regex(sitemap_content, base_url))

        return list(set(urls))

    def _clean_xml_content(self, content: str) -> str:
        """Clean XML content by removing HTML wrapper if present.
        
        Args:
            content: Raw content (may be HTML-wrapped XML)
            
        Returns:
            Cleaned XML content
        """
        content = content.strip()

        if content.startswith("<?xml") or content.startswith("<"):
            xml_match = re.search(r"(<\?xml.*?</(?:urlset|sitemapindex)>)", content, re.DOTALL)
            if xml_match:
                return xml_match.group(1)

        xml_match = re.search(r"(<urlset[^>]*>.*?</urlset>)", content, re.DOTALL | re.IGNORECASE)
        if xml_match:
            return xml_match.group(1)

        xml_match = re.search(r"(<sitemapindex[^>]*>.*?</sitemapindex>)", content, re.DOTALL | re.IGNORECASE)
        if xml_match:
            return xml_match.group(1)

        return content

    def _extract_urls_regex(self, content: str, base_url: str) -> list[str]:
        """Extract URLs using regex fallback when XML parsing fails.
        
        Args:
            content: Content to extract URLs from
            base_url: Base URL for resolving relative URLs
            
        Returns:
            List of extracted URLs
        """
        urls: list[str] = []

        url_patterns = [
            r"<loc>(.*?)</loc>",
            r'<loc\s*>(.*?)</loc>',
            r'url="([^"]+)"',
            r"url='([^']+)'",
            r"href=['\"](https?://[^'\"]+)['\"]",
        ]

        for pattern in url_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                url = match.strip()
                if url and (url.startswith("http") or url.startswith("/")):
                    full_url = urljoin(base_url, url)
                    if full_url.startswith("http"):
                        urls.append(full_url)

        return urls

    def _filter_urls(
        self,
        urls: list[str],
        path_patterns: list[str],
        content_types: list[str] | None = None,
    ) -> list[str]:
        """Filter URLs by path patterns and content types.
        
        Uses OR logic: URL matches if it matches ANY path pattern AND (if specified) ANY content type.
        If no path patterns specified, all URLs pass path filtering.
        If no content types specified, all URLs pass content type filtering.
        
        Args:
            urls: List of URLs to filter
            path_patterns: Path patterns to match (empty list = no filtering)
            content_types: Content types to include (None = no filtering)
            
        Returns:
            Filtered list of URLs
        """
        if not urls:
            return []

        if not path_patterns and not content_types:
            return urls

        filtered_urls = []

        for url in urls:
            url_lower = url.lower()
            parsed = urlparse(url)
            path = parsed.path.lower()

            path_match = True
            if path_patterns:
                path_match = any(pattern.lower() in path for pattern in path_patterns)

            content_match = True
            if content_types:
                has_extension = any(url_lower.endswith(f".{ct}") for ct in content_types)
                has_in_path = any(f".{ct}" in url_lower or f"/{ct}/" in path for ct in content_types)
                content_match = has_extension or has_in_path

            if path_match and content_match:
                filtered_urls.append(url)

        return filtered_urls

    async def _discover_from_search(
        self,
        domain: str,
        path_patterns: list[str],
    ) -> dict[str, list[str]]:
        """Discover URLs using domain-specific search APIs.
        
        Args:
            domain: Domain to search
            path_patterns: Path patterns (used as search queries for GitHub)
            
        Returns:
            Dictionary with "web_urls" and "pdf_urls" lists
        """
        if "github.com" in domain:
            return await self._discover_from_github(path_patterns)

        logger.warning("Search discovery not implemented for domain: %s", domain)
        return {"web_urls": [], "pdf_urls": []}

    async def _discover_from_github(self, search_queries: list[str]) -> dict[str, list[str]]:
        """Discover GitHub repositories using search API.
        
        Args:
            search_queries: List of search queries
            
        Returns:
            Dictionary with "web_urls" and "pdf_urls" lists
        """
        discovered_urls: list[str] = []
        session = await self._get_session()

        for query in search_queries:
            try:
                search_url = (
                    f"https://api.github.com/search/repositories"
                    f"?q={query}&sort=stars&order=desc&per_page=10"
                )

                async with session.get(search_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        repos = data.get("items", [])

                        for repo in repos:
                            repo_url = repo.get("html_url", "")
                            if repo_url:
                                discovered_urls.append(repo_url)

            except (ValueError, RuntimeError, AttributeError, TypeError, ConnectionError) as e:
                logger.warning("Failed to search GitHub for %s: %s", query, e)

        return {
            "web_urls": discovered_urls,
            "pdf_urls": [],
        }

    async def _discover_from_crawl(
        self,
        domain: str,
        path_patterns: list[str],
        content_types: list[str] | None = None,
    ) -> dict[str, list[str]]:
        """Discover URLs by crawling domain (not implemented yet).
        
        Args:
            domain: Domain to crawl
            path_patterns: Path patterns to match (unused, reserved for future)
            content_types: Content types to include (unused, reserved for future)
            
        Returns:
            Dictionary with "web_urls" and "pdf_urls" lists
        """
        _ = path_patterns
        _ = content_types
        logger.warning("Crawl discovery not implemented yet for domain: %s", domain)
        return {"web_urls": [], "pdf_urls": []}

    async def discover_all_for_domain(
        self, domain_config: dict[str, Any]
    ) -> dict[str, list[str]]:
        """Discover all URLs for a domain configuration.
        
        Args:
            domain_config: Domain configuration dictionary
            
        Returns:
            Dictionary with "web_urls" and "pdf_urls" lists
        """
        domain = domain_config["domain"]
        discovery_mode = domain_config.get("discovery_mode", "sitemap")
        path_patterns = domain_config.get("path_patterns", [])
        content_types = domain_config.get("content_types")
        enable_rss_discovery = domain_config.get("enable_rss_discovery", False)
        max_rss_feeds = domain_config.get("max_rss_feeds", 50)
        enable_link_following = domain_config.get("enable_link_following", False)
        link_following_depth = domain_config.get("link_following_depth", 2)
        max_links_per_page = domain_config.get("max_links_per_page", 20)
        link_quality_threshold = domain_config.get("link_quality_threshold", 0.6)
        max_sitemap_depth = domain_config.get("max_sitemap_depth")

        try:
            if discovery_mode == "sitemap":
                result = await self._discover_from_sitemap(
                    domain, path_patterns, content_types, max_sitemap_depth=max_sitemap_depth
                )
            elif discovery_mode == "search":
                result = await self._discover_from_search(domain, path_patterns)
            elif discovery_mode == "crawl":
                result = await self._discover_from_crawl(domain, path_patterns, content_types)
            else:
                logger.warning("Unknown discovery mode: %s", discovery_mode)
                result = {"web_urls": [], "pdf_urls": []}
        except (asyncio.TimeoutError, aiohttp.ServerTimeoutError) as e:
            logger.error("Timeout during discovery for domain %s: %s", domain, e)
            result = {"web_urls": [], "pdf_urls": []}
        except Exception as e:
            logger.error("Error during discovery for domain %s: %s", domain, e, exc_info=True)
            result = {"web_urls": [], "pdf_urls": []}
        
        if enable_rss_discovery:
            try:
                seed_urls = [f"https://{domain}", f"https://www.{domain}"]
                rss_result = await self._discover_from_rss_feeds(seed_urls, max_feeds=max_rss_feeds)
                result["web_urls"].extend(rss_result["web_urls"])
                result["pdf_urls"].extend(rss_result["pdf_urls"])
                logger.info(
                    "RSS discovery added %d web URLs and %d PDF URLs from %s",
                    len(rss_result["web_urls"]),
                    len(rss_result["pdf_urls"]),
                    domain,
                )
            except (ValueError, RuntimeError, AttributeError, TypeError, ConnectionError) as e:
                logger.warning("RSS discovery failed for %s: %s", domain, e)
        
        if enable_link_following:
            try:
                seed_urls = result["web_urls"][:10]
                if seed_urls:
                    async with LinkFollower(
                        max_depth=link_following_depth,
                        max_links_per_page=max_links_per_page,
                        quality_threshold=link_quality_threshold,
                    ) as link_follower:
                        link_result = await link_follower.follow_links(seed_urls, domain_filter=domain)
                        result["web_urls"].extend(link_result["web_urls"])
                        result["pdf_urls"].extend(link_result["pdf_urls"])
                        logger.info(
                            "Link following added %d web URLs and %d PDF URLs from %s",
                            len(link_result["web_urls"]),
                            len(link_result["pdf_urls"]),
                            domain,
                        )
            except (ValueError, RuntimeError, AttributeError, TypeError, ConnectionError) as e:
                logger.warning("Link following failed for %s: %s", domain, e)
        
        result["web_urls"] = list(set(result["web_urls"]))
        result["pdf_urls"] = list(set(result["pdf_urls"]))
        
        return result

    async def _discover_from_rss_feeds(
        self,
        seed_urls: list[str],
        max_feeds: int = 50,
    ) -> dict[str, list[str]]:
        """Discover URLs from RSS/Atom feeds.
        
        Process:
        1. Detect RSS/Atom feeds from seed URLs
        2. Parse feed entries
        3. Extract article URLs
        4. Filter by quality indicators
        
        Args:
            seed_urls: Seed URLs to discover feeds from
            max_feeds: Maximum feeds to process
            
        Returns:
            Dictionary with "web_urls" and "pdf_urls" lists
        """
        discovered_urls: list[str] = []
        session = await self._get_session()
        
        feed_paths = [
            "/feed",
            "/rss",
            "/atom",
            "/feed.xml",
            "/rss.xml",
            "/atom.xml",
            "/feeds/all",
            "/blog/feed",
            "/news/feed",
            "/feed/rss",
            "/feed/atom",
        ]
        
        feed_urls: set[str] = set()
        
        for seed_url in seed_urls:
            try:
                parsed = urlparse(seed_url)
                base_url = f"{parsed.scheme}://{parsed.netloc}"
                
                for path in feed_paths:
                    feed_url = f"{base_url}{path}"
                    if await self._is_valid_feed(feed_url):
                        feed_urls.add(feed_url)
                
                try:
                    timeout = aiohttp.ClientTimeout(total=10, connect=5)
                    async with session.get(seed_url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"}) as response:
                        if response.status == 200:
                            html = await response.text()
                            feed_links = self._extract_feed_links(html, base_url)
                            feed_urls.update(feed_links)
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    logger.debug("Failed to check feed links from %s: %s", seed_url, e)
            except (ValueError, RuntimeError, AttributeError, TypeError) as e:
                logger.debug("Error processing seed URL %s: %s", seed_url, e)
        
        feed_list = list(feed_urls)[:max_feeds]
        logger.info("Discovered %d feed URLs, processing %d", len(feed_urls), len(feed_list))
        
        for feed_url in feed_list:
            try:
                urls = await self._parse_feed(feed_url)
                discovered_urls.extend(urls)
            except (ValueError, RuntimeError, AttributeError, TypeError, ConnectionError) as e:
                logger.debug("Failed to parse feed %s: %s", feed_url, e)
        
        pdf_urls = [url for url in discovered_urls if url.endswith(".pdf")]
        web_urls = [url for url in discovered_urls if not url.endswith(".pdf")]
        
        logger.info(
            "RSS discovery found %d URLs (%d web, %d PDFs)",
            len(discovered_urls),
            len(web_urls),
            len(pdf_urls),
        )
        
        return {
            "web_urls": web_urls,
            "pdf_urls": pdf_urls,
        }
    
    async def _is_valid_feed(self, feed_url: str) -> bool:
        """Check if URL is a valid RSS/Atom feed.
        
        Args:
            feed_url: URL to check
            
        Returns:
            True if valid feed
        """
        try:
            session = await self._get_session()
            timeout = aiohttp.ClientTimeout(total=10, connect=5)
            async with session.get(feed_url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"}) as response:
                if response.status != 200:
                    return False
                
                content_type = response.headers.get("Content-Type", "").lower()
                if "xml" not in content_type and "rss" not in content_type and "atom" not in content_type:
                    if not feed_url.endswith((".xml", "/feed", "/rss", "/atom")):
                        return False
                
                content = await response.text()
                if not content or len(content.strip()) < 50:
                    return False
                
                return "<rss" in content or "<feed" in content or "<rdf:RDF" in content
        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError, RuntimeError, AttributeError, TypeError, ConnectionError):
            return False
    
    def _extract_feed_links(self, html: str, base_url: str) -> list[str]:
        """Extract RSS/Atom feed links from HTML.
        
        Args:
            html: HTML content
            base_url: Base URL for resolving relative URLs
            
        Returns:
            List of feed URLs
        """
        feed_urls = []
        
        try:
            soup = BeautifulSoup(html, "html.parser")
            
            for link_tag in soup.find_all("link", rel=True):
                rel = link_tag.get("rel", [])
                if isinstance(rel, list):
                    rel_str = " ".join(rel).lower()
                else:
                    rel_str = str(rel).lower()
                
                if "alternate" in rel_str:
                    link_type = link_tag.get("type", "").lower()
                    href = link_tag.get("href", "")
                    
                    if href and ("rss" in link_type or "atom" in link_type or "xml" in link_type):
                        feed_url = urljoin(base_url, href)
                        feed_urls.append(feed_url)
            
            rss_pattern = r'<link[^>]*rel=["\']alternate["\'][^>]*type=["\']application/rss\+xml["\'][^>]*href=["\']([^"\']+)["\']'
            atom_pattern = r'<link[^>]*rel=["\']alternate["\'][^>]*type=["\']application/atom\+xml["\'][^>]*href=["\']([^"\']+)["\']'
            
            for pattern in [rss_pattern, atom_pattern]:
                matches = re.findall(pattern, html, re.IGNORECASE)
                for match in matches:
                    feed_url = urljoin(base_url, match)
                    if feed_url not in feed_urls:
                        feed_urls.append(feed_url)
        except (ValueError, RuntimeError, AttributeError, TypeError) as e:
            logger.debug("Error extracting feed links: %s", e)
        
        return feed_urls
    
    async def _parse_feed(self, feed_url: str, use_cache: bool = True) -> list[str]:
        """Parse RSS/Atom feed and extract article URLs.
        
        Uses caching to avoid redundant feed parsing.
        
        Args:
            feed_url: Feed URL to parse
            use_cache: Use cache if available (default: True)
            
        Returns:
            List of article URLs
        """
        if use_cache:
            cached_urls = url_cache.get("feed", None, feed_url=feed_url)
            if cached_urls:
                logger.debug("Using cached feed URLs for %s", feed_url)
                return cached_urls.get("web_urls", [])
        
        session = await self._get_session()
        urls = []
        
        try:
            timeout = aiohttp.ClientTimeout(total=15, connect=5)
            async with session.get(feed_url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"}) as response:
                if response.status != 200:
                    return []
                
                content = await response.text()
                
                if not content or len(content.strip()) < 50:
                    return []
                
                content_clean = self._clean_xml_content(content)
                
                try:
                    root = ET.fromstring(content_clean)
                    
                    if root.tag.endswith("rss") or root.tag.endswith("channel"):
                        for item in root.findall(".//item"):
                            link = item.find("link")
                            if link is not None and link.text:
                                url = link.text.strip()
                                if url.startswith(("http://", "https://")):
                                    urls.append(url)
                    
                    elif root.tag.endswith("feed"):
                        atom_ns = "{http://www.w3.org/2005/Atom}"
                        for entry in root.findall(f".//{atom_ns}entry"):
                            link = entry.find(f"{atom_ns}link")
                            if link is not None:
                                href = link.get("href")
                                if href:
                                    url = href.strip()
                                    if url.startswith(("http://", "https://")):
                                        urls.append(url)
                    
                    elif root.tag.endswith("RDF"):
                        rss_ns = "{http://purl.org/rss/1.0/}"
                        for item in root.findall(f".//{rss_ns}item"):
                            link = item.find(f"{rss_ns}link")
                            if link is not None and link.text:
                                url = link.text.strip()
                                if url.startswith(("http://", "https://")):
                                    urls.append(url)
                
                except ET.ParseError:
                    urls.extend(self._extract_feed_urls_regex(content, feed_url))
        
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logger.debug("HTTP error parsing feed %s: %s", feed_url, e)
        except (ValueError, RuntimeError, AttributeError, TypeError, ConnectionError) as e:
            logger.debug("Error parsing feed %s: %s", feed_url, e)
        
        unique_urls = list(set(urls))
        
        if use_cache and unique_urls:
            url_cache.set("feed", {"web_urls": unique_urls}, None, feed_url=feed_url, ttl_seconds=3600)
            logger.debug("Cached feed URLs for %s", feed_url)
        
        return unique_urls
    
    def _extract_feed_urls_regex(self, content: str, base_url: str) -> list[str]:
        """Extract URLs from feed using regex fallback.
        
        Args:
            content: Feed content
            base_url: Base URL for resolving relative URLs
            
        Returns:
            List of extracted URLs
        """
        urls = []
        
        url_patterns = [
            r"<link>(.*?)</link>",
            r'<link[^>]*>(.*?)</link>',
            r'<guid[^>]*>(.*?)</guid>',
            r'<id>(.*?)</id>',
            r'href=["\']([^"\']+)["\']',
        ]
        
        for pattern in url_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            for match in matches:
                url = match.strip()
                if url and (url.startswith(("http://", "https://")) or url.startswith("/")):
                    full_url = urljoin(base_url, url)
                    if full_url.startswith(("http://", "https://")):
                        if full_url not in urls:
                            urls.append(full_url)
        
        return urls

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
