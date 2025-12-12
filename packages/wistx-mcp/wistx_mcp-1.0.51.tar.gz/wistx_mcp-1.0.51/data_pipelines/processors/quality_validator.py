"""Content quality validator for knowledge articles."""

from dataclasses import dataclass
from datetime import datetime

from ..models.knowledge_article import KnowledgeArticle
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class QualityScore:
    """Content quality score breakdown."""

    source_credibility: float
    completeness: float
    accuracy: float
    actionability: float
    freshness: float
    cross_domain_links: float
    industry_relevance: float
    overall_score: float


class ContentQualityValidator:
    """Validates content quality for knowledge articles."""

    SOURCE_CREDIBILITY_TIERS = {
        "tier_1": {
            "domains": [
                "aws.amazon.com",
                "cloud.google.com",
                "azure.microsoft.com",
                "pcisecuritystandards.org",
                "hhs.gov",
                "nih.gov",
                "privacyruleandresearch.nih.gov",
                "csrc.nist.gov",
                "iso.org",
                "finops.org",
            ],
            "score": 100.0,
        },
        "tier_2": {
            "domains": [
                "github.com/aws",
                "terraform.io",
                "cncf.io",
                "kubernetes.io",
                "owasp.org",
            ],
            "score": 85.0,
        },
        "tier_3": {
            "domains": ["medium.com", "dev.to", "stackoverflow.com"],
            "score": 70.0,
        },
    }

    def validate(self, article: KnowledgeArticle) -> QualityScore:
        """Validate article quality.
        
        Args:
            article: Knowledge article to validate
            
        Returns:
            QualityScore with breakdown
        """
        source_credibility = self._validate_source(article.source_url)
        completeness = self._check_completeness(article)
        accuracy = self._validate_accuracy(article)
        actionability = self._score_actionability(article)
        freshness = self._check_freshness(article)
        cross_domain_links = self._validate_links(article)
        industry_relevance = self._score_industry_relevance(article)

        overall_score = (
            source_credibility * 0.2
            + completeness * 0.15
            + accuracy * 0.2
            + actionability * 0.15
            + freshness * 0.1
            + cross_domain_links * 0.1
            + industry_relevance * 0.1
        )

        return QualityScore(
            source_credibility=source_credibility,
            completeness=completeness,
            accuracy=accuracy,
            actionability=actionability,
            freshness=freshness,
            cross_domain_links=cross_domain_links,
            industry_relevance=industry_relevance,
            overall_score=overall_score,
        )

    def _validate_source(self, source_url: str) -> float:
        """Validate source credibility.
        
        Args:
            source_url: Source URL
            
        Returns:
            Credibility score (0-100)
        """
        for tier_data in self.SOURCE_CREDIBILITY_TIERS.values():
            if any(domain in source_url for domain in tier_data["domains"]):
                return tier_data["score"]
        return 50.0

    def _check_completeness(self, article: KnowledgeArticle) -> float:
        """Check content completeness.
        
        Args:
            article: Knowledge article
            
        Returns:
            Completeness score (0-100)
        """
        required_fields = ["title", "summary", "content", "source_url"]
        present_fields = sum(1 for field in required_fields if getattr(article, field))
        return (present_fields / len(required_fields)) * 100.0

    def _validate_accuracy(self, article: KnowledgeArticle) -> float:
        """Validate accuracy (placeholder - requires expert review).
        
        Args:
            article: Knowledge article
            
        Returns:
            Accuracy score (0-100)
        """
        if article.source_credibility:
            return article.source_credibility
        return 70.0

    def _score_actionability(self, article: KnowledgeArticle) -> float:
        """Score actionability.
        
        For compliance/regulatory content, scores based on structured impact fields
        and compliance-specific keywords. For implementation content, uses
        implementation keywords.
        
        Args:
            article: Knowledge article
            
        Returns:
            Actionability score (0-100)
        """
        content_lower = article.content.lower()
        
        if article.domain == "compliance":
            compliance_keywords = [
                "require",
                "must",
                "shall",
                "compliance",
                "standard",
                "regulation",
                "rule",
                "requirement",
                "control",
                "mandatory",
            ]
            keyword_count = sum(1 for keyword in compliance_keywords if keyword in content_lower)
            
            structured_data_score = 0.0
            if article.compliance_impact:
                structured_data_score += 30.0
            if article.security_impact:
                structured_data_score += 20.0
            if article.cost_impact:
                structured_data_score += 10.0
            
            keyword_score = min(keyword_count * 5.0, 50.0)
            return min(keyword_score + structured_data_score, 100.0)
        
        actionability_keywords = [
            "implement",
            "configure",
            "enable",
            "set up",
            "create",
            "deploy",
            "install",
            "setup",
        ]
        keyword_count = sum(1 for keyword in actionability_keywords if keyword in content_lower)
        return min(keyword_count * 15.0, 100.0)

    def _check_freshness(self, article: KnowledgeArticle) -> float:
        """Check content freshness.
        
        Args:
            article: Knowledge article
            
        Returns:
            Freshness score (0-100)
        """
        days_since_update = (datetime.utcnow() - article.updated_at).days

        if days_since_update < 30:
            return 100.0
        elif days_since_update < 90:
            return 80.0
        elif days_since_update < 180:
            return 60.0
        else:
            return 40.0

    def _validate_links(self, article: KnowledgeArticle) -> float:
        """Validate cross-domain links.
        
        Args:
            article: Knowledge article
            
        Returns:
            Link score (0-100)
        """
        total_links = (
            len(article.related_articles)
            + len(article.related_controls)
            + len(article.related_code_examples)
        )
        return min(total_links * 10.0, 100.0)

    def _score_industry_relevance(self, article: KnowledgeArticle) -> float:
        """Score industry relevance.
        
        Args:
            article: Knowledge article
            
        Returns:
            Industry relevance score (0-100)
        """
        if article.industries:
            return 100.0
        return 50.0

