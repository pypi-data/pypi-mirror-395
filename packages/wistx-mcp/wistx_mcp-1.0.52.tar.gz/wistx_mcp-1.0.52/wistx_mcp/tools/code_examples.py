"""Code examples tool - search infrastructure code examples."""

import logging
import sys
from typing import Any

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.vector_search import VectorSearch
from wistx_mcp.tools.lib.auth_context import get_auth_context
from wistx_mcp.config import settings

logger = logging.getLogger(__name__)

# Patch sys.exit to prevent api.config from exiting the MCP server
_original_sys_exit = sys.exit

def _mcp_safe_exit(code: int = 0) -> None:
    """MCP-safe sys.exit that raises SystemExit instead of exiting."""
    raise SystemExit(code)


async def get_code_examples(
    query: str,
    code_types: list[str] | None = None,
    cloud_provider: str | None = None,
    services: list[str] | None = None,
    min_quality_score: int | None = None,
    compliance_standard: str | None = None,
    limit: int = 1000,
) -> dict[str, Any]:
    """Search infrastructure code examples.
    
    Args:
        query: Search query (e.g., "RDS database with encryption")
        code_types: Filter by code types (terraform, kubernetes, docker, pulumi, etc.)
        cloud_provider: Filter by cloud provider (aws, gcp, azure, oracle, alibaba).
                       Use None or omit for multi-cloud searches across all providers.
        services: Filter by cloud services (rds, s3, ec2, etc.)
        min_quality_score: Minimum quality score (0-100)
        compliance_standard: Filter by compliance standard (PCI-DSS, HIPAA, etc.)
        limit: Maximum number of results
        
    Returns:
        Dictionary with code examples and metadata
        
    Raises:
        RuntimeError: If quota is exceeded or search fails
        ValueError: If query is invalid or cloud_provider is invalid
    """
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")
    
    if limit <= 0 or limit > 50000:
        raise ValueError("Limit must be between 1 and 50000")
    
    valid_providers = ["aws", "gcp", "azure", "oracle", "alibaba"]
    
    cloud_provider_normalized = None
    if cloud_provider:
        cloud_provider_normalized = cloud_provider.strip().lower()
        
        if cloud_provider_normalized == "multi-cloud" or cloud_provider_normalized == "multi_cloud":
            logger.info(
                "Multi-cloud search requested. Searching across all providers by setting cloud_provider to None."
            )
            cloud_provider_normalized = None
        elif cloud_provider_normalized not in valid_providers:
            raise ValueError(
                f"Invalid cloud_provider: {cloud_provider}. "
                f"Must be one of: {', '.join(valid_providers)}, or 'multi-cloud' (which searches all providers)."
            )
    
    auth_ctx = get_auth_context()
    if auth_ctx:
        user_id = auth_ctx.get_user_id()
        if user_id:
            try:
                sys.exit = _mcp_safe_exit
                from api.services.quota_service import quota_service, QuotaExceededError
                sys.exit = _original_sys_exit

                plan = "professional"
                if auth_ctx.user_info:
                    plan = auth_ctx.user_info.get("plan", "professional")
                await quota_service.check_query_quota(user_id, plan)
            except ImportError:
                sys.exit = _original_sys_exit
                logger.debug("API quota service not available, skipping quota check")
            except QuotaExceededError as e:
                sys.exit = _original_sys_exit
                logger.warning("Quota exceeded for user %s: %s", user_id, e)
                raise RuntimeError(f"Quota exceeded: {e}") from e
            except Exception as e:
                sys.exit = _original_sys_exit
                logger.warning("Failed to check quota (continuing): %s", e)
    
    async with MongoDBClient() as client:
        vector_search = VectorSearch(client, gemini_api_key=settings.gemini_api_key)
        
        try:
            results = await vector_search.search_code_examples(
                query=query,
                code_types=code_types,
                cloud_provider=cloud_provider_normalized,
                services=services,
                min_quality_score=min_quality_score,
                compliance_standard=compliance_standard,
                limit=limit,
            )
            
            formatted_results = []
            for result in results:
                formatted_result = {
                    "example_id": result.get("example_id"),
                    "title": result.get("title"),
                    "description": result.get("description"),
                    "contextual_description": result.get("contextual_description"),
                    "code_type": result.get("code_type"),
                    "cloud_provider": result.get("cloud_provider"),
                    "services": result.get("services", []),
                    "resources": result.get("resources", []),
                    "code": result.get("code", ""),
                    "github_url": result.get("github_url"),
                    "file_path": result.get("file_path"),
                    "stars": result.get("stars", 0),
                    "quality_score": result.get("quality_score", 0),
                    "best_practices": result.get("best_practices", []),
                    "hybrid_score": result.get("hybrid_score", 0.0),
                    "vector_score": result.get("vector_score", 0.0),
                    "bm25_score": result.get("bm25_score", 0.0),
                }
                
                compliance_analysis = result.get("compliance_analysis")
                if compliance_analysis:
                    formatted_result["compliance_analysis"] = {
                        "applicable_standards": compliance_analysis.get("applicable_standards", []),
                        "compliance_score": compliance_analysis.get("compliance_score", {}),
                    }
                
                cost_analysis = result.get("cost_analysis")
                if cost_analysis:
                    formatted_result["cost_analysis"] = {
                        "estimated_monthly": cost_analysis.get("estimated_monthly", 0.0),
                        "estimated_annual": cost_analysis.get("estimated_annual", 0.0),
                    }
                
                formatted_results.append(formatted_result)
            
            result_dict = {
                "examples": formatted_results,
                "total": len(formatted_results),
                "query": query,
            }
            
            # Provide suggestions if no results found
            if len(formatted_results) == 0:
                suggestions = _generate_query_suggestions(query, code_types, cloud_provider, services)
                result_dict["suggestions"] = suggestions
                result_dict["message"] = (
                    "No code examples found for your query. Try the suggested alternative queries below, "
                    "or refine your search by adjusting filters."
                )
            
            return result_dict
        
        except ValueError as e:
            logger.warning("Invalid query parameters: %s", e)
            raise
        except Exception as e:
            logger.error("Error searching code examples: %s", e, exc_info=True)
            raise RuntimeError(f"Failed to search code examples: {e}") from e


