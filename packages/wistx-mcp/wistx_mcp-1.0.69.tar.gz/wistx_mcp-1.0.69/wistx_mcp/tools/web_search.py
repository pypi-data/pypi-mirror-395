"""Web search tool - unified search for DevOps/infrastructure/compliance/finops/SRE."""

import logging
import sys
from typing import Any

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.security_client import SecurityClient
from wistx_mcp.tools.lib.web_search_client import WebSearchClient
from wistx_mcp.tools.lib.auth_context import get_auth_context
from wistx_mcp.config import settings
from wistx_mcp.tools.lib.constants import MAX_SEARCH_RESULTS

logger = logging.getLogger(__name__)

_original_sys_exit = sys.exit


def _mcp_safe_exit(code: int = 0) -> None:
    """MCP-safe sys.exit that raises SystemExit instead of exiting."""
    raise SystemExit(code)


def _infer_domains_from_search_context(
    search_type: str,
    resource_type: str | None = None,
    cloud_provider: str | None = None,
) -> list[str]:
    """Infer knowledge domains from search context.

    Args:
        search_type: Type of search (general, security)
        resource_type: Resource type filter (RDS, S3, EKS, etc.)
        cloud_provider: Cloud provider filter (aws, gcp, azure)

    Returns:
        List of inferred domains
    """
    domains = []

    if search_type == "security":
        domains.append("security")

    if resource_type:
        resource_lower = resource_type.lower()
        if resource_lower in ["rds", "s3", "ec2", "lambda", "eks", "gke", "aks", "vpc", "iam"]:
            domains.append("infrastructure")
        if resource_lower in ["rds", "s3", "eks", "gke", "aks"]:
            domains.append("compliance")

    if cloud_provider:
        domains.append("infrastructure")

    if not domains:
        domains = ["devops", "infrastructure"]

    return list(set(domains))


async def web_search(
    query: str,
    search_type: str = "general",
    resource_type: str | None = None,
    cloud_provider: str | None = None,
    severity: str | None = None,
    include_cves: bool = True,
    include_advisories: bool = True,
    limit: int = 1000,
    api_key: str = "",
) -> dict[str, Any]:
    """Web search for security information and general web content.

    Focused on security searches (CVEs, advisories) and general web search.
    For compliance requirements, use get_compliance_requirements tool.
    For deep research, use research_knowledge_base tool.

    Args:
        query: Search query
        search_type: Type of search (general, security)
        resource_type: Filter by resource type (RDS, S3, EKS, etc.)
        cloud_provider: Filter by cloud provider (aws, gcp, azure)
        severity: Filter by severity (for security searches)
        include_cves: Include CVE database results
        include_advisories: Include security advisories
        limit: Maximum number of results
        api_key: WISTX API key (required for authentication)

    Returns:
        Dictionary with search results:
        - web: Web search results (Tavily)
        - security: Security-related results (CVEs, advisories)
        - total: Total results count

    Raises:
        ValueError: If invalid search_type or parameters
        Exception: If search fails
    """
    if search_type not in ["general", "security"]:
        raise ValueError(f"Invalid search_type: {search_type}. Use 'general' or 'security'")

    if limit < 1 or limit > MAX_SEARCH_RESULTS:
        raise ValueError(f"limit must be between 1 and {MAX_SEARCH_RESULTS}")

    from wistx_mcp.tools.lib.input_sanitizer import validate_query_input

    validate_query_input(query)

    from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id

    try:
        await validate_api_key_and_get_user_id(api_key)
    except (ValueError, RuntimeError):
        raise

    logger.info(
        "Web search: query='%s', type=%s, resource=%s, cloud=%s",
        query[:100],
        search_type,
        resource_type,
        cloud_provider,
    )

    auth_ctx = get_auth_context()
    if auth_ctx:
        user_id = auth_ctx.get_user_id()
        if user_id:
            try:
                from api.services.quota_service import quota_service, QuotaExceededError

                plan = "professional"
                if auth_ctx.user_info:
                    plan = auth_ctx.user_info.get("plan", "professional")
                await quota_service.check_query_quota(user_id, plan)
            except ImportError:
                logger.debug("API quota service not available, skipping quota check")
            except QuotaExceededError as e:
                logger.warning("Quota exceeded for user %s: %s", user_id, e)
                raise RuntimeError(f"Quota exceeded: {e}") from e
            except Exception as e:
                logger.warning("Failed to check quota (continuing): %s", e)

    results: dict[str, Any] = {
        "web": [],
        "security": [],
        "total": 0,
    }

    security_client = None
    web_search_client = None

    async with MongoDBClient() as mongodb_client:

        security_client = SecurityClient(mongodb_client)

        if settings.tavily_api_key:
            web_search_client = WebSearchClient(api_key=settings.tavily_api_key)

        if web_search_client:
            try:
                web_results = await web_search_client.search_devops(
                    query=query,
                    max_results=limit,
                )

                web_items = []
                if web_results.get("answer"):
                    web_items.append({
                        "title": "AI Answer",
                        "content": web_results["answer"],
                        "source": "tavily",
                        "type": "answer",
                    })

                for result in web_results.get("results", []):
                    web_items.append({
                        "title": result.get("title", ""),
                        "content": result.get("content", ""),
                        "url": result.get("url", ""),
                        "score": result.get("score", 0),
                        "source": "tavily",
                        "type": "web_result",
                    })

                results["web"] = web_items

                if web_results and web_items:
                    try:
                        sys.exit = _mcp_safe_exit
                        from api.services.web_search_storage_service import web_search_storage_service
                        sys.exit = _original_sys_exit

                        domains_searched = _infer_domains_from_search_context(
                            search_type=search_type,
                            resource_type=resource_type,
                            cloud_provider=cloud_provider,
                        )

                        storage_stats = await web_search_storage_service.store_web_search_results(
                            web_results={
                                "results": web_results.get("results", []),
                                "answer": web_results.get("answer"),
                            },
                            query=query,
                            domains_searched=domains_searched,
                            store_in_background=True,
                        )

                        logger.info(
                            "Web search results storage initiated: query='%s', %d results, %d will be stored",
                            query[:100],
                            storage_stats["total_results"],
                            storage_stats.get("stored", 0) + storage_stats.get("converted", 0),
                        )
                    except ImportError:
                        logger.debug("Web search storage service not available, skipping storage")
                    except Exception as e:
                        logger.warning("Failed to store web search results (non-critical): %s", e, exc_info=True)
            except Exception as e:
                logger.warning("Failed to perform web search: %s", e)

        if search_type in ["general", "security"] and include_cves:
            try:
                cves = await security_client.search_cves(
                    query=query,
                    resource_type=resource_type,
                    severity=severity,
                    limit=limit,
                )
                results["security"].extend(cves)
            except Exception as e:
                logger.warning("Failed to search CVEs: %s", e)

        if search_type in ["general", "security"] and include_advisories:
            try:
                advisories = await security_client.search_advisories(
                    query=query,
                    cloud_provider=cloud_provider,
                    limit=limit,
                )
                results["security"].extend(advisories)
            except Exception as e:
                logger.warning("Failed to search advisories: %s", e)

        if search_type in ["general", "security"]:
            try:
                k8s_security = await security_client.search_kubernetes_security(
                    query=query,
                    limit=limit,
                )
                results["security"].extend(k8s_security)
            except Exception as e:
                logger.warning("Failed to search Kubernetes security: %s", e)


        results["total"] = len(results["web"]) + len(results["security"])

        logger.info("Web search completed: %d total results", results["total"])

        return results

