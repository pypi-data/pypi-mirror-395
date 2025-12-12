"""Pattern validation service for validating infrastructure integration patterns.

Validates patterns against WISTX quality standards using TemplateValidationService methodology.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class PatternValidationService:
    """Service for validating infrastructure integration patterns against WISTX standards."""

    VALIDATION_THRESHOLD = 70.0

    async def validate_pattern(self, pattern: dict[str, Any]) -> dict[str, Any]:
        """Validate pattern meets WISTX standards.

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
            Validation result dictionary with:
            - valid: Whether pattern is valid (score >= 70.0)
            - score: Validation score (0-100)
            - checks: Dictionary of individual check scores
            - recommendations: List of improvement recommendations
        """
        checks = {
            "structure_complete": self._check_pattern_structure(pattern),
            "security": self._check_pattern_security(pattern),
            "monitoring": self._check_pattern_monitoring(pattern),
            "documentation": self._check_pattern_documentation(pattern),
            "compliance": self._check_pattern_compliance(pattern),
            "implementation": self._check_implementation_guidance(pattern),
        }

        score = sum(checks.values()) / len(checks) * 100

        return {
            "valid": score >= self.VALIDATION_THRESHOLD,
            "score": round(score, 2),
            "checks": {k: round(v * 100, 2) for k, v in checks.items()},
            "recommendations": self._generate_recommendations(checks),
        }

    def _check_pattern_structure(self, pattern: dict[str, Any]) -> float:
        """Check pattern has required components.

        Args:
            pattern: Pattern dictionary

        Returns:
            Score (0-1.0)
        """
        required_fields = [
            "description",
            "providers",
            "components",
        ]
        has_required = sum(1 for field in required_fields if pattern.get(field))

        has_example = bool(pattern.get("terraform_example") or pattern.get("kubernetes_example"))

        return min((has_required + (1.0 if has_example else 0.0)) / (len(required_fields) + 1), 1.0)

    def _check_pattern_security(self, pattern: dict[str, Any]) -> float:
        """Check security best practices.

        Args:
            pattern: Pattern dictionary

        Returns:
            Score (0-1.0)
        """
        security_rules = pattern.get("security_rules", [])
        if not security_rules:
            return 0.0

        score = 0.0

        if len(security_rules) >= 3:
            score += 0.3
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
            "authentication",
            "authorization",
        ]
        rules_text = " ".join(security_rules).lower()
        found_keywords = sum(1 for kw in security_keywords if kw in rules_text)
        score += min(found_keywords / 5.0, 0.5)

        return min(score, 1.0)

    def _check_pattern_monitoring(self, pattern: dict[str, Any]) -> float:
        """Check monitoring configuration.

        Args:
            pattern: Pattern dictionary

        Returns:
            Score (0-1.0)
        """
        monitoring_config = pattern.get("monitoring_config", {})
        if not monitoring_config:
            return 0.0

        if not isinstance(monitoring_config, dict):
            return 0.0

        score = 0.0

        if monitoring_config.get("metrics"):
            score += 0.4
            if len(monitoring_config["metrics"]) >= 3:
                score += 0.1

        if monitoring_config.get("alarms"):
            score += 0.3
            if len(monitoring_config["alarms"]) >= 2:
                score += 0.1

        if monitoring_config.get("logs"):
            score += 0.1

        return min(score, 1.0)

    def _check_pattern_documentation(self, pattern: dict[str, Any]) -> float:
        """Check documentation quality.

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
            if len(implementation_guidance) >= 5:
                score += 0.1

        return min(score, 1.0)

    def _check_pattern_compliance(self, pattern: dict[str, Any]) -> float:
        """Check compliance considerations.

        Args:
            pattern: Pattern dictionary

        Returns:
            Score (0-1.0)
        """
        compliance_considerations = pattern.get("compliance_considerations", [])
        if not compliance_considerations:
            return 0.0

        score = 0.0

        if len(compliance_considerations) >= 2:
            score += 0.5
        if len(compliance_considerations) >= 4:
            score += 0.3

        compliance_keywords = [
            "pci-dss",
            "hipaa",
            "soc2",
            "nist",
            "gdpr",
            "iso",
            "fedramp",
        ]
        considerations_text = " ".join(compliance_considerations).lower()
        found_keywords = sum(1 for kw in compliance_keywords if kw in considerations_text)
        score += min(found_keywords / 3.0, 0.2)

        return min(score, 1.0)

    def _check_implementation_guidance(self, pattern: dict[str, Any]) -> float:
        """Check implementation guidance quality.

        Args:
            pattern: Pattern dictionary

        Returns:
            Score (0-1.0)
        """
        implementation_guidance = pattern.get("implementation_guidance", [])
        if not implementation_guidance:
            return 0.0

        score = 0.0

        if len(implementation_guidance) >= 3:
            score += 0.4
        if len(implementation_guidance) >= 5:
            score += 0.3
        if len(implementation_guidance) >= 7:
            score += 0.3

        return min(score, 1.0)

    def _generate_recommendations(self, checks: dict[str, float]) -> list[str]:
        """Generate recommendations based on validation checks.

        Args:
            checks: Validation checks dictionary

        Returns:
            List of recommendations
        """
        recommendations = []

        if checks["structure_complete"] < 0.7:
            recommendations.append("Add required fields: description, providers, components, code examples")

        if checks["security"] < 0.7:
            recommendations.append("Add security rules (at least 5 rules covering encryption, access control, audit)")

        if checks["monitoring"] < 0.7:
            recommendations.append("Add monitoring configuration with metrics, alarms, and logs")

        if checks["documentation"] < 0.7:
            recommendations.append("Improve documentation: expand description (> 200 chars) and add implementation guidance")

        if checks["compliance"] < 0.7:
            recommendations.append("Add compliance considerations (at least 2 standards: PCI-DSS, HIPAA, SOC2, NIST)")

        if checks["implementation"] < 0.7:
            recommendations.append("Add detailed implementation guidance (at least 5 steps)")

        return recommendations

