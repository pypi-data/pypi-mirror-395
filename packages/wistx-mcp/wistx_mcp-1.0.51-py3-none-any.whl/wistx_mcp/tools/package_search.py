"""DevOps resource search tool - unified search across packages, tools, services, and documentation."""

import logging
from typing import Any

from wistx_mcp.tools.lib.api_client import WISTXAPIClient
from wistx_mcp.tools.lib.context_builder import ContextBuilder
from wistx_mcp.tools.lib.devops_resource_search_service import DevOpsResourceSearchService
from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.package_indexing_service import PackageIndexingService
from wistx_mcp.tools.lib.plan_enforcement import require_query_quota

logger = logging.getLogger(__name__)

api_client = WISTXAPIClient()


@require_query_quota
async def search_devops_resources(
    query: str,
    resource_types: list[str] | None = None,
    pattern: str | None = None,
    template: str | None = None,
    search_type: str = "semantic",
    registry: str | None = None,
    domain: str | None = None,
    category: str | None = None,
    package_name: str | None = None,
    limit: int = 1000,
    api_key: str = "",
) -> dict[str, Any]:
    """Search across all DevOps and infrastructure resources: packages, CLI tools, services, and documentation.

    Args:
        query: Natural language search query (required for semantic search)
        resource_types: Filter by resource types (package, tool, service, documentation, template, all)
                       Default: ["all"] - searches all resource types
        pattern: Regex pattern (for regex search on packages)
        template: Pre-built template name (alternative to pattern)
        search_type: Search type (semantic, regex, hybrid) - applies to packages only
        registry: Filter by registry (for packages: pypi, npm, terraform, etc.)
        domain: Filter by domain (devops, infrastructure, compliance, finops, platform, sre)
        category: Filter by category (infrastructure-as-code, cloud-providers, kubernetes, etc.)
        package_name: Search specific package (packages only)
        limit: Maximum results per resource type
        api_key: WISTX API key for authentication

    Returns:
        Dictionary with search results:
        - packages: List of packages
        - tools: List of CLI tools
        - services: List of services/integrations
        - documentation: List of documentation
        - unified_results: Cross-type ranked results
        - total: Total results across all types

    Raises:
        ValueError: If invalid parameters or authentication fails
        RuntimeError: If search fails
    """
    from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id

    try:
        await validate_api_key_and_get_user_id(api_key)
    except (ValueError, RuntimeError) as e:
        raise

    if not query:
        raise ValueError("query is required")

    if not resource_types:
        resource_types = ["all"]

    if "all" in resource_types:
        resource_types = ["package", "tool", "service", "documentation"]

    logger.info(
        "DevOps resource search: query=%s, resource_types=%s, registry=%s, domain=%s",
        query[:100],
        resource_types,
        registry,
        domain,
    )

    try:
        mongodb_client = MongoDBClient()
        search_service = DevOpsResourceSearchService(mongodb_client)

        api_packages = []
        if "package" in resource_types and (pattern or template or package_name or search_type in ["regex", "hybrid"]):
            try:
                api_response = await api_client.search_packages(
                    query=query,
                    pattern=pattern,
                    template=template,
                    search_type=search_type,
                    registry=registry,
                    domain=domain,
                    category=category,
                    package_name=package_name,
                    limit=limit,
                    api_key=api_key,
                )

                if api_response.get("data"):
                    api_packages = api_response["data"].get("results", [])
            except Exception as e:
                logger.warning("API package search failed, falling back to unified search: %s", e)

        unified_results = await search_service.search(
            query=query,
            resource_types=resource_types,
            registry=registry,
            domain=domain,
            category=category,
            limit=limit,
        )

        if api_packages:
            unified_results["packages"] = api_packages
        elif "package" in resource_types and not unified_results.get("packages"):
            unified_results["packages"] = []

        unified_results["total"] = sum(
            len(v) for v in unified_results.values() if isinstance(v, list)
        )

        return unified_results

    except Exception as e:
        logger.error("Error in search_devops_resources: %s", e, exc_info=True)
        raise


