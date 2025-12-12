"""Base email provider interface."""

from abc import ABC, abstractmethod
from typing import Any

from api.services.email.models import EmailMessage, EmailResponse


class BaseEmailProvider(ABC):
    """Abstract base class for email providers.

    All email providers must implement this interface.
    """

    @abstractmethod
    async def send_email(self, message: EmailMessage) -> EmailResponse:
        """Send email message.

        Args:
            message: Email message to send

        Returns:
            Email response with success status and message ID

        Raises:
            ValueError: If message is invalid
            RuntimeError: If provider is not configured
            ConnectionError: If provider connection fails
        """
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """Validate provider configuration.

        Returns:
            True if configuration is valid, False otherwise
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Get provider name.

        Returns:
            Provider name string
        """
        pass

    def _generate_text_from_html(self, html: str) -> str:
        """Generate plain text from HTML (simple implementation).

        Args:
            html: HTML content

        Returns:
            Plain text content
        """
        import re

        text = html
        text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"\s+", " ", text)
        text = text.strip()
        return text

