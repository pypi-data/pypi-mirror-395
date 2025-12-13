"""Section organizer service - groups components into functional sections."""

import logging
from typing import Any, Optional
from collections import defaultdict

from api.models.documentation_section import DocumentationSection, SectionType
from api.database.mongodb import mongodb_manager
from api.exceptions import NotFoundError, AuthorizationError

logger = logging.getLogger(__name__)


class SectionOrganizer:
    """Organizes components into functional sections."""

    SECTION_PATTERNS = {
        SectionType.API: [
            "api",
            "openapi",
            "rest",
            "graphql",
            "rpc",
            "endpoint",
            "route",
            "handler",
            "controller",
            "service",
        ],
        SectionType.ARCHITECTURE: [
            "architecture",
            "design",
            "structure",
            "system",
            "component",
            "module",
            "layer",
        ],
        SectionType.COMPONENT_GROUP: [
            "control",
            "manager",
            "orchestrator",
            "scheduler",
            "controller",
            "agent",
            "worker",
        ],
        SectionType.WORKFLOW: [
            "workflow",
            "pipeline",
            "process",
            "lifecycle",
            "execution",
            "runtime",
        ],
        SectionType.CONFIGURATION: [
            "config",
            "setting",
            "parameter",
            "option",
            "environment",
            "variable",
        ],
        SectionType.SECURITY: [
            "security",
            "auth",
            "authorization",
            "authentication",
            "encryption",
            "certificate",
            "token",
        ],
        SectionType.COMPLIANCE: [
            "compliance",
            "policy",
            "enforcement",
            "audit",
            "governance",
            "regulation",
            "pci",
            "hipaa",
            "soc2",
            "gdpr",
            "cis",
            "nist",
        ],
        SectionType.FINOPS: [
            "cost",
            "budget",
            "pricing",
            "billing",
            "finops",
            "spend",
            "allocation",
            "optimization",
            "reservation",
            "savings",
            "tagging",
            "chargeback",
        ],
        SectionType.PLATFORM: [
            "platform",
            "developer",
            "internal",
            "self-service",
            "golden-path",
            "paved-road",
            "developer-experience",
            "dx",
            "internal-tooling",
            "platform-service",
        ],
        SectionType.SRE: [
            "sre",
            "reliability",
            "slo",
            "sli",
            "error-budget",
            "monitoring",
            "alerting",
            "incident",
            "oncall",
            "runbook",
            "postmortem",
            "toil",
        ],
        SectionType.INFRASTRUCTURE: [
            "infrastructure",
            "terraform",
            "cloudformation",
            "pulumi",
            "infrastructure-as-code",
            "iac",
            "provisioning",
            "infra",
        ],
        SectionType.AUTOMATION: [
            "automation",
            "ci",
            "cd",
            "pipeline",
            "workflow",
            "orchestration",
            "automated",
            "script",
        ],
    }

    def __init__(self):
        """Initialize section organizer."""
        self._db = None

    def _get_db(self):
        """Get MongoDB database instance."""
        if self._db is None:
            self._db = mongodb_manager.get_database()
        return self._db

    async def organize_components_into_sections(
        self,
        resource_id: str,
        user_id: str,
        commit_sha: Optional[str] = None,
        branch: Optional[str] = None,
    ) -> list[DocumentationSection]:
        """Organize components into functional sections.

        Args:
            resource_id: Resource ID
            user_id: User ID
            commit_sha: Commit SHA
            branch: Branch name

        Returns:
            List of created sections
        """
        db = self._get_db()
        articles_collection = db.knowledge_articles

        articles = list(articles_collection.find({
            "resource_id": resource_id,
            "user_id": user_id if user_id else {"$exists": False},
        }))

        if not articles:
            logger.info("No articles found for resource: %s", resource_id)
            return []

        section_groups = await self._detect_sections(articles)

        sections = []
        for section_data in section_groups:
            section = await self._create_section(
                resource_id=resource_id,
                user_id=user_id,
                section_data=section_data,
                commit_sha=commit_sha,
                branch=branch,
            )
            sections.append(section)

        logger.info(
            "Organized %d components into %d sections for resource %s",
            len(articles),
            len(sections),
            resource_id,
        )

        return sections

    async def _detect_sections(
        self,
        articles: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Detect sections from articles using pattern matching.

        Args:
            articles: List of article dictionaries

        Returns:
            List of section data dictionaries
        """
        pattern_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)

        for article in articles:
            title_lower = article.get("title", "").lower()
            summary_lower = article.get("summary", "").lower()
            content_lower = article.get("content", "").lower()
            tags_lower = [t.lower() for t in article.get("tags", [])]

            detected_type = self._detect_section_type(
                title_lower,
                summary_lower,
                content_lower,
                tags_lower,
            )

            section_key = self._generate_section_key(
                detected_type,
                title_lower,
                summary_lower,
            )

            pattern_groups[section_key].append(article)

        sections = []
        for section_key, group_articles in pattern_groups.items():
            if len(group_articles) < 2:
                continue

            section_type, keywords = self._parse_section_key(section_key)

            sections.append({
                "section_type": section_type,
                "keywords": keywords,
                "articles": group_articles,
                "title": self._generate_section_title(section_type, keywords, group_articles),
            })

        return sections

    def _detect_section_type(
        self,
        title: str,
        summary: str,
        content: str,
        tags: list[str],
    ) -> SectionType:
        """Detect section type from text content.

        Args:
            title: Article title (lowercase)
            summary: Article summary (lowercase)
            content: Article content (lowercase)
            tags: Article tags (lowercase)

        Returns:
            Detected section type
        """
        combined_text = f"{title} {summary} {content} {' '.join(tags)}"

        scores: dict[SectionType, float] = {}

        for section_type, patterns in self.SECTION_PATTERNS.items():
            score = 0.0
            for pattern in patterns:
                if pattern in combined_text:
                    score += 1.0

            if score > 0:
                scores[section_type] = score

        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]

        return SectionType.CUSTOM

    def _generate_section_key(
        self,
        section_type: SectionType,
        title: str,
        summary: str,
    ) -> str:
        """Generate section grouping key.

        Args:
            section_type: Section type
            title: Article title
            summary: Article summary

        Returns:
            Section key string
        """
        key_terms = []

        if "api" in title or "api" in summary:
            key_terms.append("api")
        if "control" in title or "control" in summary:
            key_terms.append("control")
        if "node" in title or "node" in summary:
            key_terms.append("node")
        if "plugin" in title or "plugin" in summary:
            key_terms.append("plugin")
        if "cost" in title or "cost" in summary or "budget" in title or "budget" in summary:
            key_terms.append("cost")
        if "platform" in title or "platform" in summary:
            key_terms.append("platform")
        if "sre" in title or "sre" in summary or "reliability" in title or "reliability" in summary:
            key_terms.append("sre")
        if "infrastructure" in title or "infrastructure" in summary or "terraform" in title or "terraform" in summary:
            key_terms.append("infrastructure")
        if "automation" in title or "automation" in summary or "ci" in title or "cd" in title:
            key_terms.append("automation")

        key_terms_str = "_".join(sorted(key_terms)) if key_terms else "general"

        return f"{section_type.value}_{key_terms_str}"

    def _parse_section_key(self, key: str) -> tuple[SectionType, list[str]]:
        """Parse section key into type and keywords.

        Args:
            key: Section key string

        Returns:
            Tuple of (section_type, keywords)
        """
        parts = key.split("_", 1)
        section_type = SectionType(parts[0])
        keywords = parts[1].split("_") if len(parts) > 1 else []

        return section_type, keywords

    def _generate_section_title(
        self,
        section_type: SectionType,
        keywords: list[str],
        articles: list[dict[str, Any]],
    ) -> str:
        """Generate section title.

        Args:
            section_type: Section type
            keywords: Keywords
            articles: Articles in section

        Returns:
            Section title
        """
        if articles:
            first_title = articles[0].get("title", "")
            words = first_title.split()
            if len(words) > 2:
                prefix = " ".join(words[:2])
                return f"{prefix} {section_type.value.replace('_', ' ').title()}"

        type_name = section_type.value.replace("_", " ").title()
        if keywords:
            keywords_str = " ".join(k.title() for k in keywords)
            return f"{keywords_str} {type_name}"

        return type_name

    async def _create_section(
        self,
        resource_id: str,
        user_id: str,
        section_data: dict[str, Any],
        commit_sha: Optional[str],
        branch: Optional[str],
    ) -> DocumentationSection:
        """Create section from section data.

        Args:
            resource_id: Resource ID
            user_id: User ID
            section_data: Section data dictionary
            commit_sha: Commit SHA
            branch: Branch name

        Returns:
            Created DocumentationSection
        """
        from api.services.section_summarizer import section_summarizer

        articles = section_data["articles"]
        article_ids = [a["_id"] for a in articles]

        summary = await section_summarizer.generate_section_summary(
            section_title=section_data["title"],
            articles=articles,
        )

        architecture_diagram, diagram_format = await self._generate_section_diagram(
            section_data=section_data,
            articles=articles,
        )

        section_id = f"sec_{resource_id}_{section_data['section_type'].value}_{len(article_ids)}"

        section = DocumentationSection(
            section_id=section_id,
            resource_id=resource_id,
            user_id=user_id,
            title=section_data["title"],
            summary=summary,
            section_type=section_data["section_type"],
            component_article_ids=article_ids,
            tags=section_data.get("keywords", []),
            commit_sha=commit_sha,
            branch=branch,
            architecture_diagram=architecture_diagram,
            architecture_diagram_format=diagram_format,
        )

        db = self._get_db()
        sections_collection = db.documentation_sections
        sections_collection.replace_one(
            {"_id": section_id},
            section.to_dict(),
            upsert=True,
        )

        articles_collection = db.knowledge_articles
        articles_collection.update_many(
            {"_id": {"$in": article_ids}},
            {"$set": {"section_id": section_id}},
        )

        return section

    async def _generate_section_diagram(
        self,
        section_data: dict[str, Any],
        articles: list[dict[str, Any]],
    ) -> tuple[Optional[str], Optional[str]]:
        """Generate architecture diagram for a section.

        Args:
            section_data: Section data dictionary
            articles: List of article dictionaries in section

        Returns:
            Tuple of (diagram_code, diagram_format) or (None, None) if generation fails
        """
        try:
            from wistx_mcp.tools.lib.infrastructure_visualizer import InfrastructureVisualizer

            visualizer = InfrastructureVisualizer()

            infrastructure_code_parts = []
            infrastructure_type = None

            for article in articles[:10]:
                content = article.get("content", "")
                source_url = article.get("source_url", "")

                if not content:
                    continue

                if ".tf" in source_url or "terraform" in content.lower():
                    infrastructure_type = "terraform"
                    infrastructure_code_parts.append(content[:5000])
                elif "apiVersion" in content or "kind:" in content:
                    infrastructure_type = "kubernetes"
                    infrastructure_code_parts.append(content[:5000])
                elif "dockerfile" in source_url.lower() or "FROM" in content:
                    infrastructure_type = "docker"
                    infrastructure_code_parts.append(content[:5000])

            if not infrastructure_code_parts:
                return None, None

            combined_code = "\n\n".join(infrastructure_code_parts[:3])

            visualization_result = await visualizer.generate_visualization(
                infrastructure_code=combined_code,
                infrastructure_type=infrastructure_type,
                visualization_type="architecture",
                format="mermaid",
                include_resources=True,
                include_networking=True,
                depth=2,
            )

            diagram = visualization_result.get("diagram")
            if diagram:
                return diagram, "mermaid"

            return None, None

        except Exception as e:
            logger.debug("Failed to generate section diagram: %s", e)
            return None, None

    async def get_sections_for_resource(
        self,
        resource_id: str,
        user_id: str,
    ) -> list[DocumentationSection]:
        """Get sections for a resource.

        Args:
            resource_id: Resource ID
            user_id: User ID

        Returns:
            List of sections for the resource
        """
        db = self._get_db()
        sections_collection = db.documentation_sections

        from bson import ObjectId

        sections = list(sections_collection.find({
            "resource_id": resource_id,
            "user_id": user_id,
        }).sort("title", 1))

        return [DocumentationSection.from_dict(s) for s in sections]

    async def group_results_by_section(
        self,
        results: list[dict[str, Any]],
        resource_ids: list[str],
        user_id: str,
    ) -> dict[str, Any]:
        """Group search results by section.

        Args:
            results: Search results (with article_id)
            resource_ids: Resource IDs
            user_id: User ID

        Returns:
            Dictionary with results grouped by section
        """
        db = self._get_db()
        sections_collection = db.documentation_sections

        from bson import ObjectId

        sections = list(sections_collection.find({
            "resource_id": {"$in": resource_ids},
            "user_id": user_id,
        }))

        article_to_section: dict[str, str] = {}
        for section_doc in sections:
            section = DocumentationSection.from_dict(section_doc)
            for article_id in section.component_article_ids:
                article_to_section[article_id] = section.section_id

        grouped: dict[str, list[dict[str, Any]]] = {}
        ungrouped: list[dict[str, Any]] = []

        for result in results:
            article_id = result.get("article_id") or result.get("_id")
            if article_id and article_id in article_to_section:
                section_id = article_to_section[article_id]
                if section_id not in grouped:
                    grouped[section_id] = []
                grouped[section_id].append(result)
            else:
                ungrouped.append(result)

        section_groups = []
        for section_doc in sections:
            section = DocumentationSection.from_dict(section_doc)
            if section.section_id in grouped:
                section_groups.append({
                    "section": section.model_dump(),
                    "results": grouped[section.section_id],
                    "count": len(grouped[section.section_id]),
                })

        return {
            "grouped": section_groups,
            "ungrouped": ungrouped,
            "total_sections": len(section_groups),
            "total_grouped": sum(len(g["results"]) for g in section_groups),
            "total_ungrouped": len(ungrouped),
        }

    async def export_section_as_document(
        self,
        section_id: str,
        user_id: str,
        include_toc: bool = True,
        include_diagrams: bool = True,
    ) -> dict[str, Any]:
        """Export a documentation section as a complete combined document.

        Combines the section summary with all component articles into a single
        cohesive document with table of contents and architecture diagrams.

        Args:
            section_id: Section ID to export
            user_id: User ID
            include_toc: Include table of contents
            include_diagrams: Include architecture diagrams

        Returns:
            Dictionary with:
            - content: Combined markdown content
            - title: Section title
            - component_count: Number of components included
            - metadata: Section metadata
        """
        from datetime import datetime

        db = self._get_db()
        sections_collection = db.documentation_sections
        articles_collection = db.knowledge_articles

        section_doc = sections_collection.find_one({"_id": section_id})
        if not section_doc:
            raise NotFoundError(
                message=f"Section not found: {section_id}",
                user_message="Section not found",
                error_code="SECTION_NOT_FOUND",
                details={"section_id": section_id}
            )

        section = DocumentationSection.from_dict(section_doc)

        if section.user_id != user_id:
            raise AuthorizationError(
                message="Section does not belong to user",
                user_message="You do not have permission to access this section",
                error_code="SECTION_ACCESS_DENIED",
                details={"section_id": section_id, "user_id": user_id, "section_user_id": section.user_id}
            )

        articles = list(articles_collection.find({
            "_id": {"$in": section.component_article_ids},
        }))

        markdown = f"# {section.title}\n\n"
        markdown += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        markdown += f"**Section Type**: {section.section_type.value}\n\n"
        markdown += f"**Components**: {len(articles)}\n\n"

        if section.tags:
            markdown += f"**Tags**: {', '.join(section.tags)}\n\n"

        markdown += "---\n\n"

        toc_entries = []

        markdown += "## Overview\n\n"
        toc_entries.append(("Overview", 2))

        if section.summary:
            markdown += f"{section.summary}\n\n"
        else:
            markdown += f"This section contains {len(articles)} components related to {section.title}.\n\n"

        if include_diagrams and section.architecture_diagram:
            markdown += "## Architecture\n\n"
            toc_entries.append(("Architecture", 2))
            diagram_format = section.architecture_diagram_format or "mermaid"
            markdown += f"```{diagram_format}\n{section.architecture_diagram}\n```\n\n"

        markdown += "---\n\n"

        markdown += "## Components\n\n"
        toc_entries.append(("Components", 2))

        for i, article in enumerate(articles, 1):
            article_title = article.get("title", f"Component {i}")
            article_summary = article.get("summary", "")
            article_content = article.get("content", "")
            source_url = article.get("source_url", "")

            markdown += f"### {article_title}\n\n"
            toc_entries.append((article_title, 3))

            if source_url:
                markdown += f"**Source**: [{source_url}]({source_url})\n\n"

            if article_summary:
                markdown += f"{article_summary}\n\n"

            compliance_status = article.get("compliance_status", {})
            if compliance_status:
                markdown += "#### Compliance\n\n"
                markdown += "| Standard | Status |\n"
                markdown += "|----------|--------|\n"
                for standard, status in compliance_status.items():
                    status_icon = "✅" if status == "compliant" else "⚡" if status == "partial" else "⚠️"
                    markdown += f"| {standard} | {status_icon} {status} |\n"
                markdown += "\n"

            cost_impact = article.get("cost_impact", {})
            if cost_impact and cost_impact.get("monthly_estimate"):
                markdown += "#### Cost Impact\n\n"
                markdown += f"**Monthly Estimate**: {cost_impact.get('monthly_estimate')}\n\n"

            if article_content and len(article_content) < 5000:
                markdown += "#### Details\n\n"
                markdown += f"{article_content}\n\n"

            markdown += "---\n\n"

        if include_toc and toc_entries:
            toc_markdown = "## Table of Contents\n\n"
            for title, level in toc_entries:
                indent = "  " * (level - 2)
                anchor = title.lower().replace(" ", "-").replace("/", "").replace("(", "").replace(")", "")
                toc_markdown += f"{indent}- [{title}](#{anchor})\n"
            toc_markdown += "\n"

            insert_pos = markdown.find("---\n\n") + 5
            markdown = markdown[:insert_pos] + toc_markdown + markdown[insert_pos:]

        return {
            "content": markdown,
            "title": section.title,
            "section_id": section_id,
            "section_type": section.section_type.value,
            "component_count": len(articles),
            "metadata": {
                "resource_id": section.resource_id,
                "commit_sha": section.commit_sha,
                "branch": section.branch,
                "tags": section.tags,
                "generated_at": datetime.now().isoformat(),
            },
        }


section_organizer = SectionOrganizer()

