"""Architecture knowledge processor - processes Architecture guides and articles."""

import re
from typing import Any

from ..models.knowledge_article import ContentType, Domain, KnowledgeArticle, Reference
from ..processors.base_knowledge_processor import BaseKnowledgeProcessor
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class ArchitectureKnowledgeProcessor(BaseKnowledgeProcessor):
    """Process Architecture knowledge articles."""

    def __init__(self, save_intermediate: bool = False):
        """Initialize Architecture knowledge processor.

        Args:
            save_intermediate: If True, save intermediate files
        """
        super().__init__(domain="architecture", save_intermediate=save_intermediate)

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
                title = f"Architecture Guide: {title}"

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
            domain=Domain.ARCHITECTURE,
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
        """Extract Architecture-specific structured data.

        Args:
            raw_data: Raw data

        Returns:
            Structured data dictionary
        """
        structured = raw_data.get("structured_data", {}) or {}
        content = raw_data.get("content", "").lower()
        title = raw_data.get("title", "").lower()

        domain_data: dict[str, Any] = {}

        architecture_pattern = structured.get("architecture_pattern") or ""
        if not architecture_pattern:
            architecture_pattern = self._infer_architecture_pattern(content, title)
        if architecture_pattern:
            domain_data["architecture_pattern"] = architecture_pattern

        design_principle = structured.get("design_principle") or ""
        if not design_principle:
            design_principle = self._infer_design_principle(content, title)
        if design_principle:
            domain_data["design_principle"] = design_principle

        scalability_approach = structured.get("scalability_approach") or ""
        if not scalability_approach:
            scalability_approach = self._infer_scalability_approach(content, title)
        if scalability_approach:
            domain_data["scalability_approach"] = scalability_approach

        return domain_data

    def _extract_subdomain(self, raw_data: dict[str, Any], source_url: str) -> str:
        """Extract Architecture subdomain from raw data or URL.

        Args:
            raw_data: Raw data
            source_url: Source URL

        Returns:
            Subdomain string
        """
        subdomain = raw_data.get("subdomain") or "general"

        architecture_subdomains = [
            ("microservices", ["microservice", "microservices", "micro-service", "service-oriented"]),
            ("serverless", ["serverless", "function as a service", "faas", "lambda", "cloud functions"]),
            ("event-driven", ["event-driven", "event driven", "event sourcing", "event stream", "pub/sub"]),
            ("distributed-systems", ["distributed system", "distributed architecture", "distributed computing"]),
            ("design-patterns", ["design pattern", "architectural pattern", "pattern", "best practice"]),
            ("api-design", ["api design", "rest api", "graphql", "api architecture", "api gateway"]),
            ("data-architecture", ["data architecture", "data modeling", "data design", "database design"]),
            ("security-architecture", ["security architecture", "secure design", "security pattern"]),
        ]

        text = f"{raw_data.get('title', '')} {raw_data.get('content', '')}".lower()
        url_lower = source_url.lower()

        for domain_key, keywords in architecture_subdomains:
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
        return "Architecture Article"

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
                r"api gateway",
            ],
            "gcp": [
                r"\bgcp\b",
                r"google cloud",
                r"google cloud platform",
                r"\bgke\b",
                r"cloud storage",
                r"cloud sql",
                r"cloud functions",
                r"cloud run",
                r"cloud endpoints",
            ],
            "azure": [
                r"\bazure\b",
                r"microsoft azure",
                r"azure\s+cloud",
                r"\baks\b",
                r"blob storage",
                r"azure sql",
                r"azure functions",
                r"azure api management",
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

        if not providers and ("cloud" in text or "architecture" in text):
            providers.add("multi-cloud")

        return sorted(list(providers)) if providers else ["multi-cloud"]

    def _infer_services(self, content: str, title: str, cloud_providers: list[str] | None = None) -> list[str]:
        """Infer architecture-related services from content.

        Infers API gateways, message queues, databases, compute services, etc.

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
            "api-gateway": [r"api gateway", r"api-gateway", r"apigateway"],
            "lambda": [r"\blambda\b", r"aws lambda", r"serverless function"],
            "cloud-functions": [r"cloud functions", r"google cloud functions"],
            "azure-functions": [r"azure functions"],
            "sqs": [r"\bsqs\b", r"simple queue service"],
            "sns": [r"\bsns\b", r"simple notification service"],
            "pub-sub": [r"pub/sub", r"pubsub", r"publish subscribe"],
            "kafka": [r"\bkafka\b", r"apache kafka"],
            "rabbitmq": [r"\brabbitmq\b"],
            "rds": [r"\brds\b", r"amazon rds", r"relational database service"],
            "dynamodb": [r"\bdynamodb\b"],
            "cloud-sql": [r"cloud sql", r"google cloud sql"],
            "azure-sql": [r"azure sql"],
            "ec2": [r"\bec2\b", r"elastic compute cloud"],
            "eks": [r"\beks\b", r"elastic kubernetes service"],
            "gke": [r"\bgke\b", r"google kubernetes engine"],
            "aks": [r"\baks\b", r"azure kubernetes service"],
            "kubernetes": [r"\bkubernetes\b", r"\bk8s\b"],
            "ecs": [r"\becs\b", r"elastic container service"],
            "s3": [r"\bs3\b", r"simple storage service"],
            "cloud-storage": [r"cloud storage", r"google cloud storage"],
            "blob-storage": [r"blob storage", r"azure blob"],
            "cloudfront": [r"\bcloudfront\b"],
            "load-balancer": [r"load balancer", r"load balancing", r"\belb\b"],
        }

        for service_name, patterns in service_patterns.items():
            if any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns):
                services.add(service_name)

        if not services:
            if "api" in text or "rest" in text or "graphql" in text:
                services.add("api")
            if "database" in text or "db" in text:
                services.add("database")
            if "message" in text or "queue" in text or "event" in text:
                services.add("messaging")
            if "compute" in text or "server" in text:
                services.add("compute")

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
        if "serverless" in text or "lambda" in text:
            optimization_opportunities.append("serverless")
        if "auto-scaling" in text:
            optimization_opportunities.append("auto-scaling")
        if "microservices" in text:
            optimization_opportunities.append("microservices")

        return {
            "optimization_opportunities": optimization_opportunities if optimization_opportunities else None,
            "cost_category": "architecture",
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
            "requirements": ["architecture-review", "design-documentation"],
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
            "security", "secure", "authentication", "authorization",
            "encryption", "network security",
        ]

        if not any(indicator in text for indicator in security_indicators):
            return None

        threats_mitigated = []
        if "authentication" in text or "auth" in text:
            threats_mitigated.append("unauthorized-access")
        if "encryption" in text:
            threats_mitigated.append("data-exposure")
        if "network" in text or "vpc" in text:
            threats_mitigated.append("network-isolation")

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
            subdomain: Architecture subdomain
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

            architecture_keywords = [
                "architecture", "pattern", "design", "microservice",
                "serverless", "distributed", "scalability",
            ]

            for keyword in architecture_keywords:
                if keyword in text:
                    text_keywords.add(keyword)

            if text_keywords:
                query = {
                    "domain": "architecture",
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

    def _infer_architecture_pattern(self, content: str, title: str) -> str:
        """Infer architecture pattern from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            Architecture pattern or empty string
        """
        text = f"{title} {content}".lower()

        if "microservice" in text:
            return "microservices"
        if "serverless" in text:
            return "serverless"
        if "event-driven" in text or "event driven" in text:
            return "event-driven"
        if "monolith" in text or "monolithic" in text:
            return "monolithic"
        if "layered" in text or "n-tier" in text:
            return "layered"
        if "service-oriented" in text or "soa" in text:
            return "service-oriented"

        return ""

    def _infer_design_principle(self, content: str, title: str) -> str:
        """Infer design principle from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            Design principle or empty string
        """
        text = f"{title} {content}".lower()

        if "separation of concerns" in text or "separation" in text:
            return "separation-of-concerns"
        if "single responsibility" in text:
            return "single-responsibility"
        if "loose coupling" in text or "decoupling" in text:
            return "loose-coupling"
        if "high cohesion" in text:
            return "high-cohesion"
        if "fail fast" in text or "fail-fast" in text:
            return "fail-fast"
        if "resilience" in text or "resilient" in text:
            return "resilience"

        return ""

    def _infer_scalability_approach(self, content: str, title: str) -> str:
        """Infer scalability approach from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            Scalability approach or empty string
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
