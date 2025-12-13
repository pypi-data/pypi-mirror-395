"""Get GitHub file tree tool - retrieve repository structure."""

import logging
from typing import Any

from wistx_mcp.tools.lib.github_tree_fetcher import GitHubTreeFetcher

logger = logging.getLogger(__name__)


async def get_github_file_tree(
    repo_url: str,
    github_token: str | None = None,
    branch: str = "main",
    include_content: bool = False,
    max_file_size: int = 100000,
    include_patterns: list[str] | None = None,
    exclude_patterns: list[str] | None = None,
    depth: int = 10,
    format: str = "json",
    evaluate_quality: bool = False,
    auto_store: bool = True,
) -> dict[str, Any]:
    """Get GitHub repository file tree.

    Args:
        repo_url: GitHub repository URL
        github_token: GitHub token for private repos
        branch: Branch name (default: "main")
        include_content: Include file contents (default: False)
        max_file_size: Max file size to include content in bytes (default: 100KB)
        include_patterns: Glob patterns to include
        exclude_patterns: Glob patterns to exclude
        depth: Max directory depth (default: 10)
        format: Output format: "json", "tree", "markdown" (default: "json")
        evaluate_quality: Evaluate and score repository tree quality (default: False)
        auto_store: Automatically store templates with quality score >= 80% (default: True)

    Returns:
        Dictionary with file tree structure

    Raises:
        ValueError: If invalid parameters
        Exception: If fetch fails
    """
    if not repo_url:
        from wistx_mcp.tools.lib.error_handler import ErrorHandler

        raise ValueError(
            ErrorHandler.get_user_friendly_error_message(
                ValueError("repo_url is required"),
                tool_name="wistx_get_github_file_tree",
            )
        )

    if format not in ["json", "tree", "markdown"]:
        from wistx_mcp.tools.lib.error_handler import ErrorHandler

        raise ValueError(
            ErrorHandler.get_user_friendly_error_message(
                ValueError(f"Invalid format: {format}"),
                tool_name="wistx_get_github_file_tree",
            )
        )

    logger.info("Fetching file tree for: %s (branch: %s)", repo_url, branch)

    fetcher = GitHubTreeFetcher(github_token=github_token)

    tree = await fetcher.fetch_tree(
        repo_url=repo_url,
        branch=branch,
        include_content=include_content,
        max_file_size=max_file_size,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
        max_depth=depth,
    )

    quality_score_result = None
    template_id = None

    if evaluate_quality:
        from wistx_mcp.services.quality_scorer import QualityScorer
        from wistx_mcp.services.template_storage_service import TemplateStorageService
        from wistx_mcp.tools.lib.mongodb_client import MongoDBClient

        scorer = QualityScorer()
        quality_score_result = scorer.score_repository_tree(tree)

        if auto_store and quality_score_result.meets_threshold:
            async with MongoDBClient() as mongodb_client:
                storage_service = TemplateStorageService(mongodb_client)

                metadata = tree.get("metadata", {})
                tags = []
                if metadata.get("languages"):
                    tags.extend(metadata["languages"][:5])

                categories = []
                languages = metadata.get("languages", [])
                if any("terraform" in lang.lower() or "tf" in lang.lower() for lang in languages):
                    categories.append("terraform")
                if any("yaml" in lang.lower() or "yml" in lang.lower() for lang in languages):
                    categories.append("kubernetes")

                try:
                    template_id = await storage_service.store_template(
                        template_type="repository_tree",
                        content=tree.get("structure", {}),
                        quality_score=quality_score_result.overall_score,
                        score_breakdown=quality_score_result.score_breakdown,
                        metadata=metadata,
                        source_repo_url=repo_url,
                        tags=tags,
                        categories=categories,
                        visibility="global",
                    )
                    logger.info("Stored repository tree as quality template: %s", template_id)
                except Exception as e:
                    logger.warning("Failed to store quality template: %s", e, exc_info=True)

    result_base = {
        "repo_url": repo_url,
        "branch": branch,
        "format": format,
    }

    if quality_score_result:
        result_base["quality_score"] = {
            "overall_score": quality_score_result.overall_score,
            "score_breakdown": quality_score_result.score_breakdown,
            "recommendations": quality_score_result.recommendations,
            "stored_as_template": template_id is not None,
            "template_id": template_id,
        }

    if format == "tree":
        tree_text = fetcher.format_as_tree(tree)
        result_base.update({
            "tree": tree_text,
            "metadata": tree.get("metadata", {}),
        })
        return result_base
    elif format == "markdown":
        markdown = fetcher.format_as_markdown(tree)
        result_base.update({
            "markdown": markdown,
            "metadata": tree.get("metadata", {}),
        })
        return result_base
    else:
        result_base.update({
            "structure": tree.get("structure", {}),
            "metadata": tree.get("metadata", {}),
        })
        return result_base

