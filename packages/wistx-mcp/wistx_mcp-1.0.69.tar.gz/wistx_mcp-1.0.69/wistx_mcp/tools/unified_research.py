"""Unified research tool - knowledge base and web search.

This module merges research capabilities into one unified interface:
- research_knowledge_base (deep research across domains)
- web_search (general and security web search)

Usage:
    # Research knowledge base with optional web search
    result = await wistx_research(source="knowledge_base", query="terraform vpc best practices", ...)

    # General web search
    result = await wistx_research(source="web", query="latest kubernetes security advisories", ...)

    # Security-focused search (CVEs, advisories)
    result = await wistx_research(source="security", query="CVE-2024 terraform", ...)

    # Combined search (all sources)
    result = await wistx_research(source="all", query="aws rds encryption", ...)
"""

import logging
from typing import Any

from wistx_mcp.tools.lib.plan_enforcement import require_query_quota

logger = logging.getLogger(__name__)

# Valid sources
VALID_SOURCES = ["knowledge_base", "web", "security", "all"]


@require_query_quota
async def wistx_research(
    # REQUIRED
    source: str,
    query: str,

    # API KEY (optional - uses context or MCP initialization)
    api_key: str | None = None,

    # === KNOWLEDGE BASE (source="knowledge_base", "all") ===
    domains: list[str] | None = None,
    content_types: list[str] | None = None,
    include_cross_domain: bool = True,
    include_web_search: bool = True,
    format: str = "structured",
    research_url: str | None = None,
    enable_deep_research: bool = False,

    # === WEB SEARCH (source="web", "security", "all") ===
    search_type: str = "general",
    resource_type: str | None = None,
    cloud_provider: str | None = None,
    severity: str | None = None,
    include_cves: bool = True,
    include_advisories: bool = True,

    # === COMMON ===
    max_results: int = 1000,
) -> dict[str, Any]:
    """Unified research across knowledge base and web.

    **Sources:**

    - "knowledge_base": Search internal knowledge base with optional web enrichment
    - "web": General web search for DevOps/infrastructure topics
    - "security": Security-focused search (CVEs, advisories)
    - "all": Combined search across all sources

    Args:
        source: Research source (required)
        query: Search query (required)
        api_key: WISTX API key for authentication (required)

        For knowledge_base:
        - domains: Filter by domains (compliance, finops, devops, infrastructure, security)
        - content_types: Filter by types (guide, pattern, strategy)
        - include_cross_domain: Include cross-domain relationships (default: True)
        - include_web_search: Include web search enrichment (default: True)
        - format: Response format (structured, markdown, executive_summary)
        - research_url: URL to research directly (fetches, chunks, indexes)
        - enable_deep_research: Enable on-demand contextual retrieval

        For web/security:
        - search_type: Type of search (general, security) - auto-set for source="security"
        - resource_type: Filter by resource (RDS, S3, EKS, etc.)
        - cloud_provider: Filter by cloud (aws, gcp, azure)
        - severity: Filter by severity (security searches)
        - include_cves: Include CVE database (default: True)
        - include_advisories: Include security advisories (default: True)

        Common:
        - max_results: Maximum results (default: 1000)

    Returns:
        Dictionary with results specific to the source:
        - For knowledge_base: {results, web_results, research_summary}
        - For web: {web, total}
        - For security: {web, security, total}
        - For all: Combined results from all sources

    Raises:
        ValueError: If invalid source or missing required parameters
        RuntimeError: If search fails
    """
    if source not in VALID_SOURCES:
        raise ValueError(
            f"Invalid source: {source}. "
            f"Valid sources: {', '.join(VALID_SOURCES)}"
        )

    if not query or len(query.strip()) < 3:
        raise ValueError("query must be at least 3 characters")

    logger.info("Unified research: source=%s, query=%s...", source, query[:50])

    # Route to appropriate handler(s)
    if source == "knowledge_base":
        return await _handle_knowledge_base(
            query=query,
            api_key=api_key,
            domains=domains,
            content_types=content_types,
            include_cross_domain=include_cross_domain,
            include_web_search=include_web_search,
            format=format,
            max_results=max_results,
            research_url=research_url,
            enable_deep_research=enable_deep_research,
        )

    elif source == "web":
        return await _handle_web_search(
            query=query,
            api_key=api_key,
            search_type="general",
            resource_type=resource_type,
            cloud_provider=cloud_provider,
            severity=severity,
            include_cves=include_cves,
            include_advisories=include_advisories,
            limit=max_results,
        )

    elif source == "security":
        return await _handle_web_search(
            query=query,
            api_key=api_key,
            search_type="security",
            resource_type=resource_type,
            cloud_provider=cloud_provider,
            severity=severity,
            include_cves=include_cves,
            include_advisories=include_advisories,
            limit=max_results,
        )

    elif source == "all":
        return await _handle_all_sources(
            query=query,
            api_key=api_key,
            domains=domains,
            content_types=content_types,
            include_cross_domain=include_cross_domain,
            format=format,
            max_results=max_results,
            resource_type=resource_type,
            cloud_provider=cloud_provider,
            severity=severity,
            include_cves=include_cves,
            include_advisories=include_advisories,
            research_url=research_url,
            enable_deep_research=enable_deep_research,
        )


