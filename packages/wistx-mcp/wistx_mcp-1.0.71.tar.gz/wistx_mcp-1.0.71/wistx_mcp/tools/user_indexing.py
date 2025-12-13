"""MCP tools for user-provided resource indexing."""

import logging
from typing import Any, Optional

from wistx_mcp.tools.lib.api_client import WISTXAPIClient
from wistx_mcp.tools.lib.retry_utils import with_timeout_and_retry
from wistx_mcp.tools.lib.ai_analyzer import AIAnalyzer
from wistx_mcp.tools.lib.url_validator import validate_github_url, validate_url

logger = logging.getLogger(__name__)

api_client = WISTXAPIClient()
ai_analyzer = AIAnalyzer()


async def index_repository(
    repo_url: str,
    branch: str = "main",
    name: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[list[str]] = None,
    github_token: Optional[str] = None,
    include_patterns: Optional[list[str]] = None,
    exclude_patterns: Optional[list[str]] = None,
    api_key: Optional[str] = None,
) -> dict[str, Any]:
    """Index a GitHub repository for user-specific search.

    Supports both public and private repositories:
    - Public repos: No GitHub token needed (uses internal token automatically)
    - Private repos: Uses OAuth token automatically if connected during signup
    - github_token parameter: Optional, only needed for backward compatibility

    Args:
        repo_url: GitHub repository URL
        branch: Branch to index (default: main)
        name: Custom name for the resource
        description: Resource description
        tags: Tags for categorization
        github_token: GitHub personal access token (optional - OAuth token used automatically if available)
        include_patterns: File path patterns to include (glob patterns)
        exclude_patterns: File path patterns to exclude (glob patterns)
        api_key: WISTX API key (required for authentication)

    Returns:
        Dictionary with resource_id and status

    Raises:
        ValueError: If api_key is not provided
    """
    from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id

    try:
        await validate_api_key_and_get_user_id(api_key)
    except (ValueError, RuntimeError) as e:
        raise

    if not repo_url or not isinstance(repo_url, str):
        raise ValueError("Repository URL is required and must be a string")
    
    repo_url = repo_url.strip()
    
    if repo_url.startswith("file://") or repo_url.startswith("/") or ("\\" in repo_url and not repo_url.startswith("http")):
        raise ValueError(
            "Local file paths are not supported. This tool (wistx_index_repository) is for GitHub repositories ONLY. "
            "For documentation websites or document files, use wistx_index_resource instead. "
            "Please provide a GitHub repository URL (e.g., https://github.com/owner/repo)."
        )
    
    if not repo_url.startswith(("http://", "https://")):
        raise ValueError(
            "Invalid repository URL format. This tool (wistx_index_repository) is for GitHub repositories ONLY. "
            "For documentation websites or document files, use wistx_index_resource instead. "
            "Please provide a GitHub repository URL (e.g., https://github.com/owner/repo)."
        )
    
    if "github.com" not in repo_url.lower():
        raise ValueError(
            "This tool (wistx_index_repository) only supports GitHub repositories. "
            f"Provided URL does not appear to be a GitHub repository: {repo_url}. "
            "For documentation websites or document files, use wistx_index_resource instead."
        )
    
    from wistx_mcp.tools.lib.input_sanitizer import validate_repository_url_input

    validate_repository_url_input(repo_url)

    try:
        validated_repo_url = await validate_github_url(repo_url)
    except ValueError as e:
        error_msg = str(e)
        if "file" in error_msg.lower() or repo_url.startswith("file://"):
            raise ValueError(
                f"Local file paths are not supported. This tool requires a GitHub repository URL provided by the user. "
                f"Please ask the user for their GitHub repository URL (e.g., https://github.com/owner/repo). Error: {error_msg}"
            ) from e
        raise ValueError(f"Invalid GitHub repository URL: {error_msg}") from e

    try:
        from wistx_mcp.tools.lib.constants import INDEXING_TIMEOUT_SECONDS

        result = await with_timeout_and_retry(
            api_client.index_repository,
            timeout_seconds=INDEXING_TIMEOUT_SECONDS,
            max_attempts=2,
            retryable_exceptions=(RuntimeError, ConnectionError, TimeoutError),
            repo_url=validated_repo_url,
            branch=branch,
            name=name,
            description=description,
            tags=tags or [],
            github_token=github_token,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
            api_key=api_key,
        )
        return result
    except (ValueError, RuntimeError, ConnectionError, TimeoutError) as e:
        logger.error("Error indexing repository: %s", e, exc_info=True)
        raise
    except Exception as e:
        logger.error("Unexpected error indexing repository: %s", e, exc_info=True)
        raise RuntimeError(f"Unexpected error indexing repository: {e}") from e


