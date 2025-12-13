"""WISTX MCP Server main entry point."""

import asyncio
import hashlib
import json
import logging
import os
import re
import signal
import sys
import time
import uuid
import warnings
from contextvars import ContextVar
from typing import Any
import httpx

if sys.version_info < (3, 11):
    raise RuntimeError(f"Python 3.11+ required, found {sys.version_info.major}.{sys.version_info.minor}")

warnings.filterwarnings("ignore")
warnings.simplefilter("ignore")

if not sys.warnoptions:
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=ImportWarning)
    warnings.filterwarnings("ignore", category=UnicodeWarning)
    warnings.filterwarnings("ignore", category=BytesWarning)
    warnings.filterwarnings("ignore", category=ResourceWarning)

os.environ["PYTHONWARNINGS"] = "ignore"

if not logging.getLogger().handlers:
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

if sys.version_info >= (3, 13):
    logger.debug(
        "Python %d.%d is very new and may have compatibility issues. "
        "Consider using Python 3.11 or 3.12 for better stability.",
        sys.version_info.major,
        sys.version_info.minor,
    )

if sys.version_info[:2] == (3, 11):
    logger.debug("Python 3.11 detected. If you experience crashes, try Python 3.12 instead.")

import typing
typing_file = typing.__file__
expected_version = f"{sys.version_info.major}.{sys.version_info.minor}"
if expected_version not in typing_file:
    raise RuntimeError(
        f"Python version mismatch detected! "
        f"Running Python {sys.version_info.major}.{sys.version_info.minor} but typing module is from: {typing_file}. "
        f"This indicates a corrupted Python environment. Please recreate your virtual environment."
    )

_original_sys_exit = sys.exit

def _mcp_safe_exit(code: int = 0) -> None:
    """MCP-safe sys.exit that raises SystemExit instead of exiting.
    
    This allows api.config to fail initialization without killing the MCP server.
    """
    raise SystemExit(code)

def _safe_import_with_sys_exit_patch(module_name: str, fallback: Any = None) -> Any:
    """Safely import a module that might call sys.exit, with temporary sys.exit patching."""
    sys.exit = _mcp_safe_exit
    try:
        return __import__(module_name, fromlist=[""])
    except SystemExit:
        return fallback
    finally:
        sys.exit = _original_sys_exit

_original_stdout = sys.stdout
_original_stderr = sys.stderr

class _SuppressStdout:
    def write(self, s):
        pass
    def flush(self):
        pass

_suppress_stdout = _SuppressStdout()

try:
    sys.exit = _mcp_safe_exit
    sys.stdout = _suppress_stdout
    try:
        from wistx_mcp.config import settings
    finally:
        sys.stdout = _original_stdout
    sys.exit = _original_sys_exit
    settings.reload_from_env()
except SystemExit as e:
    sys.exit = _original_sys_exit
    sys.stdout = _original_stdout
    logging.basicConfig(level=logging.WARNING)
    logger.warning("Failed to load MCP config, using defaults")
    sys.stdout = _suppress_stdout
    try:
        from wistx_mcp.config import MCPServerSettings
        settings = MCPServerSettings()
    finally:
        sys.stdout = _original_stdout

try:
    sys.exit = _mcp_safe_exit
    sys.stdout = _suppress_stdout
    try:
        from wistx_mcp.tools.lib.auth_context import AuthContext, get_auth_context, set_auth_context
    finally:
        sys.stdout = _original_stdout
    sys.exit = _original_sys_exit
except SystemExit:
    sys.exit = _original_sys_exit
    sys.stdout = _original_stdout
    logger.warning("Failed to import auth_context (api.config dependency issue), continuing without it")
    AuthContext = None
    get_auth_context = lambda: None
    set_auth_context = lambda x: None
from wistx_mcp.tools.lib.concurrent_limiter import get_concurrent_limiter
from wistx_mcp.tools.lib.input_sanitizer import sanitize_tool_arguments
from wistx_mcp.tools.lib.logging_utils import safe_json_dumps, sanitize_error_message, sanitize_arguments
from wistx_mcp.tools.lib.mcp_errors import MCPError, MCPErrorCode
from wistx_mcp.tools.lib.request_context import (
    get_request_context,
    set_request_context,
    update_request_context,
)
from wistx_mcp.tools.lib.rate_limiter import get_rate_limiter
from wistx_mcp.tools.lib.request_deduplicator import get_request_deduplicator
from wistx_mcp.tools.lib.session_context import (
    set_connection_id,
    extract_session_id,
    set_current_session_id,
    get_current_session_id,
    store_tool_result,
    get_previous_tool_result,
    enrich_arguments_from_session,
)
from wistx_mcp.tools.lib.resource_manager import get_resource_manager
from wistx_mcp.tools.lib.constants import (
    MAX_REQUEST_SIZE_BYTES,
    GLOBAL_TOOL_TIMEOUT_SECONDS,
    MAX_RATE_LIMIT_CALLS,
    RATE_LIMIT_WINDOW_SECONDS,
    MAX_CONCURRENT_TOOLS,
    REQUEST_DEDUPLICATION_TTL_SECONDS,
    MAX_REQUEST_ID_LENGTH,
    TOOL_TIMEOUTS,
    INITIALIZATION_TIMEOUT_SECONDS,
)

request_id_var: ContextVar[str] = ContextVar("request_id", default="")

from wistx_mcp.tools.lib.protocol_handler import (
    SUPPORTED_PROTOCOL_VERSIONS,
    DEFAULT_PROTOCOL_VERSION,
)

# Phase 2 & Phase 3 Imports
from wistx_mcp.tools.lib.lazy_tool_loader import LazyToolLoader
from wistx_mcp.tools.lib.rate_limit_headers import RateLimitHeaders
from wistx_mcp.tools.lib.tool_analytics import ToolAnalytics
from wistx_mcp.tools.lib.distributed_tool_cache import DistributedToolCache
from wistx_mcp.tools.lib.comprehensive_audit_logger import ComprehensiveAuditLogger

