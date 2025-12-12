"""Intelligent context management tools for multi-resource context storage."""

import logging
from typing import Any

from wistx_mcp.tools.lib.api_client import WISTXAPIClient
from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id
from wistx_mcp.tools.lib.plan_enforcement import require_query_quota

logger = logging.getLogger(__name__)

api_client = WISTXAPIClient()


@require_query_quota
async def wistx_save_context_with_analysis(
    context_type: str,
    title: str,
    summary: str,
    api_key: str,
    description: str | None = None,
    conversation_history: list[dict[str, Any]] | None = None,
    code_snippets: list[dict[str, Any]] | None = None,
    plans: list[dict[str, Any]] | None = None,
    decisions: list[dict[str, Any]] | None = None,
    infrastructure_resources: list[dict[str, Any]] | None = None,
    linked_resources: list[str] | None = None,
    tags: list[str] | None = None,
    workspace: str | None = None,
    auto_analyze: bool = True,
) -> dict[str, Any]:
    """Save context with automatic infrastructure analysis (compliance, costs, security).

    Args:
        context_type: Type of context ('conversation', 'architecture_design', 'code_review', etc.)
        title: Context title
        summary: Context summary
        api_key: WISTX API key for authentication
        description: Detailed description
        conversation_history: Conversation history
        code_snippets: Code snippets referenced
        plans: Plans or workflows
        decisions: Decisions made
        infrastructure_resources: Infrastructure resources referenced (list of dicts with resource_id, path, type, etc.)
        linked_resources: Linked resource IDs
        tags: Tags for categorization
        workspace: Workspace identifier
        auto_analyze: Automatically analyze infrastructure, compliance, costs, security

    Returns:
        Dictionary with saved context and analysis:
        {
            "context_id": "ctx_abc123",
            "title": "...",
            "summary": "...",
            "analysis": {
                "compliance": {...},
                "costs": {...},
                "security": {...},
                "infrastructure": {...}
            }
        }
    """
    user_id = await validate_api_key_and_get_user_id(api_key)
    if not user_id:
        raise ValueError("Authentication required - api_key is invalid")

    valid_types = [
        "conversation",
        "architecture_design",
        "code_review",
        "troubleshooting",
        "documentation",
        "compliance_audit",
        "cost_analysis",
        "security_scan",
        "infrastructure_change",
        "custom",
    ]
    if context_type not in valid_types:
        raise ValueError(
            f"Invalid context_type: {context_type}. "
            f"Must be one of: {', '.join(valid_types)}"
        )

    try:
        response = await api_client.save_context_with_analysis(
            context_type=context_type,
            title=title,
            summary=summary,
            description=description,
            conversation_history=conversation_history,
            code_snippets=code_snippets,
            plans=plans,
            decisions=decisions,
            infrastructure_resources=infrastructure_resources,
            linked_resources=linked_resources,
            tags=tags,
            workspace=workspace,
            auto_analyze=auto_analyze,
            api_key=api_key,
        )

        return response.get("data") or response

    except Exception as e:
        logger.error("Error in wistx_save_context_with_analysis: %s", e, exc_info=True)
        raise


@require_query_quota
async def wistx_search_contexts_intelligently(
    query: str,
    api_key: str,
    context_type: str | None = None,
    compliance_standard: str | None = None,
    cost_range: dict[str, float] | None = None,
    security_score_min: float | None = None,
    limit: int = 50,
) -> dict[str, Any]:
    """Intelligent context search with infrastructure awareness.

    Searches across conversation content, infrastructure resources, compliance standards,
    cost implications, and security issues.

    Args:
        query: Search query
        api_key: WISTX API key for authentication
        context_type: Filter by context type
        compliance_standard: Filter by compliance standard (PCI-DSS, HIPAA, etc.)
        cost_range: Filter by cost range ({"min": 0.0, "max": 1000.0})
        security_score_min: Minimum security score (0-100)
        limit: Maximum number of results

    Returns:
        Dictionary with search results:
        {
            "query": "...",
            "results": [
                {
                    "context_id": "ctx_abc123",
                    "title": "...",
                    "summary": "...",
                    "analysis": {...}
                }
            ],
            "total": 10
        }
    """
    user_id = await validate_api_key_and_get_user_id(api_key)
    if not user_id:
        raise ValueError("Authentication required - api_key is invalid")

    if not query or len(query) < 3:
        raise ValueError("Query must be at least 3 characters")

    if limit < 1 or limit > 500:
        raise ValueError("limit must be between 1 and 500")

    try:
        response = await api_client.search_contexts_intelligently(
            query=query,
            context_type=context_type,
            compliance_standard=compliance_standard,
            cost_range=cost_range,
            security_score_min=security_score_min,
            limit=limit,
            api_key=api_key,
        )

        return response.get("data") or response

    except Exception as e:
        logger.error("Error in wistx_search_contexts_intelligently: %s", e, exc_info=True)
        raise


