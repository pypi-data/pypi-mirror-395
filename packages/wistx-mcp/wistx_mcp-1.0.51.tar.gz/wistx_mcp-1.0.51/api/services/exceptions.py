"""Quota and organization exceptions."""

from typing import Any


class QuotaExceededError(Exception):
    """Exception raised when quota is exceeded."""

    def __init__(self, message: str, limit_type: str, current: int | float, limit: int | float):
        super().__init__(message)
        self.limit_type = limit_type
        self.current = current
        self.limit = limit


class OrganizationQuotaExceededError(QuotaExceededError):
    """Organization quota exceeded error with detailed breakdown."""

    def __init__(
        self,
        message: str,
        limit_type: str,
        current: int | float,
        limit: int | float,
        organization_id: str,
        member_breakdown: list[dict[str, Any]] | None = None,
    ):
        super().__init__(message, limit_type, current, limit)
        self.organization_id = organization_id
        self.member_breakdown = member_breakdown or []

