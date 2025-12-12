"""MCP tool for getting existing infrastructure context."""

import logging
from typing import Any

from wistx_mcp.tools.lib.api_client import WISTXAPIClient
from wistx_mcp.tools.lib.url_validator import validate_github_url
from wistx_mcp.tools.lib.plan_enforcement import require_query_quota

logger = logging.getLogger(__name__)

api_client = WISTXAPIClient()


@require_query_quota
async def get_existing_infrastructure(
    repository_url: str,
    environment_name: str | None = None,
    include_compliance: bool = True,
    include_costs: bool = True,
    api_key: str = "",
) -> dict[str, Any]:
    """Get existing infrastructure context for coding agents.

    This tool provides context about existing infrastructure so coding agents
    can make informed decisions when adding new resources.

    Args:
        repository_url: GitHub repository URL
        environment_name: Environment name (dev, stage, prod, etc.)
        include_compliance: Include compliance status
        include_costs: Include cost information
        api_key: WISTX API key (required for authentication)

    Returns:
        Dictionary with existing infrastructure context:
        - resources: List of existing resources
        - total_monthly_cost: Total monthly cost
        - compliance_summary: Compliance assessment
        - recommendations: Recommendations for new resources

    Raises:
        ValueError: If api_key is missing or invalid
        RuntimeError: If API call fails
    """
    if not repository_url or not isinstance(repository_url, str):
        raise ValueError("Repository URL is required and must be a string")
    
    repository_url = repository_url.strip()
    
    if repository_url.startswith("file://") or repository_url.startswith("/") or ("\\" in repository_url and not repository_url.startswith("http")):
        raise ValueError(
            "Local file paths are not supported. This tool requires a GitHub repository URL provided by the user. "
            "Please ask the user for their GitHub repository URL (e.g., https://github.com/owner/repo) before calling this tool."
        )
    
    if not repository_url.startswith(("http://", "https://")):
        raise ValueError(
            "Invalid repository URL format. This tool requires a GitHub repository URL provided by the user. "
            "Please ask the user for their GitHub repository URL (e.g., https://github.com/owner/repo) before calling this tool."
        )
    
    from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id
    from wistx_mcp.tools.lib.input_sanitizer import validate_repository_url_input

    validate_repository_url_input(repository_url)

    try:
        validated_repo_url = await validate_github_url(repository_url)
    except ValueError as e:
        error_msg = str(e)
        if "file" in error_msg.lower() or repository_url.startswith("file://"):
            raise ValueError(
                f"Local file paths are not supported. This tool requires a GitHub repository URL provided by the user. "
                f"Please ask the user for their GitHub repository URL (e.g., https://github.com/owner/repo). Error: {error_msg}"
            ) from e
        raise ValueError(f"Invalid GitHub repository URL: {error_msg}") from e

    try:
        user_id = await validate_api_key_and_get_user_id(api_key)
    except (ValueError, RuntimeError) as e:
        raise

    # Check if repository is indexed BEFORE calling API
    is_indexed = await _check_repository_indexed(user_id, validated_repo_url)
    if not is_indexed:
        logger.info("Repository %s not indexed for user %s, returning setup guide", validated_repo_url, user_id)
        return await _get_repository_indexing_setup_guide(validated_repo_url, user_id, api_key)

    try:
        api_response = await api_client.get_infrastructure_inventory(
            repository_url=validated_repo_url,
            environment_name=environment_name,
            api_key=api_key,
        )

        if api_response.get("data"):
            return api_response["data"]
        return api_response

    except Exception as e:
        logger.error("Error getting existing infrastructure: %s", e, exc_info=True)
        raise RuntimeError(f"Failed to get existing infrastructure context: {e}") from e


def _group_by_service(resources: list[dict[str, Any]]) -> dict[str, float]:
    """Group resources by service and sum costs.

    Args:
        resources: List of resources

    Returns:
        Dictionary mapping service to total monthly cost
    """
    grouped = {}
    for resource in resources:
        service = resource.get("service", "unknown")
        cost = resource.get("monthly_cost", 0)
        grouped[service] = grouped.get(service, 0) + cost
    return grouped


def _group_by_resource_type(resources: list[dict[str, Any]]) -> dict[str, float]:
    """Group resources by resource type and sum costs.

    Args:
        resources: List of resources

    Returns:
        Dictionary mapping resource type to total monthly cost
    """
    grouped = {}
    for resource in resources:
        resource_type = resource.get("resource_type", "unknown")
        cost = resource.get("monthly_cost", 0)
        grouped[resource_type] = grouped.get(resource_type, 0) + cost
    return grouped


def _calculate_overall_compliance(compliance_summary: dict[str, Any]) -> str:
    """Calculate overall compliance status.

    Args:
        compliance_summary: Compliance summary dictionary

    Returns:
        Overall compliance status (compliant, partial, non_compliant)
    """
    if not compliance_summary:
        return "unknown"

    total_compliant = 0
    total_non_compliant = 0

    for standard_data in compliance_summary.values():
        total_compliant += standard_data.get("compliant_count", 0)
        total_non_compliant += standard_data.get("non_compliant_count", 0)

    total = total_compliant + total_non_compliant
    if total == 0:
        return "unknown"

    compliance_rate = (total_compliant / total) * 100

    if compliance_rate >= 90:
        return "compliant"
    elif compliance_rate >= 50:
        return "partial"
    else:
        return "non_compliant"


