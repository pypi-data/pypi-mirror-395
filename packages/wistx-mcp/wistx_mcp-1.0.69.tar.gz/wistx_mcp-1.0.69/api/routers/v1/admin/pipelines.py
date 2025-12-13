"""Admin pipeline management endpoints."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies.auth import require_super_admin
from api.models.admin.pipeline import (
    PipelineConfigResponse,
    PipelineConfigUpdateRequest,
    PipelineMetricsResponse,
)
from api.models.pipeline import PipelineStatus, PipelineType
from api.services.pipeline_execution_service import pipeline_execution_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/pipelines", tags=["admin"])


@router.post("/compliance/trigger", summary="Trigger compliance pipeline")
async def trigger_compliance_pipeline(
    standard: str | None = Query(None, description="Compliance standard (leave empty for all)"),
    version: str = Query("latest", description="Standard version"),
    run_collection: bool = Query(True, description="Run collection stage"),
    enable_change_detection: bool = Query(True, description="Enable change detection"),
    enable_streaming_saves: bool = Query(True, description="Enable streaming saves"),
    streaming_batch_size: int = Query(10, ge=1, le=1000, description="Streaming batch size"),
    embedding_batch_size: int = Query(20, ge=1, le=1000, description="Embedding batch size"),
    max_controls: int | None = Query(None, ge=1, description="Maximum number of controls to process (None for all)"),
    max_standards: int | None = Query(None, ge=1, description="Maximum number of standards to process (None for all)"),
    max_pdfs: int | None = Query(None, ge=1, description="Maximum number of PDFs to process (None for all)"),
    max_urls: int | None = Query(None, ge=1, description="Maximum number of seed URLs to process (None for all). Note: Deep crawling may discover additional pages from seed URLs"),
    disable_deep_crawl_when_limited: bool = Query(False, description="Disable deep crawling when max_urls is set (default: False)"),
    execution_mode: str = Query("async", description="Execution mode (async/sync)"),
    priority: int = Query(5, ge=1, le=10, description="Pipeline priority"),
    current_user: dict[str, Any] = Depends(require_super_admin),
) -> dict[str, Any]:
    """Trigger compliance pipeline execution.

    Args:
        standard: Compliance standard name (optional, processes all if not provided)
        version: Standard version
        run_collection: Whether to run collection stage
        enable_change_detection: Enable change detection
        enable_streaming_saves: Enable streaming saves
        streaming_batch_size: Batch size for streaming saves
        embedding_batch_size: Batch size for embedding generation
        execution_mode: Execution mode (async/sync)
        priority: Pipeline priority (1-10)
        current_user: Current super admin user

    Returns:
        Pipeline job information
    """
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found",
            )

        request = {
            "standard": standard,
            "version": version,
            "run_collection": run_collection,
            "enable_change_detection": enable_change_detection,
            "enable_streaming_saves": enable_streaming_saves,
            "streaming_batch_size": streaming_batch_size,
            "embedding_batch_size": embedding_batch_size,
            "max_controls": max_controls,
            "max_standards": max_standards,
            "max_pdfs": max_pdfs,
            "max_urls": max_urls,
            "disable_deep_crawl_when_limited": disable_deep_crawl_when_limited,
        }

        job = await pipeline_execution_service.trigger_pipeline(
            pipeline_type=PipelineType.COMPLIANCE,
            request=request,
            user_id=user_id,
            priority=priority,
        )

        return {
            "pipeline_id": job.pipeline_id,
            "status": job.status.value,
            "pipeline_type": job.pipeline_type.value,
            "created_at": job.created_at.isoformat(),
            "correlation_id": job.correlation_id,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error triggering compliance pipeline: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to trigger pipeline",
        ) from e


@router.post("/cost-data/trigger", summary="Trigger cost data pipeline")
async def trigger_cost_data_pipeline(
    providers: str | None = Query(None, description="Comma-separated list of providers (aws,gcp,azure,oracle,alibaba)"),
    regions: str | None = Query(None, description="Comma-separated list of regions"),
    services: str | None = Query(None, description="Comma-separated list of services"),
    run_collection: bool = Query(True, description="Run collection stage"),
    enable_change_detection: bool = Query(True, description="Enable change detection"),
    enable_streaming_saves: bool = Query(True, description="Enable streaming saves"),
    max_providers: int | None = Query(None, ge=1, description="Maximum number of providers to process (None for all)"),
    max_regions: int | None = Query(None, ge=1, description="Maximum number of regions per provider (None for all)"),
    max_services: int | None = Query(None, ge=1, description="Maximum number of services per provider (None for all)"),
    max_records: int | None = Query(None, ge=1, description="Maximum number of cost records to process (None for all)"),
    execution_mode: str = Query("async", description="Execution mode (async/sync)"),
    priority: int = Query(5, ge=1, le=10, description="Pipeline priority"),
    current_user: dict[str, Any] = Depends(require_super_admin),
) -> dict[str, Any]:
    """Trigger cost data pipeline execution.

    Args:
        providers: Comma-separated list of providers
        regions: Comma-separated list of regions
        services: Comma-separated list of services
        run_collection: Whether to run collection stage
        enable_change_detection: Enable change detection
        enable_streaming_saves: Enable streaming saves
        execution_mode: Execution mode (async/sync)
        priority: Pipeline priority (1-10)
        current_user: Current super admin user

    Returns:
        Pipeline job information
    """
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found",
            )

        request: dict[str, Any] = {
            "run_collection": run_collection,
            "enable_change_detection": enable_change_detection,
            "enable_streaming_saves": enable_streaming_saves,
        }

        if providers:
            request["providers"] = [p.strip() for p in providers.split(",")]
        if regions:
            request["regions"] = [r.strip() for r in regions.split(",")]
        if services:
            request["services"] = [s.strip() for s in services.split(",")]
        if max_providers:
            request["max_providers"] = max_providers
        if max_regions:
            request["max_regions"] = max_regions
        if max_services:
            request["max_services"] = max_services
        if max_records:
            request["max_records"] = max_records

        job = await pipeline_execution_service.trigger_pipeline(
            pipeline_type=PipelineType.COST_DATA,
            request=request,
            user_id=user_id,
            priority=priority,
        )

        return {
            "pipeline_id": job.pipeline_id,
            "status": job.status.value,
            "pipeline_type": job.pipeline_type.value,
            "created_at": job.created_at.isoformat(),
            "correlation_id": job.correlation_id,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error triggering cost data pipeline: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to trigger pipeline",
        ) from e


@router.post("/code-examples/trigger", summary="Trigger code examples pipeline")
async def trigger_code_examples_pipeline(
    max_examples: int | None = Query(None, ge=1, description="Maximum number of examples to process (None for all)"),
    max_repos: int | None = Query(None, ge=1, description="Maximum number of repositories to process (None for all)"),
    max_files: int | None = Query(None, ge=1, description="Maximum number of files per repository (None for all)"),
    min_stars: int = Query(200, ge=0, description="Minimum stars for repositories"),
    execution_mode: str = Query("async", description="Execution mode (async/sync)"),
    priority: int = Query(5, ge=1, le=10, description="Pipeline priority"),
    current_user: dict[str, Any] = Depends(require_super_admin),
) -> dict[str, Any]:
    """Trigger code examples pipeline execution.

    Args:
        max_examples: Maximum number of examples to process
        execution_mode: Execution mode (async/sync)
        priority: Pipeline priority (1-10)
        current_user: Current super admin user

    Returns:
        Pipeline job information
    """
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found",
            )

        request = {
            "min_stars": min_stars,
        }
        if max_examples:
            request["max_examples"] = max_examples
        if max_repos:
            request["max_repos"] = max_repos
        if max_files:
            request["max_files"] = max_files

        job = await pipeline_execution_service.trigger_pipeline(
            pipeline_type=PipelineType.CODE_EXAMPLES,
            request=request,
            user_id=user_id,
            priority=priority,
        )

        return {
            "pipeline_id": job.pipeline_id,
            "status": job.status.value,
            "pipeline_type": job.pipeline_type.value,
            "created_at": job.created_at.isoformat(),
            "correlation_id": job.correlation_id,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error triggering code examples pipeline: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to trigger pipeline",
        ) from e


@router.post("/knowledge/trigger", summary="Trigger knowledge pipeline")
async def trigger_knowledge_pipeline(
    domain: str = Query(..., description="Knowledge domain(s). Use 'all' or '*' to process all domains, or specify comma-separated domains (e.g., 'compliance,devops,security')"),
    subdomain: str | None = Query(None, description="Optional subdomain"),
    run_collection: bool = Query(True, description="Run collection stage"),
    enable_change_detection: bool = Query(True, description="Enable change detection"),
    max_concurrent: int = Query(10, ge=1, le=200, description="Maximum concurrent URL fetches (default: 10, recommended: 50-100 for large datasets)"),
    max_urls: int | None = Query(None, ge=1, description="Maximum number of URLs to process (None for all). Note: Deep crawling may discover additional pages from seed URLs"),
    max_pdfs: int | None = Query(None, ge=1, description="Maximum number of PDFs to process (None for all)"),
    max_docs: int | None = Query(None, ge=1, description="Maximum number of documents to process (None for all)"),
    max_articles: int | None = Query(None, ge=1, description="Maximum number of articles to extract (None for all)"),
    disable_deep_crawl_when_limited: bool = Query(False, description="Disable deep crawling (sitemap recursion) when max_urls is set (default: False)"),
    execution_mode: str = Query("async", description="Execution mode (async/sync)"),
    priority: int = Query(5, ge=1, le=10, description="Pipeline priority"),
    current_user: dict[str, Any] = Depends(require_super_admin),
) -> dict[str, Any]:
    """Trigger knowledge pipeline execution.

    Args:
        domain: Knowledge domain
        subdomain: Optional subdomain
        run_collection: Whether to run collection stage
        enable_change_detection: Enable change detection
        max_concurrent: Maximum concurrent URL fetches
        execution_mode: Execution mode (async/sync)
        priority: Pipeline priority (1-10)
        current_user: Current super admin user

    Returns:
        Pipeline job information
    """
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found",
            )

        request = {
            "domain": domain,
            "subdomain": subdomain,
            "run_collection": run_collection,
            "enable_change_detection": enable_change_detection,
            "max_concurrent": max_concurrent,
            "max_urls": max_urls,
            "max_pdfs": max_pdfs,
            "max_docs": max_docs,
            "max_articles": max_articles,
            "disable_deep_crawl_when_limited": disable_deep_crawl_when_limited,
        }

        job = await pipeline_execution_service.trigger_pipeline(
            pipeline_type=PipelineType.KNOWLEDGE,
            request=request,
            user_id=user_id,
            priority=priority,
        )

        return {
            "pipeline_id": job.pipeline_id,
            "status": job.status.value,
            "pipeline_type": job.pipeline_type.value,
            "created_at": job.created_at.isoformat(),
            "correlation_id": job.correlation_id,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error triggering knowledge pipeline: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to trigger pipeline",
        ) from e


@router.get("/", summary="List pipeline jobs")
async def list_pipelines(
    status_param: str | None = Query(None, alias="status", description="Filter by status"),
    pipeline_type: str | None = Query(None, description="Filter by pipeline type"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    current_user: dict[str, Any] = Depends(require_super_admin),
) -> dict[str, Any]:
    """List pipeline jobs.

    Args:
        status: Filter by status
        pipeline_type: Filter by pipeline type
        limit: Maximum number of results
        offset: Offset for pagination
        current_user: Current super admin user

    Returns:
        List of pipeline jobs
    """
    try:
        status_filter = None
        if status_param:
            try:
                status_filter = PipelineStatus(status_param)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid status: {status_param}",
                )

        type_filter = None
        if pipeline_type:
            try:
                type_filter = PipelineType(pipeline_type)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid pipeline type: {pipeline_type}",
                )

        pipelines, total = await pipeline_execution_service.list_pipelines(
            status=status_filter,
            pipeline_type=type_filter,
            limit=limit,
            offset=offset,
        )

        return {
            "pipelines": [
                {
                    "pipeline_id": p.pipeline_id,
                    "pipeline_type": p.pipeline_type.value,
                    "status": p.status.value,
                    "progress": p.progress,
                    "current_stage": p.current_stage,
                    "created_at": p.created_at.isoformat(),
                    "started_at": p.started_at.isoformat() if p.started_at else None,
                    "completed_at": p.completed_at.isoformat() if p.completed_at else None,
                    "stats": p.stats.model_dump(),
                }
                for p in pipelines
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error listing pipelines: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list pipelines",
        ) from e


@router.get("/config", response_model=PipelineConfigResponse, summary="Get pipeline configuration")
async def get_pipeline_config(
    current_user: dict[str, Any] = Depends(require_super_admin),
) -> PipelineConfigResponse:
    """Get pipeline configuration.

    Args:
        current_user: Current super admin user

    Returns:
        Pipeline configuration
    """
    try:
        config = await pipeline_execution_service.get_configuration()
        return PipelineConfigResponse(**config)
    except Exception as e:
        logger.error("Error getting pipeline config: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get pipeline configuration",
        ) from e


@router.put("/config", response_model=PipelineConfigResponse, summary="Update pipeline configuration")
async def update_pipeline_config(
    request: PipelineConfigUpdateRequest,
    current_user: dict[str, Any] = Depends(require_super_admin),
) -> PipelineConfigResponse:
    """Update pipeline configuration.

    Args:
        request: Configuration update request
        current_user: Current super admin user

    Returns:
        Updated pipeline configuration
    """
    try:
        config = await pipeline_execution_service.update_configuration(request.model_dump(exclude_none=True))
        return PipelineConfigResponse(**config)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Error updating pipeline config: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update pipeline configuration",
        ) from e


@router.get("/metrics", response_model=PipelineMetricsResponse, summary="Get pipeline metrics")
async def get_pipeline_metrics(
    current_user: dict[str, Any] = Depends(require_super_admin),
) -> PipelineMetricsResponse:
    """Get pipeline metrics and analytics.

    Args:
        current_user: Current super admin user

    Returns:
        Pipeline metrics
    """
    try:
        metrics = await pipeline_execution_service.get_metrics()
        return PipelineMetricsResponse(**metrics)
    except Exception as e:
        logger.error("Error getting pipeline metrics: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get pipeline metrics",
        ) from e


@router.get("/{pipeline_id}", summary="Get pipeline job details")
async def get_pipeline(
    pipeline_id: str,
    current_user: dict[str, Any] = Depends(require_super_admin),
) -> dict[str, Any]:
    """Get pipeline job details.

    Args:
        pipeline_id: Pipeline ID
        current_user: Current super admin user

    Returns:
        Pipeline job details
    """
    try:
        job = await pipeline_execution_service.get_pipeline(pipeline_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pipeline not found",
            )

        return {
            "pipeline_id": job.pipeline_id,
            "pipeline_type": job.pipeline_type.value,
            "status": job.status.value,
            "progress": job.progress,
            "current_stage": job.current_stage,
            "stages": {name: stage.model_dump() for name, stage in job.stages.items()},
            "stats": job.stats.model_dump(),
            "created_at": job.created_at.isoformat(),
            "started_at": job.started_at.isoformat() if job.started_at else None,
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
            "error": job.error,
            "error_details": job.error_details,
            "correlation_id": job.correlation_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting pipeline: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get pipeline",
        ) from e


@router.post("/{pipeline_id}/cancel", summary="Cancel pipeline execution")
async def cancel_pipeline(
    pipeline_id: str,
    current_user: dict[str, Any] = Depends(require_super_admin),
) -> dict[str, Any]:
    """Cancel a running pipeline.

    Args:
        pipeline_id: Pipeline ID
        current_user: Current super admin user

    Returns:
        Cancellation result
    """
    try:
        cancelled = await pipeline_execution_service.cancel_pipeline(pipeline_id)
        if not cancelled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pipeline cannot be cancelled (not found or already completed)",
            )

        return {
            "pipeline_id": pipeline_id,
            "status": "cancelled",
            "message": "Pipeline cancelled successfully",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error cancelling pipeline: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel pipeline",
        ) from e


@router.get("/{pipeline_id}/progress", summary="Get pipeline progress (SSE)")
async def get_pipeline_progress_sse(
    pipeline_id: str,
    current_user: dict[str, Any] = Depends(require_super_admin),
):
    """Get pipeline progress via Server-Sent Events.

    Args:
        pipeline_id: Pipeline ID
        current_user: Current super admin user

    Yields:
        Progress updates as SSE events
    """
    from fastapi.responses import StreamingResponse
    import asyncio
    import json

    async def event_generator():
        """Generate SSE events for pipeline progress."""
        last_progress = None
        while True:
            try:
                job = await pipeline_execution_service.get_pipeline(pipeline_id)
                if not job:
                    yield f"data: {json.dumps({'error': 'Pipeline not found'})}\n\n"
                    break

                if job.status in (PipelineStatus.COMPLETED, PipelineStatus.FAILED, PipelineStatus.CANCELLED):
                    yield f"data: {json.dumps({'status': job.status.value, 'progress': job.progress, 'final': True})}\n\n"
                    break

                current_progress = {
                    "status": job.status.value,
                    "progress": job.progress,
                    "current_stage": job.current_stage,
                    "stages": {name: stage.model_dump() for name, stage in job.stages.items()},
                    "stats": job.stats.model_dump(),
                }

                if current_progress != last_progress:
                    yield f"data: {json.dumps(current_progress)}\n\n"
                    last_progress = current_progress

                await asyncio.sleep(1)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Error in SSE stream: %s", e)
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
                break

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/{pipeline_id}/resume", summary="Resume pipeline from checkpoint")
async def resume_pipeline(
    pipeline_id: str,
    current_user: dict[str, Any] = Depends(require_super_admin),
) -> dict[str, Any]:
    """Resume a failed pipeline from its latest checkpoint.
    
    Args:
        pipeline_id: Pipeline ID to resume
        current_user: Current super admin user
        
    Returns:
        Pipeline job information
    """
    try:
        from data_pipelines.utils.pipeline_progress import PipelineProgress
        
        progress = PipelineProgress(pipeline_id)
        latest_checkpoint = await progress.get_latest_checkpoint()
        
        if not latest_checkpoint:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No checkpoint found for pipeline {pipeline_id}",
            )
        
        checkpoint_stats = latest_checkpoint.get("stats", {})
        domain = checkpoint_stats.get("domain")
        subdomain = checkpoint_stats.get("subdomain")
        
        if not domain:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot determine domain from checkpoint",
            )
        
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found",
            )
        
        request = {
            "domain": domain,
            "subdomain": subdomain,
            "pipeline_id": pipeline_id,
            "resume_from_checkpoint": True,
            "run_collection": True,
            "enable_change_detection": True,
        }
        
        job = await pipeline_execution_service.trigger_pipeline(
            pipeline_type=PipelineType.KNOWLEDGE,
            request=request,
            user_id=user_id,
            priority=5,
        )
        
        return {
            "pipeline_id": job.pipeline_id,
            "status": job.status.value,
            "pipeline_type": job.pipeline_type.value,
            "resumed_from_checkpoint": True,
            "checkpoint_stage": latest_checkpoint.get("stage"),
            "checkpoint_timestamp": latest_checkpoint.get("timestamp").isoformat() if latest_checkpoint.get("timestamp") else None,
            "created_at": job.created_at.isoformat(),
            "correlation_id": job.correlation_id,
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error resuming pipeline %s: %s", pipeline_id, e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to resume pipeline: {str(e)}",
        ) from e


@router.get("/{pipeline_id}/checkpoint", summary="Get pipeline checkpoint")
async def get_pipeline_checkpoint(
    pipeline_id: str,
    current_user: dict[str, Any] = Depends(require_super_admin),
) -> dict[str, Any]:
    """Get checkpoint information for a pipeline.
    
    Args:
        pipeline_id: Pipeline ID
        current_user: Current super admin user
        
    Returns:
        Checkpoint information
    """
    try:
        from data_pipelines.utils.pipeline_progress import PipelineProgress
        
        progress = PipelineProgress(pipeline_id)
        latest_checkpoint = await progress.get_latest_checkpoint()
        all_checkpoints = await progress.get_all_checkpoints()
        
        if not latest_checkpoint:
            return {
                "pipeline_id": pipeline_id,
                "checkpoint_found": False,
                "checkpoints": [],
            }
        
        return {
            "pipeline_id": pipeline_id,
            "checkpoint_found": True,
            "latest_checkpoint": {
                "stage": latest_checkpoint.get("stage"),
                "timestamp": latest_checkpoint.get("timestamp").isoformat() if latest_checkpoint.get("timestamp") else None,
                "stats": latest_checkpoint.get("stats", {}),
                "metadata": latest_checkpoint.get("metadata", {}),
            },
            "all_checkpoints": [
                {
                    "stage": cp.get("stage"),
                    "timestamp": cp.get("timestamp").isoformat() if cp.get("timestamp") else None,
                    "stats": cp.get("stats", {}),
                }
                for cp in all_checkpoints
            ],
        }
        
    except Exception as e:
        logger.error("Error getting checkpoint for pipeline %s: %s", pipeline_id, e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get checkpoint: {str(e)}",
        ) from e

