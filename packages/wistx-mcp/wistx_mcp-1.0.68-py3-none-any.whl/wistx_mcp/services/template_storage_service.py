"""Template storage service for quality-scored templates."""

import logging
import uuid
from datetime import datetime
from typing import Any

from wistx_mcp.models.template_storage import QualityTemplate, TemplateFilter
from wistx_mcp.tools.lib.mongodb_client import MongoDBClient

logger = logging.getLogger(__name__)


class TemplateStorageService:
    """Service for storing and retrieving quality-scored templates."""

    COLLECTION_NAME = "quality_templates"

    def __init__(self, mongodb_client: MongoDBClient):
        """Initialize template storage service.

        Args:
            mongodb_client: MongoDB client instance
        """
        self.mongodb_client = mongodb_client

    async def store_template(
        self,
        template_type: str,
        content: dict[str, Any],
        quality_score: float,
        score_breakdown: dict[str, float],
        metadata: dict[str, Any],
        source_repo_url: str | None = None,
        tags: list[str] | None = None,
        categories: list[str] | None = None,
        user_id: str | None = None,
        organization_id: str | None = None,
        visibility: str = "global",
    ) -> str:
        """Store a quality template.

        Args:
            template_type: Type of template (repository_tree or infrastructure_visualization)
            content: Template content
            quality_score: Overall quality score
            score_breakdown: Detailed score breakdown
            metadata: Original metadata
            source_repo_url: Source repository URL
            tags: Tags for filtering
            categories: Categories
            user_id: User ID for user-specific templates
            organization_id: Organization ID for org-specific templates
            visibility: Visibility level (global, user, organization)

        Returns:
            Template ID
        """
        await self.mongodb_client.connect()

        if self.mongodb_client.database is None:
            raise RuntimeError("MongoDB database connection failed")

        template_id = str(uuid.uuid4())

        template = QualityTemplate(
            template_id=template_id,
            type=template_type,
            source_repo_url=source_repo_url,
            quality_score=quality_score,
            score_breakdown=score_breakdown,
            content=content,
            metadata=metadata,
            tags=tags or [],
            categories=categories or [],
            created_at=datetime.utcnow(),
            user_id=user_id,
            organization_id=organization_id,
            visibility=visibility,
        )

        collection = self.mongodb_client.database[self.COLLECTION_NAME]
        await collection.insert_one(template.model_dump())

        logger.info(
            "Stored quality template: id=%s, type=%s, score=%.2f",
            template_id,
            template_type,
            quality_score,
        )

        return template_id

    async def find_templates(self, filter_params: TemplateFilter) -> list[dict[str, Any]]:
        """Find templates matching filter criteria.

        Args:
            filter_params: Template filter parameters

        Returns:
            List of matching templates
        """
        await self.mongodb_client.connect()

        if self.mongodb_client.database is None:
            return []

        collection = self.mongodb_client.database[self.COLLECTION_NAME]

        mongo_filter: dict[str, Any] = {}

        if filter_params.type:
            mongo_filter["type"] = filter_params.type

        if filter_params.min_quality_score is not None:
            mongo_filter["quality_score"] = {"$gte": filter_params.min_quality_score}

        if filter_params.tags:
            mongo_filter["tags"] = {"$in": filter_params.tags}

        if filter_params.categories:
            mongo_filter["categories"] = {"$in": filter_params.categories}

        if filter_params.visibility:
            mongo_filter["visibility"] = {"$in": filter_params.visibility}

        if filter_params.user_id:
            mongo_filter["user_id"] = filter_params.user_id

        if filter_params.organization_id:
            mongo_filter["organization_id"] = filter_params.organization_id

        cursor = collection.find(mongo_filter).sort("quality_score", -1).limit(filter_params.limit)
        results = await cursor.to_list(length=filter_params.limit)

        return results

    async def get_template(self, template_id: str) -> dict[str, Any] | None:
        """Get template by ID.

        Args:
            template_id: Template ID

        Returns:
            Template document or None if not found
        """
        await self.mongodb_client.connect()

        if self.mongodb_client.database is None:
            return None

        collection = self.mongodb_client.database[self.COLLECTION_NAME]
        result = await collection.find_one({"template_id": template_id})

        return result

    async def increment_usage(self, template_id: str) -> None:
        """Increment template usage count.

        Args:
            template_id: Template ID
        """
        await self.mongodb_client.connect()

        if self.mongodb_client.database is None:
            return

        collection = self.mongodb_client.database[self.COLLECTION_NAME]
        await collection.update_one(
            {"template_id": template_id},
            {
                "$inc": {"usage_count": 1},
                "$set": {"last_used_at": datetime.utcnow()},
            },
        )

    async def delete_template(self, template_id: str, user_id: str | None = None) -> bool:
        """Delete template (only if user owns it or is admin).

        Args:
            template_id: Template ID
            user_id: User ID for authorization check

        Returns:
            True if deleted, False otherwise
        """
        await self.mongodb_client.connect()

        if self.mongodb_client.database is None:
            return False

        collection = self.mongodb_client.database[self.COLLECTION_NAME]

        filter_query: dict[str, Any] = {"template_id": template_id}

        if user_id:
            filter_query["user_id"] = user_id

        result = await collection.delete_one(filter_query)

        return result.deleted_count > 0

