"""Input sanitization for tool arguments."""

import re
import unicodedata
from typing import Any

from wistx_mcp.tools.lib.constants import (
    MAX_QUERY_LENGTH,
    MAX_INFRASTRUCTURE_CODE_LENGTH,
    MAX_REPOSITORY_URL_LENGTH,
    MAX_CONTENT_URL_LENGTH,
    MAX_DOCUMENTATION_LENGTH,
    MAX_PATTERN_LENGTH,
    MAX_ISSUE_DESCRIPTION_LENGTH,
    MAX_SUBJECT_LENGTH,
    MAX_DESCRIPTION_LENGTH,
    MAX_SUMMARY_LENGTH,
    MAX_ARRAY_LENGTH,
)

BIDIRECTIONAL_OVERRIDE_CHARS = [
    '\u202A',  # LEFT-TO-RIGHT EMBEDDING
    '\u202B',  # RIGHT-TO-LEFT EMBEDDING
    '\u202C',  # POP DIRECTIONAL FORMATTING
    '\u202D',  # LEFT-TO-RIGHT OVERRIDE
    '\u202E',  # RIGHT-TO-LEFT OVERRIDE
    '\u2066',  # LEFT-TO-RIGHT ISOLATE
    '\u2067',  # RIGHT-TO-LEFT ISOLATE
    '\u2068',  # FIRST STRONG ISOLATE
    '\u2069',  # POP DIRECTIONAL ISOLATE
]

ZERO_WIDTH_CHARS = [
    '\u200B',  # ZERO WIDTH SPACE
    '\u200C',  # ZERO WIDTH NON-JOINER
    '\u200D',  # ZERO WIDTH JOINER
    '\uFEFF',  # ZERO WIDTH NO-BREAK SPACE (BOM)
    '\u200E',  # LEFT-TO-RIGHT MARK
    '\u200F',  # RIGHT-TO-LEFT MARK
]

HOMOGRAPH_MAP = {
    '\u0430': 'a',  # CYRILLIC SMALL LETTER A
    '\u0435': 'e',  # CYRILLIC SMALL LETTER IE
    '\u043E': 'o',  # CYRILLIC SMALL LETTER O
    '\u0440': 'p',  # CYRILLIC SMALL LETTER ER
    '\u0441': 'c',  # CYRILLIC SMALL LETTER ES
    '\u0443': 'y',  # CYRILLIC SMALL LETTER U
    '\u0445': 'x',  # CYRILLIC SMALL LETTER HA
}


def sanitize_string_input(value: str, max_length: int | None = 10000) -> str:
    """Sanitize string input with comprehensive Unicode protection.

    Args:
        value: String value to sanitize
        max_length: Maximum allowed length (None for unlimited)

    Returns:
        Sanitized string

    Raises:
        ValueError: If input is invalid or too long
    """
    if not isinstance(value, str):
        raise ValueError("Input must be a string")

    if max_length is not None and len(value) > max_length:
        raise ValueError(f"Input too long (max {max_length} characters)")

    # Remove ASCII control characters (existing)
    sanitized = re.sub(r"[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]", "", value)

    # Remove all Unicode control characters except \n, \r, \t
    sanitized = "".join(
        char for char in sanitized
        if unicodedata.category(char)[0] != 'C' or char in '\n\r\t'
    )

    # Remove bidirectional override characters
    for char in BIDIRECTIONAL_OVERRIDE_CHARS:
        sanitized = sanitized.replace(char, '')

    # Remove zero-width characters
    for char in ZERO_WIDTH_CHARS:
        sanitized = sanitized.replace(char, '')

    # Normalize homograph characters to ASCII equivalents
    for cyrillic, ascii_char in HOMOGRAPH_MAP.items():
        sanitized = sanitized.replace(cyrillic, ascii_char)

    # Normalize Unicode (NFKC: Compatibility Decomposition + Composition)
    sanitized = unicodedata.normalize('NFKC', sanitized)

    return sanitized


def validate_input_size(value: str, field_name: str, max_length: int) -> None:
    """Validate input size for a specific field.

    Args:
        value: String value to validate
        field_name: Name of the field for error messages
        max_length: Maximum allowed length

    Raises:
        ValueError: If input exceeds maximum length
    """
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")

    if len(value) > max_length:
        raise ValueError(
            f"{field_name} too long: {len(value)} characters (max {max_length})"
        )


def validate_query_input(query: str) -> None:
    """Validate query input size.

    Args:
        query: Query string to validate

    Raises:
        ValueError: If query exceeds maximum length
    """
    validate_input_size(query, "query", MAX_QUERY_LENGTH)


def validate_infrastructure_code_input(code: str) -> None:
    """Validate infrastructure code input size.

    Args:
        code: Infrastructure code to validate

    Raises:
        ValueError: If code exceeds maximum length
    """
    validate_input_size(code, "infrastructure_code", MAX_INFRASTRUCTURE_CODE_LENGTH)


def validate_repository_url_input(url: str) -> None:
    """Validate repository URL input size.

    Args:
        url: Repository URL to validate

    Raises:
        ValueError: If URL exceeds maximum length
    """
    validate_input_size(url, "repository_url", MAX_REPOSITORY_URL_LENGTH)


def validate_content_url_input(url: str) -> None:
    """Validate content URL input size.

    Args:
        url: Content URL to validate

    Raises:
        ValueError: If URL exceeds maximum length
    """
    validate_input_size(url, "content_url", MAX_CONTENT_URL_LENGTH)


def validate_pattern_input(pattern: str) -> None:
    """Validate pattern input size.

    Args:
        pattern: Pattern string to validate

    Raises:
        ValueError: If pattern exceeds maximum length
    """
    validate_input_size(pattern, "pattern", MAX_PATTERN_LENGTH)


def sanitize_tool_arguments(arguments: dict[str, Any]) -> dict[str, Any]:
    """Sanitize all string values in tool arguments.

    Args:
        arguments: Tool arguments dictionary

    Returns:
        Sanitized arguments dictionary

    Raises:
        ValueError: If any input is invalid
    """
    field_max_lengths: dict[str, int | None] = {
        "infrastructure_code": None,
        "configuration_code": None,
        "code": None,
        "logs": None,
        "content": None,
        "query": MAX_QUERY_LENGTH,
        "repository_url": MAX_REPOSITORY_URL_LENGTH,
        "content_url": MAX_CONTENT_URL_LENGTH,
        "documentation": MAX_DOCUMENTATION_LENGTH,
        "pattern": MAX_PATTERN_LENGTH,
        "issue_description": MAX_ISSUE_DESCRIPTION_LENGTH,
        "subject": MAX_SUBJECT_LENGTH,
        "description": MAX_DESCRIPTION_LENGTH,
        "summary": MAX_SUMMARY_LENGTH,
    }

    sanitized: dict[str, Any] = {}

    for key, value in arguments.items():
        if isinstance(value, str):
            max_length = field_max_lengths.get(key, 10000)
            sanitized[key] = sanitize_string_input(value, max_length=max_length)
        elif isinstance(value, list):
            if len(value) > MAX_ARRAY_LENGTH:
                raise ValueError(f"Array too long (max {MAX_ARRAY_LENGTH} items): {key}")
            sanitized[key] = [
                sanitize_string_input(item, max_length=field_max_lengths.get(key, 10000)) if isinstance(item, str) else item for item in value
            ]
        elif isinstance(value, dict):
            sanitized[key] = sanitize_tool_arguments(value)
        else:
            sanitized[key] = value

    return sanitized

