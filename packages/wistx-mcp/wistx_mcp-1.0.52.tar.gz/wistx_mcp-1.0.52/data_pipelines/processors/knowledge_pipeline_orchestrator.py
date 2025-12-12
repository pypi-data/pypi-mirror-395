"""Knowledge pipeline orchestrator - coordinates knowledge article pipeline.

Coordinates Collection → Processing → Quality Validation → Embedding → Loading stages
for knowledge articles across all domains.
"""

from typing import Any, AsyncIterator

import asyncio

from ..collectors.discovery_helper import get_discovered_urls
from ..loaders.mongodb_loader import MongoDBLoader
from ..processors.base_knowledge_processor import BaseKnowledgeProcessor
from ..processors.quality_validator import ContentQualityValidator
from ..processors.llm_knowledge_extractor import LLMKnowledgeExtractor
from ..processors.embedding_generator import EmbeddingGenerator
from ..utils.change_detector import ChangeDetector
from ..utils.tracing import TracingContext, get_correlation_id
from ..utils.logger import setup_logger
from ..utils.config import PipelineSettings
from ..utils.pipeline_progress import PipelineProgress
from ..utils.domain_circuit_breaker import DomainCircuitBreakerManager
from ..utils.domain_rate_limiter import DomainRateLimiter
from ..utils.dead_letter_queue import DeadLetterQueue
from .monitoring import PipelineMetrics

logger = setup_logger(__name__)


