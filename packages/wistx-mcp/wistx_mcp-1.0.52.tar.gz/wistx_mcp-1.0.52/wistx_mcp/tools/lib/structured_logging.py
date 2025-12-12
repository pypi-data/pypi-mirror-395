"""Structured logging utilities for MCP server."""

import json
import logging
import sys
from typing import Any, Optional

logger = logging.getLogger(__name__)


class StructuredFormatter(logging.Formatter):
    """Structured log formatter that outputs JSON."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON.

        Args:
            record: Log record to format

        Returns:
            JSON string representation of log record
        """
        log_data: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id

        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id

        if hasattr(record, "tool_name"):
            log_data["tool_name"] = record.tool_name

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        if hasattr(record, "extra"):
            log_data.update(record.extra)

        return json.dumps(log_data)


class StructuredLoggerAdapter(logging.LoggerAdapter):
    """Logger adapter that adds structured context to log records."""

    def process(self, msg: str, kwargs: Any) -> tuple[str, Any]:
        """Process log message and add context.

        Args:
            msg: Log message
            kwargs: Log keyword arguments

        Returns:
            Tuple of (message, kwargs) with context added
        """
        if "extra" not in kwargs:
            kwargs["extra"] = {}

        extra = kwargs["extra"]

        if hasattr(self, "request_id"):
            extra["request_id"] = self.request_id

        if hasattr(self, "user_id"):
            extra["user_id"] = self.user_id

        if hasattr(self, "tool_name"):
            extra["tool_name"] = self.tool_name

        return msg, kwargs


def get_structured_logger(
    name: str,
    request_id: Optional[str] = None,
    user_id: Optional[str] = None,
    tool_name: Optional[str] = None,
) -> StructuredLoggerAdapter:
    """Get structured logger with context.

    Args:
        name: Logger name
        request_id: Request ID for context
        user_id: User ID for context
        tool_name: Tool name for context

    Returns:
        Structured logger adapter
    """
    base_logger = logging.getLogger(name)
    adapter = StructuredLoggerAdapter(base_logger, {})
    adapter.request_id = request_id
    adapter.user_id = user_id
    adapter.tool_name = tool_name
    return adapter


def setup_structured_logging(use_json: bool = False) -> None:
    """Setup structured logging for the application.

    Args:
        use_json: If True, use JSON formatter; otherwise use standard formatter
    """
    root_logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)

    if use_json:
        formatter = StructuredFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - [request_id=%(request_id)s] [user_id=%(user_id)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    handler.setFormatter(formatter)
    root_logger.addHandler(handler)


def get_logger_with_context(
    name: str | None = None,
    tool_name: str | None = None,
) -> StructuredLoggerAdapter:
    """Get logger with automatic context from request context.

    Automatically includes request_id and user_id from request context.

    Args:
        name: Logger name (defaults to calling module name)
        tool_name: Tool name for context

    Returns:
        Structured logger adapter with context
    """
    from wistx_mcp.tools.lib.request_context import get_request_id, get_user_id

    if name is None:
        import inspect
        frame = inspect.currentframe()
        if frame and frame.f_back:
            name = frame.f_back.f_globals.get("__name__", "wistx_mcp")
        else:
            name = "wistx_mcp"

    request_id = get_request_id()
    user_id = get_user_id()

    return get_structured_logger(
        name=name,
        request_id=request_id,
        user_id=user_id,
        tool_name=tool_name,
    )

