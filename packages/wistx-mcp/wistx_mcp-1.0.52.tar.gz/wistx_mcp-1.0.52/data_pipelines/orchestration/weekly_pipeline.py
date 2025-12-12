"""Weekly full refresh pipeline orchestration."""

import asyncio
from datetime import datetime

from data_pipelines.processors.pipeline_orchestrator import PipelineOrchestrator, PipelineConfig
from data_pipelines.utils.logger import setup_logger
from data_pipelines.utils.tracing import TracingContext, get_correlation_id

logger = setup_logger(__name__)


async def run_weekly_pipeline():
    """Run weekly full refresh pipeline.

    This runs a complete refresh for all compliance standards,
    processing all data regardless of change detection.
    """
    correlation_id = get_correlation_id()
    
    with TracingContext("weekly_pipeline", correlation_id=correlation_id):
        config = PipelineConfig(
            mode="streaming",
            enable_change_detection=False,
            enable_streaming_saves=True,
        )
        
        orchestrator = PipelineOrchestrator(config)
        
        results = await orchestrator.run_all_standards()
        
        logger.info("Weekly pipeline completed at %s", datetime.utcnow().isoformat())
        return results


if __name__ == "__main__":
    asyncio.run(run_weekly_pipeline())
