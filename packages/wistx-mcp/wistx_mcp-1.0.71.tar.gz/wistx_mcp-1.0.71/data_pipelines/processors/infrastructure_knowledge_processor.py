"""Infrastructure knowledge processor - processes Infrastructure guides and articles."""

import re
from typing import Any

from ..models.knowledge_article import ContentType, Domain, KnowledgeArticle, Reference
from ..processors.base_knowledge_processor import BaseKnowledgeProcessor
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class InfrastructureKnowledgeProcessor(BaseKnowledgeProcessor):
    """Process Infrastructure knowledge articles."""

    def __init__(self, save_intermediate: bool = False):
        """Initialize Infrastructure knowledge processor.

        Args:
            save_intermediate: If True, save intermediate files
        """
        super().__init__(domain="infrastructure", save_intermediate=save_intermediate)

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
                title = f"Infrastructure Guide: {title}"

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
            domain=Domain.INFRASTRUCTURE,
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
        """Extract Infrastructure-specific structured data.

        Args:
            raw_data: Raw data

        Returns:
            Structured data dictionary
        """
        structured = raw_data.get("structured_data", {}) or {}
        content = raw_data.get("content", "").lower()
        title = raw_data.get("title", "").lower()

        domain_data: dict[str, Any] = {}

        infrastructure_type = structured.get("infrastructure_type") or ""
        if not infrastructure_type:
            infrastructure_type = self._infer_infrastructure_type(content, title)
        if infrastructure_type:
            domain_data["infrastructure_type"] = infrastructure_type

        scalability_pattern = structured.get("scalability_pattern") or ""
        if not scalability_pattern:
            scalability_pattern = self._infer_scalability_pattern(content, title)
        if scalability_pattern:
            domain_data["scalability_pattern"] = scalability_pattern

        reliability_pattern = structured.get("reliability_pattern") or ""
        if not reliability_pattern:
            reliability_pattern = self._infer_reliability_pattern(content, title)
        if reliability_pattern:
            domain_data["reliability_pattern"] = reliability_pattern

        return domain_data

    def _extract_subdomain(self, raw_data: dict[str, Any], source_url: str) -> str:
        """Extract Infrastructure subdomain from raw data or URL.

        Args:
            raw_data: Raw data
            source_url: Source URL

        Returns:
            Subdomain string
        """
        subdomain = raw_data.get("subdomain") or "general"

        infrastructure_subdomains = [
            ("networking", ["network", "networking", "vpc", "subnet", "routing", "load balancer", "cdn"]),
            ("compute", ["compute", "instance", "vm", "server", "ec2", "compute engine", "virtual machine"]),
            ("storage", ["storage", "s3", "blob", "disk", "volume", "file storage", "object storage"]),
            ("database", ["database", "rds", "sql", "nosql", "dynamodb", "database service"]),
            ("scalability", ["scalability", "scale", "scaling", "auto-scaling", "horizontal scaling", "vertical scaling"]),
            ("reliability", ["reliability", "availability", "high availability", "ha", "redundancy", "failover"]),
            ("performance", ["performance", "optimization", "latency", "throughput", "speed"]),
            ("monitoring", ["monitoring", "observability", "metrics", "logging", "alerting"]),
            ("disaster-recovery", ["disaster recovery", "backup", "recovery", "dr", "business continuity"]),
        ]

        text = f"{raw_data.get('title', '')} {raw_data.get('content', '')}".lower()
        url_lower = source_url.lower()

        for domain_key, keywords in infrastructure_subdomains:
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
        return "Infrastructure Article"

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
                r"\beks\b",
                r"\becs\b",
            ],
            "gcp": [
                r"\bgcp\b",
                r"google cloud",
                r"google cloud platform",
                r"\bgke\b",
                r"cloud storage",
                r"cloud sql",
                r"cloud functions",
                r"compute engine",
                r"cloud run",
            ],
            "azure": [
                r"\bazure\b",
                r"microsoft azure",
                r"azure\s+cloud",
                r"\baks\b",
                r"blob storage",
                r"azure sql",
                r"azure functions",
                r"virtual machines",
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

        if not providers and ("cloud" in text or "infrastructure" in text):
            providers.add("multi-cloud")

        return sorted(list(providers)) if providers else ["multi-cloud"]

    def _infer_services(self, content: str, title: str, cloud_providers: list[str] | None = None) -> list[str]:
        """Infer infrastructure services from content.

        Infers compute, storage, networking, and database services.

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
            "ec2": [r"\bec2\b", r"elastic compute cloud", r"amazon ec2"],
            "lambda": [r"\blambda\b", r"aws lambda", r"serverless function"],
            "ecs": [r"\becs\b", r"elastic container service"],
            "eks": [r"\beks\b", r"elastic kubernetes service"],
            "fargate": [r"\bfargate\b"],
            "s3": [r"\bs3\b", r"simple storage service", r"amazon s3"],
            "ebs": [r"\bebs\b", r"elastic block store"],
            "efs": [r"\befs\b", r"elastic file system"],
            "rds": [r"\brds\b", r"amazon rds", r"relational database service"],
            "dynamodb": [r"\bdynamodb\b"],
            "vpc": [r"\bvpc\b", r"virtual private cloud"],
            "cloudfront": [r"\bcloudfront\b"],
            "route53": [r"\broute53\b"],
            "elb": [r"\belb\b", r"elastic load balancing", r"load balancer"],
            "cloud-storage": [r"cloud storage", r"google cloud storage"],
            "compute-engine": [r"compute engine", r"gce"],
            "cloud-sql": [r"cloud sql", r"google cloud sql"],
            "cloud-functions": [r"cloud functions", r"google cloud functions"],
            "cloud-run": [r"cloud run"],
            "gke": [r"\bgke\b", r"google kubernetes engine"],
            "blob-storage": [r"blob storage", r"azure blob"],
            "azure-sql": [r"azure sql"],
            "azure-functions": [r"azure functions"],
            "azure-vm": [r"azure virtual machine", r"azure vm"],
            "aks": [r"\baks\b", r"azure kubernetes service"],
            "kubernetes": [r"\bkubernetes\b", r"\bk8s\b"],
            "terraform": [r"\bterraform\b"],
            "cloudformation": [r"\bcloudformation\b"],
            "pulumi": [r"\bpulumi\b"],
        }

        for service_name, patterns in service_patterns.items():
            if any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns):
                services.add(service_name)

        if not services:
            if "compute" in text or "instance" in text or "vm" in text:
                services.add("compute")
            if "storage" in text or "data storage" in text:
                services.add("storage")
            if "database" in text or "db" in text:
                services.add("database")
            if "network" in text or "networking" in text:
                services.add("networking")
            if "load balancer" in text or "lb" in text:
                services.add("load-balancing")

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
            "savings", "optimization", "reduce cost",
        ]

        if not any(indicator in text for indicator in cost_indicators):
            return None

        optimization_opportunities = []
        if "auto-scaling" in text or "autoscaling" in text:
            optimization_opportunities.append("auto-scaling")
        if "reserved" in text or "spot" in text:
            optimization_opportunities.append("instance-optimization")
        if "serverless" in text or "lambda" in text:
            optimization_opportunities.append("serverless")

        return {
            "optimization_opportunities": optimization_opportunities if optimization_opportunities else None,
            "cost_category": "infrastructure",
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

        if "compliance" not in text and "audit" not in text:
            return None

        return {
            "requirements": ["infrastructure-audit", "resource-tracking"],
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
            "security", "vulnerability", "access control",
            "network security", "firewall",
        ]

        if not any(indicator in text for indicator in security_indicators):
            return None

        threats_mitigated = []
        if "network" in text or "vpc" in text:
            threats_mitigated.append("network-isolation")
        if "access" in text or "iam" in text:
            threats_mitigated.append("access-control")

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
            subdomain: Infrastructure subdomain
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

            infrastructure_keywords = [
                "infrastructure", "compute", "storage", "network",
                "scalability", "reliability", "performance",
            ]

            for keyword in infrastructure_keywords:
                if keyword in text:
                    text_keywords.add(keyword)

            if text_keywords:
                query = {
                    "domain": "infrastructure",
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

    def _infer_infrastructure_type(self, content: str, title: str) -> str:
        """Infer infrastructure type from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            Infrastructure type or empty string
        """
        text = f"{title} {content}".lower()

        if "serverless" in text or "lambda" in text or "function" in text:
            return "serverless"
        if "container" in text or "kubernetes" in text or "docker" in text:
            return "containerized"
        if "virtual machine" in text or "vm" in text or "instance" in text:
            return "virtualized"
        if "bare metal" in text or "bare-metal" in text:
            return "bare-metal"

        return ""

    def _infer_scalability_pattern(self, content: str, title: str) -> str:
        """Infer scalability pattern from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            Scalability pattern or empty string
        """
        text = f"{title} {content}".lower()

        if "horizontal scaling" in text or "scale out" in text:
            return "horizontal"
        if "vertical scaling" in text or "scale up" in text:
            return "vertical"
        if "auto-scaling" in text or "autoscaling" in text:
            return "auto-scaling"
        if "elastic" in text:
            return "elastic"

        return ""

    def _infer_reliability_pattern(self, content: str, title: str) -> str:
        """Infer reliability pattern from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            Reliability pattern or empty string
        """
        text = f"{title} {content}".lower()

        if "high availability" in text or "ha" in text:
            return "high-availability"
        if "redundancy" in text or "redundant" in text:
            return "redundancy"
        if "failover" in text:
            return "failover"
        if "multi-az" in text or "multi-availability-zone" in text:
            return "multi-az"
        if "disaster recovery" in text or "dr" in text:
            return "disaster-recovery"

        return ""
