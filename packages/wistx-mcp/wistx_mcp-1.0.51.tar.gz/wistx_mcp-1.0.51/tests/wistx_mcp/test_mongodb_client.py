"""Unit tests for MongoDB client."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient


@pytest.mark.asyncio
async def test_mongodb_client_connect_success():
    """Test successful MongoDB connection."""
    client = MongoDBClient()

    with patch("wistx_mcp.tools.lib.mongodb_client.AsyncIOMotorClient") as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.admin.command = AsyncMock(return_value={"ok": 1})
        mock_client.__getitem__ = MagicMock(return_value=MagicMock())

        await client.connect()

        assert client.client is not None
        assert client.database is not None
        mock_client.admin.command.assert_called_once()


@pytest.mark.asyncio
async def test_mongodb_client_connect_with_retry():
    """Test MongoDB connection with retry on timeout."""
    client = MongoDBClient()

    with patch("wistx_mcp.tools.lib.mongodb_client.AsyncIOMotorClient") as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.__getitem__ = MagicMock(return_value=MagicMock())

        import asyncio
        mock_client.admin.command = AsyncMock(side_effect=[
            asyncio.TimeoutError(),
            {"ok": 1},
        ])

        await client.connect()

        assert client.client is not None
        assert mock_client.admin.command.call_count == 2


@pytest.mark.asyncio
async def test_mongodb_client_connect_failure_after_retries():
    """Test MongoDB connection failure after all retries."""
    client = MongoDBClient()

    with patch("wistx_mcp.tools.lib.mongodb_client.AsyncIOMotorClient") as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.__getitem__ = MagicMock(return_value=MagicMock())

        import asyncio
        mock_client.admin.command = AsyncMock(side_effect=asyncio.TimeoutError())

        with pytest.raises(RuntimeError, match="MongoDB connection timeout"):
            await client.connect()


@pytest.mark.asyncio
async def test_mongodb_client_disconnect():
    """Test MongoDB disconnection."""
    client = MongoDBClient()

    with patch("wistx_mcp.tools.lib.mongodb_client.AsyncIOMotorClient") as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.admin.command = AsyncMock(return_value={"ok": 1})
        mock_client.__getitem__ = MagicMock(return_value=MagicMock())
        mock_client.close = MagicMock()

        await client.connect()
        await client.disconnect()

        assert client.client is None
        assert client.database is None
        mock_client.close.assert_called_once()


@pytest.mark.asyncio
async def test_mongodb_client_health_check_success():
    """Test successful health check."""
    client = MongoDBClient()

    with patch("wistx_mcp.tools.lib.mongodb_client.AsyncIOMotorClient") as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.admin.command = AsyncMock(return_value={"ok": 1})
        mock_client.__getitem__ = MagicMock(return_value=MagicMock())

        await client.connect()

        is_healthy = await client.health_check()

        assert is_healthy is True


@pytest.mark.asyncio
async def test_mongodb_client_health_check_failure():
    """Test health check failure."""
    client = MongoDBClient()

    is_healthy = await client.health_check()

    assert is_healthy is False


@pytest.mark.asyncio
async def test_mongodb_client_connection_pooling():
    """Test connection pooling configuration."""
    client = MongoDBClient()

    with patch("wistx_mcp.tools.lib.mongodb_client.AsyncIOMotorClient") as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.admin.command = AsyncMock(return_value={"ok": 1})
        mock_client.__getitem__ = MagicMock(return_value=MagicMock())

        await client.connect()

        mock_client_class.assert_called_once()
        call_kwargs = mock_client_class.call_args[1]

        assert call_kwargs["maxPoolSize"] == 50
        assert call_kwargs["minPoolSize"] == 10
        assert call_kwargs["serverSelectionTimeoutMS"] == 5000
        assert call_kwargs["connectTimeoutMS"] == 10000
        assert call_kwargs["socketTimeoutMS"] == 30000
        assert call_kwargs["retryWrites"] is True
        assert call_kwargs["retryReads"] is True

