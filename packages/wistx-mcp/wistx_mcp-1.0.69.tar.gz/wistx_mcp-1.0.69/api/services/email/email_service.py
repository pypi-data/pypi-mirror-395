"""Email service orchestrator."""

import asyncio
import logging
from typing import Any

from api.config import settings
from api.services.email.models import EmailMessage, EmailResponse, EmailProvider
from api.services.email.providers import ResendProvider, SendGridProvider, SESProvider

logger = logging.getLogger(__name__)


class EmailService:
    """Email service with multi-provider support and retry logic.

    Features:
    - Multi-provider support (Resend, SendGrid, SES)
    - Automatic provider selection based on configuration
    - Retry logic with exponential backoff
    - Graceful degradation
    - Template support
    """

    def __init__(self):
        """Initialize email service."""
        self._provider: Any = None
        self._provider_name: EmailProvider | None = None
        self._max_retries = 3
        self._retry_initial_delay = 1.0
        self._retry_max_delay = 10.0

    def _initialize_provider(self) -> None:
        """Initialize email provider based on configuration."""
        if self._provider is not None:
            return

        provider_name = getattr(settings, "email_provider", EmailProvider.RESEND.value)

        try:
            if provider_name == EmailProvider.RESEND.value:
                self._provider = ResendProvider()
                self._provider_name = EmailProvider.RESEND
            elif provider_name == EmailProvider.SENDGRID.value:
                self._provider = SendGridProvider()
                self._provider_name = EmailProvider.SENDGRID
            elif provider_name == EmailProvider.SES.value:
                self._provider = SESProvider()
                self._provider_name = EmailProvider.SES
            else:
                logger.warning("Unknown email provider: %s, defaulting to Resend", provider_name)
                self._provider = ResendProvider()
                self._provider_name = EmailProvider.RESEND

            if not self._provider.validate_config():
                logger.warning(
                    "Email provider %s not configured, email sending will fail",
                    provider_name,
                )
                self._provider = None
                self._provider_name = None
            else:
                logger.info("Email provider initialized: %s", provider_name)

        except Exception as e:
            logger.error("Failed to initialize email provider: %s", e, exc_info=True)
            self._provider = None
            self._provider_name = None

    def is_configured(self) -> bool:
        """Check if email service is configured.

        Returns:
            True if email provider is configured, False otherwise
        """
        self._initialize_provider()
        return self._provider is not None

    async def send_email(
        self,
        to: str | list[str],
        subject: str,
        html: str,
        text: str | None = None,
        from_email: str | None = None,
        from_name: str | None = None,
        reply_to: str | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> EmailResponse:
        """Send email message.

        Args:
            to: Recipient email address(es)
            subject: Email subject
            html: HTML email body
            text: Plain text email body (optional)
            from_email: Sender email address (optional)
            from_name: Sender name (optional)
            reply_to: Reply-to email address (optional)
            tags: Email tags for tracking (optional)
            metadata: Additional metadata (optional)

        Returns:
            Email response with success status and message ID
        """
        self._initialize_provider()

        if not self._provider:
            error_msg = "Email service not configured. Set email provider and credentials in environment variables."
            logger.warning(error_msg)
            return EmailResponse(
                success=False,
                provider=self._provider_name or EmailProvider.RESEND,
                error=error_msg,
            )

        message = EmailMessage(
            to=to,
            subject=subject,
            html=html,
            text=text,
            from_email=from_email,
            from_name=from_name,
            reply_to=reply_to,
            tags=tags,
            metadata=metadata,
        )

        return await self._send_with_retry(message)

    async def _send_with_retry(self, message: EmailMessage) -> EmailResponse:
        """Send email with retry logic.

        Args:
            message: Email message to send

        Returns:
            Email response
        """
        last_error: Exception | None = None

        for attempt in range(self._max_retries):
            try:
                if attempt > 0:
                    delay = min(
                        self._retry_initial_delay * (2 ** (attempt - 1)),
                        self._retry_max_delay,
                    )
                    logger.info(
                        "Retrying email send (attempt %d/%d) after %.1fs delay",
                        attempt + 1,
                        self._max_retries,
                        delay,
                    )
                    await asyncio.sleep(delay)

                response = await self._provider.send_email(message)

                if response.success:
                    if attempt > 0:
                        logger.info("Email sent successfully after %d attempts", attempt + 1)
                    return response

                last_error = Exception(response.error or "Unknown error")

            except (ConnectionError, RuntimeError) as e:
                last_error = e
                logger.warning("Email send attempt %d failed: %s", attempt + 1, str(e))
                if attempt == self._max_retries - 1:
                    break

            except Exception as e:
                last_error = e
                logger.error("Unexpected error sending email: %s", e, exc_info=True)
                break

        error_msg = f"Failed to send email after {self._max_retries} attempts: {str(last_error)}"
        logger.error(error_msg)

        return EmailResponse(
            success=False,
            provider=self._provider_name or EmailProvider.RESEND,
            error=error_msg,
        )

    async def send_template(
        self,
        template_name: str,
        to: str | list[str],
        subject: str,
        context: dict[str, Any],
        **kwargs: Any,
    ) -> EmailResponse:
        """Send email using template.

        Args:
            template_name: Template name (without .html extension)
            to: Recipient email address(es)
            subject: Email subject
            context: Template context variables
            **kwargs: Additional arguments passed to send_email

        Returns:
            Email response
        """
        from api.services.email.templates import render_template

        try:
            html = await render_template(template_name, context)
            return await self.send_email(to=to, subject=subject, html=html, **kwargs)
        except Exception as e:
            error_msg = f"Failed to render template {template_name}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return EmailResponse(
                success=False,
                provider=self._provider_name or EmailProvider.RESEND,
                error=error_msg,
            )


email_service = EmailService()

