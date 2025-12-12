"""Alert service for budget notifications."""

import logging
import secrets
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

from bson import ObjectId

from api.database.mongodb import mongodb_manager

logger = logging.getLogger(__name__)


class AlertChannel(str, Enum):
    """Alert notification channels."""

    EMAIL = "email"
    WEBHOOK = "webhook"
    SLACK = "slack"
    IN_APP = "in_app"


class AlertStatus(str, Enum):
    """Alert status."""

    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    ACKNOWLEDGED = "acknowledged"


class AlertService:
    """Service for managing budget alerts."""

    async def create_alert(
        self,
        budget_id: str | None,
        user_id: str,
        alert_type: str,
        message: str,
        utilization_percent: float = 0.0,
        channels: list[AlertChannel] | None = None,
    ) -> dict[str, Any] | None:
        """Create and send alert.

        Args:
            budget_id: Budget ID (optional for non-budget alerts)
            user_id: User ID
            alert_type: Alert type (warning, critical, exceeded, api_key_rotation, etc.)
            message: Alert message
            utilization_percent: Budget utilization percentage (default: 0.0)
            channels: Notification channels (defaults to user preferences)

        Returns:
            Alert record dictionary or None if duplicate
        """
        if await self._is_duplicate_alert(budget_id, alert_type, utilization_percent, user_id=user_id):
            logger.info(
                "Skipping duplicate alert for budget %s (type: %s, utilization: %.1f%%)",
                budget_id,
                alert_type,
                utilization_percent,
            )
            return None

        if channels is None:
            channels = await self._get_user_alert_channels(user_id)

        alert_id = self._generate_alert_id()
        alert = {
            "_id": alert_id,
            "budget_id": budget_id,
            "user_id": ObjectId(user_id),
            "alert_type": alert_type,
            "message": message,
            "utilization_percent": utilization_percent,
            "channels": [c.value for c in channels],
            "status": AlertStatus.PENDING.value,
            "created_at": datetime.utcnow(),
            "sent_at": None,
            "acknowledged_at": None,
        }

        db = mongodb_manager.get_database()
        collection = db.budget_alerts
        collection.insert_one(alert)

        await self._send_notifications(alert, channels)

        return alert

    async def _is_duplicate_alert(
        self,
        budget_id: str | None,
        alert_type: str,
        utilization_percent: float,
        window_minutes: int = 60,
        user_id: str | None = None,
    ) -> bool:
        """Check if similar alert was sent recently.

        Args:
            budget_id: Budget ID (optional)
            alert_type: Alert type
            utilization_percent: Utilization percentage
            window_minutes: Deduplication window in minutes
            user_id: User ID (for non-budget alerts)

        Returns:
            True if duplicate alert found
        """
        db = mongodb_manager.get_database()
        collection = db.budget_alerts

        window_start = datetime.utcnow() - timedelta(minutes=window_minutes)

        query: dict[str, Any] = {
            "alert_type": alert_type,
            "created_at": {"$gte": window_start},
            "status": {"$in": [AlertStatus.SENT.value, AlertStatus.PENDING.value]},
        }
        
        if budget_id:
            query["budget_id"] = budget_id
            query["utilization_percent"] = {
                "$gte": utilization_percent - 1.0,
                "$lte": utilization_percent + 1.0,
            }
        elif user_id:
            query["user_id"] = ObjectId(user_id)

        duplicate = collection.find_one(query)

        return duplicate is not None

    async def _get_user_alert_channels(self, user_id: str) -> list[AlertChannel]:
        """Get user's preferred alert channels.

        Args:
            user_id: User ID

        Returns:
            List of alert channels
        """
        db = mongodb_manager.get_database()
        preferences_collection = db.alert_preferences

        preferences = preferences_collection.find_one({"user_id": ObjectId(user_id)})

        if not preferences:
            return [AlertChannel.IN_APP, AlertChannel.EMAIL]

        channels = []
        if preferences.get("email_enabled", True):
            channels.append(AlertChannel.EMAIL)
        if preferences.get("webhook_enabled", False) and preferences.get("webhook_url"):
            channels.append(AlertChannel.WEBHOOK)
        if preferences.get("slack_enabled", False) and preferences.get("slack_webhook_url"):
            channels.append(AlertChannel.SLACK)
        if preferences.get("in_app_enabled", True):
            channels.append(AlertChannel.IN_APP)

        return channels if channels else [AlertChannel.IN_APP]

    async def _send_notifications(
        self,
        alert: dict[str, Any],
        channels: list[AlertChannel],
    ) -> None:
        """Send notifications via specified channels.

        Args:
            alert: Alert record
            channels: Notification channels
        """
        db = mongodb_manager.get_database()
        collection = db.budget_alerts

        for channel in channels:
            try:
                if channel == AlertChannel.EMAIL:
                    await self._send_email(alert)
                elif channel == AlertChannel.WEBHOOK:
                    await self._send_webhook(alert)
                elif channel == AlertChannel.SLACK:
                    await self._send_slack(alert)
                elif channel == AlertChannel.IN_APP:
                    await self._create_in_app_notification(alert)

                collection.update_one(
                    {"_id": alert["_id"]},
                    {"$set": {"status": AlertStatus.SENT.value, "sent_at": datetime.utcnow()}},
                )
            except Exception as e:
                logger.error(
                    "Failed to send alert via %s: %s",
                    channel.value,
                    e,
                    exc_info=True,
                )
                collection.update_one(
                    {"_id": alert["_id"]},
                    {"$set": {"status": AlertStatus.FAILED.value}},
                )

    async def _send_email(self, alert: dict[str, Any]) -> None:
        """Send email notification.

        Args:
            alert: Alert record
        """
        db = mongodb_manager.get_database()
        users_collection = db.users

        user = users_collection.find_one({"_id": alert["user_id"]})
        if not user or not user.get("email"):
            logger.warning("User %s has no email address, skipping email alert", alert["user_id"])
            return

        email = user.get("email")
        subject = f"Budget Alert: {alert['alert_type'].upper()} - {alert['message']}"

        try:
            from api.services.email import email_service
            from api.config import settings
            from datetime import datetime

            frontend_url = (
                settings.oauth_frontend_redirect_url_prod.replace("/auth/callback/{provider}", "")
                if not settings.debug
                else settings.oauth_frontend_redirect_url_dev.replace("/auth/callback/{provider}", "")
            )
            dashboard_url = f"{frontend_url}/admin/budgets"

            alert_type_label = alert["alert_type"].replace("_", " ").title()
            budget_name = alert.get("budget_id", "Unknown Budget")

            await email_service.send_template(
                template_name="budget_alert",
                to=email,
                subject=subject,
                context={
                    "alert_type": alert["alert_type"],
                    "alert_type_label": alert_type_label,
                    "message": alert["message"],
                    "utilization_percent": alert.get("utilization_percent", 0),
                    "budget_name": budget_name,
                    "dashboard_url": dashboard_url,
                    "user_email": email,
                    "current_year": datetime.now().year,
                },
                tags=["budget_alert", alert["alert_type"]],
            )
            logger.info("Sent email alert to %s for budget %s", email, alert["budget_id"])
        except ImportError:
            logger.warning("Email service not available, skipping email alert")
        except Exception as e:
            logger.error("Failed to send email alert: %s", e, exc_info=True)

    async def _send_webhook(self, alert: dict[str, Any]) -> None:
        """Send webhook notification.

        Args:
            alert: Alert record
        """
        db = mongodb_manager.get_database()
        preferences_collection = db.alert_preferences

        preferences = preferences_collection.find_one({"user_id": alert["user_id"]})
        if not preferences or not preferences.get("webhook_url"):
            logger.warning("No webhook URL configured for user %s", alert["user_id"])
            return

        webhook_url = preferences.get("webhook_url")
        payload = {
            "alert_id": str(alert["_id"]),
            "budget_id": alert["budget_id"],
            "alert_type": alert["alert_type"],
            "message": alert["message"],
            "utilization_percent": alert["utilization_percent"],
            "timestamp": alert["created_at"].isoformat(),
        }

        try:
            import httpx

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(webhook_url, json=payload)
                response.raise_for_status()
            logger.info("Sent webhook alert to %s for budget %s", webhook_url, alert["budget_id"])
        except Exception as e:
            logger.error("Failed to send webhook alert: %s", e, exc_info=True)
            raise

    async def _send_slack(self, alert: dict[str, Any]) -> None:
        """Send Slack notification.

        Args:
            alert: Alert record
        """
        db = mongodb_manager.get_database()
        preferences_collection = db.alert_preferences

        preferences = preferences_collection.find_one({"user_id": alert["user_id"]})
        if not preferences or not preferences.get("slack_webhook_url"):
            logger.warning("No Slack webhook URL configured for user %s", alert["user_id"])
            return

        slack_webhook_url = preferences.get("slack_webhook_url")
        alert_emoji = {
            "warning": "⚠️",
            "critical": "🔴",
            "exceeded": "🚫",
        }

        payload = {
            "text": f"{alert_emoji.get(alert['alert_type'], '⚠️')} Budget Alert",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"Budget Alert: {alert['alert_type'].upper()}",
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{alert['message']}*\n\nUtilization: {alert['utilization_percent']:.1f}%",
                    },
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"Budget ID: `{alert['budget_id']}`",
                        },
                    ],
                },
            ],
        }

        try:
            import httpx

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(slack_webhook_url, json=payload)
                response.raise_for_status()
            logger.info("Sent Slack alert for budget %s", alert["budget_id"])
        except Exception as e:
            logger.error("Failed to send Slack alert: %s", e, exc_info=True)
            raise

    async def _create_in_app_notification(self, alert: dict[str, Any]) -> None:
        """Create in-app notification.

        Args:
            alert: Alert record
        """
        db = mongodb_manager.get_database()
        notifications_collection = db.user_notifications

        notification = {
            "user_id": alert["user_id"],
            "type": "budget_alert",
            "title": f"Budget Alert: {alert['alert_type'].upper()}",
            "message": alert["message"],
            "budget_id": alert["budget_id"],
            "utilization_percent": alert["utilization_percent"],
            "read": False,
            "created_at": datetime.utcnow(),
        }

        notifications_collection.insert_one(notification)
        logger.info("Created in-app notification for budget %s", alert["budget_id"])

    def _format_email_body(self, alert: dict[str, Any]) -> str:
        """Format email body.

        Args:
            alert: Alert record

        Returns:
            Formatted email body
        """
        alert_emoji = {
            "warning": "⚠️",
            "critical": "🔴",
            "exceeded": "🚫",
        }

        return f"""
{alert_emoji.get(alert['alert_type'], '⚠️')} Budget Alert: {alert['alert_type'].upper()}

{alert['message']}

Utilization: {alert['utilization_percent']:.1f}%
Budget ID: {alert['budget_id']}
Timestamp: {alert['created_at'].strftime('%Y-%m-%d %H:%M:%S UTC')}

---
This is an automated alert from WISTX Budget Management.
"""

    def _generate_alert_id(self) -> str:
        """Generate unique alert ID.

        Returns:
            Alert ID string
        """
        return f"alert_{secrets.token_hex(12)}"


alert_service = AlertService()

