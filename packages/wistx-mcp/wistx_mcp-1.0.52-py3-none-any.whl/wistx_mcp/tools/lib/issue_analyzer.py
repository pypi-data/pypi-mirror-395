"""Issue analyzer for troubleshooting infrastructure and code issues."""

import logging
import re
from typing import Any

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.vector_search import VectorSearch
from wistx_mcp.config import settings

logger = logging.getLogger(__name__)


class IssueAnalyzer:
    """Analyzer for diagnosing infrastructure and code issues."""

    def __init__(self, mongodb_client: MongoDBClient):
        """Initialize issue analyzer.

        Args:
            mongodb_client: MongoDB client for knowledge base access
        """
        self.mongodb_client = mongodb_client
        self.vector_search = VectorSearch(
            mongodb_client,
            gemini_api_key=settings.gemini_api_key,
        )

    async def analyze_error(
        self,
        error_message: str,
        infrastructure_type: str | None = None,
        cloud_provider: str | None = None,
    ) -> dict[str, Any]:
        """Analyze error message to identify issue patterns.

        Args:
            error_message: Error message text
            infrastructure_type: Type of infrastructure
            cloud_provider: Cloud provider

        Returns:
            Dictionary with error analysis
        """
        error_patterns = self._extract_error_patterns(error_message)

        query = f"{error_message} {infrastructure_type} {cloud_provider}"
        similar_issues = await self.vector_search.search_knowledge_articles(
            query=query,
            domains=["devops", "infrastructure", "security"],
            limit=10,
        )

        return {
            "error_patterns": error_patterns,
            "similar_issues": similar_issues,
            "likely_causes": self._identify_likely_causes(error_patterns),
        }

    def _extract_error_patterns(self, error_message: str) -> list[str]:
        """Extract error patterns from error message.

        Args:
            error_message: Error message text

        Returns:
            List of error patterns found
        """
        patterns = []

        common_patterns = [
            (r"timeout", "timeout"),
            (r"connection.*refused", "connection_refused"),
            (r"permission.*denied", "permission_denied"),
            (r"resource.*not.*found", "resource_not_found"),
            (r"already.*exists", "already_exists"),
            (r"invalid.*configuration", "invalid_configuration"),
            (r"quota.*exceeded", "quota_exceeded"),
            (r"authentication.*failed", "authentication_failed"),
            (r"network.*error", "network_error"),
            (r"service.*unavailable", "service_unavailable"),
            (r"rate.*limit", "rate_limit"),
            (r"dependency.*missing", "dependency_missing"),
        ]

        error_lower = error_message.lower()
        for pattern_regex, pattern_name in common_patterns:
            if re.search(pattern_regex, error_lower):
                patterns.append(pattern_name)

        return patterns

    def _identify_likely_causes(self, error_patterns: list[str]) -> list[str]:
        """Identify likely causes based on error patterns.

        Args:
            error_patterns: List of error patterns

        Returns:
            List of likely causes
        """
        cause_mapping = {
            "timeout": "Network connectivity issue or resource overload. Check network configuration and resource capacity.",
            "connection_refused": "Service not running or firewall blocking. Verify service status and security groups.",
            "permission_denied": "IAM/security group misconfiguration. Check permissions and access policies.",
            "resource_not_found": "Resource doesn't exist or wrong region. Verify resource name and region.",
            "already_exists": "Resource naming conflict. Use unique names or check for existing resources.",
            "invalid_configuration": "Configuration syntax or value error. Validate configuration format and values.",
            "quota_exceeded": "Resource quota limit reached. Check quotas and request increases if needed.",
            "authentication_failed": "Invalid credentials or token expired. Verify credentials and refresh tokens.",
            "network_error": "Network connectivity issue. Check VPC, subnets, and routing configuration.",
            "service_unavailable": "Service is down or not accessible. Check service status and health checks.",
            "rate_limit": "API rate limit exceeded. Implement retry logic with exponential backoff.",
            "dependency_missing": "Required dependency not available. Check dependencies and installation.",
        }

        causes = []
        for pattern in error_patterns:
            if pattern in cause_mapping:
                causes.append(cause_mapping[pattern])

        if not causes:
            causes.append("Unable to identify specific cause. Review error message and configuration.")

        return causes

    def analyze_logs(self, logs: str) -> dict[str, Any]:
        """Analyze log output for issues.

        Args:
            logs: Log output text

        Returns:
            Dictionary with log analysis
        """
        error_lines = []
        warning_lines = []
        critical_patterns = []

        log_lines = logs.split("\n")
        for line in log_lines:
            line_lower = line.lower()
            if "error" in line_lower or "failed" in line_lower:
                error_lines.append(line[:200])
            if "warning" in line_lower:
                warning_lines.append(line[:200])
            if any(pattern in line_lower for pattern in ["critical", "fatal", "panic"]):
                critical_patterns.append(line[:200])

        return {
            "error_count": len(error_lines),
            "warning_count": len(warning_lines),
            "critical_count": len(critical_patterns),
            "error_lines": error_lines[:10],
            "warning_lines": warning_lines[:10],
            "critical_lines": critical_patterns[:10],
        }

    async def analyze_configuration(
        self,
        configuration_code: str,
        infrastructure_type: str | None = None,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Analyze configuration code for potential issues.

        Args:
            configuration_code: Configuration code text
            infrastructure_type: Type of infrastructure
            api_key: Optional API key for codebase-wide regex search

        Returns:
            Dictionary with configuration analysis
        """
        issues = []
        warnings = []
        regex_issues = []

        if infrastructure_type == "terraform":
            if "resource" in configuration_code and "provider" not in configuration_code:
                warnings.append("Missing provider configuration")

            if re.search(r'password\s*=\s*["\']', configuration_code, re.IGNORECASE):
                issues.append("Hardcoded password detected - use variables or secrets")

            if re.search(r'access_key\s*=\s*["\']', configuration_code, re.IGNORECASE):
                issues.append("Hardcoded access key detected - use environment variables")

        if infrastructure_type == "kubernetes":
            if "image:" in configuration_code and ":latest" in configuration_code:
                warnings.append("Using 'latest' tag - specify version for production")

            if "resources:" not in configuration_code:
                warnings.append("Missing resource limits - recommended for production")

        if api_key:
            try:
                from wistx_mcp.tools import regex_search

                security_templates = ["api_key", "password", "secret_key", "token", "credential"]
                file_types_map = {
                    "terraform": [".tf"],
                    "kubernetes": [".yaml", ".yml"],
                    "docker": [".dockerfile", "Dockerfile"],
                    "python": [".py"],
                }
                file_types = file_types_map.get(infrastructure_type or "", [])

                for template in security_templates:
                    try:
                        regex_results = await regex_search.regex_search_codebase(
                            template=template,
                            api_key=api_key,
                            file_types=file_types if file_types else None,
                            code_type=infrastructure_type,
                            include_context=True,
                            limit=10,
                        )
                        matches = regex_results.get("matches", [])
                        if matches:
                            regex_issues.append({
                                "type": template,
                                "count": len(matches),
                                "matches": matches[:5],
                            })
                    except Exception as e:
                        logger.warning("Regex search failed for template %s: %s", template, e)

                if infrastructure_type == "terraform":
                    compliance_templates = ["unencrypted_storage", "public_access", "missing_backup"]
                    for template in compliance_templates:
                        try:
                            regex_results = await regex_search.regex_search_codebase(
                                template=template,
                                api_key=api_key,
                                file_types=[".tf"],
                                include_context=True,
                                limit=5,
                            )
                            matches = regex_results.get("matches", [])
                            if matches:
                                regex_issues.append({
                                    "type": template,
                                    "count": len(matches),
                                    "matches": matches[:3],
                                })
                        except Exception as e:
                            logger.warning("Regex search failed for template %s: %s", template, e)

                if infrastructure_type == "kubernetes":
                    k8s_templates = ["latest_tag", "no_resource_limits"]
                    for template in k8s_templates:
                        try:
                            regex_results = await regex_search.regex_search_codebase(
                                template=template,
                                api_key=api_key,
                                file_types=[".yaml", ".yml"],
                                include_context=True,
                                limit=5,
                            )
                            matches = regex_results.get("matches", [])
                            if matches:
                                regex_issues.append({
                                    "type": template,
                                    "count": len(matches),
                                    "matches": matches[:3],
                                })
                        except Exception as e:
                            logger.warning("Regex search failed for template %s: %s", template, e)

            except ImportError:
                logger.warning("regex_search module not available, using basic analysis only")
            except Exception as e:
                logger.warning("Regex search integration failed: %s", e, exc_info=True)

        if regex_issues:
            for regex_issue in regex_issues:
                issue_type = regex_issue["type"].replace("_", " ").title()
                issues.append(
                    f"Found {regex_issue['count']} {issue_type} issues in codebase "
                    f"(see regex_search results for details)"
                )

        return {
            "issues": issues,
            "warnings": warnings,
            "has_security_issues": len(issues) > 0,
            "regex_issues": regex_issues if regex_issues else None,
        }

