"""Main script for curating and forking high-quality templates from GitHub."""

import asyncio
import logging
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from wistx_mcp.services.repository_discovery import RepositoryDiscoveryService
from wistx_mcp.services.repository_forking import RepositoryForkingService
from wistx_mcp.services.template_standardization import TemplateStandardizationService
from wistx_mcp.services.template_validation import TemplateValidationService
from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.template_repository import TemplateRepositoryManager
from wistx_mcp.models.template import TemplateSource

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


async def curate_and_fork_templates(
    github_token: str,
    max_templates: int = 1000,
    min_quality_score: float = 70.0,
):
    """Main curation and forking workflow.

    Args:
        github_token: GitHub personal access token
        max_templates: Maximum number of templates to fork
        min_quality_score: Minimum quality score threshold
    """
    logger.info("Starting template curation and forking process...")

    discovery = RepositoryDiscoveryService(github_token=github_token)
    forking = RepositoryForkingService(github_token=github_token)
    standardization = TemplateStandardizationService(github_token=github_token)
    validation = TemplateValidationService()

    logger.info("Step 1: Discovering high-quality repositories...")
    candidates = await discovery.discover_repositories(
        queries=SEARCH_QUERIES,
        min_stars=500,
        min_quality_score=min_quality_score,
        max_results=max_templates * 2,
    )

    logger.info("Found %d candidate repositories", len(candidates))

    mongodb_client = MongoDBClient()
    await mongodb_client.connect()
    template_manager = TemplateRepositoryManager(mongodb_client)

    registered_count = 0
    failed_count = 0

    for i, repo in enumerate(candidates[:max_templates], 1):
        try:
            logger.info(
                "[%d/%d] Processing: %s (Score: %.1f)",
                i,
                min(len(candidates), max_templates),
                repo["full_name"],
                repo.get("quality_score", 0),
            )

            repo_url = repo["html_url"]

            fork_result = await forking.fork_to_organization(repo_url)

            if fork_result.get("already_exists"):
                logger.info("Repository already forked, skipping standardization")
                continue

            fork_url = fork_result["fork_url"]

            template_data = await standardization.add_template_metadata(
                repo_url=fork_url,
                original_repo=repo,
                template_metadata={
                    "forked_at": fork_result.get("forked_at"),
                },
                github_token=github_token,
            )

            validation_result = await validation.validate_template(
                repo_path=fork_url,
                structure=template_data["structure"],
            )

            if validation_result["valid"]:
                metadata = template_data["metadata"]

                template = await template_manager.register_template(
                    name=metadata["name"],
                    structure=template_data["structure"],
                    project_type=metadata.get("project_type", "unknown"),
                    architecture_type=metadata.get("architecture_type"),
                    cloud_provider=metadata.get("cloud_provider"),
                    source_type=TemplateSource.GITHUB,
                    source_url=fork_url,
                    version=metadata.get("version", "1.0.0"),
                    tags=metadata.get("tags", []),
                    visibility="public",
                    changelog=metadata.get("changelog", []),
                )

                logger.info(
                    "✅ Registered template: %s (ID: %s, Score: %.1f)",
                    template.name,
                    template.template_id,
                    validation_result["score"],
                )
                registered_count += 1
            else:
                logger.warning(
                    "Template validation failed: %s (Score: %.1f)",
                    repo["full_name"],
                    validation_result["score"],
                )
                failed_count += 1

        except Exception as e:
            logger.error("Failed to process repository %s: %s", repo.get("full_name"), e, exc_info=True)
            failed_count += 1

    logger.info(
        "Curation complete: %d registered, %d failed",
        registered_count,
        failed_count,
    )

    await mongodb_client.close()


if __name__ == "__main__":
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        logger.error("GITHUB_TOKEN environment variable is required")
        sys.exit(1)

    asyncio.run(
        curate_and_fork_templates(
            github_token=github_token,
            max_templates=1000,
            min_quality_score=70.0,
        )
    )

