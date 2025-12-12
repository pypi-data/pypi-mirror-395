"""Conversation context management for maintaining state between tool calls."""

import logging
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any

logger = logging.getLogger(__name__)


class ConversationContext:
    """Manage conversation context and state."""

    def __init__(self, session_id: str, user_id: str | None = None):
        """Initialize conversation context.

        Args:
            session_id: Unique session identifier
            user_id: User identifier (optional)
        """
        self.session_id = session_id
        self.user_id = user_id
        self.messages: list[dict[str, Any]] = []
        self.tool_calls: list[dict[str, Any]] = []
        self.tool_results: dict[str, Any] = {}
        self.user_preferences: dict[str, Any] = {}
        self.created_at = datetime.utcnow()
        self.last_activity = datetime.utcnow()

    def add_message(self, role: str, content: str, metadata: dict[str, Any] | None = None) -> None:
        """Add message to conversation history.

        Args:
            role: Message role (user, assistant, system)
            content: Message content
            metadata: Optional metadata
        """
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata or {},
        })
        self.last_activity = datetime.utcnow()

    def add_tool_call(self, tool_name: str, arguments: dict[str, Any], result: Any) -> None:
        """Add tool call to history.

        Args:
            tool_name: Name of the tool called
            arguments: Tool arguments
            result: Tool result
        """
        call_record = {
            "tool_name": tool_name,
            "arguments": arguments,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.tool_calls.append(call_record)
        self.tool_results[tool_name] = result
        self.last_activity = datetime.utcnow()

    def get_recent_context(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get recent conversation context.

        Args:
            limit: Maximum number of messages to return

        Returns:
            List of recent messages
        """
        return self.messages[-limit:]

    def get_tool_history(self, tool_name: str | None = None) -> list[dict[str, Any]]:
        """Get tool call history.

        Args:
            tool_name: Optional tool name filter

        Returns:
            List of tool calls
        """
        if tool_name:
            return [call for call in self.tool_calls if call["tool_name"] == tool_name]
        return self.tool_calls

    def get_last_tool_result(self, tool_name: str) -> Any | None:
        """Get last result from a tool.

        Args:
            tool_name: Name of the tool

        Returns:
            Last tool result or None
        """
        return self.tool_results.get(tool_name)

    def summarize_context(self, max_length: int = 1000) -> str:
        """Summarize conversation context.

        Args:
            max_length: Maximum summary length

        Returns:
            Context summary string
        """
        summary_parts = []

        if self.tool_calls:
            recent_tools = self.tool_calls[-5:]
            tool_summary = ", ".join([call["tool_name"] for call in recent_tools])
            summary_parts.append(f"Recent tools used: {tool_summary}")

        if self.messages:
            recent_messages = self.messages[-3:]
            message_summary = " | ".join([
                f"{msg['role']}: {msg['content'][:100]}"
                for msg in recent_messages
            ])
            summary_parts.append(f"Recent conversation: {message_summary}")

        summary = ". ".join(summary_parts)
        if len(summary) > max_length:
            summary = summary[:max_length] + "..."

        return summary


class ConversationContextManager:
    """Manage multiple conversation contexts."""

    def __init__(self, ttl_hours: int = 24):
        """Initialize context manager.

        Args:
            ttl_hours: Time-to-live for contexts in hours
        """
        self.contexts: dict[str, ConversationContext] = {}
        self.ttl_hours = ttl_hours

    def get_or_create_context(self, session_id: str, user_id: str | None = None) -> ConversationContext:
        """Get or create conversation context.

        Args:
            session_id: Session identifier
            user_id: User identifier

        Returns:
            Conversation context
        """
        if session_id not in self.contexts:
            self.contexts[session_id] = ConversationContext(session_id, user_id)
        else:
            self.contexts[session_id].last_activity = datetime.utcnow()

        return self.contexts[session_id]

    def get_context(self, session_id: str) -> ConversationContext | None:
        """Get conversation context.

        Args:
            session_id: Session identifier

        Returns:
            Conversation context or None if not found
        """
        context = self.contexts.get(session_id)
        if context:
            age = datetime.utcnow() - context.last_activity
            if age > timedelta(hours=self.ttl_hours):
                del self.contexts[session_id]
                return None
        return context

    def cleanup_expired(self) -> int:
        """Clean up expired contexts.

        Returns:
            Number of contexts cleaned up
        """
        now = datetime.utcnow()
        expired = [
            session_id
            for session_id, context in self.contexts.items()
            if now - context.last_activity > timedelta(hours=self.ttl_hours)
        ]

        for session_id in expired:
            del self.contexts[session_id]

        return len(expired)


_global_context_manager: ConversationContextManager | None = None


def get_conversation_context_manager() -> ConversationContextManager:
    """Get global conversation context manager.

    Returns:
        ConversationContextManager instance
    """
    global _global_context_manager
    if _global_context_manager is None:
        _global_context_manager = ConversationContextManager()
    return _global_context_manager

