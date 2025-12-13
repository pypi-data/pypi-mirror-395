"""Cloud knowledge processor - processes Cloud guides and articles."""

import re
from typing import Any

from ..models.knowledge_article import ContentType, Domain, KnowledgeArticle, Reference
from ..processors.base_knowledge_processor import BaseKnowledgeProcessor
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class CloudKnowledgeProcessor(BaseKnowledgeProcessor):
    """Process Cloud knowledge articles."""

    def __init__(self, save_intermediate: bool = False):
        """Initialize Cloud knowledge processor.

        Args:
            save_intermediate: If True, save intermediate files
        """
        super().__init__(domain="cloud", save_intermediate=save_intermediate)

    def process_raw_data(self, raw_data: dict[str, Any]) -> KnowledgeArticle:
        """Process raw data into KnowledgeArticle.

        Args:
            raw_data: Raw data from collector

        Returns:
            Processed KnowledgeArticle

        Raises:
            ValueError: If article fails validation
        """
        if not self._filter_low_quality_extractions(raw_data):
            logger.debug(
                "Article filtered out: title='%s', content_length=%d",
                raw_data.get("title", "")[:50],
                len(raw_data.get("content", "")),
            )
            raise ValueError(
                f"Article filtered out: title='{raw_data.get('title', '')[:50]}', "
                f"content_length={len(raw_data.get('content', ''))}"
            )

        source_url = raw_data.get("source_url", "")
        title = raw_data.get("title", "").strip()
        content = raw_data.get("content", "").strip()
        summary = raw_data.get("summary", "").strip()

        if not title or len(title) < 10:
            title = self._extract_title_from_content(content)
            if len(title) < 10:
                title = f"Cloud Guide: {title}"

        if not summary or len(summary) < 50:
            summary = self._extract_summary_from_content(content)
            if len(summary) < 50:
                summary = content[:500] if content else "No summary available"

        if len(summary) > 500:
            summary = summary[:497] + "..."

        if len(content) < 100:
            raise ValueError(f"Content too short: {len(content)} characters (minimum: 100)")

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
            services = self._infer_services(content, title, cloud_providers)

        cost_impact = raw_data.get("cost_impact") or self._infer_cost_impact(content, title)
        compliance_impact = raw_data.get("compliance_impact") or self._infer_compliance_impact(content, title)
        security_impact = raw_data.get("security_impact") or self._infer_security_impact(content, title)

        related_articles = raw_data.get("related_articles", []) or []
        related_code_examples = raw_data.get("related_code_examples", []) or []

        if not related_articles:
            discovered_relations = self._discover_related_items(
                article_id, subdomain, content, title, tags
            )
            related_articles = discovered_relations.get("articles", [])

        references = self._extract_references(raw_data, source_url)
        content_hash = self._generate_content_hash(content)
        source_hash = self._generate_source_hash(source_url, raw_data)

        article = KnowledgeArticle(
            article_id=article_id,
            domain=Domain.CLOUD,
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
            related_articles=related_articles,
            related_code_examples=related_code_examples,
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
        """Extract Cloud-specific structured data.

        Args:
            raw_data: Raw data

        Returns:
            Structured data dictionary
        """
        structured = raw_data.get("structured_data", {}) or {}
        content = raw_data.get("content", "").lower()
        title = raw_data.get("title", "").lower()

        domain_data: dict[str, Any] = {}

        cloud_strategy = structured.get("cloud_strategy") or ""
        if not cloud_strategy:
            cloud_strategy = self._infer_cloud_strategy(content, title)
        if cloud_strategy:
            domain_data["cloud_strategy"] = cloud_strategy

        migration_approach = structured.get("migration_approach") or ""
        if not migration_approach:
            migration_approach = self._infer_migration_approach(content, title)
        if migration_approach:
            domain_data["migration_approach"] = migration_approach

        adoption_stage = structured.get("adoption_stage") or ""
        if not adoption_stage:
            adoption_stage = self._infer_adoption_stage(content, title)
        if adoption_stage:
            domain_data["adoption_stage"] = adoption_stage

        return domain_data

    def _extract_subdomain(self, raw_data: dict[str, Any], source_url: str) -> str:
        """Extract Cloud subdomain from raw data or URL.

        Args:
            raw_data: Raw data
            source_url: Source URL

        Returns:
            Subdomain string
        """
        subdomain = raw_data.get("subdomain") or "general"

        cloud_subdomains = [
            ("multi-cloud", ["multi-cloud", "multi cloud", "multi cloud strategy", "multiple cloud"]),
            ("hybrid-cloud", ["hybrid cloud", "hybrid-cloud", "on-premises", "on-prem", "private cloud"]),
            ("cloud-migration", ["cloud migration", "migration", "migrate to cloud", "lift and shift"]),
            ("cloud-native", ["cloud native", "cloud-native", "cloud native application", "cncf"]),
            ("cloud-strategy", ["cloud strategy", "cloud adoption strategy", "cloud roadmap"]),
            ("cloud-adoption", ["cloud adoption", "adoption", "cloud transformation", "digital transformation"]),
            ("cloud-governance", ["cloud governance", "governance", "cloud management", "cloud policy"]),
            ("cloud-security", ["cloud security", "cloud security best practices", "cloud security strategy"]),
            ("cloud-cost", ["cloud cost", "cloud pricing", "cloud economics", "cloud spend"]),
            ("cloud-operations", ["cloud operations", "cloud ops", "cloud monitoring", "cloud management"]),
        ]

        text = f"{raw_data.get('title', '')} {raw_data.get('content', '')}".lower()
        url_lower = source_url.lower()

        for domain_key, keywords in cloud_subdomains:
            if any(keyword in text for keyword in keywords) or domain_key in url_lower:
                return domain_key

        return subdomain.lower().replace("_", "-")

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
        lines = content.split("\n")[:5]
        for line in lines:
            if line.strip() and len(line.strip()) > 10:
                return line.strip()[:200]
        return "Cloud Article"

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

        Supports all major cloud providers, not just AWS/GCP/Azure.

        Args:
            content: Article content
            title: Article title

        Returns:
            List of cloud provider names (lowercase, standardized)
        """
        text = f"{title} {content}".lower()
        providers = set()

        provider_patterns = {
            "aws": [
                r"\baws\b",
                r"amazon web services",
                r"amazon\s+cloud",
                r"\bec2\b",
                r"\bs3\b",
                r"\brds\b",
                r"\blambda\b",
                r"\bvpc\b",
                r"\biam\b",
                r"cloudformation\b",
            ],
            "gcp": [
                r"\bgcp\b",
                r"google cloud",
                r"google cloud platform",
                r"\bgke\b",
                r"cloud storage",
                r"cloud sql",
                r"cloud functions",
            ],
            "azure": [
                r"\bazure\b",
                r"microsoft azure",
                r"azure\s+cloud",
                r"\baks\b",
                r"blob storage",
                r"azure sql",
                r"azure functions",
            ],
            "oracle": [
                r"\boracle cloud\b",
                r"oracle cloud infrastructure",
                r"\boci\b",
            ],
            "ibm": [
                r"\bibm cloud\b",
                r"ibm cloud platform",
            ],
            "alibaba": [
                r"\balibaba cloud\b",
                r"aliyun",
            ],
        }

        for provider_name, patterns in provider_patterns.items():
            if any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns):
                providers.add(provider_name)

        if not providers and ("cloud" in text or "migration" in text or "adoption" in text):
            providers.add("multi-cloud")

        return sorted(list(providers)) if providers else ["multi-cloud"]

    def _infer_services(self, content: str, title: str, cloud_providers: list[str] | None = None) -> list[str]:
        """Infer cloud services from content.

        Infers services from all major cloud providers.

        Args:
            content: Article content
            title: Article title
            cloud_providers: List of detected cloud providers

        Returns:
            List of service names
        """
        text = f"{title} {content}".lower()
        services = set()

        service_patterns = {
            "ec2": [r"\bec2\b", r"elastic compute cloud"],
            "s3": [r"\bs3\b", r"simple storage service"],
            "rds": [r"\brds\b", r"amazon rds"],
            "lambda": [r"\blambda\b", r"aws lambda"],
            "vpc": [r"\bvpc\b", r"virtual private cloud"],
            "iam": [r"\biam\b", r"identity and access management"],
            "cloud-storage": [r"cloud storage", r"google cloud storage"],
            "cloud-sql": [r"cloud sql", r"google cloud sql"],
            "cloud-functions": [r"cloud functions", r"google cloud functions"],
            "compute-engine": [r"compute engine", r"gce"],
            "blob-storage": [r"blob storage", r"azure blob"],
            "azure-sql": [r"azure sql"],
            "azure-functions": [r"azure functions"],
            "azure-vm": [r"azure virtual machine", r"azure vm"],
            "kubernetes": [r"\bkubernetes\b", r"\bk8s\b"],
            "eks": [r"\beks\b"],
            "gke": [r"\bgke\b"],
            "aks": [r"\baks\b"],
        }

        for service_name, patterns in service_patterns.items():
            if any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns):
                services.add(service_name)

        if not services:
            if "compute" in text or "instance" in text:
                services.add("compute")
            if "storage" in text:
                services.add("storage")
            if "database" in text:
                services.add("database")
            if "network" in text:
                services.add("networking")

        return sorted(list(services))

    def _infer_cost_impact(self, content: str, title: str) -> dict[str, Any] | None:
        """Infer cost impact from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            Cost impact dictionary or None
        """
        text = f"{title} {content}".lower()

        cost_indicators = [
            "cost", "pricing", "expensive", "cheap", "budget",
            "savings", "optimization", "reduce cost", "tco",
        ]

        if not any(indicator in text for indicator in cost_indicators):
            return None

        optimization_opportunities = []
        if "migration" in text:
            optimization_opportunities.append("migration-cost")
        if "multi-cloud" in text:
            optimization_opportunities.append("multi-cloud-optimization")

        return {
            "optimization_opportunities": optimization_opportunities if optimization_opportunities else None,
            "cost_category": "cloud-adoption",
        }

    def _infer_compliance_impact(self, content: str, title: str) -> dict[str, Any] | None:
        """Infer compliance impact from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            Compliance impact dictionary or None
        """
        text = f"{title} {content}".lower()

        if "compliance" not in text and "regulation" not in text:
            return None

        return {
            "requirements": ["cloud-compliance", "data-residency"],
            "severity": "medium",
        }

    def _infer_security_impact(self, content: str, title: str) -> dict[str, Any] | None:
        """Infer security impact from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            Security impact dictionary or None
        """
        text = f"{title} {content}".lower()

        security_indicators = [
            "security", "secure", "encryption", "access control",
            "cloud security", "shared responsibility",
        ]

        if not any(indicator in text for indicator in security_indicators):
            return None

        threats_mitigated = []
        if "encryption" in text:
            threats_mitigated.append("data-exposure")
        if "access" in text or "iam" in text:
            threats_mitigated.append("unauthorized-access")

        return {
            "threats_mitigated": threats_mitigated if threats_mitigated else ["security-improvement"],
            "security_level": "medium",
        }

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

        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _generate_source_hash(self, source_url: str, raw_data: dict[str, Any]) -> str:
        """Generate source hash.

        Args:
            source_url: Source URL
            raw_data: Raw data

        Returns:
            SHA-256 hash string
        """
        import hashlib

        source_data = f"{source_url}:{raw_data.get('title', '')}:{raw_data.get('version', '1.0')}"
        return hashlib.sha256(source_data.encode("utf-8")).hexdigest()

    def _filter_low_quality_extractions(self, raw_data: dict[str, Any]) -> bool:
        """Filter out low-quality LLM extractions.

        Args:
            raw_data: Raw article data from LLM extraction

        Returns:
            True if article should be processed, False if filtered out
        """
        title = raw_data.get("title", "").strip()
        content = raw_data.get("content", "").strip()

        if not title or len(title) < 10:
            return False

        if not content or len(content) < 200:
            return False

        if content.startswith("[") and "](http" in content and len(content) < 150:
            return False

        if "\n" not in content and len(content) < 300:
            return False

        link_only_pattern = r"^\[.*?\]\(https?://.*?\)\s*$"
        if re.match(link_only_pattern, content.strip(), re.MULTILINE):
            return False

        return True

    def _discover_related_items(
        self,
        article_id: str,
        subdomain: str,
        content: str,
        title: str,
        tags: list[str],
    ) -> dict[str, list[str]]:
        """Discover related articles based on content similarity.

        Uses keyword matching and subdomain matching to find related items.

        Args:
            article_id: Current article ID
            subdomain: Cloud subdomain
            content: Article content
            title: Article title
            tags: Article tags

        Returns:
            Dictionary with "articles" list
        """
        related_articles: list[str] = []

        try:
            from api.database.mongodb import mongodb_manager

            mongodb_manager.connect()
            db = mongodb_manager.get_database()

            text_keywords = set()
            text = f"{title} {content}".lower()

            cloud_keywords = [
                "cloud", "migration", "adoption", "multi-cloud",
                "hybrid cloud", "cloud native", "strategy",
            ]

            for keyword in cloud_keywords:
                if keyword in text:
                    text_keywords.add(keyword)

            if text_keywords:
                query = {
                    "domain": "cloud",
                    "$or": [
                        {"subdomain": subdomain},
                        {"tags": {"$in": list(text_keywords)}},
                    ],
                    "article_id": {"$ne": article_id},
                }

                related = db.knowledge_articles.find(query).limit(5)
                for doc in related:
                    related_articles.append(doc.get("article_id", ""))

        except Exception as e:
            logger.debug("Error discovering related items: %s", e)

        return {"articles": related_articles}

    def _infer_cloud_strategy(self, content: str, title: str) -> str:
        """Infer cloud strategy from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            Cloud strategy or empty string
        """
        text = f"{title} {content}".lower()

        if "multi-cloud" in text:
            return "multi-cloud"
        if "hybrid cloud" in text or "hybrid-cloud" in text:
            return "hybrid-cloud"
        if "single cloud" in text or "single-cloud" in text:
            return "single-cloud"
        if "cloud native" in text or "cloud-native" in text:
            return "cloud-native"

        return ""

    def _infer_migration_approach(self, content: str, title: str) -> str:
        """Infer migration approach from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            Migration approach or empty string
        """
        text = f"{title} {content}".lower()

        if "lift and shift" in text or "rehost" in text:
            return "lift-and-shift"
        if "refactor" in text or "replatform" in text:
            return "refactor"
        if "rearchitect" in text or "rebuild" in text:
            return "rearchitect"
        if "repurchase" in text or "replace" in text:
            return "repurchase"
        if "retire" in text or "retain" in text:
            return "retire"

        return ""

    def _infer_adoption_stage(self, content: str, title: str) -> str:
        """Infer adoption stage from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            Adoption stage or empty string
        """
        text = f"{title} {content}".lower()

        if "planning" in text or "plan" in text:
            return "planning"
        if "pilot" in text or "proof of concept" in text or "poc" in text:
            return "pilot"
        if "migration" in text or "migrating" in text:
            return "migration"
        if "optimization" in text or "optimize" in text:
            return "optimization"
        if "mature" in text or "maturity" in text:
            return "mature"

        return ""
