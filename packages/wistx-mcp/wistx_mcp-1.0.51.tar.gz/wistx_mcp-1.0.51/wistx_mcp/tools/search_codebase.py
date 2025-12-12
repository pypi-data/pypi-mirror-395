"""Search codebase tool - search user's indexed repositories, documentation, and documents."""

import logging
from typing import Any

from bson import ObjectId

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.vector_search import VectorSearch
from wistx_mcp.tools.lib.api_client import WISTXAPIClient
from wistx_mcp.tools.lib.ai_analyzer import AIAnalyzer
from wistx_mcp.tools.lib.plan_enforcement import require_query_quota
from wistx_mcp.config import settings

logger = logging.getLogger(__name__)

api_client = WISTXAPIClient()
ai_analyzer = AIAnalyzer()


@require_query_quota
async def search_codebase(
    query: str,
    api_key: str,
    repositories: list[str] | None = None,
    resource_ids: list[str] | None = None,
    resource_types: list[str] | None = None,
    file_types: list[str] | None = None,
    code_type: str | None = None,
    cloud_provider: str | None = None,
    include_sources: bool = True,
    include_ai_analysis: bool = True,
    limit: int = 1000,
    analysis_mode: str | None = None,
    include_aggregated_summary: bool = False,
    check_freshness: bool = False,
    include_fresh_content: bool = False,
    max_stale_minutes: int = 60,
) -> dict[str, Any]:
    """Search user's indexed codebase with optional analysis aggregation.

    **CRITICAL: All results are user-scoped. Analysis only aggregates
    data from the authenticated user's indexed repositories.**

    Args:
        query: Natural language search question (or analysis type if analysis_mode specified)
        api_key: WISTX API key for authentication
        repositories: List of repositories to search (owner/repo format)
        resource_ids: Filter by specific indexed resources (alternative to repositories)
        resource_types: Filter by resource type (repository, documentation, document)
        file_types: Filter by file extensions (.tf, .yaml, .py, .md, etc.)
        code_type: Filter by code type (terraform, kubernetes, docker, python)
        cloud_provider: Filter by cloud provider mentioned in code
        include_sources: Include source code snippets in results (default: True)
        include_ai_analysis: Include AI-analyzed results with explanations (default: True)
        limit: Maximum number of results
        analysis_mode: "cost" | "compliance" | "infrastructure" | "security" | "all" | None
        include_aggregated_summary: Include aggregated summary in normal search (default: False)
        check_freshness: Check if indexed content is stale compared to repository (default: False)
        include_fresh_content: Fetch fresh content from GitHub for stale results (default: False)
        max_stale_minutes: Consider content stale if older than this many minutes (default: 60)

    Returns:
        If analysis_mode specified:
        {
            "analysis": {
                "cost": {...},
                "compliance": {...},
                "infrastructure": {...},
                "security": {...},
            },
            "resource_ids": [...],
            "user_id": "...",
        }

        Otherwise (normal search):
        {
            "results": [...],
            "resources": [...],
            "total": 123,
            "aggregated_summary": {...},  # If include_aggregated_summary=True
            "freshness": {...},  # If check_freshness=True or include_fresh_content=True
        }

    Raises:
        ValueError: If api_key is not provided or invalid parameters
        Exception: If search fails
    """
    from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id

    user_id = await validate_api_key_and_get_user_id(api_key)
    if not user_id:
        raise ValueError("Authentication required - api_key is invalid")

    if analysis_mode:
        if analysis_mode not in ["cost", "compliance", "infrastructure", "security", "all"]:
            raise ValueError(
                f"Invalid analysis_mode: {analysis_mode}. "
                "Must be one of: cost, compliance, infrastructure, security, all"
            )

        return await _get_aggregated_analysis(
            resource_ids=resource_ids or [],
            repositories=repositories or [],
            user_id=user_id,
            analysis_types=[analysis_mode] if analysis_mode != "all" else None,
            api_key=api_key,
        )

    from wistx_mcp.tools.lib.input_sanitizer import validate_query_input

    validate_query_input(query)

    if limit < 1 or limit > 50000:
        raise ValueError("limit must be between 1 and 50000")

    # Check if user has indexed resources BEFORE searching
    if not resource_ids and not repositories:
        has_indexed_resources = await _check_user_has_indexed_resources(user_id)
        if not has_indexed_resources:
            logger.info("No indexed resources found for user %s, returning setup guide", user_id)
            return await _get_indexing_setup_guide(user_id, api_key)

    logger.info(
        "Codebase search: query='%s', resources=%s, types=%s",
        query[:100],
        resource_ids,
        resource_types,
    )

    try:
        api_response = await api_client.search_codebase(
            query=query,
            repositories=repositories,
            resource_ids=resource_ids,
            resource_types=resource_types,
            file_types=file_types,
            code_type=code_type,
            cloud_provider=cloud_provider,
            include_sources=include_sources,
            include_ai_analysis=include_ai_analysis,
            limit=limit,
            api_key=api_key,
            check_freshness=check_freshness,
            include_fresh_content=include_fresh_content,
            max_stale_minutes=max_stale_minutes,
        )

        result = api_response.get("data") or api_response

        # Add metadata explaining empty results
        results_list = result.get("results", [])
        if len(results_list) == 0:
            result["empty_results_metadata"] = {
                "reason": "no_matches",
                "explanation": "No matches found for your query in the indexed resources",
                "possible_causes": [
                    "Query may be too specific - try broader terms",
                    "Resources may not contain matching content",
                    "Try refining your search query or filters",
                ],
                "suggestions": [
                    "Try using more general search terms",
                    "Remove specific filters to search more broadly",
                    "Check if your indexed resources contain relevant content",
                ],
            }
            if resource_ids or repositories:
                result["empty_results_metadata"]["reason"] = "no_matches_in_specified_resources"
                result["empty_results_metadata"]["explanation"] = (
                    "No matches found in the specified resources. "
                    "Try searching without resource filters to search all indexed resources."
                )

        if include_aggregated_summary and (resource_ids or repositories):
            summary = await _generate_aggregated_summary(
                resource_ids=resource_ids or [],
                repositories=repositories or [],
                user_id=user_id,
                results=results_list,
                api_key=api_key,
            )
            result["aggregated_summary"] = summary

        return result

    except Exception as e:
        logger.error("Error in search_codebase: %s", e, exc_info=True)
        raise


