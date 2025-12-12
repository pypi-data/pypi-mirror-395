"""Organization usage analytics service."""

import logging
from datetime import datetime, timedelta
from typing import Any

from bson import ObjectId

from api.database.mongodb import mongodb_manager
from api.models.organization_usage import (
    DailyOrganizationUsage,
    MemberUsageBreakdown,
    OrganizationQuotaStatus,
    OrganizationUsageSummary,
    OrganizationUsageTrends,
)
from api.models.usage import IndexMetrics, QueryMetrics
from api.services.alert_service import AlertChannel, alert_service
from api.services.organization_quota_service import organization_quota_service
from api.services.plan_service import plan_service
from api.services.usage_aggregator import usage_aggregator
from api.exceptions import NotFoundError

logger = logging.getLogger(__name__)


class OrganizationAnalyticsService:
    """Service for organization-level usage analytics."""

    def __init__(self):
        """Initialize organization analytics service."""
        self._db = None

    @property
    def db(self):
        """Get database connection."""
        if self._db is None:
            mongodb_manager.connect()
            self._db = mongodb_manager.get_database()
        return self._db

    async def get_organization_usage_summary(
        self,
        organization_id: str,
        start_date: datetime,
        end_date: datetime,
    ) -> OrganizationUsageSummary:
        """Get organization usage summary with member breakdown.

        Args:
            organization_id: Organization ID
            start_date: Start date
            end_date: End date

        Returns:
            Organization usage summary
        """
        org = self.db.organizations.find_one({"_id": ObjectId(organization_id)})
        if not org:
            raise NotFoundError(
                message=f"Organization {organization_id} not found",
                user_message="Organization not found",
                error_code="ORGANIZATION_NOT_FOUND",
                details={"organization_id": organization_id}
            )

        usage_data = await organization_quota_service.get_organization_usage_summary(
            organization_id, start_date, end_date
        )

        members = list(
            self.db.organization_members.find(
                {"organization_id": ObjectId(organization_id), "status": "active"}
            )
        )

        member_breakdown_data = usage_data.get("member_breakdown", [])
        member_breakdown = []
        active_member_ids = set()

        for member_data in member_breakdown_data:
            member_doc = next(
                (m for m in members if str(m["user_id"]) == member_data["user_id"]), None
            )
            if not member_doc:
                continue

            user_id = member_data["user_id"]
            active_member_ids.add(user_id)

            member_usage = await usage_aggregator.aggregate_user_usage(
                user_id, start_date, end_date
            )

            total_requests = member_usage.get("total_requests", 0)
            successful_requests = member_usage.get("successful_requests", 0)
            success_rate = (
                (successful_requests / total_requests * 100) if total_requests > 0 else 0.0
            )

            member_breakdown.append(
                MemberUsageBreakdown(
                    user_id=user_id,
                    email=member_data.get("email", "unknown"),
                    full_name=member_data.get("full_name"),
                    role=member_doc.get("role", "member"),
                    queries=member_data.get("queries", 0),
                    indexes=member_data.get("indexes", 0),
                    storage_mb=member_data.get("storage_mb", 0.0),
                    total_requests=total_requests,
                    success_rate=round(success_rate, 2),
                    average_response_time_ms=member_usage.get("avg_response_time_ms"),
                )
            )

        total_usage = await usage_aggregator.aggregate_organization_usage(
            organization_id, start_date, end_date
        )

        success_pipeline = [
            {
                "$match": {
                    "organization_id": ObjectId(organization_id),
                    "timestamp": {"$gte": start_date, "$lte": end_date},
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_requests": {"$sum": 1},
                    "successful_requests": {"$sum": {"$cond": ["$success", 1, 0]}},
                    "failed_requests": {"$sum": {"$cond": ["$success", 0, 1]}},
                }
            },
        ]

        success_result = list(self.db.api_usage.aggregate(success_pipeline))
        if success_result:
            total_requests = success_result[0].get("total_requests", 0)
            successful_requests = success_result[0].get("successful_requests", 0)
            failed_requests = success_result[0].get("failed_requests", 0)
        else:
            total_requests = 0
            successful_requests = 0
            failed_requests = 0

        success_rate = (
            (successful_requests / total_requests * 100) if total_requests > 0 else 0.0
        )

        endpoint_pipeline = [
            {
                "$match": {
                    "organization_id": ObjectId(organization_id),
                    "timestamp": {"$gte": start_date, "$lte": end_date},
                }
            },
            {"$group": {"_id": "$endpoint", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
        ]

        endpoint_results = list(self.db.api_usage.aggregate(endpoint_pipeline))
        requests_by_endpoint = {r["_id"]: r["count"] for r in endpoint_results}

        status_pipeline = [
            {
                "$match": {
                    "organization_id": ObjectId(organization_id),
                    "timestamp": {"$gte": start_date, "$lte": end_date},
                }
            },
            {"$group": {"_id": "$status_code", "count": {"$sum": 1}}},
        ]

        status_results = list(self.db.api_usage.aggregate(status_pipeline))
        requests_by_status = {r["_id"]: r["count"] for r in status_results}

        response_time_pipeline = [
            {
                "$match": {
                    "organization_id": ObjectId(organization_id),
                    "timestamp": {"$gte": start_date, "$lte": end_date},
                    "performance.total_time_ms": {"$exists": True},
                }
            },
            {"$group": {"_id": None, "avg_time": {"$avg": "$performance.total_time_ms"}}},
        ]

        response_time_result = list(self.db.api_usage.aggregate(response_time_pipeline))
        avg_response_time = (
            response_time_result[0]["avg_time"] if response_time_result else None
        )

        compliance_queries = sum(
            m.queries for m in member_breakdown
        )
        knowledge_queries = 0
        total_queries = total_usage.get("total_queries", 0)

        return OrganizationUsageSummary(
            organization_id=organization_id,
            organization_name=org.get("name", "Unknown"),
            plan_id=org.get("plan_id", "team"),
            start_date=start_date,
            end_date=end_date,
            total_requests=total_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            success_rate=round(success_rate, 2),
            queries=QueryMetrics(
                compliance_queries=compliance_queries,
                knowledge_queries=knowledge_queries,
                total_queries=total_queries,
            ),
            indexes=IndexMetrics(
                repositories_indexed=total_usage.get("total_indexes", 0),
                documents_indexed=0,
                total_indexes=total_usage.get("total_indexes", 0),
                storage_mb=total_usage.get("total_storage_mb", 0.0),
            ),
            total_members=len(members),
            active_members=len(active_member_ids),
            requests_by_endpoint=requests_by_endpoint,
            requests_by_status=requests_by_status,
            average_response_time_ms=round(avg_response_time, 2) if avg_response_time else None,
            member_breakdown=member_breakdown,
        )

    async def get_daily_organization_usage(
        self,
        organization_id: str,
        days: int = 30,
    ) -> OrganizationUsageTrends:
        """Get daily organization usage trends.

        Args:
            organization_id: Organization ID
            days: Number of days to retrieve

        Returns:
            Organization usage trends
        """
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        org = self.db.organizations.find_one({"_id": ObjectId(organization_id)})
        if not org:
            raise NotFoundError(
                message=f"Organization {organization_id} not found",
                user_message="Organization not found",
                error_code="ORGANIZATION_NOT_FOUND",
                details={"organization_id": organization_id}
            )

        pipeline = [
            {
                "$match": {
                    "organization_id": ObjectId(organization_id),
                    "timestamp": {"$gte": start_date, "$lte": end_date},
                }
            },
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$timestamp",
                        }
                    },
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
                    "active_members": {"$addToSet": "$user_id"},
                }
            },
            {"$sort": {"_id": 1}},
        ]

        results = list(self.db.api_usage.aggregate(pipeline))

        daily_usage = []
        total_queries = 0
        total_indexes = 0
        total_storage_mb = 0.0
        peak_usage_day = None
        peak_usage_requests = 0

        for result in results:
            date_str = result["_id"]
            total_requests = result.get("total_requests", 0)
            queries = result.get("total_queries", 0)
            indexes = result.get("total_indexes", 0)
            storage_mb = result.get("total_storage_mb", 0.0)
            active_members = len(result.get("active_members", []))

            total_queries += queries
            total_indexes += indexes
            total_storage_mb += storage_mb

            if total_requests > peak_usage_requests:
                peak_usage_requests = total_requests
                peak_usage_day = date_str

            daily_usage.append(
                DailyOrganizationUsage(
                    date=date_str,
                    total_requests=total_requests,
                    queries=QueryMetrics(
                        compliance_queries=queries,
                        knowledge_queries=0,
                        total_queries=queries,
                    ),
                    indexes=IndexMetrics(
                        repositories_indexed=indexes,
                        documents_indexed=0,
                        total_indexes=indexes,
                        storage_mb=round(storage_mb, 2),
                    ),
                    active_members=active_members,
                )
            )

        return OrganizationUsageTrends(
            organization_id=organization_id,
            period_days=days,
            daily_usage=daily_usage,
            total_queries=total_queries,
            total_indexes=total_indexes,
            total_storage_mb=round(total_storage_mb, 2),
            peak_usage_day=peak_usage_day,
            peak_usage_requests=peak_usage_requests,
        )

    async def get_organization_quota_status(
        self,
        organization_id: str,
    ) -> OrganizationQuotaStatus:
        """Get organization quota status with member breakdown.

        Args:
            organization_id: Organization ID

        Returns:
            Organization quota status
        """
        org = self.db.organizations.find_one({"_id": ObjectId(organization_id)})
        if not org:
            raise NotFoundError(
                message=f"Organization {organization_id} not found",
                user_message="Organization not found",
                error_code="ORGANIZATION_NOT_FOUND",
                details={"organization_id": organization_id}
            )

        plan_id = org.get("plan_id", "team")
        plan = plan_service.get_plan(plan_id)
        if not plan:
            raise NotFoundError(
                message=f"Plan {plan_id} not found",
                user_message=f"Plan {plan_id} not found",
                error_code="PLAN_NOT_FOUND",
                details={"plan_id": plan_id, "organization_id": organization_id}
            )

        now = datetime.utcnow()
        start_of_month = datetime(now.year, now.month, 1)
        end_of_month = start_of_month + timedelta(days=32)
        end_of_month = end_of_month.replace(day=1) - timedelta(seconds=1)

        usage = await usage_aggregator.aggregate_organization_usage(
            organization_id, start_of_month, end_of_month
        )

        current_queries = usage.get("total_queries", 0)
        current_indexes = usage.get("total_indexes", 0)
        current_storage = usage.get("total_storage_mb", 0.0)

        query_limit = plan.limits.queries_per_month
        index_limit = plan.limits.indexes_per_month
        storage_limit = plan.limits.storage_mb

        query_percentage = (
            (current_queries / query_limit * 100) if query_limit != -1 and query_limit > 0 else 0.0
        )
        index_percentage = (
            (current_indexes / index_limit * 100) if index_limit != -1 and index_limit > 0 else 0.0
        )
        storage_percentage = (
            (current_storage / storage_limit * 100) if storage_limit != -1 and storage_limit > 0 else 0.0
        )

        member_breakdown = await organization_quota_service._get_member_usage_breakdown(
            organization_id, "queries"
        )

        member_breakdown_list = []
        for member_data in member_breakdown:
            member_doc = self.db.organization_members.find_one(
                {
                    "organization_id": ObjectId(organization_id),
                    "user_id": ObjectId(member_data["user_id"]),
                    "status": "active",
                }
            )
            if not member_doc:
                continue

            user = self.db.users.find_one(
                {"_id": ObjectId(member_data["user_id"])}, {"email": 1, "full_name": 1}
            )

            member_usage = await usage_aggregator.aggregate_user_usage(
                member_data["user_id"], start_of_month, end_of_month
            )

            member_breakdown_list.append(
                MemberUsageBreakdown(
                    user_id=member_data["user_id"],
                    email=user.get("email", "unknown") if user else "unknown",
                    full_name=user.get("full_name") if user else None,
                    role=member_doc.get("role", "member"),
                    queries=member_usage.get("total_queries", 0),
                    indexes=member_usage.get("total_indexes", 0),
                    storage_mb=member_usage.get("total_storage_mb", 0.0),
                    total_requests=member_usage.get("total_requests", 0),
                    success_rate=0.0,
                    average_response_time_ms=member_usage.get("avg_response_time_ms"),
                )
            )

        return OrganizationQuotaStatus(
            organization_id=organization_id,
            plan_id=plan_id,
            queries={
                "current": current_queries,
                "limit": query_limit,
                "percentage": round(query_percentage, 2),
            },
            indexes={
                "current": current_indexes,
                "limit": index_limit,
                "percentage": round(index_percentage, 2),
            },
            storage={
                "current": round(current_storage, 2),
                "limit": storage_limit,
                "percentage": round(storage_percentage, 2),
            },
            member_breakdown=member_breakdown_list,
        )

    async def check_usage_alerts(
        self,
        organization_id: str,
        alert_threshold_percent: float = 80.0,
        critical_threshold_percent: float = 95.0,
    ) -> list[dict[str, Any]]:
        """Check organization usage and create alerts if thresholds exceeded.

        Args:
            organization_id: Organization ID
            alert_threshold_percent: Alert threshold percentage (default: 80%)
            critical_threshold_percent: Critical threshold percentage (default: 95%)

        Returns:
            List of alerts created
        """
        quota_status = await self.get_organization_quota_status(organization_id)

        alerts_created = []

        query_percentage = quota_status.queries.get("percentage", 0.0)
        index_percentage = quota_status.indexes.get("percentage", 0.0)
        storage_percentage = quota_status.storage.get("percentage", 0.0)

        org = self.db.organizations.find_one({"_id": ObjectId(organization_id)})
        if not org:
            return alerts_created

        org_name = org.get("name", "Unknown")

        owners_and_admins = list(
            self.db.organization_members.find(
                {
                    "organization_id": ObjectId(organization_id),
                    "status": "active",
                    "role": {"$in": ["owner", "admin"]},
                },
                {"user_id": 1},
            )
        )

        if not owners_and_admins:
            logger.warning("No owners or admins found for organization %s", organization_id)
            return alerts_created

        for member in owners_and_admins:
            user_id = str(member["user_id"])

            if query_percentage >= critical_threshold_percent:
                try:
                    await alert_service.create_alert(
                        budget_id=None,
                        user_id=user_id,
                        alert_type="critical",
                        message=f"Organization '{org_name}' query quota critical: {quota_status.queries['current']}/{quota_status.queries['limit']} queries ({query_percentage:.1f}% used)",
                        utilization_percent=query_percentage,
                        channels=[AlertChannel.IN_APP, AlertChannel.EMAIL],
                    )
                    if not any(
                        a.get("type") == "critical" and a.get("metric") == "queries"
                        for a in alerts_created
                    ):
                        alerts_created.append(
                            {
                                "type": "critical",
                                "metric": "queries",
                                "percentage": query_percentage,
                                "message": f"Query quota critical: {query_percentage:.1f}% used",
                            }
                        )
                except Exception as e:
                    logger.warning("Failed to create query quota alert for user %s: %s", user_id, e)

            elif query_percentage >= alert_threshold_percent:
                try:
                    await alert_service.create_alert(
                        budget_id=None,
                        user_id=user_id,
                        alert_type="warning",
                        message=f"Organization '{org_name}' query quota warning: {quota_status.queries['current']}/{quota_status.queries['limit']} queries ({query_percentage:.1f}% used)",
                        utilization_percent=query_percentage,
                        channels=[AlertChannel.IN_APP],
                    )
                    if not any(
                        a.get("type") == "warning" and a.get("metric") == "queries"
                        for a in alerts_created
                    ):
                        alerts_created.append(
                            {
                                "type": "warning",
                                "metric": "queries",
                                "percentage": query_percentage,
                                "message": f"Query quota warning: {query_percentage:.1f}% used",
                            }
                        )
                except Exception as e:
                    logger.warning("Failed to create query quota alert for user %s: %s", user_id, e)

            if index_percentage >= critical_threshold_percent:
                try:
                    await alert_service.create_alert(
                        budget_id=None,
                        user_id=user_id,
                        alert_type="critical",
                        message=f"Organization '{org_name}' indexing quota critical: {quota_status.indexes['current']}/{quota_status.indexes['limit']} indexes ({index_percentage:.1f}% used)",
                        utilization_percent=index_percentage,
                        channels=[AlertChannel.IN_APP, AlertChannel.EMAIL],
                    )
                    if not any(
                        a.get("type") == "critical" and a.get("metric") == "indexes"
                        for a in alerts_created
                    ):
                        alerts_created.append(
                            {
                                "type": "critical",
                                "metric": "indexes",
                                "percentage": index_percentage,
                                "message": f"Indexing quota critical: {index_percentage:.1f}% used",
                            }
                        )
                except Exception as e:
                    logger.warning("Failed to create indexing quota alert for user %s: %s", user_id, e)

            elif index_percentage >= alert_threshold_percent:
                try:
                    await alert_service.create_alert(
                        budget_id=None,
                        user_id=user_id,
                        alert_type="warning",
                        message=f"Organization '{org_name}' indexing quota warning: {quota_status.indexes['current']}/{quota_status.indexes['limit']} indexes ({index_percentage:.1f}% used)",
                        utilization_percent=index_percentage,
                        channels=[AlertChannel.IN_APP],
                    )
                    if not any(
                        a.get("type") == "warning" and a.get("metric") == "indexes"
                        for a in alerts_created
                    ):
                        alerts_created.append(
                            {
                                "type": "warning",
                                "metric": "indexes",
                                "percentage": index_percentage,
                                "message": f"Indexing quota warning: {index_percentage:.1f}% used",
                            }
                        )
                except Exception as e:
                    logger.warning("Failed to create indexing quota alert for user %s: %s", user_id, e)

            if storage_percentage >= critical_threshold_percent:
                try:
                    await alert_service.create_alert(
                        budget_id=None,
                        user_id=user_id,
                        alert_type="critical",
                        message=f"Organization '{org_name}' storage quota critical: {quota_status.storage['current']:.2f}/{quota_status.storage['limit']} MB ({storage_percentage:.1f}% used)",
                        utilization_percent=storage_percentage,
                        channels=[AlertChannel.IN_APP, AlertChannel.EMAIL],
                    )
                    if not any(
                        a.get("type") == "critical" and a.get("metric") == "storage"
                        for a in alerts_created
                    ):
                        alerts_created.append(
                            {
                                "type": "critical",
                                "metric": "storage",
                                "percentage": storage_percentage,
                                "message": f"Storage quota critical: {storage_percentage:.1f}% used",
                            }
                        )
                except Exception as e:
                    logger.warning("Failed to create storage quota alert for user %s: %s", user_id, e)

            elif storage_percentage >= alert_threshold_percent:
                try:
                    await alert_service.create_alert(
                        budget_id=None,
                        user_id=user_id,
                        alert_type="warning",
                        message=f"Organization '{org_name}' storage quota warning: {quota_status.storage['current']:.2f}/{quota_status.storage['limit']} MB ({storage_percentage:.1f}% used)",
                        utilization_percent=storage_percentage,
                        channels=[AlertChannel.IN_APP],
                    )
                    if not any(
                        a.get("type") == "warning" and a.get("metric") == "storage"
                        for a in alerts_created
                    ):
                        alerts_created.append(
                            {
                                "type": "warning",
                                "metric": "storage",
                                "percentage": storage_percentage,
                                "message": f"Storage quota warning: {storage_percentage:.1f}% used",
                            }
                        )
                except Exception as e:
                    logger.warning("Failed to create storage quota alert for user %s: %s", user_id, e)

        return alerts_created


organization_analytics_service = OrganizationAnalyticsService()