@require_query_quota
async def package_search(
    query: str | None = None,
    pattern: str | None = None,
    template: str | None = None,
    search_type: str = "semantic",
    registry: str | None = None,
    domain: str | None = None,
    category: str | None = None,
    package_name: str | None = None,
    limit: int = 1000,
    api_key: str = "",
) -> dict[str, Any]:
    """Search DevOps/infrastructure packages across registries.

    This function is kept for backward compatibility. Use search_devops_resources for unified search.

    Args:
        query: Natural language search query (for semantic/hybrid search)
        pattern: Regex pattern (for regex search)
        template: Pre-built template name (alternative to pattern)
        search_type: Search type (semantic, regex, hybrid)
        registry: Filter by registry (pypi, npm, terraform)
        domain: Filter by domain (devops, infrastructure, compliance, finops, platform, sre)
        category: Filter by category (infrastructure-as-code, cloud-providers, kubernetes, etc.)
        package_name: Search specific package
        limit: Maximum results
        api_key: WISTX API key for authentication

    Returns:
        Dictionary with search results

    Raises:
        ValueError: If invalid parameters or authentication fails
        RuntimeError: If search fails
    """
    from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id

    try:
        await validate_api_key_and_get_user_id(api_key)
    except (ValueError, RuntimeError) as e:
        raise

    if search_type not in ["semantic", "regex", "hybrid"]:
        raise ValueError(f"Invalid search_type: {search_type}. Must be semantic, regex, or hybrid")

    if search_type in ["semantic", "hybrid"] and not query:
        raise ValueError("query is required for semantic or hybrid search")

    if search_type in ["regex", "hybrid"] and not pattern and not template:
        raise ValueError("pattern or template is required for regex or hybrid search")

    logger.info(
        "Package search: type=%s, query=%s, registry=%s, domain=%s",
        search_type,
        query[:100] if query else None,
        registry,
        domain,
    )

    try:
        api_response = await api_client.search_packages(
            query=query,
            pattern=pattern,
            template=template,
            search_type=search_type,
            registry=registry,
            domain=domain,
            category=category,
            package_name=package_name,
            limit=limit,
            api_key=api_key,
        )

        if api_response.get("data"):
            return api_response["data"]
        return api_response

    except Exception as e:
        logger.error("Error in package_search: %s", e, exc_info=True)
        raise


async def index_package(
    registry: str,
    package_name: str,
    version: str | None = None,
    api_key: str = "",
) -> dict[str, Any]:
    """Index a package for search (on-demand indexing).

    Args:
        registry: Registry name (pypi, npm, terraform)
        package_name: Package name
        version: Optional version
        api_key: WISTX API key for authentication

    Returns:
        Indexed package document

    Raises:
        ValueError: If invalid parameters or authentication fails
        RuntimeError: If indexing fails
    """
    from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id

    logger.info("Indexing package: %s:%s", registry, package_name)

    try:
        user_id = await validate_api_key_and_get_user_id(api_key)

        async with MongoDBClient() as mongodb_client:
            if mongodb_client.database is None:
                raise RuntimeError("Failed to connect to MongoDB")

            indexing_service = PackageIndexingService(mongodb_client)

            from wistx_mcp.tools.lib.mongodb_client import execute_mongodb_operation
            from wistx_mcp.tools.lib.constants import API_TIMEOUT_SECONDS

            is_indexed = await indexing_service.is_package_indexed(registry, package_name)
            if is_indexed:
                logger.info("Package %s:%s already indexed", registry, package_name)
                collection = mongodb_client.database.packages

                async def _find_package() -> dict[str, Any] | None:
                    return await collection.find_one({"package_id": f"{registry}:{package_name}"})

                package_doc = await execute_mongodb_operation(
                    _find_package,
                    timeout=API_TIMEOUT_SECONDS,
                    max_retries=3,
                )
                return package_doc or {}

            indexed = await indexing_service.index_package(registry, package_name, version, pre_indexed=False)
            return indexed
    except (ValueError, RuntimeError) as e:
        raise
    except Exception as e:
        logger.error("Error indexing package: %s", e, exc_info=True)
        raise


