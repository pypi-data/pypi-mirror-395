"""Unit tests for MCP server configuration."""

import os
import pytest
from unittest.mock import patch


def test_config_reload_from_env():
    """Test that reload_from_env() properly loads environment variables."""
    from wistx_mcp.config import MCPServerSettings

    # Create initial settings without API key
    with patch.dict(os.environ, {}, clear=False):
        # Remove WISTX_API_KEY if it exists
        os.environ.pop("WISTX_API_KEY", None)
        settings = MCPServerSettings()
        assert settings.api_key == ""  # Default is empty string

    # Now set the environment variable and reload
    with patch.dict(os.environ, {"WISTX_API_KEY": "test-key-12345"}):
        settings.reload_from_env()
        assert settings.api_key == "test-key-12345"


def test_config_reload_from_env_api_url():
    """Test that reload_from_env() properly loads API URL."""
    from wistx_mcp.config import MCPServerSettings
    
    # Create initial settings with default API URL
    settings = MCPServerSettings()
    assert settings.api_url == "https://api.wistx.ai"
    
    # Now set the environment variable and reload
    with patch.dict(os.environ, {"WISTX_API_URL": "https://custom.api.wistx.ai"}):
        settings.reload_from_env()
        assert settings.api_url == "https://custom.api.wistx.ai"


def test_config_reload_from_env_multiple_vars():
    """Test that reload_from_env() loads multiple environment variables."""
    from wistx_mcp.config import MCPServerSettings
    
    settings = MCPServerSettings()
    
    # Set multiple environment variables
    env_vars = {
        "WISTX_API_KEY": "test-key-xyz",
        "WISTX_API_URL": "https://test.api.wistx.ai",
        "LOG_LEVEL": "DEBUG",
    }
    
    with patch.dict(os.environ, env_vars):
        settings.reload_from_env()
        assert settings.api_key == "test-key-xyz"
        assert settings.api_url == "https://test.api.wistx.ai"
        assert settings.log_level == "DEBUG"


def test_config_preserves_other_settings():
    """Test that reload_from_env() preserves settings not in environment."""
    from wistx_mcp.config import MCPServerSettings

    settings = MCPServerSettings()
    original_server_name = settings.server_name

    # Reload with only API key set
    with patch.dict(os.environ, {"WISTX_API_KEY": "test-key"}):
        settings.reload_from_env()
        assert settings.api_key == "test-key"
        assert settings.server_name == original_server_name


def test_config_api_key_required():
    """Test that API key is required (not optional)."""
    from wistx_mcp.config import MCPServerSettings

    # Create settings without API key
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("WISTX_API_KEY", None)
        settings = MCPServerSettings()
        # API key should be empty string (default)
        assert settings.api_key == ""
        # But it should be a string type, not None
        assert isinstance(settings.api_key, str)

