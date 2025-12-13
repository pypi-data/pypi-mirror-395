"""Unified code search tool - consolidates semantic search, regex search, and code examples.

This module merges three code search tools into one unified interface:
- search_codebase (semantic search on user's indexed repos)
- regex_search_codebase (pattern-based search on user's indexed repos)
- get_code_examples (search WISTX curated examples)

Usage:
    # Semantic search on YOUR indexed repos
    result = await wistx_search_code(search_mode="semantic", query="RDS encryption", ...)

    # Regex search on YOUR indexed repos
    result = await wistx_search_code(search_mode="regex", pattern="aws_db_instance", ...)

    # Search WISTX curated examples
    result = await wistx_search_code(search_mode="examples", query="RDS with encryption", ...)
"""

import logging
from typing import Any

from wistx_mcp.tools.lib.plan_enforcement import require_query_quota

logger = logging.getLogger(__name__)


@require_query_quota
async def wistx_search_code(
    # REQUIRED - determines which search mode
    search_mode: str,

    # COMMON PARAMETERS
    api_key: str | None = None,  # Optional - uses context or MCP initialization
    query: str | None = None,
    limit: int = 1000,
    cloud_provider: str | None = None,
    
    # FILTER PARAMETERS (semantic + regex modes - user's indexed repos)
    repositories: list[str] | None = None,
    resource_ids: list[str] | None = None,
    resource_types: list[str] | None = None,
    file_types: list[str] | None = None,
    code_type: str | None = None,
    
    # SEMANTIC-SPECIFIC (search_mode="semantic")
    include_sources: bool = True,
    include_ai_analysis: bool = True,
    analysis_mode: str | None = None,
    include_aggregated_summary: bool = False,
    check_freshness: bool = False,
    include_fresh_content: bool = False,
    max_stale_minutes: int = 60,
    
    # REGEX-SPECIFIC (search_mode="regex")
    pattern: str | None = None,
    template: str | None = None,
    case_sensitive: bool = False,
    multiline: bool = False,
    dotall: bool = False,
    include_context: bool = True,
    context_lines: int = 3,
    timeout: float = 30.0,
    
    # EXAMPLES-SPECIFIC (search_mode="examples")
    code_types: list[str] | None = None,
    services: list[str] | None = None,
    min_quality_score: int | None = None,
    compliance_standard: str | None = None,
) -> dict[str, Any]:
    """Unified code search across indexed repositories and curated examples.

    **Search Modes:**
    - "semantic": Natural language search on YOUR indexed repositories (requires query)
    - "regex": Pattern-based search on YOUR indexed repositories (requires pattern or template)
    - "examples": Search WISTX curated code examples (requires query)

    **Key Difference:**
    - "semantic" and "regex" search YOUR indexed repos (user-scoped)
    - "examples" searches WISTX's curated production-ready examples (global)

    Args:
        search_mode: Search type - "semantic", "regex", or "examples" (required)
        api_key: WISTX API key for authentication (required)
        query: Search query (required for semantic/examples, optional for regex)
        limit: Maximum number of results (default: 1000)
        cloud_provider: Filter by cloud provider (aws, gcp, azure)

        For semantic/regex modes (your indexed repos):
        - repositories: List of repositories to search (owner/repo format)
        - resource_ids: Filter by specific indexed resources
        - resource_types: Filter by type (repository, documentation, document)
        - file_types: Filter by file extensions (.tf, .yaml, .py, .md)
        - code_type: Filter by code type (terraform, kubernetes, docker)

        For semantic mode:
        - include_sources: Include source code snippets (default: True)
        - include_ai_analysis: Include AI analysis (default: True)
        - analysis_mode: "cost"|"compliance"|"infrastructure"|"security"|"all"
        - include_aggregated_summary: Include aggregated summary (default: False)
        - check_freshness: Check if content is stale (default: False)
        - include_fresh_content: Fetch fresh content for stale results (default: False)
        - max_stale_minutes: Stale threshold in minutes (default: 60)

        For regex mode:
        - pattern: Regex pattern to search (required if no template)
        - template: Pre-built pattern template (api_key, password, ip_address)
        - case_sensitive: Case-sensitive matching (default: False)
        - multiline: Multiline mode (default: False)
        - dotall: Dot matches newline (default: False)
        - include_context: Include surrounding context (default: True)
        - context_lines: Lines before/after match (default: 3)
        - timeout: Max search time in seconds (default: 30.0)

        For examples mode:
        - code_types: Filter by types (terraform, kubernetes, docker, pulumi)
        - services: Filter by services (rds, s3, ec2)
        - min_quality_score: Minimum quality score (0-100)
        - compliance_standard: Filter by standard (PCI-DSS, HIPAA)

    Returns:
        Dictionary with search results specific to the search mode

    Raises:
        ValueError: If invalid search_mode or missing required parameters
        TimeoutError: If regex search exceeds timeout
        RuntimeError: If search fails
    """
    valid_modes = ["semantic", "regex", "examples"]
    if search_mode not in valid_modes:
        raise ValueError(
            f"Invalid search_mode: {search_mode}. Must be one of: {', '.join(valid_modes)}"
        )
    
    logger.info(
        "Unified code search: mode=%s, query=%s, limit=%d",
        search_mode,
        query[:50] if query else pattern[:50] if pattern else template,
        limit,
    )
    
    if search_mode == "semantic":
        return await _handle_semantic_search(
            query=query,
            api_key=api_key,
            repositories=repositories,
            resource_ids=resource_ids,
            resource_types=resource_types,
            file_types=file_types,
            code_type=code_type,
            cloud_provider=cloud_provider,
            include_sources=include_sources,
            include_ai_analysis=include_ai_analysis,
            limit=limit,
            analysis_mode=analysis_mode,
            include_aggregated_summary=include_aggregated_summary,
            check_freshness=check_freshness,
            include_fresh_content=include_fresh_content,
            max_stale_minutes=max_stale_minutes,
        )

    elif search_mode == "regex":
        return await _handle_regex_search(
            pattern=pattern,
            api_key=api_key,
            repositories=repositories,
            resource_ids=resource_ids,
            resource_types=resource_types,
            file_types=file_types,
            code_type=code_type,
            cloud_provider=cloud_provider,
            template=template,
            case_sensitive=case_sensitive,
            multiline=multiline,
            dotall=dotall,
            include_context=include_context,
            context_lines=context_lines,
            limit=limit,
            timeout=timeout,
        )

    elif search_mode == "examples":
        return await _handle_examples_search(
            query=query,
            code_types=code_types,
            cloud_provider=cloud_provider,
            services=services,
            min_quality_score=min_quality_score,
            compliance_standard=compliance_standard,
            limit=limit,
        )


