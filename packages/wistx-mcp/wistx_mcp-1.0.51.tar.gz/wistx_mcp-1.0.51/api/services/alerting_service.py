"""Alerting service for critical events."""

import logging
from datetime import datetime
from enum import Enum
from typing import Any

from api.database.mongodb import mongodb_manager
from api.config import settings

logger = logging.getLogger(__name__)


class AlertLevel(str, Enum):
    """Alert severity levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AlertType(str, Enum):
    """Alert types."""

    ERROR = "error"
    PERFORMANCE = "performance"
    SECURITY = "security"
    QUOTA = "quota"
    SYSTEM = "system"
    DATABASE = "database"


class AlertingService:
    """Service for managing alerts and notifications."""

    def __init__(self):
        """Initialize alerting service."""
        self.db = mongodb_manager.get_database()
        self._ensure_collections()

    def _ensure_collections(self) -> None:
        """Ensure alert collections exist."""
        collections = ["alerts", "alert_preferences"]
        for collection_name in collections:
            if collection_name not in self.db.list_collection_names():
                self.db.create_collection(collection_name)
                logger.debug("Created collection: %s", collection_name)

    async def create_alert(
        self,
        alert_type: AlertType,
        level: AlertLevel,
        title: str,
        message: str,
        metadata: dict[str, Any] | None = None,
        user_id: str | None = None,
    ) -> str:
        """Create an alert.

        Args:
            alert_type: Type of alert
            level: Alert severity level
            title: Alert title
            message: Alert message
            metadata: Optional metadata
            user_id: Optional user ID (for user-specific alerts)

        Returns:
            Alert ID
        """
        alert = {
            "alert_type": alert_type.value,
            "level": level.value,
            "title": title,
            "message": message,
            "metadata": metadata or {},
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "acknowledged": False,
            "acknowledged_at": None,
            "resolved": False,
            "resolved_at": None,
        }

        result = self.db.alerts.insert_one(alert)
        alert_id = str(result.inserted_id)

        logger.info(
            "Alert created: %s [type=%s, level=%s, id=%s]",
            title,
            alert_type.value,
            level.value,
            alert_id,
        )

        if level in (AlertLevel.CRITICAL, AlertLevel.HIGH):
            await self._send_critical_alert(alert)

        return alert_id

    async def _send_critical_alert(self, alert: dict[str, Any]) -> None:
        """Send critical alert notifications with fallback logging.

        Args:
            alert: Alert document
        """
        try:
            if hasattr(settings, "alert_webhook_url") and settings.alert_webhook_url:
                logger.info(
                    "Sending critical alert via webhook: %s [level=%s, type=%s]",
                    alert["title"],
                    alert["level"],
                    alert["alert_type"],
                )
                await self._send_webhook(alert)
            else:
                logger.warning(
                    "Critical alert created but no webhook configured (alert will be stored in database): %s - %s [level=%s, type=%s]",
                    alert["title"],
                    alert["message"],
                    alert["level"],
                    alert["alert_type"],
                )
        except Exception as e:
            logger.error(
                "Failed to send critical alert notification (alert stored in database): %s - %s [error=%s]",
                alert["title"],
                alert["message"],
                e,
                exc_info=True,
            )

    async def _send_webhook(self, alert: dict[str, Any]) -> None:
        """Send alert via webhook with comprehensive error handling.

        Args:
            alert: Alert document
        """
        try:
            import httpx
            import socket

            webhook_url = getattr(settings, "alert_webhook_url", None)
            if not webhook_url:
                logger.debug("No webhook URL configured, skipping webhook notification")
                return

            logger.debug("Attempting to send webhook alert to: %s", webhook_url)

            payload = {
                "alert_type": alert["alert_type"],
                "level": alert["level"],
                "title": alert["title"],
                "message": alert["message"],
                "metadata": alert.get("metadata", {}),
                "created_at": alert["created_at"].isoformat(),
            }

            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(webhook_url, json=payload)
                    response.raise_for_status()
                    logger.info("Alert webhook sent successfully to %s", webhook_url)
            except httpx.ConnectError as e:
                logger.error(
                    "Failed to connect to webhook URL %s: %s (DNS/network issue). "
                    "Alert stored in database but webhook notification failed.",
                    webhook_url,
                    e,
                    exc_info=True,
                )
            except httpx.TimeoutException as e:
                logger.error(
                    "Webhook request timed out for %s: %s. "
                    "Alert stored in database but webhook notification failed.",
                    webhook_url,
                    e,
                    exc_info=True,
                )
            except httpx.HTTPStatusError as e:
                logger.error(
                    "Webhook returned HTTP error %s for %s: %s. "
                    "Alert stored in database but webhook notification failed.",
                    e.response.status_code if e.response else "unknown",
                    webhook_url,
                    e,
                    exc_info=True,
                )
            except httpx.HTTPError as e:
                logger.error(
                    "HTTP error sending webhook to %s: %s. "
                    "Alert stored in database but webhook notification failed.",
                    webhook_url,
                    e,
                    exc_info=True,
                )
        except Exception as e:
            logger.error(
                "Unexpected error in webhook notification: %s. "
                "Alert stored in database but webhook notification failed.",
                e,
                exc_info=True,
            )

    async def acknowledge_alert(self, alert_id: str, user_id: str | None = None) -> bool:
        """Acknowledge an alert.

        Args:
            alert_id: Alert ID
            user_id: Optional user ID who acknowledged

        Returns:
            True if acknowledged, False if not found
        """
        result = self.db.alerts.update_one(
            {"_id": alert_id},
            {
                "$set": {
                    "acknowledged": True,
                    "acknowledged_at": datetime.utcnow(),
                    "acknowledged_by": user_id,
                }
            },
        )

        return result.modified_count > 0

    async def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert.

        Args:
            alert_id: Alert ID

        Returns:
            True if resolved, False if not found
        """
        result = self.db.alerts.update_one(
            {"_id": alert_id},
            {
                "$set": {
                    "resolved": True,
                    "resolved_at": datetime.utcnow(),
                }
            },
        )

        return result.modified_count > 0

    async def get_active_alerts(
        self,
        level: AlertLevel | None = None,
        alert_type: AlertType | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Get active (unresolved) alerts.

        Args:
            level: Optional filter by level
            alert_type: Optional filter by type
            limit: Maximum number of alerts to return

        Returns:
            List of alert documents
        """
        query: dict[str, Any] = {"resolved": False}

        if level:
            query["level"] = level.value

        if alert_type:
            query["alert_type"] = alert_type.value

        alerts = (
            self.db.alerts.find(query)
            .sort("created_at", -1)
            .limit(limit)
        )

        return list(alerts)


alerting_service = AlertingService()

