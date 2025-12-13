"""Regex search tool - pattern-based code search with security and performance optimizations."""

import asyncio
import logging
from datetime import datetime
from typing import Any

from bson import ObjectId

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.api_client import WISTXAPIClient
from wistx_mcp.tools.lib.regex_engine import RegexEngine
from wistx_mcp.tools.lib.pattern_validator import PatternValidator
from wistx_mcp.tools.lib.pattern_templates import PatternTemplates
from wistx_mcp.tools.lib.plan_enforcement import require_query_quota

logger = logging.getLogger(__name__)

api_client = WISTXAPIClient()


@require_query_quota
async def regex_search_codebase(
    pattern: str | None = None,
    api_key: str = "",
    repositories: list[str] | None = None,
    resource_ids: list[str] | None = None,
    resource_types: list[str] | None = None,
    file_types: list[str] | None = None,
    code_type: str | None = None,
    cloud_provider: str | None = None,
    template: str | None = None,
    case_sensitive: bool = False,
    multiline: bool = False,
    dotall: bool = False,
    include_context: bool = True,
    context_lines: int = 3,
    limit: int = 1000,
    timeout: float = 30.0,
) -> dict[str, Any]:
    """Search codebase using regex patterns with world-class performance and security.

    Args:
        pattern: Regular expression pattern to search for
        api_key: WISTX API key for authentication
        repositories: List of repositories to search (owner/repo format)
        resource_ids: Filter by specific indexed resources
        resource_types: Filter by resource type (repository, documentation, document)
        file_types: Filter by file extensions (.tf, .yaml, .py, .md, etc.)
        code_type: Filter by code type (terraform, kubernetes, docker, python)
        cloud_provider: Filter by cloud provider mentioned in code
        template: Use pre-built pattern template (e.g., 'api_key', 'password', 'ip_address')
        case_sensitive: Case-sensitive matching (default: False)
        multiline: Multiline mode (^ and $ match line boundaries)
        dotall: Dot matches newline (default: False)
        include_context: Include surrounding code context (default: True)
        context_lines: Number of lines before/after match (default: 3)
        limit: Maximum number of results (default: 100, max: 1000)
        timeout: Maximum search time in seconds (default: 30.0)

    Returns:
        Dictionary with search results:
        - matches: List of regex matches with file paths, line numbers, and context
        - resources: Resource information
        - total: Total match count
        - pattern_info: Pattern compilation info and warnings
        - performance: Search performance metrics

    Raises:
        ValueError: If pattern is invalid or parameters are invalid
        TimeoutError: If search exceeds timeout
        Exception: If search fails
    """
    from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id

    if not pattern and not template:
        raise ValueError("Either pattern or template must be provided")

    if limit < 1 or limit > 1000:
        raise ValueError("limit must be between 1 and 1000")

    if timeout < 1.0 or timeout > 300.0:
        raise ValueError("timeout must be between 1.0 and 300.0 seconds")

    if pattern:
        from wistx_mcp.tools.lib.input_sanitizer import validate_pattern_input

        validate_pattern_input(pattern)

    logger.info(
        "Regex search: pattern='%s', template=%s, resources=%s, limit=%d",
        pattern[:100] if pattern else template,
        template,
        resource_ids,
        limit,
    )

    try:
        user_id = await validate_api_key_and_get_user_id(api_key)
    except (ValueError, RuntimeError) as e:
        raise

    if template:
        resolved_pattern = PatternTemplates.get_template(template)
        if not resolved_pattern:
            raise ValueError(f"Unknown template: {template}")
        pattern = resolved_pattern
    elif not pattern:
        raise ValueError("Either pattern or template must be provided")

    validator = PatternValidator()
    validation_result = await validator.validate_pattern(pattern)

    if not validation_result["valid"]:
        raise ValueError(f"Invalid regex pattern: {validation_result['error']}")

    compiled_pattern = validator.compile_pattern(
        pattern,
        case_sensitive=case_sensitive,
        multiline=multiline,
        dotall=dotall,
    )

    # Check if user has indexed resources BEFORE searching
    if not resource_ids and not repositories:
        has_indexed_resources = await _check_user_has_indexed_resources(user_id)
        if not has_indexed_resources:
            logger.info("No indexed resources found for user %s, returning setup guide", user_id)
            return await _get_indexing_setup_guide(user_id, api_key)

    try:
        async with MongoDBClient() as mongodb_client:
            if mongodb_client.database is None:
                raise RuntimeError("Failed to connect to MongoDB")

            resolved_resource_ids = list(resource_ids) if resource_ids else []

            if repositories:
                if mongodb_client.database is None:
                    raise RuntimeError("MongoDB database not connected")

                resources_collection = mongodb_client.database.indexed_resources
                repo_resource_ids = []

                for repo in repositories:
                    normalized_repo = repo.replace(".git", "").rstrip("/")
                    if "/" not in normalized_repo:
                        raise ValueError(f"Invalid repository format: {repo}. Expected 'owner/repo' format.")

                    repo_patterns = [
                        f"https://github.com/{normalized_repo}",
                        f"https://github.com/{normalized_repo}.git",
                        f"http://github.com/{normalized_repo}",
                        f"http://github.com/{normalized_repo}.git",
                        normalized_repo,
                    ]

                    found = False
                    for repo_pattern in repo_patterns:
                        from wistx_mcp.tools.lib.mongodb_client import execute_mongodb_operation
                        from wistx_mcp.tools.lib.constants import API_TIMEOUT_SECONDS
                        from wistx_mcp.tools.lib.mongodb_utils import escape_regex_for_mongodb

                        async def _find_resource() -> dict[str, Any] | None:
                            escaped_pattern = escape_regex_for_mongodb(repo_pattern)
                            return await resources_collection.find_one({
                                "user_id": ObjectId(user_id),
                                "resource_type": "repository",
                                "repo_url": {"$regex": escaped_pattern, "$options": "i"},
                            })

                        resource_doc = await execute_mongodb_operation(
                            _find_resource,
                            timeout=API_TIMEOUT_SECONDS,
                            max_retries=3,
                        )
                        if resource_doc and "_id" in resource_doc:
                            repo_resource_ids.append(resource_doc["_id"])
                            found = True
                            break

                    if not found:
                        logger.warning("No indexed resource found for repository: %s", repo)

                if not repo_resource_ids:
                    logger.warning("No indexed resources found for repositories: %s", repositories)

                resolved_resource_ids.extend(repo_resource_ids)

            mongo_filter: dict[str, Any] = {
                "user_id": ObjectId(user_id),
            }

            if resolved_resource_ids:
                mongo_filter["resource_id"] = {"$in": list(set(resolved_resource_ids))}

            if resource_types:
                mongo_filter["source_type"] = {"$in": resource_types}

            if not repositories and not resource_ids and not resolved_resource_ids:
                logger.info(
                    "No repositories or resource_ids specified - searching all user's indexed resources"
                )

            regex_engine = RegexEngine(
                mongodb_client=mongodb_client,
                timeout=timeout,
            )

            start_time = datetime.utcnow()

            matches = await regex_engine.search(
                pattern=compiled_pattern,
                mongo_filter=mongo_filter,
                file_types=file_types,
                code_type=code_type,
                cloud_provider=cloud_provider,
                include_context=include_context,
                context_lines=context_lines,
                limit=limit,
            )

            search_time = (datetime.utcnow() - start_time).total_seconds()

            resources_info = []
            if matches:
                resource_ids_found = set(
                    m.get("resource_id") for m in matches if m.get("resource_id")
                )
                if resource_ids_found and mongodb_client.database:
                    from wistx_mcp.tools.lib.mongodb_client import execute_mongodb_operation
                    from wistx_mcp.tools.lib.constants import API_TIMEOUT_SECONDS

                    resources_collection = mongodb_client.database.indexed_resources
                    valid_resource_ids = [rid for rid in resource_ids_found if rid]
                    if valid_resource_ids:
                        async def _fetch_resources() -> list[dict[str, Any]]:
                            resources_cursor = resources_collection.find(
                                {"_id": {"$in": valid_resource_ids}}
                            )
                            results = []
                            async for doc in resources_cursor:
                                if doc and "_id" in doc:
                                    results.append(doc)
                            return results

                        resources_info = await execute_mongodb_operation(
                            _fetch_resources,
                            timeout=API_TIMEOUT_SECONDS,
                            max_retries=3,
                        )

            helpful_message = None
            if regex_engine.files_searched == 0 and len(matches) == 0:
                if not repositories and not resource_ids:
                    helpful_message = (
                        "No matches found in your indexed repositories. Try specifying specific repositories "
                        "using the 'repositories' parameter (e.g., ['owner/repo-name']), or refine your search pattern."
                    )

            response = {
                "matches": matches,
                "resources": resources_info,
                "total": len(matches),
                "pattern_info": {
                    "pattern": pattern,
                    "template": template,
                    "flags": {
                        "case_sensitive": case_sensitive,
                        "multiline": multiline,
                        "dotall": dotall,
                    },
                    "warnings": validation_result.get("warnings", []),
                },
                "performance": {
                    "search_time_seconds": search_time,
                    "files_searched": regex_engine.files_searched,
                    "matches_found": len(matches),
                },
            }

            # Add metadata explaining empty results
            if len(matches) == 0:
                response["empty_results_metadata"] = {
                    "reason": "no_matches",
                    "explanation": "No matches found for the regex pattern",
                    "files_searched": regex_engine.files_searched,
                    "possible_causes": [
                        "Pattern may not match any content in indexed files",
                        "Pattern may be too specific or restrictive",
                        "Case sensitivity or flag settings may affect matching",
                    ],
                    "suggestions": [
                        "Try a broader or simpler pattern",
                        "Check case_sensitive, multiline, and dotall flags",
                        "Use template patterns for common searches (e.g., 'api_key', 'password')",
                        "Try specifying specific repositories or resource_ids",
                    ],
                }
                if regex_engine.files_searched == 0:
                    response["empty_results_metadata"]["reason"] = "no_files_searched"
                    response["empty_results_metadata"]["explanation"] = (
                        "No files were searched. This may indicate no indexed resources match your filters."
                    )

            if helpful_message:
                response["helpful_message"] = helpful_message
                response["suggestion"] = {
                    "action": "refine_search",
                    "message": helpful_message,
                }

            logger.info(
                "Regex search completed: %d matches in %.2f seconds",
                len(matches),
                search_time,
            )

            return response

    except asyncio.TimeoutError:
        logger.error("Regex search timed out after %.2f seconds", timeout)
        raise TimeoutError(f"Search exceeded timeout of {timeout} seconds")
    except Exception as e:
        logger.error("Error in regex_search_codebase: %s", e, exc_info=True)
        raise

