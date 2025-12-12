"""Compliance tool - get compliance requirements for infrastructure resources."""

import logging
from typing import Any

from wistx_mcp.config import settings
from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.package_search_service import PackageSearchService
from wistx_mcp.tools.lib.vector_search import VectorSearch
from wistx_mcp.tools.lib.auth_context import get_auth_context
from wistx_mcp.tools.lib.api_client import WISTXAPIClient

logger = logging.getLogger(__name__)


async def get_compliance_requirements(
    resource_type: str,
    standards: list[str] | None = None,
    severity: str | None = None,
    include_package_examples: bool = True,
    api_key: str | None = None,
) -> dict[str, Any]:
    """Get compliance requirements for a resource.

    Args:
        resource_type: AWS resource type (e.g., RDS, S3, EC2)
        standards: Compliance standards to check (e.g., ["PCI-DSS", "HIPAA"])
        severity: Filter by severity (CRITICAL, HIGH, MEDIUM, LOW)
        include_package_examples: Include package examples that implement compliance
        api_key: Optional API key for package search

    Returns:
        Dictionary with compliance controls, summary, and optional package examples

    Raises:
        RuntimeError: If quota is exceeded
        ValueError: If resource type is invalid
    """
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

    async with MongoDBClient() as client:
        vector_search = VectorSearch(client, gemini_api_key=settings.gemini_api_key)
        
        results = []
        
        if vector_search.is_available():
            query = f"{resource_type} compliance"
            if standards:
                query += " " + " ".join(standards)

            try:
                results = await vector_search.search_compliance(
                    query=query,
                    standards=standards,
                    severity=severity,
                    limit=50000,
                )
            except Exception as e:
                logger.warning("Vector search failed, falling back to REST API: %s", e)
                vector_search = None
        
        if not results and not vector_search:
            logger.info("Vector search not available, using REST API backend")
            api_key_value = api_key or (auth_ctx._get_api_key() if auth_ctx else None) or settings.api_key
            api_client = WISTXAPIClient(api_key=api_key_value)
            try:
                api_response = await api_client.get_compliance_requirements(
                    resource_types=[resource_type],
                    standards=standards,
                    severity=severity,
                    api_key=api_key_value,
                )
                results = api_response.get("controls", [])
            except Exception as e:
                logger.error("Failed to fetch compliance requirements from REST API: %s", e)
                raise RuntimeError(f"Failed to fetch compliance requirements: {e}") from e
        
        if len(results) > 10000:
            logger.warning(
                "Large compliance result set returned: %d controls. Consider using filters to narrow results.",
                len(results)
            )

        response = {
            "controls": results,
            "summary": f"Found {len(results)} compliance controls for {resource_type}",
            "total": len(results),
        }

        if include_package_examples and api_key:
            try:
                package_search_service = PackageSearchService(client)
                package_query = f"{resource_type} compliance {resource_type.lower()}"
                if standards:
                    package_query += " " + " ".join(standards)

                package_results = await package_search_service.semantic_search(
                    query=package_query,
                    domain="compliance",
                    limit=5,
                )

                if package_results:
                    response["package_examples"] = [
                        {
                            "package_id": p.get("package_id"),
                            "name": p.get("name"),
                            "registry": p.get("registry"),
                            "description": p.get("description", "")[:200],
                            "github_url": p.get("github_url"),
                        }
                        for p in package_results
                    ]
                    response["summary"] += f" | Found {len(package_results)} relevant packages"
            except Exception as e:
                logger.warning("Failed to fetch package examples for compliance: %s", e)

        return response