VALID_RESOURCE_TYPES = {"repository", "documentation", "document", "health"}
RESOURCE_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")
REQUEST_ID_PATTERN = re.compile(r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$")

_inflight_requests: set[str] = set()
_inflight_lock = asyncio.Lock()

if not logging.getLogger().handlers:
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(getattr(logging, str(settings.log_level).upper(), logging.INFO))

from wistx_mcp.tools.lib.logging_utils import SensitiveDataFilter

logging.getLogger().addFilter(SensitiveDataFilter())

# ============================================================================
# PHASE 1: Pre-Cache Server Info - Global Variables
# ============================================================================
# These variables are used to cache server info before initialization
# and to track initialization state. This fixes the race condition where
# clients call ListOfferings before the server completes initialization.

_server_info_cache: dict[str, Any] | None = None
_initialization_complete: asyncio.Event | None = None


def get_cached_server_info() -> dict[str, Any]:
    """Get cached server info, available before initialization.

    This function returns cached server info that is populated before
    the stdio server starts. This ensures that clients can get server
    info even before the on_initialize handler runs.

    Returns:
        Dictionary with server name and version
    """
    global _server_info_cache
    if _server_info_cache is None:
        _server_info_cache = {
            "name": "wistx-mcp",
            "version": "0.1.0",
        }
    return _server_info_cache


async def get_initialization_event() -> asyncio.Event:
    """Get or create the initialization event.

    This event is used to signal when server initialization is complete.
    Handlers can wait on this event to ensure initialization is done
    before proceeding.

    Returns:
        asyncio.Event that signals initialization completion
    """
    global _initialization_complete
    if _initialization_complete is None:
        _initialization_complete = asyncio.Event()
    return _initialization_complete


async def _wait_for_initialization(timeout: float = None) -> None:
    """Wait for server initialization to complete.

    This function waits for the initialization event to be set, with a
    timeout to prevent indefinite waiting.

    Args:
        timeout: Maximum time to wait in seconds (default: INITIALIZATION_TIMEOUT_SECONDS)

    Raises:
        MCPError: If initialization times out
    """
    if timeout is None:
        timeout = INITIALIZATION_TIMEOUT_SECONDS

    try:
        init_event = await get_initialization_event()
        await asyncio.wait_for(
            init_event.wait(),
            timeout=timeout
        )
        logger.debug("Initialization complete, proceeding with handler")
    except asyncio.TimeoutError:
        logger.warning("Initialization timeout after %.1f seconds", timeout)
        raise MCPError(
            code=MCPErrorCode.TIMEOUT,
            message="Server initialization timeout"
        )
    except Exception as e:
        logger.error("Error waiting for initialization: %s", e)
        raise


def _validate_and_clear_stale_bytecode_cache() -> dict[str, Any]:
    """Validate bytecode cache and clear stale .pyc files.

    This function detects stale Python bytecode cache files where the source
    file has been modified after the cache was created. Stale caches can cause
    the server to use old code, leading to unexpected behavior.

    Returns:
        Dictionary with cache validation results:
        - cleared_count: Number of stale .pyc files cleared
        - cleared_files: List of cleared file paths
        - errors: List of any errors encountered
    """
    import pathlib

    results = {
        "cleared_count": 0,
        "cleared_files": [],
        "errors": [],
    }

    # Get the wistx_mcp package directory
    try:
        wistx_mcp_dir = pathlib.Path(__file__).parent
    except Exception as e:
        logger.warning("Could not determine wistx_mcp directory: %s", e)
        return results

    if not wistx_mcp_dir.exists():
        return results

    # Find all .py source files and check for stale caches
    try:
        for source_file in wistx_mcp_dir.rglob("*.py"):
            if "__pycache__" in str(source_file):
                continue

            source_mtime = source_file.stat().st_mtime
            pycache_dir = source_file.parent / "__pycache__"

            if not pycache_dir.exists():
                continue

            # Check all .pyc files for this source
            stem = source_file.stem
            for pyc_file in pycache_dir.glob(f"{stem}.cpython-*.pyc"):
                try:
                    pyc_mtime = pyc_file.stat().st_mtime
                    if source_mtime > pyc_mtime:
                        # Source is newer than cache - delete stale cache
                        pyc_file.unlink()
                        results["cleared_count"] += 1
                        results["cleared_files"].append(str(pyc_file.relative_to(wistx_mcp_dir)))
                        logger.debug("Cleared stale cache: %s", pyc_file.name)
                except OSError as e:
                    results["errors"].append(f"Error removing {pyc_file}: {e}")

    except Exception as e:
        results["errors"].append(f"Error scanning for stale caches: {e}")
        logger.warning("Error during cache validation: %s", e)

    if results["cleared_count"] > 0:
        logger.info(
            "Cleared %d stale bytecode cache file(s) to ensure latest code is used",
            results["cleared_count"]
        )

    return results


async def main() -> None:
    """Main entry point for MCP server."""
    # Validate and clear stale bytecode cache before importing tools
    cache_results = _validate_and_clear_stale_bytecode_cache()
    if cache_results["cleared_count"] > 0:
        logger.info("Cache validation: cleared %d stale files", cache_results["cleared_count"])
    if cache_results["errors"]:
        for error in cache_results["errors"]:
            logger.warning("Cache validation error: %s", error)

    try:
        from mcp.server import Server
        from mcp.server.stdio import stdio_server
        from mcp.types import Tool, TextContent
    except ImportError as e:
        logger.error("Failed to import MCP SDK: %s", e, exc_info=True)
        raise RuntimeError(f"MCP SDK not available: {e}") from e
    
    mcp_tools_module = None
    try:
        sys.exit = _mcp_safe_exit
        sys.stdout = _suppress_stdout
        try:
            from wistx_mcp.tools import mcp_tools
            mcp_tools_module = mcp_tools
        finally:
            sys.stdout = _original_stdout
        sys.exit = _original_sys_exit
        logger.info("Core tools imported successfully")
    except SystemExit as e:
        sys.exit = _original_sys_exit
        sys.stdout = _original_stdout
        logger.warning("SystemExit during tool imports, continuing with minimal tools: %s", e)
        sys.stdout = _suppress_stdout
        try:
            from wistx_mcp.tools import mcp_tools
            mcp_tools_module = mcp_tools
        finally:
            sys.stdout = _original_stdout
    except Exception as e:
        sys.exit = _original_sys_exit
        sys.stdout = _original_stdout
        logger.error("Error importing tools: %s", e, exc_info=True)
        sys.stdout = _suppress_stdout
        try:
            from wistx_mcp.tools import mcp_tools
            mcp_tools_module = mcp_tools
        finally:
            sys.stdout = _original_stdout
    
    if mcp_tools_module is None:
        raise RuntimeError("Failed to import core tools module")

    logger.info("Starting WISTX MCP Server v%s", settings.server_version)
    logger.info("Server: %s", settings.server_name)

    resource_manager = await get_resource_manager()
    shutdown_event = resource_manager.get_shutdown_event()

    rate_limiter = None
    deduplicator = None
    concurrent_limiter = None

    # Phase 2 & Phase 3 Initialization
    lazy_tool_loader = LazyToolLoader()
    rate_limit_headers = RateLimitHeaders()
    tool_analytics = ToolAnalytics()

    # Phase 3: Initialize Redis client for distributed cache
    redis_client = None
    redis_url = settings.redis_url or os.getenv("REDIS_URL")
    if redis_url:
        try:
            import redis
            redis_client = redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2,
                health_check_interval=30,
            )
            redis_client.ping()
            logger.info("Redis connection established")
        except Exception as e:
            logger.debug("Redis connection failed, using local cache fallback: %s", e)
            redis_client = None
    else:
        logger.debug("Redis not configured, using local cache fallback")

    distributed_cache = DistributedToolCache(redis_client=redis_client, ttl=3600)
    audit_logger = ComprehensiveAuditLogger(retention_days=90)

    try:
        rate_limiter = await get_rate_limiter(
            max_calls=MAX_RATE_LIMIT_CALLS,
            window_seconds=RATE_LIMIT_WINDOW_SECONDS,
        )
        deduplicator = await get_request_deduplicator(
            ttl_seconds=REQUEST_DEDUPLICATION_TTL_SECONDS,
        )
        concurrent_limiter = await get_concurrent_limiter(
            max_concurrent=MAX_CONCURRENT_TOOLS,
        )
        logger.info("Background tasks started successfully")
    except Exception as e:
        logger.error("Failed to start background tasks: %s", e, exc_info=True)
        raise

    def signal_handler(signum: int, _frame: Any) -> None:
        """Handle shutdown signals."""
        logger.info("Received signal %d, initiating graceful shutdown...", signum)
        shutdown_event.set()

    if sys.platform != "win32":
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    else:
        logger.warning("Signal handlers not available on Windows")

    if mcp_tools_module and hasattr(mcp_tools_module, "api_client"):
        resource_manager.register_http_client(mcp_tools_module.api_client)

    from wistx_mcp.tools.lib.api_client import get_api_client
    try:
        global_api_client = await get_api_client()
        resource_manager.register_http_client(global_api_client)
    except Exception as e:
        logger.debug("Could not register global API client: %s", e)

    try:
        app = Server(
            name=settings.server_name,
        )
        logger.info("MCP Server instance created successfully with name: %s, version: %s", settings.server_name, settings.server_version)
    except (RuntimeError, ValueError, AttributeError) as e:
        logger.error("Failed to create MCP Server: %s", e, exc_info=True)
        raise
    except Exception as e:
        logger.error("Unexpected error creating MCP Server: %s", e, exc_info=True)
        raise RuntimeError(f"Failed to create MCP Server: {e}") from e

    # ========================================================================
    # PHASE 1: Pre-populate server info cache BEFORE stdio starts
    # ========================================================================
    # This ensures that when clients call ListOfferings before initialize,
    # the server info is already available. This fixes the race condition.
    global _server_info_cache
    _server_info_cache = {
        "name": settings.server_name,
        "version": settings.server_version,
    }
    logger.info("Server info cached: %s", _server_info_cache)

    # Initialize the initialization event
    global _initialization_complete
    _initialization_complete = asyncio.Event()
    logger.info("Initialization event created")

    if AuthContext is not None:
        try:
            api_key = settings.api_key or os.getenv("WISTX_API_KEY", "")
            if api_key:
                auth_ctx = AuthContext(api_key=api_key)
                set_auth_context(auth_ctx)
                logger.info("Authentication context initialized (validation deferred to first tool call)")
            else:
                logger.debug("No API key available during server startup, will check environment during tool execution")
        except Exception as e:
            logger.warning("Failed to initialize auth context: %s", e)

    on_initialize_registered = False
    try:
        @app.on_initialize()
        async def on_initialize(params: dict[str, Any]) -> dict[str, Any]:
            """Handle MCP server initialization.

            Args:
                params: Initialization parameters from client

            Returns:
                Server capabilities and information

            Raises:
                MCPError: If protocol version is unsupported or initialization fails
            """
            request_id = str(uuid.uuid4())
            request_id_var.set(request_id)
            logger.info("MCP server initialization [request_id=%s]", request_id)

            from wistx_mcp.tools.lib.protocol_handler import validate_protocol_version

            client_protocol = params.get("protocolVersion", DEFAULT_PROTOCOL_VERSION)
            try:
                validated_version = validate_protocol_version(client_protocol)
            except ValueError as e:
                raise MCPError(
                    code=MCPErrorCode.INVALID_REQUEST,
                    message=str(e),
                ) from e

            supported_version = validated_version

            set_request_context({
                "request_id": request_id,
                "protocol_version": supported_version,
            })

            init_options = params.get("initializationOptions", {}) or {}
            api_key = init_options.get("api_key") or settings.api_key
            
            if not api_key:
                env_api_key = os.getenv("WISTX_API_KEY")
                if env_api_key:
                    api_key = env_api_key
                    object.__setattr__(settings, "api_key", env_api_key)
                    logger.info("API key set from environment variable [request_id=%s]", request_id)
            
            api_url = init_options.get("api_url") or init_options.get("WISTX_API_URL")
            if api_url:
                object.__setattr__(settings, "api_url", api_url.rstrip("/"))
                logger.info("API URL set from initialization options: %s [request_id=%s]", api_url, request_id)
            elif not settings.api_url or settings.api_url == "https://api.wistx.ai":
                env_api_url = os.getenv("WISTX_API_URL")
                if env_api_url:
                    object.__setattr__(settings, "api_url", env_api_url.rstrip("/"))
                    logger.info("API URL set from environment variable: %s [request_id=%s]", env_api_url, request_id)
            
            gemini_api_key = init_options.get("gemini_api_key") or init_options.get("GEMINI_API_KEY")
            if gemini_api_key:
                object.__setattr__(settings, "gemini_api_key", gemini_api_key)
                logger.info("Gemini API key set from initialization options [request_id=%s]", request_id)
            elif not settings.gemini_api_key:
                env_gemini_key = os.getenv("GEMINI_API_KEY")
                if env_gemini_key:
                    object.__setattr__(settings, "gemini_api_key", env_gemini_key)
                    logger.info("Gemini API key set from environment variable [request_id=%s]", request_id)

            if api_key:
                object.__setattr__(settings, "api_key", api_key)
                if AuthContext is None:
                    logger.debug("API key provided but AuthContext not available (api.config dependency issue), skipping authentication")
                else:
                    try:
                        auth_ctx = AuthContext(api_key=api_key)
                        await auth_ctx.validate()
                        set_auth_context(auth_ctx)
                        logger.info(
                            "Authentication successful via initialization for user: %s [request_id=%s]",
                            auth_ctx.get_user_id(),
                            request_id,
                        )
                    except ValueError as e:
                        # Don't raise error during initialization - let tools validate API key when called
                        logger.warning("Failed to validate API key from initialization: %s [request_id=%s]", e, request_id)
                        logger.info("API key validation will be deferred to tool execution [request_id=%s]", request_id)
                    except (RuntimeError, ConnectionError) as e:
                        # Don't raise error during initialization - authentication service may be temporarily unavailable
                        logger.warning("Authentication service unavailable during initialization: %s [request_id=%s]", e, request_id)
                        logger.info("API key validation will be deferred to tool execution [request_id=%s]", request_id)
                    except Exception as e:
                        logger.warning("Unexpected error during authentication: %s [request_id=%s]", e, request_id)
                        logger.debug("Authentication error details: %s", e, exc_info=True)
                        logger.info("API key validation will be deferred to tool execution [request_id=%s]", request_id)

            from wistx_mcp.tools.lib.protocol_handler import ensure_protocol_compliance

            response = {
                "protocolVersion": supported_version,
                "capabilities": {
                    "tools": {},
                    "resources": {
                        "subscribe": True,
                        "listChanged": True,
                    },
                    "prompts": {},
                },
                "serverInfo": {
                    "name": settings.server_name,
                    "version": settings.server_version,
                },
            }

            # ================================================================
            # PHASE 1: Signal initialization complete
            # ================================================================
            # Set the initialization event so handlers waiting on it can proceed
            try:
                init_event = await get_initialization_event()
                init_event.set()
                logger.info("Initialization complete, event signaled")
            except Exception as e:
                logger.warning("Failed to signal initialization: %s", e)

            return ensure_protocol_compliance(response, protocol_version=supported_version)

        on_initialize_registered = True
        logger.info("on_initialize handler registered successfully")
    except AttributeError as e:
        logger.warning("MCP SDK version may not support on_initialize decorator, skipping initialization handler: %s", e)
        logger.debug("AttributeError details: %s", e, exc_info=True)
        on_initialize_registered = False
        try:
            init_event = await get_initialization_event()
            if not init_event.is_set():
                init_event.set()
                logger.info("Initialization event set (on_initialize not supported)")
        except Exception as init_e:
            logger.debug("Failed to set initialization event: %s", init_e)
    except Exception as e:
        logger.error("Failed to register on_initialize handler: %s", e, exc_info=True)
        on_initialize_registered = False
        try:
            init_event = await get_initialization_event()
            if not init_event.is_set():
                init_event.set()
                logger.info("Initialization event set (on_initialize registration failed)")
        except Exception as init_e:
            logger.debug("Failed to set initialization event: %s", init_e)

    @app.list_resources()
    async def list_resources() -> list[dict[str, Any]]:
        """List available MCP resources."""
        from mcp.types import Resource

        # ====================================================================
        # PHASE 3: Ensure initialization is complete before proceeding
        # ====================================================================
        # This prevents race conditions where clients call ListOfferings
        # before the server has finished initializing.
        if not _initialization_complete or not _initialization_complete.is_set():
            try:
                await _wait_for_initialization()  # Uses INITIALIZATION_TIMEOUT_SECONDS
            except Exception as e:
                logger.warning("Initialization wait failed in list_resources: %s", e)
                # Continue anyway - return cached info or empty list

        auth_ctx = get_auth_context()
        if not auth_ctx:
            return []

        user_id = auth_ctx.get_user_id() or "anonymous"
        rate_limiter_instance = await get_rate_limiter()
        if not await rate_limiter_instance.check_rate_limit(f"resource:{user_id}"):
            logger.warning("Rate limit exceeded for resource listing: user_id=%s", user_id)
            return []

        try:
            from wistx_mcp.tools import user_indexing
            from wistx_mcp.tools.lib.constants import RESOURCE_OPERATION_TIMEOUT_SECONDS

            result = await asyncio.wait_for(
                user_indexing.list_resources(
                    api_key=auth_ctx.api_key,
                    deduplicate=True,
                    status="completed",
                    include_ai_analysis=False,
                ),
                timeout=RESOURCE_OPERATION_TIMEOUT_SECONDS,
            )
            resources_list = result.get("resources", [])

            mcp_resources = []
            seen_repos = set()

            for resource in resources_list:
                if resource.get("status") != "completed":
                    continue

                if resource.get("resource_type") == "repository":
                    from wistx_mcp.tools.lib.repo_normalizer import normalize_repo_url

                    normalized_url = resource.get("normalized_repo_url") or normalize_repo_url(
                        resource.get("repo_url", "")
                    )
                    repo_key = (
                        normalized_url,
                        resource.get("branch", "main"),
                    )

                    if repo_key in seen_repos:
                        continue

                    seen_repos.add(repo_key)

                resource_type = resource.get("resource_type", "unknown")
                resource_id = resource.get("resource_id", "")
                name = resource.get("name") or resource.get("repo_url") or resource.get("documentation_url") or resource_id

                uri = f"wistx://{resource_type}/{resource_id}"
                mcp_resources.append(
                    Resource(
                        uri=uri,
                        name=name,
                        description=resource.get("description", ""),
                        mimeType="application/json",
                    )
                )


            from wistx_mcp.tools.lib.protocol_handler import ensure_protocol_compliance

            protocol_version = get_request_context().get("protocol_version")
            compliant_resources = ensure_protocol_compliance(mcp_resources, protocol_version=protocol_version)

            return compliant_resources
        except asyncio.TimeoutError:
            logger.error("Timeout listing MCP resources")
            return []
        except (ValueError, RuntimeError, ConnectionError) as e:
            logger.error("Error listing MCP resources: %s", e, exc_info=True)
            return []
        except Exception as e:
            logger.error("Unexpected error listing MCP resources: %s", e, exc_info=True)
            return []

    def validate_resource_uri(uri: str) -> tuple[str, str]:
        """Validate and parse resource URI.

        Args:
            uri: Resource URI to validate

        Returns:
            Tuple of (resource_type, resource_id)

        Raises:
            ValueError: If URI is invalid
        """
        if not uri.startswith("wistx://"):
            raise ValueError(f"Invalid resource URI: {uri}")

        parts = uri.replace("wistx://", "").split("/", 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid resource URI format: {uri}")

        resource_type, resource_id = parts

        if resource_type not in VALID_RESOURCE_TYPES:
            raise ValueError(f"Invalid resource type: {resource_type}. Valid types: {', '.join(VALID_RESOURCE_TYPES)}")

        if not RESOURCE_ID_PATTERN.match(resource_id):
            raise ValueError(f"Invalid resource ID format: {resource_id}")

        return resource_type, resource_id

    def validate_request_id(request_id: str) -> str:
        """Validate and normalize request ID.

        Args:
            request_id: Request ID to validate

        Returns:
            Validated request ID

        Raises:
            ValueError: If request ID is invalid
        """
        if not isinstance(request_id, str):
            raise ValueError("Request ID must be a string")

        if len(request_id) > MAX_REQUEST_ID_LENGTH:
            raise ValueError(f"Request ID too long (max {MAX_REQUEST_ID_LENGTH} characters)")

        if not (REQUEST_ID_PATTERN.match(request_id) or request_id.replace("-", "").replace("_", "").isalnum()):
            raise ValueError("Invalid request ID format")

        return request_id

    @app.read_resource()
    async def read_resource(uri: str) -> str:
        """Read resource content."""
        uri_str = str(uri)
        
        auth_ctx = get_auth_context()
        if auth_ctx:
            user_id = auth_ctx.get_user_id() or "anonymous"
            rate_limiter_instance = await get_rate_limiter()
            if not await rate_limiter_instance.check_rate_limit(f"resource:{user_id}"):
                raise MCPError(
                    code=MCPErrorCode.RATE_LIMIT_EXCEEDED,
                    message="Rate limit exceeded for resource operations",
                )

        if uri_str in ("wistx://metrics", "wistx://health", "wistx://cache-stats", "wistx://audit-logs"):
            raise MCPError(
                code=MCPErrorCode.INVALID_PARAMS,
                message="Internal server resources are not accessible",
            )

        auth_ctx = get_auth_context()
        if not auth_ctx:
            raise MCPError(
                code=MCPErrorCode.INVALID_REQUEST,
                message="Authentication required to read resources",
            )

        try:
            _resource_type, resource_id = validate_resource_uri(uri_str)
        except ValueError as e:
            raise MCPError(
                code=MCPErrorCode.INVALID_PARAMS,
                message=str(e),
            ) from e

        from wistx_mcp.tools import user_indexing
        from wistx_mcp.tools.lib.constants import RESOURCE_OPERATION_TIMEOUT_SECONDS

        try:
            result = await asyncio.wait_for(
                user_indexing.check_resource_status(
                    resource_id=resource_id,
                    api_key=auth_ctx.api_key,
                ),
                timeout=RESOURCE_OPERATION_TIMEOUT_SECONDS,
            )

            from wistx_mcp.tools.lib.protocol_handler import ensure_protocol_compliance

            protocol_version = get_request_context().get("protocol_version")
            compliant_result = ensure_protocol_compliance(result, protocol_version=protocol_version)

            return json.dumps(compliant_result, indent=2)
        except asyncio.TimeoutError:
            logger.error("Timeout reading MCP resource %s", uri)
            raise MCPError(
                code=MCPErrorCode.TIMEOUT,
                message=f"Resource operation timed out after {RESOURCE_OPERATION_TIMEOUT_SECONDS} seconds",
            )
        except ValueError as e:
            logger.error("Error reading MCP resource %s: %s", uri, e, exc_info=True)
            raise MCPError(
                code=MCPErrorCode.INVALID_PARAMS,
                message=f"Failed to read resource: {sanitize_error_message(e)}",
            ) from e
        except (RuntimeError, ConnectionError) as e:
            logger.error("Error reading MCP resource %s: %s", uri, e, exc_info=True)
            raise MCPError(
                code=MCPErrorCode.INTERNAL_ERROR,
                message="Failed to read resource due to internal error",
            ) from e
        except Exception as e:
            logger.error("Unexpected error reading MCP resource %s: %s", uri, e, exc_info=True)
            raise MCPError(
                code=MCPErrorCode.INTERNAL_ERROR,
                message="An unexpected error occurred while reading resource",
            ) from e

    try:
        @app.subscribe()
        async def subscribe(uri: str) -> None:
            """Subscribe to resource change notifications.

            Args:
                uri: Resource URI to subscribe to
            """
            auth_ctx = get_auth_context()
            if not auth_ctx:
                raise MCPError(
                    code=MCPErrorCode.INVALID_REQUEST,
                    message="Authentication required to subscribe to resources",
                )

            try:
                validate_resource_uri(uri)

                if not auth_ctx.user_info:
                    try:
                        await auth_ctx.validate()
                    except Exception as e:
                        logger.warning("Failed to validate auth context for resource subscription: %s", e)
                user_id = auth_ctx.get_user_id() or "unknown"

                resource_manager_instance = await get_resource_manager()
                await resource_manager_instance.subscribe(uri, user_id)

                logger.info(
                    "User %s subscribed to resource %s [request_id=%s]",
                    user_id[:8] if len(user_id) > 8 else user_id,
                    uri,
                    request_id_var.get(),
                )
            except ValueError as e:
                raise MCPError(
                    code=MCPErrorCode.INVALID_PARAMS,
                    message=f"Invalid resource URI: {sanitize_error_message(e)}",
                ) from e
            except Exception as e:
                logger.error("Error subscribing to resource %s: %s", uri, e, exc_info=True)
                raise MCPError(
                    code=MCPErrorCode.INTERNAL_ERROR,
                    message="Failed to subscribe to resource",
                ) from e
    except AttributeError:
        logger.warning("MCP SDK version may not support subscribe decorator, skipping subscription handler")

    try:
        @app.list_prompts()
        async def list_prompts() -> list[dict[str, Any]]:
            """List available MCP prompts."""
            prompts = []

            from wistx_mcp.tools.lib.protocol_handler import ensure_protocol_compliance

            protocol_version = get_request_context().get("protocol_version")
            compliant_prompts = ensure_protocol_compliance(prompts, protocol_version=protocol_version)

            return compliant_prompts
    except AttributeError:
        logger.warning("MCP SDK version may not support list_prompts decorator, skipping prompts handler")

    try:
        @app.get_prompt()
        async def get_prompt(name: str, arguments: dict[str, Any]) -> list[TextContent]:
            """Execute a prompt template.

            Args:
                name: Prompt name
                arguments: Prompt arguments (unused, no prompts available)

            Returns:
                List of TextContent results
            """
            del arguments
            auth_ctx = get_auth_context()
            if not auth_ctx:
                raise MCPError(
                    code=MCPErrorCode.INVALID_REQUEST,
                    message="Authentication required to execute prompts",
                )

            request_id = request_id_var.get() or str(uuid.uuid4())
            request_id_var.set(request_id)

            try:
                raise MCPError(
                    code=MCPErrorCode.METHOD_NOT_FOUND,
                    message=f"Unknown prompt: {name}",
                )
            except MCPError:
                raise
            except ValueError as e:
                raise MCPError(
                    code=MCPErrorCode.INVALID_PARAMS,
                    message=sanitize_error_message(e),
                ) from e
            except Exception as e:
                logger.error("Error executing prompt %s: %s [request_id=%s]", name, e, request_id, exc_info=True)
                raise MCPError(
                    code=MCPErrorCode.INTERNAL_ERROR,
                    message="Failed to execute prompt",
                ) from e
    except AttributeError:
        logger.warning("MCP SDK version may not support get_prompt decorator, skipping prompt execution handler")

    @app.list_tools()
    async def list_tools() -> list[Tool]:
        """List available MCP tools."""
        from mcp.types import Tool

        # ====================================================================
        # PHASE 3: Ensure initialization is complete before proceeding
        # ====================================================================
        # This prevents race conditions where clients call ListTools
        # before the server has finished initializing.
        if not _initialization_complete or not _initialization_complete.is_set():
            try:
                await _wait_for_initialization()  # Uses INITIALIZATION_TIMEOUT_SECONDS
            except Exception as e:
                logger.warning("Initialization wait failed in list_tools: %s", e)
                # Continue anyway - return cached tools or empty list

        cached_definitions = distributed_cache.get_tool_definitions()
        if cached_definitions:
            try:
                tools = [Tool(**tool_dict) for tool_dict in cached_definitions]
                logger.debug("Loaded tool list from cache (%d tools)", len(tools))
                return tools
            except Exception as e:
                logger.warning("Failed to deserialize cached tools, rebuilding: %s", e)
        
        logger.info("Building tool list (cache miss)")
        try:
            from wistx_mcp.tools.lib.tool_permissions import get_tool_permissions
            from wistx_mcp.tools.lib.tool_descriptions import ToolDescriptionManager
            
            def build_tool_description(tool_name: str, base_description: str | None = None) -> str:
                """Build tool description with plan requirements, using short description from ToolDescriptionManager."""
                short_desc = ToolDescriptionManager.get_short_description(tool_name)
                description = base_description if base_description else short_desc
                
                perms = get_tool_permissions(tool_name)
                required_plan = perms.get("required_plan", "professional")
                required_permission = perms.get("required_permission")
                
                plan_note = ""
                if required_plan != "professional":
                    plan_note = f" [REQUIRES: {required_plan} plan or higher]"
                if required_permission:
                    plan_note += f" [REQUIRES PERMISSION: {required_permission}]"
                
                return f"{description}{plan_note}"
            
            tools = [
            Tool(
                name="wistx_get_compliance_requirements",
                description=build_tool_description("wistx_get_compliance_requirements"),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "resource_types": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of resource types (RDS, S3, EC2, Lambda, EKS, etc.)",
                            "minItems": 1,
                        },
                        "standards": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Compliance standards (PCI-DSS, HIPAA, CIS, SOC2, NIST-800-53, ISO-27001, GDPR, FedRAMP, etc.)",
                            "default": [],
                        },
                        "severity": {
                            "type": "string",
                            "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
                            "description": "Filter by severity level",
                        },
                        "include_remediation": {
                            "type": "boolean",
                            "default": True,
                            "description": "Include remediation guidance and code snippets",
                        },
                        "include_verification": {
                            "type": "boolean",
                            "default": True,
                            "description": "Include verification procedures",
                        },
                        "generate_report": {
                            "type": "boolean",
                            "default": True,
                            "description": "Automatically generate and store a compliance report",
                        },
                        "cloud_provider": {
                            "oneOf": [
                                {
                                    "type": "string",
                                    "enum": ["aws", "gcp", "azure", "multi-cloud"],
                                    "description": "Cloud provider (aws, gcp, azure, multi-cloud) - used to validate resource types match provider. "
                                    "Use 'multi-cloud' for projects spanning multiple providers. "
                                    "If your terraform project uses GCP, specify 'gcp' to ensure correct resource types are used.",
                                },
                                {
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "enum": ["aws", "gcp", "azure"],
                                    },
                                    "description": "List of cloud providers for multi-cloud projects (e.g., ['aws', 'gcp']). "
                                    "Used to validate resource types match providers.",
                                },
                            ],
                        },
                    },
                    "required": ["resource_types"],
                },
            ),
            Tool(
                name="wistx_calculate_infrastructure_cost",
                description=build_tool_description(
                    "wistx_calculate_infrastructure_cost",
                    "Calculate infrastructure costs for cloud resources. Use this tool when asked about pricing, costs, or cost optimization for AWS/GCP/Azure resources. Returns monthly/annual costs, cost breakdown, and optimization suggestions."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "resources": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "cloud": {"type": "string", "description": "Cloud provider (aws, gcp, azure)"},
                                    "service": {"type": "string", "description": "Service name (rds, ec2, s3, etc.)"},
                                    "instance_type": {"type": "string", "description": "Instance type (db.t3.medium, etc.)"},
                                    "quantity": {"type": "integer", "description": "Quantity", "default": 1},
                                    "region": {"type": "string", "description": "Region ID (us-east-1, us-central1, etc.). Required for accurate pricing as costs vary by region."},
                                },
                                "required": ["cloud", "service", "instance_type"],
                            },
                            "description": "List of resource specifications",
                            "minItems": 1,
                        },
                    },
                    "required": ["resources"],
                },
            ),
            Tool(
                name="wistx_troubleshoot_issue",
                description=build_tool_description(
                    "wistx_troubleshoot_issue",
                    "Diagnose and fix infrastructure/code issues. "
                    "Analyzes errors, logs, and code to identify root causes, "
                    "provides fix recommendations, and prevention strategies. "
                    "Use this tool when encountering errors or issues."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "issue_description": {
                            "type": "string",
                            "description": "Description of the issue",
                            "minLength": 10,
                        },
                        "infrastructure_type": {
                            "type": "string",
                            "enum": ["terraform", "kubernetes", "docker", "cloudformation", "ansible"],
                            "description": "Type of infrastructure",
                        },
                        "cloud_provider": {
                            "oneOf": [
                                {"type": "string", "enum": ["aws", "gcp", "azure", "multi-cloud"]},
                                {"type": "array", "items": {"type": "string", "enum": ["aws", "gcp", "azure"]}},
                            ],
                            "description": "Cloud provider(s). Use 'multi-cloud' or array for multi-cloud troubleshooting.",
                        },
                        "error_messages": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of error messages",
                        },
                        "configuration_code": {
                            "type": "string",
                            "description": "Relevant configuration code",
                        },
                        "logs": {
                            "type": "string",
                            "description": "Log output",
                        },
                        "resource_type": {
                            "type": "string",
                            "description": "Resource type (RDS, S3, EKS, etc.)",
                        },
                    },
                    "required": ["issue_description"],
                },
            ),
            Tool(
                name="wistx_generate_documentation",
                description=build_tool_description(
                    "wistx_generate_documentation",
                    "Generate comprehensive documentation and reports. "
                    "Creates architecture docs, runbooks, compliance reports, "
                    "security reports, cost reports, API documentation, and deployment guides. "
                    "IMPORTANT: To generate specific (non-generic) content, you MUST pass context from previous tool calls: "
                    "- Pass resource_types (e.g., ['EC2', 'RDS', 'S3', 'VPC', 'Route53']) for specific resource documentation. "
                    "- Pass compliance_standards (e.g., ['CIS', 'SOC2', 'NIST-800-53']) for specific compliance sections. "
                    "- Pass infrastructure_code from wistx_infrastructure init_project for code documentation. "
                    "- Pass configuration with cloud_provider for provider-specific content. "
                    "Without these parameters, the output will be generic boilerplate."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "document_type": {
                            "type": "string",
                            "enum": [
                                "architecture_diagram",
                                "runbook",
                                "compliance_report",
                                "cost_report",
                                "security_report",
                                "api_documentation",
                                "deployment_guide",
                            ],
                            "description": "Type of document to generate",
                        },
                        "subject": {
                            "type": "string",
                            "description": "REQUIRED. Subject of the document (project name, resource, topic)",
                        },
                        "resource_types": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "CRITICAL for specific content. List of AWS/GCP/Azure resource types (e.g., ['EC2', 'RDS', 'S3', 'VPC', 'Route53']). Without this, output is generic.",
                        },
                        "compliance_standards": {
                            "type": "array",
                            "items": {"type": "string", "enum": ["SOC2", "PCI-DSS", "HIPAA", "GDPR", "ISO27001", "NIST-800-53", "CIS", "FedRAMP", "SOX"]},
                            "description": "⚠️ REQUIRED when include_compliance=true. Extract ALL standards from user prompt. Valid: SOC2, PCI-DSS, HIPAA, GDPR, ISO27001, NIST-800-53, CIS, FedRAMP, SOX. Example: 'PCI and HIPAA compliant' → ['PCI-DSS', 'HIPAA'].",
                        },
                        "infrastructure_code": {
                            "type": "string",
                            "description": "Infrastructure code to document. Pass the code from wistx_infrastructure init_project or other sources.",
                        },
                        "configuration": {
                            "type": "object",
                            "description": "Configuration with cloud_provider ('aws'/'gcp'/'azure'), project metadata, etc.",
                        },
                        "include_compliance": {
                            "type": "boolean",
                            "default": True,
                            "description": "⚠️ REQUIRES compliance_standards array. Set true ONLY if you also provide compliance_standards.",
                        },
                        "include_security": {
                            "type": "boolean",
                            "default": True,
                            "description": "Include security information",
                        },
                        "include_cost": {
                            "type": "boolean",
                            "default": True,
                            "description": "Include cost information",
                        },
                        "include_best_practices": {
                            "type": "boolean",
                            "default": True,
                            "description": "Include best practices",
                        },
                        "resources": {
                            "type": "array",
                            "items": {"type": "object"},
                            "description": "List of resource specifications (for cost report)",
                        },
                        "api_spec": {
                            "type": "object",
                            "description": "API specification (for api_documentation)",
                        },
                        "format": {
                            "type": "string",
                            "enum": ["markdown", "pdf", "html", "json"],
                            "default": "markdown",
                            "description": "Output format",
                        },
                        "report_variant": {
                            "type": "string",
                            "enum": ["internal", "executive_summary", "audit_package", "trust_center"],
                            "default": "internal",
                            "description": "For compliance_report: stakeholder view. 'internal' (detailed technical), 'executive_summary' (C-suite overview), 'audit_package' (SOC2 Type II for auditors), 'trust_center' (public portal).",
                        },
                    },
                    "required": ["document_type", "subject"],
                },
            ),

            # === UNIFIED TOOLS (Phase 2 consolidation) ===
            Tool(
                name="wistx_search_code",
                description=build_tool_description(
                    "wistx_search_code",
                    "🎯 UNIFIED code search tool. Combines semantic search, regex search, and code examples. "
                    "Use search_mode='semantic' for natural language queries, 'regex' for pattern matching, 'examples' for curated code. "
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "search_mode": {
                            "type": "string",
                            "enum": ["semantic", "regex", "examples"],
                            "description": "REQUIRED. Search mode: semantic (natural language), regex (pattern matching), examples (curated code)",
                        },
                        # ================================================================
                        # COMMON PARAMS (for all search modes)
                        # ================================================================
                        "query": {"type": "string", "description": "REQUIRED for semantic/examples. Search query in natural language."},
                        "repositories": {"type": "array", "items": {"type": "string"}, "description": "Filter by repository URLs."},
                        "resource_ids": {"type": "array", "items": {"type": "string"}, "description": "Filter by indexed resource IDs."},
                        "resource_types": {"type": "array", "items": {"type": "string"}, "description": "Filter by resource types (e.g., ['EC2', 'RDS'])."},
                        "file_types": {"type": "array", "items": {"type": "string"}, "description": "Filter by file extensions (e.g., ['tf', 'yaml', 'json'])."},
                        "code_type": {"type": "string", "enum": ["terraform", "kubernetes", "ansible", "cloudformation", "docker"], "description": "Filter by code type."},
                        "cloud_provider": {
                            "oneOf": [
                                {"type": "string", "enum": ["aws", "gcp", "azure", "multi-cloud"]},
                                {"type": "array", "items": {"type": "string", "enum": ["aws", "gcp", "azure"]}},
                            ],
                            "description": "Filter by cloud provider(s). Use 'multi-cloud' or array for multi-cloud search.",
                        },
                        "limit": {"type": "integer", "default": 50, "description": "Maximum results to return."},
                        # ================================================================
                        # SEMANTIC PARAMS (for search_mode='semantic')
                        # ================================================================
                        "include_sources": {"type": "boolean", "default": True, "description": "Include source file references (for semantic)."},
                        "include_ai_analysis": {"type": "boolean", "default": True, "description": "Include AI analysis of results (for semantic)."},
                        # ================================================================
                        # REGEX PARAMS (for search_mode='regex')
                        # ================================================================
                        "pattern": {"type": "string", "description": "REQUIRED for regex (if no template). Regex pattern to search."},
                        "template": {"type": "string", "description": "Pre-built template name (alternative to pattern for regex)."},
                        "case_sensitive": {"type": "boolean", "default": False, "description": "Case-sensitive regex matching (for regex)."},
                        # ================================================================
                        # EXAMPLES PARAMS (for search_mode='examples')
                        # ================================================================
                        "services": {"type": "array", "items": {"type": "string"}, "description": "Filter by AWS/GCP services (e.g., ['rds', 's3', 'eks'])."},
                        "code_types": {"type": "array", "items": {"type": "string"}, "description": "Filter by code types (e.g., ['terraform', 'kubernetes'])."},
                        "compliance_standard": {"type": "string", "description": "Filter by compliance standard (e.g., 'SOC2', 'HIPAA')."},
                    },
                    "required": ["search_mode"],
                },
            ),
            Tool(
                name="wistx_infrastructure",
                description=build_tool_description(
                    "wistx_infrastructure",
                    "🎯 UNIFIED infrastructure tool. Actions: init_project, design_project, review_project, optimize_project, "
                    "analyze, design, validate, integrate, analyze_integration, create, update, upgrade, backup, restore, "
                    "monitor, optimize_resources, get_existing, discover. Use for ALL infrastructure operations."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["init_project", "design_project", "review_project", "optimize_project",
                                     "analyze", "design", "validate", "integrate", "analyze_integration",
                                     "create", "update", "upgrade", "backup", "restore", "monitor", "optimize_resources",
                                     "get_existing", "discover"],
                            "description": "Infrastructure action to perform",
                        },
                        # ================================================================
                        # PROJECT DESIGN PARAMS (for init_project, design_project, review_project, optimize_project)
                        # ================================================================
                        "project_name": {
                            "type": "string",
                            "description": "REQUIRED for init_project. Name of the project to create.",
                        },
                        "project_type": {
                            "type": "string",
                            "enum": ["terraform", "kubernetes", "devops", "platform"],
                            "description": "REQUIRED for init_project. Type of project: terraform, kubernetes, devops, platform",
                        },
                        "requirements": {
                            "type": "object",
                            "description": "Project requirements dict (e.g., {resources: ['EC2', 'RDS'], compliance: ['SOC2']}).",
                        },
                        "description": {"type": "string", "description": "Description of the project."},
                        # ================================================================
                        # LIFECYCLE PARAMS (for create, update, upgrade, backup, restore, monitor, optimize_resources)
                        # ================================================================
                        "infrastructure_type": {
                            "type": "string",
                            "enum": ["kubernetes", "multi_cloud", "hybrid_cloud", "terraform_project"],
                            "description": "REQUIRED for lifecycle actions (create/update/upgrade/etc). NOT for init_project.",
                        },
                        "resource_name": {
                            "type": "string",
                            "description": "REQUIRED for lifecycle actions (create/update/upgrade/etc). Name of the resource/cluster.",
                        },
                        "resource_type": {
                            "type": "string",
                            "description": "Resource type (e.g., EC2, RDS, S3, EKS) for lifecycle actions.",
                        },
                        "configuration": {
                            "type": "object",
                            "description": "Resource configuration dict for lifecycle actions.",
                        },
                        "target_environment": {
                            "type": "string",
                            "enum": ["dev", "staging", "prod"],
                            "description": "Target environment for deployment.",
                        },
                        "current_version": {"type": "string", "description": "Current version (for upgrade action)"},
                        "target_version": {"type": "string", "description": "Target version (for upgrade action)"},
                        "backup_type": {"type": "string", "enum": ["full", "incremental", "snapshot"], "default": "full", "description": "Backup type (for backup action)"},
                        "source_component": {"type": "string", "description": "Source component (for integrate action)"},
                        "target_component": {"type": "string", "description": "Target component (for integrate action)"},
                        "repository_url": {"type": "string", "description": "Git repository URL (for init_project or analyze)"},
                        "cloud_provider": {
                            "oneOf": [
                                {
                                    "type": "string",
                                    "enum": ["aws", "gcp", "azure", "multi-cloud"],
                                    "description": "Single cloud provider (aws, gcp, azure) or 'multi-cloud' for multi-provider architectures.",
                                },
                                {
                                    "type": "array",
                                    "items": {"type": "string", "enum": ["aws", "gcp", "azure"]},
                                    "description": "List of cloud providers for multi-cloud projects (e.g., ['aws', 'gcp', 'azure']).",
                                },
                            ],
                            "description": "Cloud provider(s). Use 'multi-cloud' or array ['aws','gcp','azure'] for multi-cloud. Auto-enriched from session.",
                        },
                        "include_compliance": {
                            "type": "boolean",
                            "default": False,
                            "description": "⚠️ REQUIRES compliance_standards array. Set true ONLY if you also provide compliance_standards. Extract standards from user prompt (e.g., 'PCI-DSS, HIPAA' → compliance_standards=['PCI-DSS', 'HIPAA']).",
                        },
                        "compliance_standards": {
                            "type": "array",
                            "items": {"type": "string", "enum": ["SOC2", "PCI-DSS", "HIPAA", "GDPR", "ISO27001", "NIST-800-53", "CIS", "FedRAMP", "SOX"]},
                            "description": "⚠️ REQUIRED when include_compliance=true. Extract ALL standards from user prompt. Valid: SOC2, PCI-DSS, HIPAA, GDPR, ISO27001, NIST-800-53, CIS, FedRAMP, SOX. Example: user says 'PCI-DSS and HIPAA compliant' → ['PCI-DSS', 'HIPAA'].",
                        },
                        "include_pricing": {"type": "boolean", "default": False, "description": "Include cost estimates in output"},
                        "generate_diagrams": {"type": "boolean", "default": True, "description": "Generate architecture diagrams"},
                        # ================================================================
                        # DISCOVERY PARAMS (for get_existing, discover)
                        # ================================================================
                        "account_id": {"type": "string", "description": "AWS account ID (for discover action)"},
                        "regions": {"type": "array", "items": {"type": "string"}, "description": "AWS regions to discover (for discover action)"},
                        "discovery_method": {"type": "string", "enum": ["sts_assume_role", "iam_role_anywhere"], "description": "Discovery method (for discover action)"},
                    },
                    "required": ["action"],
                },
            ),
            Tool(
                name="wistx_context",
                description=build_tool_description(
                    "wistx_context",
                    "🎯 UNIFIED context management. Actions: list_files, read_file (filesystem), "
                    "save, search, get, list_saved (context). Navigate repos and manage saved contexts."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["list_files", "read_file", "save", "search", "get", "list_saved"],
                            "description": "Context action: list_files/read_file (browse indexed repos), save/search/get/list_saved (manage contexts)",
                        },
                        # ================================================================
                        # FILESYSTEM PARAMS (for action='list_files', 'read_file')
                        # ================================================================
                        "resource_id": {"type": "string", "description": "REQUIRED for list_files/read_file. Indexed resource ID from wistx_index."},
                        "path": {"type": "string", "default": "/", "description": "REQUIRED for read_file. File path within the indexed resource."},
                        "view_mode": {"type": "string", "enum": ["standard", "compact", "detailed"], "default": "standard", "description": "Display mode for file content."},
                        "start_line": {"type": "integer", "description": "Start line for file content (for read_file)."},
                        "end_line": {"type": "integer", "description": "End line for file content (for read_file)."},
                        "include_dependencies": {"type": "boolean", "default": False, "description": "Include dependency analysis (for read_file)."},
                        "include_compliance": {"type": "boolean", "default": False, "description": "Include compliance analysis (for read_file)."},
                        "include_costs": {"type": "boolean", "default": False, "description": "Include cost analysis (for read_file)."},
                        "include_security": {"type": "boolean", "default": False, "description": "Include security analysis (for read_file)."},
                        # ================================================================
                        # CONTEXT MANAGEMENT PARAMS (for action='save', 'search', 'get', 'list_saved')
                        # ================================================================
                        "context_type": {"type": "string", "description": "REQUIRED for save. Context type (e.g., 'infrastructure', 'compliance', 'architecture')."},
                        "title": {"type": "string", "description": "REQUIRED for save. Title for the saved context."},
                        "summary": {"type": "string", "description": "REQUIRED for save. Summary/description of the context."},
                        "query": {"type": "string", "description": "REQUIRED for search. Search query to find saved contexts."},
                        "context_id": {"type": "string", "description": "REQUIRED for get. ID of the context to retrieve."},
                        "status": {"type": "string", "enum": ["active", "archived"], "description": "Filter by status (for list_saved/search)."},
                        "workspace": {"type": "string", "description": "Filter by workspace (for list_saved/search)."},
                        "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags for categorization (for save) or filtering (for search)."},
                        "limit": {"type": "integer", "default": 50, "description": "Max results to return."},
                        "offset": {"type": "integer", "default": 0, "description": "Pagination offset."},
                    },
                    "required": ["action"],
                },
            ),
            Tool(
                name="wistx_index",
                description=build_tool_description(
                    "wistx_index",
                    "🎯 UNIFIED indexing tool. Actions: repository (index GitHub repos), content (index docs/files), "
                    "list, status, delete (resource management). Indexing is asynchronous - returns immediately."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["repository", "content", "list", "status", "delete"],
                            "description": "Indexing action: repository (index GitHub), content (index docs), list/status/delete (manage resources)",
                        },
                        # ================================================================
                        # REPOSITORY INDEXING PARAMS (for action='repository')
                        # ================================================================
                        "repo_url": {"type": "string", "description": "REQUIRED for repository. GitHub repository URL (e.g., https://github.com/owner/repo)."},
                        "branch": {"type": "string", "default": "main", "description": "Git branch to index (for repository)."},
                        "github_token": {"type": "string", "description": "GitHub personal access token for private repos (for repository)."},
                        # ================================================================
                        # CONTENT INDEXING PARAMS (for action='content')
                        # ================================================================
                        "content_url": {"type": "string", "description": "REQUIRED for content (if no file_path). URL of documentation to index."},
                        "file_path": {"type": "string", "description": "Alternative to content_url. Local file path to index."},
                        "content_type": {"type": "string", "description": "Content type hint (e.g., 'markdown', 'html', 'pdf')."},
                        # ================================================================
                        # COMMON PARAMS (for repository/content)
                        # ================================================================
                        "name": {"type": "string", "description": "Human-readable name for the indexed resource."},
                        "description": {"type": "string", "description": "Description of the indexed resource."},
                        "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags for categorization and filtering."},
                        "include_patterns": {"type": "array", "items": {"type": "string"}, "description": "Glob patterns to include (e.g., ['*.tf', '*.yaml'])."},
                        "exclude_patterns": {"type": "array", "items": {"type": "string"}, "description": "Glob patterns to exclude (e.g., ['node_modules/**'])."},
                        "include_ai_analysis": {"type": "boolean", "default": True, "description": "Include AI-powered analysis of code."},
                        "deduplicate": {"type": "boolean", "default": True, "description": "Deduplicate content during indexing."},
                        # ================================================================
                        # RESOURCE MANAGEMENT PARAMS (for action='list', 'status', 'delete')
                        # ================================================================
                        "resource_type": {"type": "string", "enum": ["repository", "content"], "description": "REQUIRED for delete. Type of resource to delete."},
                        "resource_id": {"type": "string", "description": "REQUIRED for status. Resource ID to check status of."},
                        "identifier": {"type": "string", "description": "REQUIRED for delete. Resource identifier (URL, owner/repo, or ID)."},
                        "status_filter": {"type": "string", "enum": ["pending", "processing", "completed", "failed"], "description": "Filter by indexing status (for list)."},
                    },
                    "required": ["action"],
                },
            ),
            Tool(
                name="wistx_research",
                description=build_tool_description(
                    "wistx_research",
                    "🎯 UNIFIED research tool. Sources: knowledge_base (internal KB), web (general search), "
                    "security (CVEs, advisories), all (combined). For deep research and real-time information."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "source": {
                            "type": "string",
                            "enum": ["knowledge_base", "web", "security", "all"],
                            "description": "REQUIRED. Research source: knowledge_base (internal), web (internet), security (CVEs), all (combined)",
                        },
                        "query": {"type": "string", "description": "REQUIRED. Search query describing what you're looking for."},
                        # ================================================================
                        # KNOWLEDGE BASE PARAMS (for source='knowledge_base')
                        # ================================================================
                        "domains": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Knowledge domains to search (e.g., ['terraform', 'kubernetes', 'aws']).",
                        },
                        "content_types": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Content types to filter (e.g., ['documentation', 'tutorial', 'reference']).",
                        },
                        "include_cross_domain": {"type": "boolean", "default": True, "description": "Include results from related domains."},
                        "include_web_search": {"type": "boolean", "default": True, "description": "Supplement KB results with web search."},
                        "format": {"type": "string", "enum": ["structured", "markdown", "json"], "default": "structured", "description": "Output format."},
                        "research_url": {"type": "string", "description": "Specific URL to research (for deep research)."},
                        "enable_deep_research": {"type": "boolean", "default": False, "description": "Enable comprehensive deep research mode."},
                        # ================================================================
                        # WEB/SECURITY PARAMS (for source='web', 'security')
                        # ================================================================
                        "search_type": {"type": "string", "enum": ["general", "technical", "pricing", "documentation"], "default": "general", "description": "Type of web search."},
                        "resource_type": {"type": "string", "description": "Resource type for security search (e.g., 'EC2', 'RDS')."},
                        "cloud_provider": {
                            "oneOf": [
                                {"type": "string", "enum": ["aws", "gcp", "azure", "multi-cloud"]},
                                {"type": "array", "items": {"type": "string", "enum": ["aws", "gcp", "azure"]}},
                            ],
                            "description": "Cloud provider(s) filter. Use 'multi-cloud' or array for multi-cloud. Auto-enriched from session.",
                        },
                        "severity": {"type": "string", "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW"], "description": "CVE severity filter (for security search)."},
                        "include_cves": {"type": "boolean", "default": True, "description": "Include CVE results (for security search)."},
                        "include_advisories": {"type": "boolean", "default": True, "description": "Include security advisories (for security search)."},
                        "max_results": {"type": "integer", "default": 1000, "description": "Maximum results to return."},
                    },
                    "required": ["source", "query"],
                },
            ),
            Tool(
                name="wistx_packages",
                description=build_tool_description(
                    "wistx_packages",
                    "🎯 UNIFIED packages tool. Actions: search (packages, tools, services, docs), "
                    "read_file (package source). Searches PyPI, npm, Terraform Registry, Helm, and more."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["search", "read_file"],
                            "description": "Packages action: search (find packages), read_file (view package source code)",
                        },
                        # ================================================================
                        # SEARCH PARAMS (for action='search')
                        # ================================================================
                        "query": {"type": "string", "description": "REQUIRED for search. Search query (e.g., 'terraform aws vpc module')."},
                        "resource_types": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Filter by resource types (e.g., ['terraform_module', 'helm_chart', 'npm_package']).",
                        },
                        "pattern": {"type": "string", "description": "Regex pattern (alternative to query for search)."},
                        "template": {"type": "string", "description": "Pre-built template name (alternative to query for search)."},
                        "search_type": {
                            "type": "string",
                            "enum": ["semantic", "exact", "regex"],
                            "default": "semantic",
                            "description": "Search type: semantic (natural language), exact (exact match), regex (pattern).",
                        },
                        "registry": {
                            "type": "string",
                            "enum": ["pypi", "npm", "terraform", "helm", "docker", "github"],
                            "description": "REQUIRED for read_file. Package registry to search in.",
                        },
                        "domain": {"type": "string", "description": "Filter by domain (e.g., 'infrastructure', 'security')."},
                        "category": {"type": "string", "description": "Filter by category (e.g., 'monitoring', 'networking')."},
                        "package_name": {"type": "string", "description": "REQUIRED for read_file. Package name to read."},
                        "limit": {"type": "integer", "default": 1000, "description": "Maximum results to return."},
                        # ================================================================
                        # READ FILE PARAMS (for action='read_file')
                        # ================================================================
                        "filename_sha256": {"type": "string", "description": "REQUIRED for read_file. SHA256 hash of the file to read."},
                        "start_line": {"type": "integer", "default": 1, "description": "Start line for file content."},
                        "end_line": {"type": "integer", "default": 100, "description": "End line for file content."},
                        "version": {"type": "string", "description": "Package version (for read_file)."},
                    },
                    "required": ["action"],
                },
            ),
            Tool(
                name="wistx_compliance_automation",
                description=build_tool_description(
                    "wistx_compliance_automation",
                    "🎯 UNIFIED compliance automation tool. Actions: generate_cicd_gate (CI/CD pipeline compliance), "
                    "calculate_sample/select_sample (PCAOB AS 2315 audit sampling), "
                    "generate_workpaper/generate_workpaper_package (AICPA-compliant audit workpapers). "
                    "Supports SOC2, PCI-DSS, HIPAA, ISO-27001, NIST-800-53, GDPR, FedRAMP, CIS, CCPA, SOX, GLBA."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["generate_cicd_gate", "generate_pre_commit", "calculate_sample", "select_sample", "generate_workpaper", "generate_workpaper_package"],
                            "description": "Action: generate_cicd_gate (CI/CD configs), calculate_sample (sample size), select_sample (select items), generate_workpaper (single), generate_workpaper_package (full package)",
                        },
                        # === CI/CD GATE PARAMS ===
                        "platform": {
                            "type": "string",
                            "enum": ["github_actions", "gitlab_ci", "azure_devops", "jenkins", "bitbucket", "circleci"],
                            "description": "CI/CD platform for generate_cicd_gate. Omit to generate for all platforms.",
                        },
                        "frameworks": {
                            "type": "array",
                            "items": {"type": "string", "enum": ["SOC2", "PCI-DSS", "HIPAA", "ISO-27001", "NIST-800-53", "GDPR", "FedRAMP", "CIS", "CCPA", "SOX", "GLBA"]},
                            "description": "Compliance frameworks to enforce in CI/CD gate.",
                        },
                        "gate_mode": {
                            "type": "string",
                            "enum": ["blocking", "warning", "audit"],
                            "default": "blocking",
                            "description": "Gate behavior: blocking (fail pipeline), warning (warn only), audit (log only).",
                        },
                        "min_compliance_score": {"type": "number", "default": 85.0, "description": "Minimum compliance score (0-100) to pass gate."},
                        "max_critical_findings": {"type": "integer", "default": 0, "description": "Max critical findings allowed."},
                        "max_high_findings": {"type": "integer", "default": 3, "description": "Max high findings allowed."},
                        # === SAMPLING PARAMS ===
                        "sampling_method": {
                            "type": "string",
                            "enum": ["mus", "attribute", "haphazard"],
                            "description": "Sampling method: mus (Monetary Unit), attribute (tests of controls), haphazard (non-statistical).",
                        },
                        "population_size": {"type": "integer", "description": "Total items in population."},
                        "population_value": {"type": "number", "description": "Total monetary value of population (for MUS)."},
                        "tolerable_misstatement": {"type": "number", "description": "Tolerable misstatement amount (for MUS)."},
                        "tolerable_rate": {"type": "number", "description": "Tolerable deviation rate 0-1 (for attribute sampling)."},
                        "expected_rate": {"type": "number", "description": "Expected deviation rate 0-1 (for attribute sampling)."},
                        "risk_level": {"type": "string", "enum": ["low", "moderate", "high"], "default": "moderate", "description": "Risk of material misstatement."},
                        "population_items": {"type": "array", "items": {"type": "object"}, "description": "Population items for select_sample."},
                        "sample_size": {"type": "integer", "description": "Sample size for haphazard sampling."},
                        # === WORKPAPER PARAMS ===
                        "engagement_name": {"type": "string", "description": "REQUIRED for workpapers. Audit engagement name."},
                        "period_start": {"type": "string", "description": "Audit period start (ISO date: YYYY-MM-DD)."},
                        "period_end": {"type": "string", "description": "Audit period end (ISO date: YYYY-MM-DD)."},
                        "preparer": {"type": "string", "description": "Workpaper preparer name."},
                        "workpaper_type": {
                            "type": "string",
                            "enum": ["control_testing", "evidence_collection", "summary"],
                            "description": "Workpaper type for generate_workpaper.",
                        },
                        "control_id": {"type": "string", "description": "Control ID (e.g., CC6.1) for control_testing workpaper."},
                        "control_description": {"type": "string", "description": "Control description for control_testing workpaper."},
                        "testing_procedures": {"type": "array", "items": {"type": "string"}, "description": "Testing procedures performed."},
                        "sample_items": {"type": "array", "items": {"type": "object"}, "description": "Sample items tested."},
                        "exceptions": {"type": "array", "items": {"type": "object"}, "description": "Exceptions/deviations found."},
                        "conclusion": {"type": "string", "description": "Testing conclusion."},
                        "evidence_items": {"type": "array", "items": {"type": "object"}, "description": "Evidence items for evidence_collection workpaper."},
                        "findings": {"type": "array", "items": {"type": "object"}, "description": "Findings for summary workpaper."},
                        "overall_conclusion": {"type": "string", "description": "Overall conclusion for summary workpaper."},
                        "controls_tested": {"type": "array", "items": {"type": "object"}, "description": "Controls tested for workpaper_package."},
                        "output_format": {"type": "string", "enum": ["markdown", "json"], "default": "markdown", "description": "Output format."},
                    },
                    "required": ["action"],
                },
            ),
            ]
            logger.info("Registered %d MCP tools: %s", len(tools), [t.name for t in tools])

            from wistx_mcp.tools.lib.protocol_handler import ensure_protocol_compliance

            protocol_version = get_request_context().get("protocol_version")
            compliant_tools = ensure_protocol_compliance(tools, protocol_version=protocol_version)

            try:
                tool_dicts = []
                for tool in compliant_tools:
                    if hasattr(tool, 'model_dump'):
                        tool_dict = tool.model_dump()
                    elif hasattr(tool, 'dict'):
                        tool_dict = tool.dict()
                    elif isinstance(tool, dict):
                        tool_dict = tool
                    else:
                        tool_dict = {
                            "name": getattr(tool, 'name', 'unknown'),
                            "description": getattr(tool, 'description', ''),
                            "inputSchema": getattr(tool, 'inputSchema', {}),
                        }
                    tool_dicts.append(tool_dict)
                distributed_cache.set_tool_definitions(tool_dicts)
                logger.debug("Cached tool list (%d tools)", len(tool_dicts))
            except Exception as e:
                logger.warning("Failed to cache tool list: %s", e)

            try:
                init_event = await get_initialization_event()
                if not init_event.is_set():
                    init_event.set()
                    logger.debug("Initialization event set after tool list build")
            except Exception as e:
                logger.debug("Failed to set initialization event: %s", e)

            return compliant_tools
        except (ValueError, RuntimeError, AttributeError) as e:
            logger.error("Error in list_tools(): %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error in list_tools(): %s", e, exc_info=True)
            raise RuntimeError(f"Failed to list tools: {e}") from e

    def _format_existing_infrastructure_result(result: dict[str, Any]) -> str:
        """Format existing infrastructure result as markdown.
        
        Args:
            result: Infrastructure context result dictionary
            
        Returns:
            Formatted markdown string
        """
        # Check if this is a setup guide response
        if result.get("setup_required"):
            from wistx_mcp.tools.lib.context_builder import ContextBuilder
            return ContextBuilder.format_indexing_setup_guide(result)
        
        from wistx_mcp.tools.lib.context_builder import MarkdownBuilder
        
        builder = MarkdownBuilder()
        builder.add_header("Existing Infrastructure Context", level=1)
        
        repository_url = result.get("repository_url", "")
        environment_name = result.get("environment_name")
        status = result.get("status", "unknown")
        resource_id = result.get("resource_id")
        
        builder.add_bold(f"Repository: {repository_url}")
        builder.add_line_break()
        if environment_name:
            builder.add_bold(f"Environment: {environment_name}")
            builder.add_line_break()
        builder.add_bold(f"Status: {status}")
        builder.add_line_break()
        
        if status == "not_indexed":
            builder.add_paragraph(result.get("message", "Repository not indexed."))
            if result.get("recommendations"):
                builder.add_header("Recommendations", level=2)
                for rec in result["recommendations"]:
                    builder.add_list_item(rec)
            return builder.build()
        
        if resource_id:
            builder.add_bold(f"Resource ID: {resource_id}")
            builder.add_line_break()
        
        resources_count = result.get("resources_count", 0)
        total_monthly = result.get("total_monthly_cost", 0.0)
        total_annual = result.get("total_annual_cost", 0.0)
        
        builder.add_header("Cost Summary", level=2)
        builder.add_list_item(f"**Total Resources**: {resources_count}")
        builder.add_list_item(f"**Monthly Cost**: ${total_monthly:.2f}")
        builder.add_list_item(f"**Annual Cost**: ${total_annual:.2f}")
        
        cost_breakdown = result.get("cost_breakdown", {})
        if cost_breakdown:
            builder.add_header("Cost Breakdown", level=3)
            for service, cost in cost_breakdown.items():
                builder.add_list_item(f"**{service}**: ${cost:.2f}/month")
        
        cost_optimizations = result.get("cost_optimizations", [])
        if cost_optimizations:
            builder.add_header("Cost Optimization Opportunities", level=2)
            for opt in cost_optimizations[:5]:
                builder.add_list_item(opt)
        
        compliance_status = result.get("compliance_status")
        compliance_summary = result.get("compliance_summary", {})
        
        if compliance_status and compliance_summary:
            builder.add_header("Compliance Status", level=2)
            builder.add_bold(f"Overall Status: {compliance_status.upper()}")
            builder.add_line_break()
            
            for standard, data in compliance_summary.items():
                rate = data.get("compliance_rate", 0)
                compliant_count = data.get("compliant_count", 0)
                total_components = data.get("total_components", 0)
                builder.add_list_item(
                    f"**{standard.upper()}**: {rate:.1f}% compliant "
                    f"({compliant_count}/{total_components} components)"
                )
        
        recommendations = result.get("recommendations", [])
        if recommendations:
            builder.add_header("Recommendations", level=2)
            for rec in recommendations:
                builder.add_list_item(rec)
        
        context_for_agents = result.get("context_for_agents")
        if context_for_agents:
            builder.add_header("Context for Coding Agents", level=2)
            builder.add_code_block(context_for_agents, language="text")
        
        return builder.build()

    _tools_cache: list[Tool] | None = None

    def _validate_tool_arguments(tool: Tool, arguments: dict) -> None:
        """Validate tool arguments against input schema with comprehensive error handling.

        Args:
            tool: Tool definition with input schema
            arguments: Arguments to validate

        Raises:
            MCPError: If validation fails with context
            RuntimeError: If jsonschema is not available
        """
        try:
            from jsonschema import validate, ValidationError, SchemaError
        except ImportError as e:
            raise RuntimeError(
                "jsonschema library is required for argument validation. "
                "Install it with: pip install jsonschema"
            ) from e

        try:
            validate(instance=arguments, schema=tool.inputSchema)
        except SchemaError as e:
            logger.error("Invalid tool schema for %s: %s", tool.name, e)
            raise MCPError(
                code=MCPErrorCode.INTERNAL_ERROR,
                message=f"Invalid tool schema: {e.message}",
                data={"tool": tool.name, "schema_error": str(e)},
            ) from e
        except ValidationError as e:
            error_path = ".".join(str(p) for p in e.path) if e.path else "root"
            error_message = e.message

            if e.validator == "required":
                missing = e.validator_value
                error_message = f"Missing required field(s): {', '.join(missing)}"
            elif e.validator == "type":
                expected = e.validator_value
                error_message = f"Expected type {expected}, got {type(e.instance).__name__}"
            elif e.validator == "enum":
                allowed = e.validator_value
                error_message = f"Value must be one of: {', '.join(str(v) for v in allowed)}"

            raise MCPError(
                code=MCPErrorCode.INVALID_PARAMS,
                message=f"Invalid argument '{error_path}': {error_message}",
                data={
                    "tool": tool.name,
                    "field": error_path,
                    "error": error_message,
                    "validator": e.validator,
                },
            ) from e
        except Exception as e:
            logger.error("Unexpected error validating arguments: %s", e, exc_info=True)
            raise MCPError(
                code=MCPErrorCode.INTERNAL_ERROR,
                message="Argument validation failed",
                data={"tool": tool.name, "error": str(e)},
            ) from e

    @app.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        """Handle tool calls with authentication, rate limiting, and security checks."""
        from wistx_mcp.tools.lib.metrics import get_tool_metrics

        request_id = request_id_var.get() or str(uuid.uuid4())
        start_time = time.time()
        success = False
        error: Exception | None = None
        try:
            request_id = validate_request_id(request_id)
        except ValueError:
            request_id = str(uuid.uuid4())

        if not request_id_var.get():
            request_id_var.set(request_id)

        # Extract and set session ID for cross-tool context sharing
        # Session ID is derived from: _meta.sessionId > connection_id > generated UUID
        session_id = extract_session_id(arguments, arguments.get("_meta"))
        set_current_session_id(session_id)

        async with _inflight_lock:
            _inflight_requests.add(request_id)

        auth_ctx = None
        try:
            if "api_key" in arguments:
                raise MCPError(
                    code=MCPErrorCode.INVALID_PARAMS,
                    message="API key cannot be passed via tool arguments for security reasons. Use WISTX_API_KEY environment variable or provide via MCP initialization.",
                    data={"request_id": request_id, "tool": name},
                )

            try:
                raw_serialized = json.dumps(arguments)
                raw_size = len(raw_serialized.encode("utf-8"))
                if raw_size > MAX_REQUEST_SIZE_BYTES:
                    raise MCPError(
                        code=MCPErrorCode.INVALID_PARAMS,
                        message=f"Request too large: {raw_size} bytes (max {MAX_REQUEST_SIZE_BYTES})",
                    )
            except (TypeError, ValueError) as e:
                if isinstance(e, MCPError):
                    raise
                raise MCPError(
                    code=MCPErrorCode.INVALID_PARAMS,
                    message=f"Cannot serialize request arguments: {sanitize_error_message(e)}",
                ) from e

            sanitized_args = sanitize_tool_arguments(arguments)
            
            from wistx_mcp.tools.lib.tool_registry import (
                is_tool_deprecated,
                get_deprecation_warning,
                get_tool_version,
                resolve_tool_name,
            )
            
            resolved_name = resolve_tool_name(name)
            if resolved_name == "wistx_search_devops_resources" or name == "wistx_search_devops_resources":
                invalid_params = ["cloud_provider", "code_types"]
                removed_params = []
                for param in invalid_params:
                    if param in sanitized_args:
                        removed_params.append(param)
                        del sanitized_args[param]
                if removed_params:
                    logger.warning(
                        "Removed invalid parameters from wistx_search_devops_resources: %s. "
                        "These parameters are not supported. Include cloud provider in query instead.",
                        removed_params,
                    )
            
            if resolved_name == "wistx_save_context_with_analysis" or name == "wistx_save_context_with_analysis":
                if "compliance_standards" in sanitized_args:
                    logger.warning(
                        "Removed invalid parameter 'compliance_standards' from wistx_save_context_with_analysis. "
                        "This parameter is not supported. Compliance standards are inferred from infrastructure_resources during auto_analyze."
                    )
                    del sanitized_args["compliance_standards"]
                
                if "infrastructure_resources" in sanitized_args and sanitized_args["infrastructure_resources"]:
                    normalized_resources = []
                    for resource in sanitized_args["infrastructure_resources"]:
                        if not isinstance(resource, dict):
                            continue
                        
                        normalized_resource = {}
                        valid_fields = ["resource_id", "resource_type", "path", "name", "changes"]
                        for field in valid_fields:
                            if field in resource:
                                normalized_resource[field] = resource[field]
                        
                        removed_fields = []
                        for field in resource.keys():
                            if field not in valid_fields:
                                removed_fields.append(field)
                        
                        if removed_fields:
                            logger.debug(
                                "Removed invalid fields from infrastructure_resource: %s. "
                                "InfrastructureResource model only supports: %s",
                                removed_fields,
                                ", ".join(valid_fields),
                            )
                        
                        required_fields = ["resource_id", "resource_type", "path", "name"]
                        if all(field in normalized_resource for field in required_fields):
                            normalized_resources.append(normalized_resource)
                        else:
                            logger.warning(
                                "Skipped infrastructure_resource missing required fields. "
                                "Required: %s, Found: %s",
                                required_fields,
                                list(normalized_resource.keys()),
                            )
                    
                    sanitized_args["infrastructure_resources"] = normalized_resources
            try:
                from api.services.version_tracking_service import version_tracking_service
            except ImportError:
                version_tracking_service = None

            tools_list = await list_tools()
            tool = next((t for t in tools_list if t.name == resolved_name), None)
            if not tool:
                raise MCPError(
                    code=MCPErrorCode.METHOD_NOT_FOUND,
                    message=f"Unknown tool: {name}",
                    data={"request_id": request_id, "tool": name},
                )

            tool_version_info = get_tool_version(resolved_name)
            tool_version = None
            if tool_version_info:
                tool_version = tool_version_info.get("current_version", "v1")
            
            actual_tool_name = resolved_name

            if is_tool_deprecated(actual_tool_name):
                deprecation_warning = get_deprecation_warning(actual_tool_name)
                if deprecation_warning:
                    logger.warning(
                        "Deprecated tool called: %s [request_id=%s] - %s",
                        actual_tool_name,
                        request_id,
                        deprecation_warning,
                    )
                    from wistx_mcp.tools.lib.tool_registry import get_tool_version
                    version_info = get_tool_version(actual_tool_name)
                    if version_info:
                        logger.info(
                            "Tool version info for %s: current=%s, deprecated=%s",
                            actual_tool_name,
                            version_info.get("current_version"),
                            version_info.get("deprecated_versions", []),
                        )

            user_id = None
            api_key_id = None
            auth_ctx = get_auth_context()
            if auth_ctx:
                user_id = auth_ctx.get_user_id()
                api_key_id = auth_ctx.get_api_key_id()

                # Phase 3: Log authentication event
                audit_logger.log_authentication(
                    user_id=user_id or "unknown",
                    auth_method="api_key",
                    success=True,
                )

            if version_tracking_service:
                try:
                    version_tracking_service.track_mcp_tool_version_usage(
                        tool_name=actual_tool_name,
                        tool_version=tool_version,
                        user_id=user_id,
                        api_key_id=api_key_id,
                    )
                except Exception as e:
                    logger.debug("Failed to track MCP tool version usage: %s", e)

            _validate_tool_arguments(tool, sanitized_args)

            deduplicator_instance = await get_request_deduplicator(ttl_seconds=REQUEST_DEDUPLICATION_TTL_SECONDS)
            cached_result = await deduplicator_instance.check_duplicate(request_id, name, sanitized_args)
            if cached_result is not None:
                logger.info("Returning cached result for duplicate request [request_id=%s]", request_id)
                success = True
                return cached_result

            context = get_request_context()
            logger.info(
                "Tool called: %s [request_id=%s, user_id=%s] with arguments: %s",
                name,
                context.get("request_id", request_id),
                context.get("user_id", "unknown"),
                safe_json_dumps(sanitize_arguments(sanitized_args), indent=2),
            )

            set_request_context({
                "request_id": request_id,
                "user_id": None,
                "tool_name": name,
            })

            from wistx_mcp.tools.lib.security_logger import (
                SecurityEventType,
                get_security_logger,
            )

            security_logger = get_security_logger()

            existing_auth_ctx = get_auth_context()
            if not existing_auth_ctx:
                api_key = os.getenv("WISTX_API_KEY") or settings.api_key
                if api_key and AuthContext is not None:
                    try:
                        logger.info("No auth context found, attempting to create from environment/settings [request_id=%s]", request_id)
                        auth_ctx = AuthContext(api_key=api_key)
                        await auth_ctx.validate()
                        set_auth_context(auth_ctx)
                        existing_auth_ctx = auth_ctx
                        logger.info(
                            "Authentication context created from environment for user: %s [request_id=%s]",
                            auth_ctx.get_user_id(),
                            request_id,
                        )
                    except Exception as e:
                        logger.warning("Failed to create auth context from environment: %s [request_id=%s]", e, request_id)
                
                if not existing_auth_ctx:
                    await security_logger.log_security_event(
                        event_type=SecurityEventType.AUTHENTICATION_FAILURE,
                        tool_name=name,
                        severity="HIGH",
                        details={"reason": "no_auth_context"},
                        alert=True,
                    )
                    raise MCPError(
                        code=MCPErrorCode.INVALID_REQUEST,
                        message="Authentication required. Set WISTX_API_KEY in Claude Desktop MCP server configuration (env section) or provide via MCP initialization options.",
                        data={"request_id": request_id, "tool": name},
                    )
            else:
                auth_ctx = existing_auth_ctx
                if not auth_ctx.user_info:
                    try:
                        await auth_ctx.validate()
                    except Exception as e:
                        logger.warning("Failed to validate auth context: %s", e)
                        await security_logger.log_security_event(
                            event_type=SecurityEventType.AUTHENTICATION_FAILURE,
                            tool_name=name,
                            severity="HIGH",
                            details={"reason": "validation_failed", "error": str(e)},
                            alert=True,
                        )
                        raise MCPError(
                            code=MCPErrorCode.INVALID_REQUEST,
                            message="Authentication failed. Invalid API key.",
                            data={"request_id": request_id, "tool": name},
                        ) from e
                user_id = auth_ctx.get_user_id() or "unknown"
                update_request_context(user_id=user_id)
                await security_logger.log_security_event(
                    event_type=SecurityEventType.AUTHENTICATION_SUCCESS,
                    user_id=user_id,
                    tool_name=name,
                    severity="INFO",
                )

            from wistx_mcp.tools.lib.tool_permissions import (
                get_tool_permissions,
                check_plan_access,
            )

            tool_perms = get_tool_permissions(actual_tool_name)
            required_plan = tool_perms.get("required_plan", "professional")
            required_permission = tool_perms.get("required_permission")
            quota_required = tool_perms.get("quota_required", True)

            from wistx_mcp.tools.lib.tool_permissions import get_default_plan
            
            default_plan = get_default_plan()
            user_plan = auth_ctx.user_info.get("plan", default_plan) if auth_ctx.user_info else default_plan

            if not check_plan_access(user_plan, required_plan):
                await security_logger.log_security_event(
                    event_type=SecurityEventType.AUTHORIZATION_DENIED,
                    user_id=user_id,
                    tool_name=actual_tool_name,
                    severity="HIGH",
                    details={
                        "reason": "insufficient_plan",
                        "required_plan": required_plan,
                        "user_plan": user_plan,
                    },
                    alert=True,
                )
                raise MCPError(
                    code=MCPErrorCode.INVALID_REQUEST,
                    message=f"Tool '{actual_tool_name}' requires {required_plan} plan or higher. Your current plan: {user_plan}",
                    data={
                        "request_id": request_id,
                        "tool": actual_tool_name,
                        "required_plan": required_plan,
                        "user_plan": user_plan,
                    },
                )

            if required_permission:
                from wistx_mcp.tools.lib.tool_permissions import check_tool_permission
                
                user_info_dict = auth_ctx.user_info or {}
                has_permission = check_tool_permission(user_info_dict, required_permission)
                
                if not has_permission:
                    await security_logger.log_security_event(
                        event_type=SecurityEventType.AUTHORIZATION_DENIED,
                        user_id=user_id,
                        tool_name=actual_tool_name,
                        severity="HIGH",
                        details={
                            "reason": "missing_permission",
                            "required_permission": required_permission,
                            "user_plan": user_plan,
                            "is_super_admin": user_info_dict.get("is_super_admin", False),
                            "admin_permissions": user_info_dict.get("admin_permissions", []),
                        },
                        alert=True,
                    )
                    raise MCPError(
                        code=MCPErrorCode.INVALID_REQUEST,
                        message=f"Tool '{actual_tool_name}' requires permission: {required_permission}",
                        data={
                            "request_id": request_id,
                            "tool": actual_tool_name,
                            "required_permission": required_permission,
                        },
                    )

            if quota_required:
                if user_id and user_id != "unknown":
                    try:
                        from api.services.quota_service import quota_service, QuotaExceededError
                        await quota_service.check_query_quota(user_id, user_plan)
                    except ImportError:
                        logger.debug("API quota service not available, skipping quota check")
                    except QuotaExceededError as e:
                        raise MCPError(
                            code=MCPErrorCode.RATE_LIMIT_EXCEEDED,
                            message=f"Quota exceeded: {sanitize_error_message(str(e))}",
                            data={"request_id": request_id, "tool": actual_tool_name, "user_id": user_id},
                        ) from e
                    except ValueError as e:
                        raise MCPError(
                            code=MCPErrorCode.RATE_LIMIT_EXCEEDED,
                            message=f"Quota exceeded: {sanitize_error_message(e)}",
                            data={"request_id": request_id, "tool": actual_tool_name, "user_id": user_id},
                        ) from e
                    except Exception as e:
                        logger.warning("Quota check failed (non-fatal): %s", e)
                else:
                    logger.debug("Skipping quota check for unauthenticated user")

            rate_limiter_instance = await get_rate_limiter(
                max_calls=MAX_RATE_LIMIT_CALLS,
                window_seconds=RATE_LIMIT_WINDOW_SECONDS,
            )
            rate_limit_id = f"{user_id}:{hashlib.sha256(f'{user_id}:{name}'.encode()).hexdigest()}"

            if not await rate_limiter_instance.check_rate_limit(rate_limit_id):
                await security_logger.log_security_event(
                    event_type=SecurityEventType.RATE_LIMIT_EXCEEDED,
                    user_id=user_id,
                    tool_name=actual_tool_name,
                    severity="MEDIUM",
                    details={"rate_limit_id": rate_limit_id[:20]},
                    alert=True,
                )

                # Phase 3: Log rate limit event
                audit_logger.log_rate_limit(
                    user_id=user_id or "unknown",
                    tool_name=actual_tool_name,
                    retry_after=RATE_LIMIT_WINDOW_SECONDS,
                )

                raise MCPError(
                    code=MCPErrorCode.RATE_LIMIT_EXCEEDED,
                    message=f"Rate limit exceeded. Limit: {MAX_RATE_LIMIT_CALLS} calls per {RATE_LIMIT_WINDOW_SECONDS} seconds. Please try again after {RATE_LIMIT_WINDOW_SECONDS} seconds.",
                    data={
                        "request_id": request_id,
                        "tool": name,
                        "user_id": user_id,
                        "limit": MAX_RATE_LIMIT_CALLS,
                        "window_seconds": RATE_LIMIT_WINDOW_SECONDS,
                        "retry_after": RATE_LIMIT_WINDOW_SECONDS,
                        "suggestion": f"Wait {RATE_LIMIT_WINDOW_SECONDS} seconds before retrying, or use a different tool if available.",
                    },
                )

            concurrent_limiter_instance = await get_concurrent_limiter(max_concurrent=MAX_CONCURRENT_TOOLS)
            acquired = False
            try:
                await concurrent_limiter_instance.acquire(user_id)
                acquired = True

                # ================================================================
                # CENTRALIZED AUTO-ENRICHMENT FROM SESSION CONTEXT
                # ================================================================
                # Enrich tool arguments with context from previous tool calls
                # in this session. This enables tool chaining without requiring
                # the AI to manually pass parameters between tools.
                #
                # Example: After wistx_infrastructure + wistx_get_compliance_requirements,
                # wistx_generate_documentation automatically receives:
                # - cloud_provider
                # - resource_types
                # - compliance_standards
                # - infrastructure_code (scaffolding)
                # ================================================================
                enriched_args, enriched_params = enrich_arguments_from_session(
                    actual_tool_name, sanitized_args
                )
                if enriched_params:
                    logger.info(
                        "Auto-enriched tool '%s' with %d parameters from session context: %s [request_id=%s]",
                        actual_tool_name,
                        len(enriched_params),
                        ", ".join(enriched_params),
                        request_id,
                    )
                # Use enriched args for tool execution
                tool_args = enriched_args

                async def execute_tool() -> list[TextContent]:
                    return await _execute_tool_internal(actual_tool_name, tool_args, auth_ctx)

                tool_timeout = TOOL_TIMEOUTS.get(name, GLOBAL_TOOL_TIMEOUT_SECONDS)
                result = await asyncio.wait_for(execute_tool(), timeout=tool_timeout)
                success = True

                from wistx_mcp.tools.lib.protocol_handler import ensure_protocol_compliance

                protocol_version = get_request_context().get("protocol_version")
                compliant_result = ensure_protocol_compliance(result, protocol_version=protocol_version)

                if is_tool_deprecated(actual_tool_name):
                    deprecation_warning = get_deprecation_warning(actual_tool_name)
                    if deprecation_warning:
                        warning_content = TextContent(
                            type="text",
                            text=f"⚠️ DEPRECATION WARNING: {deprecation_warning}"
                        )
                        compliant_result = [warning_content] + compliant_result

                await deduplicator_instance.store_result(request_id, name, sanitized_args, compliant_result)

                # Store result in session context for cross-tool context sharing
                # This enables downstream tools (e.g., wistx_generate_documentation) to
                # automatically access results from upstream tools (e.g., wistx_get_compliance_requirements)
                #
                # NOTE: Some tools (wistx_get_compliance_requirements, wistx_infrastructure, wistx_calculate_infrastructure_cost)
                # store STRUCTURED data directly in _execute_tool_internal. We should NOT overwrite that with
                # the markdown text returned. Check if structured data was already stored.
                try:
                    # Check if a structured result was already stored by the tool handler
                    existing_result = get_previous_tool_result(actual_tool_name)

                    # Only store if no structured data exists, or if existing data is just text
                    if existing_result is None or isinstance(existing_result, str):
                        # Extract structured result for context storage (first text content)
                        result_for_context = None
                        if compliant_result and len(compliant_result) > 0:
                            first_content = compliant_result[0]
                            if hasattr(first_content, 'text'):
                                # Try to parse JSON from text content
                                try:
                                    result_for_context = json.loads(first_content.text)
                                except (json.JSONDecodeError, TypeError):
                                    # Store raw text if not JSON
                                    result_for_context = first_content.text

                        if result_for_context is not None:
                            store_tool_result(actual_tool_name, tool_args, result_for_context)
                            logger.debug("Stored tool result in session context: %s", actual_tool_name)
                    else:
                        logger.debug(
                            "Skipping generic storage for %s - structured data already stored by tool handler",
                            actual_tool_name
                        )
                except Exception as e:
                    # Non-fatal: context storage failure shouldn't break tool execution
                    logger.debug("Failed to store tool result in session context: %s", e)

                return compliant_result
            finally:
                if acquired:
                    await concurrent_limiter_instance.release(user_id)

        except MCPError:
            raise
        except asyncio.TimeoutError:
            tool_timeout = TOOL_TIMEOUTS.get(name, GLOBAL_TOOL_TIMEOUT_SECONDS)
            error = TimeoutError(f"Tool {name} execution timed out after {tool_timeout} seconds")
            logger.error("Tool execution timeout: %s [request_id=%s]", name, request_id)
            raise MCPError(
                code=MCPErrorCode.TIMEOUT,
                message=f"Tool execution timed out after {tool_timeout} seconds",
                data={"request_id": request_id, "tool": name, "timeout_seconds": tool_timeout},
            ) from error
        except ValueError as e:
            error = e
            logger.error("Validation error calling tool %s: %s [request_id=%s]", name, e, request_id, exc_info=True)
            from wistx_mcp.tools.lib.error_handler import ErrorHandler
            remediation_info = ErrorHandler.format_error_with_remediation(e, {"tool_name": name})
            raise MCPError(
                code=MCPErrorCode.INVALID_PARAMS,
                message=ErrorHandler.get_user_friendly_error_message(e, name),
                data={
                    "request_id": request_id,
                    "tool": name,
                    "retryable": False,
                    "remediation_steps": remediation_info.get("remediation_steps", []),
                },
            ) from e
        except httpx.HTTPStatusError as e:
            error = e
            status_code = e.response.status_code
            logger.error("HTTP error calling tool %s: %s (status: %s) [request_id=%s]", name, e, status_code, request_id)

            code = MCPErrorCode.INTERNAL_ERROR
            message = f"External service error: {status_code}"
            remediation_steps = []

            if status_code == 401:
                code = MCPErrorCode.INVALID_REQUEST
                message = "Authentication failed with external service"
                remediation_steps = ["Check your API key is valid", "Ensure your subscription is active"]
            elif status_code == 403:
                code = MCPErrorCode.INVALID_REQUEST
                message = "Permission denied by external service"
                remediation_steps = ["Check your account permissions", "Contact support if issue persists"]
            elif status_code == 429:
                code = MCPErrorCode.RATE_LIMIT_EXCEEDED
                message = "Rate limit exceeded by external service"
                remediation_steps = ["Wait a few minutes before retrying", "Consider upgrading your plan for higher limits"]
            elif status_code >= 500:
                message = "External service temporarily unavailable. The WISTX backend is experiencing issues."
                remediation_steps = [
                    "This is a temporary backend issue - please retry in a few minutes",
                    "If the issue persists, check WISTX service status",
                    "Try using a different tool or action if available",
                ]

            raise MCPError(
                code=code,
                message=message,
                data={
                    "request_id": request_id,
                    "tool": name,
                    "status_code": status_code,
                    "retryable": status_code >= 500 or status_code == 429,
                    "remediation_steps": remediation_steps,
                },
            ) from e
        except (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError) as e:
            error = e
            logger.error("Network error calling tool %s: %s [request_id=%s]", name, e, request_id, exc_info=True)
            raise MCPError(
                code=MCPErrorCode.INTERNAL_ERROR,
                message="Unable to connect to WISTX backend service. Please check your network connection and try again.",
                data={
                    "request_id": request_id,
                    "tool": name,
                    "retryable": True,
                    "remediation_steps": [
                        "Check your internet connection",
                        "The WISTX backend may be temporarily unavailable - retry in a few minutes",
                        "If using a VPN, try disconnecting and reconnecting",
                        "Contact support if the issue persists",
                    ],
                },
            ) from e
        except (RuntimeError, ConnectionError) as e:
            error = e
            logger.error("Error calling tool %s: %s [request_id=%s]", name, e, request_id, exc_info=True)
            from wistx_mcp.tools.lib.error_handler import ErrorHandler
            remediation_info = ErrorHandler.format_error_with_remediation(e, {"tool_name": name})
            is_retryable = isinstance(e, ConnectionError) or "temporarily unavailable" in str(e).lower()

            # Provide better message for auth service unavailable
            message = ErrorHandler.get_user_friendly_error_message(e, name)
            if "authentication service temporarily unavailable" in str(e).lower():
                message = "Authentication service is temporarily unavailable. Please retry in a few minutes."
                remediation_info["remediation_steps"] = [
                    "The authentication service is experiencing issues",
                    "Please wait a few minutes and try again",
                    "If the issue persists, contact support",
                ]
                is_retryable = True

            raise MCPError(
                code=MCPErrorCode.INTERNAL_ERROR,
                message=message,
                data={
                    "request_id": request_id,
                    "tool": name,
                    "retryable": is_retryable,
                    "remediation_steps": remediation_info.get("remediation_steps", []),
                },
            ) from e
        except Exception as e:
            error = e
            logger.error("Unexpected error calling tool %s [request_id=%s]", name, request_id, exc_info=True)
            from wistx_mcp.tools.lib.error_handler import ErrorHandler
            remediation_info = ErrorHandler.format_error_with_remediation(e, {"tool_name": name})
            raise MCPError(
                code=MCPErrorCode.INTERNAL_ERROR,
                message=ErrorHandler.get_user_friendly_error_message(e, name),
                data={
                    "request_id": request_id,
                    "tool": name,
                    "retryable": False,
                    "remediation_steps": remediation_info.get("remediation_steps", []),
                },
            ) from e
        finally:
            async with _inflight_lock:
                _inflight_requests.discard(request_id)
            
            duration = time.time() - start_time
            metrics = get_tool_metrics(name)
            metrics.record_call(duration, success=success, error=error)
            logger.debug(
                "Tool %s completed in %.3f seconds (success=%s) [request_id=%s]",
                name,
                duration,
                success,
                request_id,
            )
            
            if auth_ctx and hasattr(auth_ctx, '_context_token') and auth_ctx._context_token:
                from wistx_mcp.tools.lib.auth_context import auth_context as auth_context_var
                try:
                    auth_context_var.reset(auth_ctx._context_token)
                except Exception:
                    pass

    async def _execute_tool_internal(name: str, arguments: dict, auth_ctx: AuthContext) -> list[TextContent]:
        """Internal tool execution logic.

        Args:
            name: Tool name
            arguments: Tool arguments (without api_key)
            auth_ctx: Authentication context

        Returns:
            List of TextContent results
        """
        from wistx_mcp.tools.lib.context_builder import ContextBuilder
        from wistx_mcp.tools.lib.auth_context import set_api_key_context

        tools_requiring_api_key = {
            "wistx_get_compliance_requirements",
            "wistx_research_knowledge_base",
            "wistx_calculate_infrastructure_cost",
            "wistx_index_repository",
            "wistx_index_resource",
            "wistx_manage_resources",
            "wistx_web_search",
            "wistx_search_codebase",
            "wistx_regex_search",
            "wistx_design_architecture",
            "wistx_troubleshoot_issue",
            "wistx_generate_documentation",
            "wistx_manage_infrastructure_lifecycle",
            "wistx_get_existing_infrastructure",
            "wistx_get_devops_infra_code_examples",
            "wistx_search_devops_resources",
            "wistx_list_filesystem",
            "wistx_read_file_with_context",
            "wistx_save_context_with_analysis",
            "wistx_search_contexts_intelligently",
            "wistx_discover_cloud_resources",
            # Unified tools
            "wistx_search_code",
            "wistx_infrastructure",
            "wistx_context",
            "wistx_index",
            "wistx_research",
            "wistx_packages",
        }

        if name in tools_requiring_api_key:
            api_key_value = auth_ctx.api_key if auth_ctx and auth_ctx.api_key else settings.api_key
            set_api_key_context(api_key_value)
        else:
            set_api_key_context(None)

        try:
            tool_args = arguments.copy()
            tools_accepting_api_key_param = {
                "wistx_search_devops_resources",
                "wistx_read_package_file",
                "wistx_index_repository",
                "wistx_index_resource",
                "wistx_manage_resources",
                "wistx_research_knowledge_base",
                "wistx_get_existing_infrastructure",
                "wistx_manage_infrastructure_lifecycle",
                "wistx_search_codebase",
                "wistx_regex_search",
                "wistx_list_filesystem",
                "wistx_read_file_with_context",
                "wistx_save_context_with_analysis",
                "wistx_search_contexts_intelligently",
                "wistx_discover_cloud_resources",
                # Unified tools
                "wistx_search_code",
                "wistx_infrastructure",
                "wistx_context",
                "wistx_index",
                "wistx_research",
                "wistx_packages",
            }
            if name in tools_accepting_api_key_param:
                api_key_value = auth_ctx.api_key if auth_ctx and auth_ctx.api_key else settings.api_key
                if api_key_value:
                    tool_args["api_key"] = api_key_value

            if name == "wistx_get_compliance_requirements":
                logger.info("Calling wistx_get_compliance_requirements tool...")
                try:
                    result = await mcp_tools.get_compliance_requirements(**tool_args)
                    logger.info("Tool wistx_get_compliance_requirements completed successfully")
                    logger.info("Result type received: %s", type(result))
                    logger.info("Result is None: %s", result is None)

                    if result is None:
                        logger.error("get_compliance_requirements returned None - this should never happen")
                        markdown_result = "Error: No response from compliance requirements service."
                        return [TextContent(type="text", text=markdown_result)]
                except Exception as e:
                    logger.error("Exception in get_compliance_requirements: %s", e, exc_info=True)
                    raise

                resource_type = arguments.get("resource_types", [""])[0] if arguments.get("resource_types") else None

                controls = []
                if isinstance(result, dict):
                    if "controls" in result:
                        controls = result["controls"]
                    elif "data" in result and isinstance(result["data"], dict):
                        controls = result["data"].get("controls", [])

                if not controls:
                    result_keys = list(result.keys()) if isinstance(result, dict) else "non-dict result"
                    logger.warning("No controls found in response: %s", result_keys)
                    markdown_result = "No compliance controls found for the specified criteria."
                else:
                    markdown_result = ContextBuilder.format_compliance_as_toon(controls, resource_type)

                if not isinstance(markdown_result, str):
                    logger.error("Markdown result is not a string: %s", type(markdown_result))
                    markdown_result = "Error formatting compliance requirements."

                if not markdown_result.strip():
                    logger.warning("Markdown result is empty")
                    markdown_result = "No compliance controls found for the specified criteria."

                if "report_id" in result:
                    report_id = result["report_id"]
                    markdown_result += "\n\n---\n\n**Report Generated:**\n"
                    markdown_result += f"- Report ID: `{report_id}`\n"
                    if result.get("report_view_url"):
                        markdown_result += f"- View Report: {result['report_view_url']}\n"
                    if result.get("report_download_url"):
                        markdown_result += f"- Download Report: {result['report_download_url']}\n"
                    markdown_result += "\nThe compliance report has been automatically generated and stored. You can view or download it using the links above."

                # Store STRUCTURED data in session context for downstream tools
                # This enables wistx_generate_documentation to access actual compliance controls
                try:
                    structured_data = {
                        "controls": controls,
                        "standards": tool_args.get("standards", []),
                        "resource_types": tool_args.get("resource_types", []),
                        "cloud_provider": tool_args.get("cloud_provider"),
                    }
                    store_tool_result("wistx_get_compliance_requirements", tool_args, structured_data)
                    logger.info("Stored %d compliance controls in session context for downstream tools", len(controls))
                except Exception as e:
                    logger.debug("Failed to store compliance data in session context: %s", e)

                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_research_knowledge_base":
                logger.info("Calling wistx_research_knowledge_base tool...")
                result = await mcp_tools.research_knowledge_base(**tool_args)
                logger.info("Tool wistx_research_knowledge_base completed successfully")
                
                markdown_result = ContextBuilder.format_knowledge_research_results(result)
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_calculate_infrastructure_cost":
                logger.info("Calling wistx_calculate_infrastructure_cost tool...")
                result = await mcp_tools.calculate_infrastructure_cost(**tool_args)
                logger.info("Tool wistx_calculate_infrastructure_cost completed successfully")

                markdown_result = ContextBuilder.format_pricing_as_toon(result)

                # Store STRUCTURED data in session context for downstream tools
                # This enables wistx_generate_documentation to access actual cost data
                try:
                    structured_data = {
                        "cost_breakdown": result.get("cost_breakdown", []),
                        "total_monthly_cost": result.get("total_monthly_cost"),
                        "total_annual_cost": result.get("total_annual_cost"),
                        "optimization_suggestions": result.get("optimization_suggestions", []),
                        "resources": tool_args.get("resources", []),
                    }
                    store_tool_result("wistx_calculate_infrastructure_cost", tool_args, structured_data)
                    logger.info("Stored cost data in session context for downstream tools")
                except Exception as e:
                    logger.debug("Failed to store cost data in session context: %s", e)

                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_index_repository":
                logger.info("Calling wistx_index_repository tool...")
                from wistx_mcp.tools import user_indexing
                result = await user_indexing.index_repository(**tool_args)
                logger.info("Tool wistx_index_repository completed successfully")
                markdown_result = ContextBuilder.format_indexing_results(result, operation="index")
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_index_resource":
                logger.info("Calling wistx_index_resource tool...")
                from wistx_mcp.tools import user_indexing
                result = await user_indexing.index_content(**tool_args)
                logger.info("Tool wistx_index_resource completed successfully")
                markdown_result = ContextBuilder.format_indexing_results(result, operation="index")
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_manage_resources":
                logger.info("Calling wistx_manage_resources tool...")
                from wistx_mcp.tools import user_indexing

                action = tool_args.get("action")
                if not action:
                    raise ValueError("action parameter is required for wistx_manage_resources")

                if action == "list":
                    # List all resources
                    list_args = {
                        "resource_type": tool_args.get("resource_type"),
                        "status": tool_args.get("status_filter"),
                        "api_key": tool_args.get("api_key"),
                        "include_ai_analysis": tool_args.get("include_ai_analysis", True),
                        "deduplicate": tool_args.get("deduplicate", True),
                        "show_duplicates": tool_args.get("show_duplicates", False),
                    }
                    # Remove None values
                    list_args = {k: v for k, v in list_args.items() if v is not None}
                    result = await user_indexing.list_resources(**list_args)
                    logger.info("Tool wistx_manage_resources (list) completed successfully")
                    markdown_result = ContextBuilder.format_resource_management_results(result, action="list")

                elif action == "status":
                    # Check resource status
                    resource_id = tool_args.get("resource_id")
                    if not resource_id:
                        raise ValueError("resource_id is required for 'status' action. Use action='list' first to get resource IDs.")
                    result = await user_indexing.check_resource_status(
                        resource_id=resource_id,
                        api_key=tool_args.get("api_key"),
                    )
                    logger.info("Tool wistx_manage_resources (status) completed successfully")
                    markdown_result = ContextBuilder.format_resource_management_results(result, action="status")

                elif action == "delete":
                    # Delete resource
                    resource_id = tool_args.get("resource_id")
                    identifier = tool_args.get("identifier")
                    resource_type = tool_args.get("resource_type")

                    if resource_id:
                        # Delete by resource_id - need to determine resource_type from the ID or use provided type
                        if not resource_type:
                            resource_type = "repository"  # Default, will be validated by backend
                        result = await user_indexing.delete_resource(
                            resource_type=resource_type,
                            identifier=resource_id,
                            api_key=tool_args.get("api_key"),
                        )
                    elif identifier:
                        if not resource_type:
                            raise ValueError("resource_type is required when using 'identifier' for delete. Specify 'repository', 'documentation', or 'document'.")
                        result = await user_indexing.delete_resource(
                            resource_type=resource_type,
                            identifier=identifier,
                            api_key=tool_args.get("api_key"),
                        )
                    else:
                        raise ValueError("Either 'resource_id' or 'identifier' (with 'resource_type') is required for 'delete' action.")

                    logger.info("Tool wistx_manage_resources (delete) completed successfully")
                    markdown_result = ContextBuilder.format_resource_management_results(result, action="delete")
                else:
                    raise ValueError(f"Invalid action: {action}. Must be 'list', 'status', or 'delete'.")

                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_web_search":
                logger.info("Calling wistx_web_search tool...")
                from wistx_mcp.tools import web_search
                result = await web_search.web_search(**tool_args)
                logger.info("Tool wistx_web_search completed successfully")
                
                markdown_result = ContextBuilder.format_web_search_results(result)
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_search_codebase":
                logger.info("Calling wistx_search_codebase tool...")
                from wistx_mcp.tools import search_codebase
                normalized_args = tool_args.copy()
                if "code_types" in normalized_args and "code_type" not in normalized_args:
                    code_types = normalized_args.pop("code_types")
                    if code_types and isinstance(code_types, list) and len(code_types) > 0:
                        normalized_args["code_type"] = code_types[0]
                result = await search_codebase.search_codebase(**normalized_args)
                logger.info("Tool wistx_search_codebase completed successfully")
                
                markdown_result = ContextBuilder.format_codebase_search_results(result)
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_regex_search":
                logger.info("Calling wistx_regex_search tool...")
                from wistx_mcp.tools import regex_search
                result = await regex_search.regex_search_codebase(**tool_args)
                logger.info("Tool wistx_regex_search completed successfully")
                
                markdown_result = ContextBuilder.format_regex_search_results(result)
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_list_filesystem":
                logger.info("Calling wistx_list_filesystem tool...")
                from wistx_mcp.tools import virtual_filesystem
                result = await virtual_filesystem.wistx_list_filesystem(**tool_args)
                logger.info("Tool wistx_list_filesystem completed successfully")
                
                markdown_result = ContextBuilder.format_filesystem_list_results(result)
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_read_file_with_context":
                logger.info("Calling wistx_read_file_with_context tool...")
                from wistx_mcp.tools import virtual_filesystem
                result = await virtual_filesystem.wistx_read_file_with_context(**tool_args)
                logger.info("Tool wistx_read_file_with_context completed successfully")
                
                markdown_result = ContextBuilder.format_file_read_results(result)
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_save_context_with_analysis":
                logger.info("Calling wistx_save_context_with_analysis tool...")
                from wistx_mcp.tools import intelligent_context
                result = await intelligent_context.wistx_save_context_with_analysis(**tool_args)
                logger.info("Tool wistx_save_context_with_analysis completed successfully")
                
                markdown_result = ContextBuilder.format_context_save_results(result)
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_search_contexts_intelligently":
                logger.info("Calling wistx_search_contexts_intelligently tool...")
                from wistx_mcp.tools import intelligent_context
                result = await intelligent_context.wistx_search_contexts_intelligently(**tool_args)
                logger.info("Tool wistx_search_contexts_intelligently completed successfully")
                
                markdown_result = ContextBuilder.format_context_search_results(result)
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_search_devops_resources":
                logger.info("Calling wistx_search_devops_resources tool...")
                from wistx_mcp.tools import package_search
                result = await package_search.search_devops_resources(**tool_args)
                logger.info("Tool wistx_search_devops_resources completed successfully")
                
                markdown_result = ContextBuilder.format_devops_resource_search_results(result)
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_read_package_file":
                logger.info("Calling wistx_read_package_file tool...")
                from wistx_mcp.tools import package_search
                result = await package_search.read_package_file_mcp(**tool_args)
                logger.info("Tool wistx_read_package_file completed successfully")
                
                markdown_result = ContextBuilder.format_package_read_file_results(result)
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_design_architecture":
                logger.info("Calling wistx_design_architecture tool...")
                from wistx_mcp.tools import design_architecture
                result = await design_architecture.design_architecture(**tool_args)
                logger.info("Tool wistx_design_architecture completed successfully")
                
                markdown_result = ContextBuilder.format_architecture_results(result)
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_troubleshoot_issue":
                logger.info("Calling wistx_troubleshoot_issue tool...")
                from wistx_mcp.tools import troubleshoot_issue
                result = await troubleshoot_issue.troubleshoot_issue(**tool_args)
                logger.info("Tool wistx_troubleshoot_issue completed successfully")
                
                markdown_result = ContextBuilder.format_troubleshooting_results(result)
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_generate_documentation":
                logger.info("Calling wistx_generate_documentation tool...")
                from wistx_mcp.tools import generate_documentation
                result = await generate_documentation.generate_documentation(**tool_args)
                logger.info("Tool wistx_generate_documentation completed successfully")
                
                markdown_result = ContextBuilder.format_documentation_results(result)
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_manage_infrastructure_lifecycle":
                logger.info("Calling wistx_manage_infrastructure_lifecycle tool...")
                from wistx_mcp.tools import manage_infrastructure_lifecycle
                result = await manage_infrastructure_lifecycle.manage_infrastructure_lifecycle(**tool_args)
                logger.info("Tool wistx_manage_infrastructure_lifecycle completed successfully")
                
                markdown_result = ContextBuilder.format_infrastructure_lifecycle_results(result)
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_get_existing_infrastructure":
                logger.info("Calling wistx_get_existing_infrastructure tool...")
                from wistx_mcp.tools import infrastructure_context
                result = await infrastructure_context.get_existing_infrastructure(**tool_args)
                logger.info("Tool wistx_get_existing_infrastructure completed successfully")
                
                markdown_result = _format_existing_infrastructure_result(result)
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_get_devops_infra_code_examples":
                logger.info("Calling wistx_get_devops_infra_code_examples tool...")
                from wistx_mcp.tools import code_examples
                result = await code_examples.get_code_examples(**tool_args)
                logger.info("Tool wistx_get_devops_infra_code_examples completed successfully")
                
                markdown_result = ContextBuilder.format_code_examples_as_toon(
                    result.get("examples", []),
                    suggestions=result.get("suggestions"),
                    message=result.get("message"),
                )
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_discover_cloud_resources":
                logger.info("Calling wistx_discover_cloud_resources tool...")
                from wistx_mcp.tools import discover_cloud_resources
                result = await discover_cloud_resources.discover_cloud_resources(**tool_args)
                logger.info("Tool wistx_discover_cloud_resources completed successfully")

                markdown_result = ContextBuilder.format_cloud_discovery_results(result)
                return [TextContent(type="text", text=markdown_result)]

            # === UNIFIED TOOLS HANDLERS ===
            elif name == "wistx_search_code":
                logger.info("Calling wistx_search_code unified tool...")
                from wistx_mcp.tools import unified_code_search
                result = await unified_code_search.wistx_search_code(**tool_args)
                logger.info("Tool wistx_search_code completed successfully")
                search_mode = tool_args.get("search_mode", "semantic")
                if search_mode == "semantic":
                    markdown_result = ContextBuilder.format_search_results(result)
                elif search_mode == "regex":
                    markdown_result = ContextBuilder.format_regex_search_results(result)
                else:  # examples
                    markdown_result = ContextBuilder.format_code_examples_as_toon(
                        result, show_full_files=True, max_code_length=15000
                    )
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_infrastructure":
                logger.info("Calling wistx_infrastructure unified tool...")
                from wistx_mcp.tools import unified_infrastructure
                result = await unified_infrastructure.wistx_infrastructure(**tool_args)
                logger.info("Tool wistx_infrastructure completed successfully")
                action = tool_args.get("action", "")
                if action in ["init_project", "design_project", "review_project", "optimize_project"]:
                    markdown_result = ContextBuilder.format_architecture_results(result)
                elif action in ["get_existing"]:
                    markdown_result = _format_existing_infrastructure_result(result)
                elif action == "discover":
                    markdown_result = ContextBuilder.format_cloud_discovery_results(result)
                else:
                    markdown_result = ContextBuilder.format_infrastructure_lifecycle_results(result)

                # Store STRUCTURED data in session context for downstream tools
                # This enables wistx_generate_documentation to access actual infrastructure data
                try:
                    structured_data = {
                        "scaffolding": result.get("scaffolding"),
                        "modules": result.get("modules", []),
                        "components": result.get("components", []),
                        "architecture_context": result.get("architecture_context", {}),
                        "compliance_context": result.get("compliance_context", {}),
                        "security_context": result.get("security_context", {}),
                        "cloud_provider": tool_args.get("cloud_provider"),
                        "project_type": tool_args.get("project_type"),
                        "resource_types": result.get("resource_types", []),
                        "action": action,
                    }
                    store_tool_result("wistx_infrastructure", tool_args, structured_data)
                    logger.info("Stored infrastructure data in session context for downstream tools")
                except Exception as e:
                    logger.debug("Failed to store infrastructure data in session context: %s", e)

                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_context":
                logger.info("Calling wistx_context unified tool...")
                from wistx_mcp.tools import unified_context
                result = await unified_context.wistx_context(**tool_args)
                logger.info("Tool wistx_context completed successfully")
                action = tool_args.get("action", "")
                if action == "list_files":
                    markdown_result = ContextBuilder.format_filesystem_list_results(result)
                elif action == "read_file":
                    markdown_result = ContextBuilder.format_file_read_results(result)
                elif action == "save":
                    markdown_result = ContextBuilder.format_context_save_results(result)
                elif action == "search":
                    markdown_result = ContextBuilder.format_context_search_results(result)
                else:  # get, list_saved
                    markdown_result = ContextBuilder.format_context_results(result)
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_index":
                logger.info("Calling wistx_index unified tool...")
                from wistx_mcp.tools import unified_indexing
                result = await unified_indexing.wistx_index(**tool_args)
                logger.info("Tool wistx_index completed successfully")
                action = tool_args.get("action", "")
                if action in ["repository", "content"]:
                    markdown_result = ContextBuilder.format_indexing_results(result, operation="index")
                else:  # list, status, delete
                    markdown_result = ContextBuilder.format_resource_management_results(result, action=action)
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_research":
                logger.info("Calling wistx_research unified tool...")
                from wistx_mcp.tools import unified_research
                result = await unified_research.wistx_research(**tool_args)
                logger.info("Tool wistx_research completed successfully")
                source = tool_args.get("source", "knowledge_base")
                if source == "knowledge_base":
                    markdown_result = ContextBuilder.format_knowledge_research_results(result)
                elif source in ["web", "security"]:
                    markdown_result = ContextBuilder.format_web_search_results(result)
                else:  # all
                    markdown_result = ContextBuilder.format_combined_research_results(result)
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_packages":
                logger.info("Calling wistx_packages unified tool...")
                from wistx_mcp.tools import unified_packages
                result = await unified_packages.wistx_packages(**tool_args)
                logger.info("Tool wistx_packages completed successfully")
                action = tool_args.get("action", "search")
                if action == "search":
                    markdown_result = ContextBuilder.format_devops_resource_search_results(result)
                else:  # read_file
                    markdown_result = ContextBuilder.format_package_read_file_results(result)
                return [TextContent(type="text", text=markdown_result)]

            elif name == "wistx_compliance_automation":
                logger.info("Calling wistx_compliance_automation unified tool...")
                from wistx_mcp.tools import unified_compliance_automation
                result = await unified_compliance_automation.wistx_compliance_automation(**tool_args)
                logger.info("Tool wistx_compliance_automation completed successfully")

                # Format based on action
                action = tool_args.get("action", "")
                if result.get("success"):
                    if action in ["generate_cicd_gate", "generate_pre_commit"]:
                        # Format CI/CD gate results
                        files = result.get("files", {})
                        markdown_lines = [
                            "# 🔧 CI/CD Compliance Gate Generated",
                            "",
                            f"**Action**: {action}",
                            f"**Platform**: {result.get('platform', 'all')}",
                            "",
                            "## Generated Files",
                            "",
                        ]
                        for filename, content in files.items():
                            markdown_lines.append(f"### `{filename}`")
                            markdown_lines.append("```yaml")
                            markdown_lines.append(content[:2000] + ("..." if len(content) > 2000 else ""))
                            markdown_lines.append("```")
                            markdown_lines.append("")
                        if result.get("instructions"):
                            markdown_lines.append("## Setup Instructions")
                            markdown_lines.append(result["instructions"])
                        markdown_result = "\n".join(markdown_lines)
                    elif action in ["calculate_sample", "select_sample"]:
                        # Format sampling results
                        markdown_lines = [
                            "# 📊 Audit Sampling Results",
                            "",
                            f"**Method**: {result.get('method', 'N/A')}",
                            f"**Sample Size**: {result.get('sample_size', 'N/A')}",
                            f"**Methodology**: {result.get('methodology', 'N/A')}",
                            "",
                        ]
                        if result.get("sampling_interval"):
                            markdown_lines.append(f"**Sampling Interval**: ${result['sampling_interval']:,.2f}")
                        if result.get("parameters"):
                            markdown_lines.append("")
                            markdown_lines.append("## Parameters")
                            for k, v in result["parameters"].items():
                                markdown_lines.append(f"- **{k}**: {v}")
                        if result.get("selected_items"):
                            markdown_lines.append("")
                            markdown_lines.append("## Selected Sample Items")
                            markdown_lines.append("")
                            markdown_lines.append("| ID | Value | Selection Reason |")
                            markdown_lines.append("|-----|-------|------------------|")
                            for item in result["selected_items"][:20]:  # Limit display
                                markdown_lines.append(f"| {item['id']} | ${item['value']:,.2f} | {item['selection_reason']} |")
                            if len(result["selected_items"]) > 20:
                                markdown_lines.append(f"| ... | ... | ({len(result['selected_items']) - 20} more items) |")
                        markdown_result = "\n".join(markdown_lines)
                    elif action in ["generate_workpaper", "generate_workpaper_package"]:
                        # Format workpaper results
                        markdown_lines = [
                            "# 📝 Audit Workpaper Generated",
                            "",
                            f"**Action**: {action}",
                            f"**Methodology**: {result.get('methodology', 'N/A')}",
                            "",
                        ]
                        if action == "generate_workpaper":
                            markdown_lines.append(f"**Workpaper ID**: {result.get('workpaper_id', 'N/A')}")
                            markdown_lines.append(f"**Type**: {result.get('workpaper_type', 'N/A')}")
                            markdown_lines.append("")
                            markdown_lines.append("## Content")
                            markdown_lines.append("")
                            content = result.get("content", "")
                            if isinstance(content, str):
                                markdown_lines.append(content)
                            else:
                                markdown_lines.append(f"```json\n{content}\n```")
                        else:  # generate_workpaper_package
                            markdown_lines.append(f"**Engagement**: {result.get('engagement', 'N/A')}")
                            markdown_lines.append(f"**Workpaper Count**: {result.get('workpaper_count', 0)}")
                            markdown_lines.append("")
                            markdown_lines.append("## Workpapers Generated")
                            markdown_lines.append("")
                            for wp in result.get("workpapers", []):
                                markdown_lines.append(f"- **{wp['id']}**: {wp['title']} ({wp['type']})")
                        markdown_result = "\n".join(markdown_lines)
                    else:
                        markdown_result = f"# Compliance Automation Result\n\n```json\n{result}\n```"
                else:
                    markdown_result = f"# ❌ Error\n\n{result.get('error', 'Unknown error')}"

                return [TextContent(type="text", text=markdown_result)]

            else:
                logger.warning("Unknown tool requested: %s", name)
                raise ValueError(f"Unknown tool: {name}")
        finally:
            set_api_key_context(None)

    async def _wait_for_inflight_requests() -> None:
        """Wait for in-flight requests to complete.

        This checks if there are any active tool executions and waits for them.
        """
        GRACEFUL_SHUTDOWN_TIMEOUT = 30.0
        check_interval = 0.5
        waited = 0.0

        while waited < GRACEFUL_SHUTDOWN_TIMEOUT:
            async with _inflight_lock:
                if not _inflight_requests:
                    logger.info("All in-flight requests completed")
                    return

            await asyncio.sleep(check_interval)
            waited += check_interval

        async with _inflight_lock:
            if _inflight_requests:
                logger.warning(
                    "Shutdown timeout: %d requests still in flight",
                    len(_inflight_requests),
                )

    try:
        logger.info("Starting stdio server...")
        logger.info("Server will now wait for client connection via stdio...")
        logger.info("Checking stdin/stdout connectivity...")
        logger.info("stdin: %s, stdout: %s, stderr: %s", sys.stdin, sys.stdout, sys.stderr)
        logger.info("stdin.isatty(): %s, stdout.isatty(): %s", sys.stdin.isatty(), sys.stdout.isatty())

        logger.info("Attempting to create stdio_server context manager...")
        try:
            stdio_ctx = stdio_server()
            logger.info("stdio_server context manager created successfully")
        except Exception as e:
            logger.error("Failed to create stdio_server context manager: %s", e, exc_info=True)
            raise

        try:
            async with stdio_ctx as (read_stream, write_stream):
                # Set connection ID for session isolation
                # Each stdio connection is a separate session (chat window)
                connection_id = str(uuid.uuid4())
                set_connection_id(connection_id)
                logger.info("Session context initialized with connection ID: %s", connection_id[:8] + "...")

                logger.info("stdio server started, running MCP server...")
                logger.info("Server info: name=%s, version=%s", settings.server_name, settings.server_version)
                logger.info("on_initialize handler registered: %s", on_initialize_registered)

                init_options = app.create_initialization_options()
                logger.info("Initialization options created: server_name=%s, server_version=%s", init_options.server_name, init_options.server_version)
                logger.info("Server capabilities: tools=%s, resources=%s",
                           init_options.capabilities.tools is not None if init_options.capabilities.tools else None,
                           init_options.capabilities.resources is not None if init_options.capabilities.resources else None)

                if not on_initialize_registered:
                    logger.warning("on_initialize handler not registered - SDK will handle initialization automatically")
                    logger.info("Server name and version are set in InitializationOptions and should be used by SDK")
                    logger.info("Server.name=%s", app.name)
                    logger.info("InitializationOptions.server_name=%s, InitializationOptions.server_version=%s",
                               init_options.server_name, init_options.server_version)
                    logger.warning("If you see 'No server info found' errors, this may indicate:")
                    logger.warning("  1. SDK bug in automatic initialization handling")
                    logger.warning("  2. Race condition where client calls ListOfferings before initialization")
                    logger.warning("  3. SDK version compatibility issue")

                logger.info("Starting MCP server run() - server is now ready to accept connections...")
                logger.info("Server will respond to initialize requests with serverInfo: name=%s, version=%s",
                           init_options.server_name, init_options.server_version)
                logger.info("MCP SDK version: 1.21.0 (should handle initialization automatically)")
                logger.info("NOTE: If you see 'No server info found' errors, Cursor may be calling ListOfferings")
                logger.info("before initialization completes. This is a known race condition in Cursor.")
                logger.info("The SDK should handle this gracefully, but if errors persist, try restarting Cursor.")

                # Run the server - it will exit when client disconnects or on fatal errors
                # Note: Unsupported notifications may cause app.run() to exit, but the context manager
                # will handle cleanup. The server should be restarted by Claude Desktop if needed.
                await app.run(read_stream, write_stream, init_options)
                logger.info("MCP server stopped (app.run() completed)")
        except BaseExceptionGroup as eg:
            def _check_exception_recursive(exc: Exception, depth: int = 0) -> tuple[bool, bool]:
                """Recursively check exception and nested exception groups.
                
                Args:
                    exc: Exception to check
                    depth: Current recursion depth (max 10)
                    
                Returns:
                    Tuple of (is_broken_resource_error, is_validation_error)
                """
                if depth > 10:
                    return False, False
                    
                is_broken = False
                is_validation = False
                
                error_type = type(exc).__name__
                error_msg = str(exc)
                error_repr = repr(exc)

                if "BrokenResourceError" in error_type or "BrokenPipeError" in error_type:
                    is_broken = True
                elif "ValidationError" in error_type and "notifications/cancelled" in error_msg:
                    is_validation = True
                elif "notifications/cancelled" in error_msg and "ValidationError" in error_type:
                    is_validation = True
                elif "notifications/cancelled" in error_repr and "ValidationError" in error_repr:
                    is_validation = True

                if isinstance(exc, BaseExceptionGroup):
                    try:
                        exceptions_attr = getattr(exc, "exceptions", ())
                        exceptions_list = list(exceptions_attr) if exceptions_attr else []
                        for nested_exc in exceptions_list:
                            nested_broken, nested_validation = _check_exception_recursive(nested_exc, depth + 1)
                            is_broken = is_broken or nested_broken
                            is_validation = is_validation or nested_validation
                            if is_broken and is_validation:
                                break
                    except (AttributeError, TypeError):
                        pass
                
                return is_broken, is_validation
            
            error_str = str(eg)
            error_repr = repr(eg)
            is_broken_resource_error, is_validation_error = _check_exception_recursive(eg)

            if not is_broken_resource_error and ("BrokenResourceError" in error_str or "BrokenPipeError" in error_str):
                is_broken_resource_error = True

            if not is_validation_error:
                if ("notifications/cancelled" in error_str and "ValidationError" in error_str) or \
                   ("notifications/cancelled" in error_repr and "ValidationError" in error_repr):
                    is_validation_error = True

            if is_broken_resource_error:
                logger.warning(
                    "Communication channel broken during context manager exit "
                    "(likely due to client disconnect after SDK notification handling). "
                    "This is expected behavior when the client cancels requests. "
                    "The server will shut down gracefully."
                )
                logger.info("Shutting down due to broken communication channel during cleanup")
            elif is_validation_error:
                logger.warning(
                    "MCP SDK received unsupported 'notifications/cancelled' notification "
                    "(likely from Claude Desktop canceling a timed-out request). "
                    "This is a known SDK limitation in v1.21.0. "
                    "The exception was caught during context manager exit. "
                    "Claude Desktop should automatically restart the server."
                )
                logger.info("Server will be restarted by Claude Desktop if needed")
            else:
                logger.error("Error in stdio context: %s", eg, exc_info=True)
                raise
        except (RuntimeError, ConnectionError, ValueError) as e:
            logger.error("Error starting MCP server: %s", e, exc_info=True)
            raise
        except Exception as e:
            error_type = type(e).__name__
            if "BrokenResourceError" in error_type or "BrokenPipeError" in error_type:
                logger.warning(
                    "Communication channel broken (likely due to client disconnect). "
                    "The server will shut down gracefully."
                )
                logger.info("Shutting down due to broken communication channel")
            else:
                logger.error("Unexpected error starting MCP server: %s", e, exc_info=True)
                raise RuntimeError(f"Failed to start MCP server: {e}") from e
    finally:
        logger.info("Cleaning up MCP server resources...")
        try:
            if rate_limiter:
                await rate_limiter.stop()
            if deduplicator:
                await deduplicator.stop()
            if concurrent_limiter:
                await concurrent_limiter.stop()
            logger.info("Background tasks stopped")
        except Exception as e:
            logger.warning("Error stopping background tasks: %s", e)

        try:
            await resource_manager.cleanup_all()
        except Exception as e:
            logger.warning("Error during resource cleanup: %s", e)


