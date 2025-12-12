"""Usage aggregation service for billing and analytics."""

import logging
from datetime import datetime, timedelta
from typing import Any, Optional

from bson import ObjectId

from api.database.async_mongodb import async_mongodb_adapter

logger = logging.getLogger(__name__)


class UsageAggregator:
    """Service for aggregating usage data for billing and analytics."""

    async def aggregate_user_usage(
        self,
        user_id: str,
        start_date: datetime,
        end_date: datetime,
    ) -> dict[str, Any]:
        """Aggregate usage for a user in a time period.

        Args:
            user_id: User ID
            start_date: Start date
            end_date: End date

        Returns:
            Aggregated usage data
        """
        await async_mongodb_adapter.connect()
        db = async_mongodb_adapter.get_database()
        collection = db.api_usage

        query = {
            "user_id": ObjectId(user_id),
            "timestamp": {
                "$gte": start_date,
                "$lte": end_date,
            },
        }

        pipeline = [
            {"$match": query},
            {
                "$group": {
                    "_id": None,
                    "total_requests": {"$sum": 1},
                    "successful_requests": {
                        "$sum": {"$cond": ["$success", 1, 0]},
                    },
                    "failed_requests": {
                        "$sum": {"$cond": ["$success", 0, 1]},
                    },
                    "total_queries": {
                        "$sum": {"$cond": [{"$eq": ["$operation_type", "query"]}, 1, 0]},
                    },
                    "total_indexes": {
                        "$sum": {"$cond": [{"$eq": ["$operation_type", "index"]}, 1, 0]},
                    },
                    "total_storage_mb": {
                        "$sum": "$operation_details.storage_mb",
                    },
                    "avg_response_time": {
                        "$avg": "$performance.total_time_ms",
                    },
                }
            },
        ]

        result = await collection.aggregate(pipeline).to_list(length=None)

        if not result:
            return {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "total_queries": 0,
                "total_indexes": 0,
                "total_storage_mb": 0.0,
                "avg_response_time_ms": None,
            }

        data = result[0]
        return {
            "total_requests": data.get("total_requests", 0),
            "successful_requests": data.get("successful_requests", 0),
            "failed_requests": data.get("failed_requests", 0),
            "total_queries": data.get("total_queries", 0),
            "total_indexes": data.get("total_indexes", 0),
            "total_storage_mb": round(float(data.get("total_storage_mb", 0.0)), 2),
            "avg_response_time_ms": round(data.get("avg_response_time", 0), 2) if data.get("avg_response_time") else None,
        }

    async def aggregate_organization_usage(
        self,
        organization_id: str,
        start_date: datetime,
        end_date: datetime,
    ) -> dict[str, Any]:
        """Aggregate usage for an organization in a time period.

        Args:
            organization_id: Organization ID
            start_date: Start date
            end_date: End date

        Returns:
            Aggregated usage data
        """
        await async_mongodb_adapter.connect()
        db = async_mongodb_adapter.get_database()
        collection = db.api_usage

        query = {
            "organization_id": ObjectId(organization_id),
            "timestamp": {
                "$gte": start_date,
                "$lte": end_date,
            },
        }

        pipeline = [
            {"$match": query},
            {
                "$group": {
                    "_id": "$user_id",
                    "total_requests": {"$sum": 1},
                    "total_queries": {
                        "$sum": {"$cond": [{"$eq": ["$operation_type", "query"]}, 1, 0]},
                    },
                    "total_indexes": {
                        "$sum": {"$cond": [{"$eq": ["$operation_type", "index"]}, 1, 0]},
                    },
                    "total_storage_mb": {
                        "$sum": "$operation_details.storage_mb",
                    },
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_users": {"$sum": 1},
                    "total_requests": {"$sum": "$total_requests"},
                    "total_queries": {"$sum": "$total_queries"},
                    "total_indexes": {"$sum": "$total_indexes"},
                    "total_storage_mb": {"$sum": "$total_storage_mb"},
                }
            },
        ]

        result = await collection.aggregate(pipeline).to_list(length=None)

        if not result:
            return {
                "total_users": 0,
                "total_requests": 0,
                "total_queries": 0,
                "total_indexes": 0,
                "total_storage_mb": 0.0,
            }

        data = result[0]
        return {
            "total_users": data.get("total_users", 0),
            "total_requests": data.get("total_requests", 0),
            "total_queries": data.get("total_queries", 0),
            "total_indexes": data.get("total_indexes", 0),
            "total_storage_mb": round(float(data.get("total_storage_mb", 0.0)), 2),
        }

    async def get_monthly_usage(
        self,
        user_id: str,
        year: int,
        month: int,
    ) -> dict[str, Any]:
        """Get usage for a specific month.

        Args:
            user_id: User ID
            year: Year
            month: Month (1-12)

        Returns:
            Monthly usage data
        """
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        return await self.aggregate_user_usage(user_id, start_date, end_date - timedelta(seconds=1))


usage_aggregator = UsageAggregator()
