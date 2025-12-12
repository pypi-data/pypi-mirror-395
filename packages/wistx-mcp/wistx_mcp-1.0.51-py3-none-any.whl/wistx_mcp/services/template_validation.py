"""Template validation service for validating templates against WISTX standards."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class TemplateValidationService:
    """Service for validating templates against WISTX quality standards."""

    async def validate_template(
        self,
        repo_path: str,
        structure: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Validate template meets WISTX standards.

        Args:
            repo_path: Repository path (for future file system access)
            structure: Template structure dictionary

        Returns:
            Validation result with score and checks
        """
        if not structure:
            structure = {}

        checks = {
            "structure_complete": self._check_structure_completeness(structure),
            "security": self._check_security(structure),
            "monitoring": self._check_monitoring(structure),
            "documentation": self._check_documentation(structure),
            "compliance": self._check_compliance(structure),
            "ci_cd": self._check_cicd(structure),
            "testing": self._check_testing(structure),
        }

        score = sum(checks.values()) / len(checks) * 100

        return {
            "valid": score >= 70.0,
            "score": round(score, 2),
            "checks": checks,
            "recommendations": self._generate_recommendations(checks),
        }

    def _check_structure_completeness(self, structure: dict[str, str]) -> float:
        """Check if structure is complete.

        Args:
            structure: Template structure

        Returns:
            Score (0-1)
        """
        if not structure:
            return 0.0

        required_files = ["README.md"]
        has_required = sum(1 for f in required_files if any(f in path for path in structure.keys()))

        has_config_files = any(
            "yaml" in path or "yml" in path or "json" in path or "tf" in path
            for path in structure.keys()
        )

        return min((has_required + (1.0 if has_config_files else 0.0)) / 2.0, 1.0)

    def _check_security(self, structure: dict[str, str]) -> float:
        """Check security best practices.

        Args:
            structure: Template structure

        Returns:
            Score (0-1)
        """
        security_indicators = [
            "rbac",
            "service-account",
            "network-policy",
            "security",
            "secrets",
            "encryption",
            "non-root",
            "read-only",
        ]

        found_indicators = sum(
            1
            for indicator in security_indicators
            if any(indicator.lower() in path.lower() for path in structure.keys())
        )

        return min(found_indicators / 3.0, 1.0)

    def _check_monitoring(self, structure: dict[str, str]) -> float:
        """Check monitoring setup.

        Args:
            structure: Template structure

        Returns:
            Score (0-1)
        """
        monitoring_indicators = [
            "prometheus",
            "grafana",
            "monitoring",
            "metrics",
            "alerting",
            "dashboard",
        ]

        found_indicators = sum(
            1
            for indicator in monitoring_indicators
            if any(indicator.lower() in path.lower() for path in structure.keys())
        )

        return min(found_indicators / 2.0, 1.0)

    def _check_documentation(self, structure: dict[str, str]) -> float:
        """Check documentation quality.

        Args:
            structure: Template structure

        Returns:
            Score (0-1)
        """
        has_readme = any("readme" in path.lower() for path in structure.keys())
        has_docs = any("doc" in path.lower() for path in structure.keys())

        readme_content = ""
        for path in structure.keys():
            if "readme" in path.lower():
                readme_content = structure.get(path, "")

        readme_length = len(readme_content) if readme_content else 0
        has_good_readme = readme_length > 500

        score = 0.0
        if has_readme:
            score += 0.5
        if has_docs:
            score += 0.25
        if has_good_readme:
            score += 0.25

        return min(score, 1.0)

    def _check_compliance(self, structure: dict[str, str]) -> float:
        """Check compliance configurations.

        Args:
            structure: Template structure

        Returns:
            Score (0-1)
        """
        compliance_indicators = [
            "compliance",
            "pci",
            "hipaa",
            "soc2",
            "iso",
            "audit",
        ]

        found_indicators = sum(
            1
            for indicator in compliance_indicators
            if any(indicator.lower() in path.lower() for path in structure.keys())
        )

        return min(found_indicators / 2.0, 1.0)

    def _check_cicd(self, structure: dict[str, str]) -> float:
        """Check CI/CD pipelines.

        Args:
            structure: Template structure

        Returns:
            Score (0-1)
        """
        cicd_indicators = [
            ".github/workflows",
            ".gitlab-ci",
            "jenkins",
            "ci",
            "cd",
            "pipeline",
            "deploy",
        ]

        found_indicators = sum(
            1
            for indicator in cicd_indicators
            if any(indicator.lower() in path.lower() for path in structure.keys())
        )

        return min(found_indicators / 2.0, 1.0)

    def _check_testing(self, structure: dict[str, str]) -> float:
        """Check testing setup.

        Args:
            structure: Template structure

        Returns:
            Score (0-1)
        """
        testing_indicators = [
            "test",
            "spec",
            "validate",
            "verify",
        ]

        found_indicators = sum(
            1
            for indicator in testing_indicators
            if any(indicator.lower() in path.lower() for path in structure.keys())
        )

        return min(found_indicators / 2.0, 1.0)

    def _generate_recommendations(self, checks: dict[str, float]) -> list[str]:
        """Generate recommendations based on validation checks.

        Args:
            checks: Validation checks dictionary

        Returns:
            List of recommendations
        """
        recommendations = []

        if checks["security"] < 0.5:
            recommendations.append("Add RBAC configurations and network policies")

        if checks["monitoring"] < 0.5:
            recommendations.append("Add monitoring configurations (Prometheus, Grafana)")

        if checks["compliance"] < 0.5:
            recommendations.append("Add compliance configurations (PCI-DSS, SOC2)")

        if checks["ci_cd"] < 0.5:
            recommendations.append("Add CI/CD pipeline configurations")

        if checks["testing"] < 0.5:
            recommendations.append("Add testing configurations")

        return recommendations

