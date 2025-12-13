"""Session context management for cross-tool context sharing.

This module provides session-scoped context storage that enables tools to automatically
share context with downstream tools. Each chat/conversation gets its own isolated context.

Session Isolation Architecture:
------------------------------
1. Each MCP connection typically represents one chat window
2. Session ID is derived from: MCP request meta > connection ID > generated UUID
3. Contexts are isolated per session - no cross-contamination between chats
4. TTL-based cleanup prevents memory leaks from abandoned sessions
"""

import logging
import uuid
from contextvars import ContextVar
from typing import Any

from wistx_mcp.tools.lib.conversation_context import (
    ConversationContext,
    get_conversation_context_manager,
)

logger = logging.getLogger(__name__)

# Session ID context variable - set at the start of each request
_session_id_var: ContextVar[str | None] = ContextVar("session_id", default=None)

# Connection ID for the current MCP connection (set during server initialization)
_connection_id_var: ContextVar[str | None] = ContextVar("connection_id", default=None)


def set_connection_id(connection_id: str) -> None:
    """Set the connection ID for the current MCP connection.
    
    This should be called once when an MCP connection is established.
    Each stdio/SSE connection gets a unique ID.
    
    Args:
        connection_id: Unique identifier for this MCP connection
    """
    _connection_id_var.set(connection_id)
    logger.debug("Connection ID set: %s", connection_id[:8] + "...")


def get_connection_id() -> str | None:
    """Get the current MCP connection ID."""
    return _connection_id_var.get()


def extract_session_id(arguments: dict[str, Any] | None = None, meta: dict[str, Any] | None = None) -> str:
    """Extract or generate a session ID for the current request.
    
    Priority order:
    1. Explicit session_id in arguments (for testing/advanced use)
    2. _meta.sessionId from MCP request (if client provides it)
    3. Connection ID (each MCP connection = one session)
    4. Generated UUID (fallback)
    
    Args:
        arguments: Tool arguments dict (may contain session_id)
        meta: MCP request metadata (may contain sessionId)
        
    Returns:
        Session ID string
    """
    # Priority 1: Explicit session_id in arguments
    if arguments and "session_id" in arguments:
        session_id = arguments["session_id"]
        if session_id and isinstance(session_id, str):
            return session_id
    
    # Priority 2: MCP request metadata
    if meta:
        mcp_session_id = meta.get("sessionId") or meta.get("session_id")
        if mcp_session_id and isinstance(mcp_session_id, str):
            return mcp_session_id
    
    # Priority 3: Connection ID (most common case)
    connection_id = get_connection_id()
    if connection_id:
        return connection_id
    
    # Priority 4: Generate new UUID (fallback)
    new_session_id = str(uuid.uuid4())
    logger.debug("Generated new session ID: %s", new_session_id[:8] + "...")
    return new_session_id


def set_current_session_id(session_id: str) -> None:
    """Set the session ID for the current request context.
    
    Args:
        session_id: Session ID to set
    """
    _session_id_var.set(session_id)


def get_current_session_id() -> str | None:
    """Get the session ID for the current request."""
    return _session_id_var.get()


def get_session_context(session_id: str | None = None, user_id: str | None = None) -> ConversationContext:
    """Get or create the session context for storing tool results.
    
    Args:
        session_id: Optional session ID (uses current if not provided)
        user_id: Optional user ID for the session
        
    Returns:
        ConversationContext instance for this session
    """
    if session_id is None:
        session_id = get_current_session_id()
    
    if session_id is None:
        session_id = str(uuid.uuid4())
        logger.warning("No session ID available, generating new one: %s", session_id[:8] + "...")
    
    manager = get_conversation_context_manager()
    return manager.get_or_create_context(session_id, user_id)


def store_tool_result(tool_name: str, arguments: dict[str, Any], result: Any, session_id: str | None = None) -> None:
    """Store a tool result in the session context.
    
    Args:
        tool_name: Name of the tool that produced the result
        arguments: Arguments passed to the tool
        result: The tool's result (will be stored for downstream tools)
        session_id: Optional session ID (uses current if not provided)
    """
    context = get_session_context(session_id)
    context.add_tool_call(tool_name, arguments, result)
    logger.debug("Stored result for tool '%s' in session %s", tool_name, context.session_id[:8] + "...")


