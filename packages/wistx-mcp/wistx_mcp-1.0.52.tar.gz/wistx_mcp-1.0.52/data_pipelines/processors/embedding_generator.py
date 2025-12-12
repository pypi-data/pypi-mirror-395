"""Embedding generator - generates vector embeddings for processed data."""

import asyncio
import json
from typing import Any

from google.api_core import exceptions as google_exceptions

from ..utils.config import PipelineSettings
from ..utils.logger import setup_logger
from ..utils.circuit_breaker import CircuitBreaker, CircuitBreakerOpenError
from ..utils.global_rate_limiter import get_global_rate_limiter
from wistx_mcp.tools.lib.gemini_client import GeminiClient

logger = setup_logger(__name__)
settings = PipelineSettings()


class QuotaExceededError(Exception):
    """Raised when Gemini quota is exceeded and retries exhausted."""


class EmbeddingGenerator:
    """Generate vector embeddings for processed data using Gemini API.

    Supports both streaming (production) and checkpointing (development) modes.
    """

    def __init__(self, save_intermediate: bool = False):
        """Initialize embedding generator.

        Args:
            save_intermediate: If True, save items with embeddings to disk (checkpointing mode)
        """
        self.save_intermediate = save_intermediate
        self.client = GeminiClient(api_key=settings.gemini_api_key)
        self.model = "gemini-embedding-001"
        self.dimension = 1536
        self.batch_size = min(settings.embedding_batch_size, 500)
        self.data_dir = settings.data_dir
        self.rate_limit_delay = 0.01
        self.quota_wait_seconds = 120
        self.rate_limit_wait_seconds = 60
        self.max_quota_retries = 3
        self.max_rate_limit_retries = 5
        self.max_concurrent_batches = 10
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=5,
            recovery_timeout=60.0,
            success_threshold=2,
        )
        self._rate_limiter: Any = None

    def to_searchable_text(self, item: dict[str, Any], data_type: str) -> str:
        """Convert item to searchable text for embedding.

        Args:
            item: Processed item dictionary
            data_type: Type of data (compliance, pricing, code)

        Returns:
            Searchable text string
        """
        if data_type == "compliance":
            text = f"{item.get('standard', '')} {item.get('control_id', '')}: {item.get('title', '')}\n"
            text += f"{item.get('description', '')}\n"
            if item.get("requirement"):
                text += f"{item['requirement']}\n"
            remediation = item.get("remediation", {})
            if isinstance(remediation, dict):
                text += f"{remediation.get('summary', '')}\n"
                for snippet in remediation.get("code_snippets", [])[:3]:
                    if isinstance(snippet, dict) and snippet.get("description"):
                        text += f"{snippet['description']}\n"
            return text

        elif data_type == "pricing":
            text = f"{item.get('cloud', '')} {item.get('service', '')} {item.get('resource_type', '')}\n"
            text += f"Region: {item.get('region', '')}\n"
            if item.get("specifications"):
                text += f"Specifications: {json.dumps(item['specifications'])}\n"
            if item.get("pricing"):
                pricing_str = json.dumps(
                    {k: v.get("hourly", 0) if isinstance(v, dict) else v for k, v in item["pricing"].items()}
                )
                text += f"Pricing: {pricing_str}\n"
            return text

        elif data_type == "code":
            contextual_description = item.get("contextual_description", "")
            if contextual_description:
                text = f"{contextual_description}\n\n"
            else:
                text = ""
            
            text += f"{item.get('title', '')}\n{item.get('description', '')}\n"
            text += f"Type: {item.get('code_type', '')}\n"
            text += f"Cloud: {item.get('cloud_provider', '')}\n"
            text += f"Services: {', '.join(item.get('services', []))}\n"
            
            resources = item.get("resources", [])
            if resources:
                text += f"Resources: {', '.join(resources[:10])}\n"
            
            best_practices = item.get("best_practices", [])
            if best_practices:
                text += f"Best Practices: {', '.join(best_practices)}\n"
            
            code = item.get("code", "")
            text += f"Code:\n{code[:2000]}\n"
            return text

        elif data_type == "knowledge":
            from ..models.knowledge_article import KnowledgeArticle
            if isinstance(item, dict):
                article = KnowledgeArticle.model_validate(item)
                searchable_text = article.to_searchable_text()
                return searchable_text
            return json.dumps(item)

        else:
            return json.dumps(item)

    async def generate_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a batch of texts.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors (1536 dimensions each)

        Raises:
            RateLimitError: If rate limit exceeded (after retries)
            CircuitBreakerOpenError: If circuit breaker is open
        """
        try:
            return await self.circuit_breaker.call_async(
                self._generate_embeddings_batch_internal,
                texts
            )
        except CircuitBreakerOpenError:
            logger.error("Gemini circuit breaker is OPEN - skipping embedding generation")
            raise
    
    async def _generate_embeddings_batch_internal(self, texts: list[str]) -> list[list[float]]:
        """Internal method to generate embeddings (wrapped by circuit breaker).

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors (1536 dimensions each)

        Raises:
            RuntimeError: If rate limit exceeded or generation fails
        """
        if self._rate_limiter is None:
            self._rate_limiter = await get_global_rate_limiter(
                max_calls=getattr(settings, "api_rate_limit_max_calls", 100),
                period=getattr(settings, "api_rate_limit_period_seconds", 60.0)
            )
            max_calls = getattr(settings, "api_rate_limit_max_calls", 100)
            period = getattr(settings, "api_rate_limit_period_seconds", 60.0)
            if max_calls != 100 or period != 60.0:
                await self._rate_limiter.update_limits(max_calls=max_calls, period=period)
        
        await self._rate_limiter.acquire()
        
        embeddings = await self.client.create_embedding(
            text=texts,
            task_type="RETRIEVAL_DOCUMENT",
        )

        if len(embeddings) != len(texts):
            logger.warning(
                "Embedding count mismatch: expected %d, got %d",
                len(texts),
                len(embeddings),
            )

        return embeddings

    async def generate_embeddings(
        self, items: list[dict[str, Any]], data_type: str
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Generate embeddings for processed items.

        Args:
            items: List of processed items (without embeddings)
            data_type: Type of data (compliance, pricing, code)

        Returns:
            Tuple of (items_with_embeddings, failed_items)
        """
        logger.info("Generating embeddings for %d %s items", len(items), data_type)

        if not items:
            return [], []

        texts = [self.to_searchable_text(item, data_type) for item in items]

        items_with_embeddings = []
        failed_items = []
        quota_retry_count = 0
        rate_limit_retry_count = 0
        quota_lock = asyncio.Lock()
        rate_limit_lock = asyncio.Lock()

        batches = [
            (texts[i : i + self.batch_size], items[i : i + self.batch_size], i)
            for i in range(0, len(texts), self.batch_size)
        ]
        
        semaphore = asyncio.Semaphore(self.max_concurrent_batches)
        
        async def process_batch(batch_texts: list[str], batch_items: list[dict[str, Any]], batch_index: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
            """Process a single embedding batch."""
            nonlocal quota_retry_count, rate_limit_retry_count
            
            async with semaphore:
                async with quota_lock:
                    if quota_retry_count > self.max_quota_retries:
                        return [], batch_items
                
                batch_embeddings_result = []
                batch_failed = []
                
                retry_attempt = 0
                max_retries = self.max_rate_limit_retries
                
                while retry_attempt <= max_retries:
                    try:
                        batch_embeddings = await self.generate_embeddings_batch(batch_texts)

                        for item, embedding in zip(batch_items, batch_embeddings):
                            if len(embedding) != self.dimension:
                                logger.warning(
                                    "Invalid embedding dimension: expected %d, got %d",
                                    self.dimension,
                                    len(embedding),
                                )
                                batch_failed.append({"item": item, "error": "Invalid embedding dimension"})
                                continue

                            item["embedding"] = embedding
                            batch_embeddings_result.append(item)

                        logger.debug(
                            "Generated embeddings for batch %d (%d items)",
                            batch_index // self.batch_size + 1,
                            len(batch_embeddings_result),
                        )

                        async with quota_lock:
                            quota_retry_count = 0
                        async with rate_limit_lock:
                            rate_limit_retry_count = 0
                        await asyncio.sleep(self.rate_limit_delay)
                        break

                    except (google_exceptions.ResourceExhausted, google_exceptions.PermissionDenied, RuntimeError) as e:
                        error_str = str(e).lower()
                        is_quota = (
                            isinstance(e, google_exceptions.PermissionDenied)
                            or "quota" in error_str
                            or "permission" in error_str
                        )
                        
                        if is_quota:
                            async with quota_lock:
                                quota_retry_count += 1
                                current_quota_count = quota_retry_count
                            
                            if current_quota_count > self.max_quota_retries:
                                logger.error(
                                    "Gemini quota exceeded after %d retries. Skipping remaining embedding generation. "
                                    "Pipeline will continue with controls saved to MongoDB (without embeddings). "
                                    "Please increase Gemini quota to generate embeddings.",
                                    self.max_quota_retries,
                                )
                                batch_failed.extend([{"item": item, "error": "Quota exceeded"} for item in batch_items])
                                break
                            
                            wait_time = self.quota_wait_seconds * (2 ** (current_quota_count - 1))
                            logger.warning(
                                "Gemini quota exceeded (attempt %d/%d). Waiting %d seconds before retry...",
                                current_quota_count,
                                self.max_quota_retries,
                                wait_time,
                            )
                            await asyncio.sleep(wait_time)
                            retry_attempt += 1
                            continue
                        else:
                            async with rate_limit_lock:
                                rate_limit_retry_count += 1
                                current_rate_limit_count = rate_limit_retry_count
                            
                            if current_rate_limit_count > self.max_rate_limit_retries:
                                logger.error("Gemini rate limit exceeded after %d retries: %s", self.max_rate_limit_retries, e)
                                batch_failed.extend([{"item": item, "error": "Rate limit exceeded"} for item in batch_items])
                                async with rate_limit_lock:
                                    rate_limit_retry_count = 0
                                break
                            
                            wait_time = min(self.rate_limit_wait_seconds * (2 ** (current_rate_limit_count - 1)), 300)
                            logger.warning(
                                "Gemini rate limit exceeded (attempt %d/%d). Waiting %d seconds before retry...",
                                current_rate_limit_count,
                                self.max_rate_limit_retries,
                                wait_time,
                            )
                            await asyncio.sleep(wait_time)
                            retry_attempt += 1
                            continue

                    except (ValueError, TypeError, KeyError) as e:
                        logger.error("Error generating embeddings for batch: %s", e)
                        batch_failed.extend([{"item": item, "error": str(e)} for item in batch_items])
                        break
                
                if retry_attempt > max_retries:
                    batch_failed.extend([{"item": item, "error": "Max retries exceeded"} for item in batch_items])
                
                return batch_embeddings_result, batch_failed
        
        tasks = [process_batch(bt, bi, idx) for bt, bi, idx in batches]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception):
                logger.error("Error processing embedding batch: %s", result, exc_info=True)
                continue
            elif isinstance(result, tuple):
                batch_embeddings, batch_failed = result
                items_with_embeddings.extend(batch_embeddings)
                failed_items.extend(batch_failed)
        
        logger.info(
            "Generated embeddings for %d items, %d failed (%s)",
            len(items_with_embeddings),
            len(failed_items),
            data_type,
        )

        if self.save_intermediate:
            self.save_with_embeddings(items_with_embeddings, data_type)

        return items_with_embeddings, failed_items

    def save_with_embeddings(self, items: list[dict[str, Any]], data_type: str) -> None:
        """Save items with embeddings to JSON file.

        Args:
            items: List of items with embeddings
            data_type: Type of data (compliance, pricing, code)
        """
        embeddings_dir = self.data_dir / data_type / "embeddings"
        embeddings_dir.mkdir(parents=True, exist_ok=True)

        output_file = embeddings_dir / f"{data_type}_with_embeddings.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, ensure_ascii=False, default=str)

        logger.info("Saved %d items with embeddings to %s", len(items), output_file)

    def filter_existing_embeddings(
        self, items: list[dict[str, Any]]
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Separate items with and without embeddings.

        Args:
            items: List of items (may or may not have embeddings)

        Returns:
            Tuple of (items_with_embeddings, items_without_embeddings)
        """
        with_embeddings = [item for item in items if item.get("embedding")]
        without_embeddings = [item for item in items if not item.get("embedding")]

        logger.info(
            "Found %d items with embeddings, %d without",
            len(with_embeddings),
            len(without_embeddings),
        )

        return with_embeddings, without_embeddings

    def generate_embedding(
        self,
        item: dict[str, Any],
        data_type: str,
    ) -> list[float] | None:
        """Generate embedding for a single item.
        
        Args:
            item: Processed item dictionary
            data_type: Type of data (compliance, pricing, code, knowledge)
            
        Returns:
            Embedding vector (1536 dimensions) or None if generation fails
        """
        try:
            text = self.to_searchable_text(item, data_type)
            embeddings = asyncio.run(self.generate_embeddings_batch([text]))
            
            if embeddings and len(embeddings) > 0:
                embedding = embeddings[0]
                if len(embedding) == self.dimension:
                    return embedding
            
            return None
        except Exception as e:
            logger.warning("Error generating embedding for single item: %s", e)
            return None
