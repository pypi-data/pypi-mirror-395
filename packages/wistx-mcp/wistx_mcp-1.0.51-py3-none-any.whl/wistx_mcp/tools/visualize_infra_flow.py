"""Visualize infrastructure flow tool - generate infrastructure diagrams."""

import logging
from typing import Any

from wistx_mcp.tools.lib.infrastructure_visualizer import InfrastructureVisualizer
from wistx_mcp.tools.lib.plan_enforcement import require_query_quota

logger = logging.getLogger(__name__)


@require_query_quota
async def visualize_infra_flow(
    infrastructure_code: str | None = None,
    infrastructure_type: str | None = None,
    visualization_type: str = "flow",
    format: str = "mermaid",
    include_resources: bool = True,
    include_networking: bool = True,
    depth: int = 3,
    focus_area: str | None = None,
    evaluate_quality: bool = False,
    auto_store: bool = True,
) -> dict[str, Any]:
    """Visualize infrastructure flow and architecture.

    Args:
        infrastructure_code: Infrastructure code to visualize
        infrastructure_type: Type (terraform, kubernetes, docker, etc.)
        visualization_type: Type of visualization (flow, architecture, dependencies, network)
        format: Output format (mermaid, plantuml)
        include_resources: Include resource details
        include_networking: Include networking flows
        depth: Visualization depth (1-5)
        focus_area: Focus on specific area
        evaluate_quality: Evaluate and score visualization quality (default: False)
        auto_store: Automatically store templates with quality score >= 80% (default: True)

    Returns:
        Dictionary with visualization data

    Raises:
        ValueError: If invalid parameters
        Exception: If visualization fails
    """
    if visualization_type not in ["flow", "architecture", "dependencies", "network"]:
        from wistx_mcp.tools.lib.error_handler import ErrorHandler

        raise ValueError(
            ErrorHandler.get_user_friendly_error_message(
                ValueError(f"Invalid visualization_type: {visualization_type}"),
                tool_name="wistx_visualize_infra_flow",
            )
        )

    if format not in ["mermaid", "plantuml"]:
        from wistx_mcp.tools.lib.error_handler import ErrorHandler

        raise ValueError(
            ErrorHandler.get_user_friendly_error_message(
                ValueError(f"Invalid format: {format}"),
                tool_name="wistx_visualize_infra_flow",
            )
        )

    logger.info(
        "Visualizing infrastructure: type=%s, viz_type=%s, format=%s",
        infrastructure_type,
        visualization_type,
        format,
    )

    visualizer = InfrastructureVisualizer(mongodb_client=None)

    visualization = await visualizer.generate_visualization(
        infrastructure_code=infrastructure_code,
        infrastructure_type=infrastructure_type,
        visualization_type=visualization_type,
        format=format,
        include_resources=include_resources,
        include_networking=include_networking,
        depth=depth,
        focus_area=focus_area,
    )

    quality_score_result = None
    template_id = None

    if evaluate_quality:
        from wistx_mcp.services.quality_scorer import QualityScorer
        from wistx_mcp.services.template_storage_service import TemplateStorageService
        from wistx_mcp.tools.lib.mongodb_client import MongoDBClient

        scorer = QualityScorer()
        quality_score_result = scorer.score_infrastructure_visualization({
            "visualization": visualization.get("diagram", ""),
            "format": format,
            "type": visualization_type,
            "components": visualization.get("components", []),
            "connections": visualization.get("connections", []),
            "metadata": visualization.get("metadata", {}),
        })

        if auto_store and quality_score_result.meets_threshold:
            async with MongoDBClient() as mongodb_client:
                storage_service = TemplateStorageService(mongodb_client)

                categories = []
                if infrastructure_type:
                    categories.append(infrastructure_type.lower())

                try:
                    template_id = await storage_service.store_template(
                        template_type="infrastructure_visualization",
                        content={
                            "visualization": visualization.get("diagram", ""),
                            "components": visualization.get("components", []),
                            "connections": visualization.get("connections", []),
                        },
                        quality_score=quality_score_result.overall_score,
                        score_breakdown=quality_score_result.score_breakdown,
                        metadata=visualization.get("metadata", {}),
                        tags=[visualization_type, format],
                        categories=categories,
                        visibility="global",
                    )
                    logger.info("Stored visualization as quality template: %s", template_id)
                except Exception as e:
                    logger.warning("Failed to store quality template: %s", e, exc_info=True)

    result = {
        "visualization": visualization.get("diagram", ""),
        "format": format,
        "type": visualization_type,
        "components": visualization.get("components", []),
        "connections": visualization.get("connections", []),
        "metadata": visualization.get("metadata", {}),
    }

    if quality_score_result:
        result["quality_score"] = {
            "overall_score": quality_score_result.overall_score,
            "score_breakdown": quality_score_result.score_breakdown,
            "recommendations": quality_score_result.recommendations,
            "stored_as_template": template_id is not None,
            "template_id": template_id,
        }

    return result

