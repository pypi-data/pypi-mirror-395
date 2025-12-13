"""Simplified script for curating templates - discover, extract, store directly in MongoDB."""

import asyncio
import logging
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from wistx_mcp.services.template_curation import TemplateCurationService
from wistx_mcp.tools.lib.mongodb_client import MongoDBClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


SEARCH_QUERIES = [
    "kubernetes microservices stars:>500 language:yaml",
    "kubernetes production-ready stars:>500",
    "k8s best-practices stars:>500",
    "terraform aws production stars:>500 language:hcl",
    "terraform modules best-practices stars:>500",
    "devops ci-cd github-actions stars:>500",
    "devops docker-compose production stars:>500",
    "platform engineering kubernetes stars:>500",
    "service mesh istio stars:>500",
    "api gateway kubernetes stars:>500",
]


async def curate_templates(
    github_token: str | None = None,
    max_templates: int = 1000,
    min_quality_score: float = 70.0,
):
    """Curate templates from GitHub and store directly in MongoDB.

    Args:
        github_token: GitHub personal access token (optional, increases rate limits)
        max_templates: Maximum number of templates to process
        min_quality_score: Minimum quality score threshold
    """
    logger.info("Starting template curation process...")
    logger.info("This will discover, extract, and store templates directly in MongoDB")

    mongodb_client = MongoDBClient()
    await mongodb_client.connect()

    curation_service = TemplateCurationService(
        mongodb_client=mongodb_client,
        github_token=github_token,
    )

    results = await curation_service.curate_templates(
        queries=SEARCH_QUERIES,
        min_stars=500,
        min_quality_score=min_quality_score,
        max_templates=max_templates,
    )

    logger.info("=" * 60)
    logger.info("CURATION RESULTS")
    logger.info("=" * 60)
    logger.info("Discovered: %d repositories", results["discovered"])
    logger.info("Processed: %d repositories", results["processed"])
    logger.info("Registered: %d templates", results["registered"])
    logger.info("Failed: %d repositories", results["failed"])
    logger.info("Skipped (already exist): %d repositories", results["skipped"])

    if results["errors"]:
        logger.warning("Errors encountered:")
        for error in results["errors"][:10]:
            logger.warning("  - %s: %s", error.get("repo", "unknown"), error.get("error", "unknown"))

    await mongodb_client.close()


if __name__ == "__main__":
    github_token = os.getenv("GITHUB_TOKEN")

    if github_token:
        logger.info("Using GitHub token for increased rate limits")
    else:
        logger.warning("No GITHUB_TOKEN found - using unauthenticated requests (lower rate limits)")

    asyncio.run(
        curate_templates(
            github_token=github_token,
            max_templates=1000,
            min_quality_score=70.0,
        )
    )

