"""Service for storing web search results as knowledge articles."""

import asyncio
import hashlib
import logging
from datetime import datetime
from typing import Any
from urllib.parse import urlparse

from data_pipelines.models.knowledge_article import ContentType, Domain, KnowledgeArticle, Reference
from api.database.mongodb import mongodb_manager
from api.services.github_service import github_service

logger = logging.getLogger(__name__)


class WebSearchStorageService:
    """Service for converting and storing web search results as knowledge articles."""

    def __init__(self):
        """Initialize web search storage service."""
        pass

    def _generate_article_id_from_url(self, url: str) -> str:
        """Generate article ID from URL hash to ensure uniqueness.

        Args:
            url: Source URL

        Returns:
            Unique article ID
        """
        url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
        return f"web_search_{url_hash}"

    def _infer_domain_from_query_and_domains(
        self, query: str, domains_searched: list[str] | None
    ) -> Domain:
        """Infer knowledge domain from query and domains searched.

        Args:
            query: Search query
            domains_searched: List of domains that were searched

        Returns:
            Domain enum value
        """
        query_lower = query.lower()
        text = f"{query} {' '.join(domains_searched or [])}".lower()

        if any(d in text for d in ["compliance", "pci", "hipaa", "gdpr", "soc"]):
            return Domain.COMPLIANCE
        if any(d in text for d in ["finops", "cost", "budget", "pricing", "billing"]):
            return Domain.FINOPS
        if any(d in text for d in ["security", "vulnerability", "cve", "threat"]):
            return Domain.SECURITY
        if any(d in text for d in ["sre", "reliability", "slo", "sla", "monitoring"]):
            return Domain.SRE
        if any(d in text for d in ["platform", "kubernetes", "k8s", "container"]):
            return Domain.PLATFORM
        if any(d in text for d in ["automation", "ci/cd", "pipeline", "deployment"]):
            return Domain.AUTOMATION
        if any(d in text for d in ["architecture", "design", "pattern"]):
            return Domain.ARCHITECTURE
        if any(d in text for d in ["infrastructure", "terraform", "cloudformation"]):
            return Domain.INFRASTRUCTURE
        if any(d in text for d in ["devops", "deployment", "operations"]):
            return Domain.DEVOPS

        if domains_searched:
            domain_map = {
                "compliance": Domain.COMPLIANCE,
                "finops": Domain.FINOPS,
                "security": Domain.SECURITY,
                "sre": Domain.SRE,
                "platform": Domain.PLATFORM,
                "automation": Domain.AUTOMATION,
                "architecture": Domain.ARCHITECTURE,
                "infrastructure": Domain.INFRASTRUCTURE,
                "devops": Domain.DEVOPS,
            }
            for domain_str in domains_searched:
                if domain_str.lower() in domain_map:
                    return domain_map[domain_str.lower()]

        return Domain.DEVOPS

    def _infer_subdomain_from_url(self, url: str) -> str:
        """Infer subdomain from URL.

        Args:
            url: Source URL

        Returns:
            Subdomain string
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()

            if "github.com" in domain:
                return "github"
            if "docs.aws.amazon.com" in domain:
                return "aws-docs"
            if "cloud.google.com" in domain:
                return "gcp-docs"
            if "learn.microsoft.com" in domain:
                return "azure-docs"
            if "kubernetes.io" in domain:
                return "kubernetes"
            if "terraform.io" in domain:
                return "terraform"

            path_parts = [p for p in parsed.path.split("/") if p]
            if path_parts:
                return path_parts[0].lower()[:50]

            return "general"
        except Exception:
            return "general"

    def _extract_summary_from_content(self, content: str, max_length: int = 500) -> str:
        """Extract summary from content.

        Args:
            content: Article content
            max_length: Maximum summary length

        Returns:
            Summary string (minimum 50 characters)
        """
        if not content:
            return "Web search result - content extracted from web search"

        min_length = 50

        if len(content) <= max_length:
            summary = content
        else:
            sentences = content.split(".")[:3]
            summary = ". ".join(s.strip() for s in sentences if s.strip())
            if not summary:
                summary = content[:max_length]
            else:
                summary = summary[:max_length]

        if len(summary) < min_length:
            if len(content) >= min_length:
                summary = content[:min_length].rstrip() + "..."
            else:
                words = content.split()
                if words:
                    summary = " ".join(words)
                    if len(summary) < min_length:
                        summary = summary + " " + "Web search result content."
                else:
                    summary = "Web search result - content extracted from web search"

        return summary[:max_length]

    async def _check_existing_article(self, source_url: str) -> bool:
        """Check if article with source_url already exists.

        Args:
            source_url: Source URL to check

        Returns:
            True if article exists, False otherwise
        """
        try:
            db = mongodb_manager.get_database()
            collection = db.knowledge_articles

            existing = collection.find_one({"source_url": source_url}, {"_id": 1})
            return existing is not None
        except Exception as e:
            logger.warning("Error checking existing article for URL %s: %s", source_url[:100], e)
            return False

    def _convert_web_result_to_article(
        self,
        web_result: dict[str, Any],
        query: str,
        domains_searched: list[str] | None,
        tavily_score: float | None = None,
        published_date: str | None = None,
    ) -> KnowledgeArticle | None:
        """Convert web search result to KnowledgeArticle.

        Args:
            web_result: Web search result dictionary
            query: Original search query
            domains_searched: List of domains searched
            tavily_score: Relevance score from Tavily (0-1)
            published_date: Published date string

        Returns:
            KnowledgeArticle or None if conversion fails
        """
        try:
            url = web_result.get("url", "").strip()
            if not url:
                logger.warning("Web result missing URL, skipping")
                return None

            title = web_result.get("title", "").strip()
            if not title or len(title) < 5:
                title = f"Web Search Result: {url}"

            content = web_result.get("content", "").strip()
            if len(content) < 100:
                logger.debug("Web result content too short (%d chars), skipping", len(content))
                return None

            article_id = self._generate_article_id_from_url(url)
            domain = self._infer_domain_from_query_and_domains(query, domains_searched)
            subdomain = self._infer_subdomain_from_url(url)
            summary = self._extract_summary_from_content(content)

            quality_score = None
            if tavily_score is not None:
                quality_score = min(100.0, max(0.0, tavily_score * 100))

            freshness_score = None
            if published_date:
                try:
                    pub_date = datetime.fromisoformat(published_date.replace("Z", "+00:00"))
                    age_days = (datetime.utcnow() - pub_date.replace(tzinfo=None)).days
                    if age_days <= 30:
                        freshness_score = 100.0
                    elif age_days <= 90:
                        freshness_score = 80.0
                    elif age_days <= 180:
                        freshness_score = 60.0
                    else:
                        freshness_score = 40.0
                except Exception:
                    pass

            references = [Reference(type="source", url=url, title=title)]

            article = KnowledgeArticle(
                article_id=article_id,
                domain=domain,
                subdomain=subdomain,
                content_type=ContentType.GUIDE,
                title=title[:200],
                summary=summary,
                content=content,
                source_url=url,
                references=references,
                quality_score=quality_score,
                freshness_score=freshness_score,
                source_type="web_search",
                visibility="global",
            )

            return article
        except Exception as e:
            logger.error("Error converting web result to article: %s", e, exc_info=True)
            return None

    async def store_web_search_results(
        self,
        web_results: dict[str, Any],
        query: str,
        domains_searched: list[str] | None = None,
        store_in_background: bool = True,
    ) -> dict[str, Any]:
        """Store web search results as knowledge articles.

        Args:
            web_results: Web search results dictionary with 'results' list
            query: Original search query
            domains_searched: List of domains that were searched
            store_in_background: If True, store asynchronously without blocking

        Returns:
            Dictionary with storage statistics
        """
        stats = {
            "total_results": 0,
            "converted": 0,
            "stored": 0,
            "skipped_duplicate": 0,
            "skipped_invalid": 0,
            "errors": [],
        }

        results = web_results.get("results", [])
        if not results:
            logger.info("No web search results to store for query: %s", query[:100])
            return stats

        stats["total_results"] = len(results)

        if store_in_background:
            task = asyncio.create_task(
                self._store_web_results_background(results, query, domains_searched, stats)
            )
            logger.info(
                "Started background storage for %d web search results (query: %s)",
                len(results),
                query[:100],
            )
            return stats

        return await self._store_web_results_background(results, query, domains_searched, stats)

    async def _store_web_results_background(
        self,
        results: list[dict[str, Any]],
        query: str,
        domains_searched: list[str] | None,
        stats: dict[str, Any],
    ) -> dict[str, Any]:
        """Store web results in background.

        Args:
            results: List of web search results
            query: Original search query
            domains_searched: List of domains searched
            stats: Statistics dictionary to update

        Returns:
            Updated statistics dictionary
        """
        try:
            for result in results:
                try:
                    url = result.get("url", "").strip()
                    if not url:
                        stats["skipped_invalid"] += 1
                        continue

                    existing = await self._check_existing_article(url)
                    if existing:
                        stats["skipped_duplicate"] += 1
                        logger.debug("Skipping duplicate article: %s", url[:100])
                        continue

                    tavily_score = result.get("score")
                    published_date = result.get("published_date")

                    article = self._convert_web_result_to_article(
                        result,
                        query,
                        domains_searched,
                        tavily_score=tavily_score,
                        published_date=published_date,
                    )

                    if not article:
                        stats["skipped_invalid"] += 1
                        continue

                    stats["converted"] += 1

                    await github_service._store_article(article)
                    stats["stored"] += 1

                    logger.info(
                        "Stored web search result as article: %s (ID: %s)",
                        url[:100],
                        article.article_id,
                    )
                except Exception as e:
                    error_msg = str(e)
                    stats["errors"].append({"url": result.get("url", ""), "error": error_msg})
                    logger.error("Error storing web result: %s", e, exc_info=True)

            logger.info(
                "Completed storing web search results: %d stored, %d duplicates, %d invalid, %d errors",
                stats["stored"],
                stats["skipped_duplicate"],
                stats["skipped_invalid"],
                len(stats["errors"]),
            )
        except Exception as e:
            logger.error("Error in background web result storage: %s", e, exc_info=True)
            stats["errors"].append({"stage": "background_storage", "error": str(e)})

        return stats


web_search_storage_service = WebSearchStorageService()

