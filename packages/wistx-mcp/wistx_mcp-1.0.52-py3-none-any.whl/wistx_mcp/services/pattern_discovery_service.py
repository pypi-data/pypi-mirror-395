"""Pattern Discovery Service - Phase 3: Extract patterns from quality templates.

Discovers integration patterns from high-quality repository templates and stores
them in the knowledge base for future use.
"""

import logging
import re
from typing import Any

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.vector_search import VectorSearch
from wistx_mcp.services.quality_scorer import QualityScorer
from data_pipelines.models.knowledge_article import ContentType, Domain, KnowledgeArticle
from api.services.github_service import GitHubService

logger = logging.getLogger(__name__)


class PatternDiscoveryService:
    """Service for discovering patterns from quality templates and repositories."""

    def __init__(self, mongodb_client: MongoDBClient, vector_search: VectorSearch):
        """Initialize pattern discovery service.

        Args:
            mongodb_client: MongoDB client for knowledge base access
            vector_search: Vector search instance for pattern matching
        """
        self.mongodb_client = mongodb_client
        self.vector_search = vector_search
        self.quality_scorer = QualityScorer()
        self.github_service = GitHubService()

    async def discover_patterns_from_repository(
        self,
        repository_url: str,
        integration_type: str,
        cloud_provider: str,
    ) -> list[dict[str, Any]]:
        """Discover patterns from a high-quality repository.

        Analyzes repository code to extract integration patterns and stores them
        in the knowledge base if they meet quality thresholds.

        Args:
            repository_url: GitHub repository URL
            integration_type: Type of integration to discover
            cloud_provider: Cloud provider context

        Returns:
            List of discovered pattern articles (already stored in knowledge base)
        """
        try:
            repo_info = await self.github_service.get_repository_info(repository_url)
            
            if repo_info.get("stars", 0) < 10:
                logger.warning(
                    "Repository %s has low stars (%d), skipping pattern discovery",
                    repository_url,
                    repo_info.get("stars", 0),
                )
                return []

            existing_patterns = await self.vector_search.search_knowledge_articles(
                query=f"{integration_type} {cloud_provider}",
                domains=[Domain.INFRASTRUCTURE.value],
                content_types=[ContentType.PATTERN.value],
                limit=50,
            )

            existing_pattern_names = {
                p.get("structured_data", {}).get("pattern_name", "")
                for p in existing_patterns
            }

            patterns = await self._extract_patterns_from_repo(
                repository_url,
                integration_type,
                cloud_provider,
                existing_pattern_names,
            )

            discovered_articles = []
            for pattern in patterns:
                if pattern.get("quality_score", 0) >= 70.0:
                    article = await self._create_pattern_article(pattern, repository_url)
                    if article:
                        await self.github_service._store_article(article)
                        discovered_articles.append(article.model_dump())
                        logger.info(
                            "Discovered and stored pattern: %s (quality: %.1f)",
                            pattern.get("name"),
                            pattern.get("quality_score", 0),
                        )

            return discovered_articles

        except Exception as e:
            logger.error(
                "Failed to discover patterns from repository %s: %s",
                repository_url,
                e,
                exc_info=True,
            )
            return []

    async def _extract_patterns_from_repo(
        self,
        repository_url: str,
        integration_type: str,
        cloud_provider: str,
        existing_pattern_names: set[str],
    ) -> list[dict[str, Any]]:
        """Extract patterns from repository code.

        Args:
            repository_url: Repository URL
            integration_type: Integration type
            cloud_provider: Cloud provider
            existing_pattern_names: Set of existing pattern names to avoid duplicates

        Returns:
            List of extracted patterns with quality scores
        """
        patterns = []

        try:
            repo_info = await self.github_service.get_repository_info(repository_url)
            repo_tree = await self.github_service.get_repository_tree(
                repository_url,
                branch=repo_info.get("default_branch", "main"),
            )

            integration_files = self._find_integration_files(repo_tree, integration_type, cloud_provider)

            for file_info in integration_files:
                file_content = await self.github_service.get_file_content(
                    repository_url,
                    file_info["path"],
                    repo_info.get("default_branch", "main"),
                )

                extracted_patterns = self._parse_pattern_from_code(
                    file_content,
                    file_info["path"],
                    integration_type,
                    cloud_provider,
                )

                for pattern in extracted_patterns:
                    if pattern.get("name") not in existing_pattern_names:
                        quality_score = self._score_extracted_pattern(pattern, repo_info)
                        pattern["quality_score"] = quality_score
                        patterns.append(pattern)

        except Exception as e:
            logger.error(
                "Failed to extract patterns from repository: %s",
                e,
                exc_info=True,
            )

        return patterns

    def _find_integration_files(
        self,
        repo_tree: list[dict[str, Any]],
        integration_type: str,
        cloud_provider: str,
    ) -> list[dict[str, Any]]:
        """Find files relevant to integration type.

        Args:
            repo_tree: Repository tree structure
            integration_type: Integration type
            cloud_provider: Cloud provider

        Returns:
            List of relevant file info dictionaries
        """
        relevant_files = []
        
        type_keywords = {
            "networking": ["network", "vpc", "subnet", "route", "peering", "vpn"],
            "security": ["security", "iam", "policy", "auth", "encrypt"],
            "service": ["service", "api", "gateway", "load", "balancer"],
            "monitoring": ["monitor", "metric", "log", "alert", "dashboard"],
        }

        keywords = type_keywords.get(integration_type, [])
        provider_keywords = {
            "aws": ["aws", "amazon", "cloudformation"],
            "gcp": ["gcp", "google", "gcloud"],
            "azure": ["azure", "microsoft"],
            "kubernetes": ["k8s", "kubernetes", "kube"],
        }
        keywords.extend(provider_keywords.get(cloud_provider, []))

        for item in repo_tree:
            path = item.get("path", "").lower()
            if any(keyword in path for keyword in keywords):
                if path.endswith((".tf", ".yaml", ".yml", ".json", ".py", ".ts", ".js")):
                    relevant_files.append(item)

        return relevant_files[:20]

    def _parse_pattern_from_code(
        self,
        code_content: str,
        file_path: str,
        integration_type: str,
        cloud_provider: str,
    ) -> list[dict[str, Any]]:
        """Parse pattern from code content.

        Args:
            code_content: File content
            file_path: File path
            integration_type: Integration type
            cloud_provider: Cloud provider

        Returns:
            List of extracted patterns
        """
        patterns = []

        pattern_name = self._extract_pattern_name(file_path, code_content)
        if not pattern_name:
            return patterns

        description = self._extract_description(code_content)
        components = self._extract_components(code_content, cloud_provider)
        dependencies = self._extract_dependencies(code_content)

        pattern = {
            "name": pattern_name,
            "description": description,
            "providers": [cloud_provider],
            "components": components,
            "dependencies": dependencies,
            "terraform_example": code_content if file_path.endswith(".tf") else "",
            "kubernetes_example": code_content if file_path.endswith((".yaml", ".yml")) else "",
            "source_file": file_path,
        }

        patterns.append(pattern)
        return patterns

    def _extract_pattern_name(self, file_path: str, code_content: str) -> str:
        """Extract pattern name from file path or code.

        Args:
            file_path: File path
            code_content: Code content

        Returns:
            Pattern name or empty string
        """
        path_parts = file_path.split("/")
        filename = path_parts[-1].replace(".tf", "").replace(".yaml", "").replace(".yml", "")
        
        if "_" in filename:
            return filename.replace("_", "_")
        elif "-" in filename:
            return filename.replace("-", "_")
        else:
            return filename.lower()

    def _extract_description(self, code_content: str) -> str:
        """Extract description from code comments or README.

        Args:
            code_content: Code content

        Returns:
            Description string
        """
        comment_patterns = [
            r"#\s*(.+?)(?:\n|$)",
            r"//\s*(.+?)(?:\n|$)",
            r"/\*\s*(.+?)\s*\*/",
        ]

        descriptions = []
        for pattern in comment_patterns:
            matches = re.findall(pattern, code_content, re.MULTILINE | re.DOTALL)
            descriptions.extend(matches[:5])

        if descriptions:
            return " ".join(descriptions[:3])[:500]

        return "Integration pattern extracted from code"

    def _extract_components(self, code_content: str, cloud_provider: str) -> list[str]:
        """Extract component names from code.

        Args:
            code_content: Code content
            cloud_provider: Cloud provider

        Returns:
            List of component names
        """
        components = []

        if cloud_provider == "aws":
            aws_resources = re.findall(r'resource\s+"aws_(\w+)"', code_content)
            components.extend([f"aws_{r}" for r in aws_resources[:5]])
        elif cloud_provider == "kubernetes":
            k8s_resources = re.findall(r"kind:\s*(\w+)", code_content, re.IGNORECASE)
            components.extend(k8s_resources[:5])

        return list(set(components))[:10]

    def _extract_dependencies(self, code_content: str) -> list[str]:
        """Extract dependencies from code.

        Args:
            code_content: Code content

        Returns:
            List of dependency descriptions
        """
        dependencies = []

        if "depends_on" in code_content:
            deps = re.findall(r'depends_on\s*=\s*\[(.+?)\]', code_content, re.DOTALL)
            dependencies.extend([f"Dependency: {d.strip()}" for d in deps[:3]])

        return dependencies

    def _score_extracted_pattern(self, pattern: dict[str, Any], repo_info: dict[str, Any]) -> float:
        """Score extracted pattern quality.

        Args:
            pattern: Pattern dictionary
            repo_info: Repository information

        Returns:
            Quality score (0-100)
        """
        score = 0.0

        if pattern.get("description") and len(pattern["description"]) > 100:
            score += 20.0

        if pattern.get("components"):
            score += 20.0

        if pattern.get("terraform_example") or pattern.get("kubernetes_example"):
            score += 30.0

        stars = repo_info.get("stars", 0)
        if stars >= 100:
            score += 15.0
        elif stars >= 50:
            score += 10.0
        elif stars >= 10:
            score += 5.0

        if repo_info.get("forks", 0) >= 10:
            score += 15.0

        return min(score, 100.0)

    async def _create_pattern_article(
        self,
        pattern: dict[str, Any],
        repository_url: str,
    ) -> KnowledgeArticle | None:
        """Create KnowledgeArticle from discovered pattern.

        Args:
            pattern: Pattern dictionary
            repository_url: Source repository URL

        Returns:
            KnowledgeArticle object or None if creation fails
        """
        try:
            integration_type = pattern.get("integration_type", "general")
            pattern_name = pattern.get("name", "unknown")
            article_id = f"pattern-discovered-{integration_type}-{pattern_name}"

            content_parts = [
                f"# {pattern_name.replace('_', ' ').title()} Pattern",
                "",
                pattern.get("description", ""),
            ]

            if pattern.get("terraform_example"):
                content_parts.append(f"\n## Terraform Example\n\n```hcl\n{pattern['terraform_example']}\n```")

            if pattern.get("kubernetes_example"):
                content_parts.append(f"\n## Kubernetes Example\n\n```yaml\n{pattern['kubernetes_example']}\n```")

            content = "\n".join(content_parts)

            article = KnowledgeArticle(
                article_id=article_id,
                domain=Domain.INFRASTRUCTURE,
                subdomain=integration_type,
                content_type=ContentType.PATTERN,
                title=f"{pattern_name.replace('_', ' ').title()} Integration Pattern (Discovered)",
                summary=pattern.get("description", "")[:500],
                content=content,
                structured_data={
                    "integration_type": integration_type,
                    "pattern_name": pattern_name,
                    "providers": pattern.get("providers", []),
                    "components": pattern.get("components", []),
                    "dependencies": pattern.get("dependencies", []),
                    "source_file": pattern.get("source_file", ""),
                    "discovered": True,
                    "discovery_source": repository_url,
                },
                tags=[integration_type, pattern_name, "discovered"],
                categories=[integration_type, "infrastructure", "integration", "discovered"],
                cloud_providers=pattern.get("providers", []),
                source_url=repository_url,
                version="1.0",
                visibility="global",
                source_type="discovered",
                quality_score=pattern.get("quality_score", 70.0),
            )

            return article

        except Exception as e:
            logger.error("Failed to create pattern article: %s", e, exc_info=True)
            return None

    async def get_discovery_summary(
        self,
        repository_url: str,
        integration_type: str,
    ) -> dict[str, Any]:
        """Get summary of pattern discovery for a repository.

        Args:
            repository_url: Repository URL
            integration_type: Integration type

        Returns:
            Discovery summary dictionary
        """
        patterns = await self.vector_search.search_knowledge_articles(
            query=f"{integration_type} discovered",
            domains=[Domain.INFRASTRUCTURE.value],
            content_types=[ContentType.PATTERN.value],
            limit=50,
        )

        discovered_patterns = [
            p for p in patterns
            if p.get("structured_data", {}).get("discovery_source") == repository_url
        ]

        return {
            "repository_url": repository_url,
            "integration_type": integration_type,
            "patterns_discovered": len(discovered_patterns),
            "patterns": [
                {
                    "name": p.get("structured_data", {}).get("pattern_name", ""),
                    "quality_score": p.get("quality_score", 0.0),
                }
                for p in discovered_patterns[:5]
            ],
        }

