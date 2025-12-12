"""DevOps knowledge processor - processes DevOps guides and articles."""

import re
from typing import Any

from ..models.knowledge_article import ContentType, Domain, KnowledgeArticle, Reference
from ..processors.base_knowledge_processor import BaseKnowledgeProcessor
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class DevOpsKnowledgeProcessor(BaseKnowledgeProcessor):
    """Process DevOps knowledge articles."""

    def __init__(self, save_intermediate: bool = False):
        """Initialize DevOps knowledge processor.

        Args:
            save_intermediate: If True, save intermediate files
        """
        super().__init__(domain="devops", save_intermediate=save_intermediate)

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
                title = f"DevOps Guide: {title}"

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
            domain=Domain.DEVOPS,
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
        """Extract DevOps-specific structured data.

        Args:
            raw_data: Raw data

        Returns:
            Structured data dictionary
        """
        structured = raw_data.get("structured_data", {}) or {}
        content = raw_data.get("content", "").lower()
        title = raw_data.get("title", "").lower()

        domain_data: dict[str, Any] = {}

        tool = structured.get("tool") or ""
        if not tool:
            tool = self._infer_tool(content, title)
        if tool:
            domain_data["tool"] = tool

        pipeline_stage = structured.get("pipeline_stage") or ""
        if not pipeline_stage:
            pipeline_stage = self._infer_pipeline_stage(content, title)
        if pipeline_stage:
            domain_data["pipeline_stage"] = pipeline_stage

        automation_level = structured.get("automation_level") or ""
        if not automation_level:
            automation_level = self._infer_automation_level(content, title)
        if automation_level:
            domain_data["automation_level"] = automation_level

        return domain_data

    def _extract_subdomain(self, raw_data: dict[str, Any], source_url: str) -> str:
        """Extract DevOps subdomain from raw data or URL.

        Args:
            raw_data: Raw data
            source_url: Source URL

        Returns:
            Subdomain string
        """
        subdomain = raw_data.get("subdomain") or "general"

        devops_subdomains = [
            ("ci-cd", ["ci/cd", "ci cd", "continuous integration", "continuous deployment", "jenkins", "gitlab ci", "github actions", "circleci", "travis"]),
            ("deployment", ["deployment", "deploy", "rollout", "release", "canary", "blue-green"]),
            ("logging", ["logging", "log", "log aggregation", "elk", "splunk", "cloudwatch logs"]),
            ("infrastructure-as-code", ["infrastructure as code", "iac", "terraform", "cloudformation", "pulumi", "ansible"]),
            ("containerization", ["container", "docker", "containerization", "container orchestration"]),
            ("kubernetes", ["kubernetes", "k8s", "eks", "gke", "aks", "helm"]),
            ("configuration-management", ["configuration management", "puppet", "chef", "ansible", "salt"]),
            ("testing", ["testing", "test automation", "unit test", "integration test", "e2e"]),
            ("security", ["devsecops", "security scanning", "vulnerability scanning", "sast", "dast"]),
        ]

        text = f"{raw_data.get('title', '')} {raw_data.get('content', '')}".lower()
        url_lower = source_url.lower()

        for domain_key, keywords in devops_subdomains:
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
        return "DevOps Article"

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
                r"codebuild",
                r"codepipeline",
            ],
            "gcp": [
                r"\bgcp\b",
                r"google cloud",
                r"google cloud platform",
                r"\bgke\b",
                r"cloud storage",
                r"cloud sql",
                r"cloud functions",
                r"cloud build",
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
                r"azure devops",
                r"azure pipelines",
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

        if not providers and ("cloud" in text or "devops" in text or "ci/cd" in text):
            providers.add("multi-cloud")

        return sorted(list(providers)) if providers else ["multi-cloud"]

    def _infer_services(self, content: str, title: str, cloud_providers: list[str] | None = None) -> list[str]:
        """Infer cloud services and DevOps tools from content.

        Infers CI/CD tools, container orchestration, IaC tools, and cloud services.

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
            "kubernetes": [r"\bkubernetes\b", r"\bk8s\b", r"\beks\b", r"\bgke\b", r"\baks\b"],
            "docker": [r"\bdocker\b", r"dockerfile", r"docker compose"],
            "terraform": [r"\bterraform\b"],
            "ansible": [r"\bansible\b"],
            "puppet": [r"\bpuppet\b"],
            "chef": [r"\bchef\b"],
            "jenkins": [r"\bjenkins\b"],
            "gitlab-ci": [r"gitlab ci", r"gitlab-ci", r"\.gitlab-ci"],
            "github-actions": [r"github actions", r"github workflows"],
            "circleci": [r"\bcircleci\b"],
            "travis-ci": [r"\btravis\b", r"travis ci"],
            "azure-devops": [r"azure devops", r"azure pipelines"],
            "cloudformation": [r"\bcloudformation\b"],
            "pulumi": [r"\bpulumi\b"],
            "helm": [r"\bhelm\b"],
            "prometheus": [r"\bprometheus\b"],
            "grafana": [r"\bgrafana\b"],
            "datadog": [r"\bdatadog\b"],
            "new-relic": [r"new relic", r"newrelic"],
            "splunk": [r"\bsplunk\b"],
            "elk": [r"\belk\b", r"elasticsearch", r"logstash", r"kibana"],
            "rds": [r"\brds\b", r"amazon rds"],
            "ec2": [r"\bec2\b", r"elastic compute cloud"],
            "s3": [r"\bs3\b", r"simple storage service"],
            "lambda": [r"\blambda\b", r"aws lambda"],
            "cloud-storage": [r"cloud storage", r"google cloud storage"],
            "cloud-sql": [r"cloud sql", r"google cloud sql"],
            "cloud-functions": [r"cloud functions", r"google cloud functions"],
            "cloud-build": [r"cloud build"],
            "cloud-run": [r"cloud run"],
            "blob-storage": [r"blob storage", r"azure blob"],
            "azure-functions": [r"azure functions"],
            "codebuild": [r"\bcodebuild\b"],
            "codepipeline": [r"\bcodepipeline\b"],
            "ecs": [r"\becs\b", r"elastic container service"],
            "fargate": [r"\bfargate\b"],
        }

        for service_name, patterns in service_patterns.items():
            if any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns):
                services.add(service_name)

        if not services:
            if "ci" in text or "cd" in text or "pipeline" in text:
                services.add("ci-cd")
            if "container" in text or "docker" in text:
                services.add("containerization")
            if "monitoring" in text or "metrics" in text:
                services.add("monitoring")
            if "logging" in text or "log" in text:
                services.add("logging")
            if "infrastructure" in text or "iac" in text:
                services.add("infrastructure-as-code")

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
        if "automation" in text or "automate" in text:
            optimization_opportunities.append("automation")
        if "container" in text or "kubernetes" in text:
            optimization_opportunities.append("containerization")
        if "serverless" in text or "lambda" in text:
            optimization_opportunities.append("serverless")

        return {
            "optimization_opportunities": optimization_opportunities if optimization_opportunities else None,
            "cost_category": "operational",
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
            "requirements": ["audit-trail", "change-management"],
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
            "security", "vulnerability", "scan", "secret", "credential",
            "authentication", "authorization", "access control",
        ]

        if not any(indicator in text for indicator in security_indicators):
            return None

        threats_mitigated = []
        if "secret" in text or "credential" in text:
            threats_mitigated.append("credential-exposure")
        if "vulnerability" in text or "scan" in text:
            threats_mitigated.append("vulnerability-exploitation")
        if "access" in text or "authentication" in text:
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
            subdomain: DevOps subdomain
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

            devops_keywords = [
                "ci", "cd", "pipeline", "deployment", "monitoring",
                "kubernetes", "docker", "terraform", "automation",
            ]

            for keyword in devops_keywords:
                if keyword in text:
                    text_keywords.add(keyword)

            if text_keywords:
                query = {
                    "domain": "devops",
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

    def _infer_tool(self, content: str, title: str) -> str:
        """Infer DevOps tool from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            Tool name or empty string
        """
        text = f"{title} {content}".lower()

        tools = {
            "jenkins": ["jenkins"],
            "gitlab-ci": ["gitlab ci", "gitlab-ci"],
            "github-actions": ["github actions", "github workflows"],
            "circleci": ["circleci"],
            "travis-ci": ["travis"],
            "azure-devops": ["azure devops", "azure pipelines"],
            "terraform": ["terraform"],
            "ansible": ["ansible"],
            "puppet": ["puppet"],
            "chef": ["chef"],
            "docker": ["docker"],
            "kubernetes": ["kubernetes", "k8s"],
            "helm": ["helm"],
            "prometheus": ["prometheus"],
            "grafana": ["grafana"],
        }

        for tool_name, keywords in tools.items():
            if any(keyword in text for keyword in keywords):
                return tool_name

        return ""

    def _infer_pipeline_stage(self, content: str, title: str) -> str:
        """Infer pipeline stage from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            Pipeline stage or empty string
        """
        text = f"{title} {content}".lower()

        if "build" in text or "compile" in text:
            return "build"
        if "test" in text or "testing" in text:
            return "test"
        if "deploy" in text or "deployment" in text:
            return "deploy"
        if "release" in text:
            return "release"
        if "monitor" in text or "monitoring" in text:
            return "monitor"

        return ""

    def _infer_automation_level(self, content: str, title: str) -> str:
        """Infer automation level from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            Automation level or empty string
        """
        text = f"{title} {content}".lower()

        if "fully automated" in text or "full automation" in text:
            return "full"
        if "semi-automated" in text or "partial automation" in text:
            return "partial"
        if "manual" in text and "automation" not in text:
            return "manual"
        if "automation" in text or "automate" in text:
            return "automated"

        return ""
