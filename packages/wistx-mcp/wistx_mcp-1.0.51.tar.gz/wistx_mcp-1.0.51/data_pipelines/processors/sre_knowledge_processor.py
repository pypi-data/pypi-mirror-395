"""SRE knowledge processor - processes SRE guides and articles."""

import re
from typing import Any

from ..models.knowledge_article import ContentType, Domain, KnowledgeArticle, Reference
from ..processors.base_knowledge_processor import BaseKnowledgeProcessor
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class SREKnowledgeProcessor(BaseKnowledgeProcessor):
    """Process SRE knowledge articles (SLO/SLI/SLA, incidents, reliability, etc.)."""

    def __init__(self, save_intermediate: bool = False):
        """Initialize SRE knowledge processor.

        Args:
            save_intermediate: If True, save intermediate files
        """
        super().__init__(domain="sre", save_intermediate=save_intermediate)

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
                title = f"SRE Guide: {title}"

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
            domain=Domain.SRE,
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
        """Extract SRE-specific structured data.

        Args:
            raw_data: Raw data

        Returns:
            Structured data dictionary
        """
        structured = raw_data.get("structured_data", {}) or {}
        content = raw_data.get("content", "").lower()
        title = raw_data.get("title", "").lower()

        sre_data: dict[str, Any] = {}

        slo_target = structured.get("slo_target") or ""
        if not slo_target:
            slo_match = re.search(r"slo[:\s]+([\d.]+)%", content, re.IGNORECASE)
            if slo_match:
                slo_target = slo_match.group(1) + "%"
        if slo_target:
            sre_data["slo_target"] = slo_target

        error_budget_policy = structured.get("error_budget_policy") or ""
        if not error_budget_policy:
            if "error budget" in content:
                if "spend" in content or "use" in content:
                    error_budget_policy = "spend-when-needed"
                elif "preserve" in content or "protect" in content:
                    error_budget_policy = "preserve-budget"
        if error_budget_policy:
            sre_data["error_budget_policy"] = error_budget_policy

        incident_severity = structured.get("incident_severity") or ""
        if not incident_severity:
            if "severity 1" in content or "sev1" in content or "p0" in content:
                incident_severity = "critical"
            elif "severity 2" in content or "sev2" in content or "p1" in content:
                incident_severity = "high"
            elif "severity 3" in content or "sev3" in content or "p2" in content:
                incident_severity = "medium"
        if incident_severity:
            sre_data["incident_severity"] = incident_severity

        reliability_pattern = structured.get("reliability_pattern") or ""
        if not reliability_pattern:
            if "circuit breaker" in content:
                reliability_pattern = "circuit-breaker"
            elif "retry" in content and "exponential" in content:
                reliability_pattern = "exponential-backoff"
            elif "timeout" in content:
                reliability_pattern = "timeout"
            elif "health check" in content:
                reliability_pattern = "health-checking"
            elif "load balancing" in content or "load balancer" in content:
                reliability_pattern = "load-balancing"
        if reliability_pattern:
            sre_data["reliability_pattern"] = reliability_pattern

        return sre_data

    def _extract_subdomain(self, raw_data: dict[str, Any], source_url: str) -> str:
        """Extract SRE subdomain from raw data or URL.

        Args:
            raw_data: Raw data
            source_url: Source URL

        Returns:
            Subdomain string
        """
        subdomain = raw_data.get("subdomain") or "general"

        sre_subdomains = [
            ("slo-sli-sla", ["slo", "sli", "sla", "service level", "service-level"]),
            ("error-budgets", ["error budget", "error-budget", "budget policy"]),
            ("incident-management", ["incident", "incident response", "incident management", "on-call"]),
            ("postmortems", ["postmortem", "post-mortem", "post mortem", "blameless"]),
            ("capacity-planning", ["capacity planning", "capacity", "scaling", "forecast"]),
            ("performance-engineering", ["performance", "latency", "throughput", "optimization"]),
            ("reliability-patterns", ["reliability", "resilience", "fault tolerance", "high availability"]),
            ("toil-reduction", ["toil", "toil reduction", "automation", "manual work"]),
        ]

        text = f"{raw_data.get('title', '')} {raw_data.get('content', '')}".lower()
        url_lower = source_url.lower()

        for domain_key, keywords in sre_subdomains:
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
        if "pattern" in text or "reliability pattern" in text:
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
        return "SRE Article"

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

        Supports all major cloud providers.

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
                r"\blambda\b",
                r"cloudwatch\b",
            ],
            "gcp": [
                r"\bgcp\b",
                r"google cloud",
                r"google cloud platform",
                r"\bgke\b",
                r"cloud monitoring",
            ],
            "azure": [
                r"\bazure\b",
                r"microsoft azure",
                r"azure\s+cloud",
                r"\baks\b",
                r"azure monitor",
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

        if not providers and ("cloud" in text or "sre" in text):
            providers.add("multi-cloud")

        return sorted(list(providers)) if providers else ["multi-cloud"]

    def _infer_services(self, content: str, title: str, cloud_providers: list[str] | None = None) -> list[str]:
        """Infer SRE services and tools from content.

        Args:
            content: Article content
            title: Article title
            cloud_providers: List of detected cloud providers

        Returns:
            List of service/tool names
        """
        text = f"{title} {content}".lower()
        services = set()

        service_patterns = {
            "prometheus": [r"\bprometheus\b"],
            "grafana": [r"\bgrafana\b"],
            "datadog": [r"\bdatadog\b"],
            "new-relic": [r"new relic", r"newrelic"],
            "splunk": [r"\bsplunk\b"],
            "elastic": [r"\belastic\b", r"elasticsearch"],
            "cloudwatch": [r"\bcloudwatch\b"],
            "azure-monitor": [r"azure monitor"],
            "stackdriver": [r"\bstackdriver\b"],
            "pagerduty": [r"\bpagerduty\b"],
            "opsgenie": [r"\bopsgenie\b"],
            "victorops": [r"\bvictorops\b"],
            "kubernetes": [r"\bkubernetes\b", r"\bk8s\b"],
            "istio": [r"\bistio\b"],
            "linkerd": [r"\blinkerd\b"],
            "envoy": [r"\benvoy\b"],
            "chaos-engineering": [r"chaos engineering", r"chaos monkey", r"chaos mesh"],
            "gremlin": [r"\bgremlin\b"],
            "litmus": [r"\blitmus\b"],
            "slo": [r"\bslo\b", r"service level objective"],
            "sli": [r"\bsli\b", r"service level indicator"],
            "sla": [r"\bsla\b", r"service level agreement"],
        }

        for service_name, patterns in service_patterns.items():
            if any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns):
                services.add(service_name)

        if not services:
            if "monitoring" in text or "observability" in text:
                services.add("monitoring")
            if "incident" in text or "alert" in text:
                services.add("incident-management")
            if "reliability" in text or "resilience" in text:
                services.add("reliability-engineering")

        return sorted(list(services))

    def _infer_cost_impact(self, content: str, title: str, subdomain: str | None = None) -> dict[str, Any] | None:
        """Infer cost impact from content.

        Args:
            content: Article content
            title: Article title
            subdomain: SRE subdomain

        Returns:
            Cost impact dictionary or None
        """
        text = f"{title} {content}".lower()

        cost_indicators = [
            "cost", "pricing", "expensive", "cheap", "budget",
            "savings", "optimization", "spend", "expense",
        ]

        if not any(indicator in text for indicator in cost_indicators):
            return None

        optimization_opportunities = []
        savings_potential = None

        if "toil reduction" in text or "automation" in text:
            optimization_opportunities.append("toil-reduction")
            savings_potential = "15-30%"
        if "capacity planning" in text or "rightsizing" in text:
            optimization_opportunities.append("capacity-optimization")
            savings_potential = "10-25%"
        if "reliability" in text and "cost" in text:
            optimization_opportunities.append("reliability-cost-balance")
            savings_potential = "5-15%"

        cost_category = "operational"
        if "monitoring" in text or "observability" in text:
            cost_category = "observability"
        elif "incident" in text:
            cost_category = "incident-management"

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
        text = f"{title} {content}".lower()

        compliance_keywords = [
            "compliance", "audit", "governance", "policy", "standard",
            "regulation", "requirement", "certification",
        ]

        if not any(keyword in text for keyword in compliance_keywords):
            return None

        standards = []
        if "soc" in text or "soc2" in text:
            standards.append("SOC2")
        if "iso" in text or "iso 27001" in text:
            standards.append("ISO-27001")
        if "gdpr" in text:
            standards.append("GDPR")

        return {
            "standards": standards if standards else None,
            "impact": "reliability-compliance",
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

        security_keywords = [
            "security", "secure", "authentication", "authorization",
            "access control", "vulnerability", "threat", "encryption",
        ]

        if not any(keyword in text for keyword in security_keywords):
            return None

        threats_mitigated = []
        if "incident" in text and "response" in text:
            threats_mitigated.append("security-incident")
        if "monitoring" in text and "security" in text:
            threats_mitigated.append("security-monitoring")
        if "access control" in text:
            threats_mitigated.append("unauthorized-access")

        security_level = "medium"
        if "critical" in text or "high" in text:
            security_level = "high"

        return {
            "threats_mitigated": threats_mitigated if threats_mitigated else None,
            "security_level": security_level,
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
            subdomain: SRE subdomain
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

            sre_keywords = [
                "sre", "reliability", "slo", "sli", "sla", "incident",
                "error budget", "postmortem", "capacity",
            ]

            for keyword in sre_keywords:
                if keyword in text:
                    text_keywords.add(keyword)

            if text_keywords:
                query = {
                    "domain": "sre",
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

