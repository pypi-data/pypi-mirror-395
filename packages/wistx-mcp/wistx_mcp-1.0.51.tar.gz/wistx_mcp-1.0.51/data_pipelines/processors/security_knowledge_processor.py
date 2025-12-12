"""Security knowledge processor - processes Security guides and articles."""

import re
from typing import Any

from ..models.knowledge_article import ContentType, Domain, KnowledgeArticle, Reference
from ..processors.base_knowledge_processor import BaseKnowledgeProcessor
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class SecurityKnowledgeProcessor(BaseKnowledgeProcessor):
    """Process Security knowledge articles."""

    def __init__(self, save_intermediate: bool = False):
        """Initialize Security knowledge processor.

        Args:
            save_intermediate: If True, save intermediate files
        """
        super().__init__(domain="security", save_intermediate=save_intermediate)

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
                title = f"Security Guide: {title}"

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
        compliance_impact = raw_data.get("compliance_impact") or self._infer_compliance_impact(content, title, subdomain)
        security_impact = raw_data.get("security_impact") or self._infer_security_impact(content, title, subdomain)

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
            domain=Domain.SECURITY,
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
        """Extract Security-specific structured data.

        Args:
            raw_data: Raw data

        Returns:
            Structured data dictionary
        """
        structured = raw_data.get("structured_data", {}) or {}
        content = raw_data.get("content", "").lower()
        title = raw_data.get("title", "").lower()

        domain_data: dict[str, Any] = {}

        threat_type = structured.get("threat_type") or ""
        if not threat_type:
            threat_type = self._infer_threat_type(content, title)
        if threat_type:
            domain_data["threat_type"] = threat_type

        security_level = structured.get("security_level") or ""
        if not security_level:
            security_level = self._infer_security_level(content, title)
        if security_level:
            domain_data["security_level"] = security_level

        mitigation_strategy = structured.get("mitigation_strategy") or ""
        if not mitigation_strategy:
            mitigation_strategy = self._infer_mitigation_strategy(content, title)
        if mitigation_strategy:
            domain_data["mitigation_strategy"] = mitigation_strategy

        return domain_data

    def _extract_subdomain(self, raw_data: dict[str, Any], source_url: str) -> str:
        """Extract Security subdomain from raw data or URL.

        Args:
            raw_data: Raw data
            source_url: Source URL

        Returns:
            Subdomain string
        """
        subdomain = raw_data.get("subdomain") or "general"

        security_subdomains = [
            ("vulnerability-management", ["vulnerability", "cve", "cve-", "exploit", "patch", "update"]),
            ("threat-detection", ["threat", "detection", "intrusion", "malware", "ransomware", "phishing"]),
            ("access-control", ["access control", "iam", "authentication", "authorization", "rbac", "mfa"]),
            ("encryption", ["encryption", "encrypt", "tls", "ssl", "aes", "key management", "kms"]),
            ("network-security", ["network security", "firewall", "waf", "vpc", "security group", "nacl"]),
            ("data-protection", ["data protection", "data loss", "dlp", "backup", "disaster recovery"]),
            ("security-practices", ["security practice", "best practice", "security policy", "security standard"]),
            ("incident-response", ["incident response", "security incident", "breach", "forensics"]),
            ("compliance-security", ["compliance", "audit", "security audit", "certification"]),
            ("identity-management", ["identity", "sso", "federation", "oauth", "saml"]),
        ]

        text = f"{raw_data.get('title', '')} {raw_data.get('content', '')}".lower()
        url_lower = source_url.lower()

        for domain_key, keywords in security_subdomains:
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
        return "Security Article"

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
                r"\bkms\b",
                r"waf",
                r"shield",
                r"guardduty",
            ],
            "gcp": [
                r"\bgcp\b",
                r"google cloud",
                r"google cloud platform",
                r"\bgke\b",
                r"cloud storage",
                r"cloud sql",
                r"cloud functions",
                r"cloud armor",
                r"cloud identity",
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
                r"key vault",
                r"azure firewall",
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

        if not providers and ("cloud" in text or "security" in text):
            providers.add("multi-cloud")

        return sorted(list(providers)) if providers else ["multi-cloud"]

    def _infer_services(self, content: str, title: str, cloud_providers: list[str] | None = None) -> list[str]:
        """Infer security services and tools from content.

        Infers security services, WAF, IAM, encryption services, etc.

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
            "iam": [r"\biam\b", r"identity and access management", r"access control"],
            "kms": [r"\bkms\b", r"key management service", r"key management"],
            "secrets-manager": [r"secrets manager", r"secrets-manager", r"secret management"],
            "waf": [r"\bwaf\b", r"web application firewall"],
            "shield": [r"\bshield\b", r"aws shield"],
            "guardduty": [r"\bguardduty\b", r"guard duty"],
            "security-hub": [r"security hub"],
            "inspector": [r"\binspector\b", r"aws inspector"],
            "macie": [r"\bmacie\b"],
            "cloud-armor": [r"cloud armor"],
            "cloud-identity": [r"cloud identity"],
            "key-vault": [r"key vault", r"azure key vault"],
            "azure-ad": [r"azure ad\b", r"azure active directory"],
            "azure-firewall": [r"azure firewall"],
            "azure-security-center": [r"azure security center", r"defender"],
            "security-groups": [r"security group", r"security groups"],
            "nacl": [r"\bnacl\b", r"network acl"],
            "vpc": [r"\bvpc\b", r"virtual private cloud"],
            "certificate-manager": [r"certificate manager", r"acm", r"ssl certificate"],
            "cloudfront": [r"\bcloudfront\b"],
            "rds": [r"\brds\b", r"amazon rds"],
            "s3": [r"\bs3\b", r"simple storage service"],
            "ec2": [r"\bec2\b", r"elastic compute cloud"],
            "lambda": [r"\blambda\b", r"aws lambda"],
            "cloud-storage": [r"cloud storage", r"google cloud storage"],
            "cloud-sql": [r"cloud sql", r"google cloud sql"],
            "blob-storage": [r"blob storage", r"azure blob"],
        }

        for service_name, patterns in service_patterns.items():
            if any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns):
                services.add(service_name)

        if not services:
            if "encryption" in text or "encrypt" in text:
                services.add("encryption")
            if "access" in text or "authentication" in text or "authorization" in text:
                services.add("identity-management")
            if "firewall" in text or "waf" in text:
                services.add("firewall")
            if "vulnerability" in text or "scan" in text:
                services.add("vulnerability-scanning")
            if "monitoring" in text or "detection" in text:
                services.add("security-monitoring")

        return sorted(list(services))

    def _infer_security_impact(self, content: str, title: str, subdomain: str | None = None) -> dict[str, Any] | None:
        """Infer security impact from content.

        Args:
            content: Article content
            title: Article title
            subdomain: Security subdomain

        Returns:
            Security impact dictionary or None
        """
        text = f"{title} {content}".lower()

        threats_mitigated = []
        security_level = "medium"

        if "vulnerability" in text or "exploit" in text or "cve" in text:
            threats_mitigated.append("vulnerability-exploitation")
            security_level = "high"
        if "data breach" in text or "breach" in text or "leak" in text:
            threats_mitigated.append("data-breach")
            security_level = "critical"
        if "unauthorized access" in text or "unauthorized" in text:
            threats_mitigated.append("unauthorized-access")
            security_level = "high"
        if "malware" in text or "ransomware" in text or "virus" in text:
            threats_mitigated.append("malware-infection")
            security_level = "high"
        if "ddos" in text or "denial of service" in text:
            threats_mitigated.append("dos-attack")
            security_level = "high"
        if "phishing" in text or "social engineering" in text:
            threats_mitigated.append("phishing-attack")
            security_level = "medium"
        if "credential" in text or "password" in text or "secret" in text:
            threats_mitigated.append("credential-exposure")
            security_level = "high"
        if "encryption" in text or "encrypt" in text:
            threats_mitigated.append("data-exposure")
            security_level = "medium"

        if not threats_mitigated and ("security" in text or "protect" in text or "secure" in text):
            threats_mitigated.append("security-improvement")
            security_level = "medium"

        return {
            "threats_mitigated": threats_mitigated if threats_mitigated else None,
            "security_level": security_level,
        }

    def _infer_compliance_impact(self, content: str, title: str, subdomain: str | None = None) -> dict[str, Any] | None:
        """Infer compliance impact from content.

        Args:
            content: Article content
            title: Article title
            subdomain: Security subdomain

        Returns:
            Compliance impact dictionary or None
        """
        text = f"{title} {content}".lower()

        if "compliance" not in text and "standard" not in text and "regulation" not in text:
            return None

        standards = []
        if "pci" in text or "pci-dss" in text:
            standards.append("PCI-DSS")
        if "hipaa" in text:
            standards.append("HIPAA")
        if "soc" in text or "soc2" in text:
            standards.append("SOC2")
        if "iso" in text or "iso 27001" in text:
            standards.append("ISO-27001")
        if "nist" in text:
            standards.append("NIST-800-53")
        if "gdpr" in text:
            standards.append("GDPR")

        requirements = []
        if "encryption" in text:
            requirements.append("encryption")
        if "access control" in text or "iam" in text:
            requirements.append("access-control")
        if "monitoring" in text or "logging" in text:
            requirements.append("monitoring")
        if "audit" in text:
            requirements.append("audit-trail")

        return {
            "standards": standards if standards else None,
            "requirements": requirements if requirements else None,
            "severity": "high" if standards else "medium",
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
            subdomain: Security subdomain
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

            security_keywords = [
                "security", "vulnerability", "threat", "encryption",
                "access control", "authentication", "firewall", "waf",
            ]

            for keyword in security_keywords:
                if keyword in text:
                    text_keywords.add(keyword)

            if text_keywords:
                query = {
                    "domain": "security",
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

    def _infer_threat_type(self, content: str, title: str) -> str:
        """Infer threat type from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            Threat type or empty string
        """
        text = f"{title} {content}".lower()

        if "vulnerability" in text or "exploit" in text:
            return "vulnerability"
        if "malware" in text or "ransomware" in text:
            return "malware"
        if "phishing" in text or "social engineering" in text:
            return "phishing"
        if "ddos" in text or "denial of service" in text:
            return "dos"
        if "data breach" in text or "breach" in text:
            return "data-breach"
        if "unauthorized access" in text:
            return "unauthorized-access"

        return ""

    def _infer_security_level(self, content: str, title: str) -> str:
        """Infer security level from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            Security level or empty string
        """
        text = f"{title} {content}".lower()

        if "critical" in text or "critical vulnerability" in text:
            return "critical"
        if "high" in text and ("risk" in text or "severity" in text):
            return "high"
        if "medium" in text and ("risk" in text or "severity" in text):
            return "medium"
        if "low" in text and ("risk" in text or "severity" in text):
            return "low"

        if "breach" in text or "critical" in text:
            return "critical"
        if "high" in text or "severe" in text:
            return "high"

        return "medium"

    def _infer_mitigation_strategy(self, content: str, title: str) -> str:
        """Infer mitigation strategy from content.

        Args:
            content: Article content
            title: Article title

        Returns:
            Mitigation strategy or empty string
        """
        text = f"{title} {content}".lower()

        if "encryption" in text:
            return "encryption"
        if "firewall" in text or "waf" in text:
            return "firewall"
        if "access control" in text or "iam" in text:
            return "access-control"
        if "monitoring" in text or "detection" in text:
            return "monitoring"
        if "patch" in text or "update" in text:
            return "patching"
        if "backup" in text or "disaster recovery" in text:
            return "backup-recovery"

        return ""
