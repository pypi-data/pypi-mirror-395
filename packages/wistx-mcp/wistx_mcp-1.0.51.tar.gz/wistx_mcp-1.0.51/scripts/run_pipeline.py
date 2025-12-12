"""Example script to run the data processing pipeline."""

import asyncio
import logging
import sys
from pathlib import Path
import argparse
from data_pipelines.processors.pipeline_orchestrator import PipelineConfig, PipelineOrchestrator

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Run the data processing pipeline."""

    parser = argparse.ArgumentParser(description="Run data processing pipeline")
    parser.add_argument(
        "--mode",
        choices=["streaming", "checkpointing"],
        default="streaming",
        help="Pipeline mode (default: streaming)",
    )
    parser.add_argument(
        "--standard",
        type=str,
        help="Process specific standard (default: all)",
    )
    parser.add_argument(
        "--version",
        type=str,
        default="latest",
        help="Standard version (default: latest)",
    )
    parser.add_argument(
        "--no-collection",
        action="store_true",
        help="Skip collection stage (use existing raw data)",
    )

    args = parser.parse_args()

    config = PipelineConfig(
        mode=args.mode,
        save_intermediate=(args.mode == "checkpointing"),
        save_raw_data=True,
    )

    orchestrator = PipelineOrchestrator(config)

    if args.standard:
        logger.info("Processing single standard: %s", args.standard)
        result = await orchestrator.run_single_standard(
            args.standard, args.version, run_collection=not args.no_collection
        )
        logger.info("Result: %s", result)
    else:
        logger.info("Processing all standards")
        results = await orchestrator.run_all_standards()

        total_processed = sum(r.get("processed", 0) for r in results.values())
        total_embedded = sum(r.get("embedded", 0) for r in results.values())
        total_loaded = sum(r.get("loaded_mongodb", 0) for r in results.values())

        logger.info("=" * 80)
        logger.info("Pipeline Summary")
        logger.info("=" * 80)
        logger.info("Total Processed: %d", total_processed)
        logger.info("Total Embedded: %d", total_embedded)
        logger.info("Total Loaded: %d", total_loaded)
        logger.info("=" * 80)

        for standard, result in results.items():
            if "error" in result:
                logger.error("%s: ERROR - %s", standard, result["error"])
            else:
                logger.info(
                    "%s: Processed=%d, Embedded=%d, Loaded=%d",
                    standard,
                    result.get("processed", 0),
                    result.get("embedded", 0),
                    result.get("loaded_mongodb", 0),
                )


if __name__ == "__main__":
    asyncio.run(main())
