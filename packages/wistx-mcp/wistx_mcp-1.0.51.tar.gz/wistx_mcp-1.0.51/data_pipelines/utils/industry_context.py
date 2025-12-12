"""Industry context engine for tailoring knowledge articles."""

from ..models.knowledge_article import Domain, KnowledgeArticle
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class IndustryContextEngine:
    """Tailors knowledge articles to specific industries."""

    INDUSTRY_PROFILES = {
        "healthcare": {
            "compliance_standards": ["HIPAA", "HITECH", "SOC2"],
            "cost_sensitivity": "high",
            "security_priority": "critical",
            "common_services": ["RDS", "S3", "Lambda"],
        },
        "finance": {
            "compliance_standards": ["PCI-DSS", "SOX", "GLBA", "FFIEC"],
            "cost_sensitivity": "medium",
            "security_priority": "critical",
            "common_services": ["RDS", "EKS", "VPC"],
        },
        "retail": {
            "compliance_standards": ["PCI-DSS", "CCPA", "GDPR"],
            "cost_sensitivity": "very_high",
            "security_priority": "high",
            "common_services": ["S3", "CloudFront", "Lambda"],
        },
        "saas": {
            "compliance_standards": ["SOC2", "GDPR", "CCPA"],
            "cost_sensitivity": "high",
            "security_priority": "high",
            "common_services": ["Lambda", "API Gateway", "DynamoDB"],
        },
        "enterprise": {
            "compliance_standards": ["SOC2", "ISO-27001", "NIST-800-53"],
            "cost_sensitivity": "medium",
            "security_priority": "critical",
            "common_services": ["EKS", "RDS", "VPC"],
        },
    }

    def tailor_article(self, article: KnowledgeArticle, industry: str) -> KnowledgeArticle:
        """Tailor article for specific industry.
        
        Args:
            article: Knowledge article to tailor
            industry: Industry name
            
        Returns:
            Tailored knowledge article
        """
        if industry not in self.INDUSTRY_PROFILES:
            logger.debug("Unknown industry: %s, returning article unchanged", industry)
            return article

        profile = self.INDUSTRY_PROFILES[industry]

        if article.domain == Domain.COMPLIANCE and article.structured_data.get("standards"):
            relevant_standards = [
                s
                for s in article.structured_data["standards"]
                if s in profile["compliance_standards"]
            ]
            if relevant_standards:
                article.structured_data["relevant_standards"] = relevant_standards

        if article.cost_impact:
            article.cost_impact["industry_context"] = profile["cost_sensitivity"]

        if article.services:
            relevant_services = [
                s for s in article.services if s in profile["common_services"]
            ]
            if relevant_services:
                article.services = relevant_services

        if industry not in article.industries:
            article.industries.append(industry)

        return article

    def get_relevant_industries(self, article: KnowledgeArticle) -> list[str]:
        """Get industries relevant to this article.
        
        Args:
            article: Knowledge article
            
        Returns:
            List of relevant industry names
        """
        relevant_industries = []

        for industry, profile in self.INDUSTRY_PROFILES.items():
            if article.domain == Domain.COMPLIANCE:
                if article.structured_data.get("standards"):
                    standards = article.structured_data["standards"]
                    if any(s in profile["compliance_standards"] for s in standards):
                        relevant_industries.append(industry)
            else:
                if article.services:
                    if any(s in profile["common_services"] for s in article.services):
                        relevant_industries.append(industry)

        return relevant_industries

