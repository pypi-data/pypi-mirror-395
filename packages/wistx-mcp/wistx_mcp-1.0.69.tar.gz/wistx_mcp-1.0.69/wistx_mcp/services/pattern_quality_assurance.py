"""Pattern Quality Assurance Service - Phase 4: Compare patterns against quality templates.

Provides quality assurance by comparing patterns against high-quality templates
and providing context-aware recommendations.
"""

import logging
from typing import Any

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.vector_search import VectorSearch
from wistx_mcp.services.quality_scorer import QualityScorer
from data_pipelines.models.knowledge_article import ContentType, Domain

logger = logging.getLogger(__name__)


class PatternQualityAssurance:
    """Service for quality assurance of patterns against quality templates."""

    def __init__(self, mongodb_client: MongoDBClient, vector_search: VectorSearch):
        """Initialize pattern quality assurance service.

        Args:
            mongodb_client: MongoDB client for knowledge base access
            vector_search: Vector search instance for template matching
        """
        self.mongodb_client = mongodb_client
        self.vector_search = vector_search
        self.quality_scorer = QualityScorer()

    async def assess_pattern(
        self,
        pattern_article: dict[str, Any],
        components: list[dict[str, Any]],
        cloud_provider: str,
    ) -> dict[str, Any]:
        """Assess pattern quality against quality templates.

        Compares pattern against high-quality templates and provides
        context-aware recommendations.

        Args:
            pattern_article: Pattern knowledge article
            components: Components to integrate
            cloud_provider: Cloud provider context

        Returns:
            Quality assurance assessment dictionary:
            - template_match_score: Score against best matching template (0-100)
            - template_comparison: Comparison with quality template
            - recommendations: Context-aware recommendations
            - quality_gaps: Identified quality gaps
            - meets_quality_standards: Boolean indicating if pattern meets standards
        """
        try:
            quality_templates = await self._find_quality_templates(
                pattern_article,
                components,
                cloud_provider,
            )

            if not quality_templates:
                return {
                    "template_match_score": 0.0,
                    "template_comparison": {},
                    "recommendations": [
                        "No quality templates found for comparison. Pattern quality assessment based on internal scoring only.",
                    ],
                    "quality_gaps": [],
                    "meets_quality_standards": pattern_article.get("quality_score", 0) >= 70.0,
                }

            best_template = quality_templates[0]
            comparison = self._compare_pattern_to_template(pattern_article, best_template)
            gaps = self._identify_quality_gaps(pattern_article, best_template)
            recommendations = self._generate_context_recommendations(
                pattern_article,
                best_template,
                components,
                cloud_provider,
            )

            template_match_score = comparison.get("overall_similarity", 0.0)
            meets_standards = (
                template_match_score >= 75.0 and
                pattern_article.get("quality_score", 0) >= 70.0 and
                len(gaps) <= 2
            )

            return {
                "template_match_score": template_match_score,
                "template_comparison": comparison,
                "recommendations": recommendations,
                "quality_gaps": gaps,
                "meets_quality_standards": meets_standards,
                "best_matching_template": {
                    "article_id": best_template.get("article_id"),
                    "title": best_template.get("title"),
                    "quality_score": best_template.get("quality_score", 0),
                },
            }

        except Exception as e:
            logger.error(
                "Failed to assess pattern quality: %s",
                e,
                exc_info=True,
            )
            return {
                "template_match_score": 0.0,
                "template_comparison": {},
                "recommendations": [f"Quality assessment failed: {str(e)}"],
                "quality_gaps": [],
                "meets_quality_standards": False,
            }

    async def _find_quality_templates(
        self,
        pattern_article: dict[str, Any],
        components: list[dict[str, Any]],
        cloud_provider: str,
    ) -> list[dict[str, Any]]:
        """Find quality templates for comparison.

        Searches for high-quality patterns (quality_score >= 85) that match
        the pattern's integration type and cloud provider.

        Args:
            pattern_article: Pattern article
            components: Components
            cloud_provider: Cloud provider

        Returns:
            List of quality template articles, sorted by relevance
        """
        structured_data = pattern_article.get("structured_data", {})
        integration_type = structured_data.get("integration_type", "")

        component_names = [comp.get("id", comp.get("type", "")) for comp in components]
        query = f"{integration_type} {cloud_provider} {' '.join(component_names[:3])}"

        templates = await self.vector_search.search_knowledge_articles(
            query=query,
            domains=[Domain.INFRASTRUCTURE.value],
            content_types=[ContentType.PATTERN.value],
            limit=20,
        )

        quality_templates = [
            t for t in templates
            if t.get("quality_score", 0) >= 85.0 and
            t.get("article_id") != pattern_article.get("article_id")
        ]

        quality_templates.sort(
            key=lambda x: (
                x.get("quality_score", 0) * 0.5 +
                x.get("relevance_score", 0) * 0.5
            ),
            reverse=True,
        )

        return quality_templates[:5]

    def _compare_pattern_to_template(
        self,
        pattern: dict[str, Any],
        template: dict[str, Any],
    ) -> dict[str, Any]:
        """Compare pattern against quality template.

        Args:
            pattern: Pattern article
            template: Quality template article

        Returns:
            Comparison dictionary with similarity scores
        """
        pattern_data = pattern.get("structured_data", {})
        template_data = template.get("structured_data", {})

        comparison = {
            "overall_similarity": 0.0,
            "description_similarity": 0.0,
            "components_similarity": 0.0,
            "dependencies_similarity": 0.0,
            "security_rules_similarity": 0.0,
            "monitoring_similarity": 0.0,
        }

        pattern_desc = pattern.get("summary", "") + " " + pattern.get("content", "")
        template_desc = template.get("summary", "") + " " + template.get("content", "")
        
        desc_similarity = self._calculate_text_similarity(pattern_desc, template_desc)
        comparison["description_similarity"] = desc_similarity

        pattern_components = set(pattern_data.get("components", []))
        template_components = set(template_data.get("components", []))
        if pattern_components or template_components:
            components_similarity = len(pattern_components & template_components) / max(
                len(pattern_components | template_components), 1
            ) * 100
            comparison["components_similarity"] = components_similarity

        pattern_deps = set(pattern_data.get("dependencies", []))
        template_deps = set(template_data.get("dependencies", []))
        if pattern_deps or template_deps:
            deps_similarity = len(pattern_deps & template_deps) / max(
                len(pattern_deps | template_deps), 1
            ) * 100
            comparison["dependencies_similarity"] = deps_similarity

        pattern_security = set(pattern_data.get("security_rules", []))
        template_security = set(template_data.get("security_rules", []))
        if pattern_security or template_security:
            security_similarity = len(pattern_security & template_security) / max(
                len(pattern_security | template_security), 1
            ) * 100
            comparison["security_rules_similarity"] = security_similarity

        pattern_monitoring = pattern_data.get("monitoring_config", {})
        template_monitoring = template_data.get("monitoring_config", {})
        monitoring_similarity = self._compare_monitoring_config(pattern_monitoring, template_monitoring)
        comparison["monitoring_similarity"] = monitoring_similarity

        comparison["overall_similarity"] = (
            desc_similarity * 0.3 +
            comparison["components_similarity"] * 0.25 +
            comparison["dependencies_similarity"] * 0.15 +
            comparison["security_rules_similarity"] * 0.15 +
            monitoring_similarity * 0.15
        )

        return comparison

    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity score.

        Args:
            text1: First text
            text2: Second text

        Returns:
            Similarity score (0-100)
        """
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = len(words1 & words2)
        union = len(words1 | words2)

        return (intersection / union) * 100 if union > 0 else 0.0

    def _compare_monitoring_config(
        self,
        config1: dict[str, Any],
        config2: dict[str, Any],
    ) -> float:
        """Compare monitoring configurations.

        Args:
            config1: First monitoring config
            config2: Second monitoring config

        Returns:
            Similarity score (0-100)
        """
        if not config1 and not config2:
            return 100.0

        metrics1 = set(config1.get("metrics", []))
        metrics2 = set(config2.get("metrics", []))
        alarms1 = set(config1.get("alarms", []))
        alarms2 = set(config2.get("alarms", []))

        metrics_sim = len(metrics1 & metrics2) / max(len(metrics1 | metrics2), 1) * 100 if (metrics1 or metrics2) else 50.0
        alarms_sim = len(alarms1 & alarms2) / max(len(alarms1 | alarms2), 1) * 100 if (alarms1 or alarms2) else 50.0

        return (metrics_sim + alarms_sim) / 2

    def _identify_quality_gaps(
        self,
        pattern: dict[str, Any],
        template: dict[str, Any],
    ) -> list[str]:
        """Identify quality gaps between pattern and template.

        Args:
            pattern: Pattern article
            template: Quality template article

        Returns:
            List of quality gap descriptions
        """
        gaps = []

        pattern_data = pattern.get("structured_data", {})
        template_data = template.get("structured_data", {})

        if not pattern_data.get("security_rules") and template_data.get("security_rules"):
            gaps.append("Missing security rules compared to quality template")

        if not pattern_data.get("monitoring_config") and template_data.get("monitoring_config"):
            gaps.append("Missing monitoring configuration compared to quality template")

        if not pattern_data.get("implementation_guidance") and template_data.get("implementation_guidance"):
            gaps.append("Missing implementation guidance compared to quality template")

        if not pattern_data.get("compliance_considerations") and template_data.get("compliance_considerations"):
            gaps.append("Missing compliance considerations compared to quality template")

        pattern_quality = pattern.get("quality_score", 0)
        template_quality = template.get("quality_score", 0)
        if pattern_quality < template_quality - 10:
            gaps.append(f"Quality score ({pattern_quality:.1f}) significantly lower than template ({template_quality:.1f})")

        return gaps

    def _generate_context_recommendations(
        self,
        pattern: dict[str, Any],
        template: dict[str, Any],
        components: list[dict[str, Any]],
        cloud_provider: str,
    ) -> list[str]:
        """Generate context-aware recommendations.

        Args:
            pattern: Pattern article
            template: Quality template article
            components: Components to integrate
            cloud_provider: Cloud provider

        Returns:
            List of recommendations
        """
        recommendations = []

        pattern_data = pattern.get("structured_data", {})
        template_data = template.get("structured_data", {})

        if not pattern_data.get("security_rules") and template_data.get("security_rules"):
            recommendations.append(
                f"Consider adding security rules similar to quality template for {cloud_provider} integration"
            )

        if not pattern_data.get("monitoring_config") and template_data.get("monitoring_config"):
            recommendations.append(
                "Add monitoring configuration to track integration health and performance"
            )

        component_names = [comp.get("id", comp.get("type", "")) for comp in components]
        if component_names:
            recommendations.append(
                f"Ensure pattern supports all components: {', '.join(component_names[:3])}"
            )

        if cloud_provider == "aws" and not pattern_data.get("terraform_example"):
            recommendations.append("Add Terraform example for AWS deployment")

        if cloud_provider == "kubernetes" and not pattern_data.get("kubernetes_example"):
            recommendations.append("Add Kubernetes manifest example for deployment")

        return recommendations