class KnowledgePipelineOrchestrator:
    """Orchestrates the knowledge article processing pipeline.
    
    Coordinates Collection → Processing → Quality Validation → Embedding → Loading stages.
    """

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize knowledge pipeline orchestrator.
        
        Args:
            config: Optional configuration dictionary
                - enable_change_detection: Enable change detection (default: True)
        """
        self.config = config or {}
        self.settings = PipelineSettings()
        self.processor: BaseKnowledgeProcessor | None = None
        self.embedder = EmbeddingGenerator(save_intermediate=False)
        self.loader = MongoDBLoader()
        self.quality_validator = ContentQualityValidator()
        self.metrics = PipelineMetrics(enable_prometheus=True)
        self.knowledge_extractor = LLMKnowledgeExtractor()
        self.change_detector: ChangeDetector | None = None
        self.enable_change_detection = self.config.get("enable_change_detection", True)
        self.url_fetch_timeout = self.config.get("url_fetch_timeout", self.settings.url_fetch_timeout_seconds)
        self.url_fetch_max_retries = self.config.get("url_fetch_max_retries", self.settings.url_fetch_max_retries)
        self.llm_api_timeout = self.config.get("llm_api_timeout", self.settings.llm_api_timeout_seconds)
        self.pdf_processing_timeout = self.config.get("pdf_processing_timeout", self.settings.pdf_processing_timeout_seconds)
        self.use_paginated_collection = self.config.get("use_paginated_collection", self.settings.use_paginated_collection)
        self.collection_batch_size = self.config.get("collection_batch_size", self.settings.collection_batch_size)
        self.use_streaming_pipeline = self.config.get("use_streaming_pipeline", self.settings.use_streaming_pipeline)
        self.enable_checkpointing = self.config.get("enable_checkpointing", self.settings.enable_checkpointing)
        self.checkpoint_interval = self.config.get("checkpoint_interval", self.settings.checkpoint_interval)
        self.pipeline_progress: "PipelineProgress | None" = None
        self.domain_circuit_breaker = DomainCircuitBreakerManager(
            failure_threshold=self.config.get("domain_circuit_breaker_failure_threshold", 3),
            recovery_timeout=self.config.get("domain_circuit_breaker_recovery_timeout", 3600.0),
        )
        self.domain_rate_limiter = DomainRateLimiter(
            max_calls_per_domain=self.config.get("domain_rate_limit_max_calls", 10),
            period_seconds=self.config.get("domain_rate_limit_period_seconds", 60.0),
        )
        self.dead_letter_queue = DeadLetterQueue(
            collection_name=self.config.get("dead_letter_queue_collection", "failed_urls")
        )

    async def run_knowledge_pipeline(
        self,
        domain: str,
        subdomain: str | None = None,
        processor: BaseKnowledgeProcessor | None = None,
        run_collection: bool = True,
        max_urls: int | None = None,
        max_pdfs: int | None = None,
        max_docs: int | None = None,
        max_articles: int | None = None,
        max_concurrent: int | None = None,
        disable_deep_crawl_when_limited: bool = False,
        pipeline_id: str | None = None,
        resume_from_checkpoint: bool = False,
    ) -> dict[str, Any]:
        """Run complete knowledge pipeline for a domain.
        
        Args:
            domain: Knowledge domain (compliance, finops, architecture, etc.)
            subdomain: Optional subdomain (e.g., "pci-dss", "cost-optimization")
            processor: Domain-specific processor (if None, uses default)
            run_collection: If True, run collection stage first
            max_urls: Maximum number of web URLs to process (None for all)
            max_pdfs: Maximum number of PDF URLs to process (None for all)
            max_docs: Maximum number of documents to process (None for all)
            max_articles: Maximum number of articles to extract (None for all)
            max_concurrent: Maximum concurrent URL fetches (None uses config default)
            disable_deep_crawl_when_limited: If True, disable deep crawling (sitemap recursion) when max_urls is set
            pipeline_id: Unique pipeline identifier for checkpointing (auto-generated if None)
            resume_from_checkpoint: If True, attempt to resume from latest checkpoint
            
        Returns:
            Dictionary with pipeline results and statistics
        """
        logger.info("=" * 80)
        logger.info("Starting knowledge pipeline for domain: %s", domain)
        if subdomain:
            logger.info("Subdomain: %s", subdomain)
        logger.info("=" * 80)

        correlation_id = get_correlation_id()
        
        if pipeline_id is None:
            import uuid
            pipeline_id = f"{domain}-{subdomain or 'all'}-{uuid.uuid4().hex[:8]}"
        
        if self.enable_checkpointing:
            self.pipeline_progress = PipelineProgress(pipeline_id)
            logger.info("Pipeline ID: %s (checkpointing enabled)", pipeline_id)
            
            if resume_from_checkpoint:
                latest_checkpoint = await self.pipeline_progress.get_latest_checkpoint()
                if latest_checkpoint:
                    logger.info(
                        "Resuming from checkpoint: stage=%s, timestamp=%s",
                        latest_checkpoint.get("stage"),
                        latest_checkpoint.get("timestamp")
                    )
                    stats.update(latest_checkpoint.get("stats", {}))
                else:
                    logger.info("No checkpoint found, starting fresh")

        with TracingContext(
            "knowledge_pipeline", domain=domain, subdomain=subdomain, correlation_id=correlation_id
        ):
            stats = {
                "domain": domain,
                "subdomain": subdomain,
                "pipeline_id": pipeline_id,
                "collected": 0,
                "processed": 0,
                "validated": 0,
                "embedded": 0,
                "loaded_mongodb": 0,
                "loaded_pinecone": 0,
                "quality_rejected": 0,
                "skipped_source_unchanged": 0,
                "skipped_content_unchanged": 0,
                "llm_calls_saved": 0,
                "embedding_calls_saved": 0,
                "errors": [],
            }
            
            if resume_from_checkpoint and self.enable_checkpointing and self.pipeline_progress:
                latest_checkpoint = await self.pipeline_progress.get_latest_checkpoint()
                if latest_checkpoint:
                    checkpoint_stats = latest_checkpoint.get("stats", {})
                    for key in ["collected", "processed", "validated", "embedded", "loaded_mongodb", "loaded_pinecone", "quality_rejected", "skipped_source_unchanged", "skipped_content_unchanged", "llm_calls_saved", "embedding_calls_saved"]:
                        if key in checkpoint_stats:
                            stats[key] = checkpoint_stats[key]
                    logger.info("Resumed stats from checkpoint: collected=%d, processed=%d, loaded=%d", 
                               stats["collected"], stats["processed"], stats["loaded_mongodb"])

            raw_articles = []

            try:
                if run_collection and self.use_paginated_collection and self.use_streaming_pipeline:
                    return await self._run_streaming_pipeline_from_collection(
                        domain, subdomain, processor, stats, max_urls, max_pdfs, max_docs,
                        max_articles, max_concurrent, disable_deep_crawl_when_limited
                    )

                if run_collection:
                    collection_metrics = self.metrics.start_stage("collection", "knowledge")
                    try:
                        disable_deep_crawl = (
                            disable_deep_crawl_when_limited 
                            and max_urls is not None
                        )
                        
                        if disable_deep_crawl:
                            logger.info(
                                "Deep crawling disabled because max_urls is set (%d) and disable_deep_crawl_when_limited=True",
                                max_urls
                            )
                        
                        discovered = await get_discovered_urls(
                            domain, 
                            subdomain, 
                            disable_deep_crawl=disable_deep_crawl
                        )

                        web_urls = discovered.get("web_urls", [])
                        pdf_urls = discovered.get("pdf_urls", [])

                        logger.info(
                            "Discovered %d web URLs and %d PDF URLs",
                            len(web_urls),
                            len(pdf_urls),
                        )

                        if max_urls is not None and len(web_urls) > max_urls:
                            logger.info(
                                "Limiting web URLs to %d (from %d)",
                                max_urls,
                                len(web_urls),
                            )
                            web_urls = web_urls[:max_urls]

                        if max_pdfs is not None and len(pdf_urls) > max_pdfs:
                            logger.info(
                                "Limiting PDF URLs to %d (from %d)",
                                max_pdfs,
                                len(pdf_urls),
                            )
                            pdf_urls = pdf_urls[:max_pdfs]

                        if max_docs is not None:
                            total_docs = len(web_urls) + len(pdf_urls)
                            if total_docs > max_docs:
                                logger.info(
                                    "Limiting total documents to %d (from %d web + %d PDF)",
                                    max_docs,
                                    len(web_urls),
                                    len(pdf_urls),
                                )
                                remaining = max_docs
                                if len(web_urls) > 0:
                                    web_urls = web_urls[:min(len(web_urls), remaining)]
                                    remaining -= len(web_urls)
                                if remaining > 0 and len(pdf_urls) > 0:
                                    pdf_urls = pdf_urls[:min(len(pdf_urls), remaining)]

                        raw_articles = await self._collect_from_urls(
                            web_urls, pdf_urls, domain, subdomain or "", 
                            max_concurrent=max_concurrent,
                            max_articles=max_articles
                        )

                        stats["collected"] = len(raw_articles)

                        for article in raw_articles:
                            self.metrics.record_item_processed("collection", "knowledge", success=True)

                        collection_metrics.items_processed = len(raw_articles)
                        collection_metrics.items_succeeded = len(raw_articles)
                        self.metrics.finish_stage("collection", "knowledge")

                        logger.info(
                            "Collected %d raw articles for domain: %s",
                            len(raw_articles),
                            domain,
                        )
                    except (ValueError, KeyError, AttributeError, RuntimeError) as e:
                        logger.error("Collection failed for domain %s: %s", domain, e)
                        stats["errors"].append({"stage": "collection", "error": str(e)})
                        self.metrics.record_error("collection", type(e).__name__, str(e))
                        self.metrics.finish_stage("collection", "knowledge")

                if not raw_articles:
                    logger.warning("No raw articles collected for domain: %s", domain)
                    return stats

                if self.enable_change_detection and raw_articles:
                    if self.change_detector is None:
                        from api.database.mongodb import mongodb_manager
                        mongodb_manager.connect()
                        db = mongodb_manager.get_database()
                        self.change_detector = ChangeDetector(
                            db.knowledge_articles,
                            enabled=self.enable_change_detection
                        )
                    
                    self.change_detector.batch_check_article_source_hashes(raw_articles)
                    filtered_raw_articles = []
                    
                    for raw_article in raw_articles:
                        article_id = raw_article.get("article_id")
                        should_process, source_hash = self.change_detector.should_process_article_source(
                            raw_article, article_id
                        )
                        
                        if not should_process:
                            stats["skipped_source_unchanged"] += 1
                            stats["llm_calls_saved"] += 1
                            stats["embedding_calls_saved"] += 1
                            logger.debug("Skipping unchanged article: %s", article_id)
                            continue
                        
                        raw_article["_source_hash"] = source_hash
                        filtered_raw_articles.append(raw_article)
                    
                    raw_articles = filtered_raw_articles
                    logger.info(
                        "Change detection: %d articles unchanged, %d articles to process",
                        stats["skipped_source_unchanged"],
                        len(raw_articles),
                    )

                if processor is None:
                    if domain == "compliance":
                        from .compliance_knowledge_processor import ComplianceKnowledgeProcessor

                        processor = ComplianceKnowledgeProcessor()
                    elif domain == "finops":
                        from .finops_knowledge_processor import FinOpsKnowledgeProcessor

                        processor = FinOpsKnowledgeProcessor()
                    elif domain == "devops":
                        from .devops_knowledge_processor import DevOpsKnowledgeProcessor

                        processor = DevOpsKnowledgeProcessor()
                    elif domain == "security":
                        from .security_knowledge_processor import SecurityKnowledgeProcessor

                        processor = SecurityKnowledgeProcessor()
                    elif domain == "infrastructure":
                        from .infrastructure_knowledge_processor import InfrastructureKnowledgeProcessor

                        processor = InfrastructureKnowledgeProcessor()
                    elif domain == "architecture":
                        from .architecture_knowledge_processor import ArchitectureKnowledgeProcessor

                        processor = ArchitectureKnowledgeProcessor()
                    elif domain == "cloud":
                        from .cloud_knowledge_processor import CloudKnowledgeProcessor

                        processor = CloudKnowledgeProcessor()
                    elif domain == "automation":
                        from .automation_knowledge_processor import AutomationKnowledgeProcessor

                        processor = AutomationKnowledgeProcessor()
                    elif domain == "platform":
                        from .platform_knowledge_processor import PlatformKnowledgeProcessor

                        processor = PlatformKnowledgeProcessor()
                    elif domain == "sre":
                        from .sre_knowledge_processor import SREKnowledgeProcessor

                        processor = SREKnowledgeProcessor()
                    else:
                        logger.error("No processor available for domain: %s", domain)
                        stats["errors"].append({"stage": "processing", "error": "No processor available"})
                        return stats

                self.processor = processor

                if self.use_streaming_pipeline and not run_collection:
                    return await self._run_streaming_pipeline(
                        raw_articles, domain, subdomain, processor, stats
                    )

                processing_metrics = self.metrics.start_stage("processing", "knowledge")

                processed_articles = []
                failed_processing = []

                for raw in raw_articles:
                    try:
                        article = processor.process_raw_data(raw)

                        if not processor.validate_article(article):
                            logger.warning(
                                "Validation failed for article: %s",
                                raw.get("title", "unknown"),
                            )
                            failed_processing.append({"raw": raw, "error": "Validation failed"})
                            continue

                        quality_score = self.quality_validator.validate(article)
                        article.quality_score = quality_score.overall_score
                        article.source_credibility = quality_score.source_credibility
                        article.freshness_score = quality_score.freshness

                        quality_threshold = self._get_quality_threshold(article.domain)
                        if quality_score.overall_score < quality_threshold:
                            logger.warning(
                                "Article %s rejected: quality score %.2f < %.1f (threshold for %s) "
                                "(source: %.1f, completeness: %.1f, accuracy: %.1f, actionability: %.1f, freshness: %.1f)",
                                article.article_id,
                                quality_score.overall_score,
                                quality_threshold,
                                article.domain,
                                quality_score.source_credibility,
                                quality_score.completeness,
                                quality_score.accuracy,
                                quality_score.actionability,
                                quality_score.freshness,
                            )
                            stats["quality_rejected"] += 1
                            continue

                        processed_articles.append(article)
                        stats["validated"] += 1

                    except ValueError as e:
                        error_msg = str(e)
                        if "Article filtered out" in error_msg:
                            logger.debug("Article filtered out during processing: %s", error_msg)
                        else:
                            logger.error("Error processing article: %s", e, exc_info=True)
                        failed_processing.append({"raw": raw, "error": str(e)})
                        continue
                    except (TypeError, KeyError, AttributeError, RuntimeError) as e:
                        logger.error("Error processing article: %s", e, exc_info=True)
                        failed_processing.append({"raw": raw, "error": str(e)})
                        continue

                stats["processed"] = len(processed_articles)
                stats["errors"].extend(failed_processing)

                if failed_processing:
                    logger.warning(
                        "Failed to process %d articles out of %d collected",
                        len(failed_processing),
                        len(raw_articles)
                    )
                    for failed in failed_processing[:5]:
                        error_msg = failed.get("error", "Unknown error")
                        raw_title = failed.get("raw", {}).get("title", "Unknown")[:50]
                        logger.warning(
                            "Processing failure: title='%s', error='%s'",
                            raw_title,
                            error_msg
                        )
                    if len(failed_processing) > 5:
                        logger.warning(
                            "... and %d more processing failures (see errors in stats)",
                            len(failed_processing) - 5
                        )

                for article in processed_articles:
                    self.metrics.record_item_processed("processing", "knowledge", success=True)

                for failed in failed_processing:
                    self.metrics.record_item_processed("processing", "knowledge", success=False)
                    self.metrics.record_error(
                        "processing", failed.get("error", "Unknown"), str(failed)
                    )

                processing_metrics.items_processed = len(processed_articles) + len(failed_processing)
                processing_metrics.items_succeeded = len(processed_articles)
                processing_metrics.items_failed = len(failed_processing)
                self.metrics.finish_stage("processing", "knowledge")

                if not processed_articles:
                    logger.warning("No articles processed for domain: %s", domain)
                    return stats

                embedding_metrics = self.metrics.start_stage("embedding", "knowledge")
                articles_dict = [article.model_dump(mode="json") for article in processed_articles]

                items_to_embed = []
                items_skipped_embedding = []
                
                if self.enable_change_detection and self.change_detector:
                    for article_dict in articles_dict:
                        article_id = article_dict.get("article_id")
                        if not article_id:
                            items_to_embed.append(article_dict)
                            continue
                        
                        try:
                            if self.change_detector.collection is not None:
                                existing_doc = self.change_detector.collection.find_one(
                                    {"article_id": article_id},
                                    {"content_hash": 1}
                                )
                            else:
                                existing_doc = None
                            
                            should_generate, content_hash = self.change_detector.should_generate_article_embedding(
                                article_dict, article_id, existing_doc
                            )
                            
                            if not should_generate:
                                stats["skipped_content_unchanged"] += 1
                                stats["embedding_calls_saved"] += 1
                                logger.debug("Skipping embedding for unchanged article: %s", article_id)
                                items_skipped_embedding.append(article_dict)
                                continue
                            
                            article_dict["_content_hash"] = content_hash
                            items_to_embed.append(article_dict)
                        except (ValueError, TypeError, KeyError, AttributeError, RuntimeError) as e:
                            logger.warning("Error checking content hash for article %s: %s - generating embedding anyway", article_id, e)
                            items_to_embed.append(article_dict)
                else:
                    items_to_embed = articles_dict

                items_with_embeddings, failed_embedding = await self.embedder.generate_embeddings(
                    items_to_embed, "knowledge"
                )
                
                if items_skipped_embedding:
                    items_with_embeddings.extend(items_skipped_embedding)

                stats["embedded"] = len([a for a in items_with_embeddings if a.get("embedding")])
                stats["errors"].extend(failed_embedding)

                for _ in items_with_embeddings:
                    self.metrics.record_item_processed("embedding", "knowledge", success=True)

                for failed in failed_embedding:
                    self.metrics.record_item_processed("embedding", "knowledge", success=False)
                    self.metrics.record_error(
                        "embedding", failed.get("error", "Unknown"), str(failed)
                    )

                embedding_metrics.items_processed = len(items_with_embeddings) + len(failed_embedding)
                embedding_metrics.items_succeeded = len(items_with_embeddings)
                embedding_metrics.items_failed = len(failed_embedding)
                self.metrics.finish_stage("embedding", "knowledge")

                loading_metrics = self.metrics.start_stage("loading", "knowledge")

                if items_with_embeddings:
                    load_stats = self.loader.load_knowledge_articles(items_with_embeddings)
                else:
                    logger.warning(
                        "No articles with embeddings for domain: %s. "
                        "Loading articles to MongoDB without embeddings.",
                        domain,
                    )
                    articles_dict_no_embedding = [
                        article.model_dump(mode="json") for article in processed_articles
                    ]
                    for article in articles_dict_no_embedding:
                        article.pop("embedding", None)
                    load_stats = self.loader.load_knowledge_articles(articles_dict_no_embedding)

                stats["loaded_mongodb"] = load_stats["mongodb_inserted"] + load_stats["mongodb_updated"]
                stats["loaded_pinecone"] = load_stats["pinecone_loaded"]

                self.metrics.record_item_processed("loading", "knowledge", success=True)
                loading_metrics.items_processed = stats["loaded_mongodb"]
                loading_metrics.items_succeeded = stats["loaded_mongodb"]
                loading_metrics.items_failed = load_stats.get("mongodb_errors", 0)
                self.metrics.finish_stage("loading", "knowledge")

                summary = self.metrics.get_summary()
                stats["metrics_summary"] = summary

                logger.info("=" * 80)
                logger.info("Knowledge pipeline completed for domain: %s", domain)
                logger.info(
                    "Collected: %d, Processed: %d, Validated: %d, Embedded: %d, Loaded: %d",
                    stats["collected"],
                    stats["processed"],
                    stats["validated"],
                    stats["embedded"],
                    stats["loaded_mongodb"],
                )
                if self.enable_change_detection:
                    logger.info(
                        "Change Detection: Skipped %d (source unchanged), %d (content unchanged)",
                        stats["skipped_source_unchanged"],
                        stats["skipped_content_unchanged"],
                    )
                    logger.info(
                        "Cost Savings: %d LLM calls saved, %d embedding calls saved",
                        stats["llm_calls_saved"],
                        stats["embedding_calls_saved"],
                    )
                logger.info("Quality Rejected: %d", stats["quality_rejected"])
                logger.info("Total Duration: %.2fs", summary["total_duration_seconds"])
                logger.info("=" * 80)

                return stats

            except (ValueError, TypeError, KeyError, RuntimeError) as e:
                logger.error("Pipeline failed for domain %s: %s", domain, e, exc_info=True)
                stats["errors"].append({"stage": "pipeline", "error": str(e)})
                self.metrics.record_error("pipeline", type(e).__name__, str(e))
                return stats

    async def _collect_from_urls(
        self,
        web_urls: list[str],
        pdf_urls: list[str],
        domain: str,
        subdomain: str,
        max_concurrent: int | None = None,
        max_articles: int | None = None,
    ) -> list[dict[str, Any]]:
        """Collect knowledge articles from URLs with parallel processing.
        
        Args:
            web_urls: List of web URLs
            pdf_urls: List of PDF URLs
            domain: Knowledge domain
            subdomain: Subdomain
            max_concurrent: Maximum concurrent URL fetches (None uses config default)
            max_articles: Maximum number of articles to extract (None for all)
            
        Returns:
            List of raw article dictionaries
        """
        if max_concurrent is None:
            max_concurrent = self.settings.max_concurrent_urls
        import asyncio
        from crawl4ai import AsyncWebCrawler

        all_articles = []
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_web_url(crawler: AsyncWebCrawler, url: str) -> list[dict[str, Any]]:
            """Process a single web URL with retry logic and circuit breaker.
            
            Args:
                crawler: Shared AsyncWebCrawler instance
                url: URL to process
                
            Returns:
                List of extracted articles
            """
            async with semaphore:
                if self.domain_circuit_breaker.is_open(url):
                    domain = self.domain_circuit_breaker.get_domain(url)
                    logger.debug(
                        "Skipping URL %s - domain %s circuit breaker is OPEN",
                        url,
                        domain
                    )
                    return []
                
                await self.domain_rate_limiter.acquire(url)
                
                max_attempts = self.url_fetch_max_retries + 1
                delay = 2.0
                import random
                
                for attempt in range(max_attempts):
                    try:
                        crawl_result = await asyncio.wait_for(
                            crawler.arun(url=url, bypass_cache=True),
                            timeout=self.url_fetch_timeout
                        )
                        markdown_content = crawl_result.markdown or ""
                        html_content = crawl_result.html or ""

                        if markdown_content or html_content:
                            content_to_use = markdown_content if markdown_content else html_content
                            articles = await asyncio.wait_for(
                                self.knowledge_extractor.extract_articles(
                                    content=content_to_use,
                                    domain=domain,
                                    subdomain=subdomain,
                                    source_url=url,
                                    prefer_markdown=True,
                                    markdown_content=markdown_content if markdown_content else None,
                                ),
                                timeout=self.llm_api_timeout
                            )
                            self.domain_circuit_breaker.record_success(url)
                            return articles
                        else:
                            logger.warning("No content extracted from web URL: %s", url)
                            self.domain_circuit_breaker.record_failure(url)
                            return []
                    except (asyncio.TimeoutError, TimeoutError) as e:
                        if attempt < max_attempts - 1:
                            jitter = random.uniform(0, delay * 0.1)
                            delay_with_jitter = delay + jitter
                            logger.warning(
                                "Timeout fetching web URL %s (attempt %d/%d, timeout: %.1fs). Retrying in %.1fs...",
                                url,
                                attempt + 1,
                                max_attempts,
                                self.url_fetch_timeout,
                                delay_with_jitter
                            )
                            await asyncio.sleep(delay_with_jitter)
                            delay = min(delay * 2.0, 10.0)
                        else:
                            logger.error(
                                "Timeout fetching web URL %s after %d attempts (timeout: %.1fs). "
                                "This may indicate network issues or the website is slow/unresponsive.",
                                url,
                                max_attempts,
                                self.url_fetch_timeout
                            )
                            self.domain_circuit_breaker.record_failure(url)
                            await self.dead_letter_queue.record_failure(
                                url=url,
                                error=f"Timeout after {max_attempts} attempts",
                                error_type="TimeoutError",
                                attempts=max_attempts,
                            )
                            return []
                    except (ValueError, TypeError, KeyError, AttributeError, ConnectionError, RuntimeError) as e:
                        error_type = type(e).__name__
                        if attempt < max_attempts - 1:
                            jitter = random.uniform(0, delay * 0.1)
                            delay_with_jitter = delay + jitter
                            logger.warning(
                                "Error fetching web URL %s (attempt %d/%d): %s: %s. Retrying in %.1fs...",
                                url,
                                attempt + 1,
                                max_attempts,
                                error_type,
                                str(e),
                                delay_with_jitter
                            )
                            await asyncio.sleep(delay_with_jitter)
                            delay = min(delay * 2.0, 10.0)
                        else:
                            logger.error(
                                "Error collecting from web URL %s after %d attempts: %s: %s",
                                url,
                                max_attempts,
                                error_type,
                                str(e)
                            )
                            self.domain_circuit_breaker.record_failure(url)
                            await self.dead_letter_queue.record_failure(
                                url=url,
                                error=str(e),
                                error_type=error_type,
                                attempts=max_attempts,
                            )
                            return []
                
                return []

        async def process_pdf_url(url: str) -> list[dict[str, Any]]:
            """Process a single PDF URL with circuit breaker.
            
            Args:
                url: PDF URL to process
                
            Returns:
                List of extracted articles
            """
            if self.domain_circuit_breaker.is_open(url):
                domain = self.domain_circuit_breaker.get_domain(url)
                logger.debug(
                    "Skipping PDF URL %s - domain %s circuit breaker is OPEN",
                    url,
                    domain
                )
                return []
            
            await self.domain_rate_limiter.acquire(url)
            async with semaphore:
                import tempfile
                from pathlib import Path
                import httpx
                import re
                
                try:
                    from ..processors.document_processor import DocumentProcessor

                    doc_processor = DocumentProcessor()
                    
                    original_url = url
                    
                    if "github.com" in url and "/blob/" in url:
                        url = re.sub(
                            r"https://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+)",
                            r"https://raw.githubusercontent.com/\1/\2/\3/\4",
                            url
                        )
                        logger.info("Converted GitHub blob URL to raw URL: %s -> %s", original_url, url)
                    
                    logger.info("Downloading PDF from URL: %s", url)
                    
                    async with httpx.AsyncClient(timeout=self.url_fetch_timeout, follow_redirects=True) as client:
                        response = await client.get(url)
                        response.raise_for_status()
                        
                        content_type = response.headers.get("content-type", "").lower()
                        is_pdf_content_type = content_type.startswith("application/pdf")
                        is_pdf_url = url.lower().endswith(".pdf") or ".pdf" in url.lower()
                        
                        if not is_pdf_content_type and not is_pdf_url:
                            logger.warning("URL does not appear to be a PDF (content-type: %s, url: %s)", content_type, url)
                            return []
                        
                        if not is_pdf_content_type and is_pdf_url:
                            logger.info("URL ends with .pdf but content-type is %s, attempting to process anyway", content_type)
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                            tmp_path = Path(tmp_file.name)
                            tmp_path.write_bytes(response.content)
                            logger.info("Downloaded PDF (%d bytes) to temporary file: %s", len(response.content), tmp_path)
                        
                        try:
                            loop = asyncio.get_event_loop()
                            pdf_content = await asyncio.wait_for(
                                loop.run_in_executor(None, doc_processor.process_pdf, tmp_path),
                                timeout=self.pdf_processing_timeout
                            )

                            if pdf_content.get("text"):
                                estimated_chunks = len(pdf_content["text"]) // 15000 + 1
                                dynamic_timeout = max(
                                    self.llm_api_timeout * estimated_chunks * 1.5,
                                    self.llm_api_timeout * 5
                                )
                                logger.debug(
                                    "Using dynamic timeout %.1fs for PDF extraction (estimated %d chunks)",
                                    dynamic_timeout,
                                    estimated_chunks
                                )
                                
                                try:
                                    articles = await asyncio.wait_for(
                                        self.knowledge_extractor.extract_articles(
                                            content=pdf_content["text"],
                                            domain=domain,
                                            subdomain=subdomain,
                                            source_url=original_url,
                                            prefer_markdown=True,
                                            markdown_content=pdf_content.get("markdown"),
                                        ),
                                        timeout=dynamic_timeout
                                    )
                                    self.domain_circuit_breaker.record_success(url)
                                    return articles
                                except asyncio.TimeoutError:
                                    logger.error(
                                        "Timeout extracting articles from PDF URL %s (timeout: %.1fs, estimated chunks: %d)",
                                        url,
                                        dynamic_timeout,
                                        estimated_chunks
                                    )
                                    return []
                            return []
                        finally:
                            if tmp_path.exists():
                                tmp_path.unlink()
                                logger.debug("Cleaned up temporary PDF file: %s", tmp_path)
                                
                except asyncio.TimeoutError as e:
                    if "extracting articles" not in str(e):
                        logger.error("Timeout processing PDF URL %s (timeout: %.1fs)", url, self.pdf_processing_timeout)
                    self.domain_circuit_breaker.record_failure(url)
                    await self.dead_letter_queue.record_failure(
                        url=url,
                        error=f"Timeout processing PDF (timeout: {self.pdf_processing_timeout}s)",
                        error_type="TimeoutError",
                        attempts=1,
                    )
                    return []
                except httpx.HTTPError as e:
                    logger.error("HTTP error downloading PDF URL %s: %s", url, e)
                    self.domain_circuit_breaker.record_failure(url)
                    await self.dead_letter_queue.record_failure(
                        url=url,
                        error=str(e),
                        error_type="HTTPError",
                        attempts=1,
                    )
                    return []
                except (ValueError, TypeError, KeyError, AttributeError, ConnectionError, RuntimeError) as e:
                    logger.error("Error collecting from PDF URL %s: %s", url, e)
                    self.domain_circuit_breaker.record_failure(url)
                    await self.dead_letter_queue.record_failure(
                        url=url,
                        error=str(e),
                        error_type=type(e).__name__,
                        attempts=1,
                    )
                    return []

        crawler_config = {
            "headless": True,
            "verbose": False,
        }
        async with AsyncWebCrawler(**crawler_config) as crawler:
            if web_urls:
                logger.info("Processing %d web URLs in parallel (max_concurrent=%d)", len(web_urls), max_concurrent)
                web_tasks = [process_web_url(crawler, url) for url in web_urls]
                web_results = await asyncio.gather(*web_tasks, return_exceptions=True)
                
                for result in web_results:
                    if isinstance(result, Exception):
                        logger.error("Exception in parallel web URL processing: %s", result)
                        continue
                    if isinstance(result, list):
                        all_articles.extend(result)

            if pdf_urls:
                logger.info("Processing %d PDF URLs in parallel (max_concurrent=%d)", len(pdf_urls), max_concurrent)
                pdf_tasks = [process_pdf_url(url) for url in pdf_urls]
                pdf_results = await asyncio.gather(*pdf_tasks, return_exceptions=True)
                
                for result in pdf_results:
                    if isinstance(result, Exception):
                        logger.error("Exception in parallel PDF URL processing: %s", result)
                        continue
                    if isinstance(result, list):
                        all_articles.extend(result)

        logger.info("Collected %d articles from %d web URLs and %d PDF URLs", len(all_articles), len(web_urls), len(pdf_urls))
        
        if max_articles is not None and len(all_articles) > max_articles:
            logger.info(
                "Limiting articles to %d (from %d)",
                max_articles,
                len(all_articles),
            )
            all_articles = all_articles[:max_articles]
        
        return all_articles

    async def _collect_from_urls_paginated(
        self,
        web_urls: list[str],
        pdf_urls: list[str],
        domain: str,
        subdomain: str,
        max_concurrent: int | None = None,
        max_articles: int | None = None,
    ) -> AsyncIterator[list[dict[str, Any]]]:
        """Collect knowledge articles from URLs with paginated processing (memory-efficient).
        
        Processes URLs in batches to avoid loading all URLs and results into memory.
        Yields batches of articles as they're collected.
        
        Args:
            web_urls: List of web URLs
            pdf_urls: List of PDF URLs
            domain: Knowledge domain
            subdomain: Subdomain
            max_concurrent: Maximum concurrent URL fetches (None uses config default)
            max_articles: Maximum number of articles to extract (None for all)
            
        Yields:
            Batches of raw article dictionaries
        """
        if max_concurrent is None:
            max_concurrent = self.settings.max_concurrent_urls
        
        total_urls = len(web_urls) + len(pdf_urls)
        processed_urls = 0
        total_articles_collected = 0
        
        logger.info(
            "Starting paginated collection: %d web URLs, %d PDF URLs (batch size: %d)",
            len(web_urls),
            len(pdf_urls),
            self.collection_batch_size
        )
        
        web_url_batches = [
            web_urls[i : i + self.collection_batch_size]
            for i in range(0, len(web_urls), self.collection_batch_size)
        ]
        
        pdf_url_batches = [
            pdf_urls[i : i + self.collection_batch_size]
            for i in range(0, len(pdf_urls), self.collection_batch_size)
        ]
        
        for batch_idx, web_batch in enumerate(web_url_batches):
            if max_articles is not None and total_articles_collected >= max_articles:
                logger.info(
                    "Reached max_articles limit (%d), stopping collection",
                    max_articles
                )
                return
            
            remaining_articles = None
            if max_articles is not None:
                remaining_articles = max_articles - total_articles_collected
            
            logger.info(
                "Processing web URL batch %d/%d (%d URLs, %.1f%% complete)",
                batch_idx + 1,
                len(web_url_batches),
                len(web_batch),
                100 * processed_urls / total_urls if total_urls > 0 else 0
            )
            
            batch_articles = await self._collect_from_urls(
                web_batch,
                [],
                domain,
                subdomain,
                max_concurrent=max_concurrent,
                max_articles=remaining_articles
            )
            
            if batch_articles:
                total_articles_collected += len(batch_articles)
                processed_urls += len(web_batch)
                yield batch_articles
                
                if max_articles is not None and total_articles_collected >= max_articles:
                    logger.info(
                        "Reached max_articles limit (%d) after batch, stopping collection",
                        max_articles
                    )
                    return
        
        for batch_idx, pdf_batch in enumerate(pdf_url_batches):
            if max_articles is not None and total_articles_collected >= max_articles:
                logger.info(
                    "Reached max_articles limit (%d), stopping collection",
                    max_articles
                )
                return
            
            remaining_articles = None
            if max_articles is not None:
                remaining_articles = max_articles - total_articles_collected
            
            logger.info(
                "Processing PDF URL batch %d/%d (%d URLs, %.1f%% complete)",
                batch_idx + 1,
                len(pdf_url_batches),
                len(pdf_batch),
                100 * processed_urls / total_urls if total_urls > 0 else 0
            )
            
            batch_articles = await self._collect_from_urls(
                [],
                pdf_batch,
                domain,
                subdomain,
                max_concurrent=max_concurrent,
                max_articles=remaining_articles
            )
            
            if batch_articles:
                total_articles_collected += len(batch_articles)
                processed_urls += len(pdf_batch)
                yield batch_articles
                
                if max_articles is not None and total_articles_collected >= max_articles:
                    logger.info(
                        "Reached max_articles limit (%d) after batch, stopping collection",
                        max_articles
                    )
                    return
        
        logger.info(
            "Paginated collection complete: processed %d/%d URLs, collected %d articles",
            processed_urls,
            total_urls,
            total_articles_collected
        )

    def _get_quality_threshold(self, domain: str) -> float:
        """Get quality threshold for domain.
        
        Compliance/regulatory content may have lower actionability scores
        but still be valuable reference materials, so we use a lower threshold.
        
        Args:
            domain: Knowledge domain
            
        Returns:
            Quality threshold (0-100)
        """
        domain_thresholds = {
            "compliance": 65.0,
            "security": 65.0,
            "finops": 70.0,
            "devops": 70.0,
            "infrastructure": 70.0,
            "architecture": 70.0,
            "cloud": 70.0,
            "automation": 70.0,
            "platform": 70.0,
            "sre": 70.0,
        }
        return domain_thresholds.get(domain, 70.0)

    async def _process_article_batch(
        self,
        raw_articles_batch: list[dict[str, Any]],
        processor: BaseKnowledgeProcessor,
        stats: dict[str, Any],
    ) -> tuple[list[dict[str, Any]], int]:
        """Process a batch of raw articles through processing → embedding → loading.
        
        Args:
            raw_articles_batch: Batch of raw article dictionaries
            processor: Domain-specific processor
            stats: Pipeline statistics dictionary (updated in-place)
            
        Returns:
            Tuple of (processed_articles_dicts, articles_loaded_count)
        """
        if not raw_articles_batch:
            return [], 0
        
        processed_articles = []
        failed_processing = []
        
        for raw in raw_articles_batch:
            try:
                article = processor.process_raw_data(raw)
                
                if not processor.validate_article(article):
                    logger.warning(
                        "Validation failed for article: %s",
                        raw.get("title", "unknown"),
                    )
                    failed_processing.append({"raw": raw, "error": "Validation failed"})
                    continue
                
                quality_score = self.quality_validator.validate(article)
                article.quality_score = quality_score.overall_score
                article.source_credibility = quality_score.source_credibility
                article.freshness_score = quality_score.freshness
                
                quality_threshold = self._get_quality_threshold(article.domain)
                if quality_score.overall_score < quality_threshold:
                    logger.warning(
                        "Article %s rejected: quality score %.2f < %.1f (threshold for %s)",
                        article.article_id,
                        quality_score.overall_score,
                        quality_threshold,
                        article.domain,
                    )
                    stats["quality_rejected"] += 1
                    continue
                
                processed_articles.append(article)
                stats["validated"] += 1
                
            except ValueError as e:
                error_msg = str(e)
                if "Article filtered out" in error_msg:
                    logger.debug("Article filtered out during processing: %s", error_msg)
                else:
                    logger.error("Error processing article: %s", e, exc_info=True)
                failed_processing.append({"raw": raw, "error": str(e)})
                continue
            except (TypeError, KeyError, AttributeError, RuntimeError) as e:
                logger.error("Error processing article: %s", e, exc_info=True)
                failed_processing.append({"raw": raw, "error": str(e)})
                continue
        
        stats["processed"] += len(processed_articles)
        stats["errors"].extend(failed_processing)
        
        for article in processed_articles:
            self.metrics.record_item_processed("processing", "knowledge", success=True)
        
        for failed in failed_processing:
            self.metrics.record_item_processed("processing", "knowledge", success=False)
            self.metrics.record_error(
                "processing", failed.get("error", "Unknown"), str(failed)
            )
        
        if not processed_articles:
            return [], 0
        
        articles_dict = [article.model_dump(mode="json") for article in processed_articles]
        
        items_to_embed = []
        items_skipped_embedding = []
        
        if self.enable_change_detection and self.change_detector:
            for article_dict in articles_dict:
                article_id = article_dict.get("article_id")
                if not article_id:
                    items_to_embed.append(article_dict)
                    continue
                
                try:
                    if self.change_detector.collection is not None:
                        existing_doc = self.change_detector.collection.find_one(
                            {"article_id": article_id},
                            {"content_hash": 1}
                        )
                    else:
                        existing_doc = None
                    
                    should_generate, content_hash = self.change_detector.should_generate_article_embedding(
                        article_dict, article_id, existing_doc
                    )
                    
                    if not should_generate:
                        stats["skipped_content_unchanged"] += 1
                        stats["embedding_calls_saved"] += 1
                        items_skipped_embedding.append(article_dict)
                        continue
                    
                    article_dict["_content_hash"] = content_hash
                    items_to_embed.append(article_dict)
                except (ValueError, TypeError, KeyError, AttributeError, RuntimeError) as e:
                    logger.warning("Error checking content hash for article %s: %s - generating embedding anyway", article_id, e)
                    items_to_embed.append(article_dict)
        else:
            items_to_embed = articles_dict
        
        if items_to_embed:
            items_with_embeddings, failed_embedding = await self.embedder.generate_embeddings(
                items_to_embed, "knowledge"
            )
            
            if items_skipped_embedding:
                items_with_embeddings.extend(items_skipped_embedding)
            
            stats["embedded"] += len([a for a in items_with_embeddings if a.get("embedding")])
            stats["errors"].extend(failed_embedding)
            
            for _ in items_with_embeddings:
                self.metrics.record_item_processed("embedding", "knowledge", success=True)
            
            for failed in failed_embedding:
                self.metrics.record_item_processed("embedding", "knowledge", success=False)
                self.metrics.record_error(
                    "embedding", failed.get("error", "Unknown"), str(failed)
                )
        else:
            items_with_embeddings = items_skipped_embedding
        
        if items_with_embeddings:
            load_stats = self.loader.load_knowledge_articles(items_with_embeddings)
            articles_loaded = load_stats["mongodb_inserted"] + load_stats["mongodb_updated"]
            stats["loaded_mongodb"] += articles_loaded
            stats["loaded_pinecone"] += load_stats["pinecone_loaded"]
            
            self.metrics.record_item_processed("loading", "knowledge", success=True)
        else:
            articles_loaded = 0
        
        return items_with_embeddings, articles_loaded

    async def _run_streaming_pipeline_from_collection(
        self,
        domain: str,
        subdomain: str | None,
        processor: BaseKnowledgeProcessor | None,
        stats: dict[str, Any],
        max_urls: int | None,
        max_pdfs: int | None,
        max_docs: int | None,
        max_articles: int | None,
        max_concurrent: int | None,
        disable_deep_crawl_when_limited: bool,
    ) -> dict[str, Any]:
        """Run streaming pipeline starting from collection (memory-efficient).
        
        Processes articles as they're collected, avoiding loading all into memory.
        
        Args:
            domain: Knowledge domain
            subdomain: Optional subdomain
            processor: Domain-specific processor
            stats: Pipeline statistics dictionary
            max_urls: Maximum web URLs
            max_pdfs: Maximum PDF URLs
            max_docs: Maximum total documents
            max_articles: Maximum articles to extract
            max_concurrent: Maximum concurrent URL fetches
            disable_deep_crawl_when_limited: Disable deep crawl when limited
            
        Returns:
            Pipeline statistics dictionary
        """
        logger.info("Running streaming pipeline with paginated collection for domain: %s", domain)
        
        collection_metrics = self.metrics.start_stage("collection", "knowledge")
        processing_metrics = self.metrics.start_stage("processing", "knowledge")
        embedding_metrics = self.metrics.start_stage("embedding", "knowledge")
        loading_metrics = self.metrics.start_stage("loading", "knowledge")
        
        disable_deep_crawl = (
            disable_deep_crawl_when_limited 
            and max_urls is not None
        )
        
        if disable_deep_crawl:
            logger.info(
                "Deep crawling disabled because max_urls is set (%d) and disable_deep_crawl_when_limited=True",
                max_urls
            )
        
        discovered = await get_discovered_urls(
            domain, 
            subdomain, 
            disable_deep_crawl=disable_deep_crawl
        )
        
        web_urls = discovered.get("web_urls", [])
        pdf_urls = discovered.get("pdf_urls", [])
        
        logger.info(
            "Discovered %d web URLs and %d PDF URLs",
            len(web_urls),
            len(pdf_urls),
        )
        
        if max_urls is not None and len(web_urls) > max_urls:
            logger.info("Limiting web URLs to %d (from %d)", max_urls, len(web_urls))
            web_urls = web_urls[:max_urls]
        
        if max_pdfs is not None and len(pdf_urls) > max_pdfs:
            logger.info("Limiting PDF URLs to %d (from %d)", max_pdfs, len(pdf_urls))
            pdf_urls = pdf_urls[:max_pdfs]
        
        if max_docs is not None:
            total_docs = len(web_urls) + len(pdf_urls)
            if total_docs > max_docs:
                logger.info(
                    "Limiting total documents to %d (from %d web + %d PDF)",
                    max_docs, len(web_urls), len(pdf_urls)
                )
                remaining = max_docs
                if len(web_urls) > 0:
                    web_urls = web_urls[:min(len(web_urls), remaining)]
                    remaining -= len(web_urls)
                if remaining > 0 and len(pdf_urls) > 0:
                    pdf_urls = pdf_urls[:min(len(pdf_urls), remaining)]
        
        if processor is None:
            processor = self._get_processor_for_domain(domain)
            if processor is None:
                stats["errors"].append({"stage": "processing", "error": "No processor available"})
                return stats
        
        self.processor = processor
        
        if self.enable_change_detection:
            if self.change_detector is None:
                from api.database.mongodb import mongodb_manager
                mongodb_manager.connect()
                db = mongodb_manager.get_database()
                self.change_detector = ChangeDetector(
                    db.knowledge_articles,
                    enabled=self.enable_change_detection
                )
        
        total_collected = 0
        total_processed = 0
        total_loaded = 0
        batch_count = 0
        
        async for article_batch in self._collect_from_urls_paginated(
            web_urls, pdf_urls, domain, subdomain or "",
            max_concurrent=max_concurrent,
            max_articles=max_articles
        ):
            total_collected += len(article_batch)
            stats["collected"] = total_collected
            batch_count += 1
            
            for article in article_batch:
                self.metrics.record_item_processed("collection", "knowledge", success=True)
            
            if self.enable_change_detection and self.change_detector:
                self.change_detector.batch_check_article_source_hashes(article_batch)
                filtered_batch = []
                
                for raw_article in article_batch:
                    article_id = raw_article.get("article_id")
                    should_process, source_hash = self.change_detector.should_process_article_source(
                        raw_article, article_id
                    )
                    
                    if not should_process:
                        stats["skipped_source_unchanged"] += 1
                        stats["llm_calls_saved"] += 1
                        stats["embedding_calls_saved"] += 1
                        continue
                    
                    raw_article["_source_hash"] = source_hash
                    filtered_batch.append(raw_article)
                
                article_batch = filtered_batch
            
            if article_batch:
                processed_batch, batch_loaded = await self._process_article_batch(
                    article_batch, processor, stats
                )
                total_processed += len(processed_batch)
                total_loaded += batch_loaded
                
                logger.info(
                    "Streaming batch complete: collected=%d, processed=%d, loaded=%d (total: collected=%d, processed=%d, loaded=%d)",
                    len(article_batch),
                    len(processed_batch),
                    batch_loaded,
                    total_collected,
                    total_processed,
                    total_loaded
                )
            
            if self.enable_checkpointing and self.pipeline_progress:
                if batch_count % (self.checkpoint_interval // self.collection_batch_size + 1) == 0 or len(article_batch) > 0:
                    await self.pipeline_progress.save_checkpoint(
                        stage="collection",
                        stats=stats.copy(),
                        metadata={
                            "batch_count": batch_count,
                            "total_collected": total_collected,
                            "total_processed": total_processed,
                            "total_loaded": total_loaded,
                        }
                    )
        
        collection_metrics.items_processed = total_collected
        collection_metrics.items_succeeded = total_collected
        self.metrics.finish_stage("collection", "knowledge")
        
        processing_metrics.items_processed = total_processed
        processing_metrics.items_succeeded = total_processed
        self.metrics.finish_stage("processing", "knowledge")
        
        embedding_metrics.items_processed = stats["embedded"]
        embedding_metrics.items_succeeded = stats["embedded"]
        self.metrics.finish_stage("embedding", "knowledge")
        
        loading_metrics.items_processed = total_loaded
        loading_metrics.items_succeeded = total_loaded
        self.metrics.finish_stage("loading", "knowledge")
        
        summary = self.metrics.get_summary()
        stats["metrics_summary"] = summary
        
        if self.enable_checkpointing and self.pipeline_progress:
            await self.pipeline_progress.save_checkpoint(
                stage="completed",
                stats=stats.copy(),
                metadata={
                    "completed": True,
                    "total_collected": total_collected,
                    "total_processed": total_processed,
                    "total_loaded": total_loaded,
                }
            )
            logger.info("Final checkpoint saved for pipeline %s", self.pipeline_progress.pipeline_id)
        
        logger.info("=" * 80)
        logger.info("Streaming pipeline completed for domain: %s", domain)
        logger.info(
            "Collected: %d, Processed: %d, Validated: %d, Embedded: %d, Loaded: %d",
            stats["collected"],
            stats["processed"],
            stats["validated"],
            stats["embedded"],
            stats["loaded_mongodb"],
        )
        logger.info("=" * 80)
        
        return stats

    async def _run_streaming_pipeline(
        self,
        raw_articles: list[dict[str, Any]],
        domain: str,
        subdomain: str | None,
        processor: BaseKnowledgeProcessor,
        stats: dict[str, Any],
    ) -> dict[str, Any]:
        """Run streaming pipeline with existing raw articles.
        
        This is called when streaming is enabled but collection was already done.
        Processes articles in batches instead of all at once.
        
        Args:
            raw_articles: List of raw article dictionaries
            domain: Knowledge domain
            subdomain: Optional subdomain
            processor: Domain-specific processor
            stats: Pipeline statistics dictionary
            
        Returns:
            Pipeline statistics dictionary
        """
        logger.info("Running streaming pipeline for domain: %s (%d articles)", domain, len(raw_articles))
        
        batch_size = self.collection_batch_size
        
        batches = [
            raw_articles[i : i + batch_size]
            for i in range(0, len(raw_articles), batch_size)
        ]
        
        processing_metrics = self.metrics.start_stage("processing", "knowledge")
        embedding_metrics = self.metrics.start_stage("embedding", "knowledge")
        loading_metrics = self.metrics.start_stage("loading", "knowledge")
        
        for batch_idx, batch in enumerate(batches):
            logger.info(
                "Processing batch %d/%d (%d articles)",
                batch_idx + 1,
                len(batches),
                len(batch)
            )
            
            processed_batch, batch_loaded = await self._process_article_batch(
                batch, processor, stats
            )
        
        processing_metrics.items_processed = stats["processed"]
        processing_metrics.items_succeeded = stats["processed"]
        self.metrics.finish_stage("processing", "knowledge")
        
        embedding_metrics.items_processed = stats["embedded"]
        embedding_metrics.items_succeeded = stats["embedded"]
        self.metrics.finish_stage("embedding", "knowledge")
        
        loading_metrics.items_processed = stats["loaded_mongodb"]
        loading_metrics.items_succeeded = stats["loaded_mongodb"]
        self.metrics.finish_stage("loading", "knowledge")
        
        summary = self.metrics.get_summary()
        stats["metrics_summary"] = summary
        
        logger.info("=" * 80)
        logger.info("Streaming pipeline completed for domain: %s", domain)
        logger.info(
            "Processed: %d, Validated: %d, Embedded: %d, Loaded: %d",
            stats["processed"],
            stats["validated"],
            stats["embedded"],
            stats["loaded_mongodb"],
        )
        logger.info("=" * 80)
        
        return stats

    def _get_processor_for_domain(self, domain: str) -> BaseKnowledgeProcessor | None:
        """Get processor for domain.
        
        Args:
            domain: Knowledge domain
            
        Returns:
            Processor instance or None if not found
        """
        if domain == "compliance":
            from .compliance_knowledge_processor import ComplianceKnowledgeProcessor
            return ComplianceKnowledgeProcessor()
        elif domain == "finops":
            from .finops_knowledge_processor import FinOpsKnowledgeProcessor
            return FinOpsKnowledgeProcessor()
        elif domain == "devops":
            from .devops_knowledge_processor import DevOpsKnowledgeProcessor
            return DevOpsKnowledgeProcessor()
        elif domain == "security":
            from .security_knowledge_processor import SecurityKnowledgeProcessor
            return SecurityKnowledgeProcessor()
        elif domain == "infrastructure":
            from .infrastructure_knowledge_processor import InfrastructureKnowledgeProcessor
            return InfrastructureKnowledgeProcessor()
        elif domain == "architecture":
            from .architecture_knowledge_processor import ArchitectureKnowledgeProcessor
            return ArchitectureKnowledgeProcessor()
        elif domain == "cloud":
            from .cloud_knowledge_processor import CloudKnowledgeProcessor
            return CloudKnowledgeProcessor()
        elif domain == "automation":
            from .automation_knowledge_processor import AutomationKnowledgeProcessor
            return AutomationKnowledgeProcessor()
        elif domain == "platform":
            from .platform_knowledge_processor import PlatformKnowledgeProcessor
            return PlatformKnowledgeProcessor()
        elif domain == "sre":
            from .sre_knowledge_processor import SREKnowledgeProcessor
            return SREKnowledgeProcessor()
        else:
            logger.error("No processor available for domain: %s", domain)
            return None

    def get_metrics_summary(self) -> dict[str, Any]:
        """Get metrics summary.
        
        Returns:
            Dictionary with metrics summary
        """
        return self.metrics.get_summary()

