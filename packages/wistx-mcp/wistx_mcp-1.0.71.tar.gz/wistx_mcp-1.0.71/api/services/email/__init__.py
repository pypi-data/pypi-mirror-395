"""Email service module."""

from api.services.email.email_service import EmailService, email_service
from api.services.email.models import EmailMessage, EmailResponse, EmailProvider

__all__ = [
    "EmailService",
    "email_service",
    "EmailMessage",
    "EmailResponse",
    "EmailProvider",
]

