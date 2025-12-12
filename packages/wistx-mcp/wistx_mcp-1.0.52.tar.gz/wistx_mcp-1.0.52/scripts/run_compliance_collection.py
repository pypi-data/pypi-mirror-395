#!/usr/bin/env python3
"""Run compliance data collection.

This script collects compliance data from all standards and saves to raw data files.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from data_pipelines.collectors import ComplianceCollector
from data_pipelines.utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Run compliance collection."""
    logger.info("=" * 80)
    logger.info("Compliance Data Collection")
    logger.info("=" * 80)
    logger.info("")

    collector = ComplianceCollector()

    logger.info("Collecting all compliance standards...")
    logger.info("")

    results = collector.collect_all()

    logger.info("")
    logger.info("=" * 80)
    logger.info("Collection Summary")
    logger.info("=" * 80)
    logger.info("")

    total_controls = 0
    for standard, controls in results.items():
        count = len(controls)
        total_controls += count
        logger.info(f"  {standard:20s}: {count:4d} controls")

    logger.info("")
    logger.info(f"Total Standards: {len(results)}")
    logger.info(f"Total Controls: {total_controls}")
    logger.info("")
    logger.info("Raw data saved to: data/compliance/raw/")
    logger.info("")
    logger.info("Next Steps:")
    logger.info("  1. Review raw data files")
    logger.info("  2. Implement compliance processor")
    logger.info("  3. Process raw data to standardized format")
    logger.info("")


if __name__ == "__main__":
    main()