async def index_content(
    content_url: Optional[str] = None,
    file_path: Optional[str] = None,
    content_type: Optional[str] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[list[str]] = None,
    include_patterns: Optional[list[str]] = None,
    exclude_patterns: Optional[list[str]] = None,
    api_key: Optional[str] = None,
) -> dict[str, Any]:
    """Index content (documentation website or document file) for user-specific search.

    Unified function that handles both:
    1. Documentation websites: Provide content_url (website URL) - crawls multiple pages
    2. Document files: Provide file_path or content_url (file URL/path) - processes single file

    Args:
        content_url: Content URL - can be:
            - Documentation website URL (for website crawling)
            - Document URL (http/https) or local file path (for single file)
        file_path: Local file path for direct upload (for single file, optional)
        content_type: Content type - can be:
            - "documentation" for website crawling
            - "pdf", "docx", "markdown", "md", "txt" for single files
            - Auto-detected from file_path or URL if not provided
        name: Custom name for the resource
        description: Resource description
        tags: Tags for categorization
        include_patterns: URL patterns to include (for documentation websites)
        exclude_patterns: URL patterns to exclude (for documentation websites)
        api_key: WISTX API key (required for authentication)

    Returns:
        Dictionary with resource_id and status

    Raises:
        ValueError: If api_key is not provided or required parameters missing
    """
    from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id

    try:
        await validate_api_key_and_get_user_id(api_key)
    except (ValueError, RuntimeError) as e:
        raise

    if not content_url and not file_path:
        raise ValueError("Either 'content_url' or 'file_path' must be provided")

    if content_url and "github.com" in content_url.lower() and "/blob/" not in content_url.lower():
        raise ValueError(
            "This tool (wistx_index_resource) is for documentation websites and document files ONLY. "
            f"GitHub repository URLs are not supported here. Use wistx_index_repository instead. "
            f"Provided URL: {content_url}"
        )

    document_extensions = {".pdf", ".docx", ".md", ".markdown", ".txt", ".xml", ".xlsx", ".xls", ".csv"}
    
    is_documentation = False
    if content_type == "documentation":
        is_documentation = True
    elif content_type and content_type not in ["documentation"]:
        is_documentation = False
    elif file_path:
        is_documentation = False
    elif content_url:
        from pathlib import Path
        url_path = Path(content_url)
        has_file_extension = url_path.suffix.lower() in document_extensions
        is_documentation = not has_file_extension

    if is_documentation:
        if not content_url:
            raise ValueError("content_url is required for documentation indexing")
        
        from wistx_mcp.tools.lib.input_sanitizer import validate_content_url_input

        validate_content_url_input(content_url)

        try:
            validated_content_url = await validate_url(content_url)
        except ValueError as e:
            raise ValueError(f"Invalid content URL: {e}") from e
        
        try:
            from wistx_mcp.tools.lib.constants import INDEXING_TIMEOUT_SECONDS

            result = await with_timeout_and_retry(
                api_client.index_documentation,
                timeout_seconds=INDEXING_TIMEOUT_SECONDS,
                max_attempts=2,
                retryable_exceptions=(RuntimeError, ConnectionError, TimeoutError),
                documentation_url=validated_content_url,
                name=name,
                description=description,
                tags=tags or [],
                include_patterns=include_patterns,
                exclude_patterns=exclude_patterns,
                api_key=api_key,
            )
            return result
        except (ValueError, RuntimeError, ConnectionError, TimeoutError) as e:
            logger.error("Error indexing documentation: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error indexing documentation: %s", e, exc_info=True)
            raise RuntimeError(f"Unexpected error indexing documentation: {e}") from e
    else:
        validated_document_url = None
        if content_url:
            try:
                validated_document_url = await validate_url(content_url)
            except ValueError as e:
                raise ValueError(f"Invalid document URL: {e}") from e
        
        try:
            from wistx_mcp.tools.lib.constants import DOCUMENT_INDEXING_TIMEOUT_SECONDS

            result = await with_timeout_and_retry(
                api_client.index_document,
                timeout_seconds=DOCUMENT_INDEXING_TIMEOUT_SECONDS,
                max_attempts=2,
                retryable_exceptions=(RuntimeError, ConnectionError, TimeoutError),
                document_url=validated_document_url,
                file_path=file_path,
                document_type=content_type,
                name=name,
                description=description,
                tags=tags or [],
                api_key=api_key,
            )
            return result
        except (ValueError, RuntimeError, ConnectionError, TimeoutError) as e:
            logger.error("Error indexing document: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error indexing document: %s", e, exc_info=True)
            raise RuntimeError(f"Unexpected error indexing document: {e}") from e


