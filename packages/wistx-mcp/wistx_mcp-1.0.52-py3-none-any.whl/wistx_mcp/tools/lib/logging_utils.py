"""Logging utilities for sanitizing sensitive data."""

import json
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)

SENSITIVE_KEYS = {
    "api_key",
    "apikey",
    "github_token",
    "password",
    "secret",
    "token",
    "authorization",
    "auth",
    "credential",
    "private_key",
    "access_key",
    "secret_key",
}

SENSITIVE_PATTERNS = [
    (r'("api_key"\s*:\s*")[^"]+(")', r'\1***REDACTED***\2'),
    (r'("apikey"\s*:\s*")[^"]+(")', r'\1***REDACTED***\2'),
    (r'("token"\s*:\s*")[^"]+(")', r'\1***REDACTED***\2'),
    (r'("password"\s*:\s*")[^"]+(")', r'\1***REDACTED***\2'),
    (r'("secret"\s*:\s*")[^"]+(")', r'\1***REDACTED***\2'),
    (r'(api_key=)[^&\s]+', r'\1***REDACTED***'),
    (r'(apikey=)[^&\s]+', r'\1***REDACTED***'),
    (r'(token=)[^&\s]+', r'\1***REDACTED***'),
    (r'(password=)[^&\s]+', r'\1***REDACTED***'),
    (r'(secret=)[^&\s]+', r'\1***REDACTED***'),
    (r'(Bearer\s+)[^\s]+', r'\1***REDACTED***'),
    (r'(bearer\s+)[^\s]+', r'\1***REDACTED***'),
]


def redact_sensitive_data(text: str) -> str:
    """Redact sensitive data from text.

    Args:
        text: Text to redact

    Returns:
        Redacted text
    """
    redacted = text
    for pattern, replacement in SENSITIVE_PATTERNS:
        redacted = re.sub(pattern, replacement, redacted, flags=re.IGNORECASE)
    return redacted


def sanitize_value(value: Any, max_length: int = 50) -> Any:
    """Sanitize a single value to prevent sensitive data leakage.

    Args:
        value: Value to sanitize
        max_length: Maximum length for string values before truncation

    Returns:
        Sanitized value
    """
    if isinstance(value, str):
        if len(value) > 32:
            return f"{value[:8]}...{value[-4:]}"
        return "***REDACTED***"
    elif isinstance(value, (int, float, bool, type(None))):
        return value
    elif isinstance(value, (list, tuple)):
        return [sanitize_value(item, max_length) for item in value]
    elif isinstance(value, dict):
        return sanitize_dict(value, max_length)
    else:
        return str(value)[:max_length] + "..." if len(str(value)) > max_length else str(value)


def sanitize_dict(data: dict[str, Any], max_length: int = 50) -> dict[str, Any]:
    """Sanitize dictionary to remove sensitive data.

    Args:
        data: Dictionary to sanitize
        max_length: Maximum length for string values

    Returns:
        Sanitized dictionary
    """
    sanitized = {}

    for key, value in data.items():
        key_lower = key.lower()

        if any(sensitive in key_lower for sensitive in SENSITIVE_KEYS):
            sanitized[key] = "***REDACTED***"
        elif isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, max_length)
        elif isinstance(value, (list, tuple)):
            sanitized[key] = [sanitize_value(item, max_length) for item in value]
        elif isinstance(value, str) and len(value) > 100:
            sanitized[key] = sanitize_value(value, max_length)
        else:
            sanitized[key] = value

    return sanitized


def sanitize_arguments(args: dict[str, Any]) -> dict[str, Any]:
    """Sanitize tool arguments for logging.

    Args:
        args: Tool arguments dictionary

    Returns:
        Sanitized arguments dictionary
    """
    return sanitize_dict(args)


def sanitize_error_message(error: Exception, tool_name: str | None = None) -> str:
    """Sanitize error message to prevent information leakage.

    Args:
        error: Exception that occurred
        tool_name: Name of the tool that failed

    Returns:
        Sanitized error message
    """
    error_str = str(error)

    error_str = re.sub(r"\b[a-zA-Z0-9]{32,}\b", "[REDACTED]", error_str)

    error_str = re.sub(r"/[^\s]+", "[PATH_REDACTED]", error_str)

    error_str = re.sub(r"Bearer\s+[^\s]+", "Bearer [REDACTED]", error_str, flags=re.IGNORECASE)

    if tool_name:
        return f"An error occurred: {error_str}"
    return f"Error: {error_str}"


def safe_json_dumps(data: Any, indent: int | None = None) -> str:
    """Safely serialize data to JSON with sanitization.

    Args:
        data: Data to serialize
        indent: JSON indentation level

    Returns:
        JSON string with sensitive data sanitized
    """
    if isinstance(data, dict):
        sanitized = sanitize_dict(data)
    else:
        sanitized = sanitize_value(data)

    try:
        json_str = json.dumps(sanitized, indent=indent, default=str)
        return redact_sensitive_data(json_str)
    except (TypeError, ValueError) as e:
        logger.warning("Failed to serialize data to JSON: %s", e)
        return redact_sensitive_data(str(sanitized))


class SensitiveDataFilter(logging.Filter):
    """Filter to redact sensitive data from log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter log record and redact sensitive data.

        Args:
            record: Log record

        Returns:
            True to allow record
        """
        if hasattr(record, "msg") and isinstance(record.msg, str):
            record.msg = redact_sensitive_data(record.msg)

        if hasattr(record, "args") and record.args:
            redacted_args = []
            for arg in record.args:
                if isinstance(arg, str):
                    redacted_args.append(redact_sensitive_data(arg))
                elif isinstance(arg, dict):
                    redacted_args.append(sanitize_arguments(arg))
                else:
                    redacted_args.append(arg)
            record.args = tuple(redacted_args)

        return True

