"""Service for managing pipeline executions."""

import asyncio
import logging
from datetime import datetime
from typing import Any, Optional

from bson import ObjectId

from api.database.mongodb import mongodb_manager
from api.models.pipeline import (
    PipelineJob,
    PipelineStatus,
    PipelineType,
    StageProgress,
    StageStatus,
    generate_pipeline_id,
)
from api.utils.tracing import get_correlation_id

logger = logging.getLogger(__name__)


class PipelineExecutionService:
    """Service for managing pipeline executions."""

    def __init__(self):
        """Initialize pipeline execution service."""
        self._db = None
        self._max_concurrent = 3
        self._max_batch_size = 1000
        self._rate_limit_per_hour = 10
        self._pipeline_timeout_hours = 24
        self._running_pipelines: dict[str, asyncio.Task] = {}

    def _get_db(self):
        """Get MongoDB database instance."""
        if self._db is None:
            self._db = mongodb_manager.get_database()
        return self._db

    async def trigger_pipeline(
        self,
        pipeline_type: PipelineType,
        request: dict[str, Any],
        user_id: str,
        priority: int = 5,
    ) -> PipelineJob:
        """Trigger a pipeline execution.

        Args:
            pipeline_type: Type of pipeline to execute
            request: Pipeline request parameters
            user_id: User ID who triggered the pipeline
            priority: Pipeline priority (1-10)

        Returns:
            Created PipelineJob

        Raises:
            ValueError: If resource limits exceeded
        """
        config = await self.get_configuration()
        max_concurrent = config.get("max_concurrent_pipelines", self._max_concurrent)

        from api.exceptions import ValidationError
        
        running_count = await self._get_running_count()
        if running_count >= max_concurrent:
            raise ValidationError(
                message=f"Maximum concurrent pipelines ({max_concurrent}) reached",
                user_message=f"Maximum concurrent pipelines ({max_concurrent}) reached. Please wait for a pipeline to complete.",
                error_code="MAX_CONCURRENT_PIPELINES_REACHED",
                details={"max_concurrent": max_concurrent, "running_count": running_count}
            )

        pipeline_id = generate_pipeline_id()
        correlation_id = get_correlation_id()

        job = PipelineJob(
            pipeline_id=pipeline_id,
            pipeline_type=pipeline_type,
            user_id=user_id,
            status=PipelineStatus.PENDING,
            priority=priority,
            request=request,
            correlation_id=correlation_id,
        )

        db = self._get_db()
        collection = db.pipeline_jobs

        job_dict = job.to_dict()
        collection.insert_one(job_dict)

        logger.info(
            "Pipeline job created: %s (type: %s, priority: %d)",
            pipeline_id,
            pipeline_type.value,
            priority,
        )

        asyncio.create_task(self._execute_pipeline(job))

        return job

    async def recover_stale_pipelines(self, stale_threshold_minutes: int = 5) -> int:
        """Recover stale running pipelines (e.g., from server restart).

        Args:
            stale_threshold_minutes: Minutes after which a running pipeline is considered stale

        Returns:
            Number of pipelines recovered
        """
        from datetime import timedelta

        db = self._get_db()
        collection = db.pipeline_jobs

        threshold = datetime.utcnow() - timedelta(minutes=stale_threshold_minutes)

        stale_pipelines = list(
            collection.find(
                {
                    "status": PipelineStatus.RUNNING.value,
                    "started_at": {"$lt": threshold},
                }
            )
        )

        if not stale_pipelines:
            return 0

        for pipeline_doc in stale_pipelines:
            pipeline_id = pipeline_doc["_id"]
            last_progress = pipeline_doc.get("progress", 0.0)
            current_stage = pipeline_doc.get("current_stage")
            last_stages = pipeline_doc.get("stages", {})

            collection.update_one(
                {"_id": pipeline_id},
                {
                    "$set": {
                        "status": PipelineStatus.FAILED.value,
                        "completed_at": datetime.utcnow(),
                        "error": "Pipeline execution interrupted by server restart or crash",
                        "error_details": {
                            "error_type": "ServerRestart",
                            "recovery": True,
                            "stale_threshold_minutes": stale_threshold_minutes,
                            "last_progress": last_progress,
                            "last_stage": current_stage,
                        },
                        "resource_acquired": False,
                    }
                },
            )

        recovered = len(stale_pipelines)
        if recovered > 0:
            logger.info("Recovered %d stale pipelines (marked as FAILED)", recovered)

        return recovered

    async def cleanup_on_shutdown(self) -> int:
        """Cancel all running pipelines on graceful shutdown.

        Returns:
            Number of pipelines cancelled
        """
        cancelled_count = 0

        for pipeline_id, task in list(self._running_pipelines.items()):
            try:
                task.cancel()
                cancelled_count += 1
            except Exception as e:
                logger.warning("Error cancelling pipeline %s: %s", pipeline_id, e)

        if cancelled_count > 0:
            db = self._get_db()
            collection = db.pipeline_jobs

            result = collection.update_many(
                {
                    "_id": {"$in": list(self._running_pipelines.keys())},
                    "status": PipelineStatus.RUNNING.value,
                },
                {
                    "$set": {
                        "status": PipelineStatus.CANCELLED.value,
                        "completed_at": datetime.utcnow(),
                        "error": "Pipeline cancelled due to server shutdown",
                        "resource_acquired": False,
                    }
                },
            )

            cancelled_count = result.modified_count
            logger.info("Cancelled %d pipelines on shutdown", cancelled_count)

        self._running_pipelines.clear()
        return cancelled_count

    async def check_stuck_pipelines(self, no_progress_threshold_minutes: int = 30) -> int:
        """Check for stuck pipelines with no progress updates.

        Args:
            no_progress_threshold_minutes: Minutes without progress update to consider stuck

        Returns:
            Number of stuck pipelines detected
        """
        from datetime import timedelta

        db = self._get_db()
        collection = db.pipeline_jobs

        threshold = datetime.utcnow() - timedelta(minutes=no_progress_threshold_minutes)

        stuck_pipelines = list(
            collection.find(
                {
                    "status": PipelineStatus.RUNNING.value,
                    "$or": [
                        {"last_progress_update": {"$lt": threshold}},
                        {"last_progress_update": {"$exists": False}, "started_at": {"$lt": threshold}},
                    ],
                }
            )
        )

        if not stuck_pipelines:
            return 0

        for pipeline_doc in stuck_pipelines:
            pipeline_id = pipeline_doc["_id"]
            last_progress = pipeline_doc.get("progress", 0.0)
            current_stage = pipeline_doc.get("current_stage")

            collection.update_one(
                {"_id": pipeline_id},
                {
                    "$set": {
                        "status": PipelineStatus.FAILED.value,
                        "completed_at": datetime.utcnow(),
                        "error": f"Pipeline appears stuck (no progress for {no_progress_threshold_minutes} minutes)",
                        "error_details": {
                            "error_type": "StuckPipeline",
                            "last_progress": last_progress,
                            "last_stage": current_stage,
                            "no_progress_threshold_minutes": no_progress_threshold_minutes,
                        },
                        "resource_acquired": False,
                    }
                },
            )

            if pipeline_id in self._running_pipelines:
                task = self._running_pipelines[pipeline_id]
                try:
                    task.cancel()
                except Exception:
                    pass
                del self._running_pipelines[pipeline_id]

        stuck_count = len(stuck_pipelines)
        if stuck_count > 0:
            logger.warning("Detected %d stuck pipelines", stuck_count)

        return stuck_count

    async def get_pipeline(self, pipeline_id: str) -> Optional[PipelineJob]:
        """Get pipeline job by ID.

        Args:
            pipeline_id: Pipeline ID

        Returns:
            PipelineJob or None if not found
        """
        db = self._get_db()
        collection = db.pipeline_jobs

        doc = collection.find_one({"_id": pipeline_id})
        if not doc:
            return None

        return PipelineJob.from_dict(doc)

    async def list_pipelines(
        self,
        status: Optional[PipelineStatus] = None,
        pipeline_type: Optional[PipelineType] = None,
        user_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[PipelineJob], int]:
        """List pipeline jobs.

        Args:
            status: Filter by status
            pipeline_type: Filter by pipeline type
            user_id: Filter by user ID
            limit: Maximum number of results
            offset: Offset for pagination

        Returns:
            Tuple of (pipelines list, total count)
        """
        db = self._get_db()
        collection = db.pipeline_jobs

        query: dict[str, Any] = {}
        if status:
            query["status"] = status.value
        if pipeline_type:
            query["pipeline_type"] = pipeline_type.value
        if user_id:
            query["user_id"] = ObjectId(user_id) if user_id else None

        total = collection.count_documents(query)

        cursor = (
            collection.find(query)
            .sort("created_at", -1)
            .skip(offset)
            .limit(limit)
        )

        pipelines = [PipelineJob.from_dict(doc) for doc in cursor]

        return pipelines, total

    async def cancel_pipeline(self, pipeline_id: str) -> bool:
        """Cancel a running pipeline.

        Args:
            pipeline_id: Pipeline ID

        Returns:
            True if cancelled, False if not found or already completed
        """
        db = self._get_db()
        collection = db.pipeline_jobs

        job = await self.get_pipeline(pipeline_id)
        if not job:
            return False

        if job.status in (PipelineStatus.COMPLETED, PipelineStatus.FAILED, PipelineStatus.CANCELLED):
            return False

        collection.update_one(
            {"_id": pipeline_id},
            {
                "$set": {
                    "status": PipelineStatus.CANCELLED.value,
                    "completed_at": datetime.utcnow(),
                }
            },
        )

        if pipeline_id in self._running_pipelines:
            task = self._running_pipelines[pipeline_id]
            task.cancel()
            del self._running_pipelines[pipeline_id]

        logger.info("Pipeline cancelled: %s", pipeline_id)
        return True

    async def _get_running_count(self) -> int:
        """Get count of currently running pipelines.

        Returns:
            Number of running pipelines
        """
        db = self._get_db()
        collection = db.pipeline_jobs

        return collection.count_documents({"status": PipelineStatus.RUNNING.value})

    async def _update_pipeline_progress(
        self,
        pipeline_id: str,
        progress: float | None = None,
        current_stage: str | None = None,
        stats: dict[str, Any] | None = None,
        stages: dict[str, Any] | None = None,
    ) -> None:
        """Update pipeline progress in database.

        Args:
            pipeline_id: Pipeline ID
            progress: Overall progress (0.0-1.0)
            current_stage: Current stage name
            stats: Pipeline statistics
            stages: Stage progress information
        """
        from api.models.pipeline import PipelineStats, StageProgress, StageStatus

        db = self._get_db()
        collection = db.pipeline_jobs

        update_data: dict[str, Any] = {}
        if progress is not None:
            update_data["progress"] = progress
        if current_stage is not None:
            update_data["current_stage"] = current_stage
        if stats is not None:
            formatted_stats = PipelineStats(
                collected=stats.get("collected", 0),
                processed=stats.get("processed", 0),
                embedded=stats.get("embedded", 0),
                loaded=stats.get("loaded_mongodb", 0) + stats.get("loaded_pinecone", 0),
                errors=[{"stage": e.get("stage", "unknown"), "error": str(e.get("error", ""))} for e in stats.get("errors", [])],
                skipped_source_unchanged=stats.get("skipped_source_unchanged", 0),
                skipped_content_unchanged=stats.get("skipped_content_unchanged", 0),
                llm_calls_saved=stats.get("llm_calls_saved", 0),
                embedding_calls_saved=stats.get("embedding_calls_saved", 0),
                context_generated=stats.get("context_generated", 0),
                loaded_mongodb=stats.get("loaded_mongodb", 0),
                loaded_pinecone=stats.get("loaded_pinecone", 0),
                allocated=stats.get("allocated", 0),
            )
            update_data["stats"] = formatted_stats.model_dump()
        if stages is not None:
            formatted_stages = {}
            for stage_name, stage_data in stages.items():
                formatted_stages[stage_name] = StageProgress(
                    stage_name=stage_data.get("stage_name", stage_name),
                    status=StageStatus(stage_data.get("status", "pending")),
                    items_processed=stage_data.get("items_processed", 0),
                    items_succeeded=stage_data.get("items_succeeded", 0),
                    items_failed=stage_data.get("items_failed", 0),
                    duration_seconds=stage_data.get("duration_seconds"),
                    progress_percentage=stage_data.get("progress_percentage", 0.0),
                ).model_dump()
            update_data["stages"] = formatted_stages

        if update_data:
            update_data["last_progress_update"] = datetime.utcnow()
            collection.update_one({"_id": pipeline_id}, {"$set": update_data})

    async def _execute_pipeline(self, job: PipelineJob) -> None:
        """Execute a pipeline (background task).

        Args:
            job: Pipeline job to execute
        """
        pipeline_id = job.pipeline_id
        self._running_pipelines[pipeline_id] = asyncio.current_task()

        try:
            db = self._get_db()
            collection = db.pipeline_jobs

            config = await self.get_configuration()
            timeout_hours = config.get("pipeline_timeout_hours", self._pipeline_timeout_hours)

            collection.update_one(
                {"_id": pipeline_id},
                {
                    "$set": {
                        "status": PipelineStatus.RUNNING.value,
                        "started_at": datetime.utcnow(),
                        "resource_acquired": True,
                        "last_progress_update": datetime.utcnow(),
                    }
                },
            )

            logger.info("Starting pipeline execution: %s (type: %s, timeout: %d hours)", pipeline_id, job.pipeline_type.value, timeout_hours)

            try:
                result = await asyncio.wait_for(
                    self._run_pipeline(job, pipeline_id),
                    timeout=timeout_hours * 3600,
                )
            except asyncio.TimeoutError:
                logger.error("Pipeline %s exceeded timeout of %d hours", pipeline_id, timeout_hours)
                collection.update_one(
                    {"_id": pipeline_id},
                    {
                        "$set": {
                            "status": PipelineStatus.FAILED.value,
                            "completed_at": datetime.utcnow(),
                            "error": f"Pipeline exceeded maximum execution time ({timeout_hours} hours)",
                            "error_details": {
                                "error_type": "Timeout",
                                "timeout_hours": timeout_hours,
                            },
                            "resource_acquired": False,
                        }
                    },
                )
                return

            final_stats = result.get("stats", {})
            final_stages = result.get("stages", {})
            
            final_progress = 1.0
            if final_stages:
                completed_count = sum(1 for s in final_stages.values() if s.get("status") == "completed")
                total_stages = len(final_stages)
                if total_stages > 0:
                    final_progress = min(completed_count / total_stages, 1.0)

            pipeline_failed = self._validate_pipeline_success(job.pipeline_type, final_stats, final_stages)
            
            if pipeline_failed:
                error_msg = self._build_failure_message(job.pipeline_type, final_stats)
                collection.update_one(
                    {"_id": pipeline_id},
                    {
                        "$set": {
                            "status": PipelineStatus.FAILED.value,
                            "completed_at": datetime.utcnow(),
                            "progress": final_progress,
                            "overall_progress_percentage": final_progress * 100,
                            "stats": final_stats,
                            "stages": final_stages,
                            "error": error_msg,
                            "error_details": {
                                "error_type": "CriticalStageFailure",
                                "validation_failed": True,
                            },
                        }
                    },
                )
                logger.warning("Pipeline failed validation: %s - %s", pipeline_id, error_msg)
            else:
                collection.update_one(
                    {"_id": pipeline_id},
                    {
                        "$set": {
                            "status": PipelineStatus.COMPLETED.value,
                            "completed_at": datetime.utcnow(),
                            "progress": final_progress,
                            "overall_progress_percentage": final_progress * 100,
                            "stats": final_stats,
                            "stages": final_stages,
                        }
                    },
                )
                logger.info("Pipeline completed: %s", pipeline_id)

        except asyncio.CancelledError:
            logger.info("Pipeline execution cancelled: %s", pipeline_id)
            db = self._get_db()
            collection = db.pipeline_jobs
            collection.update_one(
                {"_id": pipeline_id},
                {
                    "$set": {
                        "status": PipelineStatus.CANCELLED.value,
                        "completed_at": datetime.utcnow(),
                    }
                },
            )

        except Exception as e:
            logger.error("Pipeline execution failed: %s - %s", pipeline_id, e, exc_info=True)
            db = self._get_db()
            collection = db.pipeline_jobs
            collection.update_one(
                {"_id": pipeline_id},
                {
                    "$set": {
                        "status": PipelineStatus.FAILED.value,
                        "completed_at": datetime.utcnow(),
                        "error": str(e),
                        "error_details": {"error_type": type(e).__name__},
                    }
                },
            )

        finally:
            if pipeline_id in self._running_pipelines:
                del self._running_pipelines[pipeline_id]

    async def _run_pipeline(self, job: PipelineJob, pipeline_id: str) -> dict[str, Any]:
        """Run the actual pipeline based on type.

        Args:
            job: Pipeline job
            pipeline_id: Pipeline ID for progress updates

        Returns:
            Pipeline execution results
        """
        pipeline_type = job.pipeline_type
        request = job.request

        if pipeline_type == PipelineType.COMPLIANCE:
            return await self._run_compliance_pipeline(request, pipeline_id)
        elif pipeline_type == PipelineType.COST_DATA:
            return await self._run_cost_data_pipeline(request, pipeline_id)
        elif pipeline_type == PipelineType.CODE_EXAMPLES:
            return await self._run_code_examples_pipeline(request, pipeline_id)
        elif pipeline_type == PipelineType.KNOWLEDGE:
            return await self._run_knowledge_pipeline(request, pipeline_id)
        else:
            from api.exceptions import ValidationError
            raise ValidationError(
                message=f"Unknown pipeline type: {pipeline_type}",
                user_message=f"Unknown pipeline type: {pipeline_type}",
                error_code="UNKNOWN_PIPELINE_TYPE",
                details={"pipeline_type": pipeline_type}
            )

    async def _run_compliance_pipeline(
        self, request: dict[str, Any], pipeline_id: str
    ) -> dict[str, Any]:
        """Run compliance pipeline.

        Args:
            request: Pipeline request parameters
            pipeline_id: Pipeline ID for progress updates

        Returns:
            Pipeline execution results
        """
        from data_pipelines.processors.pipeline_orchestrator import (
            PipelineConfig,
            PipelineOrchestrator,
        )

        standard = request.get("standard")
        version = request.get("version", "latest")
        run_collection = request.get("run_collection", True)
        enable_change_detection = request.get("enable_change_detection", True)
        enable_streaming_saves = request.get("enable_streaming_saves", True)
        streaming_batch_size = request.get("streaming_batch_size", 10)
        embedding_batch_size = request.get("embedding_batch_size", 20)
        max_urls = request.get("max_urls")
        max_pdfs = request.get("max_pdfs")
        max_controls = request.get("max_controls")
        disable_deep_crawl_when_limited = request.get("disable_deep_crawl_when_limited", False)

        config = PipelineConfig(
            mode="streaming",
            enable_change_detection=enable_change_detection,
            enable_streaming_saves=enable_streaming_saves,
            streaming_batch_size=streaming_batch_size,
            embedding_batch_size=embedding_batch_size,
            max_urls=max_urls,
            max_pdfs=max_pdfs,
            max_controls=max_controls,
            disable_deep_crawl_when_limited=disable_deep_crawl_when_limited,
        )

        orchestrator = PipelineOrchestrator(config)

        async def progress_callback(stage: str, progress: float, stats: dict[str, Any], stages: dict[str, Any]) -> None:
            """Callback to update pipeline progress."""
            await self._update_pipeline_progress(
                pipeline_id=pipeline_id,
                progress=progress,
                current_stage=stage,
                stats=stats,
                stages=stages,
            )

        orchestrator.set_progress_callback(progress_callback)

        if standard:
            result = await orchestrator.run_compliance_pipeline(
                standard=standard,
                version=version,
                run_collection=run_collection,
                max_urls=max_urls,
                max_pdfs=max_pdfs,
                max_controls=max_controls,
            )
        else:
            result = await orchestrator.run_all_standards()

        formatted_result = self._format_pipeline_result(result)
        formatted_result["stages"] = orchestrator._build_stages_dict()
        return formatted_result

    async def _run_cost_data_pipeline(
        self, request: dict[str, Any], pipeline_id: str
    ) -> dict[str, Any]:
        """Run cost data pipeline.

        Args:
            request: Pipeline request parameters
            pipeline_id: Pipeline ID for progress updates

        Returns:
            Pipeline execution results
        """
        from data_pipelines.processors.pipeline_orchestrator import (
            PipelineConfig,
            PipelineOrchestrator,
        )

        providers = request.get("providers")
        regions = request.get("regions")
        services = request.get("services")
        run_collection = request.get("run_collection", True)
        enable_change_detection = request.get("enable_change_detection", True)
        enable_streaming_saves = request.get("enable_streaming_saves", True)
        max_providers = request.get("max_providers")
        max_regions = request.get("max_regions")
        max_services = request.get("max_services")
        max_records = request.get("max_records")

        config = PipelineConfig(
            mode="streaming",
            enable_change_detection=enable_change_detection,
            enable_streaming_saves=enable_streaming_saves,
        )

        orchestrator = PipelineOrchestrator(config)

        async def progress_callback(stage: str, progress: float, stats: dict[str, Any], stages: dict[str, Any]) -> None:
            """Callback to update pipeline progress."""
            await self._update_pipeline_progress(
                pipeline_id=pipeline_id,
                progress=progress,
                current_stage=stage,
                stats=stats,
                stages=stages,
            )

        orchestrator.set_progress_callback(progress_callback)

        result = await orchestrator.run_cost_data_pipeline(
            providers=providers,
            regions=regions,
            services=services,
            run_collection=run_collection,
            max_providers=max_providers,
            max_regions=max_regions,
            max_services=max_services,
            max_records=max_records,
        )

        return self._format_pipeline_result(result)

    async def _run_code_examples_pipeline(
        self, request: dict[str, Any], pipeline_id: str
    ) -> dict[str, Any]:
        """Run code examples pipeline.

        Args:
            request: Pipeline request parameters
            pipeline_id: Pipeline ID for progress updates

        Returns:
            Pipeline execution results
        """
        from data_pipelines.orchestration.code_examples_pipeline import CodeExamplesPipeline

        max_examples = request.get("max_examples")
        max_repos = request.get("max_repos")
        max_files = request.get("max_files")
        min_stars = request.get("min_stars")

        pipeline = CodeExamplesPipeline(
            min_stars=min_stars,
            max_repos=max_repos,
            max_files=max_files,
        )
        
        async def progress_callback(stage: str, progress: float, stats: dict[str, Any], stages: dict[str, Any]) -> None:
            """Callback to update pipeline progress."""
            await self._update_pipeline_progress(
                pipeline_id=pipeline_id,
                progress=progress,
                current_stage=stage,
                stats=stats,
                stages=stages,
            )
        
        pipeline.set_progress_callback(progress_callback)
        result = await pipeline.run_pipeline(max_examples=max_examples)

        return self._format_pipeline_result(result)

    async def _run_knowledge_pipeline(
        self, request: dict[str, Any], pipeline_id: str
    ) -> dict[str, Any]:
        """Run knowledge pipeline.

        Args:
            request: Pipeline request parameters
            pipeline_id: Pipeline ID for progress updates

        Returns:
            Pipeline execution results
        """
        from data_pipelines.processors.knowledge_pipeline_orchestrator import (
            KnowledgePipelineOrchestrator,
        )

        domain = request.get("domain")
        subdomain = request.get("subdomain")
        run_collection = request.get("run_collection", True)
        enable_change_detection = request.get("enable_change_detection", True)
        max_concurrent = request.get("max_concurrent")  # None uses config default
        max_urls = request.get("max_urls")
        max_pdfs = request.get("max_pdfs")
        max_docs = request.get("max_docs")
        max_articles = request.get("max_articles")
        disable_deep_crawl_when_limited = request.get("disable_deep_crawl_when_limited", False)

        from api.exceptions import ValidationError
        if not domain:
            raise ValidationError(
                message="Domain is required for knowledge pipeline",
                user_message="Domain is required for knowledge pipeline",
                error_code="MISSING_DOMAIN",
                details={"pipeline_type": "knowledge"}
            )

        domain = domain.strip().lower()
        
        ALL_SUPPORTED_DOMAINS = {
            "compliance", "finops", "devops", "security", "infrastructure",
            "architecture", "cloud", "automation", "platform", "sre"
        }
        
        if domain in ("all", "*"):
            domains = sorted(list(ALL_SUPPORTED_DOMAINS))
            logger.info("Processing all %d supported domains: %s", len(domains), ", ".join(domains))
        else:
            domains = [d.strip().lower() for d in domain.split(",") if d.strip()]

        from api.exceptions import ValidationError
        if not domains:
            raise ValidationError(
                message="At least one domain is required for knowledge pipeline",
                user_message="At least one domain is required for knowledge pipeline",
                error_code="MISSING_DOMAINS",
                details={"pipeline_type": "knowledge"}
            )

        invalid_domains = [d for d in domains if d not in ALL_SUPPORTED_DOMAINS]
        if invalid_domains:
            raise ValidationError(
                message=f"Invalid domain(s): {', '.join(invalid_domains)}",
                user_message=f"Invalid domain(s): {', '.join(invalid_domains)}. Supported domains: {', '.join(sorted(ALL_SUPPORTED_DOMAINS))} (or use 'all' to process all domains)",
                error_code="INVALID_DOMAINS",
                details={"invalid_domains": invalid_domains, "supported_domains": sorted(ALL_SUPPORTED_DOMAINS)}
            )

        use_paginated_collection = request.get("use_paginated_collection")
        use_streaming_pipeline = request.get("use_streaming_pipeline")
        collection_batch_size = request.get("collection_batch_size")
        enable_checkpointing = request.get("enable_checkpointing")
        checkpoint_interval = request.get("checkpoint_interval")
        pipeline_id = request.get("pipeline_id")
        resume_from_checkpoint = request.get("resume_from_checkpoint", False)
        
        config = {"enable_change_detection": enable_change_detection}
        if use_paginated_collection is not None:
            config["use_paginated_collection"] = use_paginated_collection
        if use_streaming_pipeline is not None:
            config["use_streaming_pipeline"] = use_streaming_pipeline
        if collection_batch_size is not None:
            config["collection_batch_size"] = collection_batch_size
        if enable_checkpointing is not None:
            config["enable_checkpointing"] = enable_checkpointing
        if checkpoint_interval is not None:
            config["checkpoint_interval"] = checkpoint_interval
        
        orchestrator = KnowledgePipelineOrchestrator(config)

        if len(domains) == 1:
            result = await orchestrator.run_knowledge_pipeline(
                domain=domains[0],
                subdomain=subdomain,
                run_collection=run_collection,
                max_urls=max_urls,
                max_pdfs=max_pdfs,
                max_docs=max_docs,
                max_articles=max_articles,
                max_concurrent=max_concurrent,
                disable_deep_crawl_when_limited=disable_deep_crawl_when_limited,
                pipeline_id=pipeline_id,
                resume_from_checkpoint=resume_from_checkpoint,
            )
        else:
            logger.info("Processing %d domains in parallel: %s", len(domains), ", ".join(domains))
            
            async def process_domain(domain_item: str) -> tuple[str, dict[str, Any] | Exception]:
                """Process a single domain and return domain name with result or exception.
                
                Args:
                    domain_item: Domain to process
                    
                Returns:
                    Tuple of (domain_name, result_dict_or_exception)
                """
                domain_orchestrator = KnowledgePipelineOrchestrator(config)
                try:
                    logger.info("Starting parallel processing for domain: %s", domain_item)
                    domain_result = await domain_orchestrator.run_knowledge_pipeline(
                        domain=domain_item,
                        subdomain=subdomain,
                        run_collection=run_collection,
                        max_urls=max_urls,
                        max_pdfs=max_pdfs,
                        max_docs=max_docs,
                        max_articles=max_articles,
                        max_concurrent=max_concurrent,
                        disable_deep_crawl_when_limited=disable_deep_crawl_when_limited,
                        pipeline_id=f"{pipeline_id}-{domain_item}" if pipeline_id else None,
                        resume_from_checkpoint=resume_from_checkpoint,
                    )
                    logger.info("Completed processing for domain: %s", domain_item)
                    return (domain_item, domain_result)
                except Exception as e:
                    logger.error("Error processing domain %s: %s", domain_item, e, exc_info=True)
                    return (domain_item, e)
                finally:
                    try:
                        if hasattr(domain_orchestrator, "loader") and hasattr(domain_orchestrator.loader, "close"):
                            domain_orchestrator.loader.close()
                        if hasattr(domain_orchestrator, "embedder") and hasattr(domain_orchestrator.embedder, "close"):
                            domain_orchestrator.embedder.close()
                        if hasattr(domain_orchestrator, "change_detector") and domain_orchestrator.change_detector:
                            if hasattr(domain_orchestrator.change_detector, "close"):
                                domain_orchestrator.change_detector.close()
                    except Exception as cleanup_error:
                        logger.warning("Error during cleanup for domain %s: %s", domain_item, cleanup_error)

            tasks = [process_domain(domain_item) for domain_item in domains]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            all_results = []
            aggregated_stats = {
                "domains_processed": [],
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

            for result_item in results:
                if isinstance(result_item, Exception):
                    logger.error("Unexpected exception in parallel processing: %s", result_item, exc_info=True)
                    aggregated_stats["errors"].append({
                        "domain": "unknown",
                        "stage": "pipeline",
                        "error": f"Unexpected exception: {str(result_item)}"
                    })
                    continue
                
                if not isinstance(result_item, tuple) or len(result_item) != 2:
                    logger.error("Invalid result format: %s", result_item)
                    aggregated_stats["errors"].append({
                        "domain": "unknown",
                        "stage": "pipeline",
                        "error": f"Invalid result format: {result_item}"
                    })
                    continue
                
                domain_item, domain_result = result_item
                
                if isinstance(domain_result, Exception):
                    aggregated_stats["errors"].append({
                        "domain": domain_item,
                        "stage": "pipeline",
                        "error": str(domain_result)
                    })
                    logger.error("Domain %s failed: %s", domain_item, domain_result)
                    continue

                all_results.append({"domain": domain_item, "result": domain_result})
                aggregated_stats["domains_processed"].append(domain_item)

                aggregated_stats["collected"] += domain_result.get("collected", 0)
                aggregated_stats["processed"] += domain_result.get("processed", 0)
                aggregated_stats["validated"] += domain_result.get("validated", 0)
                aggregated_stats["embedded"] += domain_result.get("embedded", 0)
                aggregated_stats["loaded_mongodb"] += domain_result.get("loaded_mongodb", 0)
                aggregated_stats["loaded_pinecone"] += domain_result.get("loaded_pinecone", 0)
                aggregated_stats["quality_rejected"] += domain_result.get("quality_rejected", 0)
                aggregated_stats["skipped_source_unchanged"] += domain_result.get("skipped_source_unchanged", 0)
                aggregated_stats["skipped_content_unchanged"] += domain_result.get("skipped_content_unchanged", 0)
                aggregated_stats["llm_calls_saved"] += domain_result.get("llm_calls_saved", 0)
                aggregated_stats["embedding_calls_saved"] += domain_result.get("embedding_calls_saved", 0)

                if domain_result.get("errors"):
                    aggregated_stats["errors"].extend([
                        {**error, "domain": domain_item}
                        for error in domain_result.get("errors", [])
                    ])

            logger.info(
                "Parallel processing completed: %d/%d domains succeeded",
                len(aggregated_stats["domains_processed"]),
                len(domains)
            )

            result = {
                **aggregated_stats,
                "domain": ", ".join(domains),
                "subdomain": subdomain,
                "domain_results": all_results,
            }

        return self._format_pipeline_result(result)

    def _format_pipeline_result(self, result: dict[str, Any]) -> dict[str, Any]:
        """Format pipeline result for storage.

        Args:
            result: Raw pipeline result

        Returns:
            Formatted result with stages and stats
        """
        from api.models.pipeline import PipelineStats

        stages = {}
        stats_dict = result.copy()

        if "embeddings_generated" in stats_dict and "embedded" not in stats_dict:
            stats_dict["embedded"] = stats_dict["embeddings_generated"]

        if "loaded_to_mongodb" in stats_dict:
            if "loaded_mongodb" not in stats_dict:
                stats_dict["loaded_mongodb"] = stats_dict["loaded_to_mongodb"]
            if "loaded" not in stats_dict:
                stats_dict["loaded"] = stats_dict["loaded_to_mongodb"]

        if "metrics_summary" in result:
            metrics = result["metrics_summary"]
            if "stages" in metrics:
                for stage_name, stage_metrics in metrics["stages"].items():
                    stages[stage_name] = StageProgress(
                        stage_name=stage_name,
                        status=StageStatus.COMPLETED,
                        items_processed=stage_metrics.get("items_processed", 0),
                        items_succeeded=stage_metrics.get("items_succeeded", 0),
                        items_failed=stage_metrics.get("items_failed", 0),
                        duration_seconds=stage_metrics.get("duration_seconds"),
                        progress_percentage=1.0,
                    )

        stats = PipelineStats(
            collected=stats_dict.get("collected", 0),
            processed=stats_dict.get("processed", 0),
            embedded=stats_dict.get("embedded", 0),
            loaded=stats_dict.get("loaded_mongodb", 0) or stats_dict.get("loaded", 0),
            errors=stats_dict.get("errors", []),
            skipped_source_unchanged=stats_dict.get("skipped_source_unchanged", 0),
            skipped_content_unchanged=stats_dict.get("skipped_content_unchanged", 0),
            llm_calls_saved=stats_dict.get("llm_calls_saved", 0),
            embedding_calls_saved=stats_dict.get("embedding_calls_saved", 0),
            context_generated=stats_dict.get("context_generated", 0),
            loaded_mongodb=stats_dict.get("loaded_mongodb", 0),
            loaded_pinecone=stats_dict.get("loaded_pinecone", 0),
            allocated=stats_dict.get("allocated", 0),
        )

        return {
            "stages": {name: stage.model_dump() for name, stage in stages.items()},
            "stats": stats.model_dump(),
        }

    def _validate_pipeline_success(
        self,
        pipeline_type: PipelineType,
        stats: dict[str, Any],
        stages: dict[str, Any],
    ) -> bool:
        """Validate if pipeline succeeded based on critical stages.

        Args:
            pipeline_type: Type of pipeline
            stats: Pipeline statistics
            stages: Pipeline stages

        Returns:
            True if pipeline failed validation, False if succeeded
        """
        if pipeline_type == PipelineType.COST_DATA:
            collected = stats.get("collected", 0)
            processed = stats.get("processed", 0)
            embedded = stats.get("embedded", 0)
            loaded_mongodb = stats.get("loaded_mongodb", 0)
            loaded_pinecone = stats.get("loaded_pinecone", 0)
            context_generated = stats.get("context_generated", 0)

            if collected == 0:
                return True

            if processed == 0 and collected > 0:
                return True

            if context_generated == 0 and processed > 0:
                return True

            if embedded == 0 and context_generated > 0:
                return True

            if loaded_mongodb == 0 and loaded_pinecone == 0 and embedded > 0:
                return True

        elif pipeline_type == PipelineType.COMPLIANCE:
            collected = stats.get("collected", 0)
            processed = stats.get("processed", 0)
            embedded = stats.get("embedded", 0)
            loaded = stats.get("loaded_mongodb", 0) or stats.get("loaded", 0)

            if collected == 0:
                return True

            if processed == 0 and collected > 0:
                return True

            if embedded == 0 and processed > 0:
                return True

            if loaded == 0 and embedded > 0:
                return True

        elif pipeline_type in (PipelineType.CODE_EXAMPLES, PipelineType.KNOWLEDGE):
            collected = stats.get("collected", 0)
            processed = stats.get("processed", 0)
            embedded = stats.get("embedded", 0)
            loaded = stats.get("loaded_mongodb", 0) or stats.get("loaded", 0)

            if collected == 0:
                return True

            if processed == 0 and collected > 0:
                return True

            if embedded == 0 and processed > 0:
                return True

            if loaded == 0 and embedded > 0:
                return True

        return False

    def _build_failure_message(
        self,
        pipeline_type: PipelineType,
        stats: dict[str, Any],
    ) -> str:
        """Build failure message based on pipeline type and stats.

        Args:
            pipeline_type: Type of pipeline
            stats: Pipeline statistics

        Returns:
            Failure message string
        """
        if pipeline_type == PipelineType.COST_DATA:
            collected = stats.get("collected", 0)
            processed = stats.get("processed", 0)
            context_generated = stats.get("context_generated", 0)
            embedded = stats.get("embedded", 0)
            loaded_mongodb = stats.get("loaded_mongodb", 0)
            loaded_pinecone = stats.get("loaded_pinecone", 0)

            if collected == 0:
                return "Critical failure: No records collected"
            if processed == 0:
                return f"Critical failure: Collected {collected} records but none processed"
            if context_generated == 0:
                return f"Critical failure: Processed {processed} records but no context generated"
            if embedded == 0:
                return f"Critical failure: Generated context for {context_generated} records but none embedded"
            if loaded_mongodb == 0 and loaded_pinecone == 0:
                return f"Critical failure: Embedded {embedded} records but none loaded to MongoDB/Pinecone"

        else:
            collected = stats.get("collected", 0)
            processed = stats.get("processed", 0)
            embedded = stats.get("embedded", 0)
            loaded = stats.get("loaded_mongodb", 0) or stats.get("loaded", 0)
            errors = stats.get("errors", [])
            quality_rejected = stats.get("quality_rejected", 0)

            if collected == 0:
                return "Critical failure: No items collected"
            if processed == 0:
                error_details = []
                if quality_rejected > 0:
                    error_details.append(f"{quality_rejected} rejected by quality filters")
                if errors:
                    filtered_errors = [e for e in errors if "Article filtered out" in str(e.get("error", ""))]
                    if filtered_errors:
                        error_details.append(f"{len(filtered_errors)} filtered out (content too short/invalid)")
                    other_errors = [e for e in errors if "Article filtered out" not in str(e.get("error", ""))]
                    if other_errors:
                        error_details.append(f"{len(other_errors)} failed processing")
                
                error_msg = f"Critical failure: Collected {collected} items but none processed"
                if error_details:
                    error_msg += f" ({', '.join(error_details)})"
                return error_msg
            if embedded == 0:
                return f"Critical failure: Processed {processed} items but none embedded"
            if loaded == 0:
                return f"Critical failure: Embedded {embedded} items but none loaded"

        return "Critical failure: Pipeline validation failed"

    async def get_configuration(self) -> dict[str, Any]:
        """Get pipeline configuration.

        Returns:
            Configuration dictionary
        """
        db = self._get_db()
        collection = db.pipeline_config

        config_doc = collection.find_one({"_id": "default"})
        if config_doc:
            return {
                "max_concurrent_pipelines": config_doc.get("max_concurrent_pipelines", self._max_concurrent),
                "max_batch_size": config_doc.get("max_batch_size", self._max_batch_size),
                "rate_limit_per_hour": config_doc.get("rate_limit_per_hour", self._rate_limit_per_hour),
                "pipeline_timeout_hours": config_doc.get("pipeline_timeout_hours", self._pipeline_timeout_hours),
            }

        return {
            "max_concurrent_pipelines": self._max_concurrent,
            "max_batch_size": self._max_batch_size,
            "rate_limit_per_hour": self._rate_limit_per_hour,
            "pipeline_timeout_hours": self._pipeline_timeout_hours,
        }

    async def update_configuration(self, updates: dict[str, Any]) -> dict[str, Any]:
        """Update pipeline configuration.

        Args:
            updates: Configuration updates

        Returns:
            Updated configuration dictionary
        """
        db = self._get_db()
        collection = db.pipeline_config

        current_config = await self.get_configuration()
        updated_config = {**current_config, **updates}

        collection.update_one(
            {"_id": "default"},
            {"$set": updated_config},
            upsert=True,
        )

        if "max_concurrent_pipelines" in updates:
            self._max_concurrent = updated_config["max_concurrent_pipelines"]
        if "max_batch_size" in updates:
            self._max_batch_size = updated_config["max_batch_size"]
        if "rate_limit_per_hour" in updates:
            self._rate_limit_per_hour = updated_config["rate_limit_per_hour"]
        if "pipeline_timeout_hours" in updates:
            self._pipeline_timeout_hours = updated_config["pipeline_timeout_hours"]

        logger.info("Pipeline configuration updated: %s", updated_config)

        return updated_config

    async def get_metrics(self) -> dict[str, Any]:
        """Get pipeline metrics and analytics.

        Returns:
            Metrics dictionary
        """
        db = self._get_db()
        collection = db.pipeline_jobs

        total_pipelines = collection.count_documents({})
        completed_pipelines = collection.count_documents({"status": PipelineStatus.COMPLETED.value})
        failed_pipelines = collection.count_documents({"status": PipelineStatus.FAILED.value})
        running_count = collection.count_documents({"status": PipelineStatus.RUNNING.value})

        success_rate = None
        if completed_pipelines + failed_pipelines > 0:
            success_rate = completed_pipelines / (completed_pipelines + failed_pipelines)

        pipeline_docs = list(
            collection.find(
                {"status": PipelineStatus.COMPLETED.value},
                {"started_at": 1, "completed_at": 1},
            ).limit(100)
        )

        durations = []
        for doc in pipeline_docs:
            if doc.get("started_at") and doc.get("completed_at"):
                duration = (doc["completed_at"] - doc["started_at"]).total_seconds()
                durations.append(duration)

        average_duration = None
        if durations:
            average_duration = sum(durations) / len(durations)

        pipelines_by_type = {}
        type_counts = collection.aggregate([
            {"$group": {"_id": "$pipeline_type", "count": {"$sum": 1}}},
        ])
        for item in type_counts:
            pipelines_by_type[item["_id"]] = item["count"]

        recent_pipelines = []
        recent_docs = list(
            collection.find({}, {"pipeline_id": 1, "pipeline_type": 1, "status": 1, "created_at": 1})
            .sort("created_at", -1)
            .limit(10)
        )
        for doc in recent_docs:
            recent_pipelines.append({
                "pipeline_id": doc.get("_id", ""),
                "pipeline_type": doc.get("pipeline_type", ""),
                "status": doc.get("status", ""),
                "created_at": doc.get("created_at").isoformat() if doc.get("created_at") else None,
            })

        return {
            "total_pipelines": total_pipelines,
            "success_rate": success_rate,
            "average_duration_seconds": average_duration,
            "running_count": running_count,
            "pipelines_by_type": pipelines_by_type,
            "recent_pipelines": recent_pipelines,
        }


pipeline_execution_service = PipelineExecutionService()

