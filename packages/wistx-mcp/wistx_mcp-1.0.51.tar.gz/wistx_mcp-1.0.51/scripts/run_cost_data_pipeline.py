"""Script to run cost data pipeline."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from data_pipelines.orchestration.cost_data_pipeline import run_cost_data_pipeline, run_cost_data_pipeline_incremental
from data_pipelines.utils.logger import setup_logger

logger = setup_logger(__name__)


async def main():
    """Run cost data pipeline."""
    if "--incremental" in sys.argv:
        logger.info("Running incremental cost data pipeline...")
        results = await run_cost_data_pipeline_incremental()
    else:
        logger.info("Running full cost data pipeline...")
        results = await run_cost_data_pipeline()

    logger.info("Pipeline results: %s", results)

    total_collected = sum(
        r.get("collected", 0) for r in results.values() if isinstance(r, dict)
    )
    total_loaded = sum(
        r.get("loaded_mongodb", 0) for r in results.values() if isinstance(r, dict)
    )

    logger.info("Total collected: %d", total_collected)
    logger.info("Total loaded: %d", total_loaded)

    if total_collected == 0:
        logger.warning("No cost data collected. Check API credentials and network connectivity.")
        sys.exit(1)

    if total_loaded == 0:
        logger.warning("No cost data loaded. Check MongoDB connection and data processing.")
        sys.exit(1)

    logger.info("Cost data pipeline completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())

