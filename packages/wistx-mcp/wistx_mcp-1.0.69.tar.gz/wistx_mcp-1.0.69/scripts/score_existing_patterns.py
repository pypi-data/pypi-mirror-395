"""Script to score existing integration patterns and store quality scores.

This script scores all patterns in INTEGRATION_PATTERNS and stores quality scores
in a format that can be used for pattern recommendations.
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any

from wistx_mcp.services.pattern_quality_scorer import PatternQualityScorer
from wistx_mcp.tools.lib.integration_patterns import INTEGRATION_PATTERNS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def score_all_patterns() -> dict[str, Any]:
    """Score all integration patterns and return results.

    Returns:
        Dictionary with pattern scores organized by integration_type
    """
    scorer = PatternQualityScorer()
    results: dict[str, Any] = {}

    for integration_type, patterns in INTEGRATION_PATTERNS.items():
        results[integration_type] = {}
        
        for pattern_name, pattern_data in patterns.items():
            try:
                quality_result = scorer.score_pattern(pattern_data)
                
                results[integration_type][pattern_name] = {
                    "quality_score": quality_result.overall_score,
                    "quality_breakdown": quality_result.score_breakdown,
                    "meets_threshold": quality_result.meets_threshold,
                    "recommendations": quality_result.recommendations,
                    "metadata": quality_result.metadata,
                }
                
                logger.info(
                    "Scored pattern %s/%s: %.2f (threshold: %.2f, meets: %s)",
                    integration_type,
                    pattern_name,
                    quality_result.overall_score,
                    scorer.QUALITY_THRESHOLD,
                    quality_result.meets_threshold,
                )
            except Exception as e:
                logger.error(
                    "Failed to score pattern %s/%s: %s",
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
    """Main function to score patterns and save results."""
    logger.info("Starting pattern quality scoring...")
    
    results = await score_all_patterns()
    
    script_dir = Path(__file__).parent
    output_file = script_dir / "pattern_quality_scores.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    logger.info("Pattern quality scores saved to %s", output_file)
    
    total_patterns = sum(len(patterns) for patterns in results.values())
    patterns_meeting_threshold = sum(
        sum(1 for p in patterns.values() if p.get("meets_threshold", False))
        for patterns in results.values()
    )
    
    logger.info(
        "Scoring complete: %d patterns scored, %d meet quality threshold (%.1f%%)",
        total_patterns,
        patterns_meeting_threshold,
        (patterns_meeting_threshold / total_patterns * 100) if total_patterns > 0 else 0,
    )
    
    avg_score = sum(
        sum(p.get("quality_score", 0) for p in patterns.values() if "quality_score" in p)
        for patterns in results.values()
    ) / total_patterns if total_patterns > 0 else 0
    
    logger.info("Average quality score: %.2f", avg_score)


if __name__ == "__main__":
    asyncio.run(main())

