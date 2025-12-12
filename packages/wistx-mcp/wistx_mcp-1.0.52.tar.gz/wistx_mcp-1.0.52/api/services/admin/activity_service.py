"""Admin activity monitoring service."""

import logging
from datetime import datetime, timedelta
from typing import Any, Optional

from bson import ObjectId

from api.database.mongodb import mongodb_manager
from api.models.admin.analytics import ActivityEntry, ActivityFeedQuery, ActivityFeedResponse

logger = logging.getLogger(__name__)


class AdminActivityService:
    """Service for admin activity monitoring."""

    async def get_activity_feed(self, query: ActivityFeedQuery) -> ActivityFeedResponse:
        """Get activity feed with filters.

        Args:
            query: Query parameters

        Returns:
            Activity feed response
        """
        db = mongodb_manager.get_database()
        collection = db.api_usage

        filter_query: dict[str, Any] = {}

        if query.user_id:
            filter_query["user_id"] = ObjectId(query.user_id)

        if query.endpoint:
            filter_query["endpoint"] = {"$regex": query.endpoint, "$options": "i"}

        if query.operation_type:
            filter_query["operation_type"] = query.operation_type

        if query.success is not None:
            filter_query["success"] = query.success

        if query.start_date or query.end_date:
            filter_query["timestamp"] = {}
            if query.start_date:
                filter_query["timestamp"]["$gte"] = query.start_date
            if query.end_date:
                filter_query["timestamp"]["$lte"] = query.end_date

        cursor = (
            collection.find(filter_query)
            .sort("timestamp", -1)
            .skip(query.offset)
            .limit(query.limit)
        )

        activities = []
        user_cache: dict[str, dict[str, Any]] = {}

        for doc in cursor:
            user_id = str(doc["user_id"])

            if user_id not in user_cache:
                user_doc = db.users.find_one({"_id": doc["user_id"]})
                user_cache[user_id] = {
                    "email": user_doc.get("email") if user_doc else None,
                }

            response_time_ms = None
            if doc.get("performance") and doc["performance"].get("total_time_ms"):
                response_time_ms = doc["performance"]["total_time_ms"]

            activities.append(
                ActivityEntry(
                    request_id=doc.get("request_id", ""),
                    user_id=user_id,
                    email=user_cache[user_id]["email"],
                    api_key_id=str(doc["api_key_id"]) if doc.get("api_key_id") else None,
                    organization_id=str(doc["organization_id"]) if doc.get("organization_id") else None,
                    plan=doc.get("plan", "professional"),
                    timestamp=doc["timestamp"],
                    endpoint=doc.get("endpoint", ""),
                    method=doc.get("method", "GET"),
                    operation_type=doc.get("operation_type", "other"),
                    status_code=doc.get("status_code", 200),
                    success=doc.get("success", True),
                    ip_address=doc.get("ip_address"),
                    user_agent=doc.get("user_agent"),
                    response_time_ms=response_time_ms,
                )
            )

        total = collection.count_documents(filter_query)

        return ActivityFeedResponse(
            activities=activities,
            total=total,
            limit=query.limit,
            offset=query.offset,
        )

    async def get_user_activity(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
    ) -> list[ActivityEntry]:
        """Get user activity timeline.

        Args:
            user_id: User ID
            start_date: Optional start date
            end_date: Optional end date
            limit: Maximum number of results

        Returns:
            List of activity entries
        """
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()

        query = ActivityFeedQuery(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=0,
        )

        response = await self.get_activity_feed(query)
        return response.activities


admin_activity_service = AdminActivityService()

