"""Scheduled cost data pipeline orchestration."""

import asyncio
from datetime import datetime

from data_pipelines.processors.pipeline_orchestrator import PipelineOrchestrator, PipelineConfig
from data_pipelines.utils.logger import setup_logger
from data_pipelines.utils.tracing import TracingContext, get_correlation_id

logger = setup_logger(__name__)


async def run_cost_data_pipeline():
    """Run cost data pipeline for all providers.

    This runs incremental updates for cost data from all cloud providers,
    processing only changed data using change detection.
    """
    correlation_id = get_correlation_id()

    with TracingContext("cost_data_pipeline", correlation_id=correlation_id):
        config = PipelineConfig(
            mode="streaming",
            enable_change_detection=True,
            enable_streaming_saves=True,
        )

        orchestrator = PipelineOrchestrator(config)

        providers = ["aws", "gcp", "azure", "oracle", "alibaba"]

        results = {}

        for provider in providers:
            try:
                logger.info("Processing cost data for provider: %s", provider)
                result = await orchestrator.run_cost_data_pipeline(
                    providers=[provider],
                    run_collection=True,
                )
                results[provider] = result
            except Exception as e:
                logger.error("Error processing provider %s: %s", provider, e, exc_info=True)
                results[provider] = {"error": str(e)}

        logger.info("Cost data pipeline completed at %s", datetime.utcnow().isoformat())
        
        try:
            logger.info("Triggering code examples cost refresh after pricing update")
            from api.services.code_examples_cost_refresh_service import code_examples_cost_refresh_service
            
            refresh_stats = await code_examples_cost_refresh_service.refresh_costs_batch(
                batch_size=100,
            )
            
            logger.info(
                "Code examples cost refresh completed: refreshed=%d, failed=%d",
                refresh_stats["refreshed"],
                refresh_stats["failed"],
            )
            
            results["code_examples_refresh"] = refresh_stats
        except Exception as e:
            logger.warning("Failed to refresh code examples costs: %s", e, exc_info=True)
            results["code_examples_refresh"] = {"error": str(e)}
        
        return results


async def run_cost_data_pipeline_incremental():
    """Run incremental cost data pipeline (daily updates).

    Only processes changed/new cost records.
    """
    correlation_id = get_correlation_id()

    with TracingContext("cost_data_pipeline_incremental", correlation_id=correlation_id):
        config = PipelineConfig(
            mode="streaming",
            enable_change_detection=True,
            enable_streaming_saves=True,
        )

        orchestrator = PipelineOrchestrator(config)

        providers = ["aws", "gcp", "azure"]

        results = {}

        for provider in providers:
            try:
                logger.info("Running incremental update for provider: %s", provider)
                result = await orchestrator.run_cost_data_pipeline(
                    providers=[provider],
                    run_collection=True,
                )
                results[provider] = result
            except Exception as e:
                logger.error("Error in incremental update for %s: %s", provider, e, exc_info=True)
                results[provider] = {"error": str(e)}

        logger.info("Incremental cost data pipeline completed at %s", datetime.utcnow().isoformat())
        return results


if __name__ == "__main__":
    asyncio.run(run_cost_data_pipeline())