def cli() -> None:
    """CLI entry point for package installation."""
    max_restarts = 10
    restart_delay = 2.0
    restart_count = 0
    
    while restart_count < max_restarts:
        try:
            asyncio.run(main())
            logger.info("MCP server exited normally")
            return
        except SystemExit as e:
            if e.code != 0:
                logger.warning("SystemExit caught (likely from api.config initialization failure), continuing anyway")
                try:
                    asyncio.run(main())
                    return
                except Exception as retry_e:
                    logger.error("Failed to start MCP server after SystemExit recovery: %s", retry_e, exc_info=True)
                    restart_count += 1
                    if restart_count >= max_restarts:
                        logger.error("Max restart attempts reached, giving up")
                        return
                    logger.info("Restarting server in %.1f seconds (attempt %d/%d)...", restart_delay, restart_count, max_restarts)
                    time.sleep(restart_delay)
                    continue
            else:
                return
        except KeyboardInterrupt:
            logger.info("Shutting down MCP server (user interrupt)")
            return
        except (RuntimeError, ConnectionError, ValueError, AttributeError) as e:
            error_str = str(e).lower()
            is_disconnect = (
                "broken" in error_str or
                "disconnect" in error_str or
                "communication channel" in error_str or
                "notifications/cancelled" in error_str
            )
            
            if is_disconnect:
                restart_count += 1
                if restart_count >= max_restarts:
                    logger.error("Max restart attempts reached after disconnect, giving up")
                    return
                logger.warning(
                    "Server disconnected (likely due to unsupported notification). "
                    "Restarting in %.1f seconds (attempt %d/%d)...",
                    restart_delay,
                    restart_count,
                    max_restarts,
                )
                time.sleep(restart_delay)
                continue
            else:
                logger.error("Failed to start MCP server: %s", e, exc_info=True)
                return
        except Exception as e:
            error_str = str(e).lower()
            error_type = type(e).__name__
            is_disconnect = (
                "broken" in error_str or
                "disconnect" in error_str or
                "communication channel" in error_str or
                "notifications/cancelled" in error_str or
                "BrokenResourceError" in error_type or
                "BrokenPipeError" in error_type
            )
            
            if is_disconnect:
                restart_count += 1
                if restart_count >= max_restarts:
                    logger.error("Max restart attempts reached after disconnect, giving up")
                    return
                logger.warning(
                    "Server disconnected. Restarting in %.1f seconds (attempt %d/%d)...",
                    restart_delay,
                    restart_count,
                    max_restarts,
                )
                time.sleep(restart_delay)
                continue
            else:
                logger.error("Unexpected error in cli: %s", e, exc_info=True)
                return
        except BaseException as e:
            logger.critical("Critical error (possibly segfault-related): %s", e, exc_info=True)
            return
    
    logger.error("Max restart attempts (%d) reached, exiting", max_restarts)


if __name__ == "__main__":
    cli()

