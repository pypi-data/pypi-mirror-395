"""Universal base collector with Crawl4AI integration.

This base class provides:
- Crawl4AI-based web crawling with JavaScript rendering
- Deep crawling support with configurable depth
- LLM-ready markdown generation
- Data validation using Pydantic models
- Error tracking with CollectionResult
- Deduplication
- Metrics collection
- Progress tracking
"""

import asyncio
import json
import time
from abc import ABC, abstractmethod
from collections.abc import Awaitable
from typing import Any, Callable

from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler
from pydantic import ValidationError
from tqdm import tqdm

try:
    from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
    HAS_DEEP_CRAWL = True
except ImportError:
    HAS_DEEP_CRAWL = False
    BFSDeepCrawlStrategy = None

from .collection_result import (
    CollectionMetrics,
    CollectionResult,
)
from ..utils.config import settings
from ..utils.logger import setup_logger
from ..utils.rate_limiter import RateLimiter

logger = setup_logger(__name__)


class BaseCollector(ABC):
    """Universal base collector for all data collection types.

    Uses Crawl4AI exclusively for web scraping with parallel processing support.

    Provides shared functionality:
    - Crawl4AI-based web crawling with JavaScript rendering
    - Parallel URL processing with asyncio
    - LLM-ready markdown generation
    - Data validation using Pydantic models
    - Error tracking with CollectionResult
    - Deduplication
    - Metrics collection
    - Progress tracking

    Subclasses implement:
    - get_source_urls() - Returns list of URLs to collect
    - parse_data() - Parses response and extracts data
    - get_validation_model() - Returns Pydantic model for validation
    - get_deduplication_key() - Returns key for deduplication
    """

    def __init__(
        self,
        collector_name: str,
        version: str,
        data_type: str,
        rate_limit: tuple[int, float] = (50, 60),
        data_subdir: str | None = None,
        use_markdown: bool = True,
        bypass_cache: bool = True,
        max_concurrent: int = 20,
        enable_deep_crawl: bool = True,
        max_depth: int = 30,
        max_pages: int = 500,
        include_external: bool = False,
        score_threshold: float = 0.3,
    ):
        """Initialize universal collector.

        Args:
            collector_name: Name of collector (e.g., "PCI-DSS", "pricing-aws")
            version: Version string (e.g., "4.0", "2024")
            data_type: Data type ("compliance", "pricing", "code", "docs")
            rate_limit: Rate limit tuple (max_calls, period_seconds)
            data_subdir: Optional subdirectory for data storage
            use_markdown: If True, use markdown output; else use HTML
            bypass_cache: If True, bypass Crawl4AI cache
            max_concurrent: Maximum concurrent URLs to process in parallel
            enable_deep_crawl: If True, enable deep crawling of linked pages
            max_depth: Maximum crawl depth (0 = single page, 1 = +1 level, 2 = +2 levels)
            max_pages: Maximum pages to crawl per URL
            include_external: If True, follow external links; else stay within domain
            score_threshold: Minimum relevance score (0.0-1.0) for URLs to crawl
        """
        self.collector_name = collector_name
        self.version = version
        self.data_type = data_type
        self.rate_limiter = RateLimiter(max_calls=rate_limit[0], period=rate_limit[1])
        self.use_markdown = use_markdown
        self.bypass_cache = bypass_cache
        self.max_concurrent = max_concurrent
        self.enable_deep_crawl = enable_deep_crawl and HAS_DEEP_CRAWL
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.include_external = include_external
        self.score_threshold = score_threshold
        self._crawler: AsyncWebCrawler | None = None
        self._crawl_strategy: Any = None

        if self.enable_deep_crawl and HAS_DEEP_CRAWL:
            try:
                self._crawl_strategy = BFSDeepCrawlStrategy(
                    max_depth=max_depth,
                    include_external=include_external,
                    max_pages=max_pages,
                    score_threshold=score_threshold,
                )
                logger.info(
                    "Deep crawling enabled for %s: max_depth=%d, max_pages=%d, include_external=%s",
                    collector_name,
                    max_depth,
                    max_pages,
                    include_external,
                )
            except Exception as e:
                logger.warning(
                    "Failed to initialize deep crawl strategy for %s: %s. Falling back to single-page crawling.",
                    collector_name,
                    e,
                )
                self.enable_deep_crawl = False
        elif enable_deep_crawl and not HAS_DEEP_CRAWL:
            logger.warning(
                "Deep crawling requested but crawl4ai.deep_crawling not available. "
                "Install latest crawl4ai: pip install --upgrade crawl4ai"
            )
            self.enable_deep_crawl = False

        data_subdir = data_subdir or data_type
        self.data_dir = settings.data_dir / data_subdir / "raw"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.output_file = self.data_dir / f"{collector_name.lower().replace('-', '_')}-raw.json"

        self.metrics = CollectionMetrics()

    async def _get_crawler(self) -> AsyncWebCrawler:
        """Get or create AsyncWebCrawler instance.

        Returns:
            AsyncWebCrawler instance

        Raises:
            RuntimeError: If Playwright browsers are not installed
        """
        if self._crawler is None:
            try:
                self._crawler = AsyncWebCrawler()
            except Exception as e:
                error_msg = str(e)
                if "Executable doesn't exist" in error_msg or "playwright" in error_msg.lower():
                    logger.error(
                        "Playwright browsers not installed. Please run: playwright install\n"
                        "Error details: %s",
                        error_msg,
                    )
                    raise RuntimeError(
                        "Playwright browsers not installed. Run 'playwright install' to install browsers."
                    ) from e
                raise
        return self._crawler

    async def fetch_page_async(self, url: str, **kwargs: Any) -> Any:
        """Fetch page using Crawl4AI with optional deep crawling (async).

        If deep crawling is enabled, follows links within the same domain up to max_depth levels.

        Args:
            url: URL to fetch
            **kwargs: Additional arguments for Crawl4AI (will override crawl_strategy if provided)

        Returns:
            CrawlResult object with markdown, HTML, and metadata.
            For deep crawling, returns aggregated results from all crawled pages.

        Raises:
            Exception: If fetch fails
        """
        await self._rate_limit_async()
        crawler = await self._get_crawler()

        crawl_kwargs = {
            "url": url,
            "bypass_cache": self.bypass_cache,
        }

        if self.enable_deep_crawl and self._crawl_strategy and "crawl_strategy" not in kwargs:
            crawl_kwargs["crawl_strategy"] = self._crawl_strategy
            logger.debug(
                "Deep crawling enabled for %s (depth=%d, max_pages=%d)",
                url,
                self.max_depth,
                self.max_pages,
            )

        crawl_kwargs.update(kwargs)

        result = await crawler.arun(**crawl_kwargs)

        if self.enable_deep_crawl and hasattr(result, "crawled_pages") and result.crawled_pages:
            logger.info(
                "Deep crawl completed for %s: %d pages crawled",
                url,
                len(result.crawled_pages),
            )

        return result

    async def _rate_limit_async(self) -> None:
        """Async rate limiting helper."""
        with self.rate_limiter.lock:
            now = time.time()
            while self.rate_limiter.calls and self.rate_limiter.calls[0] < now - self.rate_limiter.period:
                self.rate_limiter.calls.popleft()
            if len(self.rate_limiter.calls) >= self.rate_limiter.max_calls:
                sleep_time = self.rate_limiter.period - (now - self.rate_limiter.calls[0])
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                    await self._rate_limit_async()
                    return
            self.rate_limiter.calls.append(time.time())

    def fetch_page(self, url: str, **kwargs: Any) -> str | BeautifulSoup:
        """Fetch page using Crawl4AI (sync wrapper).

        Args:
            url: URL to fetch
            **kwargs: Additional arguments for Crawl4AI

        Returns:
            Markdown string if use_markdown=True, else BeautifulSoup object

        Raises:
            Exception: If fetch fails
        """
        result = asyncio.run(self.fetch_page_async(url, **kwargs))

        if self.use_markdown:
            return result.markdown or ""
        else:
            return BeautifulSoup(result.html or "", "lxml")

    async def fetch_json_async(self, url: str, **kwargs: Any) -> dict[str, Any] | list[dict[str, Any]]:
        """Fetch JSON data using Crawl4AI (async).

        Args:
            url: URL to fetch
            **kwargs: Additional arguments for Crawl4AI

        Returns:
            Parsed JSON data

        Raises:
            Exception: If fetch fails
            json.JSONDecodeError: If JSON parsing fails
        """
        result = await self.fetch_page_async(url, **kwargs)
        content = result.markdown or result.html or result.text or ""

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON from %s, trying to extract from HTML", url)
            soup = BeautifulSoup(result.html or "", "lxml")
            json_scripts = soup.find_all("script", type="application/json")
            if json_scripts:
                return json.loads(json_scripts[0].string)
            raise

    def fetch_json(self, url: str, **kwargs: Any) -> dict[str, Any] | list[dict[str, Any]]:
        """Fetch JSON data using Crawl4AI (sync wrapper).

        Args:
            url: URL to fetch
            **kwargs: Additional arguments

        Returns:
            Parsed JSON data

        Raises:
            Exception: If fetch fails
            json.JSONDecodeError: If JSON parsing fails
        """
        return asyncio.run(self.fetch_json_async(url, **kwargs))

    def validate_data(
        self,
        data: list[dict[str, Any]],
        validation_model: type[Any] | None = None,
        result: CollectionResult | None = None,
    ) -> list[dict[str, Any]]:
        """Validate data using Pydantic models.

        Args:
            data: List of data dictionaries to validate
            validation_model: Pydantic model class (if None, uses get_validation_model())
            result: Optional CollectionResult to track validation errors

        Returns:
            List of validated data dictionaries
        """
        validation_model_to_use = validation_model
        if validation_model_to_use is None:
            model_result = self.get_validation_model()
            if model_result is None:
                logger.warning("No validation model defined, skipping validation")
                return data
            validation_model_to_use = model_result  # type: ignore[assignment]

        if result is None:
            metrics = CollectionMetrics()
        else:
            metrics = result.metrics
        validated = []

        for item in data:
            try:
                item_for_validation = self._normalize_item_for_validation(item)
                validated_item = validation_model_to_use(**item_for_validation)
                validated.append(validated_item.model_dump())
            except ValidationError as e:
                metrics.validation_errors += 1
                item_id = (
                    item.get("control_id")
                    or item.get("benchmark_id")
                    or item.get("article_id")
                    or item.get("requirement_id")
                    or item.get("title", "unknown")
                )
                logger.warning("Validation error for item %s: %s", item_id, e)
                logger.debug("Item data: %s", {k: v for k, v in item.items() if k not in ["remediation", "references"]})

                if result:
                    result.add_error(
                        item.get("source_url", ""),
                        "ValidationError",
                        f"Item {item_id}: {str(e)}",
                    )
                continue
            except (TypeError, ValueError) as e:
                metrics.validation_errors += 1
                item_id = item.get("control_id") or item.get("title", "unknown")
                logger.warning("Error validating item %s: %s", item_id, e)
                if result:
                    result.add_error(
                        item.get("source_url", ""),
                        "ValidationError",
                        f"Item {item_id}: {str(e)}",
                    )
                continue

        logger.info(
            "Validated %d/%d items (%d validation errors)",
            len(validated),
            len(data),
            metrics.validation_errors,
        )

        return validated

    def _normalize_item_for_validation(self, item: dict[str, Any]) -> dict[str, Any]:
        """Normalize item structure for validation.

        Converts LLM-extracted controls to match RawComplianceControl structure.

        Args:
            item: Raw item dictionary (may have LLM structure)

        Returns:
            Normalized item dictionary
        """
        normalized = item.copy()

        if "remediation" in normalized and isinstance(normalized["remediation"], dict):
            remediation_dict = normalized["remediation"]
            remediation_parts = []
            if remediation_dict.get("summary"):
                remediation_parts.append(str(remediation_dict["summary"]))
            if remediation_dict.get("steps") and isinstance(remediation_dict["steps"], list):
                remediation_parts.extend([str(s) for s in remediation_dict["steps"]])
            normalized["remediation"] = "\n".join(remediation_parts) if remediation_parts else None

        if "references" in normalized:
            normalized.pop("references", None)

        if "applies_to" in normalized:
            normalized.pop("applies_to", None)

        # DO NOT remove severity - it's needed for processing stage
        # if "severity" in normalized:
        #     normalized.pop("severity", None)

        if "category" in normalized:
            normalized.pop("category", None)

        if "subcategory" in normalized:
            normalized.pop("subcategory", None)

        if not normalized.get("control_id"):
            if normalized.get("title"):
                normalized["control_id"] = str(normalized["title"])[:50]
            elif normalized.get("requirement"):
                normalized["control_id"] = str(normalized["requirement"])[:50]
            else:
                normalized["control_id"] = "unknown"

        if not normalized.get("requirement") and normalized.get("description"):
            normalized["requirement"] = str(normalized["description"])

        if not normalized.get("description") and normalized.get("requirement"):
            normalized["description"] = str(normalized["requirement"])

        if not normalized.get("title") and normalized.get("control_id"):
            normalized["title"] = str(normalized["control_id"])

        if not normalized.get("source_url"):
            normalized["source_url"] = ""

        if normalized.get("testing_procedures") and isinstance(normalized["testing_procedures"], str):
            normalized["testing_procedures"] = [normalized["testing_procedures"]]

        return normalized

    def deduplicate(
        self, data: list[dict[str, Any]], key_func: Callable[[dict], tuple] | None = None
    ) -> list[dict[str, Any]]:
        """Deduplicate data using custom key function.

        For compliance controls, merges controls with the same control_id
        from different sources by combining source URLs.

        Args:
            data: List of data dictionaries
            key_func: Function to generate deduplication key (if None, uses get_deduplication_key())

        Returns:
            Deduplicated list of data dictionaries
        """
        if key_func is None:
            key_func = self.get_deduplication_key

        seen: dict[tuple, dict[str, Any]] = {}
        source_urls_map: dict[tuple, list[str]] = {}

        for item in data:
            try:
                key = key_func(item)
                source_url = item.get("source_url", "")

                if key not in seen:
                    seen[key] = item.copy()
                    source_urls_map[key] = [source_url] if source_url else []
                else:
                    existing = seen[key]
                    if source_url and source_url not in source_urls_map[key]:
                        source_urls_map[key].append(source_url)
                        if len(source_urls_map[key]) > 1:
                            existing["source_url"] = source_urls_map[key]

            except (AttributeError, KeyError, TypeError) as e:
                logger.warning("Error generating deduplication key: %s", e)
                unknown_key = ("unknown",)
                if unknown_key not in seen:
                    seen[unknown_key] = item
                    source_urls_map[unknown_key] = [item.get("source_url", "")]
                else:
                    existing_url = item.get("source_url", "")
                    if existing_url and existing_url not in source_urls_map[unknown_key]:
                        source_urls_map[unknown_key].append(existing_url)

        unique = list(seen.values())

        for item in unique:
            key = key_func(item)
            if key in source_urls_map and len(source_urls_map[key]) > 1:
                item["source_url"] = source_urls_map[key]
            elif key in source_urls_map and len(source_urls_map[key]) == 1 and source_urls_map[key][0]:
                item["source_url"] = source_urls_map[key][0]

        duplicates = len(data) - len(unique)
        if duplicates > 0:
            logger.info("Removed %d duplicate items (merged by control_id)", duplicates)

        return unique

    def save_raw_data(self, data: list[dict[str, Any]]) -> None:
        """Save raw collected data to JSON file.

        Removes empty/null fields before saving to reduce file size.

        Args:
            data: List of raw data dictionaries
        """
        if not data:
            logger.warning("No data to save for %s", self.collector_name)
            return

        cleaned_data = []
        for item in data:
            cleaned = self._remove_empty_fields(item)
            if cleaned:
                cleaned_data.append(cleaned)

        if not cleaned_data:
            logger.error("All items were removed during cleaning for %s", self.collector_name)
            return

        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(self.output_file, "w", encoding="utf-8") as f:
                json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
            
            if not self.output_file.exists() or self.output_file.stat().st_size == 0:
                logger.error("Failed to write data to %s - file is empty", self.output_file)
            else:
                logger.info(
                    "Saved %d %s items to %s (file size: %d bytes)",
                    len(cleaned_data),
                    self.collector_name,
                    self.output_file,
                    self.output_file.stat().st_size,
                )
        except (IOError, OSError) as e:
            logger.error("Failed to save data to %s: %s", self.output_file, e, exc_info=True)

    def _remove_empty_fields(self, item: dict[str, Any]) -> dict[str, Any]:
        """Remove empty/null fields from item.

        Args:
            item: Data dictionary

        Returns:
            Cleaned dictionary without empty fields
        """
        cleaned = {}
        for key, value in item.items():
            if value is None:
                continue
            if isinstance(value, str) and not value.strip():
                continue
            if isinstance(value, list) and len(value) == 0:
                continue
            if isinstance(value, dict) and len(value) == 0:
                continue
            cleaned[key] = value
        
        if not cleaned:
            logger.warning("Item became empty after cleaning: %s", item.get("control_id", "unknown"))
        
        return cleaned

    def load_raw_data(self) -> list[dict[str, Any]]:
        """Load existing raw data if available.

        Returns:
            List of raw data dictionaries
        """
        if not self.output_file.exists():
            return []

        with open(self.output_file, "r", encoding="utf-8") as f:
            return json.load(f)

    @abstractmethod
    def get_source_urls(self) -> list[str]:
        """Get list of source URLs to collect.

        Returns:
            List of URLs to collect data from
        """
        raise NotImplementedError

    @abstractmethod
    def parse_data(
        self,
        response: str | BeautifulSoup | dict[str, Any] | list[dict[str, Any]],
        url: str,
    ) -> list[dict[str, Any]]:
        """Parse data from response.

        Args:
            response: Parsed response:
                - str: Markdown content (if use_markdown=True)
                - BeautifulSoup: Parsed HTML (if use_markdown=False)
                - dict/list: JSON data
            url: Source URL

        Returns:
            List of parsed data dictionaries
        """
        raise NotImplementedError

    def get_validation_model(self) -> type[Any] | None:
        """Get Pydantic model for data validation.

        Returns:
            Pydantic model class or None if no validation
        """
        return None

    def get_deduplication_key(self, item: dict[str, Any]) -> tuple[str, ...]:
        """Get deduplication key for an item.

        Args:
            item: Data dictionary

        Returns:
            Tuple to use as deduplication key
        """
        return (str(item.get("source_url", "")),)

    def calculate_field_completeness(self, items: list[dict[str, Any]]) -> dict[str, float]:
        """Calculate completeness score for each field.

        Args:
            items: List of data dictionaries

        Returns:
            Dictionary mapping field names to completeness scores (0.0-1.0)
        """
        if not items:
            return {}

        field_counts: dict[str, dict[str, int]] = {}

        for item in items:
            for field, value in item.items():
                if field not in field_counts:
                    field_counts[field] = {"total": 0, "present": 0}
                field_counts[field]["total"] += 1
                if value not in (None, "", [], {}):
                    field_counts[field]["present"] += 1

        return {
            field: counts["present"] / counts["total"]
            for field, counts in field_counts.items()
        }

    async def _process_url(self, url: str, result: CollectionResult) -> list[dict[str, Any]]:
        """Process a single URL and return extracted items.

        Handles PDF URLs separately using Docling, other URLs with Crawl4AI.

        Args:
            url: URL to process
            result: CollectionResult to track errors

        Returns:
            List of extracted items
        """
        try:
            if url.endswith(".pdf"):
                return await self._process_pdf_url(url, result)
            elif url.endswith(".json"):
                response = await self.fetch_json_async(url)
                items = self.parse_data(response, url)
                result.metrics.successful_urls += 1
                logger.debug("Extracted %d items from %s", len(items), url)
                return items
            else:
                crawl_result = await self.fetch_page_async(url)
                
                all_items: list[dict[str, Any]] = []
                
                if self.enable_deep_crawl and hasattr(crawl_result, "crawled_pages") and crawl_result.crawled_pages:
                    discovered_count = len(crawl_result.crawled_pages)
                    logger.info(
                        "Deep crawl discovered %d pages from seed URL %s (max_urls limit applies to seed URLs only, "
                        "deep crawling may discover additional pages)",
                        discovered_count,
                        url
                    )
                    from ..processors.llm_extractor import LLMControlExtractor

                    extractor = LLMControlExtractor()
                    standard = getattr(self, "standard_name", None) or self.collector_name

                    async def process_page(page_result: Any) -> list[dict[str, Any]]:
                        """Process a single crawled page."""
                        page_url = getattr(page_result, "url", url)
                        page_markdown = getattr(page_result, "markdown", "") or ""
                        page_html = getattr(page_result, "html", "") or ""

                        if page_markdown or page_html:
                            try:
                                page_controls = await extractor.extract_controls(
                                    content=page_html if not page_markdown else page_markdown,
                                    standard=standard,
                                    source_url=page_url,
                                    prefer_markdown=True,
                                    markdown_content=page_markdown if page_markdown else None,
                                )
                                if page_controls:
                                    logger.debug("Extracted %d controls from crawled page: %s", len(page_controls), page_url)
                                    return page_controls
                            except Exception as e:
                                logger.warning("Failed to extract controls from crawled page %s: %s", page_url, e)
                        return []
                    
                    tasks = [process_page(page_result) for page_result in crawl_result.crawled_pages]
                    page_results = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    for page_controls in page_results:
                        if isinstance(page_controls, Exception):
                            logger.warning("Error processing crawled page: %s", page_controls)
                            continue
                        elif isinstance(page_controls, list):
                            all_items.extend(page_controls)
                else:
                    markdown_content = crawl_result.markdown or ""
                    html_content = crawl_result.html or ""

                    if markdown_content or html_content:
                        from ..processors.llm_extractor import LLMControlExtractor

                        extractor = LLMControlExtractor()
                        standard = getattr(self, "standard_name", None) or self.collector_name

                        controls = await extractor.extract_controls(
                            content=html_content if not markdown_content else markdown_content,
                            standard=standard,
                            source_url=url,
                            prefer_markdown=True,
                            markdown_content=markdown_content if markdown_content else None,
                        )

                        if controls:
                            all_items = controls
                        else:
                            logger.warning("No controls extracted from %s using LLM", url)
                    else:
                        logger.warning("No content extracted from %s", url)

                if all_items:
                    result.metrics.successful_urls += 1
                    logger.info("Extracted %d total controls from %s (deep crawl: %s)", len(all_items), url, self.enable_deep_crawl)
                else:
                    result.metrics.failed_urls += 1
                    logger.warning("No controls extracted from %s", url)

                return all_items

        except RuntimeError as e:
            error_msg = str(e)
            if "playwright" in error_msg.lower() or "browser" in error_msg.lower():
                error_type = "PlaywrightError"
                result.add_error(url, error_type, error_msg)
                result.metrics.failed_urls += 1
                result.metrics.network_errors += 1
                logger.error("Playwright error collecting from %s: %s", url, error_msg)
                return []
            raise
        except (ConnectionError, TimeoutError) as e:
            error_type = type(e).__name__
            error_msg = str(e)
            result.add_error(url, error_type, error_msg)
            result.metrics.failed_urls += 1
            result.metrics.network_errors += 1
            logger.error("Network error collecting from %s: %s", url, error_msg)
            return []
        except (ValueError, KeyError, AttributeError, json.JSONDecodeError) as e:
            error_type = type(e).__name__
            error_msg = str(e)
            result.add_error(url, error_type, error_msg)
            result.metrics.failed_urls += 1
            result.metrics.parsing_errors += 1
            logger.error("Parsing error collecting from %s: %s", url, error_msg)
            return []

    async def _process_pdf_url(self, url: str, result: CollectionResult) -> list[dict[str, Any]]:
        """Process a PDF URL using Docling + LLM.

        Args:
            url: PDF URL
            result: CollectionResult to track errors

        Returns:
            List of extracted items
        """
        try:
            from ..processors.document_processor import DocumentProcessor

            document_processor = DocumentProcessor()
            standard = getattr(self, "standard_name", None) or self.collector_name

            controls = await document_processor.extract_compliance_controls_from_pdf_url_async(url, standard)

            if controls:
                result.metrics.successful_urls += 1
                logger.info("Extracted %d controls from PDF URL using Docling + LLM: %s", len(controls), url)
                return controls
            else:
                result.metrics.failed_urls += 1
                logger.warning("No controls extracted from PDF URL: %s", url)
                return []

        except ImportError:
            logger.error("DocumentProcessor not available. Cannot process PDF URL: %s", url)
            result.add_error(url, "ImportError", "DocumentProcessor not available")
            result.metrics.failed_urls += 1
            return []
        except (RuntimeError, OSError, ValueError, TypeError, KeyError) as e:
            error_type = type(e).__name__
            error_msg = str(e)
            result.add_error(url, error_type, error_msg)
            result.metrics.failed_urls += 1
            logger.error("Error processing PDF URL %s: %s", url, error_msg, exc_info=True)
            return []

    async def _process_urls_batch(
        self, 
        urls: list[str], 
        result: CollectionResult,
        max_urls: int | None = None,
        urls_processed: list[str] | None = None,
        max_controls: int | None = None,
        current_item_count: int = 0,
    ) -> list[dict[str, Any]]:
        """Process a batch of URLs in parallel.

        Args:
            urls: List of URLs to process
            result: CollectionResult to track errors
            max_urls: Maximum total URLs to process (for deep crawl tracking)
            urls_processed: List to track processed URLs
            max_controls: Maximum controls to collect
            current_item_count: Current number of items collected

        Returns:
            List of all extracted items
        """
        if max_controls is not None and current_item_count >= max_controls:
            return []
        
        tasks = [self._process_url(url, result) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_items: list[dict[str, Any]] = []
        for i, items in enumerate(results):
            if isinstance(items, Exception):
                logger.error("Task exception: %s", items, exc_info=True)
            elif isinstance(items, list):
                all_items.extend(items)
                if urls_processed is not None and i < len(urls):
                    urls_processed.append(urls[i])

        return all_items

    async def collect_async(
        self,
        max_urls: int | None = None,
        max_pdfs: int | None = None,
        max_controls: int | None = None,
        progress_callback: Callable[[int, int], None] | Callable[[int, int], Awaitable[None]] | None = None,
    ) -> CollectionResult:
        """Collect all data for this collector with parallel processing.

        Uses Crawl4AI for all web scraping with concurrent URL processing.

        Args:
            max_urls: Maximum number of URLs to process (None for all)
            max_pdfs: Maximum number of PDFs to process (None for all)
            max_controls: Maximum number of controls to collect (None for all)
            progress_callback: Optional callback(item_count, total_urls) for progress updates

        Returns:
            CollectionResult with items, errors, and metrics
        """
        result = CollectionResult(
            collector_name=self.collector_name,
            version=self.version,
            success=False,
            metrics=CollectionMetrics(),
        )

        logger.info("Starting collection for %s %s", self.collector_name, self.version)

        urls = self.get_source_urls()
        
        pdf_urls = [url for url in urls if url.endswith(".pdf")]
        web_urls = [url for url in urls if not url.endswith(".pdf")]
        
        if max_pdfs is not None and len(pdf_urls) > max_pdfs:
            logger.info("Limiting PDFs to %d (from %d)", max_pdfs, len(pdf_urls))
            pdf_urls = pdf_urls[:max_pdfs]
        
        if max_urls is not None and len(web_urls) > max_urls:
            logger.info(
                "Limiting seed URLs to %d (from %d). Note: Deep crawling may discover additional pages from these seed URLs. "
                "To disable deep crawling, set disable_deep_crawl_when_limited=True",
                max_urls,
                len(web_urls)
            )
            web_urls = web_urls[:max_urls]
        
        urls = web_urls + pdf_urls
        result.metrics.total_urls = len(urls)

        if not urls:
            logger.warning("No URLs to collect for %s", self.collector_name)
            result.items = []
            result.finalize()
            return result

        all_items: list[dict[str, Any]] = []
        urls_processed: list[str] = []

        batches = [
            urls[i : i + self.max_concurrent]
            for i in range(0, len(urls), self.max_concurrent)
        ]

        max_concurrent_batches = 3
        semaphore = asyncio.Semaphore(max_concurrent_batches)
        
        async def process_batch_with_limit(batch: list[str], current_count: int) -> list[dict[str, Any]]:
            """Process a batch with concurrency limit."""
            async with semaphore:
                if max_controls is not None and current_count >= max_controls:
                    return []
                
                batch_items = await self._process_urls_batch(
                    batch, 
                    result, 
                    max_urls=max_urls,
                    urls_processed=urls_processed,
                    max_controls=max_controls,
                    current_item_count=current_count,
                )
                return batch_items
        
        batch_tasks = [process_batch_with_limit(batch, len(all_items)) for batch in batches]
        
        with tqdm(total=len(batches), desc=f"Collecting {self.collector_name}") as pbar:
            for coro in asyncio.as_completed(batch_tasks):
                try:
                    batch_items = await coro
                    if batch_items:
                        all_items.extend(batch_items)
                        
                        if progress_callback:
                            try:
                                callback_result = progress_callback(len(all_items), result.metrics.total_urls)
                                if isinstance(callback_result, Awaitable):
                                    await callback_result
                            except Exception as e:
                                logger.warning("Progress callback failed: %s", e)
                        
                        if max_controls is not None and len(all_items) >= max_controls:
                            all_items = all_items[:max_controls]
                            logger.info("Limited items to %d controls", max_controls)
                            break
                    
                    pbar.update(1)
                except Exception as e:
                    logger.error("Error processing batch: %s", e, exc_info=True)
                    pbar.update(1)

        result.metrics.total_items_collected = len(all_items)
        logger.info("Collected %d raw items before deduplication and validation", len(all_items))

        if all_items:
            deduplicated_items = self.deduplicate(all_items)
            logger.info("After deduplication: %d items", len(deduplicated_items))
            validated_items = self.validate_data(deduplicated_items, result=result)
            logger.info("After validation: %d items", len(validated_items))
            result.items = validated_items
            result.metrics.field_completeness = self.calculate_field_completeness(
                validated_items
            )
        else:
            result.items = []
            logger.warning("No items collected from URLs")

        result.finalize()
        self.save_raw_data(result.items)

        logger.info(
            "Collected %d total items for %s (success rate: %.1f%%)",
            len(result.items),
            self.collector_name,
            result.metrics.get_success_rate() * 100,
        )

        if self._crawler:
            await self._crawler.close()
            self._crawler = None

        return result

    def collect(self) -> CollectionResult:
        """Collect all data for this collector (sync wrapper).

        Returns:
            CollectionResult with items, errors, and metrics
        """
        return asyncio.run(self.collect_async())

