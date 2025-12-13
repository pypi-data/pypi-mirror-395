"""Pydantic models for API versioning."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class APIVersionInfo(BaseModel):
    """API version information."""

    version: str = Field(..., description="API version (e.g., 'v1')")
    status: str = Field(..., description="Version status: 'current', 'deprecated', 'sunset'")
    release_date: datetime | None = Field(None, description="Version release date")
    deprecation_date: datetime | None = Field(None, description="Deprecation date (if deprecated)")
    sunset_date: datetime | None = Field(None, description="Sunset date (when version will be removed)")
    migration_guide_url: str | None = Field(None, description="URL to migration guide")


class APIVersionResponse(BaseModel):
    """API version response."""

    current_version: str = Field(..., description="Current API version")
    supported_versions: list[str] = Field(..., description="List of supported versions")
    deprecated_versions: list[APIVersionInfo] = Field(default_factory=list, description="Deprecated versions")
    version_info: dict[str, APIVersionInfo] = Field(default_factory=dict, description="Version information")


class MCPToolVersionInfo(BaseModel):
    """MCP tool version information."""

    tool_name: str = Field(..., description="Tool name (without version)")
    current_version: str = Field(..., description="Current tool version")
    available_versions: list[str] = Field(default_factory=list, description="Available versions")
    deprecated_versions: list[str] = Field(default_factory=list, description="Deprecated versions")
    deprecation_dates: dict[str, datetime] = Field(default_factory=dict, description="Deprecation dates by version")
    sunset_dates: dict[str, datetime] = Field(default_factory=dict, description="Sunset dates by version")


class MCPToolVersionResponse(BaseModel):
    """MCP tool version response."""

    tools: dict[str, MCPToolVersionInfo] = Field(default_factory=dict, description="Tool version information")