def _generate_query_suggestions(
    query: str,
    code_types: list[str] | None,
    cloud_provider: str | None,
    services: list[str] | None,
) -> dict[str, Any]:
    """Generate alternative query suggestions when no results found.
    
    Args:
        query: Original query
        code_types: Original code types filter
        cloud_provider: Original cloud provider filter
        services: Original services filter
        
    Returns:
        Dictionary with suggested queries and tips
    """
    suggestions = {
        "alternative_queries": [],
        "tips": [],
    }
    
    query_lower = query.lower()
    
    # Suggest broader queries
    if "encryption" in query_lower:
        suggestions["alternative_queries"].append(query.replace("encryption", "security"))
        suggestions["alternative_queries"].append(query.replace("encryption", "data protection"))
    
    if "autoscaling" in query_lower or "auto-scaling" in query_lower:
        suggestions["alternative_queries"].append(query.replace("autoscaling", "scaling").replace("auto-scaling", "scaling"))
        suggestions["alternative_queries"].append(query.replace("autoscaling", "elastic").replace("auto-scaling", "elastic"))
    
    if "high availability" in query_lower or "ha" in query_lower:
        suggestions["alternative_queries"].append(query.replace("high availability", "redundancy").replace("ha", "redundancy"))
        suggestions["alternative_queries"].append(query.replace("high availability", "fault tolerance").replace("ha", "fault tolerance"))
    
    # Suggest removing specific terms
    specific_terms = ["encrypted", "secure", "compliant", "production", "enterprise"]
    for term in specific_terms:
        if term in query_lower:
            simplified = query
            for t in specific_terms:
                simplified = simplified.replace(t, "").replace(t.capitalize(), "")
            simplified = " ".join(simplified.split())  # Clean up extra spaces
            if simplified and simplified != query:
                suggestions["alternative_queries"].append(simplified)
            break
    
    # Provider-specific suggestions
    if cloud_provider:
        provider_map = {
            "aws": ["EC2", "S3", "RDS", "Lambda", "EKS"],
            "gcp": ["GCE", "Cloud Storage", "Cloud SQL", "Cloud Functions", "GKE"],
            "azure": ["Virtual Machines", "Storage Account", "SQL Database", "Functions", "AKS"],
        }
        if cloud_provider.lower() in provider_map:
            suggestions["tips"].append(
                f"Try searching for specific {cloud_provider.upper()} services: "
                f"{', '.join(provider_map[cloud_provider.lower()][:3])}"
            )
    
    # Code type suggestions
    if code_types and len(code_types) == 1:
        code_type_map = {
            "terraform": ["kubernetes", "docker"],
            "kubernetes": ["terraform", "helm"],
            "docker": ["kubernetes", "terraform"],
        }
        if code_types[0].lower() in code_type_map:
            suggestions["tips"].append(
                f"Try other code types: {', '.join(code_type_map[code_types[0].lower()])}"
            )
    
    # General tips
    if not suggestions["tips"]:
        suggestions["tips"].extend([
            "Try using more general terms (e.g., 'database' instead of 'encrypted PostgreSQL database')",
            "Remove specific filters and search broadly, then narrow down",
            "Check spelling and try synonyms (e.g., 'compute' instead of 'server')",
        ])
    
    # Limit suggestions
    suggestions["alternative_queries"] = suggestions["alternative_queries"][:5]
    suggestions["tips"] = suggestions["tips"][:3]
    
    return suggestions

