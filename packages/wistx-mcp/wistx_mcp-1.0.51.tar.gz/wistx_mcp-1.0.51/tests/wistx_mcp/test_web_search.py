"""Unit tests for web_search tool."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from wistx_mcp.tools import web_search


@pytest.mark.asyncio
async def test_web_search_general():
    """Test general web search."""
    with patch("wistx_mcp.tools.web_search.MongoDBClient") as mock_mongo, \
         patch("wistx_mcp.tools.web_search.SecurityClient") as mock_security, \
         patch("wistx_mcp.tools.web_search.WebSearchClient") as mock_web, \
         patch("wistx_mcp.config.settings") as mock_settings:

        mock_settings.tavily_api_key = "test-key"

        mock_mongo_instance = MagicMock()
        mock_mongo_instance.connect = AsyncMock()
        mock_mongo.return_value = mock_mongo_instance

        mock_security_instance = MagicMock()
        mock_security_instance.search_cves = AsyncMock(return_value=[])
        mock_security_instance.search_advisories = AsyncMock(return_value=[])
        mock_security_instance.search_kubernetes_security = AsyncMock(return_value=[])
        mock_security_instance.close = AsyncMock()
        mock_security.return_value = mock_security_instance

        mock_web_instance = MagicMock()
        mock_web_instance.search_devops = AsyncMock(return_value={
            "results": [{"title": "Test", "content": "Content", "url": "https://test.com"}],
            "answer": "Test answer",
        })
        mock_web_instance.close = AsyncMock()
        mock_web.return_value = mock_web_instance

        result = await web_search.web_search(
            query="kubernetes deployment",
            search_type="general",
        )

        assert "web" in result
        assert "security" in result
        assert "total" in result
        assert result["total"] >= 0


@pytest.mark.asyncio
async def test_web_search_security():
    """Test security web search."""
    with patch("wistx_mcp.tools.web_search.MongoDBClient") as mock_mongo, \
         patch("wistx_mcp.tools.web_search.SecurityClient") as mock_security, \
         patch("wistx_mcp.config.settings") as mock_settings:

        mock_settings.tavily_api_key = None

        mock_mongo_instance = MagicMock()
        mock_mongo_instance.connect = AsyncMock()
        mock_mongo.return_value = mock_mongo_instance

        mock_security_instance = MagicMock()
        mock_security_instance.search_cves = AsyncMock(return_value=[
            {"cve_id": "CVE-2024-1234", "title": "Test CVE", "severity": "HIGH"},
        ])
        mock_security_instance.search_advisories = AsyncMock(return_value=[])
        mock_security_instance.search_kubernetes_security = AsyncMock(return_value=[])
        mock_security_instance.close = AsyncMock()
        mock_security.return_value = mock_security_instance

        result = await web_search.web_search(
            query="kubernetes vulnerability",
            search_type="security",
            include_cves=True,
        )

        assert "security" in result
        assert len(result["security"]) > 0


@pytest.mark.asyncio
async def test_web_search_invalid_search_type():
    """Test web search with invalid search type."""
    with pytest.raises(ValueError, match="Invalid search_type"):
        await web_search.web_search(
            query="test",
            search_type="invalid",
        )


@pytest.mark.asyncio
async def test_web_search_invalid_limit():
    """Test web search with invalid limit."""
    with pytest.raises(ValueError, match="limit must be between"):
        await web_search.web_search(
            query="test",
            limit=0,
        )

    with pytest.raises(ValueError, match="limit must be between"):
        await web_search.web_search(
            query="test",
            limit=101,
        )

