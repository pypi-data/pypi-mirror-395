"""Unit tests for design_architecture tool."""

import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from wistx_mcp.tools.design_architecture import (
    design_architecture,
    _validate_and_create_output_directory,
)


@pytest.mark.asyncio
async def test_validate_output_directory_valid():
    """Test valid output directory validation."""
    with patch("wistx_mcp.tools.design_architecture.Path") as mock_path:
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path_instance.is_dir.return_value = True
        mock_path_instance.__truediv__ = MagicMock(return_value=MagicMock())
        mock_path.return_value.resolve.return_value = mock_path_instance

        result = _validate_and_create_output_directory(
            output_directory=".",
            project_name="test-project",
        )

        assert result is not None


@pytest.mark.asyncio
async def test_validate_output_directory_path_traversal():
    """Test path traversal prevention."""
    with pytest.raises(ValueError, match="Path traversal not allowed"):
        _validate_and_create_output_directory(
            output_directory="../etc",
            project_name="test",
        )


@pytest.mark.asyncio
async def test_validate_output_directory_invalid_characters():
    """Test invalid character filtering."""
    with pytest.raises(ValueError, match="Invalid characters"):
        _validate_and_create_output_directory(
            output_directory=".",
            project_name="test/project",
        )


@pytest.mark.asyncio
async def test_validate_output_directory_absolute_path():
    """Test absolute path restriction."""
    with pytest.raises(ValueError, match="Only /tmp directory allowed"):
        _validate_and_create_output_directory(
            output_directory="/root",
            project_name="test",
        )


@pytest.mark.asyncio
async def test_design_architecture_initialize():
    """Test architecture initialization."""
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
            "structure": {"README.md": "# Test Project"},
        })

        mock_gather.return_value = {}
        mock_enhance.return_value = {"structure": {"README.md": "# Test Project"}}
        mock_create.return_value = None

        result = await design_architecture(
            action="initialize",
            project_type="kubernetes",
            project_name="test-project",
            output_directory=".",
        )

        assert "project_path" in result
        assert "files_created" in result
        assert "structure" in result
        assert "intelligent_context" in result


@pytest.mark.asyncio
async def test_design_architecture_invalid_action():
    """Test invalid action handling."""
    with pytest.raises(ValueError, match="Invalid action"):
        await design_architecture(action="invalid")


@pytest.mark.asyncio
async def test_design_architecture_initialize_missing_params():
    """Test initialize action with missing parameters."""
    with pytest.raises(ValueError, match="project_type and project_name are required"):
        await design_architecture(action="initialize")


@pytest.mark.asyncio
async def test_design_architecture_parallel_context_gathering():
    """Test parallel context gathering."""
    import asyncio

    with patch("wistx_mcp.tools.design_architecture.mcp_tools.get_compliance_requirements") as mock_compliance, \
         patch("wistx_mcp.tools.design_architecture.web_search.web_search") as mock_security, \
         patch("wistx_mcp.tools.design_architecture.mcp_tools.research_knowledge_base") as mock_bp, \
         patch("wistx_mcp.tools.design_architecture.code_examples.get_code_examples") as mock_code:

        mock_compliance.return_value = {"controls": []}
        mock_security.return_value = {"results": []}
        mock_bp.return_value = {"results": []}
        mock_code.return_value = {"examples": []}

        from wistx_mcp.tools.design_architecture import _gather_intelligent_context
        from wistx_mcp.tools.lib.mongodb_client import MongoDBClient

        mock_mongo = MagicMock()
        context = await _gather_intelligent_context(
            mongodb_client=mock_mongo,
            project_type="kubernetes",
            architecture_type="microservices",
            cloud_provider="aws",
            compliance_standards=["PCI-DSS"],
            include_compliance=True,
            include_security=True,
            include_best_practices=True,
            include_code_examples=True,
        )

        assert "compliance" in context or "security" in context or "best_practices" in context or "code_examples" in context