async def _validate_user_resources(
    resource_ids: list[str],
    user_id: str,
    api_key: str,
) -> list[str]:
    """Validate all resource_ids belong to authenticated user."""
    from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
    from bson import ObjectId

    async with MongoDBClient() as mongodb_client:
        await mongodb_client.connect()
        if not mongodb_client.database:
            raise RuntimeError("Database connection failed")

        collection = mongodb_client.database.indexed_resources

        valid_resources = []
        for resource_id in resource_ids:
            try:
                resource_doc = await collection.find_one({
                    "_id": ObjectId(resource_id) if ObjectId.is_valid(resource_id) else resource_id,
                    "user_id": ObjectId(user_id),
                })

                if resource_doc:
                    valid_resources.append(resource_id)
                else:
                    logger.warning(
                        "Resource %s not found or access denied for user %s",
                        resource_id,
                        user_id,
                    )
            except Exception as e:
                logger.warning("Error validating resource %s: %s", resource_id, e)
                continue

        if not valid_resources and resource_ids:
            error_msg = (
                "No valid resources found. All resource_ids must belong to the authenticated user. "
                f"Invalid resource_ids: {', '.join(resource_ids)}. "
            )
            error_msg += (
                "To get valid resource_ids, use wistx_manage_resources(action='list') "
                "to see all your indexed resources."
            )
            raise ValueError(error_msg)

        return valid_resources


