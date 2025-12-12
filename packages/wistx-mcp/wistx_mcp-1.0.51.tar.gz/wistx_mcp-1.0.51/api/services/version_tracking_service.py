"""Service for tracking API and MCP tool version usage."""

import logging
from datetime import datetime
from typing import Any

from api.database.mongodb import mongodb_manager

logger = logging.getLogger(__name__)


class VersionTrackingService:
    """Service for tracking API version and MCP tool version usage."""

    def __init__(self):
        """Initialize version tracking service."""
        self.db = mongodb_manager.get_database()
        self._ensure_collections()

    def _ensure_collections(self) -> None:
        """Ensure version tracking collections exist."""
        collections = ["api_version_usage", "mcp_tool_version_usage"]
        for collection_name in collections:
            if collection_name not in self.db.list_collection_names():
                self.db.create_collection(collection_name)
                logger.debug("Created collection: %s", collection_name)

    def track_api_version_usage(
        self,
        version: str,
        endpoint: str,
        user_id: str | None = None,
        api_key_id: str | None = None,
    ) -> None:
        """Track API version usage.

        Args:
            version: API version (e.g., "v1")
            endpoint: Endpoint path
            user_id: Optional user ID
            api_key_id: Optional API key ID
        """
        try:
            usage_doc = {
                "version": version,
                "endpoint": endpoint,
                "user_id": user_id,
                "api_key_id": api_key_id,
                "timestamp": datetime.utcnow(),
                "date": datetime.utcnow().date().isoformat(),
            }

            self.db.api_version_usage.insert_one(usage_doc)
        except Exception as e:
            logger.debug("Failed to track API version usage: %s", e)

    def track_mcp_tool_version_usage(
        self,
        tool_name: str,
        tool_version: str | None = None,
        user_id: str | None = None,
        api_key_id: str | None = None,
    ) -> None:
        """Track MCP tool version usage.

        Args:
            tool_name: Tool name (e.g., "wistx_get_compliance_requirements")
            tool_version: Tool version (e.g., "v1", "v2")
            user_id: Optional user ID
            api_key_id: Optional API key ID
        """
        try:
            usage_doc = {
                "tool_name": tool_name,
                "tool_version": tool_version,
                "user_id": user_id,
                "api_key_id": api_key_id,
                "timestamp": datetime.utcnow(),
                "date": datetime.utcnow().date().isoformat(),
            }

            self.db.mcp_tool_version_usage.insert_one(usage_doc)
        except Exception as e:
            logger.debug("Failed to track MCP tool version usage: %s", e)

    def get_api_version_stats(
        self,
        version: str | None = None,
        days: int = 30,
    ) -> dict[str, Any]:
        """Get API version usage statistics.

        Args:
            version: Optional version filter
            days: Number of days to analyze

        Returns:
            Statistics dictionary
        """
        try:
            from datetime import timedelta

            cutoff_date = datetime.utcnow() - timedelta(days=days)

            query: dict[str, Any] = {"timestamp": {"$gte": cutoff_date}}
            if version:
                query["version"] = version

            pipeline = [
                {"$match": query},
                {
                    "$group": {
                        "_id": "$version",
                        "count": {"$sum": 1},
                        "unique_users": {"$addToSet": "$user_id"},
                        "unique_endpoints": {"$addToSet": "$endpoint"},
                    }
                },
            ]

            results = list(self.db.api_version_usage.aggregate(pipeline))

            stats = {}
            for result in results:
                version_key = result["_id"]
                stats[version_key] = {
                    "total_requests": result["count"],
                    "unique_users": len([u for u in result["unique_users"] if u]),
                    "unique_endpoints": len(result["unique_endpoints"]),
                }

            return stats
        except Exception as e:
            logger.error("Failed to get API version stats: %s", e)
            return {}

    def get_mcp_tool_version_stats(
        self,
        tool_name: str | None = None,
        days: int = 30,
    ) -> dict[str, Any]:
        """Get MCP tool version usage statistics.

        Args:
            tool_name: Optional tool name filter
            days: Number of days to analyze

        Returns:
            Statistics dictionary
        """
        try:
            from datetime import timedelta

            cutoff_date = datetime.utcnow() - timedelta(days=days)

            query: dict[str, Any] = {"timestamp": {"$gte": cutoff_date}}
            if tool_name:
                query["tool_name"] = tool_name

            pipeline = [
                {"$match": query},
                {
                    "$group": {
                        "_id": {"tool_name": "$tool_name", "tool_version": "$tool_version"},
                        "count": {"$sum": 1},
                        "unique_users": {"$addToSet": "$user_id"},
                    }
                },
            ]

            results = list(self.db.mcp_tool_version_usage.aggregate(pipeline))

            stats = {}
            for result in results:
                tool_key = f"{result['_id']['tool_name']}@{result['_id']['tool_version'] or 'latest'}"
                stats[tool_key] = {
                    "total_calls": result["count"],
                    "unique_users": len([u for u in result["unique_users"] if u]),
                }

            return stats
        except Exception as e:
            logger.error("Failed to get MCP tool version stats: %s", e)
            return {}


version_tracking_service = VersionTrackingService()

