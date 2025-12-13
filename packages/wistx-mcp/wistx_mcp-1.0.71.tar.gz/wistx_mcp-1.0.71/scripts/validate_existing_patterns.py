"""Script to validate existing integration patterns against WISTX standards.

This script validates all patterns in INTEGRATION_PATTERNS and generates validation report.
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any

from wistx_mcp.services.pattern_validation_service import PatternValidationService
from wistx_mcp.tools.lib.integration_patterns import INTEGRATION_PATTERNS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def validate_all_patterns() -> dict[str, Any]:
    """Validate all integration patterns and return results.

    Returns:
        Dictionary with validation results organized by integration_type
    """
    validation_service = PatternValidationService()
    results: dict[str, Any] = {}

    for integration_type, patterns in INTEGRATION_PATTERNS.items():
        results[integration_type] = {}
        
        for pattern_name, pattern_data in patterns.items():
            try:
                validation_result = await validation_service.validate_pattern(pattern_data)
                
                results[integration_type][pattern_name] = {
                    "validation_score": validation_result["score"],
                    "validation_checks": validation_result["checks"],
                    "meets_threshold": validation_result["valid"],
                    "recommendations": validation_result["recommendations"],
                }
                
                logger.info(
                    "Validated pattern %s/%s: %.2f (threshold: %.2f, meets: %s)",
                    integration_type,
                    pattern_name,
                    validation_result["score"],
                    validation_service.VALIDATION_THRESHOLD,
                    validation_result["valid"],
                )
            except Exception as e:
                logger.error(
                    "Failed to validate pattern %s/%s: %s",
                    integration_type,
                    pattern_name,
                    e,
                    exc_info=True,
                )
                results[integration_type][pattern_name] = {
                    "error": str(e),
                }

    return results


async def main():
    """Main function to validate patterns and save results."""
    logger.info("Starting pattern validation...")
    
    results = await validate_all_patterns()
    
    script_dir = Path(__file__).parent
    output_file = script_dir / "pattern_validation_results.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    logger.info("Pattern validation results saved to %s", output_file)
    
    total_patterns = sum(len(patterns) for patterns in results.values())
    patterns_meeting_threshold = sum(
        sum(1 for p in patterns.values() if p.get("meets_threshold", False))
        for patterns in results.values()
    )
    
    logger.info(
        "Validation complete: %d patterns validated, %d meet validation threshold (%.1f%%)",
        total_patterns,
        patterns_meeting_threshold,
        (patterns_meeting_threshold / total_patterns * 100) if total_patterns > 0 else 0,
    )
    
    avg_score = sum(
        sum(p.get("validation_score", 0) for p in patterns.values() if "validation_score" in p)
        for patterns in results.values()
    ) / total_patterns if total_patterns > 0 else 0
    
    logger.info("Average validation score: %.2f", avg_score)


if __name__ == "__main__":
    asyncio.run(main())

