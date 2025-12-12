"""Script to refresh cost data for code examples after pricing updates."""

import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from api.services.code_examples_cost_refresh_service import code_examples_cost_refresh_service
from api.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    """Refresh costs for code examples."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Refresh cost data for code examples")
    parser.add_argument(
        "--cloud-provider",
        type=str,
        choices=["aws", "gcp", "azure"],
        help="Filter by cloud provider",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Batch size for processing (default: 100)",
    )
    parser.add_argument(
        "--max-examples",
        type=int,
        help="Maximum number of examples to refresh (default: all)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run mode - check what would be refreshed without updating",
    )
    
    args = parser.parse_args()
    
    logger.info("=" * 80)
    logger.info("Code Examples Cost Refresh")
    logger.info("=" * 80)
    
    if args.dry_run:
        logger.info("DRY RUN MODE - No changes will be made")
    
    latest_timestamp = await code_examples_cost_refresh_service.get_latest_pricing_timestamp(
        args.cloud_provider
    )
    
    if latest_timestamp:
        logger.info("Latest pricing data timestamp: %s", latest_timestamp.isoformat())
    else:
        logger.warning("No pricing data found")
        return
    
    if not args.dry_run:
        stats = await code_examples_cost_refresh_service.refresh_costs_batch(
            cloud_provider=args.cloud_provider,
            batch_size=args.batch_size,
            max_examples=args.max_examples,
        )
        
        logger.info("=" * 80)
        logger.info("Refresh Statistics")
        logger.info("=" * 80)
        logger.info("Total found: %d", stats["total_found"])
        logger.info("Refreshed: %d", stats["refreshed"])
        logger.info("Failed: %d", stats["failed"])
        logger.info("Skipped: %d", stats["skipped"])
        
        if stats["errors"]:
            logger.warning("Errors encountered:")
            for error in stats["errors"][:10]:
                logger.warning("  - %s", error)
            if len(stats["errors"]) > 10:
                logger.warning("  ... and %d more errors", len(stats["errors"]) - 10)
    else:
        logger.info("Dry run complete - no changes made")


if __name__ == "__main__":
    asyncio.run(main())