async def _resolve_and_validate_repositories(
    repositories: list[str],
    user_id: str,
    api_key: str,
) -> list[str]:
    """Resolve repository URLs to resource_ids and validate user ownership."""
    from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
    from bson import ObjectId
    from wistx_mcp.tools.lib.repo_normalizer import normalize_repo_url

    async with MongoDBClient() as mongodb_client:
        await mongodb_client.connect()
        if not mongodb_client.database:
            raise RuntimeError("Database connection failed")

        collection = mongodb_client.database.indexed_resources
        resolved_resource_ids = []

        for repo in repositories:
            normalized_repo = repo.replace(".git", "").rstrip("/")
            if "/" not in normalized_repo:
                logger.warning("Invalid repository format: %s", repo)
                continue

            repo_patterns = [
                f"https://github.com/{normalized_repo}",
                f"https://github.com/{normalized_repo}.git",
                f"http://github.com/{normalized_repo}",
                f"http://github.com/{normalized_repo}.git",
                normalized_repo,
            ]

            found = False
            for pattern in repo_patterns:
                normalized_pattern = normalize_repo_url(pattern)
                resource_doc = await collection.find_one({
                    "user_id": ObjectId(user_id),
                    "resource_type": "repository",
                    "$or": [
                        {"normalized_repo_url": normalized_pattern},
                        {"repo_url": {"$regex": pattern, "$options": "i"}},
                    ],
                    "status": "completed",
                })

                if resource_doc:
                    resolved_resource_ids.append(str(resource_doc["_id"]))
                    found = True
                    break

            if not found:
                logger.warning(
                    "Repository %s not found or not owned by user %s",
                    repo,
                    user_id,
                )

        return resolved_resource_ids


async def _get_aggregated_analysis(
    resource_ids: list[str],
    repositories: list[str],
    user_id: str,
    analysis_types: list[str] | None,
    api_key: str,
) -> dict[str, Any]:
    """Get aggregated analysis from knowledge articles (USER-SCOPED)."""
    from api.services.repository_analysis_service import repository_analysis_service

    if repositories and not resource_ids:
        resource_ids = await _resolve_and_validate_repositories(
            repositories=repositories,
            user_id=user_id,
            api_key=api_key,
        )

    if not resource_ids:
        raise ValueError("Either resource_ids or repositories must be provided")

    if not user_id:
        raise ValueError("user_id is required for analysis aggregation")

    analysis_results = {}

    for resource_id in resource_ids:
        resource_analysis = {}

        if not analysis_types or "cost" in analysis_types:
            try:
                cost_analysis = await repository_analysis_service.get_cost_analysis(
                    resource_id=resource_id,
                    user_id=user_id,
                    refresh=False,
                )
                resource_analysis["cost"] = cost_analysis
            except Exception as e:
                logger.warning("Error getting cost analysis for %s: %s", resource_id, e)
                resource_analysis["cost"] = {"error": str(e)}

        if not analysis_types or "compliance" in analysis_types:
            try:
                compliance_analysis = await repository_analysis_service.get_compliance_analysis(
                    resource_id=resource_id,
                    user_id=user_id,
                    refresh=False,
                )
                resource_analysis["compliance"] = compliance_analysis
            except Exception as e:
                logger.warning("Error getting compliance analysis for %s: %s", resource_id, e)
                resource_analysis["compliance"] = {"error": str(e)}

        if not analysis_types or "infrastructure" in analysis_types:
            try:
                infra_analysis = await _get_infrastructure_analysis(
                    resource_id=resource_id,
                    user_id=user_id,
                )
                resource_analysis["infrastructure"] = infra_analysis
            except Exception as e:
                logger.warning("Error getting infrastructure analysis for %s: %s", resource_id, e)
                resource_analysis["infrastructure"] = {"error": str(e)}

        analysis_results[resource_id] = resource_analysis

    if len(resource_ids) == 1:
        return {
            "analysis": analysis_results[resource_ids[0]],
            "resource_id": resource_ids[0],
            "user_id": user_id,
        }

    return {
        "analysis": _aggregate_multiple_resources(analysis_results),
        "per_resource": analysis_results,
        "resource_ids": resource_ids,
        "user_id": user_id,
    }


