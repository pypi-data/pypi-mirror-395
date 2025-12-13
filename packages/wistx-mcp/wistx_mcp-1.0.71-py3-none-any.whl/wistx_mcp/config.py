"""MCP server configuration."""

import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MCPServerSettings(BaseSettings):
    """MCP server configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    mongodb_url: str | None = Field(
        default=None,
        validation_alias="MONGODB_URI",
        description="MongoDB connection URL (optional, only needed for tools that access MongoDB directly)",
    )

    mongodb_database: str = Field(
        default="wistx-production",
        validation_alias="DATABASE_NAME",
        description="MongoDB database name",
    )

    pinecone_api_key: str | None = Field(
        default=None,
        validation_alias="PINECONE_API_KEY",
        description="Pinecone API key (optional, only needed for tools that access Pinecone directly)",
    )

    pinecone_environment: str = Field(
        default="us-east-1-aws",
        validation_alias="PINECONE_ENVIRONMENT",
        description="Pinecone environment/region",
    )

    pinecone_index_name: str = Field(
        default="wistx",
        validation_alias="PINECONE_INDEX_NAME",
        description="Pinecone index name",
    )

    server_name: str = Field(
        default="wistx-mcp",
        description="MCP server name",
    )

    server_version: str = Field(
        default="0.1.0",
        description="MCP server version",
    )

    log_level: str = Field(
        default="INFO",
        description="Logging level",
    )

    api_key: str = Field(
        default="",
        validation_alias="WISTX_API_KEY",
        description="WISTX API key for REST API calls (optional, required for API-dependent tools)",
    )

    api_url: str = Field(
        default="https://api.wistx.ai",
        validation_alias="WISTX_API_URL",
        description="WISTX API base URL",
    )

    gemini_api_key: str | None = Field(
        default=None,
        validation_alias="GEMINI_API_KEY",
        description="Gemini API key for embeddings and chat completions",
    )

    tavily_api_key: str | None = Field(
        default=None,
        validation_alias="TAVILY_API_KEY",
        description="Tavily API key for web search",
    )

    tavily_max_age_days: int = Field(
        default=90,
        validation_alias="TAVILY_MAX_AGE_DAYS",
        description="Maximum age of web search results in days (default: 90 days for DevOps/infrastructure)",
    )

    memorystore_host: str | None = Field(
        default=None,
        validation_alias="MEMORYSTORE_HOST",
        description="Google Memorystore (Redis) host for distributed rate limiting (optional, falls back to in-memory if not set)",
    )

    memorystore_port: int = Field(
        default=6379,
        validation_alias="MEMORYSTORE_PORT",
        description="Google Memorystore (Redis) port",
    )

    memorystore_enabled: bool = Field(
        default=False,
        validation_alias="MEMORYSTORE_ENABLED",
        description="Enable Google Memorystore for distributed rate limiting (required for Cloud Run horizontal scaling)",
    )

    redis_url: str | None = Field(
        default=None,
        validation_alias="REDIS_URL",
        description="Redis URL for distributed rate limiting (alternative to Memorystore host/port, format: redis://host:port or redis://user:pass@host:port/0)",
    )

    upload_base_dir: str = Field(
        default="/tmp/wistx_uploads",
        validation_alias="UPLOAD_BASE_DIR",
        description="Base directory for file uploads (must exist and be writable)",
    )

    def reload_from_env(self) -> None:
        """Reload settings from environment variables.

        This is useful when environment variables are set after the initial
        settings object is created (e.g., by MCP server configuration).
        """
        # Re-read from environment
        new_settings = MCPServerSettings()

        # Update all fields from the new settings
        for field_name in MCPServerSettings.model_fields.keys():
            setattr(self, field_name, getattr(new_settings, field_name))


settings = MCPServerSettings()