def _generate_recommendations(result: dict[str, Any]) -> list[str]:
    """Generate recommendations based on analysis results.

    Args:
        result: Analysis result dictionary

    Returns:
        List of recommendation strings
    """
    recommendations = []
    
    total_cost = result.get("total_monthly_cost", 0)
    if total_cost > 500:
        recommendations.append(f"Consider cost optimization - current spending: ${total_cost:.2f}/month")
    
    compliance_status = result.get("compliance_status", "unknown")
    if compliance_status == "non_compliant":
        recommendations.append("Address compliance issues before adding new resources")
    elif compliance_status == "partial":
        recommendations.append("Review partial compliance issues")
    
    return recommendations


def _generate_agent_context(result: dict[str, Any]) -> str:
    """Generate context message for coding agents.

    Args:
        inventory: Infrastructure inventory

    Returns:
        Context message string
    """
    resources_count = result.get("resources_count", 0)
    total_cost = result.get("total_monthly_cost", 0)
    compliance_summary = result.get("compliance_summary", {})

    context = f"Existing Infrastructure Context:\n\n"
    context += f"- Total Resources: {resources_count}\n"
    context += f"- Monthly Cost: ${total_cost:.2f}\n"

    if compliance_summary:
        context += f"\nCompliance Status:\n"
        for standard, data in compliance_summary.items():
            rate = data.get("compliance_rate", 0)
            context += f"- {standard.upper()}: {rate:.1f}% compliant "
            context += f"({data.get('compliant_count', 0)}/{data.get('total_components', 0)})\n"

    recommendations = result.get("recommendations", [])
    if recommendations:
        context += f"\nRecommendations:\n"
        for rec in recommendations[:5]:
            context += f"- {rec}\n"

    context += f"\nWhen adding new resources, consider:\n"
    context += f"- Existing resources to avoid duplicates\n"
    context += f"- Compliance requirements for new resources\n"
    context += f"- Budget constraints (current: ${total_cost:.2f}/month)\n"
    context += f"- Integration with existing infrastructure\n"

    return context


async def _check_repository_indexed(user_id: str, repository_url: str) -> bool:
    """Check if repository is indexed for the user.
    
    Args:
        user_id: User ID
        repository_url: Repository URL to check
        
    Returns:
        True if repository is indexed and completed, False otherwise
    """
    try:
        from wistx_mcp.tools.lib.mongodb_client import MongoDBClient, execute_mongodb_operation
        from wistx_mcp.tools.lib.repo_normalizer import normalize_repo_url
        from wistx_mcp.tools.lib.constants import API_TIMEOUT_SECONDS
        from bson import ObjectId
        
        async with MongoDBClient() as mongodb_client:
            await mongodb_client.connect()
            if not mongodb_client.database:
                return False
            
            collection = mongodb_client.database.indexed_resources
            normalized_repo = normalize_repo_url(repository_url)
            
            async def _check_indexed() -> bool:
                resource_doc = await collection.find_one({
                    "user_id": ObjectId(user_id),
                    "resource_type": "repository",
                    "$or": [
                        {"normalized_repo_url": normalized_repo},
                        {"repo_url": {"$regex": repository_url, "$options": "i"}},
                    ],
                    "status": "completed",
                })
                return resource_doc is not None
            
            is_indexed = await execute_mongodb_operation(
                _check_indexed,
                timeout=API_TIMEOUT_SECONDS,
                max_retries=2,
            )
            
            return is_indexed
    except Exception as e:
        logger.warning("Failed to check repository indexing status: %s", e)
        return False


async def _get_repository_indexing_setup_guide(
    repository_url: str,
    user_id: str,
    api_key: str,
) -> dict[str, Any]:
    """Generate setup guide for repository indexing.
    
    Args:
        repository_url: Repository URL that needs to be indexed
        user_id: User ID
        api_key: API key for authentication
        
    Returns:
        Dictionary with setup guide and instructions
    """
    return {
        "setup_required": True,
        "error": "Repository not indexed",
        "message": (
            f"The repository {repository_url} is not indexed yet. "
            "You need to index it first to get infrastructure context."
        ),
        "repository_url": repository_url,
        "setup_guide": {
            "overview": (
                "This tool requires the repository to be indexed first. "
                "Indexing analyzes your repository structure and extracts infrastructure information."
            ),
            "steps": [
                {
                    "step": 1,
                    "title": "Index the Repository",
                    "description": f"Index {repository_url} to enable infrastructure context",
                    "status": "pending",
                    "action": "Use the wistx_index_repository tool to index this repository",
                    "instructions": [
                        f"1. Use wistx_index_repository with repo_url='{repository_url}'",
                        "2. Wait for indexing to complete (usually takes a few minutes)",
                        "3. Check indexing status with wistx_manage_resources(action='list')",
                        "4. Once status is 'completed', you can get infrastructure context",
                    ],
                    "example_request": {
                        "method": "MCP Tool Call",
                        "tool": "wistx_index_repository",
                        "parameters": {
                            "repo_url": repository_url,
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
                        f"2. Look for your repository: {repository_url}",
                        "3. Check that status='completed'",
                        "4. If status='indexing', wait a bit longer",
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
                    "title": "Get Infrastructure Context",
                    "description": "Once indexing is complete, get infrastructure context",
                    "status": "pending",
                    "note": (
                        "After indexing completes, return here and use wistx_get_existing_infrastructure "
                        f"with repository_url='{repository_url}' to get infrastructure context."
                    ),
                },
            ],
            "quick_start": {
                "description": "Quick start example to index this repository:",
                "example": (
                    f"wistx_index_repository(\n"
                    f"    repo_url='{repository_url}',\n"
                    f"    branch='main',\n"
                    f"    api_key='YOUR_API_KEY'\n"
                    f")"
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
                "description": f"Index {repository_url} for infrastructure analysis",
            },
            "list_resources": {
                "tool": "wistx_manage_resources",
                "description": "List all indexed resources and check status",
            },
        },
    }

