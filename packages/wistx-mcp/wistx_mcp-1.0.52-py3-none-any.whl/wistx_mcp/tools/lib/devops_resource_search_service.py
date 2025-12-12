"""Unified DevOps resource search service."""

import logging
from typing import Any

from wistx_mcp.tools.lib.devops_resource_types import (
    DEVOPS_SERVICES,
    DEVOPS_TOOLS,
    get_services_by_category,
    get_tools_by_category,
)
from wistx_mcp.tools.lib.package_search_service import PackageSearchService
from wistx_mcp.config import settings

logger = logging.getLogger(__name__)


class DevOpsResourceSearchService:
    """Unified search across all DevOps resources."""

    def __init__(self, mongodb_client):
        """Initialize search service.

        Args:
            mongodb_client: MongoDB client instance
        """
        self.mongodb_client = mongodb_client
        self.package_search_service = PackageSearchService(mongodb_client)

    async def search(
        self,
        query: str,
        resource_types: list[str] | None = None,
        registry: str | None = None,
        domain: str | None = None,
        category: str | None = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        """Search across all DevOps resources.

        Args:
            query: Search query
            resource_types: Filter by resource types (package, tool, service, documentation, template, all)
            registry: Filter by registry (for packages)
            domain: Filter by domain
            category: Filter by category
            limit: Maximum results per resource type

        Returns:
            Dictionary with unified results:
            - packages: List of packages
            - tools: List of CLI tools
            - services: List of services/integrations
            - documentation: List of documentation
            - templates: List of templates
            - total: Total results across all types
        """
        if not resource_types:
            resource_types = ["all"]

        if "all" in resource_types:
            resource_types = ["package", "tool", "service", "documentation"]

        results = {
            "packages": [],
            "tools": [],
            "services": [],
            "documentation": [],
            "templates": [],
        }

        if "package" in resource_types:
            try:
                packages = await self.package_search_service.semantic_search(
                    query=query,
                    registry=registry,
                    domain=domain,
                    category=category,
                    limit=limit,
                )
                results["packages"] = packages
                logger.info("Found %d packages", len(packages))
            except Exception as e:
                logger.warning("Package search failed: %s", e)

        if "tool" in resource_types:
            try:
                tools = await self._search_tools(query, domain, category, limit)
                results["tools"] = tools
                logger.info("Found %d tools", len(tools))
            except Exception as e:
                logger.warning("Tool search failed: %s", e)

        if "service" in resource_types:
            try:
                services = await self._search_services(query, domain, category, limit)
                results["services"] = services
                logger.info("Found %d services", len(services))
            except Exception as e:
                logger.warning("Service search failed: %s", e)

        if "documentation" in resource_types:
            try:
                docs = await self._search_documentation(query, domain, category, limit)
                results["documentation"] = docs
                logger.info("Found %d documentation items", len(docs))
            except Exception as e:
                logger.warning("Documentation search failed: %s", e)

        unified_results = self._rank_unified_results(results, query)

        return {
            **results,
            "unified_results": unified_results,
            "total": sum(len(v) for v in results.values()),
        }

    async def _search_tools(
        self,
        query: str,
        domain: str | None,
        category: str | None,
        limit: int,
    ) -> list[dict[str, Any]]:
        """Search CLI tools.

        Args:
            query: Search query
            domain: Optional domain filter
            category: Optional category filter
            limit: Maximum results

        Returns:
            List of matching tools
        """
        query_lower = query.lower()
        matched_tools = []

        tools_to_search = get_tools_by_category(category) if category else DEVOPS_TOOLS

        for tool in tools_to_search:
            score = self._calculate_match_score(tool, query_lower)
            if score > 0.3:
                matched_tools.append({
                    "resource_type": "tool",
                    "name": tool.name,
                    "description": tool.description,
                    "category": tool.category,
                    "install_command": tool.install_command,
                    "official_url": tool.official_url,
                    "github_url": tool.github_url,
                    "match_score": score,
                    "popularity_score": tool.popularity_score,
                })

        matched_tools.sort(
            key=lambda x: (x["match_score"] * 0.7 + x["popularity_score"] * 0.3),
            reverse=True,
        )

        return matched_tools[:limit]

    async def _search_services(
        self,
        query: str,
        domain: str | None,
        category: str | None,
        limit: int,
    ) -> list[dict[str, Any]]:
        """Search services/integrations.

        Args:
            query: Search query
            domain: Optional domain filter
            category: Optional category filter
            limit: Maximum results

        Returns:
            List of matching services
        """
        query_lower = query.lower()
        matched_services = []

        services_to_search = (
            get_services_by_category(category) if category else DEVOPS_SERVICES
        )

        for service in services_to_search:
            score = self._calculate_match_score(service, query_lower)
            if score > 0.3:
                matched_services.append({
                    "resource_type": "service",
                    "name": service.name,
                    "description": service.description,
                    "category": service.category,
                    "official_url": service.official_url,
                    "integration_type": service.integration_type,
                    "match_score": score,
                    "popularity_score": service.popularity_score,
                })

        matched_services.sort(
            key=lambda x: (x["match_score"] * 0.7 + x["popularity_score"] * 0.3),
            reverse=True,
        )

        return matched_services[:limit]

    async def _search_documentation(
        self,
        query: str,
        domain: str | None,
        category: str | None,
        limit: int,
    ) -> list[dict[str, Any]]:
        """Search documentation (integrate with knowledge base).

        Args:
            query: Search query
            domain: Optional domain filter
            category: Optional category filter
            limit: Maximum results

        Returns:
            List of matching documentation
        """
        try:
            from wistx_mcp.tools.lib.vector_search import VectorSearch

            vector_search = VectorSearch(
                self.mongodb_client,
                gemini_api_key=settings.gemini_api_key,
                pinecone_api_key=settings.pinecone_api_key,
                pinecone_index_name=settings.pinecone_index_name,
            )

            docs = await vector_search.search_knowledge_articles(
                query=query,
                domains=[domain] if domain else None,
                content_types=["guide", "reference", "best_practice"],
                limit=limit,
            )

            return [
                {
                    "resource_type": "documentation",
                    "title": doc.get("title", ""),
                    "summary": doc.get("summary", ""),
                    "url": doc.get("url"),
                    "similarity_score": doc.get("similarity_score", 0.0),
                }
                for doc in docs
            ]
        except Exception as e:
            logger.warning("Documentation search failed: %s", e)
            return []

    def _calculate_match_score(self, resource: Any, query: str) -> float:
        """Calculate how well resource matches query.

        Args:
            resource: DevOpsTool or DevOpsService object
            query: Search query

        Returns:
            Match score between 0.0 and 1.0
        """
        name = resource.name.lower()
        description = resource.description.lower()
        keywords = " ".join(resource.keywords).lower() if resource.keywords else ""

        query_lower = query.lower()
        query_words = set(query_lower.split())

        name_words = set(name.split())
        desc_words = set(description.split())
        keyword_words = set(keywords.split()) if keywords else set()

        if query_lower in name:
            return 1.0

        name_overlap = len(query_words & name_words) / max(len(query_words), 1)
        desc_overlap = len(query_words & desc_words) / max(len(query_words), 1)
        keyword_overlap = (
            len(query_words & keyword_words) / max(len(query_words), 1)
            if keyword_words
            else 0.0
        )

        score = (name_overlap * 0.5 + desc_overlap * 0.3 + keyword_overlap * 0.2)
        return min(1.0, score)

    def _rank_unified_results(
        self,
        results: dict[str, Any],
        query: str,
    ) -> list[dict[str, Any]]:
        """Rank results across all resource types.

        Args:
            results: Dictionary with results by type
            query: Original search query

        Returns:
            Unified ranked list of results
        """
        unified = []

        for resource_type, items in results.items():
            for item in items:
                normalized_score = self._normalize_score(item, resource_type)
                unified.append({
                    **item,
                    "normalized_score": normalized_score,
                })

        unified.sort(key=lambda x: x.get("normalized_score", 0), reverse=True)

        return unified

    def _normalize_score(self, item: dict[str, Any], resource_type: str) -> float:
        """Normalize scores across different resource types.

        Args:
            item: Result item dictionary
            resource_type: Type of resource

        Returns:
            Normalized score between 0.0 and 1.0
        """
        if resource_type == "package":
            return item.get("final_score", item.get("vector_score", item.get("similarity_score", 0.0)))
        elif resource_type == "tool":
            return (
                item.get("match_score", 0.0) * 0.7
                + item.get("popularity_score", 0.0) * 0.3
            )
        elif resource_type == "service":
            return (
                item.get("match_score", 0.0) * 0.7
                + item.get("popularity_score", 0.0) * 0.3
            )
        elif resource_type == "documentation":
            return item.get("similarity_score", 0.0)
        else:
            return 0.5