async def _handle_semantic_search(
    query: str | None,
    api_key: str,
    repositories: list[str] | None,
    resource_ids: list[str] | None,
    resource_types: list[str] | None,
    file_types: list[str] | None,
    code_type: str | None,
    cloud_provider: str | None,
    include_sources: bool,
    include_ai_analysis: bool,
    limit: int,
    analysis_mode: str | None,
    include_aggregated_summary: bool,
    check_freshness: bool,
    include_fresh_content: bool,
    max_stale_minutes: int,
) -> dict[str, Any]:
    """Handle semantic search mode - delegates to search_codebase."""
    if not query:
        raise ValueError("query is required for search_mode='semantic'")

    from wistx_mcp.tools.search_codebase import search_codebase

    return await search_codebase(
        query=query,
        api_key=api_key,
        repositories=repositories,
        resource_ids=resource_ids,
        resource_types=resource_types,
        file_types=file_types,
        code_type=code_type,
        cloud_provider=cloud_provider,
        include_sources=include_sources,
        include_ai_analysis=include_ai_analysis,
        limit=limit,
        analysis_mode=analysis_mode,
        include_aggregated_summary=include_aggregated_summary,
        check_freshness=check_freshness,
        include_fresh_content=include_fresh_content,
        max_stale_minutes=max_stale_minutes,
    )


async def _handle_regex_search(
    pattern: str | None,
    api_key: str,
    repositories: list[str] | None,
    resource_ids: list[str] | None,
    resource_types: list[str] | None,
    file_types: list[str] | None,
    code_type: str | None,
    cloud_provider: str | None,
    template: str | None,
    case_sensitive: bool,
    multiline: bool,
    dotall: bool,
    include_context: bool,
    context_lines: int,
    limit: int,
    timeout: float,
) -> dict[str, Any]:
    """Handle regex search mode - delegates to regex_search_codebase."""
    if not pattern and not template:
        raise ValueError("pattern or template is required for search_mode='regex'")

    from wistx_mcp.tools.regex_search import regex_search_codebase

    return await regex_search_codebase(
        pattern=pattern,
        api_key=api_key,
        repositories=repositories,
        resource_ids=resource_ids,
        resource_types=resource_types,
        file_types=file_types,
        code_type=code_type,
        cloud_provider=cloud_provider,
        template=template,
        case_sensitive=case_sensitive,
        multiline=multiline,
        dotall=dotall,
        include_context=include_context,
        context_lines=context_lines,
        limit=limit,
        timeout=timeout,
    )


async def _handle_examples_search(
    query: str | None,
    code_types: list[str] | None,
    cloud_provider: str | None,
    services: list[str] | None,
    min_quality_score: int | None,
    compliance_standard: str | None,
    limit: int,
) -> dict[str, Any]:
    """Handle examples search mode - delegates to get_code_examples."""
    if not query:
        raise ValueError("query is required for search_mode='examples'")

    from wistx_mcp.tools.code_examples import get_code_examples

    return await get_code_examples(
        query=query,
        code_types=code_types,
        cloud_provider=cloud_provider,
        services=services,
        min_quality_score=min_quality_score,
        compliance_standard=compliance_standard,
        limit=limit,
    )

