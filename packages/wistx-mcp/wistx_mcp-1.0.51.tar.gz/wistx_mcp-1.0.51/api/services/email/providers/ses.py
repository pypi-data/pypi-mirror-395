"""AWS SES email provider implementation."""

import logging
from typing import Any

from api.config import settings
from api.services.email.models import EmailMessage, EmailResponse, EmailProvider
from api.services.email.providers.base import BaseEmailProvider

logger = logging.getLogger(__name__)


class SESProvider(BaseEmailProvider):
    """AWS SES email provider.

    Documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses.html
    """

    def __init__(self):
        """Initialize SES provider."""
        self.aws_access_key_id = getattr(settings, "aws_access_key_id", None)
        self.aws_secret_access_key = getattr(settings, "aws_secret_access_key", None)
        self.aws_region = getattr(settings, "aws_region", "us-east-1")
        self._client: Any = None

    def validate_config(self) -> bool:
        """Validate SES configuration.

        Returns:
            True if AWS credentials are configured, False otherwise
        """
        return (
            self.aws_access_key_id is not None
            and len(self.aws_access_key_id) > 0
            and self.aws_secret_access_key is not None
            and len(self.aws_secret_access_key) > 0
        )

    def get_provider_name(self) -> str:
        """Get provider name.

        Returns:
            Provider name
        """
        return EmailProvider.SES.value

    def _get_client(self) -> Any:
        """Get or create boto3 SES client.

        Returns:
            boto3 SES client

        Raises:
            ImportError: If boto3 is not installed
        """
        if self._client is None:
            try:
                import boto3
            except ImportError as e:
                raise ImportError(
                    "boto3 is required for SES provider. Install with: pip install boto3"
                ) from e

            self._client = boto3.client(
                "ses",
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.aws_region,
            )

        return self._client

    async def send_email(self, message: EmailMessage) -> EmailResponse:
        """Send email via AWS SES.

        Args:
            message: Email message to send

        Returns:
            Email response with success status and message ID

        Raises:
            ValueError: If message is invalid
            RuntimeError: If provider is not configured
            ConnectionError: If AWS connection fails
        """
        from api.exceptions import ValidationError
        if not self.validate_config():
            raise ValidationError(
                message="AWS SES credentials not configured",
                user_message="Email service is not configured. Please contact support.",
                error_code="EMAIL_SERVICE_NOT_CONFIGURED",
                details={"provider": "ses"}
            )

        import asyncio

        if not message.text:
            message.text = self._generate_text_from_html(message.html)

        from_email = message.from_email or getattr(settings, "email_from_address", "noreply@wistx.ai")

        recipients = message.to if isinstance(message.to, list) else [message.to]

        destination: dict[str, Any] = {
            "ToAddresses": recipients,
        }

        if message.reply_to:
            destination["ReplyToAddresses"] = [message.reply_to]

        message_body: dict[str, Any] = {
            "Text": {"Data": message.text, "Charset": "UTF-8"},
            "Html": {"Data": message.html, "Charset": "UTF-8"},
        }

        ses_message: dict[str, Any] = {
            "Subject": {"Data": message.subject, "Charset": "UTF-8"},
            "Body": message_body,
        }

        try:
            client = self._get_client()

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                client.send_email,
                {"Source": from_email, "Destination": destination, "Message": ses_message},
            )

            message_id = response.get("MessageId")

            logger.info(
                "Email sent via SES to %s (message_id: %s)",
                message.to,
                message_id,
            )

            return EmailResponse(
                success=True,
                message_id=message_id,
                provider=EmailProvider.SES,
            )

        except Exception as e:
            error_msg = f"Error sending email via SES: {str(e)}"
            logger.error(error_msg, exc_info=True)

            from api.exceptions import ValidationError, AuthenticationError
            if "InvalidParameterValue" in str(e) or "MessageRejected" in str(e):
                raise ValidationError(
                    message=error_msg,
                    user_message="Invalid email parameters. Please check your email configuration.",
                    error_code="INVALID_EMAIL_PARAMETERS",
                    details={"error": str(e)}
                ) from e

            if "AccessDenied" in str(e) or "InvalidAccessKeyId" in str(e):
                raise AuthenticationError(
                    message=f"AWS SES authentication failed: {error_msg}",
                    user_message="Email service authentication failed. Please contact support.",
                    error_code="EMAIL_AUTH_FAILED",
                    details={"error": str(e), "provider": "ses"}
                ) from e

            raise ConnectionError(error_msg) from e

