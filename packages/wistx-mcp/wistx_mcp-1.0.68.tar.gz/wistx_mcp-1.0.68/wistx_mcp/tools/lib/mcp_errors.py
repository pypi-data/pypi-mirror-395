"""MCP error handling utilities."""

from typing import Any

try:
    from mcp.types import ErrorCode as MCPErrorCodeType
except ImportError:
    MCPErrorCodeType = None


class MCPError(Exception):
    """Base MCP error exception with JSON-RPC compliance."""

    def __init__(
        self,
        code: int,
        message: str,
        data: dict[str, Any] | None = None,
        jsonrpc_code: int | None = None,
    ):
        """Initialize MCP error.

        Args:
            code: Custom error code (integer)
            message: Error message
            data: Optional error data
            jsonrpc_code: JSON-RPC error code (if different from custom code)
        """
        super().__init__(message)
        self.code = code
        self.message = message
        self.data = data or {}
        self.jsonrpc_code = jsonrpc_code

    def to_jsonrpc(self) -> dict[str, Any]:
        """Convert to JSON-RPC error format.

        Returns:
            JSON-RPC error object
        """
        from wistx_mcp.tools.lib.mcp_error_handler import ERROR_CODE_MAPPING

        if self.jsonrpc_code is not None:
            jsonrpc_code = self.jsonrpc_code
        else:
            jsonrpc_code = ERROR_CODE_MAPPING.get(
                self.code,
                -32603 if MCPErrorCodeType is None else MCPErrorCodeType.INTERNAL_ERROR
            )

        return {
            "code": jsonrpc_code,
            "message": self.message,
            "data": {
                **self.data,
                "original_code": self.code,
            }
        }


class MCPErrorCode:
    """MCP error codes."""

    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603
    TIMEOUT = -1000
    RATE_LIMIT_EXCEEDED = -1001


def create_mcp_error(code: int, message: str, data: dict[str, Any] | None = None) -> MCPError:
    """Create an MCP error exception.

    Args:
        code: Error code (integer)
        message: Error message
        data: Optional error data

    Returns:
        MCPError instance
    """
    return MCPError(code=code, message=message, data=data)

