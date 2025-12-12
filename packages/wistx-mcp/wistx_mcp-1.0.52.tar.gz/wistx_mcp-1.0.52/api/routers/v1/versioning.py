"""API versioning endpoints."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, Request

from api.dependencies.auth import get_current_user
from api.models.versioning import APIVersionResponse, MCPToolVersionResponse
from api.services.version_tracking_service import version_tracking_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/versioning", tags=["versioning"])


@router.get("/api-versions", response_model=APIVersionResponse)
async def get_api_versions(
    request: Request,
    current_user: dict[str, Any] | None = Depends(get_current_user),
) -> APIVersionResponse:
    """Get API version information.

    Returns:
        API version information including current, supported, and deprecated versions
    """
    from api.middleware.versioning import SUPPORTED_VERSIONS, CURRENT_VERSION, DEPRECATED_VERSIONS
    from api.models.versioning import APIVersionInfo

    deprecated_info = []
    for version, deprecation_data in DEPRECATED_VERSIONS.items():
        deprecated_info.append(
            APIVersionInfo(
                version=version,
                status="deprecated",
                deprecation_date=None,
                sunset_date=None,
                migration_guide_url=deprecation_data.get("migration_guide", ""),
            )
        )

    return APIVersionResponse(
        current_version=CURRENT_VERSION,
        supported_versions=SUPPORTED_VERSIONS,
        deprecated_versions=deprecated_info,
        version_info={},
    )


@router.get("/mcp-tool-versions", response_model=MCPToolVersionResponse)
async def get_mcp_tool_versions(
    request: Request,
    current_user: dict[str, Any] | None = Depends(get_current_user),
) -> MCPToolVersionResponse:
    """Get MCP tool version information.

    Returns:
        MCP tool version information
    """
    from api.models.versioning import MCPToolVersionInfo
    from wistx_mcp.tools.lib.tool_registry import get_tool_versions

    tool_versions = get_tool_versions()

    tools_info = {}
    for tool_name, version_info in tool_versions.items():
        tools_info[tool_name] = MCPToolVersionInfo(
            tool_name=tool_name,
            current_version=version_info.get("current_version", "v1"),
            available_versions=version_info.get("available_versions", ["v1"]),
            deprecated_versions=version_info.get("deprecated_versions", []),
            deprecation_dates={},
            sunset_dates={},
        )

    return MCPToolVersionResponse(tools=tools_info)


@router.get("/api-version-stats")
async def get_api_version_stats(
    request: Request,
    version: str | None = None,
    days: int = 30,
    current_user: dict[str, Any] | None = Depends(get_current_user),
) -> dict[str, Any]:
    """Get API version usage statistics.

    Args:
        request: Request object
        version: Optional version filter
        days: Number of days to analyze

    Returns:
        Version usage statistics
    """
    stats = version_tracking_service.get_api_version_stats(version=version, days=days)
    return {"stats": stats, "period_days": days}


@router.get("/mcp-tool-version-stats")
async def get_mcp_tool_version_stats(
    request: Request,
    tool_name: str | None = None,
    days: int = 30,
    current_user: dict[str, Any] | None = Depends(get_current_user),
) -> dict[str, Any]:
    """Get MCP tool version usage statistics.

    Args:
        request: Request object
        tool_name: Optional tool name filter
        days: Number of days to analyze

    Returns:
        Tool version usage statistics
    """
    stats = version_tracking_service.get_mcp_tool_version_stats(tool_name=tool_name, days=days)
    return {"stats": stats, "period_days": days}

