"""Comprehensive audit logging for all tool calls, results, errors, and auth events."""

import json
import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


class ComprehensiveAuditLogger:
    """Log all tool calls, results, errors, and authentication events."""

    def __init__(self, storage_backend=None, retention_days: int = 90):
        """Initialize comprehensive audit logger.
        
        Args:
            storage_backend: Backend for storing audit logs (e.g., database)
            retention_days: Number of days to retain logs
        """
        self.storage_backend = storage_backend
        self.retention_days = retention_days
        self.audit_logs = []

    def log_tool_call(self, tool_name: str, user_id: str, arguments: dict[str, Any],
                     request_id: str | None = None) -> str:
        """Log a tool call.
        
        Args:
            tool_name: Name of the tool
            user_id: User identifier
            arguments: Tool arguments
            request_id: Optional request identifier
            
        Returns:
            Log entry ID
        """
        try:
            log_entry = {
                "event_type": "tool_call",
                "timestamp": time.time(),
                "tool_name": tool_name,
                "user_id": user_id,
                "arguments": arguments,
                "request_id": request_id,
            }
            
            self._store_log(log_entry)
            logger.info(f"Logged tool call: {tool_name} by {user_id}")
            return log_entry.get("id", "")
        except Exception as e:
            logger.error(f"Error logging tool call: {e}", exc_info=True)
            return ""

    def log_tool_result(self, tool_name: str, user_id: str, result: Any,
                       execution_time: float, request_id: str | None = None) -> None:
        """Log a tool result.
        
        Args:
            tool_name: Name of the tool
            user_id: User identifier
            result: Tool result
            execution_time: Time taken to execute
            request_id: Optional request identifier
        """
        try:
            log_entry = {
                "event_type": "tool_result",
                "timestamp": time.time(),
                "tool_name": tool_name,
                "user_id": user_id,
                "result_size": len(str(result)),
                "execution_time": execution_time,
                "request_id": request_id,
            }
            
            self._store_log(log_entry)
            logger.info(f"Logged tool result: {tool_name} ({execution_time:.2f}s)")
        except Exception as e:
            logger.error(f"Error logging tool result: {e}", exc_info=True)

    def log_tool_error(self, tool_name: str, user_id: str, error: str,
                      error_type: str | None = None, request_id: str | None = None) -> None:
        """Log a tool error.
        
        Args:
            tool_name: Name of the tool
            user_id: User identifier
            error: Error message
            error_type: Type of error
            request_id: Optional request identifier
        """
        try:
            log_entry = {
                "event_type": "tool_error",
                "timestamp": time.time(),
                "tool_name": tool_name,
                "user_id": user_id,
                "error": error,
                "error_type": error_type,
                "request_id": request_id,
            }
            
            self._store_log(log_entry)
            logger.warning(f"Logged tool error: {tool_name} - {error_type}")
        except Exception as e:
            logger.error(f"Error logging tool error: {e}", exc_info=True)

    def log_authentication(self, user_id: str, auth_method: str, success: bool,
                          reason: str | None = None) -> None:
        """Log authentication event.
        
        Args:
            user_id: User identifier
            auth_method: Authentication method used
            success: Whether authentication succeeded
            reason: Reason for failure if unsuccessful
        """
        try:
            log_entry = {
                "event_type": "authentication",
                "timestamp": time.time(),
                "user_id": user_id,
                "auth_method": auth_method,
                "success": success,
                "reason": reason,
            }
            
            self._store_log(log_entry)
            status = "successful" if success else "failed"
            logger.info(f"Logged authentication {status}: {user_id} via {auth_method}")
        except Exception as e:
            logger.error(f"Error logging authentication: {e}", exc_info=True)

    def log_rate_limit(self, user_id: str, tool_name: str | None = None,
                      retry_after: int | None = None) -> None:
        """Log rate limit event.
        
        Args:
            user_id: User identifier
            tool_name: Optional tool name
            retry_after: Seconds to wait before retry
        """
        try:
            log_entry = {
                "event_type": "rate_limit",
                "timestamp": time.time(),
                "user_id": user_id,
                "tool_name": tool_name,
                "retry_after": retry_after,
            }
            
            self._store_log(log_entry)
            logger.warning(f"Logged rate limit: {user_id}")
        except Exception as e:
            logger.error(f"Error logging rate limit: {e}", exc_info=True)

    def log_permission_denied(self, user_id: str, tool_name: str, reason: str) -> None:
        """Log permission denied event.
        
        Args:
            user_id: User identifier
            tool_name: Name of the tool
            reason: Reason for denial
        """
        try:
            log_entry = {
                "event_type": "permission_denied",
                "timestamp": time.time(),
                "user_id": user_id,
                "tool_name": tool_name,
                "reason": reason,
            }
            
            self._store_log(log_entry)
            logger.warning(f"Logged permission denied: {user_id} for {tool_name}")
        except Exception as e:
            logger.error(f"Error logging permission denied: {e}", exc_info=True)

    def _store_log(self, log_entry: dict[str, Any]) -> None:
        """Store a log entry.
        
        Args:
            log_entry: Log entry to store
        """
        log_entry["id"] = f"{log_entry['timestamp']}-{len(self.audit_logs)}"
        self.audit_logs.append(log_entry)
        
        if self.storage_backend:
            try:
                self.storage_backend.store(log_entry)
            except Exception as e:
                logger.error(f"Error storing log in backend: {e}", exc_info=True)

    def get_logs(self, user_id: str | None = None, tool_name: str | None = None,
                event_type: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
        """Get audit logs with optional filtering.
        
        Args:
            user_id: Optional user filter
            tool_name: Optional tool filter
            event_type: Optional event type filter
            limit: Maximum number of logs to return
            
        Returns:
            List of matching log entries
        """
        logs = self.audit_logs
        
        if user_id:
            logs = [log for log in logs if log.get("user_id") == user_id]
        
        if tool_name:
            logs = [log for log in logs if log.get("tool_name") == tool_name]
        
        if event_type:
            logs = [log for log in logs if log.get("event_type") == event_type]
        
        return logs[-limit:]

    def get_user_activity(self, user_id: str) -> dict[str, Any]:
        """Get activity summary for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with user activity summary
        """
        user_logs = [log for log in self.audit_logs if log.get("user_id") == user_id]
        
        return {
            "user_id": user_id,
            "total_events": len(user_logs),
            "tool_calls": len([log for log in user_logs if log.get("event_type") == "tool_call"]),
            "errors": len([log for log in user_logs if log.get("event_type") == "tool_error"]),
            "rate_limits": len([log for log in user_logs if log.get("event_type") == "rate_limit"]),
            "auth_events": len([log for log in user_logs if log.get("event_type") == "authentication"]),
            "recent_logs": user_logs[-10:],
        }

    def cleanup_old_logs(self) -> int:
        """Clean up logs older than retention period.
        
        Returns:
            Number of logs cleaned up
        """
        cutoff_time = time.time() - (self.retention_days * 86400)
        initial_count = len(self.audit_logs)
        
        self.audit_logs = [log for log in self.audit_logs if log.get("timestamp", 0) > cutoff_time]
        
        cleaned_count = initial_count - len(self.audit_logs)
        if cleaned_count > 0:
            logger.info(f"Cleaned up {cleaned_count} old audit logs")
        
        return cleaned_count

    def export_logs(self, user_id: str | None = None) -> str:
        """Export logs as JSON.
        
        Args:
            user_id: Optional user filter
            
        Returns:
            JSON string of logs
        """
        logs = self.get_logs(user_id=user_id, limit=10000)
        return json.dumps(logs, indent=2, default=str)

