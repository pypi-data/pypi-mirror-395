"""MCP error handler for JSON-RPC protocol compliance."""

import logging
import uuid
from typing import Any

logger = logging.getLogger(__name__)

try:
    from mcp.types import ErrorCode
except ImportError:
    logger.warning("MCP SDK ErrorCode not available, using fallback")
    class ErrorCode:
        INVALID_REQUEST = -32600
        METHOD_NOT_FOUND = -32601
        INVALID_PARAMS = -32602
        INTERNAL_ERROR = -32603

from wistx_mcp.tools.lib.mcp_errors import MCPError, MCPErrorCode

ERROR_CODE_MAPPING = {
    MCPErrorCode.INVALID_REQUEST: ErrorCode.INVALID_REQUEST,
    MCPErrorCode.METHOD_NOT_FOUND: ErrorCode.METHOD_NOT_FOUND,
    MCPErrorCode.INVALID_PARAMS: ErrorCode.INVALID_PARAMS,
    MCPErrorCode.INTERNAL_ERROR: ErrorCode.INTERNAL_ERROR,
    MCPErrorCode.TIMEOUT: ErrorCode.INTERNAL_ERROR,
    MCPErrorCode.RATE_LIMIT_EXCEEDED: ErrorCode.INTERNAL_ERROR,
}


def serialize_mcp_error(error: MCPError) -> dict[str, Any]:
    """Serialize MCPError to JSON-RPC error format.

    Args:
        error: MCPError instance

    Returns:
        JSON-RPC error object with code, message, and data
    """
    jsonrpc_code = ERROR_CODE_MAPPING.get(
        error.code,
        ErrorCode.INTERNAL_ERROR
    )

    return {
        "code": jsonrpc_code,
        "message": error.message,
        "data": {
            **error.data,
            "original_code": error.code,
        }
    }


def handle_mcp_error(error: Exception) -> dict[str, Any]:
    """Handle and serialize any exception to JSON-RPC format.

    Args:
        error: Exception to handle

    Returns:
        JSON-RPC error object
    """
    if isinstance(error, MCPError):
        return serialize_mcp_error(error)

    error_id = str(uuid.uuid4())
    logger.error("Unexpected error [error_id=%s]: %s", error_id, error, exc_info=True)
    return {
        "code": ErrorCode.INTERNAL_ERROR,
        "message": "An internal error occurred",
        "data": {
            "error_id": error_id,
        }
    }