async def _handle_knowledge_base(
    query: str,
    api_key: str,
    domains: list[str] | None,
    content_types: list[str] | None,
    include_cross_domain: bool,
    include_web_search: bool,
    format: str,
    max_results: int,
    research_url: str | None,
    enable_deep_research: bool,
) -> dict[str, Any]:
    """Handle knowledge_base source - delegates to research_knowledge_base."""
    from wistx_mcp.tools.mcp_tools import research_knowledge_base

    return await research_knowledge_base(
        query=query,
        domains=domains,
        content_types=content_types,
        include_cross_domain=include_cross_domain,
        include_web_search=include_web_search,
        format=format,
        max_results=max_results,
        api_key=api_key,
        research_url=research_url,
        enable_deep_research=enable_deep_research,
    )


async def _handle_web_search(
    query: str,
    api_key: str,
    search_type: str,
    resource_type: str | None,
    cloud_provider: str | None,
    severity: str | None,
    include_cves: bool,
    include_advisories: bool,
    limit: int,
) -> dict[str, Any]:
    """Handle web/security source - delegates to web_search."""
    from wistx_mcp.tools.web_search import web_search

    return await web_search(
        query=query,
        search_type=search_type,
        resource_type=resource_type,
        cloud_provider=cloud_provider,
        severity=severity,
        include_cves=include_cves,
        include_advisories=include_advisories,
        limit=limit,
        api_key=api_key,
    )


async def _handle_all_sources(
    query: str,
    api_key: str,
    domains: list[str] | None,
    content_types: list[str] | None,
    include_cross_domain: bool,
    format: str,
    max_results: int,
    resource_type: str | None,
    cloud_provider: str | None,
    severity: str | None,
    include_cves: bool,
    include_advisories: bool,
    research_url: str | None,
    enable_deep_research: bool,
) -> dict[str, Any]:
    """Handle all sources - combines knowledge base and web search."""
    import asyncio

    # Run both searches in parallel
    kb_task = _handle_knowledge_base(
        query=query,
        api_key=api_key,
        domains=domains,
        content_types=content_types,
        include_cross_domain=include_cross_domain,
        include_web_search=False,  # Don't double-search web
        format=format,
        max_results=max_results,
        research_url=research_url,
        enable_deep_research=enable_deep_research,
    )

    web_task = _handle_web_search(
        query=query,
        api_key=api_key,
        search_type="general",
        resource_type=resource_type,
        cloud_provider=cloud_provider,
        severity=severity,
        include_cves=include_cves,
        include_advisories=include_advisories,
        limit=max_results,
    )

    # Gather results
    kb_result, web_result = await asyncio.gather(
        kb_task,
        web_task,
        return_exceptions=True,
    )

    combined: dict[str, Any] = {
        "source": "all",
        "query": query,
        "knowledge_base": {},
        "web": {},
        "security": [],
    }

    if isinstance(kb_result, Exception):
        logger.warning("Knowledge base search failed: %s", kb_result)
        combined["knowledge_base"] = {"error": str(kb_result)}
    else:
        combined["knowledge_base"] = kb_result

    if isinstance(web_result, Exception):
        logger.warning("Web search failed: %s", web_result)
        combined["web"] = {"error": str(web_result)}
    else:
        combined["web"] = web_result.get("web", [])
        combined["security"] = web_result.get("security", [])

    return combined
