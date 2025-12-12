"""MCP tools library utilities - lazy loading to prevent segfaults."""

# NOTE: Lazy imports to prevent segmentation faults during module loading
# The utilities are imported on-demand rather than at module load time

__all__ = [
    "WISTXAPIClient",
    "CodeValidator",
    "ErrorHandler",
    "GitHubTreeFetcher",
    "InfrastructureVisualizer",
    "MongoDBClient",
    "TemplateValidator",
    "VectorSearch",
    "SecurityClient",
    "WebSearchClient",
    "TemplateRepositoryManager",
    "TemplateVersionManager",
    "TemplateMarketplace",
    "IncidentTracker",
    "SolutionKnowledgeBuilder",
    "PatternRecognizer",
    "ReportTemplateManager",
    "FormatConverter",
    "TemplateLibrary",
    "ArchitectureTemplates",
    "IssueAnalyzer",
    "DocumentGenerator",
    "IntegrationAnalyzer",
    "IntegrationGenerator",
    "KubernetesManager",
    "MultiCloudManager",
    "with_timeout",
    "with_retry",
    "with_timeout_and_retry",
    "retry_on_failure",
    "timeout",
    "get_tool_versions",
    "get_tool_version",
    "is_tool_deprecated",
    "get_deprecation_warning",
    "resolve_tool_name",
]

def __getattr__(name):
    """Lazy load utilities on demand."""
    if name == "WISTXAPIClient":
        from wistx_mcp.tools.lib.api_client import WISTXAPIClient
        return WISTXAPIClient
    elif name == "CodeValidator":
        from wistx_mcp.tools.lib.code_validator import CodeValidator
        return CodeValidator
    elif name == "ErrorHandler":
        from wistx_mcp.tools.lib.error_handler import ErrorHandler
        return ErrorHandler
    elif name == "GitHubTreeFetcher":
        from wistx_mcp.tools.lib.github_tree_fetcher import GitHubTreeFetcher
        return GitHubTreeFetcher
    elif name == "InfrastructureVisualizer":
        from wistx_mcp.tools.lib.infrastructure_visualizer import InfrastructureVisualizer
        return InfrastructureVisualizer
    elif name == "MongoDBClient":
        from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
        return MongoDBClient
    elif name == "TemplateValidator":
        from wistx_mcp.tools.lib.template_validator import TemplateValidator
        return TemplateValidator
    elif name == "VectorSearch":
        from wistx_mcp.tools.lib.vector_search import VectorSearch
        return VectorSearch
    elif name == "SecurityClient":
        from wistx_mcp.tools.lib.security_client import SecurityClient
        return SecurityClient
    elif name == "WebSearchClient":
        from wistx_mcp.tools.lib.web_search_client import WebSearchClient
        return WebSearchClient
    elif name == "TemplateRepositoryManager":
        from wistx_mcp.tools.lib.template_repository import TemplateRepositoryManager
        return TemplateRepositoryManager
    elif name == "TemplateVersionManager":
        from wistx_mcp.tools.lib.template_version_manager import TemplateVersionManager
        return TemplateVersionManager
    elif name == "TemplateMarketplace":
        from wistx_mcp.tools.lib.template_marketplace import TemplateMarketplace
        return TemplateMarketplace
    elif name == "IncidentTracker":
        from wistx_mcp.tools.lib.incident_tracker import IncidentTracker
        return IncidentTracker
    elif name == "SolutionKnowledgeBuilder":
        from wistx_mcp.tools.lib.solution_builder import SolutionKnowledgeBuilder
        return SolutionKnowledgeBuilder
    elif name == "PatternRecognizer":
        from wistx_mcp.tools.lib.pattern_recognizer import PatternRecognizer
        return PatternRecognizer
    elif name == "ReportTemplateManager":
        from wistx_mcp.tools.lib.report_template_manager import ReportTemplateManager
        return ReportTemplateManager
    elif name == "FormatConverter":
        from wistx_mcp.tools.lib.format_converter import FormatConverter
        return FormatConverter
    elif name == "TemplateLibrary":
        from wistx_mcp.tools.lib.template_library import TemplateLibrary
        return TemplateLibrary
    elif name == "ArchitectureTemplates":
        from wistx_mcp.tools.lib.architecture_templates import ArchitectureTemplates
        return ArchitectureTemplates
    elif name == "IssueAnalyzer":
        from wistx_mcp.tools.lib.issue_analyzer import IssueAnalyzer
        return IssueAnalyzer
    elif name == "DocumentGenerator":
        from wistx_mcp.tools.lib.document_generator import DocumentGenerator
        return DocumentGenerator
    elif name == "IntegrationAnalyzer":
        from wistx_mcp.tools.lib.integration_analyzer import IntegrationAnalyzer
        return IntegrationAnalyzer
    elif name == "IntegrationGenerator":
        from wistx_mcp.tools.lib.integration_generator import IntegrationGenerator
        return IntegrationGenerator
    elif name == "KubernetesManager":
        from wistx_mcp.tools.lib.kubernetes_manager import KubernetesManager
        return KubernetesManager
    elif name == "MultiCloudManager":
        from wistx_mcp.tools.lib.multi_cloud_manager import MultiCloudManager
        return MultiCloudManager
    elif name in ("with_timeout", "with_retry", "with_timeout_and_retry", "retry_on_failure", "timeout"):
        from wistx_mcp.tools.lib import retry_utils
        return getattr(retry_utils, name)
    elif name in ("get_tool_versions", "get_tool_version", "is_tool_deprecated", "get_deprecation_warning", "resolve_tool_name"):
        from wistx_mcp.tools.lib import tool_registry
        return getattr(tool_registry, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

