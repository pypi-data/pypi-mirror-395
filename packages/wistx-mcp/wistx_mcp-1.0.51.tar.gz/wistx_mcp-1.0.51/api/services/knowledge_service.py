"""Knowledge research service - business logic for knowledge base operations."""

import logging
import time

from api.models.v1_requests import KnowledgeResearchRequest
from api.models.v1_responses import (
    KnowledgeArticleResponse,
    KnowledgeResearchResponse,
    KnowledgeResearchSummary,
)
from api.database.async_mongodb import async_mongodb_adapter
from wistx_mcp.tools.lib.vector_search import VectorSearch
from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.retry_utils import with_timeout_and_retry
from api.config import settings
from api.exceptions import ExternalServiceError

logger = logging.getLogger(__name__)


class KnowledgeService:
    """Service for knowledge base research operations."""

    def __init__(self):
        """Initialize knowledge service."""
        self.mongodb_adapter = async_mongodb_adapter
        mcp_mongodb_client = MongoDBClient()
        self.vector_search = VectorSearch(
            mcp_mongodb_client,
            gemini_api_key=settings.gemini_api_key,
            pinecone_api_key=settings.pinecone_api_key,
            pinecone_index_name=settings.pinecone_index_name,
        )

    async def research_knowledge_base(
        self,
        request: KnowledgeResearchRequest,
        user_id: str | None = None,
        organization_id: str | None = None,
    ) -> KnowledgeResearchResponse:
        """Research knowledge base across all domains.

        Args:
            request: Knowledge research request
            user_id: User ID for user-specific content filtering
            organization_id: Organization ID for org-shared content filtering

        Returns:
            Knowledge research response with articles and summary

        Raises:
            RuntimeError: If operation times out or fails
        """
        logger.info(
            "Researching knowledge base: query='%s', domains=%s, content_types=%s, max_results=%d, include_cross_domain=%s, include_global=%s, user_id=%s",
            request.query[:100] if len(request.query) > 100 else request.query,
            request.domains,
            request.content_types,
            request.max_results,
            request.include_cross_domain,
            request.include_global,
            user_id,
        )

        await self.mongodb_adapter.connect()

        search_start_time = time.time()
        
        from wistx_mcp.tools.lib.constants import TOOL_TIMEOUTS
        
        tool_timeout = TOOL_TIMEOUTS.get("wistx_research_knowledge_base", 90.0)
        
        knowledge_base_timeout = tool_timeout - 10.0
        
        if request.max_results > 1000:
            knowledge_base_timeout = min(tool_timeout - 5.0, 60.0 + (request.max_results / 1000) * 5.0)
        
        try:
            results = await with_timeout_and_retry(
                self.vector_search.search_knowledge_articles,
                timeout_seconds=knowledge_base_timeout,
                max_attempts=1,
                retryable_exceptions=(RuntimeError, ConnectionError, TimeoutError),
                query=request.query,
                domains=request.domains if request.domains else None,
                content_types=request.content_types if request.content_types else None,
                user_id=user_id,
                organization_id=organization_id,
                include_global=request.include_global,
                limit=min(request.max_results, 1000),
            )
        except (RuntimeError, ConnectionError, TimeoutError) as e:
            error_msg = str(e)
            if "timeout" in error_msg.lower():
                logger.error(
                    "Knowledge base search timed out after %.1f seconds: query='%s', max_results=%d",
                    knowledge_base_timeout,
                    request.query[:100],
                    request.max_results,
                )
                raise ExternalServiceError(
                    message=f"Knowledge base search timed out after {knowledge_base_timeout:.0f} seconds",
                    user_message=f"Knowledge base search timed out after {knowledge_base_timeout:.0f} seconds. This may occur with large result sets or slow network conditions. Try reducing max_results (current: {request.max_results}) or retry the query.",
                    error_code="KNOWLEDGE_SEARCH_TIMEOUT",
                    details={"timeout_seconds": knowledge_base_timeout, "max_results": request.max_results, "query": request.query[:100]}
                ) from e
            raise
        search_time_ms = int((time.time() - search_start_time) * 1000)

        if not results:
            logger.info(
                "No results found for query: '%s' (domains=%s, content_types=%s, user_id=%s)",
                request.query[:100],
                request.domains,
                request.content_types,
                user_id,
            )
            return KnowledgeResearchResponse(
                results=[],
                research_summary=KnowledgeResearchSummary(
                    total_found=0,
                    domains_covered=[],
                    key_insights=[],
                ),
                metadata={
                    "query_time_ms": search_time_ms,
                    "sources": [],
                },
            )

        if len(results) > request.max_results * 2:
            logger.warning(
                "Result set larger than expected: %d results (max: %d), truncating",
                len(results),
                request.max_results,
            )
            results = results[:request.max_results]

        articles = []
        domains_covered: set[str] = set()

        for result in results:
            domain = result.get("domain", "")
            domains_covered.add(domain)

            article = KnowledgeArticleResponse(
                article_id=result.get("article_id", ""),
                domain=domain,
                subdomain=result.get("subdomain", ""),
                content_type=result.get("content_type", ""),
                title=result.get("title", ""),
                summary=result.get("summary", ""),
                content=result.get("content") if request.format == "markdown" else None,
                tags=result.get("tags", []),
                categories=result.get("categories", []),
                industries=result.get("industries", []),
                cloud_providers=result.get("cloud_providers", []),
                services=result.get("services", []),
                cross_domain_impacts=result.get("compliance_impact") or result.get("cost_impact") or result.get("security_impact")
                if request.include_cross_domain
                else None,
                source_url=result.get("source_url"),
                quality_score=result.get("quality_score"),
            )
            articles.append(article)

        key_insights = []
        if articles:
            key_insights = [article.summary[:200] + "..." for article in articles[:3]]

        summary = KnowledgeResearchSummary(
            total_found=len(articles),
            domains_covered=sorted(domains_covered),
            key_insights=key_insights,
        )

        return KnowledgeResearchResponse(
            results=articles,
            research_summary=summary,
            metadata={
                "query_time_ms": search_time_ms,
                "sources": list(set(article.source_url for article in articles if article.source_url)),
            },
        )
