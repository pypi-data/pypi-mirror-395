"""Template marketplace - discovery, search, rating, and analytics."""

import logging
from datetime import datetime
from typing import Any

from wistx_mcp.models.template import TemplateMetadata
from wistx_mcp.models.template_rating import TemplateAnalytics, TemplateRating
from wistx_mcp.tools.lib.mongodb_client import MongoDBClient

logger = logging.getLogger(__name__)


class TemplateMarketplace:
    """Template marketplace with discovery, search, rating, and analytics."""

    def __init__(self, mongodb_client: MongoDBClient):
        """Initialize template marketplace.

        Args:
            mongodb_client: MongoDB client instance
        """
        self.mongodb_client = mongodb_client
        self.template_collection = "template_registry"
        self.rating_collection = "template_ratings"
        self.analytics_collection = "template_analytics"

    async def search_templates(
        self,
        query: str | None = None,
        project_type: str | None = None,
        cloud_provider: str | None = None,
        architecture_type: str | None = None,
        tags: list[str] | None = None,
        min_rating: float | None = None,
        min_usage_count: int | None = None,
        source_type: str | None = None,
        visibility: str = "public",
        user_id: str | None = None,
        sort_by: str = "popularity",
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Search and filter templates.

        Args:
            query: Text search query
            project_type: Filter by project type
            cloud_provider: Filter by cloud provider
            architecture_type: Filter by architecture type
            tags: Filter by tags
            min_rating: Minimum average rating
            min_usage_count: Minimum usage count
            source_type: Filter by source type (github, user)
            visibility: Filter by visibility
            user_id: Filter by user ID
            sort_by: Sort order (popularity, rating, usage, newest, oldest)
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            Dictionary with search results and metadata
        """
        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available")
            return {"templates": [], "total": 0}
        collection = db[self.template_collection]

        query_filter: dict[str, Any] = {"is_latest": True}

        if project_type:
            query_filter["project_type"] = project_type
        if cloud_provider:
            query_filter["cloud_provider"] = cloud_provider
        if architecture_type:
            query_filter["architecture_type"] = architecture_type
        if tags:
            query_filter["tags"] = {"$in": tags}
        if source_type:
            query_filter["source_type"] = source_type
        if visibility:
            query_filter["visibility"] = visibility
        if user_id:
            query_filter["user_id"] = user_id

        if query:
            query_filter["$text"] = {"$search": query}

        cursor = collection.find(query_filter)

        if sort_by == "popularity":
            cursor = cursor.sort("usage_count", -1)
        elif sort_by == "rating":
            cursor = cursor.sort("quality_score", -1)
        elif sort_by == "usage":
            cursor = cursor.sort("usage_count", -1)
        elif sort_by == "newest":
            cursor = cursor.sort("created_at", -1)
        elif sort_by == "oldest":
            cursor = cursor.sort("created_at", 1)
        else:
            cursor = cursor.sort("usage_count", -1)

        total_count = await collection.count_documents(query_filter)
        cursor = cursor.skip(offset).limit(limit)

        templates = []
        template_ids = []

        async for doc in cursor:
            doc.pop("_id", None)
            template_ids.append(doc["template_id"])

            analytics = await self._get_analytics(doc["template_id"])
            if analytics:
                doc["average_rating"] = analytics.average_rating
                doc["total_ratings"] = analytics.total_ratings
                doc["unique_users"] = analytics.unique_users

            if min_rating and doc.get("average_rating", 0) < min_rating:
                continue

            if min_usage_count and doc.get("usage_count", 0) < min_usage_count:
                continue

            try:
                template = TemplateMetadata(**doc)
                templates.append(template)
            except Exception as e:
                logger.warning("Failed to parse template %s: %s", doc.get("template_id"), e)

        return {
            "templates": templates,
            "total": total_count,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + limit) < total_count,
        }

    async def rate_template(
        self,
        template_id: str,
        user_id: str,
        rating: int,
        comment: str | None = None,
        version: str | None = None,
    ) -> TemplateRating:
        """Rate a template.

        Args:
            template_id: Template identifier
            user_id: User ID
            rating: Rating (1-5 stars)
            comment: Optional comment
            version: Template version (default: latest)

        Returns:
            TemplateRating instance

        Raises:
            ValueError: If invalid rating or template not found
        """
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")

        if not version:
            template = await self._get_latest_template(template_id)
            if not template:
                raise ValueError(f"Template not found: {template_id}")
            version = template["version"]

        rating_id = f"{template_id}-{user_id}-{version}"

        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available")
            return None
        rating_collection = db[self.rating_collection]

        rating_doc = {
            "rating_id": rating_id,
            "template_id": template_id,
            "version": version,
            "user_id": user_id,
            "rating": rating,
            "comment": comment,
            "updated_at": datetime.utcnow(),
        }

        existing = await rating_collection.find_one({"rating_id": rating_id})
        if existing:
            rating_doc["created_at"] = existing.get("created_at", datetime.utcnow())
            await rating_collection.update_one(
                {"rating_id": rating_id},
                {"$set": rating_doc},
            )
        else:
            rating_doc["created_at"] = datetime.utcnow()
            await rating_collection.insert_one(rating_doc)

        await self._update_analytics(template_id)

        template_rating = TemplateRating(**rating_doc)
        logger.info(
            "Template rated: template_id=%s, user_id=%s, rating=%d",
            template_id,
            user_id,
            rating,
        )

        return template_rating

    async def get_template_ratings(
        self,
        template_id: str,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Get ratings for a template.

        Args:
            template_id: Template identifier
            limit: Maximum number of ratings
            offset: Pagination offset

        Returns:
            Dictionary with ratings and metadata
        """
        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available")
            return {"ratings": [], "average_rating": 0.0, "total_ratings": 0}
        rating_collection = db[self.rating_collection]

        query = {"template_id": template_id}
        cursor = rating_collection.find(query).sort("created_at", -1).skip(offset).limit(limit)
        total_count = await rating_collection.count_documents(query)

        ratings = []
        async for doc in cursor:
            doc.pop("_id", None)
            try:
                rating = TemplateRating(**doc)
                ratings.append(rating)
            except Exception as e:
                logger.warning("Failed to parse rating %s: %s", doc.get("rating_id"), e)

        return {
            "ratings": ratings,
            "total": total_count,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + limit) < total_count,
        }

    async def get_analytics(
        self,
        template_id: str,
    ) -> TemplateAnalytics | None:
        """Get analytics for a template.

        Args:
            template_id: Template identifier

        Returns:
            TemplateAnalytics instance or None
        """
        return await self._get_analytics(template_id)

    async def track_usage(
        self,
        template_id: str,
        user_id: str | None = None,
    ) -> None:
        """Track template usage.

        Args:
            template_id: Template identifier
            user_id: User ID (optional)
        """
        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available")
            return None
        collection = db[self.template_collection]

        update: dict[str, Any] = {
            "$inc": {"usage_count": 1},
            "$set": {"last_used_at": datetime.utcnow()},
        }

        await collection.update_one(
            {"template_id": template_id, "is_latest": True},
            update,
        )

        await self._update_analytics(template_id, user_id=user_id)

        logger.debug("Tracked usage for template: %s", template_id)

    async def get_popular_templates(
        self,
        project_type: str | None = None,
        limit: int = 10,
    ) -> list[TemplateMetadata]:
        """Get popular templates.

        Args:
            project_type: Filter by project type
            limit: Maximum number of results

        Returns:
            List of popular templates
        """
        results = await self.search_templates(
            project_type=project_type,
            sort_by="popularity",
            limit=limit,
        )
        return results["templates"]

    async def get_top_rated_templates(
        self,
        project_type: str | None = None,
        min_ratings: int = 5,
        limit: int = 10,
    ) -> list[TemplateMetadata]:
        """Get top-rated templates.

        Args:
            project_type: Filter by project type
            min_ratings: Minimum number of ratings required
            limit: Maximum number of results

        Returns:
            List of top-rated templates
        """
        results = await self.search_templates(
            project_type=project_type,
            min_rating=4.0,
            min_usage_count=min_ratings,
            sort_by="rating",
            limit=limit,
        )
        return results["templates"]

    async def _get_analytics(self, template_id: str) -> TemplateAnalytics | None:
        """Get analytics for a template (internal).

        Args:
            template_id: Template identifier

        Returns:
            TemplateAnalytics instance or None
        """
        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available")
            return None
        analytics_collection = db[self.analytics_collection]

        doc = await analytics_collection.find_one({"template_id": template_id})
        if not doc:
            return None

        doc.pop("_id", None)
        try:
            return TemplateAnalytics(**doc)
        except Exception as e:
            logger.warning("Failed to parse analytics for %s: %s", template_id, e)
            return None

    async def _update_analytics(
        self,
        template_id: str,
        user_id: str | None = None,
    ) -> None:
        """Update analytics for a template.

        Args:
            template_id: Template identifier
            user_id: User ID (optional)
        """
        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available")
            return None
        rating_collection = db[self.rating_collection]
        analytics_collection = db[self.analytics_collection]

        ratings_cursor = rating_collection.find({"template_id": template_id})
        ratings = []
        async for doc in ratings_cursor:
            ratings.append(doc["rating"])

        total_ratings = len(ratings)
        average_rating = sum(ratings) / total_ratings if ratings else 0.0

        rating_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for rating in ratings:
            rating_distribution[rating] = rating_distribution.get(rating, 0) + 1

        template = await self._get_latest_template(template_id)
        usage_count = template.get("usage_count", 0) if template else 0

        unique_users_list = await rating_collection.distinct("user_id", {"template_id": template_id})
        unique_users = len(unique_users_list)

        analytics = TemplateAnalytics(
            template_id=template_id,
            total_ratings=total_ratings,
            average_rating=round(average_rating, 2),
            rating_distribution=rating_distribution,
            usage_count=usage_count,
            unique_users=unique_users,
            updated_at=datetime.utcnow(),
        )

        await analytics_collection.update_one(
            {"template_id": template_id},
            {"$set": analytics.model_dump()},
            upsert=True,
        )

    async def _get_latest_template(self, template_id: str) -> dict[str, Any] | None:
        """Get latest template (internal).

        Args:
            template_id: Template identifier

        Returns:
            Template dictionary or None
        """
        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB database not available")
            return None
        collection = db[self.template_collection]

        doc = await collection.find_one({"template_id": template_id, "is_latest": True})
        if doc:
            doc.pop("_id", None)
        return doc

