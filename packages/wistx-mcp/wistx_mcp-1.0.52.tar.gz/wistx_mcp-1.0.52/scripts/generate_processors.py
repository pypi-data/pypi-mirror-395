#!/usr/bin/env python3
"""Generate domain knowledge processors from template."""

domains_config = [
    {
        "key": "devops",
        "name": "DevOps",
        "enum": "DEVOPS",
        "subdomains": ["ci-cd", "deployment", "monitoring", "logging", "infrastructure-as-code", "containerization"],
        "structured_fields": ["tool", "pipeline_stage", "automation_level"],
    },
    {
        "key": "security",
        "name": "Security",
        "enum": "SECURITY",
        "subdomains": ["vulnerability-management", "threat-detection", "access-control", "encryption", "security-practices", "incident-response"],
        "structured_fields": ["threat_type", "security_level", "mitigation_strategy"],
    },
    {
        "key": "infrastructure",
        "name": "Infrastructure",
        "enum": "INFRASTRUCTURE",
        "subdomains": ["networking", "compute", "storage", "scalability", "reliability", "performance"],
        "structured_fields": ["infrastructure_type", "scalability_pattern", "reliability_pattern"],
    },
    {
        "key": "architecture",
        "name": "Architecture",
        "enum": "ARCHITECTURE",
        "subdomains": ["microservices", "serverless", "event-driven", "distributed-systems", "design-patterns", "scalability"],
        "structured_fields": ["architecture_pattern", "design_principle", "scalability_approach"],
    },
    {
        "key": "cloud",
        "name": "Cloud",
        "enum": "CLOUD",
        "subdomains": ["multi-cloud", "hybrid-cloud", "cloud-migration", "cloud-native", "cloud-strategy", "cloud-adoption"],
        "structured_fields": ["cloud_strategy", "migration_approach", "adoption_stage"],
    },
    {
        "key": "automation",
        "name": "Automation",
        "enum": "AUTOMATION",
        "subdomains": ["infrastructure-automation", "ci-cd-automation", "deployment-automation", "testing-automation", "monitoring-automation"],
        "structured_fields": ["automation_type", "tool_category", "automation_level"],
    },
]

