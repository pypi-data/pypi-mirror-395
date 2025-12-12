"""REST API client for MCP server."""

import asyncio
import json
import logging
import os
import stat
from pathlib import Path
from typing import Any, BinaryIO, Optional
from urllib.parse import urlparse

import httpx

from wistx_mcp.config import settings
from wistx_mcp.tools.lib.circuit_breaker import CircuitBreaker, CircuitBreakerError
from wistx_mcp.tools.lib.retry_utils import with_timeout_and_retry
from wistx_mcp.tools.lib.secure_storage import SecureString

logger = logging.getLogger(__name__)

_global_api_client: Optional["WISTXAPIClient"] = None
_api_client_lock = asyncio.Lock()
_api_circuit_breaker = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=60,
    expected_exceptions=(RuntimeError, ConnectionError, TimeoutError),
    name="wistx_api",
)


def _read_file_atomic(file_path: Path) -> bytes:
    """Read file atomically with TOCTOU protection.

    Prevents race conditions where file could be replaced between validation
    and read by verifying inode consistency and file type.

    Args:
        file_path: Path to file (must be pre-validated)

    Returns:
        File contents as bytes

    Raises:
        SecurityError: If file is modified during read or type changes
        OSError: If file cannot be read
    """
    try:
        with open(file_path, 'rb') as f:
            # Get initial file stats
            stat_before = os.fstat(f.fileno())

            # Verify it's a regular file
            if not stat.S_ISREG(stat_before.st_mode):
                raise RuntimeError(f"Not a regular file: {file_path}")

            # Read file content
            content = f.read()

            # Get final file stats
            stat_after = os.fstat(f.fileno())

            # Verify inode hasn't changed (TOCTOU protection)
            if stat_before.st_ino != stat_after.st_ino:
                raise RuntimeError("File inode changed during read (TOCTOU attack detected)")

            # Verify file type hasn't changed
            if not stat.S_ISREG(stat_after.st_mode):
                raise RuntimeError("File type changed during read (TOCTOU attack detected)")

            # Verify file size is consistent
            if stat_before.st_size != stat_after.st_size:
                logger.warning(
                    "File size changed during read: %d -> %d bytes",
                    stat_before.st_size,
                    stat_after.st_size,
                )

            return content
    except (OSError, RuntimeError) as e:
        logger.error("Error reading file atomically: %s", e)
        raise


