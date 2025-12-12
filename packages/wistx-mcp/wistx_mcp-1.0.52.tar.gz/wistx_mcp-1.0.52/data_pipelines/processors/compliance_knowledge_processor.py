"""Compliance knowledge processor - processes compliance guides and articles."""

import hashlib
import re
from typing import Any
from urllib.parse import urlparse

from ..models.knowledge_article import ContentType, Domain, KnowledgeArticle, Reference
from ..processors.base_knowledge_processor import BaseKnowledgeProcessor
from ..processors.category_resource_mapper import CategoryResourceMapper
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class ComplianceKnowledgeProcessor(BaseKnowledgeProcessor):
    """Process compliance knowledge articles (guides, not controls).
    
    Processes compliance guides, implementation guides, and best practices
    that go beyond individual controls.
    """

    def __init__(self, save_intermediate: bool = False):
        """Initialize compliance knowledge processor.
        
        Args:
            save_intermediate: If True, save intermediate files
        """
        super().__init__(domain="compliance", save_intermediate=save_intermediate)
        self.resource_mapper = CategoryResourceMapper()
        self._standard_metadata_cache: dict[str, dict[str, Any]] = {}

    def process_raw_data(self, raw_data: dict[str, Any]) -> KnowledgeArticle:
        """Process raw data into KnowledgeArticle.
        
        Args:
            raw_data: Raw data from collector
            
        Returns:
            Processed KnowledgeArticle
            
        Raises:
            ValueError: If article fails pre-validation filtering
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
                title = f"Compliance Guide: {title}"

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
        
        if not cloud_providers:
            cloud_providers = self._infer_cloud_providers_from_compliance_context(subdomain, content, title)
        
        services = raw_data.get("services", []) or []
        
        if not services:
            services = self._infer_services(content, title)
            logger.debug(
                "Services inferred from content: %s (title: %s)",
                services,
                title[:50],
            )
        
        if not services and cloud_providers:
            services = self._infer_generic_services_from_providers(cloud_providers, content)
            logger.debug(
                "Services inferred from providers: %s (providers: %s)",
                services,
                cloud_providers,
            )
        
        compliance_impact = raw_data.get("compliance_impact")
        if not compliance_impact:
            compliance_impact = self._infer_compliance_impact(content, title, subdomain)
        
        if not compliance_impact and subdomain:
            standard_metadata = self._get_standard_metadata(subdomain)
            compliance_impact = {
                "standards": [subdomain.upper().replace("-", "-")],
                "severity": standard_metadata.get("severity", "medium"),
            }
        
        if not services:
            services = self._infer_services_from_compliance_requirements(
                content, title, subdomain, structured_data, compliance_impact
            )
            logger.debug(
                "Services inferred from compliance requirements: %s (subdomain: %s)",
                services,
                subdomain,
            )
        
        cost_impact = raw_data.get("cost_impact")
        if not cost_impact:
            cost_impact = self._infer_cost_impact(content, title)
        
        security_impact = raw_data.get("security_impact")
        if not security_impact:
            security_impact = self._infer_security_impact(content, title)
        
        if not security_impact and subdomain:
            standard_metadata = self._get_standard_metadata(subdomain)
            if standard_metadata.get("security_level") == "high":
                security_impact = {
                    "threats_mitigated": standard_metadata.get("threats_mitigated", ["data-breach", "unauthorized-access"]),
                    "security_level": "high",
                }

        references = self._extract_references(raw_data, source_url)
        
        content_hash = self._generate_content_hash(content)
        source_hash = self._generate_source_hash(source_url, raw_data)

        related_articles = raw_data.get("related_articles", []) or []
        related_controls = raw_data.get("related_controls", []) or []
        related_code_examples = raw_data.get("related_code_examples", []) or []
        
        if not related_articles or not related_controls:
            discovered_relations = self._discover_related_items(
                article_id, subdomain, content, title, tags
            )
            if not related_articles:
                related_articles = discovered_relations.get("articles", [])
            if not related_controls:
                related_controls = discovered_relations.get("controls", [])

        article = KnowledgeArticle(
            article_id=article_id,
            domain=Domain.COMPLIANCE,
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
            related_controls=related_controls,
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
            "digitalocean": [
                r"\bdigitalocean\b",
                r"digital ocean",
            ],
            "vultr": [
                r"\bvultr\b",
            ],
            "linode": [
                r"\blinode\b",
            ],
        }
        
        for provider_name, patterns in provider_patterns.items():
            if any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns):
                providers.add(provider_name)
        
        if not providers and ("cloud" in text or "cloud computing" in text):
            providers.add("multi-cloud")
        
        return sorted(list(providers))

    def _infer_cloud_providers_from_compliance_context(
        self, subdomain: str, content: str, title: str
    ) -> list[str]:
        """Infer cloud providers from compliance context (final fallback).
        
        Compliance standards apply to all cloud providers.
        If no specific providers detected, default to multi-cloud for compliance articles.
        
        Args:
            subdomain: Compliance subdomain
            content: Article content
            title: Article title
            
        Returns:
            List of cloud provider names (typically ["multi-cloud"])
        """
        text = f"{title} {content}".lower()
        
        standard_metadata = self._get_standard_metadata(subdomain)
        if standard_metadata.get("applies_to_cloud", True):
            if "electronic" in text or "digital" in text or "technology" in text or "system" in text:
                return ["multi-cloud"]
        
        return []

    def _infer_services(self, content: str, title: str) -> list[str]:
        """Infer cloud services from content.
        
        Infers services from ANY cloud provider, not just AWS.
        Uses generic service categories when specific services aren't mentioned.
        
        Args:
            content: Article content
            title: Article title
            
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
            "secrets-manager": [r"\bsecrets manager\b", r"\bsecrets-manager\b"],
            "cloudfront": [r"\bcloudfront\b"],
            "route53": [r"\broute53\b"],
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
            
            if "database" in text or "data persistence" in text or "ephi" in text or "phi" in text or "protected health information" in text:
                services.add("database")
            
            if "network" in text or "networking" in text or "vpc" in text:
                services.add("networking")
        
        return sorted(list(services))

    def _infer_generic_services_from_providers(
        self, cloud_providers: list[str], content: str
    ) -> list[str]:
        """Infer generic services based on cloud providers and compliance requirements.
        
        Uses provider-agnostic service categories when possible.
        Falls back to provider-specific services only when providers are known.
        
        Args:
            cloud_providers: List of cloud providers (any provider)
            content: Article content
            
        Returns:
            List of service names (generic or provider-specific)
        """
        text = content.lower()
        services = set()
        
        provider_agnostic = "multi-cloud" in cloud_providers or len(cloud_providers) > 1
        
        if provider_agnostic:
            if "encryption" in text or "encrypt" in text or "key" in text:
                services.add("key-management")
            if "access" in text or "authentication" in text or "identity" in text:
                services.add("identity-management")
            if "monitoring" in text or "logging" in text or "audit" in text:
                services.add("monitoring")
            if "storage" in text or "data" in text:
                services.add("object-storage")
            if "database" in text or "data persistence" in text:
                services.add("database")
            if "network" in text or "security" in text:
                services.add("networking")
        else:
            for provider in cloud_providers:
                provider_lower = provider.lower()
                
                if provider_lower == "aws":
                    if "encryption" in text or "encrypt" in text or "key" in text:
                        services.add("kms")
                        services.add("secrets-manager")
                    if "access" in text or "authentication" in text or "identity" in text:
                        services.add("iam")
                    if "monitoring" in text or "logging" in text or "audit" in text:
                        services.add("cloudwatch")
                    if "storage" in text or "data" in text:
                        services.add("s3")
                    if "network" in text or "security" in text:
                        services.add("vpc")
                
                elif provider_lower == "gcp":
                    if "encryption" in text or "encrypt" in text or "key" in text:
                        services.add("cloud-kms")
                    if "access" in text or "authentication" in text or "identity" in text:
                        services.add("cloud-iam")
                    if "monitoring" in text or "logging" in text:
                        services.add("cloud-monitoring")
                    if "storage" in text or "data" in text:
                        services.add("cloud-storage")
                
                elif provider_lower == "azure":
                    if "encryption" in text or "encrypt" in text or "key" in text:
                        services.add("key-vault")
                    if "access" in text or "authentication" in text or "identity" in text:
                        services.add("azure-ad")
                    if "monitoring" in text or "logging" in text:
                        services.add("azure-monitor")
                    if "storage" in text or "data" in text:
                        services.add("blob-storage")
                
                else:
                    if "encryption" in text or "encrypt" in text or "key" in text:
                        services.add("key-management")
                    if "access" in text or "authentication" in text or "identity" in text:
                        services.add("identity-management")
                    if "monitoring" in text or "logging" in text or "audit" in text:
                        services.add("monitoring")
                    if "storage" in text or "data" in text:
                        services.add("object-storage")
                    if "database" in text or "data persistence" in text:
                        services.add("database")
                    if "network" in text or "security" in text:
                        services.add("networking")
        
        return sorted(list(services))

    def _infer_services_from_compliance_requirements(
        self,
        content: str,
        title: str,
        subdomain: str,
        structured_data: dict[str, Any],
        compliance_impact: dict[str, Any] | None,
    ) -> list[str]:
        """Infer services from compliance requirements using CategoryResourceMapper.
        
        Fully data-driven approach:
        1. Extract categories from compliance_impact requirements
        2. Extract categories from structured_data requirement_area
        3. Extract categories from content keywords (fallback)
        4. Use CategoryResourceMapper to get resources for each category
        5. Convert resources to generic service names
        
        Args:
            content: Article content
            title: Article title
            subdomain: Compliance subdomain
            structured_data: Structured data dictionary
            compliance_impact: Compliance impact dictionary
            
        Returns:
            List of generic service names based on compliance requirements
        """
        services = set()
        categories = set()
        
        if compliance_impact:
            requirements = compliance_impact.get("requirements") or []
            for requirement in requirements:
                category = self._requirement_to_category(requirement)
                if category:
                    categories.add(category)
        
        requirement_area = structured_data.get("requirement_area") or structured_data.get("category")
        if requirement_area:
            category = self._requirement_area_to_category(requirement_area)
            if category:
                categories.add(category)
        
        if not categories:
            text = f"{title} {content}".lower()
            categories = set(self._extract_compliance_categories(text))
        
        for category in categories:
            category_resources = self.resource_mapper.get_all_for_category(category)
            category_services = self._resources_to_services(category_resources)
            services.update(category_services)
        
        if not services and subdomain:
            default_categories = self._get_default_categories_for_standard(subdomain)
            for category in default_categories:
                category_resources = self.resource_mapper.get_all_for_category(category)
                category_services = self._resources_to_services(category_resources)
                services.update(category_services)
        
        return sorted(list(services)) if services else ["compliance-services"]

    def _get_standard_metadata(self, subdomain: str) -> dict[str, Any]:
        """Get standard metadata (severity, threats, security level) from data sources.
        
        Data-driven approach:
        1. Query MongoDB compliance_controls to infer metadata from actual controls
        2. Fallback to config-based metadata (COMPLIANCE_URLS)
        3. Final fallback to hardcoded defaults (backward compatibility)
        
        Args:
            subdomain: Compliance subdomain (e.g., "hipaa", "pci-dss")
            
        Returns:
            Dictionary with standard metadata:
            - severity: "high" | "medium" | "low"
            - security_level: "high" | "medium" | "low"
            - threats_mitigated: List of threat strings
            - applies_to_cloud: Boolean (default: True)
        """
        subdomain_lower = subdomain.lower().replace("_", "-")
        
        if subdomain_lower in self._standard_metadata_cache:
            return self._standard_metadata_cache[subdomain_lower]
        
        metadata: dict[str, Any] = {
            "severity": "medium",
            "security_level": "medium",
            "threats_mitigated": [],
            "applies_to_cloud": True,
        }
        
        try:
            from api.database.mongodb import mongodb_manager
            from pymongo.errors import (
                AutoReconnect,
                NetworkTimeout,
                ServerSelectionTimeoutError,
                ConnectionFailure,
                ExecutionTimeout,
            )
            
            mongodb_manager.connect()
            db = mongodb_manager.get_database()
            
            standard_upper = subdomain.upper().replace("-", "-")
            
            controls_cursor = db.compliance_controls.find(
                {"standard": {"$regex": standard_upper, "$options": "i"}},
                {"severity": 1}
            ).limit(100)
            
            severities = []
            for doc in controls_cursor:
                severity = doc.get("severity")
                if severity:
                    severities.append(severity.upper())
            
            if severities:
                high_count = sum(1 for s in severities if s in ["HIGH", "CRITICAL"])
                total_count = len(severities)
                
                if high_count / total_count > 0.5:
                    metadata["severity"] = "high"
                    metadata["security_level"] = "high"
                    metadata["threats_mitigated"] = ["data-breach", "unauthorized-access"]
                elif high_count / total_count > 0.2:
                    metadata["severity"] = "high"
                    metadata["security_level"] = "medium"
                    metadata["threats_mitigated"] = ["data-breach"]
                else:
                    metadata["severity"] = "medium"
                    metadata["security_level"] = "medium"
                
                logger.debug(
                    "Inferred metadata from %d controls for %s: severity=%s, security_level=%s",
                    total_count,
                    subdomain,
                    metadata["severity"],
                    metadata["security_level"],
                )
        
        except (
            AutoReconnect,
            NetworkTimeout,
            ServerSelectionTimeoutError,
            ConnectionFailure,
            ExecutionTimeout,
        ) as e:
            logger.warning(
                "MongoDB connection error while inferring metadata for subdomain %s: %s. "
                "Using default metadata.",
                subdomain,
                e,
            )
        except (ValueError, TypeError, KeyError, AttributeError, RuntimeError, ImportError) as e:
            logger.debug("Could not query standard metadata from MongoDB: %s", e)
        
        if metadata["severity"] == "medium" and metadata["security_level"] == "medium":
            metadata = self._get_standard_metadata_from_config(subdomain_lower, metadata)
        
        self._standard_metadata_cache[subdomain_lower] = metadata
        return metadata

    def _get_standard_metadata_from_config(
        self, subdomain: str, default_metadata: dict[str, Any]
    ) -> dict[str, Any]:
        """Get standard metadata from configuration file.
        
        Args:
            subdomain: Compliance subdomain (normalized)
            default_metadata: Default metadata dictionary
            
        Returns:
            Metadata dictionary with config-based values
        """
        try:
            from ..config.compliance_urls import COMPLIANCE_URLS
            
            standard_key = None
            for key in COMPLIANCE_URLS.keys():
                if key.lower().replace("-", "-") == subdomain.replace("-", "-"):
                    standard_key = key
                    break
            
            if not standard_key:
                return default_metadata
            
            config_metadata = {
                "severity": "high" if standard_key in ["HIPAA", "PCI-DSS"] else "medium",
                "security_level": "high" if standard_key in ["HIPAA", "PCI-DSS", "GDPR"] else "medium",
                "threats_mitigated": (
                    ["data-breach", "unauthorized-access"]
                    if standard_key in ["HIPAA", "PCI-DSS", "GDPR"]
                    else ["data-breach"]
                ),
                "applies_to_cloud": True,
            }
            
            logger.debug(
                "Using config metadata for %s: severity=%s, security_level=%s",
                subdomain,
                config_metadata["severity"],
                config_metadata["security_level"],
            )
            
            return config_metadata
        
        except (ImportError, AttributeError, KeyError) as e:
            logger.debug("Could not load config metadata: %s", e)
            return default_metadata

    def _get_default_categories_for_standard(self, subdomain: str) -> list[str]:
        """Get default compliance categories for a compliance standard.
        
        Queries MongoDB to find actual categories used by controls for this standard.
        Falls back to hardcoded defaults if no controls exist yet.
        
        Args:
            subdomain: Compliance subdomain (e.g., "hipaa", "pci-dss")
            
        Returns:
            List of default categories for the standard
        """
        try:
            from api.database.mongodb import mongodb_manager
            from pymongo.errors import (
                AutoReconnect,
                NetworkTimeout,
                ServerSelectionTimeoutError,
                ConnectionFailure,
                ExecutionTimeout,
            )
            
            mongodb_manager.connect()
            db = mongodb_manager.get_database()
            
            standard_upper = subdomain.upper().replace("-", "-")
            
            categories_cursor = db.compliance_controls.find(
                {"standard": {"$regex": standard_upper, "$options": "i"}},
                {"category": 1}
            ).limit(100)
            
            categories = set()
            for doc in categories_cursor:
                category = doc.get("category")
                if category:
                    category_normalized = category.lower().replace("-", "_").replace(" ", "_")
                    if category_normalized in self.resource_mapper.mapping:
                        categories.add(category_normalized)
            
            if categories:
                logger.debug(
                    "Found %d categories from actual controls for %s: %s",
                    len(categories),
                    subdomain,
                    list(categories),
                )
                return sorted(list(categories))
        
        except (
            AutoReconnect,
            NetworkTimeout,
            ServerSelectionTimeoutError,
            ConnectionFailure,
            ExecutionTimeout,
        ) as e:
            logger.warning(
                "MongoDB connection error while querying categories for subdomain %s: %s. "
                "Using default categories.",
                subdomain,
                e,
            )
        except (ValueError, TypeError, KeyError, AttributeError, RuntimeError, ImportError) as e:
            logger.debug("Could not query categories from MongoDB: %s", e)
        
        subdomain_lower = subdomain.lower()
        
        standard_to_categories = {
            "hipaa": ["data_protection", "access_control", "monitoring_testing", "backup_recovery"],
            "pci-dss": ["data_protection", "access_control", "monitoring_testing", "network_security"],
            "gdpr": ["data_protection", "access_control", "monitoring_testing", "backup_recovery"],
            "soc2": ["data_protection", "access_control", "monitoring_testing", "vulnerability_management"],
            "nist-800-53": ["data_protection", "access_control", "monitoring_testing", "network_security", "vulnerability_management"],
            "iso-27001": ["data_protection", "access_control", "monitoring_testing", "network_security", "backup_recovery"],
        }
        
        return standard_to_categories.get(subdomain_lower, ["data_protection", "access_control", "monitoring_testing"])

    def _requirement_to_category(self, requirement: str) -> str | None:
        """Map compliance requirement to category.
        
        Args:
            requirement: Requirement string (e.g., "encryption", "access_control")
            
        Returns:
            Category name or None
        """
        requirement_lower = requirement.lower().replace("-", "_").replace(" ", "_")
        
        requirement_to_category = {
            "encryption": "data_protection",
            "data_protection": "data_protection",
            "data_at_rest": "data_protection",
            "data_in_transit": "data_protection",
            "access_control": "access_control",
            "authentication": "access_control",
            "authorization": "access_control",
            "identity": "access_control",
            "logging": "monitoring_testing",
            "audit": "monitoring_testing",
            "monitoring": "monitoring_testing",
            "security_testing": "monitoring_testing",
            "backup_recovery": "backup_recovery",
            "backup": "backup_recovery",
            "disaster_recovery": "backup_recovery",
            "network_security": "network_security",
            "firewall": "network_security",
            "network_segmentation": "network_security",
            "vulnerability": "vulnerability_management",
            "patch": "vulnerability_management",
            "application_security": "application_security",
            "api_security": "application_security",
        }
        
        return requirement_to_category.get(requirement_lower)

    def _requirement_area_to_category(self, requirement_area: str) -> str | None:
        """Map requirement area to category.
        
        Args:
            requirement_area: Requirement area string
            
        Returns:
            Category name or None
        """
        return self._requirement_to_category(requirement_area)

    def _extract_compliance_categories(self, text: str) -> list[str]:
        """Extract compliance categories from text.
        
        Args:
            text: Lowercase text content
            
        Returns:
            List of compliance categories found in text
        """
        categories = []
        
        category_keywords = {
            "data_protection": [
                "data protection", "data at rest", "data in transit", "encryption",
                "ephi", "phi", "protected health information", "personal data",
                "sensitive data", "data security", "data encryption",
            ],
            "access_control": [
                "access control", "authentication", "authorization", "identity",
                "iam", "user access", "role", "permission", "access management",
            ],
            "monitoring_testing": [
                "monitoring", "logging", "audit", "audit trail", "log", "tracking",
                "security testing", "vulnerability", "assessment",
            ],
            "network_security": [
                "network security", "firewall", "network segmentation", "vpc",
                "network", "transmission", "communication", "network access",
            ],
            "backup_recovery": [
                "backup", "recovery", "disaster recovery", "data backup",
                "restore", "business continuity",
            ],
            "vulnerability_management": [
                "vulnerability", "patch", "antivirus", "security update",
                "secure systems",
            ],
            "application_security": [
                "application security", "api security", "container security",
                "serverless",
            ],
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in text for keyword in keywords):
                categories.append(category)
        
        return categories

    def _resources_to_services(self, resources: list[str]) -> list[str]:
        """Convert cloud resource identifiers to generic service names.
        
        Args:
            resources: List of cloud resource identifiers (e.g., "AWS::RDS::DBInstance")
            
        Returns:
            List of generic service names (e.g., ["database"])
        """
        service_mapping = {
            "database": [
                "rds", "dynamodb", "redshift", "sql", "database", "cosmosdb",
                "firestore", "bigtable", "nosql", "autonomous",
            ],
            "object-storage": [
                "s3", "storage", "blob", "bucket", "objectstorage", "filesystem",
                "efs", "fsx", "filestorage",
            ],
            "key-management": [
                "kms", "keyvault", "vault", "secretsmanager", "secret",
                "cryptokey", "keyring",
            ],
            "identity-management": [
                "iam", "cognito", "ad", "identity", "authorization", "policy",
                "role", "user", "serviceaccount",
            ],
            "monitoring": [
                "cloudwatch", "monitor", "logging", "log", "cloudtrail", "config",
                "operationalinsights", "metric", "alarm",
            ],
            "networking": [
                "vpc", "network", "subnet", "routetable", "loadbalancer",
                "firewall", "securitygroup", "networkacl", "gateway",
            ],
            "compute": [
                "ec2", "lambda", "compute", "instance", "function", "container",
                "eks", "gke", "aks", "ecs",
            ],
        }
        
        services = set()
        resources_lower = " ".join(resources).lower()
        
        for service_name, keywords in service_mapping.items():
            if any(keyword in resources_lower for keyword in keywords):
                services.add(service_name)
        
        return sorted(list(services))

    def _discover_related_items(
        self,
        article_id: str,
        subdomain: str,
        content: str,
        title: str,
        tags: list[str],
    ) -> dict[str, list[str]]:
        """Discover related articles and controls based on content similarity.
        
        Uses keyword matching and subdomain matching to find related items.
        This is a lightweight approach - full semantic search would require
        vector similarity queries (future enhancement).
        
        Args:
            article_id: Current article ID
            subdomain: Compliance subdomain
            content: Article content
            title: Article title
            tags: Article tags
            
        Returns:
            Dictionary with "articles" and "controls" lists
        """
        related_articles: list[str] = []
        related_controls: list[str] = []
        
        try:
            from api.database.mongodb import mongodb_manager
            from pymongo.errors import (
                AutoReconnect,
                NetworkTimeout,
                ServerSelectionTimeoutError,
                ConnectionFailure,
                ExecutionTimeout,
            )
            
            mongodb_manager.connect()
            db = mongodb_manager.get_database()
            
            text_keywords = set()
            title_words = set(title.lower().split())
            content_words = set(content.lower().split()[:100])
            tag_words = set(t.lower() for t in tags)
            
            text_keywords.update(title_words)
            text_keywords.update(content_words)
            text_keywords.update(tag_words)
            
            text_keywords = {w for w in text_keywords if len(w) > 4}
            
            if text_keywords:
                escaped_keywords = [re.escape(keyword) for keyword in list(text_keywords)[:10]]
                keyword_query = {"$or": [
                    {"title": {"$regex": keyword, "$options": "i"}}
                    for keyword in escaped_keywords
                ]}
                
                related_articles_cursor = db.knowledge_articles.find(
                    {
                        "$and": [
                            {"article_id": {"$ne": article_id}},
                            {"domain": "compliance"},
                            {"subdomain": subdomain},
                            keyword_query,
                        ]
                    },
                    {"article_id": 1}
                ).limit(5)
                
                related_articles = [doc["article_id"] for doc in related_articles_cursor]
            
            if subdomain:
                escaped_subdomain = re.escape(subdomain)
                related_controls_cursor = db.compliance_controls.find(
                    {
                        "standard": {"$regex": escaped_subdomain, "$options": "i"}
                    },
                    {"control_id": 1}
                ).limit(5)
                
                related_controls = [doc["control_id"] for doc in related_controls_cursor]
        
        except (
            AutoReconnect,
            NetworkTimeout,
            ServerSelectionTimeoutError,
            ConnectionFailure,
            ExecutionTimeout,
        ) as e:
            logger.warning(
                "MongoDB connection error while discovering related items (article_id=%s): %s. "
                "Continuing without related items.",
                article_id,
                e,
            )
        except (ValueError, TypeError, KeyError, AttributeError, RuntimeError, ImportError) as e:
            logger.debug("Could not discover related items: %s", e)
        
        return {
            "articles": related_articles,
            "controls": related_controls,
        }

    def _infer_compliance_impact(self, content: str, title: str, subdomain: str) -> dict[str, Any] | None:
        """Infer compliance impact from content.
        
        Args:
            content: Article content
            title: Article title
            subdomain: Compliance subdomain
            
        Returns:
            Compliance impact dictionary or None
        """
        text = f"{title} {content}".lower()
        
        standards = []
        if subdomain:
            subdomain_upper = subdomain.upper().replace("-", "-")
            if subdomain_upper not in standards:
                standards.append(subdomain_upper)
        
        if "hipaa" in text or "health insurance portability" in text:
            if "HIPAA" not in standards:
                standards.append("HIPAA")
        if "pci" in text or "payment card" in text:
            if "PCI-DSS" not in standards:
                standards.append("PCI-DSS")
        if "soc" in text or "service organization" in text:
            if "SOC2" not in standards:
                standards.append("SOC2")
        if "gdpr" in text or "general data protection" in text:
            if "GDPR" not in standards:
                standards.append("GDPR")
        if "nist" in text:
            if "NIST-800-53" not in standards:
                standards.append("NIST-800-53")
        if "iso" in text or "iso 27001" in text:
            if "ISO-27001" not in standards:
                standards.append("ISO-27001")
        
        if not standards:
            return None
        
        requirements = []
        if "encryption" in text or "encrypt" in text:
            requirements.append("encryption")
        if "access control" in text or "authentication" in text:
            requirements.append("access_control")
        if "logging" in text or "audit" in text:
            requirements.append("logging")
        if "backup" in text or "recovery" in text:
            requirements.append("backup_recovery")
        if "monitoring" in text or "alerting" in text:
            requirements.append("monitoring")
        
        severity = "medium"
        if standards:
            standard_metadata = self._get_standard_metadata(standards[0].lower().replace("-", "-"))
            severity = standard_metadata.get("severity", "medium")
        
        return {
            "standards": list(set(standards)),
            "requirements": list(set(requirements)) if requirements else None,
            "severity": severity,
        }

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
            "cost", "pricing", "price", "expensive", "cheap", "budget",
            "savings", "optimization", "reserved", "spot", "on-demand",
        ]
        
        if not any(indicator in text for indicator in cost_indicators):
            return None
        
        optimization_opportunities = []
        if "reserved" in text or "reserved instance" in text:
            optimization_opportunities.append("reserved-instances")
        if "spot" in text or "spot instance" in text:
            optimization_opportunities.append("spot-instances")
        if "rightsizing" in text or "right-sizing" in text:
            optimization_opportunities.append("rightsizing")
        if "auto-scaling" in text or "autoscaling" in text:
            optimization_opportunities.append("auto-scaling")
        
        return {
            "optimization_opportunities": optimization_opportunities if optimization_opportunities else None,
            "cost_category": "compliance" if "compliance" in text else "operational",
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
        
        threats_mitigated = []
        if "breach" in text or "data breach" in text:
            threats_mitigated.append("data-breach")
        if "unauthorized access" in text or "unauthorized" in text:
            threats_mitigated.append("unauthorized-access")
        if "malware" in text or "virus" in text:
            threats_mitigated.append("malware")
        if "ddos" in text or "denial of service" in text:
            threats_mitigated.append("ddos")
        if "phishing" in text:
            threats_mitigated.append("phishing")
        if "insider threat" in text or "insider" in text:
            threats_mitigated.append("insider-threat")
        
        if not threats_mitigated:
            return None
        
        return {
            "threats_mitigated": threats_mitigated,
            "security_level": "high" if len(threats_mitigated) > 2 else "medium",
        }

    def _generate_content_hash(self, content: str) -> str:
        """Generate SHA-256 hash of content.
        
        Args:
            content: Article content
            
        Returns:
            SHA-256 hash string
        """
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _generate_source_hash(self, source_url: str, raw_data: dict[str, Any]) -> str:
        """Generate SHA-256 hash of source data.
        
        Args:
            source_url: Source URL
            raw_data: Raw article data
            
        Returns:
            SHA-256 hash string
        """
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

    def extract_structured_data(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Extract domain-specific structured data.
        
        Args:
            raw_data: Raw data
            
        Returns:
            Structured data dictionary
        """
        structured_data: dict[str, Any] = {}

        compliance_type = raw_data.get("compliance_type") or "guidance"
        structured_data["compliance_type"] = compliance_type

        standards = raw_data.get("standards") or raw_data.get("compliance_standards") or []
        if standards:
            structured_data["standards"] = standards

        requirement_area = raw_data.get("requirement_area") or raw_data.get("category")
        if requirement_area:
            structured_data["requirement_area"] = requirement_area

        implementation_complexity = raw_data.get("implementation_complexity")
        if implementation_complexity:
            structured_data["implementation_complexity"] = implementation_complexity

        applies_to_industries = raw_data.get("applies_to_industries") or raw_data.get("industries")
        if applies_to_industries:
            structured_data["applies_to_industries"] = applies_to_industries

        return structured_data

    def _extract_subdomain(self, raw_data: dict[str, Any], source_url: str) -> str:
        """Extract subdomain from raw data or source URL.
        
        Args:
            raw_data: Raw data
            source_url: Source URL
            
        Returns:
            Subdomain string
        """
        subdomain = raw_data.get("subdomain") or raw_data.get("standard")

        if not subdomain:
            if "pci" in source_url.lower() or "pci" in raw_data.get("title", "").lower():
                subdomain = "pci-dss"
            elif "hipaa" in source_url.lower() or "hipaa" in raw_data.get("title", "").lower():
                subdomain = "hipaa"
            elif "soc" in source_url.lower() or "soc" in raw_data.get("title", "").lower():
                subdomain = "soc2"
            elif "nist" in source_url.lower() or "nist" in raw_data.get("title", "").lower():
                subdomain = "nist-800-53"
            elif "iso" in source_url.lower() or "iso" in raw_data.get("title", "").lower():
                subdomain = "iso-27001"
            elif "gdpr" in source_url.lower() or "gdpr" in raw_data.get("title", "").lower():
                subdomain = "gdpr"
            else:
                subdomain = "general"

        return subdomain.lower().replace("_", "-")

    def _infer_content_type(
        self, raw_data: dict[str, Any], content: str
    ) -> ContentType:
        """Infer content type from raw data and content.
        
        Args:
            raw_data: Raw data
            content: Article content
            
        Returns:
            ContentType enum
        """
        content_type_str = raw_data.get("content_type", "").lower()

        if content_type_str:
            try:
                return ContentType(content_type_str)
            except ValueError:
                pass

        content_lower = content.lower()

        if "pattern" in content_lower or "architecture pattern" in content_lower:
            return ContentType.PATTERN
        elif "checklist" in content_lower or "check list" in content_lower:
            return ContentType.CHECKLIST
        elif "strategy" in content_lower or "strategic" in content_lower:
            return ContentType.STRATEGY
        elif "best practice" in content_lower or "best practices" in content_lower:
            return ContentType.BEST_PRACTICE
        elif "reference" in content_lower or "documentation" in content_lower:
            return ContentType.REFERENCE
        else:
            return ContentType.GUIDE

    def _extract_title_from_content(self, content: str) -> str:
        """Extract title from content if not provided.
        
        Args:
            content: Article content
            
        Returns:
            Extracted title
        """
        lines = content.split("\n")
        for line in lines[:10]:
            line = line.strip()
            if line and len(line) > 10 and len(line) < 200:
                if line.startswith("#"):
                    return line.lstrip("#").strip()
                return line
        return "Untitled Compliance Guide"

    def _extract_summary_from_content(self, content: str) -> str:
        """Extract summary from content if not provided.
        
        Args:
            content: Article content
            
        Returns:
            Extracted summary
        """
        paragraphs = content.split("\n\n")
        for para in paragraphs[:3]:
            para = para.strip()
            if len(para) > 50 and len(para) < 500:
                return para
        return content[:500] if content else "No summary available"

    def _extract_references(
        self, raw_data: dict[str, Any], source_url: str
    ) -> list[Reference]:
        """Extract references from raw data.
        
        Args:
            raw_data: Raw data
            source_url: Source URL
            
        Returns:
            List of Reference objects
        """
        references = []

        if raw_data.get("references"):
            for ref_data in raw_data["references"]:
                if isinstance(ref_data, dict):
                    references.append(
                        Reference(
                            type=ref_data.get("type", "reference"),
                            url=ref_data.get("url", ""),
                            title=ref_data.get("title", ""),
                        )
                    )

        if source_url and not any(ref.url == source_url for ref in references):
            parsed = urlparse(source_url)
            references.append(
                Reference(
                    type="official" if parsed.netloc in ["pcisecuritystandards.org", "hhs.gov"] else "source",
                    url=source_url,
                    title=parsed.path.split("/")[-1] or "Source",
                )
            )

        return references

