"""Documentation analyzer service - analyzes documentation content and generates rich articles.

Uses Claude Opus for analysis generation (same as repository indexing) and integrates with
compliance and cost tools for comprehensive documentation analysis.
"""

import asyncio
import hashlib
import json
import logging
from asyncio import TimeoutError as AsyncTimeoutError
from datetime import datetime
from typing import Any, Callable, Optional

try:
    from anthropic import AsyncAnthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    AsyncAnthropic = None

from api.config import settings
from api.services.compliance_service import ComplianceService
from api.models.v1_requests import ComplianceRequirementsRequest
from wistx_mcp.tools import pricing
from wistx_mcp.tools.lib.retry_utils import with_retry
from wistx_mcp.tools.lib.metrics import track_tool_metrics
from data_pipelines.models.knowledge_article import (
    ContentType,
    Domain,
    KnowledgeArticle,
)

logger = logging.getLogger(__name__)


class DocumentationAnalyzer:
    """Analyzes documentation content and generates rich knowledge articles.
    
    Uses the same Claude Opus model as CodeAnalyzer for consistent quality.
    Integrates with compliance and cost tools for enriched analysis.
    """

    def __init__(self):
        """Initialize documentation analyzer with compliance and cost services."""
        self.compliance_service = ComplianceService()
        self.pricing_tool = pricing
        
        if not ANTHROPIC_AVAILABLE:
            logger.warning(
                "anthropic package not installed. Documentation analysis will fail. "
                "Install with: pip install anthropic"
            )
            self.llm_client = None
            self.model = None
        else:
            anthropic_api_key = getattr(settings, "anthropic_api_key", None)
            if not anthropic_api_key:
                logger.warning(
                    "ANTHROPIC_API_KEY not set. Documentation analysis will fail. "
                    "Set ANTHROPIC_API_KEY in .env file."
                )
                self.llm_client = None
                self.model = None
            else:
                self.llm_client = AsyncAnthropic(api_key=anthropic_api_key)
                self.model = "claude-opus-4-1"
        
        self.temperature = 0.1
        self.max_tokens = 8000
        self.llm_timeout_seconds = 120.0
        self.max_content_length = 100000
        self.chunk_size = 30000
        self.chunk_overlap = 2000

    def _chunk_content(self, content: str) -> list[str]:
        """Intelligently chunk content for LLM processing.
        
        Args:
            content: Content to chunk
            
        Returns:
            List of content chunks
        """
        if len(content) <= self.chunk_size:
            return [content]

        chunks = []
        lines = content.split("\n")
        current_chunk = []
        current_size = 0

        for line in lines:
            line_size = len(line) + 1

            # Check for section headers (markdown)
            if line.startswith("#") and current_size >= self.chunk_size * 0.7:
                if current_chunk:
                    chunks.append("\n".join(current_chunk))
                    # Keep some overlap
                    overlap_lines = current_chunk[-self.chunk_overlap // 50:]
                    current_chunk = overlap_lines + [line]
                    current_size = sum(len(l) + 1 for l in current_chunk)
            elif current_size + line_size > self.chunk_size:
                if current_chunk:
                    chunks.append("\n".join(current_chunk))
                    overlap_lines = current_chunk[-self.chunk_overlap // 50:]
                    current_chunk = overlap_lines + [line]
                    current_size = sum(len(l) + 1 for l in current_chunk)
            else:
                current_chunk.append(line)
                current_size += line_size

        if current_chunk:
            chunks.append("\n".join(current_chunk))

        return chunks

    def _compute_content_hash(self, content: str) -> str:
        """Compute hash for content to enable incremental updates.
        
        Args:
            content: Content to hash
            
        Returns:
            SHA256 hash string
        """
        return hashlib.sha256(content.encode()).hexdigest()

    async def get_compliance_for_topics(
        self,
        topics: list[str],
        standards: list[str] | None = None,
    ) -> dict[str, Any]:
        """Get compliance requirements for documentation topics.
        
        Args:
            topics: List of topics/technologies mentioned
            standards: Optional list of compliance standards to check
            
        Returns:
            Dictionary with compliance data
        """
        if not topics:
            return {
                "controls": [],
                "summary": {"total": 0, "by_standard": {}, "by_severity": {}},
            }

        # Map topics to resource types for compliance lookup
        topic_to_resource = {
            "kubernetes": "container",
            "docker": "container",
            "aws": "cloud",
            "azure": "cloud",
            "gcp": "cloud",
            "database": "database",
            "encryption": "security",
            "authentication": "identity",
            "networking": "network",
            "storage": "storage",
            "api": "api",
            "serverless": "function",
        }
        
        resource_types = []
        for topic in topics:
            topic_lower = topic.lower()
            for key, resource_type in topic_to_resource.items():
                if key in topic_lower:
                    resource_types.append(resource_type)
                    break

        resource_types = list(set(resource_types)) or ["cloud"]

        try:
            request = ComplianceRequirementsRequest(
                resource_types=resource_types,
                standards=standards or [],
                include_remediation=True,
                include_verification=True,
            )

            response = await self.compliance_service.get_compliance_requirements(request)

            def _serialize_remediation(remediation: Any) -> dict | None:
                """Safely serialize remediation data."""
                if remediation is None:
                    return None
                if isinstance(remediation, dict):
                    return remediation
                if hasattr(remediation, "model_dump"):
                    return remediation.model_dump()
                if hasattr(remediation, "__dict__"):
                    return remediation.__dict__
                return {"value": str(remediation)}

            return {
                "controls": [
                    {
                        "control_id": c.control_id,
                        "standard": c.standard,
                        "title": c.title,
                        "description": c.description,
                        "severity": c.severity,
                        "applies_to": c.applies_to or [],
                        "remediation": _serialize_remediation(c.remediation),
                    }
                    for c in response.controls
                ],
                "summary": {
                    "total": response.summary.total,
                    "by_standard": response.summary.by_standard,
                    "by_severity": response.summary.by_severity,
                },
            }
        except Exception as e:
            logger.error("Error getting compliance for topics: %s", e, exc_info=True)
            return {
                "controls": [],
                "summary": {"total": 0, "by_standard": {}, "by_severity": {}},
                "error": str(e),
            }

    async def calculate_costs_for_services(
        self,
        services: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Calculate costs for services mentioned in documentation.

        Args:
            services: List of service specifications

        Returns:
            Dictionary with cost breakdown
        """
        if not services:
            return {
                "total_monthly": 0.0,
                "total_annual": 0.0,
                "breakdown": [],
                "optimizations": [],
            }

        try:
            result = await self.pricing_tool.calculate_infrastructure_cost(services)

            return {
                "total_monthly": result.get("total_monthly", 0.0),
                "total_annual": result.get("total_annual", 0.0),
                "breakdown": result.get("breakdown", []),
                "optimizations": result.get("optimizations", []),
            }
        except Exception as e:
            logger.error("Error calculating costs: %s", e, exc_info=True)
            return {
                "total_monthly": 0.0,
                "total_annual": 0.0,
                "breakdown": [],
                "optimizations": [],
                "error": str(e),
            }

    async def _extract_topics_and_services(
        self,
        content: str,
        source_url: str,
    ) -> dict[str, Any]:
        """Extract topics and services from documentation content.

        Args:
            content: Documentation content
            source_url: Source URL

        Returns:
            Dictionary with topics, services, and metadata
        """
        if not self.llm_client:
            return self._fallback_extract_topics(content)

        prompt = f"""Analyze this documentation content and extract key information.

Source: {source_url}

Content:
{content[:30000]}

Extract:
1. **Topics**: Main topics/technologies discussed (e.g., kubernetes, terraform, aws, security)
2. **Services**: Cloud services mentioned with provider (e.g., {{"provider": "aws", "service": "s3"}})
3. **Industries**: Industries this documentation applies to
4. **Compliance**: Any compliance standards mentioned (SOC2, PCI-DSS, HIPAA, etc.)
5. **Content Type**: Type of documentation (guide, reference, tutorial, best_practice, architecture)

Return JSON:
{{
    "topics": ["topic1", "topic2"],
    "services": [
        {{"provider": "aws", "service": "s3", "type": "storage"}},
        {{"provider": "azure", "service": "blob", "type": "storage"}}
    ],
    "industries": ["healthcare", "finance"],
    "compliance_standards": ["SOC2", "PCI-DSS"],
    "content_type": "guide",
    "key_concepts": ["concept1", "concept2"],
    "architecture_patterns": ["pattern1", "pattern2"]
}}
"""

        try:
            async with asyncio.timeout(60.0):
                response = await self.llm_client.messages.create(
                    model=self.model,
                    max_tokens=2000,
                    temperature=self.temperature,
                    messages=[{"role": "user", "content": prompt}],
                )

            response_text = response.content[0].text if response.content else ""

            if not response_text:
                return self._fallback_extract_topics(content)

            try:
                # Clean up response - sometimes LLM adds markdown
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0]
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0]

                return json.loads(response_text)
            except json.JSONDecodeError:
                return self._fallback_extract_topics(content)
        except Exception as e:
            logger.warning("Error extracting topics: %s", e)
            return self._fallback_extract_topics(content)

    def _fallback_extract_topics(self, content: str) -> dict[str, Any]:
        """Fallback topic extraction using keyword matching.

        Args:
            content: Content to analyze

        Returns:
            Dictionary with extracted topics
        """
        content_lower = content.lower()

        topic_keywords = {
            "kubernetes": ["kubernetes", "k8s", "kubectl", "pod", "deployment"],
            "docker": ["docker", "container", "dockerfile", "compose"],
            "terraform": ["terraform", "hcl", "tfvars", "provider"],
            "aws": ["aws", "amazon", "ec2", "s3", "lambda", "rds"],
            "azure": ["azure", "microsoft cloud", "blob storage"],
            "gcp": ["gcp", "google cloud", "bigquery", "cloud storage"],
            "security": ["security", "encryption", "authentication", "authorization"],
            "networking": ["network", "vpc", "subnet", "firewall", "load balancer"],
            "database": ["database", "sql", "nosql", "mongodb", "postgresql"],
            "ci/cd": ["ci/cd", "pipeline", "jenkins", "github actions", "gitlab ci"],
        }

        topics = []
        for topic, keywords in topic_keywords.items():
            if any(kw in content_lower for kw in keywords):
                topics.append(topic)

        return {
            "topics": topics or ["general"],
            "services": [],
            "industries": [],
            "compliance_standards": [],
            "content_type": "guide",
            "key_concepts": [],
            "architecture_patterns": [],
        }

    @track_tool_metrics(tool_name="documentation_analyzer.analyze_documentation")
    async def analyze_documentation(
        self,
        content: str,
        source_url: str,
        title: str | None = None,
        doc_context: dict[str, Any] | None = None,
        activity_callback: Callable[[str, str, dict[str, Any] | None], None] | None = None,
    ) -> list[KnowledgeArticle]:
        """Analyze documentation content and generate rich knowledge articles.

        Args:
            content: Documentation content (markdown or text)
            source_url: Source URL or file path
            title: Optional title for the documentation
            doc_context: Documentation context (resource_id, user_id, etc.)
            activity_callback: Optional callback for activity logging

        Returns:
            List of KnowledgeArticle objects
        """
        doc_context = doc_context or {}

        if activity_callback:
            activity_callback(
                "ANALYSIS_STARTED",
                f"Starting analysis of {source_url}",
                {"content_length": len(content)},
            )

        # Extract topics and services
        extracted_info = await self._extract_topics_and_services(content, source_url)

        if activity_callback:
            activity_callback(
                "TOPICS_EXTRACTED",
                f"Extracted {len(extracted_info.get('topics', []))} topics",
                {"topics": extracted_info.get("topics", [])},
            )

        # Get compliance data for topics
        compliance_data = await self.get_compliance_for_topics(
            topics=extracted_info.get("topics", []),
            standards=extracted_info.get("compliance_standards") or doc_context.get("compliance_standards"),
        )

        # Get cost data for services
        cost_data = await self.calculate_costs_for_services(
            services=extracted_info.get("services", []),
        )

        # Chunk content if needed
        chunks = self._chunk_content(content)

        if activity_callback:
            activity_callback(
                "PROCESSING_CHUNKS",
                f"Processing {len(chunks)} content chunks",
                {"chunk_count": len(chunks)},
            )

        # Analyze each chunk
        all_articles = []
        for i, chunk in enumerate(chunks):
            if activity_callback:
                activity_callback(
                    "ANALYZING_CHUNK",
                    f"Analyzing chunk {i + 1}/{len(chunks)}",
                    {"chunk_index": i, "chunk_size": len(chunk)},
                )

            articles = await self._analyze_chunk(
                chunk=chunk,
                chunk_index=i,
                total_chunks=len(chunks),
                source_url=source_url,
                title=title,
                extracted_info=extracted_info,
                compliance_data=compliance_data,
                cost_data=cost_data,
                doc_context=doc_context,
            )
            all_articles.extend(articles)

        if activity_callback:
            activity_callback(
                "ANALYSIS_COMPLETE",
                f"Generated {len(all_articles)} articles",
                {"article_count": len(all_articles)},
            )

        return all_articles

    async def _analyze_chunk(
        self,
        chunk: str,
        chunk_index: int,
        total_chunks: int,
        source_url: str,
        title: str | None,
        extracted_info: dict[str, Any],
        compliance_data: dict[str, Any],
        cost_data: dict[str, Any],
        doc_context: dict[str, Any],
    ) -> list[KnowledgeArticle]:
        """Analyze a single chunk of documentation.

        Args:
            chunk: Content chunk
            chunk_index: Index of this chunk
            total_chunks: Total number of chunks
            source_url: Source URL
            title: Optional title
            extracted_info: Extracted topics and services
            compliance_data: Compliance data from tool
            cost_data: Cost data from tool
            doc_context: Documentation context

        Returns:
            List of KnowledgeArticle objects
        """
        if not self.llm_client:
            return self._fallback_analyze(chunk, source_url, title, doc_context)

        chunk_info = ""
        if total_chunks > 1:
            chunk_info = f"\n\nNote: This is section {chunk_index + 1} of {total_chunks}. Extract knowledge articles from this section."

        prompt = self._build_analysis_prompt(
            content=chunk,
            source_url=source_url,
            title=title,
            extracted_info=extracted_info,
            compliance_data=compliance_data,
            cost_data=cost_data,
            chunk_info=chunk_info,
        )

        try:
            async def call_llm():
                async with asyncio.timeout(self.llm_timeout_seconds):
                    return await self.llm_client.messages.create(
                        model=self.model,
                        max_tokens=self.max_tokens,
                        temperature=self.temperature,
                        messages=[{"role": "user", "content": prompt}],
                    )

            response = await with_retry(
                call_llm,
                max_attempts=3,
                initial_delay=1.0,
                max_delay=10.0,
                backoff_multiplier=2.0,
                retryable_exceptions=(TimeoutError, ConnectionError, RuntimeError),
            )

            response_text = response.content[0].text if response.content else ""

            if not response_text:
                logger.warning("Empty response from LLM for documentation analysis")
                return self._fallback_analyze(chunk, source_url, title, doc_context)

            return self._parse_analysis_response(
                response_text=response_text,
                source_url=source_url,
                extracted_info=extracted_info,
                doc_context=doc_context,
            )
        except AsyncTimeoutError:
            logger.error("Timeout analyzing chunk %d of %s", chunk_index + 1, source_url)
            return self._fallback_analyze(chunk, source_url, title, doc_context)
        except Exception as e:
            logger.error("Error analyzing chunk %d: %s", chunk_index + 1, e, exc_info=True)
            return self._fallback_analyze(chunk, source_url, title, doc_context)

    def _build_analysis_prompt(
        self,
        content: str,
        source_url: str,
        title: str | None,
        extracted_info: dict[str, Any],
        compliance_data: dict[str, Any],
        cost_data: dict[str, Any],
        chunk_info: str,
    ) -> str:
        """Build the analysis prompt for Claude Opus.

        Args:
            content: Content to analyze
            source_url: Source URL
            title: Optional title
            extracted_info: Extracted topics and services
            compliance_data: Compliance data
            cost_data: Cost data
            chunk_info: Chunk information

        Returns:
            Prompt string
        """
        return f"""You are an expert documentation analyst. Analyze this documentation and generate comprehensive, professional knowledge articles.

Source: {source_url}
Title: {title or "Not specified"}
Topics: {json.dumps(extracted_info.get("topics", []))}
Content Type: {extracted_info.get("content_type", "guide")}
{chunk_info}

Documentation Content:
{content[:40000]}

Compliance Requirements (from WISTX compliance database):
{json.dumps(compliance_data, indent=2)}

Cost Analysis (from WISTX pricing database):
{json.dumps(cost_data, indent=2)}

Generate detailed, professional knowledge articles from this documentation. Your output should be rich and comprehensive, utilizing all appropriate markdown features.

## CONTENT REQUIREMENTS FOR EACH ARTICLE:

### 1. Overview
- Clear description of what this documentation covers
- Target audience and prerequisites

### 2. Key Concepts
- Main concepts explained with examples
- Include RELEVANT CODE SNIPPETS where they help illustrate:
  - Configuration examples
  - Implementation patterns
  - Command examples
- Format code blocks with appropriate language tags (```yaml, ```bash, ```python, etc.)

### 3. Compliance Mapping (if applicable)
Use compliance_data provided above. Present as a TABLE:
| Control | Standard | Relevance |
|---------|----------|-----------|
| Control ID | Standard Name | How this documentation relates |

### 4. Cost Implications (if applicable)
Use cost_data provided above. Include:
- Cost breakdown TABLE if services are mentioned
- Cost optimization recommendations

### 5. Architecture Diagram (if applicable)
Include a Mermaid diagram showing relationships:
```mermaid
graph TD
    A[Component] --> B[Dependency]
```

### 6. Best Practices
Present as a checklist TABLE:
| Practice | Description | Priority |
|----------|-------------|----------|
| Practice name | Description | High/Medium/Low |

### 7. Implementation Steps (if applicable)
- Step-by-step instructions with code examples
- Common pitfalls and solutions

## FORMATTING GUIDELINES:
- Use tables for structured comparisons and data
- Use code blocks with language tags for all code/config snippets
- Use Mermaid diagrams for architecture visualization
- Use task lists (- [ ] / - [x]) for checklists
- Use blockquotes for important notes
- Use headers (##, ###) for clear section organization
- DO NOT use emojis - use professional language only

## CODE SNIPPET POLICY:
- Include code snippets that illustrate key concepts
- Include command examples where relevant
- Include configuration examples
- Format all code with appropriate syntax highlighting

## DATA USAGE:
- Use compliance_data provided (from WISTX compliance tool) - do not generate generic compliance info
- Use cost_data provided (from WISTX pricing tool) - do not estimate costs manually
- Reference specific controls, costs, and findings from the provided data

Return JSON with multiple articles:
{{
    "articles": [
        {{
            "title": "Clear, descriptive title",
            "summary": "50-200 word professional summary",
            "content": "Full markdown content with tables, code snippets, and diagrams as appropriate",
            "content_type": "guide|reference|tutorial|best_practice|architecture",
            "tags": ["tag1", "tag2", "tag3"],
            "categories": ["category1", "subcategory1"],
            "industries": ["industry1", "industry2"],
            "cloud_providers": ["aws", "azure", "gcp"],
            "services": ["s3", "ec2", "rds"],
            "security_impact": {{
                "threats_mitigated": ["threat1"],
                "strengths": ["strength1"],
                "concerns": ["concern1"]
            }},
            "compliance_impact": {{
                "standards": ["SOC2"],
                "requirements": ["requirement1"]
            }},
            "cost_impact": {{
                "monthly_estimate": "XX-XX",
                "optimization_opportunities": ["opportunity1"]
            }}
        }}
    ]
}}

Extract ALL distinct knowledge articles from this content. If the content covers multiple topics, create separate articles for each."""

    def _parse_analysis_response(
        self,
        response_text: str,
        source_url: str,
        extracted_info: dict[str, Any],
        doc_context: dict[str, Any],
    ) -> list[KnowledgeArticle]:
        """Parse LLM response and create KnowledgeArticle objects.

        Args:
            response_text: LLM response text
            source_url: Source URL
            extracted_info: Extracted topics and services
            doc_context: Documentation context

        Returns:
            List of KnowledgeArticle objects
        """
        try:
            # Clean up response - sometimes LLM adds markdown
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif response_text.startswith("```"):
                response_text = response_text.split("```")[1].split("```")[0]

            result = json.loads(response_text)
            articles_data = result.get("articles", [])

            if not articles_data:
                logger.warning("No articles extracted from response")
                return []

            articles = []
            for idx, article_data in enumerate(articles_data):
                # Map content_type string to enum
                content_type_str = article_data.get("content_type", "guide").lower()
                content_type_map = {
                    "guide": ContentType.GUIDE,
                    "reference": ContentType.REFERENCE,
                    "tutorial": ContentType.GUIDE,
                    "best_practice": ContentType.PATTERN,
                    "architecture": ContentType.REFERENCE,
                    "pattern": ContentType.PATTERN,
                    "strategy": ContentType.STRATEGY,
                    "checklist": ContentType.CHECKLIST,
                }
                content_type = content_type_map.get(content_type_str, ContentType.GUIDE)

                article = KnowledgeArticle(
                    article_id=f"doc_{doc_context.get('resource_id', 'unknown')}_{idx}_{hashlib.md5(article_data.get('title', '').encode()).hexdigest()[:8]}",
                    domain=Domain.DEVOPS,
                    subdomain=extracted_info.get("content_type", "documentation"),
                    content_type=content_type,
                    title=article_data.get("title", "Untitled"),
                    summary=article_data.get("summary", ""),
                    content=article_data.get("content", ""),
                    source_url=source_url,
                    user_id=doc_context.get("user_id"),
                    visibility="user",
                    source_type="documentation",
                    resource_id=doc_context.get("resource_id"),
                    tags=article_data.get("tags", []),
                    categories=article_data.get("categories", []),
                    industries=article_data.get("industries", []),
                    cloud_providers=article_data.get("cloud_providers", []),
                    services=article_data.get("services", []),
                )

                # Add cross-domain impacts as metadata
                if article_data.get("security_impact"):
                    article.security_impact = article_data["security_impact"]
                if article_data.get("compliance_impact"):
                    article.compliance_impact = article_data["compliance_impact"]
                if article_data.get("cost_impact"):
                    article.cost_impact = article_data["cost_impact"]

                articles.append(article)

            logger.info("Parsed %d articles from response", len(articles))
            return articles

        except json.JSONDecodeError as e:
            logger.error("Failed to parse LLM response as JSON: %s", e)
            logger.debug("Response text: %s", response_text[:500])
            return []
        except Exception as e:
            logger.error("Error parsing analysis response: %s", e, exc_info=True)
            return []

    def _fallback_analyze(
        self,
        content: str,
        source_url: str,
        title: str | None,
        doc_context: dict[str, Any],
    ) -> list[KnowledgeArticle]:
        """Fallback analysis when LLM is unavailable.

        Args:
            content: Content to analyze
            source_url: Source URL
            title: Optional title
            doc_context: Documentation context

        Returns:
            List of KnowledgeArticle objects
        """
        # Extract title from content if not provided
        if not title:
            lines = content.split("\n")
            for line in lines:
                if line.startswith("# "):
                    title = line[2:].strip()
                    break
            if not title:
                title = source_url.split("/")[-1] or "Documentation"

        # Create a single article from the content
        summary_lines = []
        for line in content.split("\n")[:10]:
            line = line.strip()
            if line and not line.startswith("#"):
                summary_lines.append(line)
            if len(" ".join(summary_lines)) > 200:
                break
        summary = " ".join(summary_lines)[:500] or "Documentation article"

        article = KnowledgeArticle(
            article_id=f"doc_{doc_context.get('resource_id', 'unknown')}_fallback_{hashlib.md5(content[:100].encode()).hexdigest()[:8]}",
            domain=Domain.DEVOPS,
            subdomain="documentation",
            content_type=ContentType.GUIDE,
            title=title,
            summary=summary,
            content=content,
            source_url=source_url,
            user_id=doc_context.get("user_id"),
            visibility="user",
            source_type="documentation",
            resource_id=doc_context.get("resource_id"),
        )

        return [article]

    async def analyze_uploaded_document(
        self,
        content: str,
        file_path: str,
        file_name: str,
        doc_context: dict[str, Any],
        activity_callback: Callable[[str, str, dict[str, Any] | None], None] | None = None,
    ) -> list[KnowledgeArticle]:
        """Analyze an uploaded document (PDF, DOCX, etc.).

        This method provides a specialized entry point for uploaded documents
        that may have different structure than URL-based documentation.

        Args:
            content: Extracted text content from document
            file_path: Original file path
            file_name: File name
            doc_context: Documentation context
            activity_callback: Optional activity callback

        Returns:
            List of KnowledgeArticle objects
        """
        return await self.analyze_documentation(
            content=content,
            source_url=file_path,
            title=file_name,
            doc_context=doc_context,
            activity_callback=activity_callback,
        )


# Singleton instance
documentation_analyzer = DocumentationAnalyzer()