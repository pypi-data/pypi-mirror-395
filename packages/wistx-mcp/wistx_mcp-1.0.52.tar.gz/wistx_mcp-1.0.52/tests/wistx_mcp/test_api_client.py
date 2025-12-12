"""Unit tests for API client."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from wistx_mcp.tools.lib.api_client import WISTXAPIClient


@pytest.mark.asyncio
async def test_api_client_get_compliance_requirements():
    """Test compliance requirements API call."""
    client = WISTXAPIClient()

    mock_response = MagicMock()
    mock_response.json.return_value = {"controls": []}
    mock_response.raise_for_status = MagicMock()

    with patch("wistx_mcp.tools.lib.api_client.with_timeout_and_retry") as mock_retry:
        mock_retry.return_value = mock_response

        result = await client.get_compliance_requirements(
            resource_types=["RDS"],
            standards=["PCI-DSS"],
        )

        assert "controls" in result
        mock_retry.assert_called_once()


@pytest.mark.asyncio
async def test_api_client_research_knowledge_base():
    """Test knowledge base research API call."""
    client = WISTXAPIClient()

    mock_response = MagicMock()
    mock_response.json.return_value = {"results": []}
    mock_response.raise_for_status = MagicMock()

    with patch("wistx_mcp.tools.lib.api_client.with_timeout_and_retry") as mock_retry:
        mock_retry.return_value = mock_response

        result = await client.research_knowledge_base(
            query="kubernetes best practices",
            domains=["devops"],
        )

        assert "results" in result
        mock_retry.assert_called_once()


@pytest.mark.asyncio
async def test_api_client_close():
    """Test API client cleanup."""
    client = WISTXAPIClient()

    mock_client = AsyncMock()
    client.client = mock_client

    await client.close()

    mock_client.aclose.assert_called_once()

