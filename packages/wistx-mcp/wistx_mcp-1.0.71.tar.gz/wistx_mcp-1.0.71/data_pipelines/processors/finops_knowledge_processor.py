"""FinOps knowledge processor - processes FinOps guides and articles."""

import re
from typing import Any

from ..models.knowledge_article import ContentType, Domain, KnowledgeArticle, Reference
from ..processors.base_knowledge_processor import BaseKnowledgeProcessor
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class FinOpsKnowledgeProcessor(BaseKnowledgeProcessor):
    """Process FinOps knowledge articles (cost optimization, budgeting, etc.)."""

    def __init__(self, save_intermediate: bool = False):
        """Initialize FinOps knowledge processor.

        Args:
            save_intermediate: If True, save intermediate files
        """
        super().__init__(domain="finops", save_intermediate=save_intermediate)

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
                title = f"FinOps Guide: {title}"

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

        cost_impact = raw_data.get("cost_impact") or self._infer_cost_impact(content, title, subdomain)
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
            domain=Domain.FINOPS,
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
        """Extract FinOps-specific structured data.

        Args:
            raw_data: Raw data

        Returns:
            Structured data dictionary
        """
        structured = raw_data.get("structured_data", {}) or {}
        content = raw_data.get("content", "").lower()
        title = raw_data.get("title", "").lower()

        finops_data: dict[str, Any] = {}

        cost_category = structured.get("cost_category") or ""
        if not cost_category:
            if "compute" in content or "instance" in content:
                cost_category = "compute"
            elif "storage" in content:
                cost_category = "storage"
            elif "network" in content or "transfer" in content:
                cost_category = "network"
            elif "database" in content:
                cost_category = "database"
        if cost_category:
            finops_data["cost_category"] = cost_category

        optimization_type = structured.get("optimization_type") or ""
        if not optimization_type:
            if "reserved" in content:
                optimization_type = "reserved-instances"
            elif "spot" in content or "preemptible" in content:
                optimization_type = "spot-instances"
            elif "rightsizing" in content:
                optimization_type = "rightsizing"
            elif "auto-scaling" in content:
                optimization_type = "auto-scaling"
        if optimization_type:
            finops_data["optimization_type"] = optimization_type

        savings_potential = structured.get("savings_potential") or ""
        if savings_potential:
            finops_data["savings_potential"] = savings_potential

        budget_impact = structured.get("budget_impact") or ""
        if budget_impact:
            finops_data["budget_impact"] = budget_impact

        return finops_data

    def _extract_subdomain(self, raw_data: dict[str, Any], source_url: str) -> str:
        """Extract FinOps subdomain from raw data or URL.

        Args:
            raw_data: Raw data
            source_url: Source URL

        Returns:
            Subdomain string
        """
        subdomain = raw_data.get("subdomain") or "general"

        finops_subdomains = [
            ("cost-optimization", ["cost optimization", "cost optimize", "reduce cost", "lower cost"]),
            ("budgeting", ["budget", "budgeting", "budget management", "budget alert"]),
            ("resource-rightsizing", ["rightsizing", "right-sizing", "rightsize", "instance sizing"]),
            ("reserved-instances", ["reserved instance", "reserved capacity", "ri", "reserved"]),
            ("spot-instances", ["spot instance", "spot fleet", "preemptible", "spot"]),
            ("savings-plans", ["savings plan", "sp", "savings plans"]),
            ("cost-allocation", ["cost allocation", "cost attribution", "chargeback", "showback"]),
            ("cost-visibility", ["cost visibility", "cost reporting", "cost dashboard", "cost analysis"]),
            ("finops-practices", ["finops", "financial operations", "cloud financial management"]),
            ("waste-reduction", ["waste", "unused", "idle", "orphaned", "zombie"]),
            ("pricing-optimization", ["pricing", "pricing model", "pricing strategy"]),
        ]

        text = f"{raw_data.get('title', '')} {raw_data.get('content', '')}".lower()
        url_lower = source_url.lower()

        for domain_key, keywords in finops_subdomains:
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
        return "FinOps Article"

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
                r"bigquery\b",
            ],
            "azure": [
                r"\bazure\b",
                r"microsoft azure",
                r"azure\s+cloud",
                r"\baks\b",
                r"blob storage",
                r"azure sql",
                r"azure functions",
                r"azure ad\b",
            ],
            "oracle": [
                r"\boracle cloud\b",
                r"oracle cloud infrastructure",
                r"\boci\b",
                r"oracle autonomous",
            ],
            "ibm": [
                r"\bibm cloud\b",
                r"ibm cloud platform",
                r"watson",
            ],
            "alibaba": [
                r"\balibaba cloud\b",
                r"aliyun",
                r"alibaba cloud computing",
            ],
        }

        for provider_name, patterns in provider_patterns.items():
            if any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns):
                providers.add(provider_name)

        if not providers and ("cloud" in text or "cloud computing" in text or "finops" in text):
            providers.add("multi-cloud")

        return sorted(list(providers)) if providers else ["multi-cloud"]

    def _infer_services(self, content: str, title: str, cloud_providers: list[str] | None = None) -> list[str]:
        """Infer cloud services from content.

        Infers services from ANY cloud provider, not just AWS.
        Uses generic service categories when specific services aren't mentioned.

        Args:
            content: Article content
            title: Article title
            cloud_providers: List of detected cloud providers

        Returns:
            List of cloud service names (provider-agnostic where possible)
        """
        text = f"{title} {content}".lower()
        services = set()

        service_patterns = {
            "rds": [r"\brds\b", r"amazon rds", r"relational database service"],
            "s3": [r"\bs3\b", r"simple storage service", r"amazon s3"],
            "ec2": [r"\bec2\b", r"elastic compute cloud", r"amazon ec2"],
            "lambda": [r"\blambda\b", r"aws lambda", r"serverless function"],
            "vpc": [r"\bvpc\b", r"virtual private cloud"],
            "eks": [r"\beks\b", r"elastic kubernetes service"],
            "gke": [r"\bgke\b", r"google kubernetes engine"],
            "aks": [r"\baks\b", r"azure kubernetes service"],
            "kubernetes": [r"\bkubernetes\b", r"\bk8s\b"],
            "terraform": [r"\bterraform\b"],
            "cloudformation": [r"\bcloudformation\b"],
            "dynamodb": [r"\bdynamodb\b"],
            "sns": [r"\bsns\b", r"simple notification service"],
            "sqs": [r"\bsqs\b", r"simple queue service"],
            "cloudwatch": [r"\bcloudwatch\b"],
            "iam": [r"\biam\b", r"identity and access management"],
            "kms": [r"\bkms\b", r"key management service"],
            "cloud-storage": [r"cloud storage", r"google cloud storage"],
            "cloud-sql": [r"cloud sql", r"google cloud sql"],
            "cloud-functions": [r"cloud functions", r"google cloud functions"],
            "bigquery": [r"\bbigquery\b"],
            "blob-storage": [r"blob storage", r"azure blob"],
            "azure-sql": [r"azure sql"],
            "azure-functions": [r"azure functions"],
            "azure-ad": [r"azure ad\b", r"azure active directory"],
            "key-vault": [r"key vault", r"azure key vault"],
            "azure-monitor": [r"azure monitor"],
            "compute-engine": [r"compute engine", r"gce"],
            "app-engine": [r"app engine"],
            "cloud-run": [r"cloud run"],
            "cost-management": [r"cost management", r"cost explorer", r"billing"],
            "budget": [r"budget", r"budget alert", r"budget notification"],
            "reserved-instances": [r"reserved instance", r"reserved capacity", r"ri"],
            "savings-plans": [r"savings plan", r"sp"],
            "spot-instances": [r"spot instance", r"spot fleet", r"preemptible"],
        }

        for service_name, patterns in service_patterns.items():
            if any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns):
                services.add(service_name)

        if not services:
            if "encryption" in text or "encrypt" in text or "key management" in text:
                services.add("key-management")
            if "access control" in text or "authentication" in text or "authorization" in text:
                services.add("identity-management")
            if "monitoring" in text or "logging" in text or "audit" in text:
                services.add("monitoring")
            if "storage" in text or "data storage" in text:
                services.add("object-storage")
            if "database" in text or "data persistence" in text:
                services.add("database")
            if "network" in text or "networking" in text:
                services.add("networking")
            if "compute" in text or "instance" in text or "vm" in text:
                services.add("compute")
            if "cost" in text or "pricing" in text or "budget" in text:
                services.add("cost-management")

        return sorted(list(services))

    def _infer_cost_impact(self, content: str, title: str, subdomain: str | None = None) -> dict[str, Any] | None:
        """Infer cost impact from content.

        Args:
            content: Article content
            title: Article title
            subdomain: FinOps subdomain

        Returns:
            Cost impact dictionary or None
        """
        text = f"{title} {content}".lower()

        cost_indicators = [
            "cost", "pricing", "price", "expensive", "cheap", "budget",
            "savings", "optimization", "reserved", "spot", "on-demand",
            "spend", "expense", "billing", "charge", "fee",
        ]

        if not any(indicator in text for indicator in cost_indicators):
            return None

        optimization_opportunities = []
        savings_potential = None

        if re.search(r"reserved\s+instance|reserved\s+capacity|\bri\b", text):
            optimization_opportunities.append("reserved-instances")
            savings_potential = "30-40%"
        if re.search(r"spot\s+instance|spot\s+fleet|preemptible", text):
            optimization_opportunities.append("spot-instances")
            savings_potential = "50-90%"
        if re.search(r"savings\s+plan|\bsp\b", text):
            optimization_opportunities.append("savings-plans")
            savings_potential = "30-40%"
        if re.search(r"rightsizing|right-sizing|rightsize", text):
            optimization_opportunities.append("rightsizing")
            savings_potential = "20-40%"
        if re.search(r"auto-scaling|autoscaling|auto\s+scale", text):
            optimization_opportunities.append("auto-scaling")
            savings_potential = "10-30%"
        if re.search(r"idle\s+resource|unused\s+resource|orphaned", text):
            optimization_opportunities.append("resource-cleanup")
            savings_potential = "10-20%"
        if re.search(r"data\s+transfer|egress|bandwidth", text):
            optimization_opportunities.append("data-transfer-optimization")
            savings_potential = "5-15%"
        if re.search(r"storage\s+optimization|lifecycle|archive", text):
            optimization_opportunities.append("storage-optimization")
            savings_potential = "20-60%"

        if not optimization_opportunities and ("save" in text or "reduce" in text or "optimize" in text):
            optimization_opportunities.append("cost-reduction")

        cost_category = "operational"
        if "compute" in text or "instance" in text or "vm" in text:
            cost_category = "compute"
        elif "storage" in text or "s3" in text or "blob" in text:
            cost_category = "storage"
        elif "network" in text or "transfer" in text or "egress" in text:
            cost_category = "network"
        elif "database" in text or "rds" in text or "sql" in text:
            cost_category = "database"
        elif "monitoring" in text or "logging" in text:
            cost_category = "observability"

        return {
            "optimization_opportunities": optimization_opportunities if optimization_opportunities else None,
            "savings_potential": savings_potential,
            "cost_category": cost_category,
        }

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
            subdomain: FinOps subdomain
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

            finops_keywords = [
                "cost", "pricing", "budget", "savings", "optimization",
                "reserved", "spot", "rightsizing", "finops",
            ]

            for keyword in finops_keywords:
                if keyword in text:
                    text_keywords.add(keyword)

            if text_keywords:
                query = {
                    "domain": "finops",
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

