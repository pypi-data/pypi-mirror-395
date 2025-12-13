"""Daily data pipeline orchestration."""

import asyncio
from datetime import datetime

from data_pipelines.processors.pipeline_orchestrator import PipelineOrchestrator, PipelineConfig
from data_pipelines.utils.logger import setup_logger
from data_pipelines.utils.tracing import TracingContext, get_correlation_id

logger = setup_logger(__name__)


async def run_daily_pipeline():
    """Run daily compliance pipeline updates.

    This runs incremental updates for all compliance standards,
    processing only changed data using change detection.
    """
    correlation_id = get_correlation_id()
    
    with TracingContext("daily_pipeline", correlation_id=correlation_id):
        config = PipelineConfig(
            mode="streaming",
            enable_change_detection=True,
            enable_streaming_saves=True,
        )
        
        orchestrator = PipelineOrchestrator(config)
        
        standards = [
            "PCI-DSS",
            "CIS",
            "HIPAA",
            "SOC2",
            "NIST-800-53",
            "ISO-27001",
            "GDPR",
            "FedRAMP",
            "CCPA",
            "SOX",
            "GLBA",
        ]
        
        results = {}
        
        for standard in standards:
            try:
                logger.info("Processing standard: %s", standard)
                result = await orchestrator.run_compliance_pipeline(standard, run_collection=True)
                results[standard] = result
            except Exception as e:
                logger.error("Error processing standard %s: %s", standard, e, exc_info=True)
                results[standard] = {"error": str(e)}
        
        logger.info("Daily pipeline completed at %s", datetime.utcnow().isoformat())
        return results


if __name__ == "__main__":
    asyncio.run(run_daily_pipeline())
