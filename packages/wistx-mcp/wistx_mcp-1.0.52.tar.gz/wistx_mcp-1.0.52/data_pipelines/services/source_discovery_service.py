"""Source Discovery Service for on-demand knowledge research.

Multi-strategy source discovery that finds authoritative documentation
based on user intent analysis. Supports:
1. Official docs registry lookup
2. Web search for additional sources
3. GitHub repository discovery

Focused on WISTX domains: DevOps, Infrastructure, Compliance, FinOps, Platform Engineering.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any

from ..config.official_docs_registry import (
    get_doc_source,
    get_docs_url,
    OFFICIAL_DOCS_REGISTRY,
)
from .intent_analysis_service import IntentAnalysisResult

logger = logging.getLogger(__name__)


@dataclass
class DiscoveredSource:
    """A discovered documentation source."""
    url: str
    title: str
    source_type: str  # "official_docs", "web_search", "github"
    technology: str | None = None
    priority: int = 1  # 1 = highest
    confidence: float = 1.0
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "url": self.url,
            "title": self.title,
            "source_type": self.source_type,
            "technology": self.technology,
            "priority": self.priority,
            "confidence": self.confidence,
        }


@dataclass
class DiscoveryResult:
    """Result of source discovery."""
    sources: list[DiscoveredSource] = field(default_factory=list)
    technologies_found: list[str] = field(default_factory=list)
    search_queries_used: list[str] = field(default_factory=list)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "sources": [s.to_dict() for s in self.sources],
            "technologies_found": self.technologies_found,
            "search_queries_used": self.search_queries_used,
            "total_sources": len(self.sources),
        }
    
    def get_urls(self) -> list[str]:
        """Get all discovered URLs sorted by priority."""
        sorted_sources = sorted(self.sources, key=lambda s: (s.priority, -s.confidence))
        return [s.url for s in sorted_sources]


class SourceDiscoveryService:
    """Service for discovering documentation sources based on user intent."""
    
    def __init__(self, web_search_client: Any | None = None):
        """Initialize source discovery service.
        
        Args:
            web_search_client: Optional web search client for additional discovery
        """
        self.web_search_client = web_search_client
        self._github_base_url = "https://github.com"
    
    async def discover_sources(
        self,
        intent: IntentAnalysisResult,
        max_sources_per_tech: int = 3,
        include_web_search: bool = True,
        include_github: bool = True,
    ) -> DiscoveryResult:
        """Discover documentation sources based on analyzed intent.
        
        Args:
            intent: Result from IntentAnalysisService
            max_sources_per_tech: Maximum sources to return per technology
            include_web_search: Whether to include web search results
            include_github: Whether to include GitHub repositories
            
        Returns:
            DiscoveryResult with discovered sources
        """
        result = DiscoveryResult()
        result.technologies_found = list(intent.technologies)
        
        # Strategy 1: Official docs registry lookup
        for tech in intent.technologies:
            official_sources = self._discover_from_registry(tech)
            result.sources.extend(official_sources[:max_sources_per_tech])
        
        # Strategy 2: Web search for additional sources
        if include_web_search and self.web_search_client and intent.research_queries:
            web_sources = await self._discover_from_web_search(
                intent.research_queries[:5],  # Limit queries
                intent.technologies,
            )
            result.sources.extend(web_sources)
            result.search_queries_used.extend(intent.research_queries[:5])
        
        # Strategy 3: GitHub repository discovery
        if include_github:
            github_sources = self._discover_from_github(intent.technologies)
            result.sources.extend(github_sources)
        
        # Deduplicate by URL
        seen_urls = set()
        unique_sources = []
        for source in result.sources:
            if source.url not in seen_urls:
                seen_urls.add(source.url)
                unique_sources.append(source)
        result.sources = unique_sources
        
        logger.info(
            "Discovered %d sources for %d technologies",
            len(result.sources),
            len(intent.technologies),
        )
        
        return result
    
    def _discover_from_registry(self, technology: str) -> list[DiscoveredSource]:
        """Discover sources from official docs registry."""
        sources = []
        doc_source = get_doc_source(technology)
        
        if doc_source:
            # Main documentation URL
            docs_url = get_docs_url(technology)
            if docs_url:
                sources.append(DiscoveredSource(
                    url=docs_url,
                    title=f"{technology.title()} Documentation",
                    source_type="official_docs",
                    technology=technology,
                    priority=1,
                    confidence=1.0,
                ))
            
            # API reference if available
            if doc_source.get("api_path"):
                api_url = f"https://{doc_source['base_url']}{doc_source['api_path']}"
                sources.append(DiscoveredSource(
                    url=api_url,
                    title=f"{technology.title()} API Reference",
                    source_type="official_docs",
                    technology=technology,
                    priority=2,
                    confidence=1.0,
                ))

        return sources

    def _discover_from_github(self, technologies: list[str]) -> list[DiscoveredSource]:
        """Discover GitHub repositories for technologies."""
        sources = []

        for tech in technologies:
            doc_source = get_doc_source(tech)
            if doc_source and doc_source.get("github_repo"):
                repo = doc_source["github_repo"]
                sources.append(DiscoveredSource(
                    url=f"{self._github_base_url}/{repo}",
                    title=f"{tech.title()} GitHub Repository",
                    source_type="github",
                    technology=tech,
                    priority=3,
                    confidence=1.0,
                ))
                # Also add the README as a direct source
                sources.append(DiscoveredSource(
                    url=f"{self._github_base_url}/{repo}#readme",
                    title=f"{tech.title()} README",
                    source_type="github",
                    technology=tech,
                    priority=3,
                    confidence=0.9,
                ))

        return sources

    async def _discover_from_web_search(
        self,
        queries: list[str],
        technologies: list[str],
    ) -> list[DiscoveredSource]:
        """Discover sources from web search.

        Args:
            queries: Search queries to execute
            technologies: Technologies to match results against

        Returns:
            List of discovered sources from web search
        """
        if not self.web_search_client:
            return []

        sources = []
        tech_set = {t.lower() for t in technologies}

        for query in queries:
            try:
                results = await self.web_search_client.search(query, num_results=5)

                for result in results:
                    url = result.get("url", "")
                    title = result.get("title", "")

                    # Skip non-documentation URLs
                    if not self._is_documentation_url(url):
                        continue

                    # Determine which technology this relates to
                    matched_tech = None
                    for tech in tech_set:
                        if tech in url.lower() or tech in title.lower():
                            matched_tech = tech
                            break

                    sources.append(DiscoveredSource(
                        url=url,
                        title=title,
                        source_type="web_search",
                        technology=matched_tech,
                        priority=4,  # Lower priority than official docs
                        confidence=0.7,
                    ))
            except Exception as e:
                logger.warning("Web search failed for query '%s': %s", query, e)

        return sources

    def _is_documentation_url(self, url: str) -> bool:
        """Check if URL appears to be documentation.

        Args:
            url: URL to check

        Returns:
            True if URL appears to be documentation
        """
        url_lower = url.lower()

        # Positive indicators
        doc_indicators = [
            "/docs", "/documentation", "/guide", "/tutorial",
            "/reference", "/api", "/manual", "/learn",
            "docs.", "developer.", "learn.",
        ]

        # Negative indicators (not documentation)
        non_doc_indicators = [
            "/blog", "/news", "/pricing", "/about",
            "/contact", "/careers", "/jobs", "/login",
            "twitter.com", "facebook.com", "linkedin.com",
            "youtube.com", "reddit.com",
        ]

        # Check negative first
        for indicator in non_doc_indicators:
            if indicator in url_lower:
                return False

        # Check positive
        for indicator in doc_indicators:
            if indicator in url_lower:
                return True

        # Check if it's from a known official docs domain
        for tech, source in OFFICIAL_DOCS_REGISTRY.items():
            if source["base_url"] in url_lower:
                return True

        return False

    async def discover_for_url(self, url: str) -> DiscoveryResult:
        """Discover related sources for a given URL.

        When user provides a URL, find related documentation.

        Args:
            url: User-provided URL

        Returns:
            DiscoveryResult with the provided URL and related sources
        """
        result = DiscoveryResult()

        # Add the user-provided URL as primary source
        result.sources.append(DiscoveredSource(
            url=url,
            title="User-provided source",
            source_type="user_provided",
            priority=0,  # Highest priority
            confidence=1.0,
        ))

        # Try to identify technology from URL
        url_lower = url.lower()
        for tech in OFFICIAL_DOCS_REGISTRY.keys():
            if tech.replace(" ", "-") in url_lower or tech.replace(" ", "") in url_lower:
                result.technologies_found.append(tech)
                # Add official docs for this technology
                official_sources = self._discover_from_registry(tech)
                for source in official_sources:
                    if source.url != url:  # Don't duplicate user URL
                        result.sources.append(source)

        return result

