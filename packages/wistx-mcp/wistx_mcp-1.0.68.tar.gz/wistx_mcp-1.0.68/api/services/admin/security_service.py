"""Admin security service."""

import logging
from datetime import datetime, timedelta
from typing import Any

from bson import ObjectId

from api.database.mongodb import mongodb_manager
from api.models.admin.security import (
    AdminAPIKeyResponse,
    APIKeyListQuery,
    APIKeyListResponse,
    IPMonitoringEntry,
    IPMonitoringResponse,
    SecurityEventsQuery,
    SecurityEventsSummaryResponse,
    SecurityEventSummary,
)
from api.models.audit_log import AuditEventType, AuditLogSeverity
from api.services.audit_log_service import audit_log_service

logger = logging.getLogger(__name__)


class AdminSecurityService:
    """Service for admin security operations."""

    async def get_security_events_summary(
        self, query: SecurityEventsQuery
    ) -> SecurityEventsSummaryResponse:
        """Get security events summary.

        Args:
            query: Query parameters

        Returns:
            Security events summary response
        """
        security_event_types = [
            AuditEventType.AUTHENTICATION_FAILURE,
            AuditEventType.UNAUTHORIZED_ACCESS_ATTEMPT,
            AuditEventType.RATE_LIMIT_EXCEEDED,
            AuditEventType.SUSPICIOUS_ACTIVITY,
            AuditEventType.SECURITY_ALERT,
            AuditEventType.API_KEY_DELETED,
            AuditEventType.TOKEN_REVOKED,
        ]

        start_date = query.start_date or (datetime.utcnow() - timedelta(days=30))
        end_date = query.end_date or datetime.utcnow()

        audit_query = {
            "event_type": {"$in": [et.value for et in security_event_types]},
            "timestamp": {"$gte": start_date, "$lte": end_date},
        }

        if query.severity:
            audit_query["severity"] = query.severity.value

        db = mongodb_manager.get_database()
        collection = db.security_audit_logs

        total_events = collection.count_documents(audit_query)

        pipeline = [
            {"$match": audit_query},
            {
                "$group": {
                    "_id": "$event_type",
                    "count": {"$sum": 1},
                    "severity": {"$first": "$severity"},
                }
            },
            {"$sort": {"count": -1}},
        ]

        results = list(collection.aggregate(pipeline))

        events_by_type = [
            SecurityEventSummary(
                event_type=AuditEventType(result["_id"]),
                count=result["count"],
                severity=AuditLogSeverity(result["severity"]),
            )
            for result in results
        ]

        severity_pipeline = [
            {"$match": audit_query},
            {"$group": {"_id": "$severity", "count": {"$sum": 1}}},
        ]

        severity_results = list(collection.aggregate(severity_pipeline))
        events_by_severity = {
            result["_id"]: result["count"] for result in severity_results
        }

        period_days = (end_date - start_date).days

        return SecurityEventsSummaryResponse(
            total_events=total_events,
            events_by_type=events_by_type,
            events_by_severity=events_by_severity,
            period_days=period_days,
        )

    async def get_ip_monitoring(self, days: int = 7) -> IPMonitoringResponse:
        """Get IP address monitoring data.

        Args:
            days: Number of days to analyze

        Returns:
            IP monitoring response
        """
        db = mongodb_manager.get_database()
        collection = db.security_audit_logs

        start_date = datetime.utcnow() - timedelta(days=days)

        pipeline = [
            {"$match": {"timestamp": {"$gte": start_date}, "ip_address": {"$exists": True, "$ne": None}}},
            {
                "$group": {
                    "_id": "$ip_address",
                    "request_count": {"$sum": 1},
                    "failed_auth_count": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$event_type", AuditEventType.AUTHENTICATION_FAILURE.value]},
                                1,
                                0,
                            ]
                        }
                    },
                    "rate_limit_violations": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$event_type", AuditEventType.RATE_LIMIT_EXCEEDED.value]},
                                1,
                                0,
                            ]
                        }
                    },
                    "last_seen": {"$max": "$timestamp"},
                    "user_ids": {"$addToSet": "$user_id"},
                }
            },
            {"$sort": {"request_count": -1}},
            {"$limit": 100},
        ]

        results = list(collection.aggregate(pipeline))

        ips = []
        for result in results:
            user_ids = [str(uid) for uid in result.get("user_ids", []) if uid]
            ips.append(
                IPMonitoringEntry(
                    ip_address=result["_id"],
                    request_count=result["request_count"],
                    failed_auth_count=result["failed_auth_count"],
                    rate_limit_violations=result["rate_limit_violations"],
                    last_seen=result["last_seen"],
                    user_ids=user_ids,
                )
            )

        total_unique_ips = collection.distinct("ip_address", {"timestamp": {"$gte": start_date}})
        total_unique_ips = len([ip for ip in total_unique_ips if ip])

        return IPMonitoringResponse(
            ips=ips,
            total_unique_ips=total_unique_ips,
            period_days=days,
        )

    async def list_api_keys(self, query: APIKeyListQuery) -> APIKeyListResponse:
        """List all API keys with filters.

        Args:
            query: Query parameters

        Returns:
            API key list response
        """
        db = mongodb_manager.get_database()
        collection = db.api_keys

        filter_query: dict[str, Any] = {}

        if query.user_id:
            filter_query["user_id"] = ObjectId(query.user_id)

        if query.organization_id:
            filter_query["organization_id"] = ObjectId(query.organization_id)

        if query.is_active is not None:
            filter_query["is_active"] = query.is_active

        if query.plan:
            filter_query["plan"] = query.plan

        if query.search:
            search_term = query.search.lower()
            filter_query["$or"] = [
                {"key_prefix": {"$regex": search_term, "$options": "i"}},
                {"name": {"$regex": search_term, "$options": "i"}},
            ]

        cursor = (
            collection.find(filter_query)
            .sort("created_at", -1)
            .skip(query.offset)
            .limit(query.limit)
        )

        api_keys = []
        user_cache: dict[str, str] = {}

        for doc in cursor:
            user_id = str(doc["user_id"])

            if user_id not in user_cache:
                user_doc = db.users.find_one({"_id": doc["user_id"]})
                user_cache[user_id] = user_doc.get("email") if user_doc else None

            api_keys.append(
                AdminAPIKeyResponse(
                    api_key_id=str(doc["_id"]),
                    key_prefix=doc.get("key_prefix", ""),
                    name=doc.get("name"),
                    user_id=user_id,
                    user_email=user_cache[user_id],
                    organization_id=str(doc["organization_id"]) if doc.get("organization_id") else None,
                    plan=doc.get("plan", "professional"),
                    is_active=doc.get("is_active", False),
                    is_test_key=doc.get("is_test_key", False),
                    usage_count=doc.get("usage_count", 0),
                    last_used_at=doc.get("last_used_at"),
                    last_used_ip=doc.get("last_used_ip"),
                    created_at=doc.get("created_at", datetime.utcnow()),
                    expires_at=doc.get("expires_at"),
                    revoked_at=doc.get("revoked_at"),
                )
            )

        total = collection.count_documents(filter_query)

        return APIKeyListResponse(
            api_keys=api_keys,
            total=total,
            limit=query.limit,
            offset=query.offset,
        )

    async def revoke_api_key_admin(
        self, api_key_id: str, reason: str | None = None, admin_user_info: dict[str, Any] | None = None
    ) -> AdminAPIKeyResponse:
        """Revoke API key (admin override).

        Args:
            api_key_id: API key ID
            reason: Revocation reason
            admin_user_info: Admin user information for audit logging

        Returns:
            Revoked API key response

        Raises:
            ValueError: If API key not found
        """
        db = mongodb_manager.get_database()
        collection = db.api_keys

        from api.exceptions import NotFoundError
        
        api_key_doc = collection.find_one({"_id": ObjectId(api_key_id)})
        if not api_key_doc:
            raise NotFoundError(
                message=f"API key not found: {api_key_id}",
                user_message="API key not found",
                error_code="API_KEY_NOT_FOUND",
                details={"api_key_id": api_key_id}
            )

        collection.update_one(
            {"_id": ObjectId(api_key_id)},
            {
                "$set": {
                    "is_active": False,
                    "revoked_at": datetime.utcnow(),
                    "revoked_reason": reason or "Revoked by admin",
                }
            },
        )

        logger.warning("API key %s revoked by admin: %s", api_key_id, reason)

        user_doc = db.users.find_one({"_id": api_key_doc["user_id"]})
        user_email = user_doc.get("email") if user_doc else None

        if admin_user_info:
            audit_log_service.log_event(
                event_type=AuditEventType.API_KEY_DELETED,
                severity=AuditLogSeverity.HIGH,
                message=f"Admin revoked API key {api_key_id}: {reason or 'Revoked by admin'}",
                success=True,
                user_id=admin_user_info.get("user_id"),
                api_key_id=admin_user_info.get("api_key_id"),
                organization_id=admin_user_info.get("organization_id"),
                endpoint=f"/admin/security/api-keys/{api_key_id}/revoke",
                method="POST",
                status_code=200,
                details={
                    "target_api_key_id": api_key_id,
                    "target_user_id": str(api_key_doc["user_id"]),
                    "target_user_email": user_email,
                    "key_prefix": api_key_doc.get("key_prefix", ""),
                    "revocation_reason": reason or "Revoked by admin",
                    "admin_email": admin_user_info.get("email"),
                },
                compliance_tags=["SOC2", "PCI-DSS-10"],
            )

        return AdminAPIKeyResponse(
            api_key_id=api_key_id,
            key_prefix=api_key_doc.get("key_prefix", ""),
            name=api_key_doc.get("name"),
            user_id=str(api_key_doc["user_id"]),
            user_email=user_email,
            organization_id=str(api_key_doc["organization_id"]) if api_key_doc.get("organization_id") else None,
            plan=api_key_doc.get("plan", "professional"),
            is_active=False,
            is_test_key=api_key_doc.get("is_test_key", False),
            usage_count=api_key_doc.get("usage_count", 0),
            last_used_at=api_key_doc.get("last_used_at"),
            last_used_ip=api_key_doc.get("last_used_ip"),
            created_at=api_key_doc.get("created_at", datetime.utcnow()),
            expires_at=api_key_doc.get("expires_at"),
            revoked_at=datetime.utcnow(),
        )


admin_security_service = AdminSecurityService()

