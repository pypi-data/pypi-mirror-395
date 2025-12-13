"""Template discovery service for auto-registering templates from curated GitHub repositories."""

import logging
from typing import Any

import httpx

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.template_repository import TemplateRepositoryManager
from wistx_mcp.models.template import TemplateSource

logger = logging.getLogger(__name__)


class TemplateDiscoveryService:
    """Service for discovering and auto-registering templates from GitHub."""

    def __init__(self, mongodb_client: MongoDBClient):
        """Initialize template discovery service.

        Args:
            mongodb_client: MongoDB client instance
        """
        self.mongodb_client = mongodb_client
        self.template_manager = TemplateRepositoryManager(mongodb_client)
        self.curated_org = "wistx-templates"

    async def discover_and_register_all(self) -> dict[str, Any]:
        """Discover templates from curated GitHub organization and register them.

        Returns:
            Dictionary with discovery results
        """
        results = {
            "discovered": 0,
            "registered": 0,
            "updated": 0,
            "failed": 0,
            "errors": [],
        }

        try:
            repos = await self._list_org_repositories(self.curated_org)

            for repo in repos:
                try:
                    if await self._is_template_repository(repo):
                        result = await self._register_template_from_repo(repo)
                        if result["action"] == "registered":
                            results["registered"] += 1
                        elif result["action"] == "updated":
                            results["updated"] += 1
                        results["discovered"] += 1
                except Exception as e:
                    logger.error("Failed to process repository %s: %s", repo["full_name"], e)
                    results["failed"] += 1
                    results["errors"].append({"repo": repo["full_name"], "error": str(e)})

        except Exception as e:
            logger.error("Failed to discover templates: %s", e, exc_info=True)
            results["errors"].append({"error": str(e)})

        return results

    async def _list_org_repositories(self, org: str) -> list[dict[str, Any]]:
        """List repositories in GitHub organization.

        Args:
            org: GitHub organization name

        Returns:
            List of repository dictionaries

        Raises:
            ValueError: If API call fails
        """
        api_url = f"https://api.github.com/orgs/{org}/repos"
        params = {"type": "public", "per_page": 100}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(api_url, params=params, timeout=30.0)
                response.raise_for_status()
                repos = response.json()

                return [
                    {
                        "name": repo["name"],
                        "full_name": repo["full_name"],
                        "url": repo["html_url"],
                        "description": repo.get("description", ""),
                        "default_branch": repo.get("default_branch", "main"),
                    }
                    for repo in repos
                ]

        except httpx.HTTPStatusError as e:
            raise ValueError(f"Failed to list repositories: {e.response.status_code}")
        except Exception as e:
            raise ValueError(f"Failed to list repositories: {e}")

    async def _is_template_repository(self, repo: dict[str, Any]) -> bool:
        """Check if repository is a template repository.

        Args:
            repo: Repository dictionary

        Returns:
            True if repository is a template repository
        """
        try:
            template_structure = await self.template_manager.fetch_from_github(
                repo["url"],
                path="template.json",
                ref=repo["default_branch"],
            )
            return bool(template_structure.get("structure"))
        except Exception:
            return False

    async def _register_template_from_repo(self, repo: dict[str, Any]) -> dict[str, Any]:
        """Register template from GitHub repository.

        Args:
            repo: Repository dictionary

        Returns:
            Dictionary with registration result
        """
        try:
            template_structure = await self.template_manager.fetch_from_github(
                repo["url"],
                path="template.json",
                ref=repo["default_branch"],
            )

            metadata = template_structure.get("metadata", {})
            project_type = metadata.get("project_type", "unknown")
            architecture_type = metadata.get("architecture_type")
            cloud_provider = metadata.get("cloud_provider")

            template_id = self._generate_template_id(
                name=repo["name"],
                project_type=project_type,
                architecture_type=architecture_type,
                cloud_provider=cloud_provider,
            )

            existing_template = await self.template_manager.fetch_template(template_id)

            if existing_template:
                existing_version = existing_template.get("version", "1.0.0")
                new_version = metadata.get("version", "1.0.0")

                from wistx_mcp.tools.lib.template_version_manager import TemplateVersionManager

                if TemplateVersionManager.is_newer_version(new_version, existing_version):
                    await self.template_manager.register_template(
                        name=metadata.get("name", repo["name"]),
                        structure=template_structure.get("structure", {}),
                        project_type=project_type,
                        architecture_type=architecture_type,
                        cloud_provider=cloud_provider,
                        source_type=TemplateSource.GITHUB,
                        source_url=repo["url"],
                        version=new_version,
                        tags=metadata.get("tags", []),
                        visibility="public",
                        changelog=metadata.get("changelog", []),
                    )
                    return {"action": "updated", "template_id": template_id}
                else:
                    return {"action": "skipped", "template_id": template_id, "reason": "not_newer"}

            await self.template_manager.register_template(
                name=metadata.get("name", repo["name"]),
                structure=template_structure.get("structure", {}),
                project_type=project_type,
                architecture_type=architecture_type,
                cloud_provider=cloud_provider,
                source_type=TemplateSource.GITHUB,
                source_url=repo["url"],
                version=metadata.get("version", "1.0.0"),
                tags=metadata.get("tags", []),
                visibility="public",
                changelog=metadata.get("changelog", []),
            )

            return {"action": "registered", "template_id": template_id}

        except ValueError as e:
            if "not found" in str(e).lower():
                existing_template = None
            else:
                raise
        except Exception as e:
            logger.error("Failed to register template from repo %s: %s", repo["url"], e)
            raise

    def _generate_template_id(
        self,
        name: str,
        project_type: str,
        architecture_type: str | None = None,
        cloud_provider: str | None = None,
    ) -> str:
        """Generate template ID from components.

        Args:
            name: Template name
            project_type: Project type
            architecture_type: Architecture type
            cloud_provider: Cloud provider

        Returns:
            Template ID string
        """
        parts = [project_type]
        if architecture_type:
            parts.append(architecture_type)
        if cloud_provider:
            parts.append(cloud_provider)

        template_id = "-".join(parts).lower().replace("_", "-")
        return template_id