@require_query_quota
async def wistx_get_context(
    context_id: str,
    api_key: str,
) -> dict[str, Any]:
    """Retrieve context by ID with full analysis.

    Args:
        context_id: Context ID
        api_key: WISTX API key for authentication

    Returns:
        Dictionary with context details:
        {
            "context_id": "ctx_abc123",
            "title": "...",
            "summary": "...",
            "description": "...",
            "conversation_history": [...],
            "code_snippets": [...],
            "infrastructure_resources": [...],
            "analysis": {...},
            "linked_resources": [...],
            "linked_contexts": [...]
        }
    """
    user_id = await validate_api_key_and_get_user_id(api_key)
    if not user_id:
        raise ValueError("Authentication required - api_key is invalid")

    if not context_id:
        raise ValueError("context_id is required")

    try:
        response = await api_client.get_context(
            context_id=context_id,
            api_key=api_key,
        )

        return response.get("data") or response

    except Exception as e:
        logger.error("Error in wistx_get_context: %s", e, exc_info=True)
        raise


@require_query_quota
async def wistx_list_contexts(
    api_key: str,
    context_type: str | None = None,
    status: str | None = None,
    workspace: str | None = None,
    tags: list[str] | None = None,
    limit: int = 100,
    offset: int = 0,
) -> dict[str, Any]:
    """List contexts with filtering.

    Args:
        api_key: WISTX API key for authentication
        context_type: Filter by context type
        status: Filter by status ('active', 'archived', 'deleted')
        workspace: Filter by workspace
        tags: Filter by tags
        limit: Maximum number of results
        offset: Offset for pagination

    Returns:
        Dictionary with contexts list:
        {
            "contexts": [
                {
                    "context_id": "ctx_abc123",
                    "title": "...",
                    "type": "...",
                    "created_at": "..."
                }
            ],
            "total": 50,
            "limit": 100,
            "offset": 0
        }
    """
    user_id = await validate_api_key_and_get_user_id(api_key)
    if not user_id:
        raise ValueError("Authentication required - api_key is invalid")

    if limit < 1 or limit > 1000:
        raise ValueError("limit must be between 1 and 1000")
    if offset < 0:
        raise ValueError("offset must be >= 0")

    try:
        response = await api_client.list_contexts(
            context_type=context_type,
            status=status,
            workspace=workspace,
            tags=tags,
            limit=limit,
            offset=offset,
            api_key=api_key,
        )

        return response.get("data") or response

    except Exception as e:
        logger.error("Error in wistx_list_contexts: %s", e, exc_info=True)
        raise


@require_query_quota
async def wistx_link_contexts(
    source_context_id: str,
    target_context_id: str,
    relationship_type: str,
    api_key: str,
    strength: float = 1.0,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Link contexts with semantic relationship.

    Args:
        source_context_id: Source context ID
        target_context_id: Target context ID
        relationship_type: Relationship type ('depends_on', 'related_to', 'implements', 'references', 'supersedes')
        api_key: WISTX API key for authentication
        strength: Relationship strength (0.0-1.0, default: 1.0)
        metadata: Additional metadata

    Returns:
        Dictionary with link information:
        {
            "link_id": "link_abc123",
            "source_context_id": "ctx_abc123",
            "target_context_id": "ctx_def456",
            "relationship_type": "depends_on",
            "strength": 1.0
        }
    """
    user_id = await validate_api_key_and_get_user_id(api_key)
    if not user_id:
        raise ValueError("Authentication required - api_key is invalid")

    if not source_context_id or not target_context_id:
        raise ValueError("Both source_context_id and target_context_id are required")

    if source_context_id == target_context_id:
        raise ValueError("source_context_id and target_context_id must be different")

    valid_relationships = [
        "depends_on",
        "related_to",
        "implements",
        "references",
        "supersedes",
        "conflicts_with",
        "extends",
    ]
    if relationship_type not in valid_relationships:
        raise ValueError(
            f"Invalid relationship_type: {relationship_type}. "
            f"Must be one of: {', '.join(valid_relationships)}"
        )

    if strength < 0.0 or strength > 1.0:
        raise ValueError("strength must be between 0.0 and 1.0")

    try:
        response = await api_client.link_contexts(
            source_context_id=source_context_id,
            target_context_id=target_context_id,
            relationship_type=relationship_type,
            strength=strength,
            metadata=metadata,
            api_key=api_key,
        )

        return response.get("data") or response

    except Exception as e:
        logger.error("Error in wistx_link_contexts: %s", e, exc_info=True)
        raise


@require_query_quota
async def wistx_get_context_graph(
    context_id: str,
    api_key: str,
    depth: int = 2,
) -> dict[str, Any]:
    """Get context dependency graph showing relationships between contexts.

    Args:
        context_id: Root context ID
        api_key: WISTX API key for authentication
        depth: Maximum depth to traverse (default: 2)

    Returns:
        Dictionary with graph structure:
        {
            "root_context_id": "ctx_abc123",
            "nodes": [
                {
                    "context_id": "ctx_abc123",
                    "title": "...",
                    "type": "..."
                }
            ],
            "edges": [
                {
                    "source": "ctx_abc123",
                    "target": "ctx_def456",
                    "relationship": "depends_on",
                    "strength": 1.0
                }
            ]
        }
    """
    user_id = await validate_api_key_and_get_user_id(api_key)
    if not user_id:
        raise ValueError("Authentication required - api_key is invalid")

    if not context_id:
        raise ValueError("context_id is required")

    if depth < 1 or depth > 10:
        raise ValueError("depth must be between 1 and 10")

    try:
        response = await api_client.get_context_graph(
            context_id=context_id,
            depth=depth,
            api_key=api_key,
        )

        return response.get("data") or response

    except Exception as e:
        logger.error("Error in wistx_get_context_graph: %s", e, exc_info=True)
        raise