async def index_documentation(
    documentation_url: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[list[str]] = None,
    include_patterns: Optional[list[str]] = None,
    exclude_patterns: Optional[list[str]] = None,
    api_key: Optional[str] = None,
) -> dict[str, Any]:
    """Index a documentation website for user-specific search.

    Legacy function - use index_content instead.

    Args:
        documentation_url: Documentation website URL
        name: Custom name for the resource
        description: Resource description
        tags: Tags for categorization
        include_patterns: URL patterns to include
        exclude_patterns: URL patterns to exclude
        api_key: WISTX API key (required for authentication)

    Returns:
        Dictionary with resource_id and status
    """
    return await index_content(
        content_url=documentation_url,
        content_type="documentation",
        name=name,
        description=description,
        tags=tags,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
        api_key=api_key,
    )


async def index_document(
    document_url: Optional[str] = None,
    file_path: Optional[str] = None,
    document_type: Optional[str] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[list[str]] = None,
    api_key: Optional[str] = None,
) -> dict[str, Any]:
    """Index a document for user-specific search.

    Legacy function - use index_content instead.

    Args:
        document_url: Document URL (http/https) or local file path (optional)
        file_path: Local file path for direct upload (optional)
        document_type: Document type (pdf, docx, markdown, txt)
        name: Custom name for the resource
        description: Resource description
        tags: Tags for categorization
        api_key: WISTX API key (required for authentication)

    Returns:
        Dictionary with resource_id and status
    """
    return await index_content(
        content_url=document_url,
        file_path=file_path,
        content_type=document_type,
        name=name,
        description=description,
        tags=tags,
        api_key=api_key,
    )


