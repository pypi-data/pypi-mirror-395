"""Resend email provider implementation."""

import logging
from typing import Any

import httpx

from api.config import settings
from api.services.email.models import EmailMessage, EmailResponse, EmailProvider
from api.services.email.providers.base import BaseEmailProvider

logger = logging.getLogger(__name__)


class ResendProvider(BaseEmailProvider):
    """Resend email provider.

    Documentation: https://resend.com/docs/api-reference/emails/send-email
    """

    def __init__(self):
        """Initialize Resend provider."""
        self.api_key = getattr(settings, "resend_api_key", None)
        self.api_url = "https://api.resend.com/emails"
        self.timeout = 10.0

    def validate_config(self) -> bool:
        """Validate Resend configuration.

        Returns:
            True if API key is configured, False otherwise
        """
        return self.api_key is not None and len(self.api_key) > 0

    def get_provider_name(self) -> str:
        """Get provider name.

        Returns:
            Provider name
        """
        return EmailProvider.RESEND.value

    async def send_email(self, message: EmailMessage) -> EmailResponse:
        """Send email via Resend API.

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
                message="Resend API key not configured",
                user_message="Email service is not configured. Please contact support.",
                error_code="EMAIL_SERVICE_NOT_CONFIGURED",
                details={"provider": "resend"}
            )

        if not message.text:
            message.text = self._generate_text_from_html(message.html)

        from_email = message.from_email or getattr(settings, "email_from_address", "noreply@wistx.ai")
        from_name = message.from_name or getattr(settings, "email_from_name", "WISTX")

        logger.debug(
            "Preparing email via Resend: from=%s <%s>, to=%s, subject=%s",
            from_name,
            from_email,
            message.to,
            message.subject,
        )

        payload: dict[str, Any] = {
            "from": f"{from_name} <{from_email}>",
            "to": message.to if isinstance(message.to, list) else [message.to],
            "subject": message.subject,
            "html": message.html,
            "text": message.text,
        }

        if message.reply_to:
            payload["reply_to"] = message.reply_to

        if message.tags:
            logger.debug("Tags provided but not sent to Resend (not supported by API): %s", message.tags)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(self.api_url, json=payload, headers=headers)
                response.raise_for_status()

                result = response.json()
                message_id = result.get("id")

                logger.info(
                    "Email sent via Resend to %s (message_id: %s, status_code: %d)",
                    message.to,
                    message_id,
                    response.status_code,
                )
                logger.debug(
                    "Resend API response: %s",
                    result,
                )

                return EmailResponse(
                    success=True,
                    message_id=message_id,
                    provider=EmailProvider.RESEND,
                )

        except httpx.HTTPStatusError as e:
            error_msg = f"Resend API error: {e.response.status_code} - {e.response.text}"
            logger.error(error_msg)
            return EmailResponse(
                success=False,
                provider=EmailProvider.RESEND,
                error=error_msg,
            )
        except httpx.RequestError as e:
            error_msg = f"Resend connection error: {str(e)}"
            logger.error(error_msg)
            raise ConnectionError(error_msg) from e
        except Exception as e:
            error_msg = f"Unexpected error sending email via Resend: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return EmailResponse(
                success=False,
                provider=EmailProvider.RESEND,
                error=error_msg,
            )

