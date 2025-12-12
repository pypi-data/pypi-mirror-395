"""Email service models."""

import re
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class EmailProvider(str, Enum):
    """Email provider types."""

    RESEND = "resend"
    SENDGRID = "sendgrid"
    SES = "ses"


class EmailMessage(BaseModel):
    """Email message model.

    Attributes:
        to: Recipient email address(es)
        subject: Email subject
        html: HTML email body
        text: Plain text email body (optional, auto-generated from HTML if not provided)
        from_email: Sender email address (optional, uses default from config)
        from_name: Sender name (optional, uses default from config)
        reply_to: Reply-to email address (optional)
        tags: Email tags for tracking/grouping (optional)
        metadata: Additional metadata (optional)
    """

    to: str | list[str] = Field(..., description="Recipient email address(es)")
    subject: str = Field(..., min_length=1, max_length=200, description="Email subject")
    html: str = Field(..., min_length=1, description="HTML email body")
    text: str | None = Field(default=None, description="Plain text email body")
    from_email: str | None = Field(default=None, description="Sender email address")
    from_name: str | None = Field(default=None, description="Sender name")
    reply_to: str | None = Field(default=None, description="Reply-to email address")
    tags: list[str] | None = Field(default=None, description="Email tags")
    metadata: dict[str, Any] | None = Field(default=None, description="Additional metadata")

    @field_validator("to")
    @classmethod
    def validate_to(cls, v: str | list[str]) -> str | list[str]:
        """Validate recipient email address(es)."""
        from api.exceptions import ValidationError
        if isinstance(v, str):
            if not v or "@" not in v:
                raise ValidationError(
                    message="Invalid email address",
                    user_message="Invalid email address format",
                    error_code="INVALID_EMAIL",
                    details={"email": v}
                )
        elif isinstance(v, list):
            if not v:
                raise ValidationError(
                    message="At least one recipient required",
                    user_message="At least one email recipient is required",
                    error_code="NO_RECIPIENTS",
                    details={}
                )
            for email in v:
                if not email or "@" not in email:
                    raise ValidationError(
                        message=f"Invalid email address: {email}",
                        user_message=f"Invalid email address format: {email}",
                        error_code="INVALID_EMAIL",
                        details={"email": email}
                    )
        return v

    @field_validator("html")
    @classmethod
    def validate_html(cls, v: str) -> str:
        """Validate HTML content."""
        from api.exceptions import ValidationError
        if not v or not v.strip():
            raise ValidationError(
                message="HTML content cannot be empty",
                user_message="Email HTML content cannot be empty",
                error_code="EMPTY_HTML_CONTENT",
                details={}
            )
        return v

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: list[str] | None) -> list[str] | None:
        """Validate and sanitize email tags.
        
        Tags must only contain ASCII letters, numbers, underscores, or dashes.
        Invalid characters are replaced with underscores.
        
        Args:
            v: List of tag strings
            
        Returns:
            Sanitized list of tags
        """
        if v is None:
            return None
        
        sanitized_tags = []
        tag_pattern = re.compile(r"[^a-zA-Z0-9_-]")
        
        for tag in v:
            if not tag:
                continue
            
            sanitized_tag = tag_pattern.sub("_", tag)
            
            if sanitized_tag and sanitized_tag not in sanitized_tags:
                sanitized_tags.append(sanitized_tag)
        
        return sanitized_tags if sanitized_tags else None


class EmailResponse(BaseModel):
    """Email send response model.

    Attributes:
        success: Whether email was sent successfully
        message_id: Provider-specific message ID
        provider: Email provider used
        error: Error message if failed
    """

    success: bool = Field(..., description="Whether email was sent successfully")
    message_id: str | None = Field(default=None, description="Provider-specific message ID")
    provider: EmailProvider = Field(..., description="Email provider used")
    error: str | None = Field(default=None, description="Error message if failed")