template = '''"""{name} knowledge processor - processes {name} guides and articles."""

import re
from typing import Any

from ..models.knowledge_article import ContentType, Domain, KnowledgeArticle, Reference
from ..processors.base_knowledge_processor import BaseKnowledgeProcessor
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class {class_name}KnowledgeProcessor(BaseKnowledgeProcessor):
    """Process {name} knowledge articles."""

    def __init__(self, save_intermediate: bool = False):
        """Initialize {name} knowledge processor.

        Args:
            save_intermediate: If True, save intermediate files
        """
        super().__init__(domain="{domain_key}", save_intermediate=save_intermediate)

    def process_raw_data(self, raw_data: dict[str, Any]) -> KnowledgeArticle:
        """Process raw data into KnowledgeArticle.

        Args:
            raw_data: Raw data from collector

        Returns:
            Processed KnowledgeArticle

        Raises:
            ValueError: If article fails validation
        """
        source_url = raw_data.get("source_url", "")
        title = raw_data.get("title", "").strip()
        content = raw_data.get("content", "").strip()
        summary = raw_data.get("summary", "").strip()

        if not title or len(title) < 10:
            title = self._extract_title_from_content(content)
            if len(title) < 10:
                title = f"{name} Guide: {{title}}"

        if not summary or len(summary) < 50:
            summary = self._extract_summary_from_content(content)
            if len(summary) < 50:
                summary = content[:500] if content else "No summary available"

        if len(summary) > 500:
            summary = summary[:497] + "..."

        if len(content) < 100:
            raise ValueError(f"Content too short: {{len(content)}} characters (minimum: 100)")

        subdomain = self._extract_subdomain(raw_data, source_url)
        content_type = self._infer_content_type(raw_data, content)
        article_id = self.generate_article_id(title, self.domain, subdomain, content_type.value)

        structured_data = self.extract_structured_data(raw_data)
        tags = raw_data.get("tags", []) or []
        if not tags:
            tags = self.extract_tags(content, title)

        categories = raw_data.get("categories", []) or []
        industries = raw_data.get("industries", []) or []
        cloud_providers = raw_data.get("cloud_providers", []) or []
        if not cloud_providers:
            cloud_providers = self._infer_cloud_providers(content, title)

        services = raw_data.get("services", []) or []
        if not services:
            services = self._infer_services(content, title)

        cost_impact = raw_data.get("cost_impact") or self._infer_cost_impact(content, title)
        compliance_impact = raw_data.get("compliance_impact") or self._infer_compliance_impact(content, title)
        security_impact = raw_data.get("security_impact") or self._infer_security_impact(content, title)

        references = self._extract_references(raw_data, source_url)
        content_hash = self._generate_content_hash(content)
        source_hash = self._generate_source_hash(source_url, raw_data)

        article = KnowledgeArticle(
            article_id=article_id,
            domain=Domain.{enum},
            subdomain=subdomain,
            content_type=content_type,
            title=title,
            summary=summary,
            content=content,
            structured_data=structured_data,
            tags=tags,
            categories=categories,
            industries=industries,
            cloud_providers=cloud_providers,
            services=services,
            compliance_impact=compliance_impact,
            cost_impact=cost_impact,
            security_impact=security_impact,
            source_url=source_url,
            references=references,
            version=raw_data.get("version", "1.0"),
            content_hash=content_hash,
            source_hash=source_hash,
        )

        return article

    def extract_structured_data(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Extract {name}-specific structured data.

        Args:
            raw_data: Raw data

        Returns:
            Structured data dictionary
        """
        structured = raw_data.get("structured_data", {{}}) or {{}}

        domain_data = {{
{structured_fields}
        }}

        return {{k: v for k, v in domain_data.items() if v}}

    def _extract_subdomain(self, raw_data: dict[str, Any], source_url: str) -> str:
        """Extract {name} subdomain from raw data or URL.

        Args:
            raw_data: Raw data
            source_url: Source URL

        Returns:
            Subdomain string
        """
        subdomain = raw_data.get("subdomain") or "general"

        domain_subdomains = {subdomains_list}

        text = f"{{raw_data.get('title', '')}} {{raw_data.get('content', '')}}".lower()

        for domain in domain_subdomains:
            if domain.replace("-", " ") in text or domain in source_url.lower():
                return domain

        return subdomain

    def _infer_content_type(self, raw_data: dict[str, Any], content: str) -> ContentType:
        """Infer content type from raw data and content.

        Args:
            raw_data: Raw data
            content: Article content

        Returns:
            ContentType enum value
        """
        content_type_str = raw_data.get("content_type", "").lower()
        if content_type_str in ["guide", "pattern", "strategy", "checklist", "reference", "best_practice"]:
            return ContentType(content_type_str)

        text = content.lower()
        if "checklist" in text or "steps" in text[:500]:
            return ContentType.CHECKLIST
        if "pattern" in text or "architecture pattern" in text:
            return ContentType.PATTERN
        if "strategy" in text or "approach" in text:
            return ContentType.STRATEGY
        if "best practice" in text or "recommendation" in text:
            return ContentType.BEST_PRACTICE

        return ContentType.GUIDE

    def _extract_title_from_content(self, content: str) -> str:
        """Extract title from content.

        Args:
            content: Article content

        Returns:
            Extracted title
        """
        lines = content.split("\\n")[:5]
        for line in lines:
            if line.strip() and len(line.strip()) > 10:
                return line.strip()[:200]
        return "{name} Article"

    def _extract_summary_from_content(self, content: str) -> str:
        """Extract summary from content.

        Args:
            content: Article content

        Returns:
            Extracted summary
        """
        if len(content) < 200:
            return content

        sentences = content.split(".")[:3]
        summary = ". ".join(s.strip() for s in sentences if s.strip())
        return summary[:500] if summary else content[:500]

    def _infer_cloud_providers(self, content: str, title: str) -> list[str]:
        """Infer cloud providers from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            List of cloud provider names
        """
        text = f"{{title}} {{content}}".lower()
        providers = set()

        if re.search(r"\\baws\\b|\\bec2\\b|\\bs3\\b|\\brds\\b", text):
            providers.add("aws")
        if re.search(r"\\bgcp\\b|google cloud", text):
            providers.add("gcp")
        if re.search(r"\\bazure\\b|microsoft azure", text):
            providers.add("azure")

        return sorted(list(providers)) if providers else ["multi-cloud"]

    def _infer_services(self, content: str, title: str) -> list[str]:
        """Infer cloud services from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            List of service names
        """
        text = f"{{title}} {{content}}".lower()
        services = set()

        service_patterns = [
            (r"\\brds\\b", "rds"),
            (r"\\bec2\\b", "ec2"),
            (r"\\bs3\\b", "s3"),
            (r"\\blambda\\b", "lambda"),
            (r"\\bcloud storage\\b", "cloud-storage"),
            (r"\\bcloud sql\\b", "cloud-sql"),
            (r"\\bblob storage\\b", "blob-storage"),
        ]

        for pattern, service in service_patterns:
            if re.search(pattern, text):
                services.add(service)

        return sorted(list(services))

    def _infer_cost_impact(self, content: str, title: str) -> dict[str, Any] | None:
        """Infer cost impact from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            Cost impact dictionary or None
        """
        return None

    def _infer_compliance_impact(self, content: str, title: str) -> dict[str, Any] | None:
        """Infer compliance impact from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            Compliance impact dictionary or None
        """
        return None

    def _infer_security_impact(self, content: str, title: str) -> dict[str, Any] | None:
        """Infer security impact from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            Security impact dictionary or None
        """
        return None

    def _extract_references(self, raw_data: dict[str, Any], source_url: str) -> list[Reference]:
        """Extract references from raw data.

        Args:
            raw_data: Raw data
            source_url: Source URL

        Returns:
            List of Reference objects
        """
        references = []
        refs = raw_data.get("references", []) or []

        for ref in refs:
            if isinstance(ref, dict):
                references.append(
                    Reference(
                        type=ref.get("type", "external"),
                        url=ref.get("url", ""),
                        title=ref.get("title", ""),
                    )
                )

        if source_url and not any(r.url == source_url for r in references):
            references.append(Reference(type="source", url=source_url, title="Source"))

        return references

    def _generate_content_hash(self, content: str) -> str:
        """Generate content hash.

        Args:
            content: Article content

        Returns:
            SHA-256 hash string
        """
        import hashlib

        return hashlib.sha256(content.encode()).hexdigest()

    def _generate_source_hash(self, source_url: str, raw_data: dict[str, Any]) -> str:
        """Generate source hash.

        Args:
            source_url: Source URL
            raw_data: Raw data

        Returns:
            SHA-256 hash string
        """
        import hashlib

        source_data = f"{{source_url}}{{raw_data.get('title', '')}}"
        return hashlib.sha256(source_data.encode()).hexdigest()
'''

for config in domains_config:
    class_name = config["name"].replace(" ", "")
    domain_key = config["key"]
    enum = config["enum"]
    name = config["name"]
    
    structured_fields = ",\n".join(
        f'            "{field}": structured.get("{field}", "")'
        for field in config["structured_fields"]
    )
    
    subdomains_list = "[\n            " + ",\n            ".join(f'"{s}"' for s in config["subdomains"]) + ",\n        ]"
    
    content = template.format(
        class_name=class_name,
        domain_key=domain_key,
        enum=enum,
        name=name,
        structured_fields=structured_fields,
        subdomains_list=subdomains_list,
    )
    
    filename = f"data_pipelines/processors/{domain_key}_knowledge_processor.py"
    with open(filename, "w") as f:
        f.write(content)
    print(f"Created {filename}")

