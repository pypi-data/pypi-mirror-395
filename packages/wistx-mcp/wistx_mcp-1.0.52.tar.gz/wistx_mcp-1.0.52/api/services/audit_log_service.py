"""Security audit logging service for compliance and security."""

import logging
import uuid
from datetime import datetime, timedelta
from typing import Any

from api.database.mongodb import mongodb_manager
from api.models.audit_log import (
    AuditEventType,
    AuditLog,
    AuditLogQuery,
    AuditLogResponse,
    AuditLogSeverity,
)

logger = logging.getLogger(__name__)

AUDIT_LOG_RETENTION_DAYS = 365


class AuditLogService:
    """Service for security audit logging.

    Provides comprehensive audit logging for compliance (PCI-DSS, HIPAA, SOC2)
    and security incident investigation.
    """

    def __init__(self):
        """Initialize audit log service."""
        self._db = None
        self._initialized = False

    @property
    def db(self):
        """Lazy initialization of database connection."""
        if self._db is None:
            try:
                self._db = mongodb_manager.get_database()
                if not self._initialized:
                    self._ensure_collection()
                    self._initialized = True
            except Exception as e:
                logger.warning("Failed to connect to MongoDB for audit logging: %s", e)
                raise
        return self._db

    def _ensure_collection(self) -> None:
        """Ensure audit log collection exists with proper indexes."""
        collection_name = "security_audit_logs"
        if collection_name not in self.db.list_collection_names():
            self.db.create_collection(collection_name)
            logger.info("Created collection: %s", collection_name)

        collection = self.db[collection_name]

        indexes = [
            [("event_id", 1)],
            [("timestamp", -1)],
            [("event_type", 1), ("timestamp", -1)],
            [("user_id", 1), ("timestamp", -1)],
            [("api_key_id", 1), ("timestamp", -1)],
            [("organization_id", 1), ("timestamp", -1)],
            [("ip_address", 1), ("timestamp", -1)],
            [("severity", 1), ("timestamp", -1)],
            [("success", 1), ("timestamp", -1)],
            [("compliance_tags", 1), ("timestamp", -1)],
            [("request_id", 1)],
        ]

        existing_indexes = collection.list_indexes()
        existing_index_names = [idx["name"] for idx in existing_indexes]

        for index_spec in indexes:
            index_name = "_".join([f"{field}_{direction}" for field, direction in index_spec])
            if index_name not in existing_index_names:
                try:
                    collection.create_index(index_spec, name=index_name, background=True)
                    logger.debug("Created index: %s", index_name)
                except Exception as e:
                    logger.warning("Failed to create index %s: %s", index_name, e)

        try:
            retention_date = datetime.utcnow() - timedelta(days=AUDIT_LOG_RETENTION_DAYS)
            collection.create_index(
                [("timestamp", 1)],
                name="ttl_index",
                expireAfterSeconds=AUDIT_LOG_RETENTION_DAYS * 24 * 60 * 60,
                partialFilterExpression={"timestamp": {"$lt": retention_date}},
                background=True,
            )
        except Exception as e:
            logger.debug("TTL index may already exist or failed: %s", e)

    def log_event(
        self,
        event_type: AuditEventType,
        severity: AuditLogSeverity,
        message: str,
        success: bool,
        user_id: str | None = None,
        api_key_id: str | None = None,
        organization_id: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        request_id: str | None = None,
        endpoint: str | None = None,
        method: str | None = None,
        status_code: int | None = None,
        details: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        compliance_tags: list[str] | None = None,
    ) -> str:
        """Log a security audit event.

        Args:
            event_type: Type of audit event
            severity: Event severity level
            message: Human-readable event message
            success: Whether operation was successful
            user_id: Optional user ID
            api_key_id: Optional API key ID
            organization_id: Optional organization ID
            ip_address: Optional client IP address
            user_agent: Optional user agent string
            request_id: Optional request ID for correlation
            endpoint: Optional API endpoint or MCP tool name
            method: Optional HTTP method
            status_code: Optional HTTP status code
            details: Optional additional event details
            metadata: Optional additional metadata
            compliance_tags: Optional compliance tags (PCI-DSS, HIPAA, etc.)

        Returns:
            Event ID
        """
        event_id = str(uuid.uuid4())

        audit_log = AuditLog(
            event_id=event_id,
            event_type=event_type,
            severity=severity,
            timestamp=datetime.utcnow(),
            user_id=user_id,
            api_key_id=api_key_id,
            organization_id=organization_id,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            success=success,
            message=message,
            details=details or {},
            metadata=metadata or {},
            compliance_tags=compliance_tags or [],
        )

        try:
            self.db.security_audit_logs.insert_one(audit_log.model_dump())
            logger.debug("Audit log created: %s [type=%s, severity=%s]", event_id, event_type.value, severity.value)
        except Exception as e:
            logger.error("Failed to create audit log: %s", e, exc_info=True)

        return event_id

    def query_logs(self, query: AuditLogQuery) -> AuditLogResponse:
        """Query audit logs with filters.

        Args:
            query: Query parameters

        Returns:
            Audit log response with matching entries
        """
        filter_query: dict[str, Any] = {}

        if query.event_types:
            event_type_values = [et.value if hasattr(et, "value") else str(et) for et in query.event_types]
            filter_query["event_type"] = {"$in": event_type_values}
            logger.debug("Filtering by event types: %s", event_type_values)

        if query.severity:
            filter_query["severity"] = query.severity.value if hasattr(query.severity, "value") else str(query.severity)

        if query.user_id:
            filter_query["user_id"] = query.user_id

        if query.api_key_id:
            filter_query["api_key_id"] = query.api_key_id

        if query.organization_id:
            filter_query["organization_id"] = query.organization_id

        if query.ip_address:
            filter_query["ip_address"] = query.ip_address

        if query.start_date or query.end_date:
            filter_query["timestamp"] = {}
            if query.start_date:
                filter_query["timestamp"]["$gte"] = query.start_date
            if query.end_date:
                filter_query["timestamp"]["$lte"] = query.end_date

        logger.debug("MongoDB filter query: %s", filter_query)

        try:
            cursor = (
                self.db.security_audit_logs.find(filter_query)
                .sort("timestamp", -1)
                .skip(query.offset)
                .limit(query.limit)
            )

            logs = [AuditLog(**doc) for doc in cursor]

            total = self.db.security_audit_logs.count_documents(filter_query)

            logger.debug("Query results: total=%d, returned=%d, offset=%d, limit=%d", total, len(logs), query.offset, query.limit)

            return AuditLogResponse(
                logs=logs,
                total=total,
                limit=query.limit,
                offset=query.offset,
            )
        except Exception as e:
            logger.error("Failed to query audit logs: %s", e, exc_info=True)
            return AuditLogResponse(logs=[], total=0, limit=query.limit, offset=query.offset)

    def get_security_events(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        severity: AuditLogSeverity | None = None,
        limit: int = 100,
    ) -> list[AuditLog]:
        """Get security-related events.

        Args:
            start_date: Optional start date
            end_date: Optional end date
            severity: Optional severity filter
            limit: Maximum number of results

        Returns:
            List of security audit logs
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

        query = AuditLogQuery(
            event_types=security_event_types,
            severity=severity,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
        )

        response = self.query_logs(query)
        return response.logs

    def get_user_audit_trail(
        self,
        user_id: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[AuditLog]:
        """Get audit trail for a specific user.

        Args:
            user_id: User ID
            start_date: Optional start date
            end_date: Optional end date
            limit: Maximum number of results
            offset: Offset for pagination

        Returns:
            List of audit logs for the user
        """
        query = AuditLogQuery(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset,
        )

        response = self.query_logs(query)
        return response.logs

    def get_compliance_audit_trail(
        self,
        compliance_tag: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int = 1000,
    ) -> list[AuditLog]:
        """Get audit trail for compliance requirements.

        Args:
            compliance_tag: Compliance tag (PCI-DSS, HIPAA, SOC2, etc.)
            start_date: Optional start date
            end_date: Optional end date
            limit: Maximum number of results

        Returns:
            List of audit logs tagged with compliance requirement
        """
        filter_query: dict[str, Any] = {
            "compliance_tags": compliance_tag,
        }

        if start_date or end_date:
            filter_query["timestamp"] = {}
            if start_date:
                filter_query["timestamp"]["$gte"] = start_date
            if end_date:
                filter_query["timestamp"]["$lte"] = end_date

        try:
            cursor = (
                self.db.security_audit_logs.find(filter_query)
                .sort("timestamp", -1)
                .limit(limit)
            )

            return [AuditLog(**doc) for doc in cursor]
        except Exception as e:
            logger.error("Failed to get compliance audit trail: %s", e, exc_info=True)
            return []


_audit_log_service_instance: AuditLogService | None = None


class _AuditLogServiceProxy:
    """Proxy for lazy initialization of audit log service."""

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to audit log service instance."""
        global _audit_log_service_instance
        if _audit_log_service_instance is None:
            _audit_log_service_instance = AuditLogService()
        return getattr(_audit_log_service_instance, name)


audit_log_service = _AuditLogServiceProxy()

