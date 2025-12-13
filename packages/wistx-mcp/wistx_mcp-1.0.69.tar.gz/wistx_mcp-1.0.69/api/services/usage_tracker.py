"""Usage tracking service."""

import logging
import secrets
from datetime import datetime, timedelta
from typing import Any, Optional

from bson import ObjectId

from api.database.mongodb import mongodb_manager
from api.models.usage import APIUsageRequest, IndexMetrics, QueryMetrics

logger = logging.getLogger(__name__)


class UsageTracker:
    """Production-ready usage tracking service."""

    async def track_request(self, usage_request: APIUsageRequest) -> None:
        """Track API request usage.

        Args:
            usage_request: Usage request data
        """
        db = mongodb_manager.get_database()
        collection = db.api_usage

        usage_doc = {
            "request_id": usage_request.request_id,
            "user_id": ObjectId(usage_request.user_id),
            "api_key_id": ObjectId(usage_request.api_key_id) if usage_request.api_key_id else None,
            "organization_id": ObjectId(usage_request.organization_id) if usage_request.organization_id else None,
            "plan": usage_request.plan,
            "timestamp": datetime.utcnow(),
            "date": datetime.utcnow().date().isoformat(),
            "endpoint": usage_request.endpoint,
            "method": usage_request.method,
            "operation_type": usage_request.operation_type,
            "operation_details": usage_request.operation_details,
            "status_code": usage_request.status_code,
            "success": usage_request.success,
            "ip_address": usage_request.ip_address,
            "user_agent": usage_request.user_agent,
        }

        if usage_request.performance:
            usage_doc["performance"] = usage_request.performance.model_dump()

        try:
            collection.insert_one(usage_doc)

            if usage_request.organization_id:
                from api.services.organization_quota_service import organization_quota_service

                if usage_request.operation_type == "query":
                    await organization_quota_service.update_cache_after_usage(
                        usage_request.organization_id, "queries", 1
                    )
                elif usage_request.operation_type == "index":
                    await organization_quota_service.update_cache_after_usage(
                        usage_request.organization_id, "indexes", 1
                    )
                    storage_mb = usage_request.operation_details.get("storage_mb", 0.0)
                    if storage_mb:
                        await organization_quota_service.update_cache_after_usage(
                            usage_request.organization_id, "storage", storage_mb
                        )
        except Exception as e:
            logger.error("Failed to track usage: %s", e, exc_info=True)

    async def track_indexing_operation(
        self,
        user_id: str,
        api_key_id: str,
        index_type: str,
        resource_id: str,
        documents_count: int = 0,
        storage_mb: float = 0.0,
        organization_id: Optional[str] = None,
        plan: str = "professional",
    ) -> None:
        """Track indexing operation.

        Args:
            user_id: User ID
            api_key_id: API key ID
            index_type: Type of index (repository, document, documentation)
            resource_id: Resource ID that was indexed
            documents_count: Number of documents indexed
            storage_mb: Storage used in MB
            organization_id: Organization ID
            plan: User plan
        """
        request_id = f"idx_{secrets.token_hex(12)}"

        usage_request = APIUsageRequest(
            request_id=request_id,
            user_id=user_id,
            api_key_id=api_key_id,
            organization_id=organization_id,
            plan=plan,
            endpoint="/v1/indexing",
            method="POST",
            operation_type="index",
            operation_details={
                "index_type": index_type,
                "resource_id": resource_id,
                "documents_count": documents_count,
                "storage_mb": storage_mb,
            },
            status_code=200,
            success=True,
        )

        await self.track_request(usage_request)

    async def get_usage_summary(
        self,
        user_id: str,
        start_date: datetime,
        end_date: datetime,
        organization_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get usage summary for a time period.

        Args:
            user_id: User ID
            start_date: Start date
            end_date: End date
            organization_id: Optional organization ID filter

        Returns:
            Dictionary with usage summary
        """
        db = mongodb_manager.get_database()
        collection = db.api_usage

        query: dict[str, Any] = {
            "user_id": ObjectId(user_id),
            "timestamp": {
                "$gte": start_date,
                "$lte": end_date,
            },
        }

        if organization_id:
            query["organization_id"] = ObjectId(organization_id)

        pipeline = [
            {"$match": query},
            {
                "$group": {
                    "_id": None,
                    "total_requests": {"$sum": 1},
                    "compliance_queries": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$operation_type", "query"]},
                                {"$cond": [{"$eq": ["$endpoint", "/v1/compliance/requirements"]}, 1, 0]},
                                0,
                            ]
                        }
                    },
                    "knowledge_queries": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$operation_type", "query"]},
                                {"$cond": [{"$eq": ["$endpoint", "/v1/knowledge/research"]}, 1, 0]},
                                0,
                            ]
                        }
                    },
                    "index_operations": {
                        "$sum": {"$cond": [{"$eq": ["$operation_type", "index"]}, 1, 0]},
                    },
                    "repositories_indexed": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$operation_details.index_type", "repository"]},
                                1,
                                0,
                            ]
                        }
                    },
                    "documents_indexed": {
                        "$sum": "$operation_details.documents_count",
                    },
                    "storage_mb": {
                        "$sum": "$operation_details.storage_mb",
                    },
                    "requests_by_endpoint": {
                        "$push": "$endpoint",
                    },
                    "requests_by_status": {
                        "$push": "$status_code",
                    },
                    "response_times": {
                        "$push": "$performance.total_time_ms",
                    },
                }
            },
        ]

        result = list(collection.aggregate(pipeline))

        if not result:
            return {
                "total_requests": 0,
                "queries": {
                    "compliance_queries": 0,
                    "knowledge_queries": 0,
                    "total_queries": 0,
                },
                "indexes": {
                    "repositories_indexed": 0,
                    "documents_indexed": 0,
                    "total_indexes": 0,
                    "storage_mb": 0.0,
                },
                "requests_by_endpoint": {},
                "requests_by_status": {},
                "average_response_time_ms": None,
            }

        data = result[0]

        endpoint_counts: dict[str, int] = {}
        for endpoint in data.get("requests_by_endpoint", []):
            endpoint_counts[endpoint] = endpoint_counts.get(endpoint, 0) + 1

        status_counts: dict[int, int] = {}
        for status in data.get("requests_by_status", []):
            status_counts[status] = status_counts.get(status, 0) + 1

        response_times = [t for t in data.get("response_times", []) if t is not None]
        avg_response_time = sum(response_times) / len(response_times) if response_times else None

        compliance_queries = data.get("compliance_queries", 0)
        knowledge_queries = data.get("knowledge_queries", 0)
        total_queries = compliance_queries + knowledge_queries

        repositories_indexed = data.get("repositories_indexed", 0)
        documents_indexed = int(data.get("documents_indexed", 0))
        total_indexes = data.get("index_operations", 0)
        storage_mb = float(data.get("storage_mb", 0.0))

        return {
            "total_requests": data.get("total_requests", 0),
            "queries": {
                "compliance_queries": compliance_queries,
                "knowledge_queries": knowledge_queries,
                "total_queries": total_queries,
            },
            "indexes": {
                "repositories_indexed": repositories_indexed,
                "documents_indexed": documents_indexed,
                "total_indexes": total_indexes,
                "storage_mb": round(storage_mb, 2),
            },
            "requests_by_endpoint": endpoint_counts,
            "requests_by_status": status_counts,
            "average_response_time_ms": round(avg_response_time, 2) if avg_response_time else None,
        }

    async def get_daily_usage(
        self,
        user_id: str,
        days: int = 30,
        organization_id: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """Get daily usage for the last N days.

        Args:
            user_id: User ID
            days: Number of days to retrieve
            organization_id: Optional organization ID filter

        Returns:
            List of daily usage summaries
        """
        db = mongodb_manager.get_database()
        collection = db.api_usage

        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        query: dict[str, Any] = {
            "user_id": ObjectId(user_id),
            "timestamp": {
                "$gte": start_date,
                "$lte": end_date,
            },
        }

        if organization_id:
            query["organization_id"] = ObjectId(organization_id)

        pipeline = [
            {"$match": query},
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$timestamp",
                        }
                    },
                    "total_requests": {"$sum": 1},
                    "compliance_queries": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$operation_type", "query"]},
                                {"$cond": [{"$eq": ["$endpoint", "/v1/compliance/requirements"]}, 1, 0]},
                                0,
                            ]
                        }
                    },
                    "knowledge_queries": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$operation_type", "query"]},
                                {"$cond": [{"$eq": ["$endpoint", "/v1/knowledge/research"]}, 1, 0]},
                                0,
                            ]
                        }
                    },
                    "repositories_indexed": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$operation_details.index_type", "repository"]},
                                1,
                                0,
                            ]
                        }
                    },
                    "documents_indexed": {
                        "$sum": "$operation_details.documents_count",
                    },
                    "storage_mb": {
                        "$sum": "$operation_details.storage_mb",
                    },
                }
            },
            {"$sort": {"_id": 1}},
        ]

        results = list(collection.aggregate(pipeline))

        daily_data = [
            {
                "date": result["_id"],
                "total_requests": result.get("total_requests", 0),
                "queries": {
                    "compliance_queries": result.get("compliance_queries", 0),
                    "knowledge_queries": result.get("knowledge_queries", 0),
                    "total_queries": result.get("compliance_queries", 0) + result.get("knowledge_queries", 0),
                },
                "indexes": {
                    "repositories_indexed": result.get("repositories_indexed", 0),
                    "documents_indexed": int(result.get("documents_indexed", 0)),
                    "total_indexes": result.get("repositories_indexed", 0),
                    "storage_mb": round(float(result.get("storage_mb", 0.0)), 2),
                },
            }
            for result in results
        ]
        
        daily_data.sort(key=lambda x: x["date"])
        
        return daily_data


usage_tracker = UsageTracker()
