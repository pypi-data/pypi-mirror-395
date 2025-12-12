"""Unit tests for troubleshoot_issue tool."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from wistx_mcp.tools import troubleshoot_issue
from wistx_mcp.tools.lib.issue_analyzer import IssueAnalyzer


@pytest.mark.asyncio
async def test_troubleshoot_issue_basic():
    """Test basic troubleshooting."""
    with patch("wistx_mcp.tools.troubleshoot_issue.MongoDBClient") as mock_mongo, \
         patch("wistx_mcp.tools.troubleshoot_issue.VectorSearch") as mock_vector, \
         patch("wistx_mcp.tools.troubleshoot_issue.WebSearchClient") as mock_web, \
         patch("wistx_mcp.config.settings") as mock_settings:

        mock_settings.tavily_api_key = None
        mock_settings.gemini_api_key = "test-key"

        mock_mongo_instance = MagicMock()
        mock_mongo_instance.connect = AsyncMock()
        mock_mongo.return_value = mock_mongo_instance

        mock_vector_instance = MagicMock()
        mock_vector_instance.search_knowledge_articles = AsyncMock(return_value=[])
        mock_vector.return_value = mock_vector_instance

        result = await troubleshoot_issue.troubleshoot_issue(
            issue_description="Kubernetes pod failing to start",
            infrastructure_type="kubernetes",
        )

        assert "diagnosis" in result
        assert "issues" in result
        assert "fixes" in result
        assert "prevention" in result


@pytest.mark.asyncio
async def test_troubleshoot_issue_with_errors():
    """Test troubleshooting with error messages."""
    with patch("wistx_mcp.tools.troubleshoot_issue.MongoDBClient") as mock_mongo, \
         patch("wistx_mcp.tools.troubleshoot_issue.VectorSearch") as mock_vector, \
         patch("wistx_mcp.config.settings") as mock_settings:

        mock_settings.tavily_api_key = None
        mock_settings.gemini_api_key = "test-key"

        mock_mongo_instance = MagicMock()
        mock_mongo_instance.connect = AsyncMock()
        mock_mongo.return_value = mock_mongo_instance

        mock_vector_instance = MagicMock()
        mock_vector_instance.search_knowledge_articles = AsyncMock(return_value=[])
        mock_vector.return_value = mock_vector_instance

        result = await troubleshoot_issue.troubleshoot_issue(
            issue_description="Pod startup failure",
            error_messages=["Error: ImagePullBackOff", "Error: CrashLoopBackOff"],
            infrastructure_type="kubernetes",
        )

        assert "diagnosis" in result
        assert "error_patterns" in result.get("diagnosis", {})


@pytest.mark.asyncio
async def test_troubleshoot_issue_missing_description():
    """Test troubleshooting with missing description."""
    with pytest.raises(ValueError, match="issue_description is required"):
        await troubleshoot_issue.troubleshoot_issue(
            issue_description="",
        )


def test_issue_analyzer_extract_patterns():
    """Test error pattern extraction."""
    analyzer = IssueAnalyzer(MagicMock())

    patterns = analyzer._extract_error_patterns("Connection timeout error occurred")
    assert "timeout" in patterns

    patterns = analyzer._extract_error_patterns("Permission denied when accessing resource")
    assert "permission_denied" in patterns


def test_issue_analyzer_identify_causes():
    """Test likely cause identification."""
    analyzer = IssueAnalyzer(MagicMock())

    causes = analyzer._identify_likely_causes(["timeout"])
    assert len(causes) > 0
    assert "Network connectivity" in causes[0] or "timeout" in causes[0].lower()


def test_issue_analyzer_analyze_logs():
    """Test log analysis."""
    analyzer = IssueAnalyzer(MagicMock())

    logs = """
2024-01-01 ERROR: Failed to connect
2024-01-01 WARNING: High memory usage
2024-01-01 CRITICAL: Service unavailable
"""

    analysis = analyzer.analyze_logs(logs)
    assert analysis["error_count"] > 0
    assert analysis["warning_count"] > 0
    assert analysis["critical_count"] > 0


def test_issue_analyzer_analyze_configuration():
    """Test configuration analysis."""
    analyzer = IssueAnalyzer(MagicMock())

    terraform_code = """
resource "aws_instance" "web" {
  password = "hardcoded-password"
}
"""

    analysis = analyzer.analyze_configuration(terraform_code, "terraform")
    assert len(analysis["issues"]) > 0
    assert "password" in str(analysis["issues"]).lower()

