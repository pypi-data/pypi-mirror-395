"""Alert preferences model."""

from pydantic import BaseModel, Field
from typing import Optional

from api.services.alert_service import AlertChannel


class AlertPreferences(BaseModel):
    """User alert preferences."""

    user_id: str = Field(..., description="User ID")
    budget_id: Optional[str] = Field(
        default=None,
        description="Budget ID (None for global preferences)",
    )

    email_enabled: bool = Field(default=True, description="Enable email alerts")
    webhook_enabled: bool = Field(default=False, description="Enable webhook alerts")
    slack_enabled: bool = Field(default=False, description="Enable Slack alerts")
    in_app_enabled: bool = Field(default=True, description="Enable in-app alerts")

    webhook_url: Optional[str] = Field(default=None, description="Webhook URL")
    slack_webhook_url: Optional[str] = Field(default=None, description="Slack webhook URL")

    custom_alert_threshold: Optional[float] = Field(
        default=None,
        description="Custom alert threshold (overrides budget default)",
    )
    custom_critical_threshold: Optional[float] = Field(
        default=None,
        description="Custom critical threshold (overrides budget default)",
    )

    min_alert_interval_minutes: int = Field(
        default=60,
        description="Minimum interval between alerts (deduplication)",
    )

    def get_enabled_channels(self) -> list[AlertChannel]:
        """Get list of enabled alert channels.

        Returns:
            List of enabled channels
        """
        channels = []
        if self.email_enabled:
            channels.append(AlertChannel.EMAIL)
        if self.webhook_enabled and self.webhook_url:
            channels.append(AlertChannel.WEBHOOK)
        if self.slack_enabled and self.slack_webhook_url:
            channels.append(AlertChannel.SLACK)
        if self.in_app_enabled:
            channels.append(AlertChannel.IN_APP)
        return channels if channels else [AlertChannel.IN_APP]

