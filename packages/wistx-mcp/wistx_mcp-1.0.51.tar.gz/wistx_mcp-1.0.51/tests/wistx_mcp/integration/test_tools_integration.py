"""Integration tests for MCP tools."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from wistx_mcp.tools import mcp_tools, web_search, design_architecture


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_compliance_requirements_integration():
    """Integration test for compliance requirements tool."""
    with patch("wistx_mcp.tools.mcp_tools.api_client") as mock_client:
        mock_client.get_compliance_requirements = AsyncMock(return_value={
            "controls": [
                {
                    "control_id": "PCI-DSS-3.4",
                    "title": "Encrypt cardholder data",
                    "severity": "HIGH",
                },
            ],
        })

        result = await mcp_tools.get_compliance_requirements(
            resource_types=["RDS"],
            standards=["PCI-DSS"],
        )

        assert "controls" in result
        assert len(result["controls"]) > 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_web_search_integration():
    """Integration test for web search tool."""
    with patch("wistx_mcp.tools.web_search.MongoDBClient") as mock_mongo, \
         patch("wistx_mcp.tools.web_search.SecurityClient") as mock_security, \
         patch("wistx_mcp.tools.web_search.WebSearchClient") as mock_web:

        mock_mongo_instance = MagicMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_mongo_instance.connect = AsyncMock()
        mock_mongo_instance.disconnect = AsyncMock()

        mock_security_instance = MagicMock()
        mock_security.return_value = mock_security_instance
        mock_security_instance.search_cves = AsyncMock(return_value=[])
        mock_security_instance.search_advisories = AsyncMock(return_value=[])
        mock_security_instance.search_kubernetes_security = AsyncMock(return_value=[])
        mock_security_instance.close = AsyncMock()

        mock_web_instance = MagicMock()
        mock_web.return_value = mock_web_instance
        mock_web_instance.search_devops = AsyncMock(return_value={
            "results": [],
            "answer": None,
        })
        mock_web_instance.close = AsyncMock()

        result = await web_search.web_search(
            query="kubernetes security",
            search_type="security",
        )

        assert "security" in result
        assert "web" in result
        assert "total" in result


@pytest.mark.integration
@pytest.mark.asyncio
async def test_design_architecture_integration():
    """Integration test for architecture design tool."""
    with patch("wistx_mcp.tools.design_architecture.MongoDBClient") as mock_mongo, \
         patch("wistx_mcp.tools.design_architecture.ArchitectureTemplates") as mock_templates, \
         patch("wistx_mcp.tools.design_architecture._gather_intelligent_context") as mock_gather, \
         patch("wistx_mcp.tools.design_architecture._enhance_template_with_context") as mock_enhance, \
         patch("wistx_mcp.tools.design_architecture._create_intelligent_project_structure") as mock_create:

        mock_mongo_instance = MagicMock()
        mock_mongo.return_value = mock_mongo_instance
        mock_mongo_instance.connect = AsyncMock()
        mock_mongo_instance.close = AsyncMock()

        mock_templates_instance = MagicMock()
        mock_templates.return_value = mock_templates_instance
        mock_templates_instance.get_template = AsyncMock(return_value={
            "structure": {
                "README.md": "# Test Project",
                "deployments": {},
            },
        })

        mock_gather.return_value = {
            "compliance": {"controls": []},
            "security": {"results": []},
        }
        mock_enhance.return_value = {
            "structure": {"README.md": "# Test Project"},
        }
        mock_create.return_value = None

        result = await design_architecture.design_architecture(
            action="initialize",
            project_type="kubernetes",
            project_name="test-project",
            output_directory=".",
            compliance_standards=["PCI-DSS"],
        )

        assert "project_path" in result
        assert "intelligent_context" in result
        assert result["compliance_applied"] is True

