"""Best practices tool - search DevOps best practices."""

import logging
from typing import Any

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.vector_search import VectorSearch
from wistx_mcp.tools.lib.auth_context import get_auth_context
from wistx_mcp.config import settings

logger = logging.getLogger(__name__)


async def search_best_practices(
    query: str,
    category: str | None = None,
    limit: int = 10,
) -> dict[str, Any]:
    """Search DevOps best practices.

    Args:
        query: Search query
        category: Filter by category
        limit: Maximum number of results

    Returns:
        Dictionary with best practices

    Raises:
        RuntimeError: If quota is exceeded
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

        domains = ["devops", "architecture", "infrastructure"]
        content_types = ["best_practice", "guide", "pattern"]

        results = await vector_search.search_knowledge_articles(
            query=query,
            domains=domains,
            content_types=content_types,
            include_global=True,
            limit=limit,
        )

        if category:
            filtered_results = []
            for result in results:
                tags = result.get("tags", [])
                categories_list = result.get("categories", [])
                if category.lower() in [t.lower() for t in tags] or category.lower() in [c.lower() for c in categories_list]:
                    filtered_results.append(result)
            results = filtered_results

        return {
            "practices": results,
            "total": len(results),
        }

