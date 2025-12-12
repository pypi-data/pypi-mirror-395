"""Pipeline orchestrator - coordinates all pipeline stages."""

import asyncio
import random
from typing import Any, Callable

from ..collectors.compliance_collector import ComplianceCollector
from ..config.compliance_urls import COMPLIANCE_URLS
from ..loaders.mongodb_loader import MongoDBLoader
from ..utils.change_detector import ChangeDetector, extract_control_id
from ..utils.tracing import TracingContext, get_correlation_id
from .compliance_processor import ComplianceProcessor
from .cost_data_processor import CostDataProcessor
from .cost_allocation_processor import CostAllocationProcessor
from .embedding_generator import EmbeddingGenerator
from .monitoring import HealthCheck, PipelineMetrics
from ..collectors.pricing_collector import CostDataCollector
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class PipelineConfig:
    """Pipeline configuration."""

    def __init__(
        self,
        mode: str = "streaming",
        save_intermediate: bool = False,
        save_raw_data: bool = True,
        enable_change_detection: bool = True,
        enable_streaming_saves: bool = True,
        streaming_batch_size: int = 10,
        embedding_batch_size: int = 20,
        max_urls: int | None = None,
        max_pdfs: int | None = None,
        max_controls: int | None = None,
        disable_deep_crawl_when_limited: bool = False,
        context_generation_concurrency: int = 5,
        context_generation_fail_fast: bool = False,
    ):
        """Initialize pipeline configuration.

        Args:
            mode: Pipeline mode ("streaming" or "checkpointing")
            save_intermediate: Save intermediate files (checkpointing mode)
            save_raw_data: Save raw data (always recommended)
            enable_change_detection: Enable source-level change detection (default: True)
            enable_streaming_saves: Enable streaming saves to MongoDB (default: True)
            streaming_batch_size: Batch size for streaming saves progress logging (default: 10)
            embedding_batch_size: Batch size for embedding generation (default: 20)
            max_urls: Maximum number of seed URLs to process (None for all). 
                     Note: Deep crawling may discover additional pages from seed URLs.
            max_pdfs: Maximum number of PDFs to process (None for all)
            max_controls: Maximum number of controls to collect (None for all)
            disable_deep_crawl_when_limited: If True, disable deep crawling when max_urls is set (default: False)
            context_generation_concurrency: Maximum concurrent context generation requests (default: 10)
            context_generation_fail_fast: If True, stop on first context generation error (default: False)
        """
        self.mode = mode
        self.save_intermediate = save_intermediate if mode == "checkpointing" else False
        self.save_raw_data = save_raw_data
        self.enable_change_detection = enable_change_detection
        self.enable_streaming_saves = enable_streaming_saves
        self.streaming_batch_size = streaming_batch_size
        self.embedding_batch_size = embedding_batch_size
        self.max_urls = max_urls
        self.max_pdfs = max_pdfs
        self.max_controls = max_controls
        self.disable_deep_crawl_when_limited = disable_deep_crawl_when_limited
        self.context_generation_concurrency = context_generation_concurrency
        self.context_generation_fail_fast = context_generation_fail_fast