async def _get_infrastructure_analysis(
    resource_id: str,
    user_id: str,
) -> dict[str, Any]:
    """Get infrastructure analysis by searching knowledge articles (USER-SCOPED)."""
    async with MongoDBClient() as mongodb_client:
        await mongodb_client.connect()
        if not mongodb_client.database:
            return {"resources": [], "relationships": [], "total_resources": 0}

        vector_search = VectorSearch(
            mongodb_client,
            gemini_api_key=settings.gemini_api_key,
        )

        search_results = await vector_search.search_knowledge_articles(
            query="infrastructure resources components dependencies",
            user_id=user_id,
            include_global=False,
            resource_ids=[resource_id],
            limit=1000,
        )

        resources = []
        relationships = []

        for article in search_results:
            structured_data = article.get("structured_data", {})
            if structured_data.get("resource_type"):
                resources.append({
                    "name": article.get("title", ""),
                    "type": structured_data.get("resource_type"),
                    "file_path": article.get("source_url", ""),
                    "cost": article.get("cost_impact", {}).get("total_monthly", 0),
                })

            if "dependencies" in structured_data:
                relationships.extend(structured_data["dependencies"])

        return {
            "resources": resources,
            "relationships": relationships,
            "total_resources": len(resources),
        }


def _aggregate_multiple_resources(
    analysis_results: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Aggregate analysis across multiple resources."""
    aggregated = {
        "cost": {
            "total_monthly": 0.0,
            "breakdown": {"by_service": {}, "by_resource_type": {}, "by_cloud_provider": {}},
        },
        "compliance": {
            "standards": {},
            "overall_status": "unknown",
        },
        "infrastructure": {
            "resources": [],
            "relationships": [],
        },
    }

    for resource_id, analysis in analysis_results.items():
        if "cost" in analysis and isinstance(analysis["cost"], dict):
            cost = analysis["cost"]
            aggregated["cost"]["total_monthly"] += cost.get("total_monthly", 0.0)

        if "compliance" in analysis and isinstance(analysis["compliance"], dict):
            compliance = analysis["compliance"]
            standards = compliance.get("standards", {})
            for standard, data in standards.items():
                if standard not in aggregated["compliance"]["standards"]:
                    aggregated["compliance"]["standards"][standard] = {
                        "compliant_count": 0,
                        "non_compliant_count": 0,
                        "partial_count": 0,
                    }
                aggregated["compliance"]["standards"][standard]["compliant_count"] += data.get("compliant_count", 0)
                aggregated["compliance"]["standards"][standard]["non_compliant_count"] += data.get("non_compliant_count", 0)
                aggregated["compliance"]["standards"][standard]["partial_count"] += data.get("partial_count", 0)

        if "infrastructure" in analysis and isinstance(analysis["infrastructure"], dict):
            infra = analysis["infrastructure"]
            aggregated["infrastructure"]["resources"].extend(infra.get("resources", []))
            aggregated["infrastructure"]["relationships"].extend(infra.get("relationships", []))

    return aggregated


async def _generate_aggregated_summary(
    resource_ids: list[str],
    repositories: list[str],
    user_id: str,
    results: list[dict[str, Any]],
    api_key: str,
) -> dict[str, Any]:
    """Generate aggregated summary from search results."""
    if not resource_ids and repositories:
        resource_ids = await _resolve_and_validate_repositories(
            repositories=repositories,
            user_id=user_id,
            api_key=api_key,
        )

    if not resource_ids:
        return {}

    from api.services.repository_analysis_service import repository_analysis_service

    summary = {
        "resource_count": len(resource_ids),
        "results_count": len(results),
    }

    try:
        cost_summary = await repository_analysis_service.get_cost_analysis(
            resource_id=resource_ids[0],
            user_id=user_id,
            refresh=False,
        )
        summary["cost_summary"] = {
            "total_monthly": cost_summary.get("total_monthly", 0),
        }
    except Exception:
        pass

    return summary


async def _check_user_has_indexed_resources(user_id: str) -> bool:
    """Check if user has any indexed resources.
    
    Args:
        user_id: User ID
        
    Returns:
        True if user has indexed resources, False otherwise
    """
    try:
        async with MongoDBClient() as mongodb_client:
            await mongodb_client.connect()
            if not mongodb_client.database:
                return False
            
            collection = mongodb_client.database.indexed_resources
            
            from bson import ObjectId
            from wistx_mcp.tools.lib.mongodb_client import execute_mongodb_operation
            from wistx_mcp.tools.lib.constants import API_TIMEOUT_SECONDS
            
            async def _count_resources() -> int:
                count = await collection.count_documents({
                    "user_id": ObjectId(user_id),
                    "status": "completed",
                })
                return count
            
            resource_count = await execute_mongodb_operation(
                _count_resources,
                timeout=API_TIMEOUT_SECONDS,
                max_retries=2,
            )
            
            return resource_count > 0
    except Exception as e:
        logger.warning("Failed to check indexed resources: %s", e)
        return False


async def _get_indexing_setup_guide(user_id: str, api_key: str) -> dict[str, Any]:
    """Generate comprehensive setup guide for indexing repositories.
    
    Args:
        user_id: User ID
        api_key: API key for authentication
        
    Returns:
        Dictionary with setup guide and instructions
    """
    return {
        "setup_required": True,
        "error": "No indexed resources found",
        "message": (
            "To search your codebase, you need to index repositories first. "
            "I can help you get started with indexing."
        ),
        "setup_guide": {
            "overview": (
                "You need to index at least one GitHub repository before you can search your codebase. "
                "Indexing makes your code searchable and enables codebase analysis features."
            ),
            "steps": [
                {
                    "step": 1,
                    "title": "Index a Repository",
                    "description": "Index your GitHub repository to make it searchable",
                    "status": "pending",
                    "action": "Use the wistx_index_repository tool to index your repository",
                    "instructions": [
                        "1. Get your GitHub repository URL (e.g., https://github.com/owner/repo)",
                        "2. Use wistx_index_repository tool with the repository URL",
                        "3. Wait for indexing to complete (usually takes a few minutes)",
                        "4. Check indexing status with wistx_manage_resources(action='list')",
                    ],
                    "example_request": {
                        "method": "MCP Tool Call",
                        "tool": "wistx_index_repository",
                        "parameters": {
                            "repo_url": "https://github.com/owner/repo",
                            "branch": "main",
                            "api_key": "YOUR_API_KEY",
                        },
                    },
                    "note": "Indexing runs in the background. You can check status anytime.",
                },
                {
                    "step": 2,
                    "title": "Check Indexing Status",
                    "description": "Verify that indexing completed successfully",
                    "status": "pending",
                    "action": "Use wistx_manage_resources to check status",
                    "instructions": [
                        "1. Use wistx_manage_resources(action='list') to see all indexed resources",
                        "2. Look for status='completed' for your repository",
                        "3. If status='indexing', wait a bit longer",
                        "4. If status='failed', check the error message and retry",
                    ],
                    "example_request": {
                        "method": "MCP Tool Call",
                        "tool": "wistx_manage_resources",
                        "parameters": {
                            "action": "list",
                            "api_key": "YOUR_API_KEY",
                        },
                    },
                },
                {
                    "step": 3,
                    "title": "Search Your Codebase",
                    "description": "Once indexing is complete, you can search your codebase",
                    "status": "pending",
                    "note": (
                        "After indexing completes, return here and use wistx_search_codebase "
                        "to search your code. The tool will automatically use your indexed repositories."
                    ),
                },
            ],
            "quick_start": {
                "description": "Quick start example to index a repository:",
                "example": (
                    "wistx_index_repository(\n"
                    "    repo_url='https://github.com/your-org/your-repo',\n"
                    "    branch='main',\n"
                    "    api_key='YOUR_API_KEY'\n"
                    ")"
                ),
            },
            "alternative_methods": {
                "dashboard": (
                    "You can also index repositories via the WISTX dashboard at "
                    "https://app.wistx.com/resources for a visual experience."
                ),
            },
        },
        "api_endpoints": {
            "index_repository": {
                "tool": "wistx_index_repository",
                "description": "Index a GitHub repository for search",
            },
            "list_resources": {
                "tool": "wistx_manage_resources",
                "description": "List all indexed resources and check status",
            },
            "check_status": {
                "tool": "wistx_manage_resources",
                "description": "Check indexing status for a specific resource",
            },
        },
    }

