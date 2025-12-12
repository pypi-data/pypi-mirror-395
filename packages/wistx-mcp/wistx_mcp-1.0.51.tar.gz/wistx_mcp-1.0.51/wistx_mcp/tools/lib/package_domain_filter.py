"""Package domain filter - identify DevOps/infrastructure packages."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


DEVOPS_KEYWORDS = [
    "terraform", "ansible", "pulumi", "kubernetes", "docker",
    "ci-cd", "deployment", "automation", "infrastructure",
    "devops", "sre", "observability", "monitoring", "logging",
    "helm", "kubectl", "jenkins", "gitlab", "github",
    "aws", "gcp", "azure", "cloud", "serverless",
    "iac", "infrastructure-as-code", "configuration-management",
]

INFRASTRUCTURE_KEYWORDS = [
    "aws", "gcp", "azure", "cloud", "compute", "storage",
    "networking", "database", "cache", "load-balancer",
    "vpc", "subnet", "security-group", "iam", "s3", "rds",
    "ec2", "eks", "gke", "aks", "lambda", "functions",
]

COMPLIANCE_KEYWORDS = [
    "security", "compliance", "audit", "scan", "check",
    "pci", "hipaa", "soc2", "nist", "cis", "gdpr",
    "vulnerability", "threat", "encryption", "access-control",
]

FINOPS_KEYWORDS = [
    "cost", "pricing", "billing", "budget", "optimization",
    "finops", "cost-management", "resource-optimization",
    "rightsizing", "cost-allocation",
]

PLATFORM_KEYWORDS = [
    "platform", "abstraction", "sdk", "framework", "internal",
    "developer-platform", "crossplane", "backstage",
]

SRE_KEYWORDS = [
    "sre", "reliability", "observability", "monitoring",
    "alerting", "incident", "chaos", "resilience",
    "prometheus", "grafana", "datadog", "newrelic",
]

PACKAGE_CATEGORIES = {
    "infrastructure-as-code": [
        "terraform", "pulumi", "ansible", "cloudformation",
        "cdk", "cdktf", "terragrunt",
    ],
    "cloud-providers": [
        "aws", "gcp", "azure", "oracle", "alibaba",
    ],
    "kubernetes": [
        "kubernetes", "k8s", "helm", "operator", "kubectl",
    ],
    "ci-cd": [
        "jenkins", "gitlab", "github", "circleci", "travis",
        "argo", "tekton", "spinnaker",
    ],
    "monitoring": [
        "prometheus", "grafana", "datadog", "newrelic",
        "sentry", "opentelemetry",
    ],
    "security": [
        "checkov", "tfsec", "terrascan", "bandit", "safety",
        "snyk", "prowler",
    ],
    "cost": [
        "infracost", "cloud-pricing", "cost-optimization",
    ],
}


class PackageDomainFilter:
    """Filter packages by DevOps/infrastructure domain."""

    @staticmethod
    def is_devops_infrastructure_package(package_metadata: dict[str, Any]) -> bool:
        """Check if package is DevOps/infrastructure related.

        Args:
            package_metadata: Package metadata dictionary

        Returns:
            True if package is DevOps/infrastructure related
        """
        name = package_metadata.get("name", "").lower()
        description = package_metadata.get("description", "").lower()
        keywords = package_metadata.get("keywords", [])
        keywords_str = " ".join(keywords).lower() if isinstance(keywords, list) else str(keywords).lower()
        classifiers = package_metadata.get("classifiers", [])
        classifiers_str = " ".join(classifiers).lower() if isinstance(classifiers, list) else ""

        searchable_text = f"{name} {description} {keywords_str} {classifiers_str}".lower()

        all_keywords = (
            DEVOPS_KEYWORDS +
            INFRASTRUCTURE_KEYWORDS +
            COMPLIANCE_KEYWORDS +
            FINOPS_KEYWORDS +
            PLATFORM_KEYWORDS +
            SRE_KEYWORDS
        )

        if any(keyword in searchable_text for keyword in all_keywords):
            return True

        if classifiers:
            for classifier in classifiers:
                classifier_lower = classifier.lower()
                if any(term in classifier_lower for term in ["devops", "infrastructure", "cloud", "automation"]):
                    return True

        return False

    @staticmethod
    def get_domain_tags(package_metadata: dict[str, Any]) -> list[str]:
        """Get domain tags for package.

        Args:
            package_metadata: Package metadata dictionary

        Returns:
            List of domain tags
        """
        tags = []
        name = package_metadata.get("name", "").lower()
        description = package_metadata.get("description", "").lower()
        keywords = package_metadata.get("keywords", [])
        keywords_str = " ".join(keywords).lower() if isinstance(keywords, list) else str(keywords).lower()

        searchable_text = f"{name} {description} {keywords_str}".lower()

        if any(keyword in searchable_text for keyword in DEVOPS_KEYWORDS):
            tags.append("devops")

        if any(keyword in searchable_text for keyword in INFRASTRUCTURE_KEYWORDS):
            tags.append("infrastructure")

        if any(keyword in searchable_text for keyword in COMPLIANCE_KEYWORDS):
            tags.append("compliance")

        if any(keyword in searchable_text for keyword in FINOPS_KEYWORDS):
            tags.append("finops")

        if any(keyword in searchable_text for keyword in PLATFORM_KEYWORDS):
            tags.append("platform")

        if any(keyword in searchable_text for keyword in SRE_KEYWORDS):
            tags.append("sre")

        return list(set(tags)) if tags else ["devops"]

    @staticmethod
    def get_category(package_metadata: dict[str, Any]) -> str | None:
        """Get package category.

        Args:
            package_metadata: Package metadata dictionary

        Returns:
            Category name or None
        """
        name = package_metadata.get("name", "").lower()
        description = package_metadata.get("description", "").lower()
        keywords = package_metadata.get("keywords", [])
        keywords_str = " ".join(keywords).lower() if isinstance(keywords, list) else str(keywords).lower()

        searchable_text = f"{name} {description} {keywords_str}".lower()

        for category, category_keywords in PACKAGE_CATEGORIES.items():
            if any(keyword in searchable_text for keyword in category_keywords):
                return category

        return None

    @staticmethod
    def calculate_relevance_score(package_metadata: dict[str, Any], domain: str | None = None) -> float:
        """Calculate relevance score for package.

        Args:
            package_metadata: Package metadata dictionary
            domain: Optional domain filter

        Returns:
            Relevance score (0.0 to 1.0)
        """
        if not PackageDomainFilter.is_devops_infrastructure_package(package_metadata):
            return 0.0

        score = 0.5

        domain_tags = PackageDomainFilter.get_domain_tags(package_metadata)
        if domain and domain in domain_tags:
            score += 0.3

        category = PackageDomainFilter.get_category(package_metadata)
        if category:
            score += 0.2

        downloads = package_metadata.get("downloads", 0)
        if downloads > 1000000:
            score += 0.1
        elif downloads > 100000:
            score += 0.05

        return min(1.0, score)

