"""Tests for MCP server initialization and caching."""

import asyncio
import pytest
from unittest.mock import patch, MagicMock


@pytest.mark.asyncio
async def test_server_info_cached():
    """Test that server info is cached before initialization."""
    # Import the function
    from wistx_mcp.server import get_cached_server_info
    
    # Get cached server info
    info = get_cached_server_info()
    
    # Verify it has the expected structure
    assert isinstance(info, dict)
    assert "name" in info
    assert "version" in info
    assert info["name"] == "wistx-mcp"
    assert info["version"] == "0.1.0"


@pytest.mark.asyncio
async def test_initialization_event_creation():
    """Test that initialization event can be created."""
    from wistx_mcp.server import get_initialization_event
    
    # Get the event
    event = await get_initialization_event()
    
    # Verify it's an asyncio.Event
    assert isinstance(event, asyncio.Event)
    
    # Initially should not be set
    assert not event.is_set()


@pytest.mark.asyncio
async def test_initialization_event_signaling():
    """Test that initialization event can be signaled."""
    from wistx_mcp.server import get_initialization_event
    
    # Get the event
    event = await get_initialization_event()
    
    # Initially not set
    assert not event.is_set()
    
    # Set it
    event.set()
    
    # Now it should be set
    assert event.is_set()


@pytest.mark.asyncio
async def test_wait_for_initialization_success():
    """Test that wait_for_initialization completes when event is set."""
    from wistx_mcp.server import get_initialization_event, _wait_for_initialization
    
    # Get the event and set it
    event = await get_initialization_event()
    event.set()
    
    # Wait should complete immediately
    await _wait_for_initialization(timeout=1.0)
    
    # If we get here, the test passed


@pytest.mark.asyncio
async def test_wait_for_initialization_timeout():
    """Test that wait_for_initialization times out if event is not set."""
    from wistx_mcp.server import _wait_for_initialization
    from wistx_mcp.tools.lib.mcp_errors import MCPError
    
    # Create a new event that won't be set
    import asyncio
    test_event = asyncio.Event()
    
    # Patch the get_initialization_event to return our test event
    with patch('wistx_mcp.server.get_initialization_event') as mock_get_event:
        mock_get_event.return_value = test_event
        
        # Wait should timeout
        with pytest.raises(MCPError):
            await _wait_for_initialization(timeout=0.1)


@pytest.mark.asyncio
async def test_cached_server_info_consistency():
    """Test that cached server info is consistent across calls."""
    from wistx_mcp.server import get_cached_server_info
    
    # Get info multiple times
    info1 = get_cached_server_info()
    info2 = get_cached_server_info()
    
    # Should be the same
    assert info1 == info2
    assert info1["name"] == info2["name"]
    assert info1["version"] == info2["version"]


def test_server_info_structure():
    """Test that server info has the correct structure."""
    from wistx_mcp.server import get_cached_server_info
    
    info = get_cached_server_info()
    
    # Verify structure
    assert isinstance(info, dict)
    assert len(info) == 2
    assert "name" in info
    assert "version" in info
    
    # Verify types
    assert isinstance(info["name"], str)
    assert isinstance(info["version"], str)
    
    # Verify values are not empty
    assert len(info["name"]) > 0
    assert len(info["version"]) > 0

