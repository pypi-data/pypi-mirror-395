"""Pre-index core packages script - index 2,000-3,000 popular DevOps packages."""

import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from wistx_mcp.config import settings
from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.package_indexing_service import PackageIndexingService
from data_pipelines.package_lists.core_packages import get_all_packages, get_all_expanded_packages

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def pre_index_packages(
    batch_size: int = 50,
    max_workers: int = 10,
    dry_run: bool = False,
    expanded: bool = False,
) -> None:
    """Pre-index core packages.

    Args:
        batch_size: Number of packages to process in each batch
        max_workers: Maximum concurrent workers
        dry_run: If True, only log what would be indexed without actually indexing
        expanded: If True, use expanded package list (3,000-5,000 packages)
    """
    logger.info("Starting pre-indexing of %s packages", "expanded" if expanded else "core")
    logger.info("Batch size: %d, Max workers: %d, Dry run: %s", batch_size, max_workers, dry_run)

    packages = get_all_expanded_packages() if expanded else get_all_packages()
    logger.info("Total packages to index: %d", len(packages))

    mongodb_client = MongoDBClient()
    indexing_service = PackageIndexingService(mongodb_client)

    try:
        await mongodb_client.connect()
        if not mongodb_client.database:
            raise RuntimeError("Failed to connect to MongoDB")

        indexed_count = 0
        skipped_count = 0
        error_count = 0

        semaphore = asyncio.Semaphore(max_workers)

        async def index_package_with_semaphore(package: dict[str, str]) -> tuple[str, bool, str]:
            """Index a single package with semaphore control.

            Args:
                package: Package dictionary with registry and name

            Returns:
                Tuple of (package_id, success, error_message)
            """
            async with semaphore:
                registry = package["registry"]
                package_name = package["name"]
                package_id = f"{registry}:{package_name}"

                try:
                    if dry_run:
                        logger.info("Would index: %s", package_id)
                        return (package_id, True, "")

                    is_indexed = await indexing_service.is_package_indexed(registry, package_name)
                    if is_indexed:
                        logger.debug("Package already indexed: %s", package_id)
                        return (package_id, False, "already_indexed")

                    await indexing_service.index_package(
                        registry=registry,
                        package_name=package_name,
                        version=None,
                        pre_indexed=True,
                    )
                    logger.info("Indexed: %s", package_id)
                    return (package_id, True, "")
                except Exception as e:
                    logger.error("Failed to index %s: %s", package_id, e)
                    return (package_id, False, str(e))

        batches = [packages[i : i + batch_size] for i in range(0, len(packages), batch_size)]
        logger.info("Processing %d batches", len(batches))

        for batch_num, batch in enumerate(batches, 1):
            logger.info("Processing batch %d/%d (%d packages)", batch_num, len(batches), len(batch))

            tasks = [index_package_with_semaphore(package) for package in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, Exception):
                    error_count += 1
                    logger.error("Unexpected error: %s", result)
                else:
                    package_id, success, error_msg = result
                    if success:
                        indexed_count += 1
                    elif error_msg == "already_indexed":
                        skipped_count += 1
                    else:
                        error_count += 1

            logger.info(
                "Batch %d complete: indexed=%d, skipped=%d, errors=%d",
                batch_num,
                indexed_count,
                skipped_count,
                error_count,
            )

            if batch_num < len(batches):
                await asyncio.sleep(1)

        logger.info("Pre-indexing complete!")
        logger.info("Total packages: %d", len(packages))
        logger.info("Indexed: %d", indexed_count)
        logger.info("Skipped (already indexed): %d", skipped_count)
        logger.info("Errors: %d", error_count)

    except Exception as e:
        logger.error("Pre-indexing failed: %s", e, exc_info=True)
        raise
    finally:
        await mongodb_client.disconnect()


async def main() -> None:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Pre-index core DevOps/infrastructure packages")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Number of packages to process in each batch (default: 50)",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=10,
        help="Maximum concurrent workers (default: 10)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run mode - only log what would be indexed",
    )
    parser.add_argument(
        "--expanded",
        action="store_true",
        help="Use expanded package list (3,000-5,000 packages)",
    )

    args = parser.parse_args()

    await pre_index_packages(
        batch_size=args.batch_size,
        max_workers=args.max_workers,
        dry_run=args.dry_run,
        expanded=args.expanded,
    )


if __name__ == "__main__":
    asyncio.run(main())

