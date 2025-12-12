"""SendGrid email provider implementation."""

import logging
from typing import Any

import httpx

from api.config import settings
from api.services.email.models import EmailMessage, EmailResponse, EmailProvider
from api.services.email.providers.base import BaseEmailProvider

logger = logging.getLogger(__name__)


class SendGridProvider(BaseEmailProvider):
    """SendGrid email provider.

    Documentation: https://docs.sendgrid.com/api-reference/mail-send/mail-send
    """

    def __init__(self):
        """Initialize SendGrid provider."""
        self.api_key = getattr(settings, "sendgrid_api_key", None)
        self.api_url = "https://api.sendgrid.com/v3/mail/send"
        self.timeout = 10.0

    def validate_config(self) -> bool:
        """Validate SendGrid configuration.

        Returns:
            True if API key is configured, False otherwise
        """
        return self.api_key is not None and len(self.api_key) > 0

    def get_provider_name(self) -> str:
        """Get provider name.

        Returns:
            Provider name
        """
        return EmailProvider.SENDGRID.value

    async def send_email(self, message: EmailMessage) -> EmailResponse:
        """Send email via SendGrid API.

        Args:
            message: Email message to send

        Returns:
            Email response with success status and message ID

        Raises:
            ValueError: If message is invalid
            RuntimeError: If provider is not configured
            ConnectionError: If API request fails
        """
        from api.exceptions import ValidationError
        if not self.validate_config():
            raise ValidationError(
                message="SendGrid API key not configured",
                user_message="Email service is not configured. Please contact support.",
                error_code="EMAIL_SERVICE_NOT_CONFIGURED",
                details={"provider": "sendgrid"}
            )

        if not message.text:
            message.text = self._generate_text_from_html(message.html)

        from_email = message.from_email or getattr(settings, "email_from_address", "noreply@wistx.ai")
        from_name = message.from_name or getattr(settings, "email_from_name", "WISTX")

        recipients = message.to if isinstance(message.to, list) else [message.to]

        payload: dict[str, Any] = {
            "personalizations": [
                {
                    "to": [{"email": email} for email in recipients],
                }
            ],
            "from": {
                "email": from_email,
                "name": from_name,
            },
            "subject": message.subject,
            "content": [
                {
                    "type": "text/plain",
                    "value": message.text,
                },
                {
                    "type": "text/html",
                    "value": message.html,
                },
            ],
        }

        if message.reply_to:
            payload["reply_to"] = {"email": message.reply_to}

        if message.tags:
            payload["categories"] = message.tags

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(self.api_url, json=payload, headers=headers)
                response.raise_for_status()

                message_id = response.headers.get("X-Message-Id", "unknown")

                logger.info(
                    "Email sent via SendGrid to %s (message_id: %s)",
                    message.to,
                    message_id,
                )

                return EmailResponse(
                    success=True,
                    message_id=message_id,
                    provider=EmailProvider.SENDGRID,
                )

        except httpx.HTTPStatusError as e:
            error_body = e.response.text if hasattr(e.response, "text") else str(e.response.status_code)
            error_msg = f"SendGrid API error: {e.response.status_code} - {error_body}"
            logger.error(error_msg)
            return EmailResponse(
                success=False,
                provider=EmailProvider.SENDGRID,
                error=error_msg,
            )
        except httpx.RequestError as e:
            error_msg = f"SendGrid connection error: {str(e)}"
            logger.error(error_msg)
            raise ConnectionError(error_msg) from e
        except Exception as e:
            error_msg = f"Unexpected error sending email via SendGrid: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return EmailResponse(
                success=False,
                provider=EmailProvider.SENDGRID,
                error=error_msg,
            )

