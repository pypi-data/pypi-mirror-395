"""Input sanitization utilities for safe data storage."""

import re


def sanitize_control_id(control_id: str, max_length: int = 100) -> str:
    """Sanitize control ID for safe storage.

    Args:
        control_id: Raw control ID
        max_length: Maximum length (default: 100)

    Returns:
        Sanitized control ID
    """
    if not control_id:
        return "unknown"

    sanitized = str(control_id).strip()

    sanitized = re.sub(r'[^a-zA-Z0-9._-]', '_', sanitized)

    sanitized = re.sub(r'_+', '_', sanitized)

    sanitized = sanitized.strip('_.')

    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]

    if not sanitized:
        return "unknown"

    return sanitized


def sanitize_text(text: str | None, max_length: int = 10000) -> str:
    """Sanitize text fields (title, description).

    Args:
        text: Raw text
        max_length: Maximum length

    Returns:
        Sanitized text
    """
    if not text:
        return ""

    sanitized = str(text).strip()

    sanitized = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F]', '', sanitized)

    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length] + "..."

    return sanitized


def sanitize_url(url: str | None) -> str:
    """Sanitize URL.

    Args:
        url: Raw URL

    Returns:
        Sanitized URL
    """
    if not url:
        return ""

    url_str = str(url).strip()

    if not url_str.startswith(('http://', 'https://')):
        return ""

    url_str = re.sub(r'[\x00-\x1F]', '', url_str)

    return url_str[:2000]

