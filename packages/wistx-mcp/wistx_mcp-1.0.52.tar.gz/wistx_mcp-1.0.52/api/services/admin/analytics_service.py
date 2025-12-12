"""Admin analytics service."""

import logging
from datetime import datetime, timedelta
from typing import Any

from bson import ObjectId

from api.database.mongodb import mongodb_manager
from api.models.admin.analytics import (
    TopEndpointResponse,
    TopEndpointsResponse,
    TopUserResponse,
    TopUsersResponse,
    UsageByPlanListResponse,
    UsageByPlanResponse,
    UsageOverviewResponse,
    UsageTrendPoint,
    UsageTrendsQuery,
    UsageTrendsResponse,
)

logger = logging.getLogger(__name__)


class AdminAnalyticsService:
    """Service for admin analytics."""

    async def get_usage_overview(self) -> UsageOverviewResponse:
        """Get usage overview statistics.

        Returns:
            Usage overview response
        """
        db = mongodb_manager.get_database()

        now = datetime.utcnow()
        day_ago = now - timedelta(days=1)
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)

        total_users = db.users.count_documents({})

        active_users_24h = len(
            db.api_usage.distinct(
                "user_id", {"timestamp": {"$gte": day_ago}}
            )
        )
        active_users_7d = len(
            db.api_usage.distinct(
                "user_id", {"timestamp": {"$gte": week_ago}}
            )
        )
        active_users_30d = len(
            db.api_usage.distinct(
                "user_id", {"timestamp": {"$gte": month_ago}}
            )
        )

        total_api_requests = db.api_usage.count_documents({})
        total_api_requests_24h = db.api_usage.count_documents({"timestamp": {"$gte": day_ago}})
        total_api_requests_7d = db.api_usage.count_documents({"timestamp": {"$gte": week_ago}})
        total_api_requests_30d = db.api_usage.count_documents({"timestamp": {"$gte": month_ago}})

        total_queries = db.api_usage.count_documents({"operation_type": "query"})
        total_indexing = db.api_usage.count_documents({"operation_type": "index"})

        storage_pipeline = [
            {"$match": {"operation_type": "index"}},
            {"$group": {"_id": None, "total": {"$sum": "$operation_details.storage_mb"}}},
        ]
        storage_result = list(db.api_usage.aggregate(storage_pipeline))
        total_storage_mb = storage_result[0]["total"] if storage_result else 0.0

        performance_pipeline = [
            {
                "$match": {
                    "performance.total_time_ms": {"$exists": True, "$ne": None}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "avg_time": {"$avg": "$performance.total_time_ms"},
                }
            },
        ]
        perf_result = list(db.api_usage.aggregate(performance_pipeline))
        average_response_time_ms = perf_result[0]["avg_time"] if perf_result else None

        error_count = db.api_usage.count_documents({"success": False})
        error_rate = (error_count / total_api_requests * 100) if total_api_requests > 0 else 0.0

        return UsageOverviewResponse(
            total_users=total_users,
            active_users_24h=active_users_24h,
            active_users_7d=active_users_7d,
            active_users_30d=active_users_30d,
            total_api_requests=total_api_requests,
            total_api_requests_24h=total_api_requests_24h,
            total_api_requests_7d=total_api_requests_7d,
            total_api_requests_30d=total_api_requests_30d,
            total_queries=total_queries,
            total_indexing_operations=total_indexing,
            total_storage_mb=round(total_storage_mb, 2),
            average_response_time_ms=round(average_response_time_ms, 2) if average_response_time_ms else None,
            error_rate=round(error_rate, 2),
        )

    async def get_usage_by_plan(self) -> UsageByPlanListResponse:
        """Get usage statistics by plan.

        Returns:
            Usage by plan response
        """
        db = mongodb_manager.get_database()

        pipeline = [
            {
                "$group": {
                    "_id": "$plan",
                    "user_ids": {"$addToSet": "$user_id"},
                    "total_requests": {"$sum": 1},
                    "total_queries": {
                        "$sum": {"$cond": [{"$eq": ["$operation_type", "query"]}, 1, 0]}
                    },
                    "total_indexing": {
                        "$sum": {"$cond": [{"$eq": ["$operation_type", "index"]}, 1, 0]}
                    },
                    "total_storage": {"$sum": "$operation_details.storage_mb"},
                }
            },
        ]

        results = list(db.api_usage.aggregate(pipeline))

        plans = []
        for result in results:
            plan = result["_id"] or "professional"
            user_count = len(result["user_ids"])
            total_requests = result["total_requests"]
            total_queries = result["total_queries"]
            total_indexing = result["total_indexing"]
            total_storage_mb = float(result.get("total_storage", 0.0))

            plans.append(
                UsageByPlanResponse(
                    plan=plan,
                    user_count=user_count,
                    total_requests=total_requests,
                    total_queries=total_queries,
                    total_indexing=total_indexing,
                    total_storage_mb=round(total_storage_mb, 2),
                    average_requests_per_user=round(total_requests / user_count, 2) if user_count > 0 else 0.0,
                )
            )

        return UsageByPlanListResponse(plans=plans)

    async def get_usage_trends(self, query: UsageTrendsQuery) -> UsageTrendsResponse:
        """Get usage trends.

        Args:
            query: Query parameters

        Returns:
            Usage trends response
        """
        db = mongodb_manager.get_database()
        collection = db.api_usage

        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=query.days)

        date_format = "%Y-%m-%d"
        if query.group_by == "week":
            date_format = "%Y-W%V"
        elif query.group_by == "month":
            date_format = "%Y-%m"

        pipeline = [
            {"$match": {"timestamp": {"$gte": start_date, "$lte": end_date}}},
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": date_format,
                            "date": "$timestamp",
                        }
                    },
                    "total_requests": {"$sum": 1},
                    "total_queries": {
                        "$sum": {"$cond": [{"$eq": ["$operation_type", "query"]}, 1, 0]}
                    },
                    "total_indexing": {
                        "$sum": {"$cond": [{"$eq": ["$operation_type", "index"]}, 1, 0]}
                    },
                    "unique_users": {"$addToSet": "$user_id"},
                    "error_count": {
                        "$sum": {"$cond": [{"$eq": ["$success", False]}, 1, 0]}
                    },
                    "response_times": {
                        "$push": "$performance.total_time_ms",
                    },
                }
            },
            {"$sort": {"_id": 1}},
        ]

        results = list(collection.aggregate(pipeline))

        trends = []
        for result in results:
            response_times = [t for t in result.get("response_times", []) if t is not None]
            avg_response_time = (
                sum(response_times) / len(response_times) if response_times else None
            )

            trends.append(
                UsageTrendPoint(
                    date=result["_id"],
                    total_requests=result["total_requests"],
                    total_queries=result["total_queries"],
                    total_indexing=result["total_indexing"],
                    unique_users=len(result["unique_users"]),
                    error_count=result["error_count"],
                    average_response_time_ms=round(avg_response_time, 2) if avg_response_time else None,
                )
            )

        return UsageTrendsResponse(trends=trends, period_days=query.days)

    async def get_top_endpoints(self, days: int = 30, limit: int = 10) -> TopEndpointsResponse:
        """Get top endpoints by usage.

        Args:
            days: Number of days to analyze
            limit: Maximum number of results

        Returns:
            Top endpoints response
        """
        db = mongodb_manager.get_database()
        collection = db.api_usage

        start_date = datetime.utcnow() - timedelta(days=days)

        pipeline = [
            {"$match": {"timestamp": {"$gte": start_date}}},
            {
                "$group": {
                    "_id": "$endpoint",
                    "request_count": {"$sum": 1},
                    "error_count": {
                        "$sum": {"$cond": [{"$eq": ["$success", False]}, 1, 0]}
                    },
                    "response_times": {
                        "$push": "$performance.total_time_ms",
                    },
                }
            },
            {"$sort": {"request_count": -1}},
            {"$limit": limit},
        ]

        results = list(collection.aggregate(pipeline))

        endpoints = []
        for result in results:
            response_times = [t for t in result.get("response_times", []) if t is not None]
            avg_response_time = (
                sum(response_times) / len(response_times) if response_times else None
            )
            request_count = result["request_count"]
            error_count = result["error_count"]
            error_rate = (error_count / request_count * 100) if request_count > 0 else 0.0

            endpoints.append(
                TopEndpointResponse(
                    endpoint=result["_id"],
                    request_count=request_count,
                    average_response_time_ms=round(avg_response_time, 2) if avg_response_time else None,
                    error_count=error_count,
                    error_rate=round(error_rate, 2),
                )
            )

        return TopEndpointsResponse(endpoints=endpoints, period_days=days)

    async def get_top_users(self, days: int = 30, limit: int = 10) -> TopUsersResponse:
        """Get top users by activity.

        Args:
            days: Number of days to analyze
            limit: Maximum number of results

        Returns:
            Top users response
        """
        db = mongodb_manager.get_database()
        collection = db.api_usage

        start_date = datetime.utcnow() - timedelta(days=days)

        pipeline = [
            {"$match": {"timestamp": {"$gte": start_date}}},
            {
                "$group": {
                    "_id": "$user_id",
                    "request_count": {"$sum": 1},
                    "query_count": {
                        "$sum": {"$cond": [{"$eq": ["$operation_type", "query"]}, 1, 0]}
                    },
                    "indexing_count": {
                        "$sum": {"$cond": [{"$eq": ["$operation_type", "index"]}, 1, 0]}
                    },
                    "storage_mb": {"$sum": "$operation_details.storage_mb"},
                    "plan": {"$first": "$plan"},
                }
            },
            {"$sort": {"request_count": -1}},
            {"$limit": limit},
        ]

        results = list(collection.aggregate(pipeline))

        users = []
        for result in results:
            user_id = str(result["_id"])
            user_doc = db.users.find_one({"_id": ObjectId(user_id)})
            email = user_doc.get("email") if user_doc else "unknown"

            users.append(
                TopUserResponse(
                    user_id=user_id,
                    email=email,
                    plan=result.get("plan", "professional"),
                    request_count=result["request_count"],
                    query_count=result["query_count"],
                    indexing_count=result["indexing_count"],
                    storage_mb=round(float(result.get("storage_mb", 0.0)), 2),
                )
            )

        return TopUsersResponse(users=users, period_days=days, limit=limit)


admin_analytics_service = AdminAnalyticsService()