def get_previous_tool_result(tool_name: str, session_id: str | None = None) -> Any | None:
    """Get the result of a previously called tool in this session.
    
    Args:
        tool_name: Name of the tool whose result to retrieve
        session_id: Optional session ID (uses current if not provided)
        
    Returns:
        The tool's last result, or None if not found
    """
    context = get_session_context(session_id)
    return context.get_last_tool_result(tool_name)


def get_all_previous_results(session_id: str | None = None) -> dict[str, Any]:
    """Get all tool results from this session.

    Args:
        session_id: Optional session ID (uses current if not provided)

    Returns:
        Dict mapping tool names to their last results
    """
    context = get_session_context(session_id)
    return dict(context.tool_results)


# =============================================================================
# CENTRALIZED AUTO-ENRICHMENT MIDDLEWARE
# =============================================================================

# Parameters that can be auto-enriched from session context
# Simple parameters (strings, lists of strings, etc.)
ENRICHABLE_PARAMS = {
    "cloud_provider": ["wistx_infrastructure", "wistx_get_compliance_requirements", "wistx_design_architecture"],
    "resource_types": ["wistx_infrastructure", "wistx_get_compliance_requirements", "wistx_design_architecture"],
    "compliance_standards": ["wistx_get_compliance_requirements"],
    "project_type": ["wistx_infrastructure", "wistx_design_architecture"],
    "infrastructure_code": ["wistx_infrastructure"],  # From scaffolding
    "architecture_type": ["wistx_infrastructure", "wistx_design_architecture"],
    # Rich data parameters - actual structured data from upstream tools
    "compliance_controls": ["wistx_get_compliance_requirements"],  # Actual compliance control objects
    "infrastructure_modules": ["wistx_infrastructure"],  # Actual infrastructure module data
    "cost_data": ["wistx_calculate_infrastructure_cost"],  # Actual cost breakdown data
    "architecture_context": ["wistx_infrastructure"],  # Architecture context from design
    "security_context": ["wistx_infrastructure"],  # Security context from design
}

# Tools that should receive auto-enrichment
TOOLS_ACCEPTING_ENRICHMENT = {
    # Documentation tools - now includes rich data parameters
    # NOTE: generate_documentation does NOT accept cloud_provider or project_type
    "wistx_generate_documentation": [
        "resource_types", "compliance_standards", "infrastructure_code",
        # Rich data for generating specific (non-generic) documentation
        "compliance_controls", "infrastructure_modules", "cost_data", "architecture_context", "security_context",
    ],
    # Infrastructure tools
    "wistx_infrastructure": ["cloud_provider", "compliance_standards", "project_type"],
    "wistx_design_architecture": ["cloud_provider", "compliance_standards", "project_type"],
    # Cost calculation - NOTE: calculate_infrastructure_cost only accepts 'resources' and 'api_key'
    # Do NOT enrich with cloud_provider or resource_types as they cause unexpected keyword argument errors
    # "wistx_calculate_infrastructure_cost": [],  # No enrichment needed - resources param has cloud info
    # Troubleshooting
    "wistx_troubleshoot_issue": ["cloud_provider", "resource_types", "infrastructure_code"],
    # Research
    "wistx_research": ["cloud_provider"],
    # Context
    "wistx_context": ["cloud_provider", "resource_types", "compliance_standards"],
}


def _extract_value_from_result(result: dict[str, Any], param: str) -> Any:
    """Extract a parameter value from a tool result.

    Args:
        result: Tool result dictionary
        param: Parameter name to extract

    Returns:
        Extracted value or None
    """
    if not isinstance(result, dict):
        return None

    # Direct key match
    if param in result:
        return result[param]

    # Special case mappings
    if param == "compliance_standards":
        # wistx_get_compliance_requirements stores as "standards"
        if "standards" in result:
            return result["standards"]
        # Could also be in a nested structure
        if "compliance" in result and isinstance(result["compliance"], dict):
            return result["compliance"].get("standards")

    if param == "infrastructure_code":
        # wistx_infrastructure stores as "scaffolding"
        if "scaffolding" in result:
            return result["scaffolding"]
        # Could also be in "code" or "infrastructure"
        for key in ["code", "infrastructure", "terraform_code", "k8s_code"]:
            if key in result:
                return result[key]

    if param == "resource_types":
        # Could be stored under various keys
        for key in ["resource_types", "resources", "aws_resources", "components"]:
            if key in result and isinstance(result[key], list):
                return result[key]

    # Rich data extractions - actual structured data for documentation generation
    if param == "compliance_controls":
        # Extract actual compliance control objects from wistx_get_compliance_requirements
        if "controls" in result and isinstance(result["controls"], list):
            return result["controls"]

    if param == "infrastructure_modules":
        # Extract actual infrastructure modules from wistx_infrastructure
        if "modules" in result and isinstance(result["modules"], list):
            return result["modules"]
        # Also check for components
        if "components" in result and isinstance(result["components"], list):
            return result["components"]

    if param == "cost_data":
        # Extract cost breakdown from wistx_calculate_infrastructure_cost
        if "cost_breakdown" in result:
            return {
                "cost_breakdown": result.get("cost_breakdown", []),
                "total_monthly_cost": result.get("total_monthly_cost"),
                "total_annual_cost": result.get("total_annual_cost"),
                "optimization_suggestions": result.get("optimization_suggestions", []),
            }

    if param == "architecture_context":
        # Extract architecture context from wistx_infrastructure
        if "architecture_context" in result:
            return result["architecture_context"]

    if param == "security_context":
        # Extract security context from wistx_infrastructure
        if "security_context" in result:
            return result["security_context"]

    return None


