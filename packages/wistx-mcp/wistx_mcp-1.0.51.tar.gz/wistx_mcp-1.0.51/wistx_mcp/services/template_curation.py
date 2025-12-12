"""Simplified template curation service - discover, extract, and store templates directly."""

import logging
from datetime import datetime
from typing import Any

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.template_repository import TemplateRepositoryManager
from wistx_mcp.models.template import TemplateSource
from wistx_mcp.services.repository_discovery import RepositoryDiscoveryService
from wistx_mcp.services.template_standardization import TemplateStandardizationService
from wistx_mcp.services.template_validation import TemplateValidationService

logger = logging.getLogger(__name__)


class TemplateCurationService:
    """Simplified service for curating templates - discover, extract, store."""

    def __init__(
        self,
        mongodb_client: MongoDBClient,
        github_token: str | None = None,
    ):
        """Initialize template curation service.

        Args:
            mongodb_client: MongoDB client instance
            github_token: GitHub token for API access (optional, increases rate limits)
        """
        self.mongodb_client = mongodb_client
        self.github_token = github_token
        self.discovery = RepositoryDiscoveryService(github_token=github_token)
        self.standardization = TemplateStandardizationService(github_token=github_token)
        self.validation = TemplateValidationService()
        self.template_manager = TemplateRepositoryManager(mongodb_client)

    async def curate_templates(
        self,
        queries: list[str],
        min_stars: int = 500,
        min_quality_score: float = 70.0,
        max_templates: int = 1000,
    ) -> dict[str, Any]:
        """Curate templates from GitHub - discover, extract, validate, store.

        Args:
            queries: List of GitHub search queries
            min_stars: Minimum star count
            min_quality_score: Minimum quality score (0-100)
            max_templates: Maximum number of templates to process

        Returns:
            Dictionary with curation results
        """
        results = {
            "discovered": 0,
            "processed": 0,
            "registered": 0,
            "failed": 0,
            "skipped": 0,
            "errors": [],
        }

        logger.info("Step 1: Discovering high-quality repositories...")
        candidates = await self.discovery.discover_repositories(
            queries=queries,
            min_stars=min_stars,
            min_quality_score=min_quality_score,
            max_results=max_templates * 2,
        )

        results["discovered"] = len(candidates)
        logger.info("Found %d candidate repositories", len(candidates))

        for i, repo in enumerate(candidates[:max_templates], 1):
            try:
                repo_url = repo["html_url"]
                logger.info(
                    "[%d/%d] Processing: %s (Score: %.1f)",
                    i,
                    min(len(candidates), max_templates),
                    repo["full_name"],
                    repo.get("quality_score", 0),
                )

                results["processed"] += 1

                existing_template = await self._check_existing_template(repo_url)
                if existing_template:
                    logger.info("Template already exists: %s", repo_url)
                    results["skipped"] += 1
                    continue

                template_data = await self.standardization.add_template_metadata(
                    repo_url=repo_url,
                    original_repo=repo,
                    template_metadata={
                        "curated_at": datetime.now().isoformat(),
                    },
                    github_token=self.github_token,
                )

                validation_result = await self.validation.validate_template(
                    repo_path=repo_url,
                    structure=template_data["structure"],
                )

                if validation_result["valid"]:
                    metadata = template_data["metadata"]

                    template = await self.template_manager.register_template(
                        name=metadata["name"],
                        structure=template_data["structure"],
                        project_type=metadata.get("project_type", "unknown"),
                        architecture_type=metadata.get("architecture_type"),
                        cloud_provider=metadata.get("cloud_provider"),
                        source_type=TemplateSource.GITHUB,
                        source_url=repo_url,
                        version=metadata.get("version", "1.0.0"),
                        tags=metadata.get("tags", []),
                        visibility="public",
                        changelog=metadata.get("changelog", []),
                        quality_score=int(validation_result["score"]),
                    )

                    logger.info(
                        "✅ Registered template: %s (ID: %s, Score: %.1f)",
                        template.name,
                        template.template_id,
                        validation_result["score"],
                    )
                    results["registered"] += 1
                else:
                    logger.warning(
                        "Template validation failed: %s (Score: %.1f)",
                        repo["full_name"],
                        validation_result["score"],
                    )
                    results["failed"] += 1

            except Exception as e:
                logger.error(
                    "Failed to process repository %s: %s",
                    repo.get("full_name"),
                    e,
                    exc_info=True,
                )
                results["failed"] += 1
                results["errors"].append({"repo": repo.get("full_name"), "error": str(e)})

        logger.info(
            "Curation complete: %d discovered, %d processed, %d registered, %d failed, %d skipped",
            results["discovered"],
            results["processed"],
            results["registered"],
            results["failed"],
            results["skipped"],
        )

        return results

    async def _check_existing_template(self, repo_url: str) -> dict[str, Any] | None:
        """Check if template already exists in MongoDB.

        Args:
            repo_url: Repository URL

        Returns:
            Existing template dictionary or None
        """
        db = await self.mongodb_client.get_database()
        collection = db["template_registry"]

        existing = await collection.find_one({"source_url": repo_url, "is_latest": True})
        return existing

    async def update_existing_templates(self) -> dict[str, Any]:
        """Update existing templates from their source repositories.

        Returns:
            Dictionary with update results
        """
        results = {
            "checked": 0,
            "updated": 0,
            "no_changes": 0,
            "failed": 0,
            "errors": [],
        }

        db = await self.mongodb_client.get_database()
        collection = db["template_registry"]

        cursor = collection.find({"source_type": TemplateSource.GITHUB.value, "is_latest": True})
        async for template_doc in cursor:
            try:
                results["checked"] += 1
                source_url = template_doc.get("source_url")
                if not source_url:
                    continue

                repo_details = await self.discovery.get_repository_details(source_url)
                current_version = template_doc.get("version", "1.0.0")

                template_data = await self.standardization.add_template_metadata(
                    repo_url=source_url,
                    original_repo=repo_details,
                    github_token=self.github_token,
                )

                new_version = template_data["metadata"].get("version", "1.0.0")

                from wistx_mcp.tools.lib.template_version_manager import TemplateVersionManager

                if TemplateVersionManager.is_newer_version(new_version, current_version):
                    validation_result = await self.validation.validate_template(
                        repo_path=source_url,
                        structure=template_data["structure"],
                    )

                    if validation_result["valid"]:
                        metadata = template_data["metadata"]
                        await self.template_manager.register_template(
                            name=metadata["name"],
                            structure=template_data["structure"],
                            project_type=metadata.get("project_type", "unknown"),
                            architecture_type=metadata.get("architecture_type"),
                            cloud_provider=metadata.get("cloud_provider"),
                            source_type=TemplateSource.GITHUB,
                            source_url=source_url,
                            version=new_version,
                            tags=metadata.get("tags", []),
                            visibility="public",
                            changelog=metadata.get("changelog", []),
                            quality_score=int(validation_result["score"]),
                        )
                        results["updated"] += 1
                        logger.info("Updated template: %s (v%s -> v%s)", source_url, current_version, new_version)
                    else:
                        results["no_changes"] += 1
                else:
                    results["no_changes"] += 1

            except Exception as e:
                logger.error("Failed to update template %s: %s", template_doc.get("template_id"), e)
                results["failed"] += 1
                results["errors"].append({"template_id": template_doc.get("template_id"), "error": str(e)})

        return results

