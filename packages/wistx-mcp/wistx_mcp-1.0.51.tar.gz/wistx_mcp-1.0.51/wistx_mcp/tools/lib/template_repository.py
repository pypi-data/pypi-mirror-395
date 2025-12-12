"""Template repository manager for external templates."""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx
from semantic_version import Version

from wistx_mcp.models.template import TemplateMetadata, TemplateSource
from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.template_version_manager import TemplateVersionManager

logger = logging.getLogger(__name__)


class TemplateRepositoryManager:
    """Manages template repositories and versioning."""

    def __init__(self, mongodb_client: MongoDBClient):
        """Initialize template repository manager.

        Args:
            mongodb_client: MongoDB client instance
        """
        self.mongodb_client = mongodb_client
        self.collection_name = "template_registry"

    async def register_template(
        self,
        name: str,
        structure: dict[str, Any],
        project_type: str,
        source_type: TemplateSource,
        source_url: str | None = None,
        version: str = "1.0.0",
        architecture_type: str | None = None,
        cloud_provider: str | None = None,
        variables: dict[str, Any] | None = None,
        prompts: list[dict[str, str]] | None = None,
        author: str | None = None,
        tags: list[str] | None = None,
        user_id: str | None = None,
        organization_id: str | None = None,
        visibility: str = "public",
        changelog: list[str] | None = None,
    ) -> TemplateMetadata:
        """Register a template.

        Args:
            name: Template name
            structure: Template file structure
            project_type: Project type
            source_type: Source type (github or user)
            source_url: Source URL (for GitHub) or None (for user-provided)
            version: Template version (default: 1.0.0)
            architecture_type: Architecture pattern
            cloud_provider: Cloud provider
            variables: Template variables
            prompts: User prompts
            author: Template author
            tags: Template tags
            user_id: Owner user ID
            organization_id: Owner organization ID
            visibility: Visibility (public, private, organization)

        Returns:
            TemplateMetadata instance

        Raises:
            ValueError: If invalid parameters
        """
        TemplateVersionManager.parse_version(version)

        template_id = self._generate_template_id(
            name=name,
            project_type=project_type,
            architecture_type=architecture_type,
            cloud_provider=cloud_provider,
        )

        previous_version_id = None
        is_latest = True

        existing_versions = await self._get_template_versions(template_id)
        if existing_versions:
            latest_existing = TemplateVersionManager.get_latest_version(existing_versions)
            if TemplateVersionManager.is_newer_version(version, latest_existing):
                previous_version_id = f"{template_id}-{latest_existing}"
                is_latest = True
                await self._mark_previous_versions_not_latest(template_id)
            else:
                is_latest = False
                if TemplateVersionManager.compare_versions(version, latest_existing) == 0:
                    raise ValueError(
                        f"Version {version} already exists for template {template_id}. "
                        "Use a different version or update the existing one."
                    )

        if changelog:
            validation = TemplateVersionManager.validate_changelog(changelog)
            if not validation["valid"]:
                raise ValueError(f"Invalid changelog: {validation['errors']}")

        template = TemplateMetadata(
            template_id=template_id,
            name=name,
            description=f"Template for {project_type} projects",
            version=version,
            source_type=source_type,
            source_url=source_url,
            source_ref=None,
            project_type=project_type,
            architecture_type=architecture_type,
            cloud_provider=cloud_provider,
            structure=structure,
            variables=variables or {},
            prompts=prompts or [],
            author=author,
            tags=tags or [],
            quality_score=0,
            usage_count=0,
            is_latest=is_latest,
            previous_version=previous_version_id,
            changelog=changelog or [],
            visibility=visibility,
            user_id=user_id,
            organization_id=organization_id,
            published_at=datetime.utcnow(),
        )

        await self._save_template(template)

        from wistx_mcp.tools.lib.template_marketplace import TemplateMarketplace

        marketplace = TemplateMarketplace(self.mongodb_client)
        await marketplace._update_analytics(template_id)

        logger.info(
            "Registered template: id=%s, name=%s, version=%s, source=%s",
            template_id,
            name,
            version,
            source_type.value,
        )

        return template

    async def fetch_template(
        self,
        template_id: str,
        version: str | None = None,
    ) -> dict[str, Any]:
        """Fetch template from repository.

        Args:
            template_id: Template identifier
            version: Template version (None for latest)

        Returns:
            Template dictionary

        Raises:
            ValueError: If template not found
        """
        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available")
            return None
        collection = db[self.collection_name]

        query: dict[str, Any] = {"template_id": template_id}
        if version:
            query["version"] = version
        else:
            query["is_latest"] = True

        template_doc = await collection.find_one(query)

        if not template_doc:
            raise ValueError(f"Template not found: {template_id} (version: {version or 'latest'})")

        template_doc.pop("_id", None)
        return template_doc

    async def list_templates(
        self,
        project_type: str | None = None,
        cloud_provider: str | None = None,
        architecture_type: str | None = None,
        tags: list[str] | None = None,
        visibility: str = "public",
        user_id: str | None = None,
        limit: int = 50,
    ) -> list[TemplateMetadata]:
        """List available templates.

        Args:
            project_type: Filter by project type
            cloud_provider: Filter by cloud provider
            architecture_type: Filter by architecture type
            tags: Filter by tags
            visibility: Filter by visibility
            user_id: Filter by user ID
            limit: Maximum number of results

        Returns:
            List of TemplateMetadata instances
        """
        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available")
            return None
        collection = db[self.collection_name]

        query: dict[str, Any] = {"is_latest": True}

        if project_type:
            query["project_type"] = project_type
        if cloud_provider:
            query["cloud_provider"] = cloud_provider
        if architecture_type:
            query["architecture_type"] = architecture_type
        if tags:
            query["tags"] = {"$in": tags}
        if visibility:
            query["visibility"] = visibility
        if user_id:
            query["user_id"] = user_id

        cursor = collection.find(query).sort("usage_count", -1).limit(limit)
        templates = []

        async for doc in cursor:
            doc.pop("_id", None)
            try:
                template = TemplateMetadata(**doc)
                templates.append(template)
            except Exception as e:
                logger.warning("Failed to parse template %s: %s", doc.get("template_id"), e)

        return templates

    async def fetch_from_github(
        self,
        repo_url: str,
        path: str = "template.json",
        ref: str | None = None,
    ) -> dict[str, Any]:
        """Fetch template from GitHub repository.

        Args:
            repo_url: GitHub repository URL (e.g., https://github.com/user/repo)
            path: Path to template file in repository
            ref: Git reference (branch/tag/commit, default: main)

        Returns:
            Template dictionary

        Raises:
            ValueError: If invalid URL or fetch fails
        """
        parsed_url = urlparse(repo_url)
        if parsed_url.netloc not in ["github.com", "www.github.com"]:
            raise ValueError(f"Invalid GitHub URL: {repo_url}")

        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) < 2:
            raise ValueError(f"Invalid GitHub repository URL: {repo_url}")

        owner = path_parts[0]
        repo = path_parts[1].replace(".git", "")

        if not ref:
            ref = "main"

        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        if ref != "main":
            api_url += f"?ref={ref}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(api_url, timeout=30.0)
                response.raise_for_status()
                data = response.json()

                if data.get("encoding") == "base64":
                    import base64

                    content = base64.b64decode(data["content"]).decode("utf-8")
                    template = json.loads(content)
                    return template
                else:
                    raise ValueError("Unexpected response format from GitHub API")

        except httpx.HTTPStatusError as e:
            raise ValueError(f"Failed to fetch template from GitHub: {e.response.status_code}")
        except Exception as e:
            raise ValueError(f"Failed to fetch template from GitHub: {e}")

    async def get_version_history(
        self,
        template_id: str,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """Get version history for a template.

        Args:
            template_id: Template identifier
            limit: Maximum number of versions to return

        Returns:
            List of version dictionaries sorted by version (newest first)
        """
        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available")
            return None
        collection = db[self.collection_name]

        cursor = (
            collection.find({"template_id": template_id})
            .sort("version", -1)
            .limit(limit)
        )

        versions = []
        async for doc in cursor:
            doc.pop("_id", None)
            versions.append(doc)

        versions.sort(
            key=lambda x: TemplateVersionManager.parse_version(x["version"]),
            reverse=True,
        )

        return versions

    async def get_changelog(
        self,
        template_id: str,
        from_version: str | None = None,
        to_version: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get changelog for a template.

        Args:
            template_id: Template identifier
            from_version: Starting version (inclusive)
            to_version: Ending version (inclusive)

        Returns:
            List of changelog entries with version and changes
        """
        versions = await self.get_version_history(template_id)

        changelog = []
        for version_doc in versions:
            version = version_doc["version"]

            if from_version:
                if TemplateVersionManager.compare_versions(version, from_version) < 0:
                    continue

            if to_version:
                if TemplateVersionManager.compare_versions(version, to_version) > 0:
                    continue

            if version_doc.get("changelog"):
                changelog.append({
                    "version": version,
                    "published_at": version_doc.get("published_at"),
                    "author": version_doc.get("author"),
                    "changes": version_doc["changelog"],
                })

        return changelog

    async def suggest_next_version(
        self,
        template_id: str,
        change_type: str = "patch",
    ) -> str:
        """Suggest next version for a template.

        Args:
            template_id: Template identifier
            change_type: Type of change (major, minor, patch)

        Returns:
            Suggested next version string

        Raises:
            ValueError: If template not found or invalid change_type
        """
        versions = await self._get_template_versions(template_id)
        if not versions:
            return "1.0.0"

        latest_version = TemplateVersionManager.get_latest_version(versions)
        return TemplateVersionManager.suggest_next_version(latest_version, change_type)

    async def validate_template(
        self,
        template: dict[str, Any],
    ) -> dict[str, Any]:
        """Validate template structure and security.

        Args:
            template: Template dictionary

        Returns:
            Validation result dictionary with 'valid' and 'errors' keys
        """
        errors: list[str] = []
        warnings: list[str] = []

        if "structure" not in template:
            errors.append("Missing 'structure' field")

        if "structure" in template:
            structure = template["structure"]
            if not isinstance(structure, dict):
                errors.append("'structure' must be a dictionary")

            if not structure:
                warnings.append("Empty structure")

        if "project_type" not in template:
            errors.append("Missing 'project_type' field")

        if "version" in template:
            try:
                TemplateVersionManager.parse_version(template["version"])
            except ValueError as e:
                errors.append(str(e))

        if "changelog" in template:
            changelog = template["changelog"]
            if isinstance(changelog, list):
                validation = TemplateVersionManager.validate_changelog(changelog)
                errors.extend(validation["errors"])
                warnings.extend(validation["warnings"])

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

    async def _save_template(self, template: TemplateMetadata) -> None:
        """Save template to MongoDB.

        Args:
            template: TemplateMetadata instance
        """
        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available")
            return None
        collection = db[self.collection_name]

        template_dict = template.model_dump()
        template_dict["updated_at"] = datetime.utcnow()

        await collection.update_one(
            {"template_id": template.template_id, "version": template.version},
            {"$set": template_dict},
            upsert=True,
        )

        if template.is_latest:
            await collection.update_many(
                {
                    "template_id": template.template_id,
                    "version": {"$ne": template.version},
                },
                {"$set": {"is_latest": False}},
            )

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
            Template ID
        """
        parts = [project_type]
        if architecture_type:
            parts.append(architecture_type)
        if cloud_provider:
            parts.append(cloud_provider)

        name_slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        parts.append(name_slug)

        return "-".join(parts)

    async def _get_template_versions(self, template_id: str) -> list[str]:
        """Get all versions for a template.

        Args:
            template_id: Template identifier

        Returns:
            List of version strings
        """
        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available")
            return None
        collection = db[self.collection_name]

        cursor = collection.find(
            {"template_id": template_id},
            {"version": 1},
        )

        versions = []
        async for doc in cursor:
            versions.append(doc["version"])

        return versions

    async def _mark_previous_versions_not_latest(self, template_id: str) -> None:
        """Mark all previous versions as not latest.

        Args:
            template_id: Template identifier
        """
        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available")
            return None
        collection = db[self.collection_name]

        await collection.update_many(
            {"template_id": template_id},
            {"$set": {"is_latest": False}},
        )

