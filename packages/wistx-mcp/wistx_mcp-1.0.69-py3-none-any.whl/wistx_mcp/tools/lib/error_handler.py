"""Enhanced error handling with remediation steps."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class ErrorHandler:
    """Enhanced error handler with remediation guidance."""

    ERROR_REMEDIATIONS: dict[str, dict[str, Any]] = {
        "ValueError": {
            "message": "Invalid parameter provided",
            "remediation": [
                "Check parameter types and values",
                "Verify required parameters are provided",
                "Review tool documentation for correct parameter format",
            ],
        },
        "ConnectionError": {
            "message": "Failed to connect to service",
            "remediation": [
                "Check network connectivity",
                "Verify service is running",
                "Check firewall rules",
                "Verify credentials are correct",
            ],
        },
        "TimeoutError": {
            "message": "Operation timed out",
            "remediation": [
                "Check network latency",
                "Verify service is responsive",
                "Consider increasing timeout value",
                "Check for rate limiting",
            ],
        },
        "FileNotFoundError": {
            "message": "File or directory not found",
            "remediation": [
                "Verify file path is correct",
                "Check file permissions",
                "Ensure directory exists",
            ],
        },
        "PermissionError": {
            "message": "Permission denied",
            "remediation": [
                "Check file/directory permissions",
                "Verify user has required access",
                "Check authentication credentials",
            ],
        },
        "JSONDecodeError": {
            "message": "Invalid JSON format",
            "remediation": [
                "Validate JSON syntax",
                "Check for missing quotes or commas",
                "Use a JSON validator tool",
            ],
        },
        "YAMLError": {
            "message": "Invalid YAML format",
            "remediation": [
                "Validate YAML syntax",
                "Check indentation",
                "Verify all quotes are properly closed",
            ],
        },
    }

    @staticmethod
    def format_error_with_remediation(
        error: Exception,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Format error with remediation steps.

        Args:
            error: Exception that occurred
            context: Additional context about the error

        Returns:
            Dictionary with error details and remediation
        """
        error_type = type(error).__name__
        error_message = str(error)

        remediation_info = ErrorHandler.ERROR_REMEDIATIONS.get(error_type, {})
        remediation_steps = remediation_info.get("remediation", [])

        if context:
            if "tool_name" in context:
                remediation_steps.insert(
                    0,
                    f"Review {context['tool_name']} tool documentation",
                )
            if "parameter" in context:
                remediation_steps.insert(
                    0,
                    f"Check parameter '{context['parameter']}' value and type",
                )

        return {
            "error_type": error_type,
            "error_message": error_message,
            "remediation_steps": remediation_steps,
            "context": context or {},
        }

    @staticmethod
    def get_user_friendly_error_message(error: Exception, tool_name: str | None = None) -> str:
        """Get user-friendly error message with remediation.

        Args:
            error: Exception that occurred
            tool_name: Name of the tool that failed

        Returns:
            User-friendly error message
        """
        error_type = type(error).__name__
        error_message = str(error)

        remediation_info = ErrorHandler.ERROR_REMEDIATIONS.get(error_type, {})
        base_message = remediation_info.get("message", "An error occurred")

        message_parts = [f"❌ {base_message}: {error_message}"]

        if tool_name:
            message_parts.append(f"\n**Tool**: {tool_name}")
            try:
                from wistx_mcp.tools.lib.tool_descriptions import ToolDescriptionManager
                short_desc = ToolDescriptionManager.get_short_description(tool_name)
                if short_desc:
                    message_parts.append(f"\n**Tool Description**: {short_desc}")
                message_parts.append(
                    f"\n**To get full documentation**: Use `wistx_get_tool_documentation` tool with `tool_name=\"{tool_name}\"`"
                )
            except Exception:
                pass

        remediation_steps = remediation_info.get("remediation", [])
        if remediation_steps:
            message_parts.append("\n**Suggested Fixes**:")
            for i, step in enumerate(remediation_steps[:3], 1):
                message_parts.append(f"{i}. {step}")

        return "\n".join(message_parts)

