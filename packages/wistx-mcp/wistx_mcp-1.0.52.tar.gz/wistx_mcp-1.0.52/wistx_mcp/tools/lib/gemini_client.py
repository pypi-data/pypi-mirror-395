"""Gemini LLM client implementation."""

import logging
import re

import numpy as np
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

from wistx_mcp.tools.lib.circuit_breaker import CircuitBreaker, CircuitBreakerError
from wistx_mcp.tools.lib.llm_client import LLMClient

logger = logging.getLogger(__name__)


class GeminiClient(LLMClient):
    """Gemini LLM client for embeddings and chat completions."""

    def __init__(self, api_key: str | None = None):
        """Initialize Gemini client.

        Args:
            api_key: Gemini API key (optional, can be set via environment)
        """
        try:
            if api_key:
                genai.configure(api_key=api_key)
            else:
                import os
                api_key_from_env = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
                if api_key_from_env:
                    genai.configure(api_key=api_key_from_env)
                else:
                    genai.configure()
            self.client = genai
        except Exception as e:
            logger.warning("Failed to configure Gemini client: %s", e)
            self.client = None

        self.embedding_model = "gemini-embedding-001"
        self.embedding_dimensions = 1536
        self.default_chat_model = "gemini-2.5-flash"
        self.pro_chat_model = "gemini-2.5-flash"
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=3,
            recovery_timeout=300,
            expected_exceptions=(RuntimeError,),
            name="gemini_api",
        )

    def is_available(self) -> bool:
        """Check if Gemini client is available.

        Returns:
            True if client is available, False otherwise
        """
        return self.client is not None

    async def create_embedding(self, text: str | list[str], task_type: str = "RETRIEVAL_QUERY") -> list[float] | list[list[float]]:
        """Create embedding(s) for text(s) using Gemini.

        Args:
            text: Single text string or list of text strings
            task_type: Task type ("RETRIEVAL_QUERY" or "RETRIEVAL_DOCUMENT")

        Returns:
            Single embedding vector or list of embedding vectors (normalized for 1536 dimensions)

        Raises:
            RuntimeError: If embedding generation fails
        """
        if not self.is_available():
            raise RuntimeError("Gemini client is not available")

        try:
            if isinstance(text, str):
                texts = [text]
                single = True
            else:
                texts = text
                single = False

            if single:
                result = genai.embed_content(
                    model=self.embedding_model,
                    content=text,
                    task_type=task_type,
                    output_dimensionality=self.embedding_dimensions,
                )
                embedding_data = result.get('embedding', []) if isinstance(result, dict) else getattr(result, 'embedding', [])
                embedding_values = np.array(embedding_data)
                if len(embedding_values) == 0:
                    raise RuntimeError("Empty embedding vector")
                normalized = embedding_values / np.linalg.norm(embedding_values)
                return normalized.tolist()
            else:
                embeddings = []
                for text_item in texts:
                    result = genai.embed_content(
                        model=self.embedding_model,
                        content=text_item,
                        task_type=task_type,
                        output_dimensionality=self.embedding_dimensions,
                    )
                    embedding_data = result.get('embedding', []) if isinstance(result, dict) else getattr(result, 'embedding', [])
                    embedding_values = np.array(embedding_data)
                    if len(embedding_values) == 0:
                        raise RuntimeError("Empty embedding vector")
                    normalized = embedding_values / np.linalg.norm(embedding_values)
                    embeddings.append(normalized.tolist())
                return embeddings

        except google_exceptions.ResourceExhausted as e:
            retry_delay = self._extract_retry_delay(str(e))
            logger.error("Gemini rate limit exceeded: %s (retry after %s seconds)", e, retry_delay)
            error_msg = f"Rate limit exceeded: {e}"
            if retry_delay:
                error_msg += f" (retry after {retry_delay}s)"
            raise RuntimeError(error_msg) from e
        except google_exceptions.PermissionDenied as e:
            logger.error("Gemini quota/permission error: %s", e)
            raise RuntimeError(f"Quota exceeded: {e}") from e
        except Exception as e:
            logger.error("Gemini embedding generation failed: %s", e, exc_info=True)
            raise RuntimeError(f"Embedding generation failed: {e}") from e

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        temperature: float = 0.1,
        max_tokens: int = 4000,
        response_format: dict[str, str] | None = None,
    ) -> str:
        """Create chat completion using Gemini.

        Args:
            messages: List of message dicts with "role" and "content"
            model: Model name (defaults to gemini-2.5-flash)
            temperature: Temperature for generation
            max_tokens: Maximum tokens in response
            response_format: Response format (e.g., {"type": "json_object"})

        Returns:
            Response text content

        Raises:
            RuntimeError: If chat completion fails
            CircuitBreakerError: If circuit breaker is open
        """
        if not self.is_available():
            raise RuntimeError("Gemini client is not available")

        async def _call_api() -> str:
            return await self._chat_completion_internal(
                messages, model, temperature, max_tokens, response_format
            )

        try:
            return await self.circuit_breaker.call(_call_api)
        except CircuitBreakerError as e:
            logger.warning("Gemini API circuit breaker is open: %s", e)
            raise RuntimeError(f"Gemini API temporarily unavailable: {e}") from e

    async def _chat_completion_internal(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        temperature: float = 0.1,
        max_tokens: int = 4000,
        response_format: dict[str, str] | None = None,
    ) -> str:
        """Internal chat completion implementation."""
        try:
            model_name = model or self.default_chat_model

            prompt_parts = []
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "system":
                    prompt_parts.append(f"System: {content}\n\n")
                elif role == "user":
                    prompt_parts.append(f"User: {content}\n\n")
                elif role == "assistant":
                    prompt_parts.append(f"Assistant: {content}\n\n")

            prompt = "".join(prompt_parts).strip()

            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }

            if response_format and response_format.get("type") == "json_object":
                generation_config["response_mime_type"] = "application/json"

            model_instance = genai.GenerativeModel(model_name)
            response = model_instance.generate_content(
                prompt,
                generation_config=generation_config,
            )

            if not response or not response.text:
                raise RuntimeError("Empty response from Gemini")

            return response.text.strip()
        except google_exceptions.ResourceExhausted as e:
            retry_delay = self._extract_retry_delay(str(e))
            logger.error("Gemini rate limit exceeded: %s (retry after %s seconds)", e, retry_delay)
            error_msg = f"Rate limit exceeded: {e}"
            if retry_delay:
                error_msg += f" (retry after {retry_delay}s)"
            raise RuntimeError(error_msg) from e
        except google_exceptions.PermissionDenied as e:
            logger.error("Gemini quota/permission error: %s", e)
            raise RuntimeError(f"Quota exceeded: {e}") from e
        except Exception as e:
            logger.error("Gemini chat completion failed: %s", e, exc_info=True)
            raise RuntimeError(f"Chat completion failed: {e}") from e

    def _extract_retry_delay(self, error_message: str) -> float | None:
        """Extract retry delay from Gemini API error message.

        Args:
            error_message: Error message from Gemini API

        Returns:
            Retry delay in seconds or None if not found
        """
        patterns = [
            r"Please retry in ([\d.]+)s",
            r"retry_delay.*?seconds[:\s]+(\d+)",
            r"retry.*?(\d+).*?second",
        ]
        for pattern in patterns:
            match = re.search(pattern, error_message, re.IGNORECASE)
            if match:
                try:
                    return float(match.group(1))
                except (ValueError, IndexError):
                    continue
        return None