class PipelineOrchestrator:
    """Orchestrates the complete data processing pipeline.

    Coordinates Collection → Processing → Embedding → Loading stages.
    """

    def __init__(self, config: PipelineConfig):
        """Initialize pipeline orchestrator.

        Args:
            config: Pipeline configuration
        """
        self.config = config
        self.collector = ComplianceCollector()
        self.processor = ComplianceProcessor(save_intermediate=config.save_intermediate)
        self.embedder = EmbeddingGenerator(save_intermediate=config.save_intermediate)
        self.loader: MongoDBLoader | None = None
        self.metrics = PipelineMetrics(enable_prometheus=True)
        self.health_check = HealthCheck()
        self.change_detector: ChangeDetector | None = None
        self._streaming_stats: dict[str, int] = {
            "mongodb_inserted": 0,
            "mongodb_updated": 0,
            "mongodb_errors": 0,
            "pinecone_loaded": 0,
            "pinecone_skipped": 0,
            "skipped_content_unchanged": 0,
            "embedding_calls_saved": 0,
        }
        self._progress_callback: Callable[[str, float, dict[str, Any], dict[str, Any]], None] | None = None

        self._check_dependencies()

    def set_progress_callback(
        self, callback: Callable[[str, float, dict[str, Any], dict[str, Any]], None]
    ) -> None:
        """Set progress callback function.

        Args:
            callback: Async function(stage: str, progress: float, stats: dict, stages: dict) -> None
        """
        self._progress_callback = callback

    def _build_stages_dict(self) -> dict[str, Any]:
        """Build stages dictionary from metrics.

        Returns:
            Dictionary mapping stage names to stage progress data
        """
        stages = {}
        for key, metrics in self.metrics.stage_metrics.items():
            stage_name = metrics.stage_name
            
            if metrics.end_time:
                if metrics.items_processed > 0:
                    status = "completed"
                elif metrics.start_time:
                    status = "completed"
                else:
                    status = "pending"
            elif metrics.start_time:
                status = "running"
            else:
                status = "pending"
            
            stages[stage_name] = {
                "stage_name": stage_name,
                "status": status,
                "items_processed": metrics.items_processed,
                "items_succeeded": metrics.items_succeeded,
                "items_failed": metrics.items_failed,
                "duration_seconds": metrics.duration_seconds if metrics.end_time else None,
                "progress_percentage": (
                    metrics.items_succeeded / metrics.items_processed
                    if metrics.items_processed > 0
                    else (100.0 if metrics.end_time else 0.0)
                ),
            }
        return stages

    def _update_collection_progress(self, items_collected: int, stats: dict[str, Any]) -> None:
        """Update collection progress incrementally.
        
        Args:
            items_collected: Number of items collected so far
            stats: Statistics dictionary to update
        """
        stats["collected"] = items_collected
        collection_metrics = self.metrics.get_stage_metrics("collection", "compliance")
        if collection_metrics:
            collection_metrics.items_processed = items_collected
            collection_metrics.items_succeeded = items_collected

    def _calculate_overall_progress(self, stats: dict[str, Any]) -> float:
        """Calculate overall pipeline progress based on stage completion.

        Args:
            stats: Pipeline statistics

        Returns:
            Progress value between 0.0 and 1.0
        """
        collection_metrics = self.metrics.get_stage_metrics("collection", "compliance")
        processing_metrics = self.metrics.get_stage_metrics("processing", "compliance")
        embedding_metrics = self.metrics.get_stage_metrics("embedding", "compliance")
        loading_metrics = self.metrics.get_stage_metrics("loading", "compliance")
        
        if collection_metrics and collection_metrics.end_time:
            collection_progress = 1.0
        elif collection_metrics and collection_metrics.start_time:
            if collection_metrics.items_processed > 0:
                collection_progress = min(collection_metrics.items_succeeded / collection_metrics.items_processed, 1.0)
            else:
                collection_progress = 0.1
        else:
            collection_progress = 0.0
        
        if processing_metrics and processing_metrics.end_time:
            processing_progress = 1.0
        elif processing_metrics and processing_metrics.start_time:
            if processing_metrics.items_processed > 0:
                processing_progress = min(processing_metrics.items_succeeded / processing_metrics.items_processed, 1.0)
            else:
                processing_progress = 0.1
        else:
            processing_progress = 0.0
        
        if embedding_metrics and embedding_metrics.end_time:
            embedding_progress = 1.0
        elif embedding_metrics and embedding_metrics.start_time:
            if embedding_metrics.items_processed > 0:
                embedding_progress = min(embedding_metrics.items_succeeded / embedding_metrics.items_processed, 1.0)
            else:
                embedding_progress = 0.1
        else:
            embedding_progress = 0.0
        
        if loading_metrics and loading_metrics.end_time:
            loading_progress = 1.0
        elif loading_metrics and loading_metrics.start_time:
            if loading_metrics.items_processed > 0:
                loading_progress = min(loading_metrics.items_succeeded / loading_metrics.items_processed, 1.0)
            else:
                loading_progress = 0.1
        else:
            loading_progress = 0.0
        
        return (
            collection_progress * 0.4 +
            processing_progress * 0.3 +
            embedding_progress * 0.2 +
            loading_progress * 0.1
        )

    async def _report_progress(
        self, stage: str, progress: float | None, stats: dict[str, Any], stages: dict[str, Any] | None = None
    ) -> None:
        """Report progress via callback if set.

        Args:
            stage: Current stage name
            progress: Overall progress (0.0-1.0), or None to calculate automatically
            stats: Pipeline statistics
            stages: Stage progress information, or None to build from metrics
        """
        if self._progress_callback:
            try:
                if progress is None:
                    progress = self._calculate_overall_progress(stats)
                if stages is None:
                    stages = self._build_stages_dict()
                await self._progress_callback(stage, progress, stats, stages)
            except Exception as e:
                logger.warning("Progress callback failed: %s", e)

    def _check_dependencies(self) -> None:
        """Check required dependencies and provide helpful error messages."""
        issues = []

        try:
            import playwright
            _ = playwright
        except ImportError:
            issues.append("Playwright not installed. Install: pip install playwright")
        else:
            logger.debug("Playwright package found (browser check will happen at runtime)")

        try:
            from docling.document_converter import DocumentConverter
            _ = DocumentConverter
            logger.info("Docling package found and importable")
        except ImportError:
            issues.append("Docling not installed. Install: pip install docling")
        except (AttributeError, RuntimeError, ValueError, TypeError) as e:
            issues.append(f"Docling import error: {e}. Try: pip install --upgrade docling")

        if issues:
            logger.warning("=" * 80)
            logger.warning("DEPENDENCY WARNINGS:")
            for issue in issues:
                logger.warning("  - %s", issue)
            logger.warning("=" * 80)
            logger.warning(
                "Some features may not work. Install missing dependencies to enable full functionality."
            )

    def _calculate_control_priority_score(self, control: dict[str, Any]) -> float:
        """Calculate priority score for a control to determine which to keep when limiting.
        
        Higher score = higher priority (keep this control).
        
        Args:
            control: Control dictionary
            
        Returns:
            Priority score (higher = better)
        """
        score = 0.0
        
        source_url = control.get("source_url", "")
        if not source_url:
            return score
        
        official_domains = [
            "pcisecuritystandards.org",
            "cisecurity.org",
            "hhs.gov",
            "aicpa.org",
            "nist.gov",
            "iso.org",
            "gdpr.eu",
            "fedramp.gov",
            "oag.ca.gov",
            "sec.gov",
            "ftc.gov",
        ]
        
        for domain in official_domains:
            if domain in source_url.lower():
                score += 100.0
                break
        
        if source_url.endswith(".pdf"):
            score += 20.0
        
        control_id = control.get("control_id", "")
        if control_id and len(control_id) > 5:
            score += 10.0
        
        title = control.get("title", "")
        if title and len(title) > 10:
            score += 10.0
        
        description = control.get("description", "")
        if description:
            desc_len = len(description)
            if desc_len > 100:
                score += 20.0
            elif desc_len > 50:
                score += 10.0
        
        remediation = control.get("remediation")
        if remediation:
            score += 15.0
        
        verification = control.get("verification")
        if verification:
            score += 15.0
        
        severity = control.get("severity", "").upper()
        severity_scores = {
            "CRITICAL": 30.0,
            "HIGH": 20.0,
            "MEDIUM": 10.0,
            "LOW": 5.0,
        }
        score += severity_scores.get(severity, 0.0)
        
        return score

    def _enforce_expected_controls_count(
        self, raw_controls: list[dict[str, Any]], standard: str, stats: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Enforce expected controls count by prioritizing and limiting controls.
        
        If more than expected: prioritize by quality and limit to expected count.
        If less than expected: log warning but use all available controls.
        If exactly expected: perfect match.
        
        Args:
            raw_controls: List of raw control dictionaries
            standard: Compliance standard name
            stats: Statistics dictionary to update
            
        Returns:
            List of controls (limited to expected count if over, all if under)
        """
        standard_config = COMPLIANCE_URLS.get(standard)
        if not standard_config:
            logger.debug("No config found for standard %s, skipping expected controls enforcement", standard)
            return raw_controls
        
        expected_count = standard_config.get("expected_controls")
        if expected_count is None:
            logger.debug("No expected_controls specified for standard %s", standard)
            return raw_controls
        
        collected_count = len(raw_controls)
        stats["expected_controls"] = expected_count
        stats["collected_before_enforcement"] = collected_count
        
        if collected_count == expected_count:
            logger.info(
                "✅ Perfect match for %s: Collected exactly %d controls (expected: %d)",
                standard, collected_count, expected_count
            )
            stats["enforcement_action"] = "none"
            return raw_controls
        
        if collected_count < expected_count:
            percentage = (collected_count / expected_count) * 100
            logger.warning(
                "⚠️ Collection incomplete for %s: Collected %d controls, expected %d (%.1f%% of expected). "
                "Using all available controls.",
                standard, collected_count, expected_count, percentage
            )
            stats["enforcement_action"] = "under_limit"
            stats["collection_percentage"] = percentage
            return raw_controls
        
        logger.info(
            "📊 Collected %d controls for %s, expected %d. Prioritizing and limiting to expected count.",
            collected_count, standard, expected_count
        )
        
        prioritized_controls = sorted(
            raw_controls,
            key=self._calculate_control_priority_score,
            reverse=True
        )
        
        limited_controls = prioritized_controls[:expected_count]
        removed_count = collected_count - expected_count
        
        logger.info(
            "✅ Limited %s controls from %d to %d (removed %d lower-priority controls)",
            standard, collected_count, expected_count, removed_count
        )
        
        stats["enforcement_action"] = "limited"
        stats["controls_removed"] = removed_count
        stats["collection_percentage"] = 100.0
        
        return limited_controls

    async def run_compliance_pipeline(
        self, 
        standard: str, 
        version: str = "latest", 
        run_collection: bool = True,
        max_urls: int | None = None,
        max_pdfs: int | None = None,
        max_controls: int | None = None,
    ) -> dict[str, Any]:
        """Run complete pipeline for a compliance standard.

        Full pipeline: Collection → Processing → Embedding → Loading

        Args:
            standard: Compliance standard name
            version: Standard version
            run_collection: If True, run collection stage first (default: True)

        Returns:
            Dictionary with pipeline results and statistics
        """
        max_urls = max_urls or self.config.max_urls
        max_pdfs = max_pdfs or self.config.max_pdfs
        max_controls = max_controls or self.config.max_controls
        
        logger.info("=" * 80)
        logger.info("Starting compliance pipeline for: %s (version: %s)", standard, version)
        logger.info("Mode: %s", self.config.mode)
        logger.info("Run Collection: %s", run_collection)
        if max_urls is not None:
            logger.info("Max URLs: %d", max_urls)
        if max_pdfs is not None:
            logger.info("Max PDFs: %d", max_pdfs)
        if max_controls is not None:
            logger.info("Max Controls: %d", max_controls)
        logger.info("=" * 80)

        correlation_id = get_correlation_id()
        
        with TracingContext("compliance_pipeline", standard=standard, version=version, correlation_id=correlation_id):
            stats = {
                "standard": standard,
                "version": version,
                "mode": self.config.mode,
                "collected": 0,
                "processed": 0,
                "embedded": 0,
                "loaded_mongodb": 0,
                "loaded_pinecone": 0,
                "skipped_source_unchanged": 0,
                "skipped_content_unchanged": 0,
                "llm_calls_saved": 0,
                "embedding_calls_saved": 0,
                "mongodb_inserted": 0,
                "mongodb_updated": 0,
                "mongodb_errors": 0,
                "pinecone_skipped": 0,
                "errors": [],
            }
            
            raw_controls = []

            try:
                if run_collection:
                    collection_metrics = self.metrics.start_stage("collection", "compliance")
                    try:
                        standard_mapping = {
                            "PCI-DSS": "pci-dss",
                            "CIS": "cis-aws",
                            "HIPAA": "hipaa",
                            "SOC2": "soc2",
                            "NIST-800-53": "nist-800-53",
                            "ISO-27001": "iso-27001",
                            "GDPR": "gdpr",
                            "FedRAMP": "fedramp",
                            "CCPA": "ccpa",
                            "SOX": "sox",
                            "GLBA": "glba",
                        }
                        standard_key = standard_mapping.get(standard, standard.lower().replace("_", "-"))
                        
                        disable_deep_crawl = (
                            self.config.disable_deep_crawl_when_limited 
                            and max_urls is not None
                        )
                        
                        if disable_deep_crawl:
                            logger.info(
                                "Deep crawling disabled because max_urls is set (%d) and disable_deep_crawl_when_limited=True",
                                max_urls
                            )
                        
                        async def progress_callback_wrapper(items: int, total: int) -> None:
                            """Wrapper to update collection progress asynchronously."""
                            self._update_collection_progress(items, stats)
                            await self._report_progress("collection", None, stats)
                        
                        raw_controls = await self.collector.collect_standard_async(
                            standard_key,
                            max_urls=max_urls,
                            max_pdfs=max_pdfs,
                            max_controls=max_controls,
                            progress_callback=progress_callback_wrapper,
                            disable_deep_crawl=disable_deep_crawl,
                        )
                        
                        from api.database.mongodb import mongodb_manager
                        pool_stats = mongodb_manager.monitor_connection_pool()
                        logger.debug("MongoDB pool stats after collection: %s", pool_stats)
                        
                        if max_controls is not None and len(raw_controls) > max_controls:
                            logger.info("Limiting controls to %d (collected %d)", max_controls, len(raw_controls))
                            raw_controls = raw_controls[:max_controls]
                        
                        raw_controls = self._enforce_expected_controls_count(raw_controls, standard, stats)
                        
                        stats["collected"] = len(raw_controls)

                        for control in raw_controls:
                            self.metrics.record_item_processed("collection", "compliance", success=True)

                        collection_metrics.items_processed = len(raw_controls)
                        collection_metrics.items_succeeded = len(raw_controls)
                        self.metrics.finish_stage("collection", "compliance")

                        logger.info("Collected %d raw controls for standard: %s", len(raw_controls), standard)

                        await self._report_progress("collection", None, stats)
                    except (ValueError, KeyError, AttributeError, RuntimeError) as e:
                        logger.error("Collection failed for standard %s: %s", standard, e)
                        stats["errors"].append({"stage": "collection", "error": str(e)})
                        self.metrics.record_error("collection", type(e).__name__, str(e))
                        self.metrics.finish_stage("collection", "compliance")

                if self.config.enable_change_detection and raw_controls:
                    if self.loader is None:
                        self.loader = MongoDBLoader()
                    if self.change_detector is None:
                        from api.database.mongodb import mongodb_manager
                        db = mongodb_manager.get_database()
                        self.change_detector = ChangeDetector(
                            db.compliance_controls,
                            enabled=self.config.enable_change_detection
                        )
                    
                    try:
                        existing_map = self.change_detector.batch_check_source_hashes(raw_controls)
                    except Exception as e:
                        logger.warning("Change detection failed unexpectedly: %s - processing all controls", e)
                        existing_map = {}
                    filtered_raw_controls = []
                    
                    for raw_control in raw_controls:
                        control_id = extract_control_id(raw_control)
                        if not control_id:
                            filtered_raw_controls.append(raw_control)
                            continue
                        
                        try:
                            from ..utils.change_detector import calculate_source_hash
                            source_hash = calculate_source_hash(raw_control)
                        except ValueError:
                            logger.warning("Failed to calculate source hash for control %s - processing anyway", control_id)
                            filtered_raw_controls.append(raw_control)
                            continue
                        
                        existing = existing_map.get(control_id)
                        if existing:
                            existing_source_hash = existing.get("source_hash")
                            if existing_source_hash and existing_source_hash == source_hash:
                                stats["skipped_source_unchanged"] += 1
                                stats["llm_calls_saved"] += 1
                                stats["embedding_calls_saved"] += 1
                                logger.debug("Skipping unchanged control: %s", control_id)
                                continue
                        
                        raw_control["_source_hash"] = source_hash
                        filtered_raw_controls.append(raw_control)
                    
                    if filtered_raw_controls:
                        logger.info(
                            "Change detection: Processing %d of %d controls (%d skipped)",
                            len(filtered_raw_controls),
                            len(raw_controls),
                            stats["skipped_source_unchanged"]
                        )
                        raw_controls = filtered_raw_controls
                    else:
                        logger.info("All controls unchanged - skipping processing")
                        for stage_name in ["processing", "embedding", "loading"]:
                            existing_metrics = self.metrics.get_stage_metrics(stage_name, "compliance")
                            if not existing_metrics or not existing_metrics.end_time:
                                stage_metrics = self.metrics.start_stage(stage_name, "compliance")
                                stage_metrics.items_processed = 0
                                stage_metrics.items_succeeded = 0
                                stage_metrics.items_failed = 0
                                self.metrics.finish_stage(stage_name, "compliance")
                        
                        final_stages = self._build_stages_dict()
                        await self._report_progress("collection", 1.0, stats, final_stages)
                        return stats
                else:
                    filtered_raw_controls = raw_controls if run_collection else []

                processing_metrics = self.metrics.start_stage("processing", "compliance")
                
                if self.config.enable_streaming_saves:
                    processed_controls, failed_processing, items_with_embeddings, failed_embedding = await self._process_embed_and_save_streaming(
                        standard, version, filtered_raw_controls if run_collection else []
                    )
                else:
                    processed_controls, failed_processing = await self.processor.process_standard_async(standard, version)
                    stats["processed"] = len(processed_controls)
                    stats["errors"].extend(failed_processing)

                    for control in processed_controls:
                        self.metrics.record_item_processed("processing", "compliance", success=True)

                    for failed in failed_processing:
                        self.metrics.record_item_processed("processing", "compliance", success=False)
                        self.metrics.record_error("processing", failed.get("error", "Unknown"), str(failed))

                    processing_metrics.items_processed = len(processed_controls) + len(failed_processing)
                    processing_metrics.items_succeeded = len(processed_controls)
                    processing_metrics.items_failed = len(failed_processing)
                    self.metrics.finish_stage("processing", "compliance")

                    await self._report_progress("processing", None, stats)

                    if not processed_controls:
                        logger.warning("No controls processed for standard: %s", standard)
                        return stats

                    embedding_metrics = self.metrics.start_stage("embedding", "compliance")
                    controls_dict = [control.model_dump(mode="json") for control in processed_controls]

                    if self.config.enable_change_detection and self.change_detector:
                        control_ids = [cd.get("control_id") for cd in controls_dict if cd.get("control_id")]
                        existing_map = {}
                        if control_ids and self.change_detector.collection is not None:
                            try:
                                existing_docs = self.change_detector.collection.find(
                                    {"control_id": {"$in": control_ids}},
                                    {"control_id": 1, "content_hash": 1}
                                )
                                existing_map = {doc["control_id"]: doc for doc in existing_docs}
                            except (ValueError, TypeError, KeyError, AttributeError, RuntimeError) as e:
                                logger.warning("Failed to batch check content hashes: %s - generating embeddings for all", e)
                        
                        filtered_for_embedding = []
                        for control_dict in controls_dict:
                            control_id = control_dict.get("control_id")
                            if not control_id:
                                filtered_for_embedding.append(control_dict)
                                continue
                            
                            try:
                                from ..utils.change_detector import calculate_content_hash
                                content_hash = calculate_content_hash(control_dict)
                            except ValueError:
                                logger.warning("Failed to calculate content hash for %s - generating embedding anyway", control_id)
                                filtered_for_embedding.append(control_dict)
                                continue
                            
                            existing_doc = existing_map.get(control_id)
                            if existing_doc:
                                existing_content_hash = existing_doc.get("content_hash")
                                if existing_content_hash and existing_content_hash == content_hash:
                                    stats["skipped_content_unchanged"] += 1
                                    stats["embedding_calls_saved"] += 1
                                    control_dict["_content_hash"] = content_hash
                                    logger.debug("Skipping embedding for unchanged content: %s", control_id)
                                    continue
                            
                            control_dict["_content_hash"] = content_hash
                            filtered_for_embedding.append(control_dict)
                        
                        if filtered_for_embedding:
                            logger.info(
                                "Change detection: Generating embeddings for %d of %d controls (%d skipped)",
                                len(filtered_for_embedding),
                                len(controls_dict),
                                stats["skipped_content_unchanged"]
                            )
                            controls_dict = filtered_for_embedding
                        else:
                            logger.info("All content unchanged - skipping embedding generation")
                            controls_dict = []

                    items_with_embeddings, failed_embedding = await self.embedder.generate_embeddings(
                        controls_dict, "compliance"
                    )
                    
                    stats["embedded"] = len(items_with_embeddings)
                    stats["errors"].extend(failed_embedding)

                    for _ in items_with_embeddings:
                        self.metrics.record_item_processed("embedding", "compliance", success=True)

                    for failed in failed_embedding:
                        self.metrics.record_item_processed("embedding", "compliance", success=False)
                        self.metrics.record_error("embedding", failed.get("error", "Unknown"), str(failed))

                    embedding_metrics.items_processed = len(items_with_embeddings) + len(failed_embedding)
                    embedding_metrics.items_succeeded = len(items_with_embeddings)
                    embedding_metrics.items_failed = len(failed_embedding)
                    self.metrics.finish_stage("embedding", "compliance")

                    await self._report_progress("embedding", None, stats)
                
                if self.config.enable_streaming_saves:
                    stats["processed"] = len(processed_controls)
                    stats["errors"].extend(failed_processing)
                    stats["embedded"] = len(items_with_embeddings)
                    stats["errors"].extend(failed_embedding)

                    for control in processed_controls:
                        self.metrics.record_item_processed("processing", "compliance", success=True)

                    for failed in failed_processing:
                        self.metrics.record_item_processed("processing", "compliance", success=False)
                        self.metrics.record_error("processing", failed.get("error", "Unknown"), str(failed))

                    processing_metrics.items_processed = len(processed_controls) + len(failed_processing)
                    processing_metrics.items_succeeded = len(processed_controls)
                    processing_metrics.items_failed = len(failed_processing)
                    self.metrics.finish_stage("processing", "compliance")

                    embedding_metrics = self.metrics.start_stage("embedding", "compliance")
                    
                    for _ in items_with_embeddings:
                        self.metrics.record_item_processed("embedding", "compliance", success=True)

                    for failed in failed_embedding:
                        self.metrics.record_item_processed("embedding", "compliance", success=False)
                        self.metrics.record_error("embedding", failed.get("error", "Unknown"), str(failed))

                    embedding_metrics.items_processed = len(items_with_embeddings) + len(failed_embedding)
                    embedding_metrics.items_succeeded = len(items_with_embeddings)
                    embedding_metrics.items_failed = len(failed_embedding)
                    self.metrics.finish_stage("embedding", "compliance")

                    await self._report_progress("embedding", None, stats)

                loading_metrics = self.metrics.start_stage("loading", "compliance")
                if self.loader is None:
                    self.loader = MongoDBLoader()
                
                if self.config.enable_streaming_saves:
                    logger.info("Streaming saves enabled - data already saved incrementally")
                    load_stats = {
                        "mongodb_inserted": self._streaming_stats.get("mongodb_inserted", 0),
                        "mongodb_updated": self._streaming_stats.get("mongodb_updated", 0),
                        "mongodb_errors": self._streaming_stats.get("mongodb_errors", 0),
                        "pinecone_loaded": self._streaming_stats.get("pinecone_loaded", 0),
                        "pinecone_skipped": self._streaming_stats.get("pinecone_skipped", 0),
                    }
                else:
                    if items_with_embeddings:
                        load_stats = self.loader.load_compliance_controls(items_with_embeddings)
                    else:
                        logger.warning(
                            "No controls with embeddings for standard: %s. "
                            "Loading controls to MongoDB without embeddings (Pinecone will be skipped).",
                            standard,
                        )
                        controls_dict = [control.model_dump(mode="json") for control in processed_controls]
                        for control in controls_dict:
                            control.pop("embedding", None)
                        load_stats = self.loader.load_compliance_controls(controls_dict)
                
                stats["loaded_mongodb"] = load_stats["mongodb_inserted"] + load_stats["mongodb_updated"]
                stats["loaded_pinecone"] = load_stats["pinecone_loaded"]
                stats["mongodb_errors"] = load_stats["mongodb_errors"]
                stats["pinecone_skipped"] = load_stats["pinecone_skipped"]

                self.metrics.record_item_processed("loading", "compliance", success=True)
                loading_metrics.items_processed = stats["loaded_mongodb"]
                loading_metrics.items_succeeded = stats["loaded_mongodb"]
                loading_metrics.items_failed = load_stats["mongodb_errors"]
                self.metrics.finish_stage("loading", "compliance")

                await self._report_progress("loading", None, stats)

                summary = self.metrics.get_summary()
                stats["metrics_summary"] = summary

                if self.config.enable_streaming_saves:
                    preserved_collected = stats.get("collected", 0)
                    preserved_processed = stats.get("processed", 0)
                    preserved_embedded = stats.get("embedded", 0)
                    preserved_errors = stats.get("errors", [])
                    
                    stats["mongodb_inserted"] = self._streaming_stats.get("mongodb_inserted", 0)
                    stats["mongodb_updated"] = self._streaming_stats.get("mongodb_updated", 0)
                    stats["mongodb_errors"] = self._streaming_stats.get("mongodb_errors", 0)
                    stats["pinecone_loaded"] = self._streaming_stats.get("pinecone_loaded", 0)
                    stats["pinecone_skipped"] = self._streaming_stats.get("pinecone_skipped", 0)
                    stats["skipped_content_unchanged"] = self._streaming_stats.get("skipped_content_unchanged", 0)
                    stats["embedding_calls_saved"] = self._streaming_stats.get("embedding_calls_saved", 0)
                    stats["loaded_mongodb"] = stats["mongodb_inserted"] + stats["mongodb_updated"]
                    
                    stats["collected"] = preserved_collected
                    stats["processed"] = preserved_processed
                    stats["embedded"] = preserved_embedded
                    stats["errors"] = preserved_errors
                
                logger.info("=" * 80)
                logger.info("Pipeline completed for: %s", standard)
                logger.info("Collected: %d, Processed: %d, Embedded: %d, Loaded: %d", 
                           stats["collected"], stats["processed"], stats["embedded"], stats["loaded_mongodb"])
                
                if stats["collected"] == 0 and stats.get("processed", 0) > 0:
                    logger.warning(
                        "Stats inconsistency detected: collected=0 but processed=%d. "
                        "This may indicate a stats tracking issue.",
                        stats.get("processed", 0)
                    )
                if self.config.enable_change_detection:
                    logger.info("Change Detection: Skipped %d (source), %d (content) - Saved %d LLM calls, %d embedding calls",
                               stats["skipped_source_unchanged"], stats["skipped_content_unchanged"],
                               stats["llm_calls_saved"], stats["embedding_calls_saved"])
                if self.config.enable_streaming_saves:
                    logger.info("Streaming Saves: MongoDB (%d inserted, %d updated), Pinecone (%d loaded)",
                               stats["mongodb_inserted"], stats["mongodb_updated"], stats["pinecone_loaded"])
                logger.info("Total Duration: %.2fs", summary["total_duration_seconds"])
                logger.info("=" * 80)

                final_stages = self._build_stages_dict()
                await self._report_progress("completed", 1.0, stats, final_stages)

                return stats

            except (ValueError, TypeError, KeyError, RuntimeError) as e:
                logger.error("Pipeline failed for standard %s: %s", standard, e, exc_info=True)
                stats["errors"].append({"stage": "pipeline", "error": str(e)})
                self.metrics.record_error("pipeline", type(e).__name__, str(e))
                return stats

    async def check_health(self) -> dict[str, Any]:
        """Perform health check on all pipeline components.

        Returns:
            Dictionary with health status
        """
        from ..loaders.pinecone_loader import PineconeLoader
        from api.database.mongodb import mongodb_manager
        from wistx_mcp.tools.lib.gemini_client import GeminiClient

        await self.health_check.check_mongodb(mongodb_manager)

        pinecone_loader = PineconeLoader()
        await self.health_check.check_pinecone(pinecone_loader)

        from ..utils.config import PipelineSettings
        pipeline_settings = PipelineSettings()
        gemini_client = GeminiClient(api_key=pipeline_settings.gemini_api_key)
        await self.health_check.check_gemini(gemini_client)

        return self.health_check.get_health_status()

    async def run_cost_data_pipeline(
        self,
        providers: list[str] | None = None,
        regions: list[str] | None = None,
        services: list[str] | None = None,
        run_collection: bool = True,
        max_providers: int | None = None,
        max_regions: int | None = None,
        max_services: int | None = None,
        max_records: int | None = None,
    ) -> dict[str, Any]:
        """Run complete pipeline for cost data.

        Full pipeline: Collection → Processing → Allocation → Context Generation → Embedding → Loading

        Args:
            providers: Optional list of providers (aws, gcp, azure)
            regions: Optional list of regions to collect
            services: Optional list of services to collect
            run_collection: If True, run collection stage first (default: True)
            max_providers: Maximum number of providers to process (None for all)
            max_regions: Maximum number of regions per provider (None for all)
            max_services: Maximum number of services per provider (None for all)
            max_records: Maximum number of cost records to process (None for all)

        Returns:
            Dictionary with pipeline results and statistics
        """
        logger.info("=" * 80)
        logger.info("Starting cost data pipeline")
        logger.info("Providers: %s", providers or "all")
        logger.info("Mode: %s", self.config.mode)
        logger.info("Run Collection: %s", run_collection)
        if max_providers:
            logger.info("Max Providers: %d", max_providers)
        if max_regions:
            logger.info("Max Regions: %d", max_regions)
        if max_services:
            logger.info("Max Services: %d", max_services)
        if max_records:
            logger.info("Max Records: %d", max_records)
        logger.info("=" * 80)

        correlation_id = get_correlation_id()

        with TracingContext("cost_data_pipeline", providers=providers, correlation_id=correlation_id):
            stats = {
                "providers": providers or ["aws", "gcp", "azure"],
                "mode": self.config.mode,
                "collected": 0,
                "processed": 0,
                "allocated": 0,
                "context_generated": 0,
                "embedded": 0,
                "loaded_mongodb": 0,
                "loaded_pinecone": 0,
                "mongodb_inserted": 0,
                "mongodb_updated": 0,
                "mongodb_errors": 0,
                "pinecone_skipped": 0,
                "skipped_source_unchanged": 0,
                "skipped_content_unchanged": 0,
                "errors": [],
            }

            raw_data_by_provider = {}

            try:
                if run_collection:
                    collection_metrics = self.metrics.start_stage("collection", "cost_data")
                    try:
                        cost_collector = CostDataCollector()
                        collection_results = await cost_collector.collect_all(
                            providers=providers,
                            regions=regions,
                            services=services,
                            max_providers=max_providers,
                            max_regions=max_regions,
                            max_services=max_services,
                            max_records=max_records,
                        )

                        for provider, result in collection_results.items():
                            if result.success:
                                raw_data_by_provider[provider] = result.items
                                stats["collected"] += len(result.items)
                            else:
                                error_messages = [e.get("message", "") for e in result.errors]
                                if any("API key not configured" in msg or "MissingAPIKey" in msg for msg in error_messages):
                                    logger.info("Skipping %s collection: API key not configured", provider)
                                else:
                                    logger.warning("Collection failed for %s: %s", provider, "; ".join(error_messages) or "Unknown error")
                                    stats["errors"].append({"stage": "collection", "provider": provider, "error": "; ".join(error_messages) or "Collection failed"})

                        collection_metrics.items_processed = stats["collected"]
                        collection_metrics.items_succeeded = stats["collected"]
                        self.metrics.finish_stage("collection", "cost_data")

                        logger.info("Collected %d raw cost records", stats["collected"])
                    except Exception as e:
                        logger.error("Collection failed: %s", e, exc_info=True)
                        stats["errors"].append({"stage": "collection", "error": str(e)})
                        self.metrics.record_error("collection", type(e).__name__, str(e))
                        self.metrics.finish_stage("collection", "cost_data")

                if not raw_data_by_provider:
                    logger.warning("No raw data collected, skipping processing")
                    return stats

                if self.loader is None:
                    self.loader = MongoDBLoader()

                cost_processor = CostDataProcessor()
                allocation_processor = CostAllocationProcessor()

                from api.services.context_generator import context_generator

                from ..models.cost_data import FOCUSCostData
                from ..utils.change_detector import calculate_source_hash, calculate_content_hash

                if self.config.enable_change_detection:
                    if self.change_detector is None:
                        from api.database.mongodb import mongodb_manager
                        db = mongodb_manager.get_database()
                        self.change_detector = ChangeDetector(
                            db.cost_data_focus,
                            enabled=self.config.enable_change_detection,
                        )

                processed_records = []

                for provider, raw_data_list in raw_data_by_provider.items():
                    try:
                        processing_metrics = self.metrics.start_stage("processing", "cost_data")
                        
                        if self.config.enable_change_detection and self.change_detector:
                            processed_records_cache = []
                            for raw_item in raw_data_list:
                                temp_record = cost_processor.process_raw_data(raw_item, provider)
                                if temp_record:
                                    processed_records_cache.append(temp_record)
                            
                            if processed_records_cache:
                                lookup_keys = [r.lookup_key for r in processed_records_cache]
                                try:
                                    existing_docs = self.change_detector.collection.find(
                                        {"lookup_key": {"$in": lookup_keys}},
                                        {"lookup_key": 1, "source_hash": 1, "content_hash": 1}
                                    )
                                    existing_map = {doc["lookup_key"]: doc for doc in existing_docs}
                                except Exception as e:
                                    logger.warning("Failed to check existing records: %s - processing all", e)
                                    existing_map = {}
                                
                                filtered_records = []
                                for record in processed_records_cache:
                                    record_dict = record.model_dump()
                                    source_hash = calculate_source_hash(record_dict)
                                    
                                    existing = existing_map.get(record.lookup_key)
                                    if existing and existing.get("source_hash") == source_hash:
                                        stats["skipped_source_unchanged"] += 1
                                        logger.debug("Skipping unchanged cost record: %s", record.lookup_key)
                                        continue
                                    
                                    filtered_records.append(record)
                                
                                cost_records = filtered_records
                                logger.info(
                                    "Change detection: %d unchanged records skipped, %d to process",
                                    stats["skipped_source_unchanged"],
                                    len(cost_records),
                                )
                            else:
                                cost_records = []
                        else:
                            cost_records = cost_processor.process_batch(raw_data_list, provider)
                        stats["processed"] += len(cost_records)
                        processing_metrics.items_processed = len(cost_records)
                        processing_metrics.items_succeeded = len(cost_records)
                        self.metrics.finish_stage("processing", "cost_data")

                        allocation_metrics = self.metrics.start_stage("allocation", "cost_data")
                        allocated_records = allocation_processor.allocate_batch(cost_records)
                        stats["allocated"] += len(allocated_records)
                        allocation_metrics.items_processed = len(allocated_records)
                        allocation_metrics.items_succeeded = len(allocated_records)
                        self.metrics.finish_stage("allocation", "cost_data")

                        context_metrics = self.metrics.start_stage("context_generation", "cost_data")
                        records_with_context = []
                        
                        if allocated_records:
                            max_concurrent = self.config.context_generation_concurrency
                            semaphore = asyncio.Semaphore(max_concurrent)
                            
                            async def generate_context_with_limit(record: FOCUSCostData) -> tuple[str | None, FOCUSCostData, str | None]:
                                """Generate context for a single record with concurrency limit.
                                
                                Returns:
                                    Tuple of (context, record, error_message)
                                """
                                async with semaphore:
                                    await asyncio.sleep(random.uniform(0.1, 0.3))
                                    
                                    try:
                                        context = await context_generator.generate_context_for_cost_data(record)
                                        return context, record, None
                                    except Exception as e:
                                        logger.error(
                                            "Failed to generate context for record %s: %s",
                                            record.lookup_key,
                                            e,
                                            exc_info=True,
                                        )
                                        return None, record, str(e)
                            
                            logger.info(
                                "Generating context for %d records with concurrency %d",
                                len(allocated_records),
                                max_concurrent,
                            )
                            
                            tasks = [generate_context_with_limit(record) for record in allocated_records]
                            results = await asyncio.gather(*tasks, return_exceptions=True)
                            
                            context_errors = []
                            for result in results:
                                if isinstance(result, Exception):
                                    logger.error("Unexpected error in context generation: %s", result, exc_info=True)
                                    context_errors.append({"error": str(result)})
                                    if self.config.context_generation_fail_fast:
                                        raise RuntimeError(f"Context generation failed: {result}") from result
                                    continue
                                
                                context, record, error = result
                                
                                if error:
                                    context_errors.append({
                                        "stage": "context_generation",
                                        "record": record.lookup_key,
                                        "error": error,
                                    })
                                    if self.config.context_generation_fail_fast:
                                        raise RuntimeError(f"Context generation failed for {record.lookup_key}: {error}")
                                    continue
                                
                                if context:
                                    record_dict = record.model_dump()
                                    record_dict["contextual_description"] = context
                                    records_with_context.append(FOCUSCostData(**record_dict))
                                    stats["context_generated"] += 1
                            
                            if context_errors:
                                stats["errors"].extend(context_errors)
                                logger.warning(
                                    "Context generation failed for %d/%d records",
                                    len(context_errors),
                                    len(allocated_records),
                                )
                            
                            logger.info(
                                "Generated context for %d/%d records",
                                stats["context_generated"],
                                len(allocated_records),
                            )
                        
                        context_metrics.items_processed = len(allocated_records)
                        context_metrics.items_succeeded = stats["context_generated"]
                        self.metrics.finish_stage("context_generation", "cost_data")

                        embedding_metrics = self.metrics.start_stage("embedding", "cost_data")
                        records_with_embeddings = []
                        
                        if not records_with_context:
                            logger.warning("No records with context generated, skipping embedding stage")
                            embedding_metrics.items_processed = 0
                            embedding_metrics.items_succeeded = 0
                            self.metrics.finish_stage("embedding", "cost_data")
                        else:
                            texts_to_embed = [record.to_searchable_text() for record in records_with_context]
                            embeddings = await self.embedder.generate_embeddings_batch(texts_to_embed)

                            if len(embeddings) != len(records_with_context):
                                logger.error(
                                    "Embedding count mismatch: %d records but %d embeddings. Truncating to match.",
                                    len(records_with_context),
                                    len(embeddings),
                                )
                                min_len = min(len(records_with_context), len(embeddings))
                                records_with_context = records_with_context[:min_len]
                                embeddings = embeddings[:min_len]

                            for record, embedding in zip(records_with_context, embeddings):
                                record_dict = record.model_dump_for_mongodb()
                                record_dict["embedding"] = embedding
                                records_with_embeddings.append(record_dict)
                                stats["embedded"] += 1

                            embedding_metrics.items_processed = len(records_with_embeddings)
                            embedding_metrics.items_succeeded = stats["embedded"]
                            self.metrics.finish_stage("embedding", "cost_data")

                        processed_records.extend(records_with_embeddings)

                    except Exception as e:
                        logger.error("Processing failed for %s: %s", provider, e, exc_info=True)
                        stats["errors"].append({"stage": "processing", "provider": provider, "error": str(e)})
                        continue

                if processed_records:
                    loading_metrics = self.metrics.start_stage("loading", "cost_data")
                    load_stats = self.loader.load_cost_data_focus(processed_records)
                    stats["loaded_mongodb"] = load_stats["mongodb_inserted"] + load_stats["mongodb_updated"]
                    stats["loaded_pinecone"] = load_stats["pinecone_loaded"]
                    stats["mongodb_inserted"] = load_stats["mongodb_inserted"]
                    stats["mongodb_updated"] = load_stats["mongodb_updated"]
                    stats["mongodb_errors"] = load_stats["mongodb_errors"]
                    stats["pinecone_skipped"] = load_stats["pinecone_skipped"]
                    loading_metrics.items_processed = len(processed_records)
                    loading_metrics.items_succeeded = stats["loaded_mongodb"]
                    self.metrics.finish_stage("loading", "cost_data")

                    logger.info(
                        "Cost data pipeline completed: Collected=%d, Processed=%d, "
                        "Allocated=%d, Context=%d, Embedded=%d, Loaded MongoDB=%d, Loaded Pinecone=%d",
                        stats["collected"],
                        stats["processed"],
                        stats["allocated"],
                        stats["context_generated"],
                        stats["embedded"],
                        stats["loaded_mongodb"],
                        stats["loaded_pinecone"],
                    )

            except Exception as e:
                logger.error("Cost data pipeline failed: %s", e, exc_info=True)
                stats["errors"].append({"stage": "pipeline", "error": str(e)})

            return stats

    async def run_all_standards(self) -> dict[str, dict[str, Any]]:
        """Run pipeline for all compliance standards.

        Dynamically discovers standards from configuration.

        Returns:
            Dictionary mapping standard names to pipeline results
        """
        from ..config.compliance_urls import COMPLIANCE_URLS
        
        standards = list(COMPLIANCE_URLS.keys())

        results = {}

        for standard in standards:
            try:
                result = await self.run_compliance_pipeline(standard)
                results[standard] = result
            except (ValueError, TypeError, KeyError, RuntimeError) as e:
                logger.error("Error running pipeline for %s: %s", standard, e)
                results[standard] = {"error": str(e)}

        return results

    async def run_single_standard(
        self, standard: str, version: str = "latest", run_collection: bool = True
    ) -> dict[str, Any]:
        """Run pipeline for a single compliance standard.

        Args:
            standard: Compliance standard name
            version: Standard version
            run_collection: If True, run collection stage first

        Returns:
            Pipeline results dictionary
        """
        return await self.run_compliance_pipeline(standard, version, run_collection=run_collection)

    def get_metrics_summary(self) -> dict[str, Any]:
        """Get metrics summary.

        Returns:
            Dictionary with metrics summary
        """
        return self.metrics.get_summary()

    async def _process_embed_and_save_streaming(
        self, standard: str, version: str, raw_controls: list[dict[str, Any]]
    ) -> tuple[list[Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
        """Process, embed, and save controls with high-performance parallel processing.

        This method processes controls in parallel batches: process → save → embed → save.
        Optimized for millions of URLs/PDFs with industry-standard concurrency.

        Args:
            standard: Compliance standard name
            version: Standard version
            raw_controls: List of raw control dictionaries (if available from collection)

        Returns:
            Tuple of (processed_controls, failed_processing, items_with_embeddings, failed_embedding)
        """
        if self.loader is None:
            self.loader = MongoDBLoader()

        self._streaming_stats = {
            "mongodb_inserted": 0,
            "mongodb_updated": 0,
            "mongodb_errors": 0,
            "pinecone_loaded": 0,
            "pinecone_skipped": 0,
            "skipped_content_unchanged": 0,
            "embedding_calls_saved": 0,
        }

        processed_controls = []
        failed_processing = []
        items_with_embeddings = []
        failed_embedding = []
        streaming_batch_size = self.config.streaming_batch_size
        embedding_batch_size = self.config.embedding_batch_size
        processing_concurrency = 20

        if raw_controls:
            raw_data = raw_controls.copy()
            logger.info("Using %d controls from collection - processing these first", len(raw_data))
        else:
            raw_data_result = await self.processor._load_raw_data_async(standard)  # noqa: SLF001
            raw_data = raw_data_result if isinstance(raw_data_result, list) else []
            logger.info("Loaded %d controls from JSON files", len(raw_data))

        logger.info("Processing %d web-collected controls with parallel processing (concurrency: %d)", len(raw_data), processing_concurrency)

        semaphore = asyncio.Semaphore(processing_concurrency)
        
        async def process_single_control(raw: dict[str, Any], index: int) -> tuple[Any | None, dict[str, Any] | None, dict[str, Any] | None]:
            """Process a single control with async MongoDB save."""
            async with semaphore:
                try:
                    control = self.processor.standardize_control(raw, standard, version)

                    if not self.processor.validate_control(control):
                        logger.warning("Validation failed for control: %s", raw.get("control_id", "unknown"))
                        return None, {"raw": raw, "error": "Validation failed"}, None

                    if not control.contextual_description:
                        try:
                            from api.services.context_generator import context_generator
                            from datetime import datetime
                            
                            contextual_description = await context_generator.generate_context_for_compliance_control(
                                control=control,
                            )
                            
                            control.contextual_description = contextual_description
                            control.context_generated_at = datetime.utcnow()
                            control.context_version = "1.0"
                        except Exception as e:
                            logger.error(
                                "Failed to generate contextual description for control %s: %s",
                                control.control_id,
                                e,
                                exc_info=True,
                            )
                            raise

                    doc = control.model_dump(mode="json")
                    source_hash = raw.get("_source_hash")
                    if source_hash:
                        doc["_source_hash"] = source_hash

                    control_id = doc.get("control_id", "unknown")
                    logger.debug("Saving control %d/%d: %s", index + 1, len(raw_data), control_id)
                    
                    success, action = await self.loader.save_single_control_async(doc)
                    if success:
                        if action == "inserted":
                            self._streaming_stats["mongodb_inserted"] = self._streaming_stats.get("mongodb_inserted", 0) + 1
                        else:
                            self._streaming_stats["mongodb_updated"] = self._streaming_stats.get("mongodb_updated", 0) + 1
                        
                        return control, None, doc
                    else:
                        logger.error("✗ Failed to save control to MongoDB: %s", control_id)
                        self._streaming_stats["mongodb_errors"] = self._streaming_stats.get("mongodb_errors", 0) + 1
                        return None, {"raw": raw, "error": "Failed to save to MongoDB"}, None

                except Exception as e:  # noqa: BLE001
                    logger.error("Error processing control %d/%d: %s", index + 1, len(raw_data), e, exc_info=True)
                    return None, {"raw": raw, "error": str(e)}, None
        
        tasks = [process_single_control(raw, i) for i, raw in enumerate(raw_data)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        if self.loader and hasattr(self.loader, "db") and hasattr(self.loader.db, "client"):
            from api.database.mongodb import mongodb_manager
            pool_stats = mongodb_manager.monitor_connection_pool()
            if pool_stats.get("health_status") in ("critical", "warning"):
                logger.warning("MongoDB pool stats during processing: %s", pool_stats)
        
        embedding_batch = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error("Error processing control %d/%d: %s", i + 1, len(raw_data), result, exc_info=True)
                failed_processing.append({"raw": raw_data[i] if i < len(raw_data) else {}, "error": str(result)})
                continue
            
            control, error, doc = result
            if error:
                failed_processing.append(error)
                continue
            
            if control and doc:
                processed_controls.append(control)
                embedding_batch.append(doc)
                
                if len(embedding_batch) >= embedding_batch_size or i == len(raw_data) - 1:
                    logger.debug("Processing embedding batch (size: %d)", len(embedding_batch))
                    batch_with_embeddings, batch_failed = await self._process_embedding_batch(
                        embedding_batch.copy(), []
                    )
                    items_with_embeddings.extend(batch_with_embeddings)
                    failed_embedding.extend(batch_failed)
                    embedding_batch.clear()
            
            if (i + 1) % streaming_batch_size == 0:
                logger.info("Progress: Processed and saved %d/%d controls (%d inserted, %d updated)", 
                           i + 1, len(raw_data),
                           self._streaming_stats.get("mongodb_inserted", 0),
                           self._streaming_stats.get("mongodb_updated", 0))

        logger.info("Completed processing %d web-collected controls. Now loading PDFs...", len(processed_controls))
        
        logger.info("Loading PDF controls for standard: %s...", standard)
        pdf_data = await self.processor._load_pdf_data_async(standard)
        if pdf_data:
            logger.info("Loaded %d controls from PDFs, processing now with parallel processing", len(pdf_data))
            
            pdf_tasks = [process_single_control(raw, i) for i, raw in enumerate(pdf_data)]
            pdf_results = await asyncio.gather(*pdf_tasks, return_exceptions=True)
            
            if self.loader and hasattr(self.loader, "db") and hasattr(self.loader.db, "client"):
                from api.database.mongodb import mongodb_manager
                pool_stats = mongodb_manager.monitor_connection_pool()
                if pool_stats.get("health_status") in ("critical", "warning"):
                    logger.warning("MongoDB pool stats during PDF processing: %s", pool_stats)
            
            for i, result in enumerate(pdf_results):
                if isinstance(result, Exception):
                    logger.error("Error processing PDF control %d/%d: %s", i + 1, len(pdf_data), result, exc_info=True)
                    failed_processing.append({"raw": pdf_data[i] if i < len(pdf_data) else {}, "error": str(result)})
                    continue
                
                control, error, doc = result
                if error:
                    failed_processing.append(error)
                    continue
                
                if control and doc:
                    processed_controls.append(control)
                    embedding_batch.append(doc)
                    
                    if len(embedding_batch) >= embedding_batch_size or i == len(pdf_data) - 1:
                        logger.debug("Processing PDF embedding batch (size: %d)", len(embedding_batch))
                        batch_with_embeddings, batch_failed = await self._process_embedding_batch(
                            embedding_batch.copy(), []
                        )
                        items_with_embeddings.extend(batch_with_embeddings)
                        failed_embedding.extend(batch_failed)
                        embedding_batch.clear()
        else:
            logger.debug("No PDF data found for standard: %s (PDF directory: %s)", standard, self.processor.pdf_dir)

        if not raw_data and not pdf_data:
            logger.warning("No raw data found for standard: %s", standard)
            return [], [], [], []

        logger.info("Processed %d controls with parallel processing, %d failed", len(processed_controls), len(failed_processing))
        logger.info("Generated embeddings for %d controls, %d failed", len(items_with_embeddings), len(failed_embedding))
        return processed_controls, failed_processing, items_with_embeddings, failed_embedding

    async def _process_embedding_batch(
        self, batch_dicts: list[dict[str, Any]], _batch_controls: list[Any]
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Process a batch of controls for embedding generation.

        Args:
            batch_dicts: List of control dictionaries
            _batch_controls: List of ComplianceControl objects (unused, kept for API compatibility)

        Returns:
            Tuple of (items_with_embeddings, failed_items)
        """
        if self.config.enable_change_detection and self.change_detector:
            control_ids = [cd.get("control_id") for cd in batch_dicts if cd.get("control_id")]
            existing_map = {}
            if control_ids and self.change_detector.collection is not None:
                try:
                    existing_docs = self.change_detector.collection.find(
                        {"control_id": {"$in": control_ids}},
                        {"control_id": 1, "content_hash": 1}
                    )
                    existing_map = {doc["control_id"]: doc for doc in existing_docs}
                except (ValueError, TypeError, KeyError, AttributeError, RuntimeError) as e:
                    logger.warning("Failed to batch check content hashes: %s - generating embeddings for all", e)
            
            filtered_for_embedding = []
            for control_dict in batch_dicts:
                control_id = control_dict.get("control_id")
                if not control_id:
                    filtered_for_embedding.append(control_dict)
                    continue
                
                try:
                    from ..utils.change_detector import calculate_content_hash
                    content_hash = calculate_content_hash(control_dict)
                except ValueError:
                    logger.warning("Failed to calculate content hash for %s - generating embedding anyway", control_id)
                    filtered_for_embedding.append(control_dict)
                    continue
                
                existing_doc = existing_map.get(control_id)
                if existing_doc:
                    existing_content_hash = existing_doc.get("content_hash")
                    if existing_content_hash and existing_content_hash == content_hash:
                        self._streaming_stats["skipped_content_unchanged"] = self._streaming_stats.get("skipped_content_unchanged", 0) + 1
                        self._streaming_stats["embedding_calls_saved"] = self._streaming_stats.get("embedding_calls_saved", 0) + 1
                        control_dict["_content_hash"] = content_hash
                        logger.debug("Skipping embedding for unchanged content: %s", control_id)
                        continue
                
                control_dict["_content_hash"] = content_hash
                filtered_for_embedding.append(control_dict)
            
            batch_dicts = filtered_for_embedding

        if not batch_dicts:
            return [], []

        batch_with_embeddings, batch_failed = await self.embedder.generate_embeddings(batch_dicts, "compliance")
        
        items_with_embeddings = []
        for item in batch_with_embeddings:
            control_id = item.get("control_id")
            if not control_id:
                continue

            embedding = item.get("embedding")
            content_hash = item.get("_content_hash")

            if embedding:
                await self.loader.update_control_embedding_streaming(control_id, embedding, content_hash)
                
                if self.loader.pinecone_loader:
                    success = self.loader.pinecone_loader.upsert_single_control(item)
                    if success:
                        self._streaming_stats["pinecone_loaded"] = self._streaming_stats.get("pinecone_loaded", 0) + 1

            items_with_embeddings.append(item)

        return items_with_embeddings, batch_failed

