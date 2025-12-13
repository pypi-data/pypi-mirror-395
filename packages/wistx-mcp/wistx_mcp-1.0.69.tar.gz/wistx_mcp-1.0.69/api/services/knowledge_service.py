"""Knowledge research service - business logic for knowledge base operations.

Implements hybrid retrieval with:
1. Query routing - routes to user KB, global KB, or both
2. Hybrid search - semantic + BM25 with RRF fusion
3. Reranking - LLM-based reranking for precision
4. Caching - query embedding and result caching
"""

import logging
import time
from typing import Any

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

# Hybrid retrieval imports
from api.services.query_router_service import QueryRouterService, QueryTarget
from api.services.hybrid_retrieval_service import HybridRetrievalService, RetrievalResult
from api.services.reranker_service import RerankerService
from api.services.retrieval_cache_service import RetrievalCacheService

logger = logging.getLogger(__name__)


class KnowledgeService:
    """Service for knowledge base research operations.

    Implements intelligent hybrid retrieval:
    - Routes queries to user KB, global KB, or both based on intent
    - Uses semantic + BM25 hybrid search for user KB
    - Applies LLM reranking for improved precision
    - Caches embeddings and hot queries
    """

    def __init__(self):
        """Initialize knowledge service with hybrid retrieval components."""
        self.mongodb_adapter = async_mongodb_adapter
        mcp_mongodb_client = MongoDBClient()
        self.vector_search = VectorSearch(
            mcp_mongodb_client,
            gemini_api_key=settings.gemini_api_key,
            pinecone_api_key=settings.pinecone_api_key,
            pinecone_index_name=settings.pinecone_index_name,
        )

        # Initialize hybrid retrieval components
        self.query_router = QueryRouterService()
        self.hybrid_retrieval = HybridRetrievalService()
        self.reranker = RerankerService()
        self.cache = RetrievalCacheService()

    async def research_knowledge_base(
        self,
        request: KnowledgeResearchRequest,
        user_id: str | None = None,
        organization_id: str | None = None,
        enable_hybrid: bool = True,
        enable_reranking: bool = True,
    ) -> KnowledgeResearchResponse:
        """Research knowledge base across all domains with hybrid retrieval.

        Uses intelligent query routing to search:
        - User's personal KB (on-demand researched content)
        - Global KB (pre-indexed content)
        - Or both, merged with RRF

        Args:
            request: Knowledge research request
            user_id: User ID for user-specific content filtering
            organization_id: Organization ID for org-shared content filtering
            enable_hybrid: Enable hybrid search (semantic + BM25) for user KB
            enable_reranking: Enable LLM reranking for improved precision

        Returns:
            Knowledge research response with articles and summary

        Raises:
            RuntimeError: If operation times out or fails
        """
        logger.info(
            "Researching knowledge base: query='%s', domains=%s, content_types=%s, max_results=%d, include_cross_domain=%s, include_global=%s, user_id=%s, hybrid=%s, rerank=%s",
            request.query[:100] if len(request.query) > 100 else request.query,
            request.domains,
            request.content_types,
            request.max_results,
            request.include_cross_domain,
            request.include_global,
            user_id,
            enable_hybrid,
            enable_reranking,
        )

        await self.mongodb_adapter.connect()

        search_start_time = time.time()

        from wistx_mcp.tools.lib.constants import TOOL_TIMEOUTS

        tool_timeout = TOOL_TIMEOUTS.get("wistx_research_knowledge_base", 90.0)
        knowledge_base_timeout = tool_timeout - 10.0

        if request.max_results > 1000:
            knowledge_base_timeout = min(tool_timeout - 5.0, 60.0 + (request.max_results / 1000) * 5.0)

        # Determine routing strategy
        routing_decision = None
        user_kb_results: list[RetrievalResult] = []
        global_results: list[dict[str, Any]] = []

        if user_id and enable_hybrid:
            # Get user KB info for routing
            user_kb_info = await self.query_router.get_user_kb_info(user_id)

            routing_decision = self.query_router.route_query(
                query=request.query,
                user_has_kb=user_kb_info.get("has_content", False),
                user_kb_technologies=user_kb_info.get("technologies", []),
            )

            logger.info(
                "Query routing: target=%s, confidence=%.2f, reason='%s'",
                routing_decision.target.value,
                routing_decision.confidence,
                routing_decision.reasoning,
            )

            # Search user KB if routed there
            if routing_decision.target in (
                QueryTarget.USER_ONLY,
                QueryTarget.USER_FIRST,
                QueryTarget.BOTH_PARALLEL,
            ):
                user_kb_results = await self._search_user_kb(
                    query=request.query,
                    user_id=user_id,
                    max_results=request.max_results,
                    enable_reranking=enable_reranking,
                )

        # Search global KB based on routing
        should_search_global = (
            not routing_decision or
            routing_decision.target in (
                QueryTarget.GLOBAL_ONLY,
                QueryTarget.GLOBAL_FIRST,
                QueryTarget.BOTH_PARALLEL,
            ) or
            request.include_global
        )

        if should_search_global:
            global_results = await self._search_global_kb(
                request=request,
                user_id=user_id,
                organization_id=organization_id,
                timeout=knowledge_base_timeout,
            )

        # Merge results
        results = self._merge_results(user_kb_results, global_results, request.max_results)

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

        # Add routing info to metadata
        routing_info = None
        if routing_decision:
            routing_info = {
                "target": routing_decision.target.value,
                "confidence": routing_decision.confidence,
                "reasoning": routing_decision.reasoning,
                "detected_technologies": routing_decision.detected_technologies,
            }

        return KnowledgeResearchResponse(
            results=articles,
            research_summary=summary,
            metadata={
                "query_time_ms": search_time_ms,
                "sources": list(set(article.source_url for article in articles if article.source_url)),
                "routing": routing_info,
                "user_kb_results": len(user_kb_results),
                "global_results": len(global_results),
            },
        )

    async def _search_user_kb(
        self,
        query: str,
        user_id: str,
        max_results: int,
        enable_reranking: bool = True,
    ) -> list[RetrievalResult]:
        """Search user's personal knowledge base with hybrid retrieval.

        Args:
            query: Search query
            user_id: User ID
            max_results: Maximum results
            enable_reranking: Enable LLM reranking

        Returns:
            List of retrieval results
        """
        try:
            # Hybrid search (semantic + BM25)
            hybrid_result = await self.hybrid_retrieval.search(
                query=query,
                user_id=user_id,
                top_k=max_results * 2,  # Fetch more for reranking
            )

            if not hybrid_result.results:
                return []

            results = hybrid_result.results

            # Apply reranking if enabled
            if enable_reranking and len(results) > 1:
                ranked_results = await self.reranker.rerank_with_fallback(
                    query=query,
                    results=results,
                    top_k=max_results,
                    timeout_seconds=15.0,
                )
                results = [r.result for r in ranked_results]

            logger.info(
                "User KB search: %d semantic, %d BM25, %d final results",
                hybrid_result.total_semantic,
                hybrid_result.total_bm25,
                len(results),
            )

            return results[:max_results]
        except Exception as e:
            logger.error("User KB search failed: %s", e, exc_info=True)
            return []

    async def _search_global_kb(
        self,
        request: KnowledgeResearchRequest,
        user_id: str | None,
        organization_id: str | None,
        timeout: float,
    ) -> list[dict[str, Any]]:
        """Search global knowledge base (existing vector search).

        Args:
            request: Knowledge research request
            user_id: User ID
            organization_id: Organization ID
            timeout: Search timeout

        Returns:
            List of result dictionaries
        """
        try:
            results = await with_timeout_and_retry(
                self.vector_search.search_knowledge_articles,
                timeout_seconds=timeout,
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
            return results or []
        except (RuntimeError, ConnectionError, TimeoutError) as e:
            error_msg = str(e)
            if "timeout" in error_msg.lower():
                logger.error(
                    "Global KB search timed out after %.1f seconds",
                    timeout,
                )
                raise ExternalServiceError(
                    message=f"Knowledge base search timed out after {timeout:.0f} seconds",
                    user_message=f"Knowledge base search timed out. Try reducing max_results or retry the query.",
                    error_code="KNOWLEDGE_SEARCH_TIMEOUT",
                    details={"timeout_seconds": timeout, "max_results": request.max_results}
                ) from e
            raise

    def _merge_results(
        self,
        user_results: list[RetrievalResult],
        global_results: list[dict[str, Any]],
        max_results: int,
    ) -> list[dict[str, Any]]:
        """Merge user KB and global KB results.

        Uses interleaving strategy:
        - If both have results, interleave with user results first
        - Deduplicate by source URL

        Args:
            user_results: Results from user KB
            global_results: Results from global KB
            max_results: Maximum total results

        Returns:
            Merged result list
        """
        # Convert user results to dict format
        user_dicts = []
        for r in user_results:
            user_dicts.append({
                "article_id": r.chunk_id,
                "title": r.document_title,
                "summary": r.content[:200] if r.content else "",
                "content": r.content,
                "source_url": r.source_url,
                "domain": "user_research",
                "subdomain": r.section_title or "",
                "content_type": "documentation",
                "tags": [],
                "categories": [],
                "industries": [],
                "cloud_providers": [],
                "services": [],
                "quality_score": r.rrf_score,
                "_source": "user_kb",
            })

        # Track seen URLs for deduplication
        seen_urls: set[str] = set()
        merged: list[dict[str, Any]] = []

        # Interleave results, preferring user KB
        user_idx = 0
        global_idx = 0

        while len(merged) < max_results:
            # Add user result
            if user_idx < len(user_dicts):
                result = user_dicts[user_idx]
                url = result.get("source_url", "")
                if url not in seen_urls:
                    merged.append(result)
                    if url:
                        seen_urls.add(url)
                user_idx += 1

            # Add global result
            if global_idx < len(global_results):
                result = global_results[global_idx]
                url = result.get("source_url", "")
                if url not in seen_urls:
                    result["_source"] = "global_kb"
                    merged.append(result)
                    if url:
                        seen_urls.add(url)
                global_idx += 1

            # Break if no more results
            if user_idx >= len(user_dicts) and global_idx >= len(global_results):
                break

        return merged[:max_results]
