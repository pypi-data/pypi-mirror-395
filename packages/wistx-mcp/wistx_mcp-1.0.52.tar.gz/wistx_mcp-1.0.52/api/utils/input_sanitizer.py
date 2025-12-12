"""Input sanitization utilities for user-provided content."""

import re
import urllib.parse
from typing import Any
from urllib.parse import urlparse


def sanitize_url(url: str) -> str:
    """Sanitize and validate URL.

    Args:
        url: URL to sanitize

    Returns:
        Sanitized URL

    Raises:
        ValueError: If URL is invalid or contains dangerous patterns
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")

    url = url.strip()

    if not url:
        raise ValueError("URL cannot be empty")

    parsed = urlparse(url)

    if not parsed.scheme:
        raise ValueError("URL must include scheme (http:// or https://)")

    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Invalid URL scheme: {parsed.scheme}. Only http:// and https:// are allowed")

    if not parsed.netloc:
        raise ValueError("URL must include a valid hostname")

    dangerous_patterns = [
        r"javascript:",
        r"data:",
        r"vbscript:",
        r"onload\s*=",
        r"onerror\s*=",
        r"<script",
        r"</script>",
    ]

    url_lower = url.lower()
    for pattern in dangerous_patterns:
        if re.search(pattern, url_lower):
            raise ValueError(f"URL contains potentially dangerous content: {pattern}")

    return url


def sanitize_repository_url(repo_url: str) -> str:
    """Sanitize GitHub repository URL.

    Args:
        repo_url: Repository URL to sanitize

    Returns:
        Sanitized repository URL

    Raises:
        ValueError: If URL is invalid
    """
    if not repo_url or not isinstance(repo_url, str):
        raise ValueError("Repository URL must be a non-empty string")

    repo_url = repo_url.strip()

    if repo_url.startswith("git@"):
        raise ValueError("SSH URLs are not supported. Please use HTTPS URL (https://github.com/...)")

    if not repo_url.startswith(("http://", "https://")):
        if "/" in repo_url and not repo_url.startswith("file://"):
            repo_url = f"https://{repo_url}"

    sanitized = sanitize_url(repo_url)

    parsed = urlparse(sanitized)
    if "github.com" not in parsed.netloc and "gitlab.com" not in parsed.netloc:
        raise ValueError("Only GitHub and GitLab repositories are supported")

    return sanitized


def sanitize_search_query(query: str, max_length: int = 10000) -> str:
    """Sanitize search query string.

    Args:
        query: Search query to sanitize
        max_length: Maximum query length

    Returns:
        Sanitized query string

    Raises:
        ValueError: If query is invalid
    """
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string")

    query = query.strip()

    if not query:
        raise ValueError("Query cannot be empty")

    if len(query) > max_length:
        raise ValueError(f"Query too long (max {max_length} characters)")

    dangerous_patterns = [
        r"<script",
        r"</script>",
        r"javascript:",
        r"on\w+\s*=",
    ]

    query_lower = query.lower()
    for pattern in dangerous_patterns:
        if re.search(pattern, query_lower):
            raise ValueError(f"Query contains potentially dangerous content")

    return query


def sanitize_file_path(file_path: str) -> str:
    """Sanitize file path.

    Args:
        file_path: File path to sanitize

    Returns:
        Sanitized file path

    Raises:
        ValueError: If path is invalid or contains dangerous patterns
    """
    if not file_path or not isinstance(file_path, str):
        raise ValueError("File path must be a non-empty string")

    file_path = file_path.strip()

    if not file_path:
        raise ValueError("File path cannot be empty")

    dangerous_patterns = [
        r"\.\.",
        r"//",
        r"~",
        r"^\s*/",
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, file_path):
            raise ValueError(f"File path contains potentially dangerous pattern: {pattern}")

    if len(file_path) > 4096:
        raise ValueError("File path too long (max 4096 characters)")

    return file_path

