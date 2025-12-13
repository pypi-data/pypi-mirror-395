"""LLM client abstraction layer for embeddings and chat completions."""

import logging
from abc import ABC, abstractmethod
from typing import Any

logger = logging.getLogger(__name__)


class LLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    async def create_embedding(self, text: str | list[str], task_type: str = "RETRIEVAL_QUERY") -> list[float] | list[list[float]]:
        """Create embedding(s) for text(s).

        Args:
            text: Single text string or list of text strings
            task_type: Task type for embedding (e.g., "RETRIEVAL_QUERY", "RETRIEVAL_DOCUMENT")

        Returns:
            Single embedding vector or list of embedding vectors
        """
        pass

    @abstractmethod
    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        temperature: float = 0.1,
        max_tokens: int = 4000,
        response_format: dict[str, str] | None = None,
    ) -> str:
        """Create chat completion.

        Args:
            messages: List of message dicts with "role" and "content"
            model: Model name (optional, uses default if not provided)
            temperature: Temperature for generation
            max_tokens: Maximum tokens in response
            response_format: Response format (e.g., {"type": "json_object"})

        Returns:
            Response text content
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if client is available and configured.

        Returns:
            True if client is available, False otherwise
        """
        pass