@require_query_quota
async def read_package_file_mcp(
    registry: str,
    package_name: str,
    filename_sha256: str,
    start_line: int,
    end_line: int,
    version: str | None = None,
    api_key: str = "",
) -> dict[str, Any]:
    """Read specific file sections from package source code using SHA256 hash.

    Use this tool to get complete context around code snippets found in `wistx_search_devops_resources` results.
    The filename_sha256 is provided in package search results under 'source_files'.
    No indexing required - fetches packages on-demand from registries.

    Args:
        registry: Package registry (pypi, npm, terraform, crates_io, golang, helm, ansible, maven, nuget, rubygems)
        package_name: Package name
        filename_sha256: SHA256 hash of filename (from search results, must be 64 hex characters)
        start_line: Starting line (1-based, must be >= 1)
        end_line: Ending line (must be >= start_line, max 200 lines from start_line)
        version: Optional package version
        api_key: WISTX API key for authentication

    Returns:
        Dictionary with file content and metadata:
        - package_name: Package name
        - registry: Registry name
        - file_path: File path within package
        - filename_sha256: SHA256 hash of filename
        - start_line: Starting line
        - end_line: Ending line
        - total_lines: Total lines in file
        - content: File content for specified lines
        - line_count: Number of lines returned

    Raises:
        ValueError: If api_key is missing, invalid parameters, or file not found
        RuntimeError: If package source cannot be fetched
        ConnectionError: If network connection fails
        TimeoutError: If request times out
    """
    if not api_key:
        raise ValueError("api_key is required for reading package files")

    if not registry or not isinstance(registry, str):
        raise ValueError("registry must be a non-empty string")

    valid_registries = ["pypi", "npm", "terraform", "crates_io", "golang", "helm", "ansible", "maven", "nuget", "rubygems"]
    if registry not in valid_registries:
        raise ValueError(f"Invalid registry: {registry}. Must be one of {valid_registries}")

    if not package_name or not isinstance(package_name, str):
        raise ValueError("package_name must be a non-empty string")

    if not filename_sha256 or not isinstance(filename_sha256, str):
        raise ValueError("filename_sha256 must be a non-empty string")

    if len(filename_sha256) != 64:
        raise ValueError("filename_sha256 must be exactly 64 hexadecimal characters")

    try:
        int(filename_sha256, 16)
    except ValueError:
        raise ValueError("filename_sha256 must be a valid hexadecimal string") from None

    if not isinstance(start_line, int) or start_line < 1:
        raise ValueError("start_line must be an integer >= 1")

    if not isinstance(end_line, int) or end_line < start_line:
        raise ValueError(f"end_line must be an integer >= start_line ({start_line})")

    if end_line - start_line > 200:
        raise ValueError("Maximum 200 lines can be read at once")

    if version is not None and (not isinstance(version, str) or not version.strip()):
        raise ValueError("version must be a non-empty string if provided")

    from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id

    try:
        await validate_api_key_and_get_user_id(api_key)
    except (ValueError, RuntimeError) as e:
        raise

    logger.info(
        "Reading package file: registry=%s, package=%s, file_hash=%s, lines=%d-%d, version=%s",
        registry,
        package_name,
        filename_sha256[:16],
        start_line,
        end_line,
        version or "latest",
    )

    try:
        result = await api_client.read_package_file(
            registry=registry,
            package_name=package_name,
            filename_sha256=filename_sha256,
            start_line=start_line,
            end_line=end_line,
            version=version,
            api_key=api_key,
        )
        logger.info(
            "Successfully read package file: %s lines from %s:%s",
            result.get("line_count", 0),
            registry,
            package_name,
        )
        return result
    except ValueError as e:
        logger.error("Validation error reading package file: %s", e, exc_info=True)
        raise
    except RuntimeError as e:
        logger.error("Runtime error reading package file: %s", e, exc_info=True)
        raise
    except ConnectionError as e:
        logger.error("Connection error reading package file: %s", e, exc_info=True)
        raise
    except TimeoutError as e:
        logger.error("Timeout error reading package file: %s", e, exc_info=True)
        raise
    except Exception as e:
        logger.error("Unexpected error reading package file: %s", e, exc_info=True)
        raise RuntimeError(f"Unexpected error reading package file: {e}") from e

