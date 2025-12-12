"""Security event logging system with alerting and audit trail."""

import json
import logging
import time
from datetime import datetime
from enum import Enum
from typing import Any

from contextvars import ContextVar

from wistx_mcp.tools.lib.request_context import get_request_context

logger = logging.getLogger(__name__)

request_id_var: ContextVar[str] = ContextVar("request_id", default="")


class SecurityEventType(Enum):
    """Security event types."""

    AUTHENTICATION_SUCCESS = "auth_success"
    AUTHENTICATION_FAILURE = "auth_failure"
    AUTHORIZATION_DENIED = "authz_denied"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    RESOURCE_ACCESS_DENIED = "resource_access_denied"
    TOOL_EXECUTION = "tool_execution"
    SECURITY_POLICY_VIOLATION = "security_policy_violation"


class SecurityEventLogger:
    """Security event logger with alerting and audit trail."""

    async def log_security_event(
        self,
        event_type: SecurityEventType,
        user_id: str | None = None,
        tool_name: str | None = None,
        severity: str = "INFO",
        details: dict[str, Any] | None = None,
        alert: bool = False,
    ) -> None:
        """Log security event.

        Args:
            event_type: Type of security event
            user_id: User ID associated with event
            tool_name: Tool name if applicable
            severity: Event severity (CRITICAL, HIGH, MEDIUM, INFO)
            details: Additional event details
            alert: Whether to send alert
        """
        request_id = request_id_var.get() or get_request_context().get("request_id", "")

        event = {
            "timestamp": time.time(),
            "event_type": event_type.value,
            "user_id": user_id,
            "tool_name": tool_name,
            "severity": severity,
            "details": details or {},
            "request_id": request_id,
        }

        if severity == "CRITICAL":
            logger.critical("Security event: %s", json.dumps(event))
        elif severity == "HIGH":
            logger.error("Security event: %s", json.dumps(event))
        elif severity == "MEDIUM":
            logger.warning("Security event: %s", json.dumps(event))
        else:
            logger.info("Security event: %s", json.dumps(event))

        if alert:
            await self._send_alert(event)

        await self._store_audit_log(event)

    async def _send_alert(self, event: dict[str, Any]) -> None:
        """Send security alert.

        Args:
            event: Event dictionary
        """
        try:
            from wistx_mcp.config import settings

            alert_webhook_url = getattr(settings, "alert_webhook_url", None)
            if not alert_webhook_url:
                return

            import httpx

            async with httpx.AsyncClient(timeout=5.0) as client:
                await client.post(
                    alert_webhook_url,
                    json={
                        "event_type": event["event_type"],
                        "severity": event["severity"],
                        "user_id": event.get("user_id"),
                        "tool_name": event.get("tool_name"),
                        "timestamp": datetime.utcnow().isoformat(),
                        "details": event.get("details", {}),
                    },
                )
        except Exception as e:
            logger.warning("Failed to send security alert: %s", e)

    async def _store_audit_log(self, event: dict[str, Any]) -> None:
        """Store event in audit log database.

        Args:
            event: Event dictionary
        """
        try:
            from wistx_mcp.tools.lib.mongodb_client import get_mongodb_client

            mongodb_client = await get_mongodb_client()
            await mongodb_client.connect()

            if mongodb_client.database:
                await mongodb_client.database.security_audit_log.insert_one({
                    **event,
                    "stored_at": datetime.utcnow(),
                })
        except Exception as e:
            logger.debug("Failed to store audit log (MongoDB may not be available): %s", e)


_security_logger: SecurityEventLogger | None = None


def get_security_logger() -> SecurityEventLogger:
    """Get global security logger instance.

    Returns:
        SecurityEventLogger instance
    """
    global _security_logger
    if _security_logger is None:
        _security_logger = SecurityEventLogger()
    return _security_logger

