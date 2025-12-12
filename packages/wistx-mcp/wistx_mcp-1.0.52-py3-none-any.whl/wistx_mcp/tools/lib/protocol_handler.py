"""MCP protocol version handling and response formatting."""

import logging
from typing import Any

from wistx_mcp.tools.lib.request_context import get_request_context

logger = logging.getLogger(__name__)

SUPPORTED_PROTOCOL_VERSIONS = ["2024-11-05"]
DEFAULT_PROTOCOL_VERSION = "2024-11-05"


def get_protocol_version() -> str:
    """Get current protocol version from request context.

    Returns:
        Protocol version string
    """
    context = get_request_context()
    return context.get("protocol_version", DEFAULT_PROTOCOL_VERSION)


def format_response(data: Any, protocol_version: str | None = None) -> Any:
    """Format response according to protocol version.

    Args:
        data: Response data
        protocol_version: Protocol version (uses context if not provided)

    Returns:
        Formatted response
    """
    version = protocol_version or get_protocol_version()

    if version == "2024-11-05":
        return _format_2024_11_05_response(data)
    else:
        logger.warning("Unknown protocol version %s, using default format", version)
        return _format_2024_11_05_response(data)


def _format_2024_11_05_response(data: Any) -> Any:
    """Format response for protocol version 2024-11-05.

    Args:
        data: Response data

    Returns:
        Formatted response matching 2024-11-05 spec
    """
    if isinstance(data, dict):
        formatted = {}
        for key, value in data.items():
            formatted[key] = _format_2024_11_05_response(value)
        return formatted
    elif isinstance(data, list):
        return [_format_2024_11_05_response(item) for item in data]
    else:
        return data


def validate_protocol_version(version: str) -> str:
    """Validate and normalize protocol version.

    Args:
        version: Protocol version string

    Returns:
        Validated protocol version

    Raises:
        ValueError: If protocol version is not supported
    """
    if not isinstance(version, str):
        raise ValueError(f"Protocol version must be a string, got {type(version)}")

    version = version.strip()

    if version not in SUPPORTED_PROTOCOL_VERSIONS:
        raise ValueError(
            f"Unsupported protocol version: {version}. "
            f"Supported versions: {', '.join(SUPPORTED_PROTOCOL_VERSIONS)}"
        )

    return version


def ensure_protocol_compliance(response: Any, protocol_version: str | None = None) -> Any:
    """Ensure response complies with protocol version requirements.

    Args:
        response: Response data
        protocol_version: Protocol version (uses context if not provided)

    Returns:
        Protocol-compliant response
    """
    version = protocol_version or get_protocol_version()

    if version == "2024-11-05":
        return _ensure_2024_11_05_compliance(response)
    else:
        logger.warning("Unknown protocol version %s, using default compliance", version)
        return _ensure_2024_11_05_compliance(response)


def _ensure_2024_11_05_compliance(response: Any) -> Any:
    """Ensure response complies with 2024-11-05 protocol spec.

    Args:
        response: Response data

    Returns:
        Protocol-compliant response
    """
    if isinstance(response, dict):
        compliant = {}
        for key, value in response.items():
            compliant[key] = _ensure_2024_11_05_compliance(value)
        return compliant
    elif isinstance(response, list):
        return [_ensure_2024_11_05_compliance(item) for item in response]
    else:
        return response

