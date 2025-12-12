"""Report template manager for custom compliance report templates."""

import logging
import uuid
from datetime import datetime
from typing import Any

from jinja2 import Environment, BaseLoader, Template, TemplateError, select_autoescape
from pystache import Renderer

from wistx_mcp.models.report_template import (
    ReportTemplate,
    TemplateEngine,
    OutputFormat,
)
from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.template_version_manager import TemplateVersionManager

logger = logging.getLogger(__name__)


class ReportTemplateManager:
    """Manages report templates for documentation generation."""

    def __init__(self, mongodb_client: MongoDBClient):
        """Initialize report template manager.

        Args:
            mongodb_client: MongoDB client instance
        """
        self.mongodb_client = mongodb_client
        self.collection_name = "report_templates"
        self.jinja_env = Environment(
            loader=BaseLoader(),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.mustache_renderer = Renderer()

    async def register_template(
        self,
        name: str,
        template_content: str,
        document_type: str,
        template_engine: TemplateEngine = TemplateEngine.JINJA2,
        version: str = "1.0.0",
        compliance_standards: list[str] | None = None,
        resource_types: list[str] | None = None,
        variables: dict[str, Any] | None = None,
        sections: list[str] | None = None,
        optional_sections: list[str] | None = None,
        branding: dict[str, Any] | None = None,
        styles: dict[str, Any] | None = None,
        output_formats: list[OutputFormat] | None = None,
        author: str | None = None,
        tags: list[str] | None = None,
        user_id: str | None = None,
        organization_id: str | None = None,
        visibility: str = "public",
        changelog: list[str] | None = None,
    ) -> ReportTemplate:
        """Register a report template.

        Args:
            name: Template name
            template_content: Template content
            document_type: Document type
            template_engine: Template engine
            version: Semantic version
            compliance_standards: Applicable compliance standards
            resource_types: Applicable resource types
            variables: Template variables schema
            sections: Required sections
            optional_sections: Optional sections
            branding: Branding configuration
            styles: CSS/styles
            output_formats: Supported output formats
            author: Template author
            tags: Template tags
            user_id: Owner user ID
            organization_id: Owner organization ID
            visibility: Visibility (public, private, organization)
            changelog: Changelog entries

        Returns:
            ReportTemplate instance

        Raises:
            ValueError: If template validation fails
        """
        TemplateVersionManager.parse_version(version)

        validation = await self.validate_template(template_content, template_engine)
        if not validation["valid"]:
            raise ValueError(f"Template validation failed: {validation['errors']}")

        template_id = f"report-template-{uuid.uuid4().hex[:12]}"

        existing_versions = await self._get_template_versions(template_id)
        if existing_versions:
            latest_existing = TemplateVersionManager.get_latest_version(existing_versions)
            if TemplateVersionManager.is_newer_version(version, latest_existing):
                await self._mark_previous_versions_not_latest(template_id)
            else:
                if TemplateVersionManager.compare_versions(version, latest_existing) == 0:
                    raise ValueError(
                        f"Version {version} already exists for template {template_id}. "
                        "Use a different version or update the existing one."
                    )

        if changelog:
            changelog_validation = TemplateVersionManager.validate_changelog(changelog)
            if not changelog_validation["valid"]:
                raise ValueError(f"Invalid changelog: {changelog_validation['errors']}")

        template = ReportTemplate(
            template_id=template_id,
            name=name,
            description=f"Template for {document_type}",
            version=version,
            template_engine=template_engine,
            template_content=template_content,
            output_formats=output_formats or [OutputFormat.MARKDOWN],
            document_type=document_type,
            compliance_standards=compliance_standards or [],
            resource_types=resource_types or [],
            variables=variables or {},
            sections=sections or [],
            optional_sections=optional_sections or [],
            branding=branding or {},
            styles=styles or {},
            author=author,
            tags=tags or [],
            quality_score=self._calculate_quality_score(template_content, variables),
            is_latest=True,
            previous_version=None,
            changelog=changelog or [],
            visibility=visibility,
            user_id=user_id,
            organization_id=organization_id,
            published_at=datetime.utcnow(),
        )

        await self._save_template(template)

        logger.info(
            "Registered report template: id=%s, name=%s, version=%s, engine=%s",
            template_id,
            name,
            version,
            template_engine.value,
        )

        return template

    async def get_template(
        self,
        template_id: str,
        version: str | None = None,
    ) -> ReportTemplate | None:
        """Get template by ID and optional version.

        Args:
            template_id: Template identifier
            version: Version (if None, returns latest)

        Returns:
            ReportTemplate instance or None
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

        doc = await collection.find_one(query)
        if not doc:
            return None

        doc.pop("_id", None)
        try:
            return ReportTemplate(**doc)
        except Exception as e:
            logger.warning("Failed to parse template %s: %s", template_id, e)
            return None

    async def search_templates(
        self,
        document_type: str | None = None,
        compliance_standard: str | None = None,
        resource_type: str | None = None,
        template_engine: TemplateEngine | None = None,
        visibility: str = "public",
        user_id: str | None = None,
        organization_id: str | None = None,
        limit: int = 20,
    ) -> list[ReportTemplate]:
        """Search templates.

        Args:
            document_type: Filter by document type
            compliance_standard: Filter by compliance standard
            resource_type: Filter by resource type
            template_engine: Filter by template engine
            visibility: Visibility filter
            user_id: User ID for private templates
            organization_id: Organization ID for org templates
            limit: Maximum number of results

        Returns:
            List of ReportTemplate instances
        """
        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available")
            return []
        collection = db[self.collection_name]

        query: dict[str, Any] = {"is_latest": True}

        if document_type:
            query["document_type"] = document_type
        if compliance_standard:
            query["compliance_standards"] = compliance_standard
        if resource_type:
            query["resource_types"] = resource_type
        if template_engine:
            query["template_engine"] = template_engine.value

        if visibility == "public":
            query["visibility"] = "public"
        elif visibility == "private" and user_id:
            query["$or"] = [
                {"visibility": "public"},
                {"visibility": "private", "user_id": user_id},
            ]
        elif visibility == "organization" and organization_id:
            query["$or"] = [
                {"visibility": "public"},
                {"visibility": "organization", "organization_id": organization_id},
            ]

        cursor = collection.find(query).sort("usage_count", -1).limit(limit)

        templates = []
        async for doc in cursor:
            doc.pop("_id", None)
            try:
                template = ReportTemplate(**doc)
                templates.append(template)
            except Exception as e:
                logger.warning("Failed to parse template %s: %s", doc.get("template_id"), e)

        return templates

    async def render_template(
        self,
        template_id: str,
        data: dict[str, Any],
        output_format: OutputFormat = OutputFormat.MARKDOWN,
        version: str | None = None,
    ) -> str:
        """Render template with data.

        Args:
            template_id: Template identifier
            data: Template data
            output_format: Output format
            version: Template version (if None, uses latest)

        Returns:
            Rendered content

        Raises:
            ValueError: If template not found or rendering fails
        """
        template = await self.get_template(template_id, version)
        if not template:
            raise ValueError(f"Template not found: {template_id}")

        if output_format not in template.output_formats:
            raise ValueError(
                f"Output format {output_format.value} not supported by template. "
                f"Supported formats: {[f.value for f in template.output_formats]}"
            )

        try:
            if template.template_engine == TemplateEngine.JINJA2:
                jinja_template = self.jinja_env.from_string(template.template_content)
                rendered = jinja_template.render(**data)
            elif template.template_engine == TemplateEngine.MUSTACHE:
                rendered = self.mustache_renderer.render(template.template_content, data)
            else:
                rendered = template.template_content.format(**data)

            await self._track_usage(template_id)

            return rendered

        except TemplateError as e:
            logger.error("Jinja2 template error: %s", e)
            raise ValueError(f"Template rendering failed: {e}")
        except Exception as e:
            logger.error("Template rendering error: %s", e)
            raise ValueError(f"Template rendering failed: {e}")

    async def validate_template(
        self,
        template_content: str,
        template_engine: TemplateEngine,
    ) -> dict[str, Any]:
        """Validate template content.

        Args:
            template_content: Template content
            template_engine: Template engine

        Returns:
            Validation result with 'valid' (bool) and 'errors' (list[str])
        """
        errors = []

        if not template_content or not template_content.strip():
            errors.append("Template content is empty")

        if template_engine == TemplateEngine.JINJA2:
            try:
                self.jinja_env.from_string(template_content)
            except TemplateError as e:
                errors.append(f"Jinja2 syntax error: {e}")
        elif template_engine == TemplateEngine.MUSTACHE:
            try:
                self.mustache_renderer.render(template_content, {})
            except Exception as e:
                errors.append(f"Mustache syntax error: {e}")

        return {"valid": len(errors) == 0, "errors": errors}

    async def get_version_history(self, template_id: str) -> list[ReportTemplate]:
        """Get version history for a template.

        Args:
            template_id: Template identifier

        Returns:
            List of ReportTemplate instances (all versions)
        """
        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available")
            return []
        collection = db[self.collection_name]

        cursor = collection.find({"template_id": template_id}).sort("version", -1)

        templates = []
        async for doc in cursor:
            doc.pop("_id", None)
            try:
                template = ReportTemplate(**doc)
                templates.append(template)
            except Exception as e:
                logger.warning("Failed to parse template version %s: %s", doc.get("version"), e)

        return templates

    async def _get_template_versions(self, template_id: str) -> list[str]:
        """Get all versions for a template (internal).

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
            return []
        collection = db[self.collection_name]

        cursor = collection.find({"template_id": template_id}, {"version": 1})
        versions = []
        async for doc in cursor:
            versions.append(doc["version"])
        return versions

    async def _mark_previous_versions_not_latest(self, template_id: str) -> None:
        """Mark previous versions as not latest (internal).

        Args:
            template_id: Template identifier
        """
        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available")
            return
        collection = db[self.collection_name]

        await collection.update_many(
            {"template_id": template_id, "is_latest": True},
            {"$set": {"is_latest": False}},
        )

    async def _save_template(self, template: ReportTemplate) -> None:
        """Save template to MongoDB (internal).

        Args:
            template: ReportTemplate instance
        """
        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available")
            return
        collection = db[self.collection_name]

        template_dict = template.model_dump()
        template_dict["updated_at"] = datetime.utcnow()

        await collection.update_one(
            {"template_id": template.template_id, "version": template.version},
            {"$set": template_dict},
            upsert=True,
        )

    async def _track_usage(self, template_id: str) -> None:
        """Track template usage (internal).

        Args:
            template_id: Template identifier
        """
        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available")
            return
        collection = db[self.collection_name]

        await collection.update_one(
            {"template_id": template_id, "is_latest": True},
            {"$inc": {"usage_count": 1}, "$set": {"last_used_at": datetime.utcnow()}},
        )

    async def get_default_template(
        self,
        document_type: str,
        compliance_standard: str | None = None,
    ) -> ReportTemplate | None:
        """Get or create default template for document type and compliance standard.

        This method retrieves the default template from the template library
        for the specified document type and compliance standard. If no template
        exists in the database, it creates one from the built-in template library.

        Args:
            document_type: Type of document (e.g., "compliance_report")
            compliance_standard: Compliance standard (e.g., "PCI-DSS", "HIPAA")

        Returns:
            ReportTemplate instance or None if not found/created

        Raises:
            ValueError: If template creation fails
        """
        # First, try to find existing default template in database
        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available, using built-in template")
            return await self._get_builtin_template(document_type, compliance_standard)

        collection = db[self.collection_name]

        # Search for existing default template
        query = {
            "document_type": document_type,
            "is_latest": True,
            "visibility": "public",
            "is_default": True,
        }
        if compliance_standard:
            query["compliance_standards"] = compliance_standard

        existing = await collection.find_one(query)
        if existing:
            existing.pop("_id", None)
            try:
                return ReportTemplate(**existing)
            except Exception as e:
                logger.warning("Failed to parse existing template: %s", e)

        # If not found, create from built-in template library
        return await self._get_builtin_template(document_type, compliance_standard)

    async def _get_builtin_template(
        self,
        document_type: str,
        compliance_standard: str | None = None,
    ) -> ReportTemplate | None:
        """Get built-in template from template library and register it.

        Args:
            document_type: Type of document
            compliance_standard: Compliance standard

        Returns:
            ReportTemplate instance or None if not available
        """
        from wistx_mcp.tools.lib.template_library import TemplateLibrary

        template_dict = None

        if document_type == "compliance_report":
            if compliance_standard == "HIPAA":
                template_dict = TemplateLibrary.get_hipaa_template()
            elif compliance_standard == "PCI-DSS" or not compliance_standard:
                template_dict = TemplateLibrary.get_pci_dss_template()
            # Add more standards as needed

        if not template_dict:
            logger.warning(
                "No built-in template found for %s/%s",
                document_type,
                compliance_standard,
            )
            return None

        try:
            # Register the built-in template
            template = await self.register_template(
                name=template_dict.get("name", f"Default {compliance_standard} Template"),
                template_content=template_dict.get("template_content", ""),
                document_type=document_type,
                template_engine=TemplateEngine.JINJA2,
                version="1.0.0",
                compliance_standards=[compliance_standard] if compliance_standard else [],
                visibility="public",
                author="system",
                tags=["default", "built-in"],
            )
            # Mark as default
            if self.mongodb_client.database:
                db = self.mongodb_client.database
                if db:
                    collection = db[self.collection_name]
                    await collection.update_one(
                        {"template_id": template.template_id},
                        {"$set": {"is_default": True}},
                    )
            return template
        except Exception as e:
            logger.error("Failed to register built-in template: %s", e)
            return None

    def _calculate_quality_score(
        self,
        template_content: str,
        variables: dict[str, Any] | None,
    ) -> int:
        """Calculate quality score for template.

        Args:
            template_content: Template content
            variables: Template variables

        Returns:
            Quality score (0-100)
        """
        score = 50

        if len(template_content) > 500:
            score += 20
        if variables:
            score += 15
        if "{{" in template_content or "{%" in template_content:
            score += 15

        return min(score, 100)

