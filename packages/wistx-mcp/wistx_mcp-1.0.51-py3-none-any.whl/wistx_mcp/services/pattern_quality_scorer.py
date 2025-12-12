"""Pattern quality scorer service for infrastructure integration patterns.

Uses QualityScorer methodology to score patterns across multiple dimensions.
"""

import logging
from typing import Any

from wistx_mcp.models.quality_score import QualityScoreBreakdown, QualityScoreResult

logger = logging.getLogger(__name__)


class PatternQualityScorer:
    """Service for scoring infrastructure integration patterns using quality template methodology."""

    QUALITY_THRESHOLD = 70.0

    def score_pattern(self, pattern: dict[str, Any]) -> QualityScoreResult:
        """Score pattern quality using multi-factor analysis.

        Args:
            pattern: Pattern dictionary with:
                - description: Pattern description
                - providers: List of cloud providers
                - components: List of components
                - terraform_example: Terraform code example (optional)
                - kubernetes_example: Kubernetes code example (optional)
                - dependencies: List of dependencies (optional)
                - security_rules: List of security rules (optional)
                - monitoring_config: Monitoring configuration (optional)
                - implementation_guidance: Implementation guidance (optional)
                - compliance_considerations: Compliance considerations (optional)

        Returns:
            QualityScoreResult with overall score and breakdown
        """
        breakdown = QualityScoreBreakdown()

        breakdown.structure_completeness = self._evaluate_pattern_structure(pattern)
        breakdown.infrastructure_quality = self._evaluate_infrastructure_quality(pattern)
        breakdown.devops_maturity = self._evaluate_devops_maturity(pattern)
        breakdown.documentation_quality = self._evaluate_documentation_quality(pattern)
        breakdown.compliance_security = self._evaluate_compliance_security(pattern)
        breakdown.code_organization = self._evaluate_code_organization(pattern)

        overall_score = (
            breakdown.structure_completeness * 0.25
            + breakdown.infrastructure_quality * 0.20
            + breakdown.devops_maturity * 0.20
            + breakdown.documentation_quality * 0.15
            + breakdown.compliance_security * 0.10
            + breakdown.code_organization * 0.10
        )

        score_dict = {
            "structure_completeness": breakdown.structure_completeness * 100,
            "infrastructure_quality": breakdown.infrastructure_quality * 100,
            "devops_maturity": breakdown.devops_maturity * 100,
            "documentation_quality": breakdown.documentation_quality * 100,
            "compliance_security": breakdown.compliance_security * 100,
            "code_organization": breakdown.code_organization * 100,
        }

        recommendations = self._generate_recommendations(breakdown)

        return QualityScoreResult(
            overall_score=round(overall_score * 100, 2),
            score_breakdown=score_dict,
            recommendations=recommendations,
            metadata={
                "providers": pattern.get("providers", []),
                "components": pattern.get("components", []),
            },
            meets_threshold=overall_score * 100 >= self.QUALITY_THRESHOLD,
        )

    def _evaluate_pattern_structure(self, pattern: dict[str, Any]) -> float:
        """Evaluate pattern structure completeness (0-1.0).

        Checks for required fields: description, providers, components, examples.

        Args:
            pattern: Pattern dictionary

        Returns:
            Score (0-1.0)
        """
        score = 0.0

        if pattern.get("description"):
            score += 0.25

        if pattern.get("providers"):
            score += 0.25

        if pattern.get("components"):
            score += 0.25

        has_example = bool(pattern.get("terraform_example") or pattern.get("kubernetes_example"))
        if has_example:
            score += 0.25

        return min(score, 1.0)

    def _evaluate_infrastructure_quality(self, pattern: dict[str, Any]) -> float:
        """Evaluate infrastructure code quality (0-1.0).

        Checks for Terraform/Kubernetes examples, code completeness, best practices.

        Args:
            pattern: Pattern dictionary

        Returns:
            Score (0-1.0)
        """
        score = 0.0

        terraform_example = pattern.get("terraform_example", "")
        kubernetes_example = pattern.get("kubernetes_example", "")

        if terraform_example:
            score += 0.4
            if len(terraform_example) > 200:
                score += 0.2
            if "resource" in terraform_example.lower():
                score += 0.2
            if "variable" in terraform_example.lower() or "var." in terraform_example:
                score += 0.2

        if kubernetes_example:
            score += 0.4
            if len(kubernetes_example) > 200:
                score += 0.2
            if "apiVersion" in kubernetes_example:
                score += 0.2
            if "kind:" in kubernetes_example.lower():
                score += 0.2

        if not terraform_example and not kubernetes_example:
            return 0.0

        return min(score, 1.0)

    def _evaluate_devops_maturity(self, pattern: dict[str, Any]) -> float:
        """Evaluate DevOps maturity (0-1.0).

        Checks for monitoring config, dependencies, implementation guidance.

        Args:
            pattern: Pattern dictionary

        Returns:
            Score (0-1.0)
        """
        score = 0.0

        monitoring_config = pattern.get("monitoring_config") or pattern.get("monitoring", {})
        if monitoring_config:
            score += 0.4
            if isinstance(monitoring_config, dict):
                if monitoring_config.get("metrics"):
                    score += 0.2
                if monitoring_config.get("alarms"):
                    score += 0.2
                if monitoring_config.get("logs"):
                    score += 0.2

        dependencies = pattern.get("dependencies", [])
        if dependencies:
            score += 0.3

        implementation_guidance = pattern.get("implementation_guidance", [])
        if implementation_guidance:
            score += 0.3

        return min(score, 1.0)

    def _evaluate_documentation_quality(self, pattern: dict[str, Any]) -> float:
        """Evaluate documentation quality (0-1.0).

        Checks for description quality, implementation guidance, examples.

        Args:
            pattern: Pattern dictionary

        Returns:
            Score (0-1.0)
        """
        score = 0.0

        description = pattern.get("description", "")
        if description:
            score += 0.4
            if len(description) > 100:
                score += 0.2
            if len(description) > 200:
                score += 0.2

        implementation_guidance = pattern.get("implementation_guidance", [])
        if implementation_guidance:
            score += 0.2

        return min(score, 1.0)

    def _evaluate_compliance_security(self, pattern: dict[str, Any]) -> float:
        """Evaluate compliance and security (0-1.0).

        Checks for security rules, compliance considerations.

        Args:
            pattern: Pattern dictionary

        Returns:
            Score (0-1.0)
        """
        score = 0.0

        security_rules = pattern.get("security_rules", [])
        if security_rules:
            score += 0.5
            if len(security_rules) >= 3:
                score += 0.2
            if len(security_rules) >= 5:
                score += 0.2

            security_keywords = [
                "encryption",
                "least privilege",
                "iam",
                "secrets",
                "network policy",
                "rbac",
                "audit",
                "tls",
                "ssl",
            ]
            rules_text = " ".join(security_rules).lower()
            found_keywords = sum(1 for kw in security_keywords if kw in rules_text)
            score += min(found_keywords / 5.0, 0.1)

        compliance_considerations = pattern.get("compliance_considerations", [])
        if compliance_considerations:
            score += 0.3

        return min(score, 1.0)

    def _evaluate_code_organization(self, pattern: dict[str, Any]) -> float:
        """Evaluate code organization (0-1.0).

        Checks for component organization, dependencies, structure.

        Args:
            pattern: Pattern dictionary

        Returns:
            Score (0-1.0)
        """
        score = 0.5

        components = pattern.get("components", [])
        if components:
            score += 0.2
            if len(components) >= 2:
                score += 0.2
            if len(components) >= 3:
                score += 0.1

        providers = pattern.get("providers", [])
        if providers:
            score += 0.1

        return min(score, 1.0)

    def _generate_recommendations(self, breakdown: QualityScoreBreakdown) -> list[str]:
        """Generate improvement recommendations based on score breakdown.

        Args:
            breakdown: Quality score breakdown

        Returns:
            List of recommendations
        """
        recommendations = []

        if breakdown.structure_completeness < 0.5:
            recommendations.append("Add required fields: description, providers, components, code examples")

        if breakdown.infrastructure_quality < 0.5:
            recommendations.append("Add Terraform or Kubernetes code examples with best practices")

        if breakdown.devops_maturity < 0.5:
            recommendations.append("Add monitoring configuration, dependencies, and implementation guidance")

        if breakdown.documentation_quality < 0.5:
            recommendations.append("Improve documentation: add detailed description and implementation guidance")

        if breakdown.compliance_security < 0.5:
            recommendations.append("Add security rules and compliance considerations")

        if breakdown.code_organization < 0.5:
            recommendations.append("Improve code organization: add more components and structure")

        return recommendations