async def list_resources(
    resource_type: Optional[str] = None,
    status: Optional[str] = None,
    api_key: Optional[str] = None,
    include_ai_analysis: bool = True,
    deduplicate: bool = True,
    show_duplicates: bool = False,
) -> dict[str, Any]:
    """List all indexed resources for the user with optional deduplication.

    Args:
        resource_type: Filter by resource type (repository, documentation, document)
        status: Filter by status (pending, indexing, completed, failed)
        api_key: WISTX API key (required for authentication)
        include_ai_analysis: Include AI-analyzed insights about resource collection (default: True)
        deduplicate: If True, show only latest completed resource per repo (default: True)
        show_duplicates: If True, include duplicate information (default: False)

    Returns:
        Dictionary with list of resources and optional AI analysis

    Raises:
        ValueError: If api_key is not provided
    """
    from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id
    from wistx_mcp.tools.lib.repo_normalizer import normalize_repo_url

    try:
        await validate_api_key_and_get_user_id(api_key)
    except (ValueError, RuntimeError) as e:
        raise

    try:
        result = await api_client.list_resources(
            resource_type=resource_type,
            status=status,
            api_key=api_key,
        )

        resources = result.get("resources", [])

        if deduplicate:
            grouped = {}
            duplicates = []

            for resource in resources:
                if resource.get("resource_type") == "repository":
                    normalized_url = resource.get("normalized_repo_url") or normalize_repo_url(
                        resource.get("repo_url", "")
                    )
                    key = (
                        resource.get("user_id"),
                        normalized_url,
                        resource.get("branch", "main"),
                    )

                    if key in grouped:
                        existing = grouped[key]
                        existing_indexed_at = existing.get("indexed_at")
                        resource_indexed_at = resource.get("indexed_at")

                        if (
                            resource.get("status") == "completed"
                            and existing.get("status") != "completed"
                        ) or (
                            resource.get("status") == "completed"
                            and existing.get("status") == "completed"
                            and resource_indexed_at
                            and existing_indexed_at
                            and resource_indexed_at > existing_indexed_at
                        ):
                            duplicates.append(existing)
                            grouped[key] = resource
                        else:
                            duplicates.append(resource)
                    else:
                        grouped[key] = resource
                else:
                    grouped[id(resource)] = resource

            resources = list(grouped.values())
            result["resources"] = resources

            if show_duplicates:
                result["duplicates"] = duplicates
                result["summary"] = {
                    "total": len(resources),
                    "duplicate_count": len(duplicates),
                }

        if include_ai_analysis and resources:
            try:
                ai_analysis = await ai_analyzer.analyze_resource_collection(
                    resources=resources,
                )
                if ai_analysis:
                    result["ai_analysis"] = ai_analysis
            except Exception as e:
                logger.warning("AI analysis failed, continuing without analysis: %s", e)

        result["summary"] = {
            "total": len(resources),
            "by_type": {},
            "by_status": {},
            "deletion_info": (
                "To delete a resource, use wistx_delete_resource with the resource_id. "
                "Each resource in the list includes its resource_id field."
            ),
        }

        for resource in resources:
            res_type = resource.get("resource_type", "unknown")
            res_status = resource.get("status", "unknown")
            result["summary"]["by_type"][res_type] = result["summary"]["by_type"].get(res_type, 0) + 1
            result["summary"]["by_status"][res_status] = result["summary"]["by_status"].get(res_status, 0) + 1

        if show_duplicates and deduplicate:
            result["summary"]["duplicate_count"] = len(duplicates) if "duplicates" in result else 0

        for resource in resources:
            resource["_deletion_hint"] = (
                f"Use wistx_delete_resource with resource_id='{resource.get('resource_id')}' to delete this resource"
            )

        return result
    except Exception as e:
        logger.error("Error listing resources: %s", e, exc_info=True)
        raise


async def check_resource_status(
    resource_id: str,
    api_key: Optional[str] = None,
) -> dict[str, Any]:
    """Check indexing status and progress for a resource.

    Args:
        resource_id: Resource ID
        api_key: WISTX API key (required for authentication)

    Returns:
        Dictionary with resource status and progress

    Raises:
        ValueError: If api_key is not provided
    """
    from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id

    try:
        await validate_api_key_and_get_user_id(api_key)
    except (ValueError, RuntimeError) as e:
        raise

    try:
        result = await api_client.get_resource(
            resource_id=resource_id,
            api_key=api_key,
        )
        return result
    except Exception as e:
        logger.error("Error checking resource status: %s", e, exc_info=True)
        raise


async def delete_resource(
    resource_type: str,
    identifier: str,
    api_key: Optional[str] = None,
) -> dict[str, Any]:
    """Delete an indexed resource and all associated knowledge articles.

    Args:
        resource_type: Type of resource ("repository", "documentation", or "document")
        identifier: Resource identifier - can be repository URL (e.g., 'owner/repo' or full URL), 
                   documentation URL, document URL, or resource_id (e.g., 'res_abc123')
        api_key: WISTX API key (required for authentication)

    Returns:
        Dictionary with deletion status

    Raises:
        ValueError: If api_key is not provided or invalid resource_type
    """
    from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id

    try:
        await validate_api_key_and_get_user_id(api_key)
    except (ValueError, RuntimeError) as e:
        raise

    valid_types = ["repository", "documentation", "document"]
    if resource_type not in valid_types:
        raise ValueError(f"Invalid resource_type: {resource_type}. Must be one of {valid_types}")

    try:
        result = await api_client.delete_resource_by_identifier(
            resource_type=resource_type,
            identifier=identifier,
            api_key=api_key,
        )
        return result
    except Exception as e:
        logger.error("Error deleting resource: %s", e, exc_info=True)
        raise

