"""MCP HTTP service for handling MCP protocol over HTTP."""

import logging
import uuid
from typing import Any

from wistx_mcp.tools.lib.auth_context import AuthContext, set_auth_context
from wistx_mcp.tools.lib.request_context import set_request_context
from wistx_mcp.tools.lib.session_context import set_current_session_id

logger = logging.getLogger(__name__)


class MCPHTTPService:
    """Service for handling MCP protocol over HTTP."""

    async def handle_request(
        self,
        mcp_request: dict[str, Any],
        user_info: dict[str, Any],
    ) -> dict[str, Any]:
        """Handle MCP protocol request.

        Args:
            mcp_request: MCP protocol request (JSON-RPC format)
            user_info: User information from authentication (contains api_key, user_id, etc.)

        Returns:
            MCP protocol response (JSON-RPC format)
        """
        method = mcp_request.get("method")
        params = mcp_request.get("params", {})
        request_id = mcp_request.get("id")

        request_id_str = str(request_id) if request_id else str(uuid.uuid4())

        set_request_context({
            "request_id": request_id_str,
            "user_id": user_info.get("user_id"),
            "organization_id": user_info.get("organization_id"),
        })

        api_key = user_info.get("api_key")
        if not api_key:
            api_key = user_info.get("token")

        auth_ctx = AuthContext(api_key=api_key, request_id=request_id_str)
        set_auth_context(auth_ctx)

        session_id = params.get("_meta", {}).get("sessionId")
        if session_id:
            set_current_session_id(session_id)

        try:
            if method == "initialize":
                return await self._handle_initialize(params, request_id)
            elif method == "tools/list":
                return await self._handle_tools_list(params, request_id)
            elif method == "tools/call":
                return await self._handle_tools_call(params, request_id, auth_ctx)
            elif method == "resources/list":
                return await self._handle_resources_list(params, request_id)
            elif method == "resources/read":
                return await self._handle_resources_read(params, request_id)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}",
                    },
                }
        except Exception as e:
            logger.error("Error handling MCP request: %s", e, exc_info=True)
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": "Internal error",
                    "data": str(e),
                },
            }

    async def _handle_initialize(
        self,
        params: dict[str, Any],
        request_id: Any,
    ) -> dict[str, Any]:
        """Handle initialize request."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "resources": {},
                },
                "serverInfo": {
                    "name": "wistx-mcp",
                    "version": "1.0.65",
                },
            },
        }

    async def _handle_tools_list(
        self,
        params: dict[str, Any],
        request_id: Any,
    ) -> dict[str, Any]:
        """Handle tools/list request."""
        try:
            from wistx_mcp.tools.lib.distributed_tool_cache import DistributedToolCache
            from api.database.redis_client import get_redis_manager

            redis_manager = await get_redis_manager()
            redis_client = None
            if redis_manager:
                redis_client = await redis_manager.get_client()

            cache = DistributedToolCache(redis_client=redis_client, ttl=3600)
            cached_definitions = cache.get_tool_definitions()

            if cached_definitions:
                tool_schemas = [
                    {
                        "name": tool.get("name", ""),
                        "description": tool.get("description", ""),
                        "inputSchema": tool.get("inputSchema", {}),
                    }
                    for tool in cached_definitions
                ]
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": tool_schemas,
                    },
                }

            logger.warning("Tool definitions not in cache, returning minimal list")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": "wistx_get_compliance_requirements",
                            "description": "Get compliance requirements for infrastructure resources",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "resource_types": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "List of resource types",
                                    },
                                },
                                "required": ["resource_types"],
                            },
                        },
                    ],
                },
            }
        except Exception as e:
            logger.error("Error listing tools: %s", e, exc_info=True)
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": "Internal error",
                    "data": str(e),
                },
            }

    async def _handle_tools_call(
        self,
        params: dict[str, Any],
        request_id: Any,
        auth_ctx: AuthContext,
    ) -> dict[str, Any]:
        """Handle tools/call request."""
        try:
            tool_name = params.get("name")
            arguments = params.get("arguments", {})

            if not tool_name:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32602,
                        "message": "Tool name is required",
                    },
                }

            from wistx_mcp.tools.lib.context_builder import ContextBuilder
            from wistx_mcp.tools.lib.api_client import set_api_key_context
            from mcp.types import TextContent

            tool_func = None
            tool_func_name = tool_name.replace("wistx_", "")

            unified_tools = {
                "search_code": "unified_code_search",
                "infrastructure": "unified_infrastructure",
                "context": "unified_context",
                "index": "unified_indexing",
                "research": "unified_research",
                "packages": "unified_packages",
                "compliance_automation": "unified_compliance_automation",
            }

            if tool_name in unified_tools:
                module_name = unified_tools[tool_name]
                try:
                    module = __import__(f"wistx_mcp.tools.{module_name}", fromlist=[tool_name])
                    tool_func = getattr(module, tool_name)
                except (ImportError, AttributeError) as e:
                    logger.warning("Failed to import unified tool %s: %s", tool_name, e)
            else:
                from wistx_mcp.tools import mcp_tools
                if hasattr(mcp_tools, tool_func_name):
                    tool_func = getattr(mcp_tools, tool_func_name)
                else:
                    from wistx_mcp.tools import (
                        user_indexing,
                        web_search,
                        search_codebase,
                        regex_search,
                        package_search,
                        design_architecture,
                        troubleshoot_issue,
                        generate_documentation,
                        manage_integration,
                        manage_infrastructure,
                    )

                    tool_modules = [
                        mcp_tools,
                        user_indexing,
                        web_search,
                        search_codebase,
                        regex_search,
                        package_search,
                        design_architecture,
                        troubleshoot_issue,
                        generate_documentation,
                        manage_integration,
                        manage_infrastructure,
                    ]

                    for module in tool_modules:
                        if hasattr(module, tool_func_name):
                            tool_func = getattr(module, tool_func_name)
                            break
                        if hasattr(module, tool_name):
                            tool_func = getattr(module, tool_name)
                            break

            if not tool_func:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Tool not found: {tool_name}",
                    },
                }

            api_key = auth_ctx.api_key if auth_ctx and auth_ctx.api_key else None
            if api_key:
                set_api_key_context(api_key)
                if "api_key" not in arguments:
                    arguments["api_key"] = api_key

            try:
                result = await tool_func(**arguments)
                
                from wistx_mcp.tools.lib.context_builder import ContextBuilder
                
                if isinstance(result, dict):
                    try:
                        text_content = ContextBuilder.format_for_llm(result)
                    except Exception:
                        text_content = str(result)
                elif isinstance(result, str):
                    text_content = result
                else:
                    text_content = str(result)

                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": text_content,
                            }
                        ],
                    },
                }
            except Exception as tool_error:
                logger.error("Tool execution error: %s", tool_error, exc_info=True)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32603,
                        "message": "Tool execution failed",
                        "data": str(tool_error),
                    },
                }
        except Exception as e:
            logger.error("Error calling tool: %s", e, exc_info=True)
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": "Internal error",
                    "data": str(e),
                },
            }

    async def _handle_resources_list(
        self,
        params: dict[str, Any],
        request_id: Any,
    ) -> dict[str, Any]:
        """Handle resources/list request."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "resources": [],
            },
        }

    async def _handle_resources_read(
        self,
        params: dict[str, Any],
        request_id: Any,
    ) -> dict[str, Any]:
        """Handle resources/read request."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32601,
                "message": "Resource not found",
            },
        }