def enrich_arguments_from_session(
    tool_name: str,
    arguments: dict[str, Any],
    session_id: str | None = None,
) -> tuple[dict[str, Any], list[str]]:
    """Centralized auto-enrichment of tool arguments from session context.

    This middleware function enriches tool arguments with values from previously
    called tools in the same session. It only enriches parameters that:
    1. Are not already provided (explicit values take priority)
    2. Are relevant for the target tool
    3. Are available from previous tool results

    Args:
        tool_name: Name of the tool being called
        arguments: Original arguments passed to the tool
        session_id: Optional session ID (uses current if not provided)

    Returns:
        Tuple of (enriched_arguments, list of enriched parameter names)
    """
    # Check if this tool accepts enrichment
    if tool_name not in TOOLS_ACCEPTING_ENRICHMENT:
        return arguments, []

    accepted_params = TOOLS_ACCEPTING_ENRICHMENT[tool_name]
    enriched_args = dict(arguments)  # Create a copy
    enriched_params: list[str] = []

    # Get all previous results from session
    previous_results = get_all_previous_results(session_id)

    if not previous_results:
        return enriched_args, enriched_params

    # For each parameter this tool accepts
    for param in accepted_params:
        # Skip if already provided and not empty
        current_value = enriched_args.get(param)
        if current_value is not None and current_value != "" and current_value != []:
            continue

        # Try to find value from previous tool results
        source_tools = ENRICHABLE_PARAMS.get(param, [])

        for source_tool in source_tools:
            if source_tool in previous_results:
                result = previous_results[source_tool]
                value = _extract_value_from_result(result, param)

                if value is not None and value != "" and value != []:
                    enriched_args[param] = value
                    enriched_params.append(f"{param} (from {source_tool})")
                    logger.debug(
                        "Enriched '%s' for tool '%s' from '%s': %s",
                        param, tool_name, source_tool,
                        str(value)[:50] + "..." if len(str(value)) > 50 else value
                    )
                    break  # Found a value, stop searching

    # Special handling for configuration dict (merge instead of replace)
    if "configuration" in enriched_args or any(
        p in ["cloud_provider", "project_type"] for p in enriched_params
    ):
        config = enriched_args.get("configuration") or {}
        if not isinstance(config, dict):
            config = {}

        # Add enriched values to configuration if not present
        if "cloud_provider" in enriched_args and "cloud_provider" not in config:
            config["cloud_provider"] = enriched_args.get("cloud_provider")
        if "project_type" in enriched_args and "project_type" not in config:
            config["project_type"] = enriched_args.get("project_type")

        if config:
            enriched_args["configuration"] = config

    if enriched_params:
        logger.info(
            "Auto-enriched tool '%s' with: %s",
            tool_name, ", ".join(enriched_params)
        )
        # Log details about rich data enrichment for debugging
        for param in ["compliance_controls", "infrastructure_modules", "cost_data"]:
            if param in enriched_args and enriched_args[param]:
                value = enriched_args[param]
                if isinstance(value, list):
                    logger.info("  -> %s: %d items", param, len(value))
                elif isinstance(value, dict):
                    logger.info("  -> %s: %d keys", param, len(value))
    else:
        # Log if no enrichment happened despite previous results existing
        if previous_results:
            logger.debug(
                "No enrichment for '%s' (had %d previous results: %s)",
                tool_name, len(previous_results), list(previous_results.keys())
            )

    return enriched_args, enriched_params