class WISTXAPIClient:
    """HTTP client for calling WISTX REST API."""

    def __init__(self, api_key: str | None = None, api_url: str | None = None):
        """Initialize API client.

        Args:
            api_key: API key for authentication (defaults to WISTX_API_KEY env var)
            api_url: Base URL for API (defaults to WISTX_API_URL env var or config)
        """
        api_key_value = api_key or settings.api_key or os.getenv("WISTX_API_KEY", "")
        
        self._api_key_secure: SecureString | None = None
        if api_key_value:
            self._api_key_secure = SecureString(api_key_value)
            api_key_for_header = self._api_key_secure.get()
        else:
            api_key_for_header = ""
        
        self.api_url = (api_url or settings.api_url or os.getenv("WISTX_API_URL", "https://api.wistx.ai")).rstrip("/")

        self.client = httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(
                max_connections=10,
                max_keepalive_connections=5,
                keepalive_expiry=30.0,
            ),
            headers={
                "Authorization": f"Bearer {api_key_for_header}" if api_key_for_header else "",
                "Content-Type": "application/json",
            },
        )

    def _get_api_key(self) -> str:
        """Get API key value from secure storage.

        Returns:
            API key string or empty string if not set
        """
        if self._api_key_secure:
            return self._api_key_secure.get()
        return ""

    async def close(self) -> None:
        """Close HTTP client connection and clear API key."""
        await self.client.aclose()
        if self._api_key_secure:
            self._api_key_secure.clear()
            self._api_key_secure = None

    def __del__(self):
        """Destructor: ensure API key is cleared."""
        if self._api_key_secure:
            self._api_key_secure.clear()

    async def get_compliance_requirements(
        self,
        resource_types: list[str],
        standards: list[str] | None = None,
        severity: str | None = None,
        include_remediation: bool = True,
        include_verification: bool = True,
    ) -> dict[str, Any]:
        """Get compliance requirements for infrastructure resources.

        Args:
            resource_types: List of resource types (RDS, S3, EC2, etc.)
            standards: List of compliance standards (PCI-DSS, HIPAA, etc.)
            severity: Filter by severity level
            include_remediation: Include remediation guidance
            include_verification: Include verification procedures

        Returns:
            Dictionary with compliance controls and summary
        """
        url = f"{self.api_url}/v1/compliance/requirements"
        payload = {
            "resource_types": resource_types,
            "standards": standards or [],
            "severity": severity,
            "include_remediation": include_remediation,
            "include_verification": include_verification,
        }

        from wistx_mcp.tools.lib.size_estimator import estimate_json_size
        
        estimated_size = estimate_json_size(payload)
        if estimated_size > 100000:
            raise ValueError(f"Request payload too large (estimated {estimated_size} bytes, max 100KB)")
        
        import json
        payload_size = len(json.dumps(payload))
        if payload_size > 100000:
            raise ValueError(f"Request payload too large: {payload_size} bytes (max 100KB)")

        from wistx_mcp.tools.lib.constants import API_TIMEOUT_SECONDS
        from wistx_mcp.tools.lib.url_validator import revalidate_url_before_request

        parsed_api_url = urlparse(self.api_url)
        is_localhost_api = (
            parsed_api_url.hostname in ("localhost", "127.0.0.1", "::1", "0.0.0.0")
            or parsed_api_url.hostname is None
        )
        
        try:
            await revalidate_url_before_request(
                url,
                block_private=not is_localhost_api,
                block_localhost=not is_localhost_api,
            )
        except ValueError as e:
            logger.error("URL validation failed before request: %s", e)
            raise RuntimeError(f"URL validation failed: {e}") from e

        async def _make_request() -> httpx.Response:
            return await with_timeout_and_retry(
                self.client.post,
                timeout_seconds=API_TIMEOUT_SECONDS,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                json=payload,
            )

        try:
            response = await _api_circuit_breaker.call(_make_request)
            response.raise_for_status()

            response_text = response.text
            logger.debug("API response status: %s, body length: %d", response.status_code, len(response_text) if response_text else 0)

            try:
                result = response.json()
                logger.debug("Parsed JSON result type: %s, keys: %s", type(result), list(result.keys()) if isinstance(result, dict) else "N/A")
            except ValueError as e:
                logger.error("Invalid JSON response from compliance API: %s. Response text: %s", e, response_text[:500])
                raise RuntimeError("Invalid JSON response from API") from e

            if result is None:
                logger.error("API returned null/None response body. Response text: %s", response_text[:500])
                raise RuntimeError("API returned null response")

            if not isinstance(result, dict):
                logger.error("Unexpected response type from compliance API: %s. Response text: %s", type(result), response_text[:500])
                raise RuntimeError("Invalid response format from API")

            if "data" not in result and "controls" not in result:
                logger.error("Response missing required fields: %s", list(result.keys()))
                raise RuntimeError("Invalid response structure: missing 'data' or 'controls'")

            if "controls" in result:
                if not isinstance(result["controls"], list):
                    logger.error("Controls field is not a list: %s", type(result["controls"]))
                    raise RuntimeError("Invalid controls structure: expected list")

                for i, control in enumerate(result["controls"]):
                    if not isinstance(control, dict):
                        logger.error("Control %d is not a dict: %s", i, type(control))
                        raise RuntimeError(f"Invalid control structure at index {i}")

            if "data" in result and isinstance(result["data"], dict):
                if "controls" in result["data"]:
                    if not isinstance(result["data"]["controls"], list):
                        logger.error("Data.controls field is not a list: %s", type(result["data"]["controls"]))
                        raise RuntimeError("Invalid data.controls structure: expected list")
                
                logger.info("Extracting data from APIResponse wrapper. Data keys: %s", list(result["data"].keys()))
                extracted_data = result["data"]
                logger.info("Extracted data type: %s, has controls: %s", type(extracted_data), "controls" in extracted_data)
                return extracted_data
            
            if "controls" in result:
                logger.info("Returning result with controls at top level. Result keys: %s", list(result.keys()))
                return result
            
            logger.error("Response missing required fields. Available keys: %s", list(result.keys()))
            raise RuntimeError("Invalid response structure: missing 'data' or 'controls'")
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code if e.response else None
            error_message = f"API error: {status_code}"
            
            if e.response:
                try:
                    error_body = e.response.json()
                    if isinstance(error_body, dict):
                        if "detail" in error_body:
                            detail = error_body["detail"]
                            if isinstance(detail, dict) and "error" in detail:
                                error_info = detail["error"]
                                if isinstance(error_info, dict):
                                    error_message = error_info.get("message", error_message)
                                    if "details" in error_info and isinstance(error_info["details"], dict):
                                        if "error" in error_info["details"]:
                                            error_message = f"{error_message}: {error_info['details']['error']}"
                            elif isinstance(detail, str):
                                error_message = detail
                except (ValueError, KeyError, TypeError):
                    pass
            
            logger.error(
                "HTTP error calling compliance API: %s (status: %s)",
                error_message,
                status_code,
            )
            if status_code == 401:
                raise ValueError("Invalid API key") from e
            elif status_code == 429:
                raise RuntimeError("Rate limit exceeded") from e
            elif status_code >= 500:
                raise RuntimeError(f"Server error: {status_code}") from e
            else:
                raise ValueError(error_message) from e
        except httpx.HTTPError as e:
            logger.error("HTTP error calling compliance API: %s", e)
            raise RuntimeError(f"HTTP error: {e}") from e
        except httpx.TimeoutException as e:
            logger.error("Timeout calling compliance API: %s", e)
            raise RuntimeError("Request timeout") from e

    async def research_knowledge_base(
        self,
        query: str,
        domains: list[str] | None = None,
        content_types: list[str] | None = None,
        include_cross_domain: bool = True,
        include_global: bool = True,
        response_format: str = "structured",
        max_results: int = 1000,
    ) -> dict[str, Any]:
        """Research knowledge base across all domains.

        Args:
            query: Research query in natural language
            domains: Filter by domains (compliance, finops, devops, etc.)
            content_types: Filter by content types (guide, pattern, etc.)
            include_cross_domain: Include cross-domain relationships
            include_global: Include global/shared knowledge base content
            response_format: Response format (structured, markdown, executive_summary)
            max_results: Maximum number of results

        Returns:
            Dictionary with research results and summary
        """
        url = f"{self.api_url}/v1/knowledge/research"
        payload = {
            "query": query,
            "domains": domains or [],
            "content_types": content_types or [],
            "include_cross_domain": include_cross_domain,
            "include_global": include_global,
            "format": response_format,
            "max_results": max_results,
        }

        try:
            from wistx_mcp.tools.lib.constants import TOOL_TIMEOUTS
            
            knowledge_base_timeout = TOOL_TIMEOUTS.get("wistx_research_knowledge_base", 90.0)
            api_timeout = min(knowledge_base_timeout - 10.0, 90.0)
            
            response = await with_timeout_and_retry(
                self.client.post,
                timeout_seconds=api_timeout,
                max_attempts=2,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                json=payload,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_message = f"API error: {e.response.status_code}"
            error_details = None
            
            if e.response:
                try:
                    error_body = e.response.json()
                    logger.debug("Knowledge API error response: %s", error_body)
                    if isinstance(error_body, dict):
                        if "detail" in error_body:
                            detail = error_body["detail"]
                            if isinstance(detail, dict) and "error" in detail:
                                error_info = detail["error"]
                                if isinstance(error_info, dict):
                                    error_message = error_info.get("message", error_message)
                                    error_details = error_info.get("details", None)
                                    if error_details:
                                        if isinstance(error_details, str):
                                            error_message = f"{error_message}: {error_details}"
                                        elif isinstance(error_details, dict):
                                            if "error" in error_details:
                                                error_message = f"{error_message}: {error_details['error']}"
                            elif isinstance(detail, str):
                                error_message = detail
                            elif isinstance(detail, list) and len(detail) > 0:
                                first_error = detail[0]
                                if isinstance(first_error, dict):
                                    if "msg" in first_error:
                                        error_message = first_error["msg"]
                                    if "loc" in first_error:
                                        error_message = f"{error_message} (field: {' -> '.join(str(loc) for loc in first_error['loc'])})"
                except (ValueError, KeyError, TypeError) as parse_error:
                    logger.debug("Failed to parse error response: %s", parse_error)
                    try:
                        error_text = e.response.text[:500]
                        logger.debug("Error response text: %s", error_text)
                    except Exception:
                        pass
            
            logger.error(
                "HTTP error calling knowledge API: %s (status: %s). Payload sent: query=%s, domains=%s, content_types=%s, include_cross_domain=%s, include_global=%s, format=%s, max_results=%s",
                error_message,
                e.response.status_code if e.response else None,
                query[:100] if query else None,
                domains,
                content_types,
                include_cross_domain,
                include_global,
                response_format,
                max_results,
            )
            if e.response and e.response.status_code in (400, 422):
                raise ValueError(f"Invalid request parameters: {error_message}") from e
            raise RuntimeError(f"Knowledge API error: {error_message}") from e
        except httpx.HTTPError as e:
            logger.error("HTTP error calling knowledge API: %s", e)
            raise RuntimeError(f"HTTP error: {e}") from e

    async def index_repository(
        self,
        repo_url: str,
        branch: str = "main",
        name: str | None = None,
        description: str | None = None,
        tags: list[str] | None = None,
        github_token: str | None = None,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Index a GitHub repository.

        Args:
            repo_url: GitHub repository URL
            branch: Branch to index
            name: Custom name for the resource
            description: Resource description
            tags: Tags for categorization
            github_token: GitHub token for private repos
            include_patterns: File path patterns to include (glob patterns)
            exclude_patterns: File path patterns to exclude (glob patterns)
            api_key: API key (overrides default)

        Returns:
            Dictionary with resource_id and status
        """
        url = f"{self.api_url}/v1/indexing/repositories"
        payload = {
            "repo_url": repo_url,
            "branch": branch,
        }
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if tags:
            payload["tags"] = tags
        if github_token:
            payload["github_token"] = github_token
        if include_patterns:
            payload["include_patterns"] = include_patterns
        if exclude_patterns:
            payload["exclude_patterns"] = exclude_patterns

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.post,
                timeout_seconds=60.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Error calling indexing API: %s", e)
            raise

    async def index_documentation(
        self,
        documentation_url: str,
        name: str | None = None,
        description: str | None = None,
        tags: list[str] | None = None,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Index a documentation website.

        Args:
            documentation_url: Documentation website URL
            name: Custom name for the resource
            description: Resource description
            tags: Tags for categorization
            include_patterns: URL patterns to include
            exclude_patterns: URL patterns to exclude
            api_key: API key (overrides default)

        Returns:
            Dictionary with resource_id and status
        """
        url = f"{self.api_url}/v1/indexing/documentation"
        payload = {"documentation_url": documentation_url}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if tags:
            payload["tags"] = tags
        if include_patterns:
            payload["include_patterns"] = include_patterns
        if exclude_patterns:
            payload["exclude_patterns"] = exclude_patterns

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.post,
                timeout_seconds=60.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Error calling indexing API: %s", e)
            raise

    async def index_document(
        self,
        document_url: str | None = None,
        file_path: str | None = None,
        document_type: str | None = None,
        name: str | None = None,
        description: str | None = None,
        tags: list[str] | None = None,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Index a document.

        Supports two modes:
        1. File upload (multipart): Provide file_path
        2. URL download (multipart): Provide document_url

        Args:
            document_url: Document URL (http/https) or local file path
            file_path: Local file path for direct upload (optional)
            document_type: Document type (pdf, docx, markdown, txt). Auto-detected from file_path if not provided.
            name: Custom name for the resource
            description: Resource description
            tags: Tags for categorization
            api_key: API key (overrides default)

        Returns:
            Dictionary with resource_id and status

        Raises:
            ValueError: If neither file_path nor document_url provided
            FileNotFoundError: If file_path provided but file doesn't exist
        """
        if not file_path and not document_url:
            raise ValueError("Either 'file_path' or 'document_url' must be provided")

        url = f"{self.api_url}/v1/indexing/documents"

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        headers.pop("Content-Type", None)

        try:
            if file_path:
                from wistx_mcp.tools.lib.path_validator import (
                    validate_file_path_for_upload,
                    PathValidationError,
                )
                
                try:
                    validated_path = validate_file_path_for_upload(
                        file_path,
                        allowed_base=None,
                        allow_symlinks=False,
                    )
                except PathValidationError as e:
                    raise ValueError(f"Invalid file path: {e}") from e
                
                file_path_obj = validated_path

                detected_type = document_type
                if not detected_type:
                    file_ext = file_path_obj.suffix.lower()
                    extension_to_type = {
                        ".pdf": "pdf",
                        ".docx": "docx",
                        ".md": "markdown",
                        ".markdown": "markdown",
                        ".txt": "txt",
                    }
                    detected_type = extension_to_type.get(file_ext)

                if not detected_type:
                    raise ValueError(
                        f"Could not determine document type from file: {file_path}. "
                        "Please provide 'document_type' parameter."
                    )

                # Read file atomically with TOCTOU protection
                try:
                    file_content = _read_file_atomic(file_path_obj)
                except RuntimeError as e:
                    raise ValueError(f"Failed to read file securely: {e}") from e

                # Create file-like object from bytes
                from io import BytesIO
                file_obj = BytesIO(file_content)

                files = {"file": (file_path_obj.name, file_obj, "application/octet-stream")}
                data = {
                    "document_type": detected_type,
                }
                if name:
                    data["name"] = name
                if description:
                    data["description"] = description
                if tags:
                    data["tags"] = json.dumps(tags)

                response = await with_timeout_and_retry(
                    self.client.post,
                    timeout_seconds=120.0,
                    max_attempts=3,
                    retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                    url=url,
                    files=files,
                    data=data,
                    headers=headers,
                )

            elif document_url:
                data = {
                    "document_url": document_url,
                }
                if document_type:
                    data["document_type"] = document_type
                if name:
                    data["name"] = name
                if description:
                    data["description"] = description
                if tags:
                    data["tags"] = json.dumps(tags)

                response = await with_timeout_and_retry(
                    self.client.post,
                    timeout_seconds=60.0,
                    max_attempts=3,
                    retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                    url=url,
                    data=data,
                    headers=headers,
                )

            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Error calling indexing API: %s", e)
            raise

    async def list_resources(
        self,
        resource_type: str | None = None,
        status: str | None = None,
        deduplicate: bool = True,
        show_duplicates: bool = False,
        include_ai_analysis: bool = True,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """List indexed resources with enhanced options.

        Args:
            resource_type: Filter by resource type
            status: Filter by status
            deduplicate: Show only latest completed resource per repo (default: True)
            show_duplicates: Include duplicate information (default: False)
            include_ai_analysis: Include AI insights (default: True)
            api_key: API key (overrides default)

        Returns:
            Dictionary with list of resources and summary
        """
        url = f"{self.api_url}/v1/indexing/resources"
        params = {}
        if resource_type:
            params["resource_type"] = resource_type
        if status:
            params["status"] = status
        params["deduplicate"] = str(deduplicate).lower()
        params["show_duplicates"] = str(show_duplicates).lower()
        params["include_ai_analysis"] = str(include_ai_analysis).lower()

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.get,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                params=params,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Error calling indexing API: %s", e)
            raise

    async def get_resource(
        self,
        resource_id: str,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Get resource details.

        Args:
            resource_id: Resource ID
            api_key: API key (overrides default)

        Returns:
            Dictionary with resource details
        """
        url = f"{self.api_url}/v1/indexing/resources/{resource_id}"

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.get,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Error calling indexing API: %s", e)
            raise

    async def delete_resource(
        self,
        resource_id: str,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Delete indexed resource by resource_id (legacy method).

        Args:
            resource_id: Resource ID
            api_key: API key (overrides default)

        Returns:
            Empty dict (204 No Content)
        """
        url = f"{self.api_url}/v1/indexing/resources/{resource_id}"

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.delete,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                headers=headers,
            )
            response.raise_for_status()
            return {}
        except httpx.HTTPError as e:
            logger.error("Error calling indexing API: %s", e)
            raise

    async def delete_resource_by_identifier(
        self,
        resource_type: str,
        identifier: str,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Delete indexed resource by type and identifier.

        Args:
            resource_type: Type of resource ("repository", "documentation", or "document")
            identifier: Resource identifier (repo URL, doc URL, or resource_id)
            api_key: API key (overrides default)

        Returns:
            Empty dict (204 No Content)
        """
        url = f"{self.api_url}/v1/indexing/resources"
        params = {
            "resource_type": resource_type,
            "identifier": identifier,
        }

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.delete,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                params=params,
                headers=headers,
            )
            response.raise_for_status()
            return {}
        except httpx.HTTPError as e:
            logger.error("Error calling indexing API: %s", e)
            raise

    async def get_current_user(
        self,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Get current user information from API key.

        Args:
            api_key: API key (overrides default)

        Returns:
            Dictionary with user information (user_id, organization_id, plan, etc.)

        Raises:
            ValueError: If API key is invalid
        """
        url = f"{self.api_url}/v1/users/me"

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.get,
                timeout_seconds=120.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()

            user_id = data.get("user_id")
            if not user_id:
                raise ValueError("Could not determine user_id from API key")

            return {
                "user_id": str(user_id),
                "organization_id": data.get("organization_id"),
                "plan": data.get("plan", "free"),
            }
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ValueError("Invalid or expired API key") from e
            logger.error("Error calling users API: %s", e)
            raise
        except httpx.HTTPError as e:
            logger.error("Error calling users API: %s", e)
            raise

    async def find_resource_by_repo_url(
        self,
        api_key: str = "",
        repository_url: str = "",
    ) -> dict[str, Any] | None:
        """Find indexed resource by repository URL.

        Args:
            api_key: API key for authentication
            repository_url: Repository URL

        Returns:
            Resource dictionary or None if not found
        """
        url = f"{self.api_url}/v1/indexing/resources"
        params = {"resource_type": "repository"}
        
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        
        try:
            response = await with_timeout_and_retry(
                self.client.get,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                params=params,
                headers=headers,
            )
            response.raise_for_status()
            
            result = response.json()
            resources = result.get("resources", [])
            
            normalized_url = repository_url.replace(".git", "").rstrip("/")
            for resource in resources:
                repo_url = resource.get("repo_url", "")
                if repo_url.replace(".git", "").rstrip("/") == normalized_url:
                    return resource
            
            return None
        except Exception as e:
            logger.error("Error finding resource by repo URL: %s", e)
            return None

    async def get_cost_analysis(
        self,
        api_key: str = "",
        resource_id: str = "",
        refresh: bool = False,
    ) -> dict[str, Any] | None:
        """Get cost analysis for indexed repository.

        Args:
            api_key: API key for authentication
            resource_id: Resource ID
            refresh: Force recalculation

        Returns:
            Cost analysis dictionary or None if not found
        """
        url = f"{self.api_url}/v1/indexing/resources/{resource_id}/cost-analysis"
        params = {"refresh": refresh}
        
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        
        try:
            response = await with_timeout_and_retry(
                self.client.get,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                params=params,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            logger.error("Error calling cost analysis API: %s", e)
            raise RuntimeError(f"Failed to get cost analysis: {e}") from e
        except Exception as e:
            logger.error("Error calling cost analysis API: %s", e)
            raise RuntimeError(f"Failed to get cost analysis: {e}") from e

    async def get_compliance_analysis(
        self,
        api_key: str = "",
        resource_id: str = "",
        standards: list[str] | None = None,
        refresh: bool = False,
    ) -> dict[str, Any] | None:
        """Get compliance analysis for indexed repository.

        Args:
            api_key: API key for authentication
            resource_id: Resource ID
            standards: Filter by compliance standards
            refresh: Force recalculation

        Returns:
            Compliance analysis dictionary or None if not found
        """
        url = f"{self.api_url}/v1/indexing/resources/{resource_id}/compliance-analysis"
        params = {"refresh": refresh}
        if standards:
            params["standards"] = standards
        
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        
        try:
            response = await with_timeout_and_retry(
                self.client.get,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                params=params,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            logger.error("Error calling compliance analysis API: %s", e)
            raise RuntimeError(f"Failed to get compliance analysis: {e}") from e
        except Exception as e:
            logger.error("Error calling compliance analysis API: %s", e)
            raise RuntimeError(f"Failed to get compliance analysis: {e}") from e

    async def get_infrastructure_inventory(
        self,
        repository_url: str | None = None,
        environment_name: str | None = None,
        inventory_id: str | None = None,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Get infrastructure inventory (DEPRECATED - use analysis endpoints instead).

        Args:
            repository_url: Repository URL (optional filter)
            environment_name: Environment name (optional filter)
            inventory_id: Specific inventory ID (optional)
            api_key: API key (overrides default)

        Returns:
            Dictionary with infrastructure inventory

        Raises:
            ValueError: If API key is invalid
        """
        url = f"{self.api_url}/v1/infrastructure/inventory"
        params = {}
        if repository_url:
            params["repository_url"] = repository_url
        if environment_name:
            params["environment_name"] = environment_name
        if inventory_id:
            params["inventory_id"] = inventory_id

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.get,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                params=params,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ValueError("Invalid or expired API key") from e
            logger.error("Error calling infrastructure API: %s", e)
            raise
        except httpx.HTTPError as e:
            logger.error("Error calling infrastructure API: %s", e)
            raise

    async def search_codebase(
        self,
        query: str,
        repositories: list[str] | None = None,
        resource_ids: list[str] | None = None,
        resource_types: list[str] | None = None,
        file_types: list[str] | None = None,
        code_type: str | None = None,
        cloud_provider: str | None = None,
        include_sources: bool = True,
        include_ai_analysis: bool = True,
        limit: int = 1000,
        api_key: str | None = None,
        check_freshness: bool = False,
        include_fresh_content: bool = False,
        max_stale_minutes: int = 60,
    ) -> dict[str, Any]:
        """Search user's indexed codebase.

        Args:
            query: Natural language search question
            repositories: List of repositories to search
            resource_ids: Filter by specific indexed resources
            resource_types: Filter by resource type
            file_types: Filter by file extensions
            code_type: Filter by code type
            cloud_provider: Filter by cloud provider
            include_sources: Include source code snippets
            include_ai_analysis: Include AI-analyzed results
            limit: Maximum number of results
            api_key: API key (overrides default)
            check_freshness: Check if indexed content is stale
            include_fresh_content: Fetch fresh content for stale results
            max_stale_minutes: Consider content stale if older than this

        Returns:
            Dictionary with search results
        """
        url = f"{self.api_url}/v1/search/codebase"
        payload = {
            "query": query,
            "include_sources": include_sources,
            "include_ai_analysis": include_ai_analysis,
            "limit": limit,
            "check_freshness": check_freshness,
            "include_fresh_content": include_fresh_content,
            "max_stale_minutes": max_stale_minutes,
        }
        if repositories:
            payload["repositories"] = repositories
        if resource_ids:
            payload["resource_ids"] = resource_ids
        if resource_types:
            payload["resource_types"] = resource_types
        if file_types:
            payload["file_types"] = file_types
        if code_type:
            payload["code_type"] = code_type
        if cloud_provider:
            payload["cloud_provider"] = cloud_provider

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.post,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Error calling codebase search API: %s", e)
            raise

    async def search_packages(
        self,
        query: str | None = None,
        pattern: str | None = None,
        template: str | None = None,
        search_type: str = "semantic",
        registry: str | None = None,
        domain: str | None = None,
        category: str | None = None,
        package_name: str | None = None,
        limit: int = 1000,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Search DevOps/infrastructure packages.

        Args:
            query: Natural language search query
            pattern: Regex pattern
            template: Pre-built template name
            search_type: Search type (semantic, regex, hybrid)
            registry: Filter by registry
            domain: Filter by domain
            category: Filter by category
            package_name: Search specific package
            limit: Maximum results
            api_key: API key (overrides default)

        Returns:
            Dictionary with package search results
        """
        url = f"{self.api_url}/v1/search/packages"
        payload = {
            "search_type": search_type,
            "limit": limit,
        }
        if query:
            payload["query"] = query
        if pattern:
            payload["pattern"] = pattern
        if template:
            payload["template"] = template
        if registry:
            payload["registry"] = registry
        if domain:
            payload["domain"] = domain
        if category:
            payload["category"] = category
        if package_name:
            payload["package_name"] = package_name

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.post,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Error calling package search API: %s", e)
            raise

    async def design_architecture(
        self,
        action: str,
        project_type: str | None = None,
        project_name: str | None = None,
        architecture_type: str | None = None,
        cloud_provider: str | None = None,
        compliance_standards: list[str] | None = None,
        requirements: dict[str, Any] | None = None,
        existing_architecture: str | None = None,
        output_directory: str = ".",
        template_id: str | None = None,
        github_url: str | None = None,
        user_template: dict[str, Any] | None = None,
        include_compliance: bool = True,
        include_security: bool = True,
        include_best_practices: bool = True,
        api_key: str | None = None,
        user_id: str | None = None,
        organization_id: str | None = None,
        use_cache: bool = True,
    ) -> dict[str, Any]:
        """Design architecture via REST API.

        Args:
            action: Action type
            project_type: Project type
            project_name: Project name
            architecture_type: Architecture type
            cloud_provider: Cloud provider
            compliance_standards: Compliance standards
            requirements: Requirements dict
            existing_architecture: Existing architecture code
            output_directory: Output directory
            template_id: Template ID
            github_url: GitHub URL
            user_template: User template
            include_compliance: Include compliance
            include_security: Include security
            include_best_practices: Include best practices
            api_key: API key
            user_id: User ID (for caching)
            organization_id: Organization ID (for caching)
            use_cache: Whether to use cache

        Returns:
            API response dictionary
        """
        url = f"{self.api_url}/v1/architecture/design"

        payload: dict[str, Any] = {
            "action": action,
        }
        if project_type:
            payload["project_type"] = project_type
        if project_name:
            payload["project_name"] = project_name
        if architecture_type:
            payload["architecture_type"] = architecture_type
        if cloud_provider:
            payload["cloud_provider"] = cloud_provider
        if compliance_standards:
            payload["compliance_standards"] = compliance_standards
        if requirements:
            payload["requirements"] = requirements
        if existing_architecture:
            payload["existing_architecture"] = existing_architecture
        if output_directory:
            payload["output_directory"] = output_directory
        if template_id:
            payload["template_id"] = template_id
        if github_url:
            payload["github_url"] = github_url
        if user_template:
            payload["user_template"] = user_template
        payload["include_compliance"] = include_compliance
        payload["include_security"] = include_security
        payload["include_best_practices"] = include_best_practices

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.post,
                timeout_seconds=60.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                try:
                    error_detail = e.response.json()
                    logger.error(
                        "Error calling architecture API (400 Bad Request): %s | Response: %s | Payload keys: %s",
                        e,
                        error_detail,
                        list(payload.keys()),
                    )
                except Exception:
                    logger.error(
                        "Error calling architecture API (400 Bad Request): %s | Payload keys: %s",
                        e,
                        list(payload.keys()),
                    )
            else:
                logger.error("Error calling architecture API: %s", e)
            raise
        except httpx.HTTPError as e:
            logger.error("Error calling architecture API: %s", e)
            raise

    async def design_architecture_legacy(
        self,
        action: str,
        project_type: str | None = None,
        project_name: str | None = None,
        architecture_type: str | None = None,
        cloud_provider: str | None = None,
        compliance_standards: list[str] | None = None,
        requirements: dict[str, Any] | None = None,
        existing_architecture: str | None = None,
        output_directory: str = ".",
        template_id: str | None = None,
        github_url: str | None = None,
        user_template: dict[str, Any] | None = None,
        include_compliance: bool = True,
        include_security: bool = True,
        include_best_practices: bool = True,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Design architecture for DevOps/infrastructure projects.

        Args:
            action: Action to perform (initialize, design, review, optimize)
            project_type: Type of project
            project_name: Name of the project
            architecture_type: Architecture pattern
            cloud_provider: Cloud provider
            compliance_standards: Compliance standards to include
            requirements: Project requirements
            existing_architecture: Existing architecture code/documentation
            output_directory: Directory to create project
            template_id: Template ID from MongoDB registry
            github_url: GitHub repository URL for template
            user_template: User-provided template dictionary
            include_compliance: Include compliance requirements context
            include_security: Include security knowledge context
            include_best_practices: Include best practices from knowledge base
            api_key: API key (overrides default)

        Returns:
            Dictionary with architecture design results
        """
        url = f"{self.api_url}/v1/architecture/design"
        payload = {
            "action": action,
            "output_directory": output_directory,
            "include_compliance": include_compliance,
            "include_security": include_security,
            "include_best_practices": include_best_practices,
        }
        if project_type:
            payload["project_type"] = project_type
        if project_name:
            payload["project_name"] = project_name
        if architecture_type:
            payload["architecture_type"] = architecture_type
        if cloud_provider:
            payload["cloud_provider"] = cloud_provider
        if compliance_standards:
            payload["compliance_standards"] = compliance_standards
        if requirements:
            payload["requirements"] = requirements
        if existing_architecture:
            payload["existing_architecture"] = existing_architecture
        if template_id:
            payload["template_id"] = template_id
        if github_url:
            payload["github_url"] = github_url
        if user_template:
            payload["user_template"] = user_template

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.post,
                timeout_seconds=60.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Error calling architecture design API: %s", e)
            raise

    async def manage_infrastructure(
        self,
        action: str,
        infrastructure_type: str,
        resource_name: str,
        cloud_provider: str | list[str] | None = None,
        configuration: dict[str, Any] | None = None,
        compliance_standards: list[str] | None = None,
        current_version: str | None = None,
        target_version: str | None = None,
        backup_type: str = "full",
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Manage infrastructure lifecycle.

        Args:
            action: Action to perform (create, update, upgrade, backup, restore, monitor, optimize)
            infrastructure_type: Type of infrastructure
            resource_name: Name of the resource/cluster
            cloud_provider: Cloud provider(s)
            configuration: Infrastructure configuration
            compliance_standards: Compliance standards to enforce
            current_version: Current version (for upgrade action)
            target_version: Target version (for upgrade action)
            backup_type: Type of backup (for backup action)
            api_key: API key (overrides default)

        Returns:
            Dictionary with infrastructure management result
        """
        url = f"{self.api_url}/v1/infrastructure/manage"
        payload = {
            "action": action,
            "infrastructure_type": infrastructure_type,
            "resource_name": resource_name,
            "backup_type": backup_type,
        }
        if cloud_provider:
            payload["cloud_provider"] = cloud_provider if isinstance(cloud_provider, list) else [cloud_provider]
        if configuration:
            payload["configuration"] = configuration
        if compliance_standards:
            payload["compliance_standards"] = compliance_standards
        if current_version:
            payload["current_version"] = current_version
        if target_version:
            payload["target_version"] = target_version

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.post,
                timeout_seconds=60.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Error calling infrastructure management API: %s", e)
            raise

    async def regex_search(
        self,
        pattern: str | None = None,
        template: str | None = None,
        repositories: list[str] | None = None,
        resource_ids: list[str] | None = None,
        resource_types: list[str] | None = None,
        file_types: list[str] | None = None,
        code_type: str | None = None,
        cloud_provider: str | None = None,
        case_sensitive: bool = False,
        multiline: bool = False,
        dotall: bool = False,
        include_context: bool = True,
        context_lines: int = 3,
        limit: int = 1000,
        timeout: float = 30.0,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Search codebase using regex patterns.

        Args:
            pattern: Regular expression pattern
            template: Pre-built pattern template
            repositories: List of repositories to search
            resource_ids: Filter by specific indexed resources
            resource_types: Filter by resource type
            file_types: Filter by file extensions
            code_type: Filter by code type
            cloud_provider: Filter by cloud provider
            case_sensitive: Case-sensitive matching
            multiline: Multiline mode
            dotall: Dot matches newline
            include_context: Include surrounding code context
            context_lines: Number of lines before/after match
            limit: Maximum number of results
            timeout: Maximum search time in seconds
            api_key: API key (overrides default)

        Returns:
            Dictionary with regex search results
        """
        url = f"{self.api_url}/v1/search/regex"
        payload = {
            "case_sensitive": case_sensitive,
            "multiline": multiline,
            "dotall": dotall,
            "include_context": include_context,
            "context_lines": context_lines,
            "limit": limit,
            "timeout": timeout,
        }
        if pattern:
            payload["pattern"] = pattern
        if template:
            payload["template"] = template
        if repositories:
            payload["repositories"] = repositories
        if resource_ids:
            payload["resource_ids"] = resource_ids
        if resource_types:
            payload["resource_types"] = resource_types
        if file_types:
            payload["file_types"] = file_types
        if code_type:
            payload["code_type"] = code_type
        if cloud_provider:
            payload["cloud_provider"] = cloud_provider

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.post,
                timeout_seconds=timeout + 10.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Error calling regex search API: %s", e)
            raise

    async def web_search(
        self,
        query: str,
        search_type: str = "general",
        resource_type: str | None = None,
        cloud_provider: str | None = None,
        severity: str | None = None,
        include_cves: bool = True,
        include_advisories: bool = True,
        limit: int = 1000,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Search the web for DevOps/infrastructure information.

        Args:
            query: Search query
            search_type: Type of search (general, security)
            resource_type: Filter by resource type
            cloud_provider: Filter by cloud provider
            severity: Filter by severity (for security searches)
            include_cves: Include CVE database results
            include_advisories: Include security advisories
            limit: Maximum number of results
            api_key: API key (overrides default)

        Returns:
            Dictionary with web search results
        """
        url = f"{self.api_url}/v1/search/web"
        payload = {
            "query": query,
            "search_type": search_type,
            "include_cves": include_cves,
            "include_advisories": include_advisories,
            "limit": limit,
        }
        if resource_type:
            payload["resource_type"] = resource_type
        if cloud_provider:
            payload["cloud_provider"] = cloud_provider
        if severity:
            payload["severity"] = severity

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.post,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Error calling web search API: %s", e)
            raise

    async def troubleshoot_issue(
        self,
        issue_description: str,
        infrastructure_type: str | None = None,
        cloud_provider: str | None = None,
        error_messages: list[str] | None = None,
        configuration_code: str | None = None,
        logs: str | None = None,
        resource_type: str | None = None,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Troubleshoot infrastructure and code issues.

        Args:
            issue_description: Description of the issue
            infrastructure_type: Type of infrastructure
            cloud_provider: Cloud provider
            error_messages: List of error messages
            configuration_code: Relevant configuration code
            logs: Log output
            resource_type: Resource type
            api_key: API key (overrides default)

        Returns:
            Dictionary with troubleshooting results
        """
        url = f"{self.api_url}/v1/troubleshoot/issue"
        payload = {
            "issue_description": issue_description,
        }
        if infrastructure_type:
            payload["infrastructure_type"] = infrastructure_type
        if cloud_provider:
            payload["cloud_provider"] = cloud_provider
        if error_messages:
            payload["error_messages"] = error_messages
        if configuration_code:
            payload["configuration_code"] = configuration_code
        if logs:
            payload["logs"] = logs
        if resource_type:
            payload["resource_type"] = resource_type

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.post,
                timeout_seconds=60.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Error calling troubleshoot API: %s", e)
            raise

    async def read_package_file(
        self,
        registry: str,
        package_name: str,
        filename_sha256: str,
        start_line: int,
        end_line: int,
        version: str | None = None,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Read specific file sections from package source code.

        Args:
            registry: Package registry
            package_name: Package name
            filename_sha256: SHA256 hash of filename
            start_line: Starting line (1-based)
            end_line: Ending line
            version: Optional package version
            api_key: API key (overrides default)

        Returns:
            Dictionary with file content
        """
        url = f"{self.api_url}/v1/search/packages/read-file"
        payload = {
            "registry": registry,
            "package_name": package_name,
            "filename_sha256": filename_sha256,
            "start_line": start_line,
            "end_line": end_line,
        }
        if version:
            payload["version"] = version

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.post,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Error calling read package file API: %s", e)
            raise


    async def list_filesystem(
        self,
        resource_id: str,
        path: str = "/",
        view_mode: str = "standard",
        include_metadata: bool = False,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """List directory contents in virtual filesystem.

        Args:
            resource_id: Resource ID
            path: Directory path
            view_mode: View mode (standard, infrastructure, compliance, costs, security)
            include_metadata: Include full infrastructure metadata
            api_key: API key (overrides default)

        Returns:
            Dictionary with directory listing
        """
        url = f"{self.api_url}/v1/filesystem/{resource_id}/list"
        payload = {
            "path": path,
            "view_mode": view_mode,
            "include_metadata": include_metadata,
        }

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.post,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Error calling list filesystem API: %s", e)
            raise

    async def read_file_with_context(
        self,
        resource_id: str,
        path: str,
        start_line: int | None = None,
        end_line: int | None = None,
        include_dependencies: bool = False,
        include_compliance: bool = False,
        include_costs: bool = False,
        include_security: bool = False,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Read file from virtual filesystem with optional context.

        Args:
            resource_id: Resource ID
            path: Virtual filesystem path
            start_line: Start line number (1-based)
            end_line: End line number (1-based)
            include_dependencies: Include file dependencies
            include_compliance: Include compliance controls
            include_costs: Include cost estimates
            include_security: Include security issues
            api_key: API key (overrides default)

        Returns:
            Dictionary with file content and context
        """
        url = f"{self.api_url}/v1/filesystem/{resource_id}/read"
        payload = {
            "path": path,
            "include_dependencies": include_dependencies,
            "include_compliance": include_compliance,
            "include_costs": include_costs,
            "include_security": include_security,
        }
        if start_line is not None:
            payload["start_line"] = start_line
        if end_line is not None:
            payload["end_line"] = end_line

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.post,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Error calling read file with context API: %s", e)
            raise

    async def get_filesystem_tree(
        self,
        resource_id: str,
        root_path: str = "/",
        max_depth: int = 10,
        view_mode: str = "standard",
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Get filesystem tree structure.

        Args:
            resource_id: Resource ID
            root_path: Root path for tree
            max_depth: Maximum depth to traverse
            view_mode: View mode (standard, infrastructure, compliance, costs, security)
            api_key: API key (overrides default)

        Returns:
            Dictionary with tree structure
        """
        url = f"{self.api_url}/v1/filesystem/{resource_id}/tree"
        payload = {
            "root_path": root_path,
            "max_depth": max_depth,
            "view_mode": view_mode,
        }

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.post,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Error calling get filesystem tree API: %s", e)
            raise

    async def glob_infrastructure(
        self,
        resource_id: str,
        pattern: str,
        entry_type: str | None = None,
        code_type: str | None = None,
        cloud_provider: str | None = None,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Find filesystem entries matching glob pattern.

        Args:
            resource_id: Resource ID
            pattern: Glob pattern
            entry_type: Filter by entry type
            code_type: Filter by code type
            cloud_provider: Filter by cloud provider
            api_key: API key (overrides default)

        Returns:
            Dictionary with matching entries
        """
        url = f"{self.api_url}/v1/filesystem/{resource_id}/glob"
        payload = {"pattern": pattern}
        if entry_type:
            payload["entry_type"] = entry_type
        if code_type:
            payload["code_type"] = code_type
        if cloud_provider:
            payload["cloud_provider"] = cloud_provider

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.post,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Error calling glob infrastructure API: %s", e)
            raise


    async def save_context_with_analysis(
        self,
        context_type: str,
        title: str,
        summary: str,
        description: str | None = None,
        conversation_history: list[dict[str, Any]] | None = None,
        code_snippets: list[dict[str, Any]] | None = None,
        plans: list[dict[str, Any]] | None = None,
        decisions: list[dict[str, Any]] | None = None,
        infrastructure_resources: list[dict[str, Any]] | None = None,
        linked_resources: list[str] | None = None,
        tags: list[str] | None = None,
        workspace: str | None = None,
        auto_analyze: bool = True,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Save context with automatic analysis.

        Args:
            context_type: Type of context
            title: Context title
            summary: Context summary
            description: Detailed description
            conversation_history: Conversation history
            code_snippets: Code snippets
            plans: Plans or workflows
            decisions: Decisions made
            infrastructure_resources: Infrastructure resources
            linked_resources: Linked resource IDs
            tags: Tags
            workspace: Workspace identifier
            auto_analyze: Automatically analyze
            api_key: API key (overrides default)

        Returns:
            Dictionary with saved context
        """
        url = f"{self.api_url}/v1/contexts"
        payload = {
            "context_type": context_type,
            "title": title,
            "summary": summary,
            "auto_analyze": auto_analyze,
        }
        if description:
            payload["description"] = description
        if conversation_history:
            payload["conversation_history"] = conversation_history
        if code_snippets:
            payload["code_snippets"] = code_snippets
        if plans:
            payload["plans"] = plans
        if decisions:
            payload["decisions"] = decisions
        if infrastructure_resources:
            payload["infrastructure_resources"] = infrastructure_resources
        if linked_resources:
            payload["linked_resources"] = linked_resources
        if tags:
            payload["tags"] = tags
        if workspace:
            payload["workspace"] = workspace

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.post,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 422:
                try:
                    error_detail = e.response.json()
                    logger.error(
                        "Validation error calling save context with analysis API (422): %s. Payload keys: %s",
                        error_detail,
                        list(payload.keys()),
                    )
                except Exception:
                    logger.error(
                        "Validation error calling save context with analysis API (422). Response: %s. Payload keys: %s",
                        e.response.text[:500],
                        list(payload.keys()),
                    )
            else:
                logger.error("Error calling save context with analysis API: %s", e)
            raise
        except httpx.HTTPError as e:
            logger.error("Error calling save context with analysis API: %s", e)
            raise

    async def search_contexts_intelligently(
        self,
        query: str,
        context_type: str | None = None,
        compliance_standard: str | None = None,
        cost_range: dict[str, float] | None = None,
        security_score_min: float | None = None,
        limit: int = 50,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Search contexts intelligently.

        Args:
            query: Search query
            context_type: Filter by context type
            compliance_standard: Filter by compliance standard
            cost_range: Filter by cost range
            security_score_min: Minimum security score
            limit: Maximum results
            api_key: API key (overrides default)

        Returns:
            Dictionary with search results
        """
        url = f"{self.api_url}/v1/contexts/search"
        payload = {"query": query, "limit": limit}
        if context_type:
            payload["context_type"] = context_type
        if compliance_standard:
            payload["compliance_standard"] = compliance_standard
        if cost_range:
            payload["cost_range"] = cost_range
        if security_score_min is not None:
            payload["security_score_min"] = security_score_min

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.post,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Error calling search contexts intelligently API: %s", e)
            raise

    async def get_context(
        self,
        context_id: str,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Get context by ID.

        Args:
            context_id: Context ID
            api_key: API key (overrides default)

        Returns:
            Dictionary with context details
        """
        url = f"{self.api_url}/v1/contexts/{context_id}"

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.get,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Error calling get context API: %s", e)
            raise

    async def list_contexts(
        self,
        context_type: str | None = None,
        status: str | None = None,
        workspace: str | None = None,
        tags: list[str] | None = None,
        limit: int = 100,
        offset: int = 0,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """List contexts with filtering.

        Args:
            context_type: Filter by context type
            status: Filter by status
            workspace: Filter by workspace
            tags: Filter by tags
            limit: Maximum results
            offset: Offset for pagination
            api_key: API key (overrides default)

        Returns:
            Dictionary with contexts list
        """
        url = f"{self.api_url}/v1/contexts"
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if context_type:
            params["context_type"] = context_type
        if status:
            params["status"] = status
        if workspace:
            params["workspace"] = workspace
        if tags:
            params["tags"] = ",".join(tags)

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.get,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                params=params,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Error calling list contexts API: %s", e)
            raise

    async def link_contexts(
        self,
        source_context_id: str,
        target_context_id: str,
        relationship_type: str,
        strength: float = 1.0,
        metadata: dict[str, Any] | None = None,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Link contexts.

        Args:
            source_context_id: Source context ID
            target_context_id: Target context ID
            relationship_type: Relationship type
            strength: Relationship strength
            metadata: Additional metadata
            api_key: API key (overrides default)

        Returns:
            Dictionary with link information
        """
        url = f"{self.api_url}/v1/contexts/{source_context_id}/links"
        payload = {
            "target_context_id": target_context_id,
            "relationship_type": relationship_type,
            "strength": strength,
        }
        if metadata:
            payload["metadata"] = metadata

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.post,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Error calling link contexts API: %s", e)
            raise

    async def get_context_graph(
        self,
        context_id: str,
        depth: int = 2,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Get context dependency graph.

        Args:
            context_id: Root context ID
            depth: Maximum depth
            api_key: API key (overrides default)

        Returns:
            Dictionary with graph structure
        """
        url = f"{self.api_url}/v1/contexts/{context_id}/graph"
        params = {"depth": depth}

        headers = self.client.headers.copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = await with_timeout_and_retry(
                self.client.get,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                params=params,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Error calling get context graph API: %s", e)
            raise


async def get_api_client(api_key: str | None = None, api_url: str | None = None) -> WISTXAPIClient:
    """Get or create global API client instance.

    Args:
        api_key: API key (optional, uses default if not provided)
        api_url: API URL (optional, uses default if not provided)

    Returns:
        WISTXAPIClient instance
    """
    global _global_api_client

    async with _api_client_lock:
        if _global_api_client is None:
            _global_api_client = WISTXAPIClient(api_key=api_key, api_url=api_url)
        else:
            needs_recreate = False
            
            if api_key:
                current_key = _global_api_client._get_api_key()
                if current_key != api_key:
                    needs_recreate = True
            
            if api_url:
                current_url = _global_api_client.api_url
                if current_url != api_url.rstrip("/"):
                    needs_recreate = True
            
            if needs_recreate:
                await _global_api_client.close()
                _global_api_client = WISTXAPIClient(api_key=api_key, api_url=api_url)

        return _global_api_client

