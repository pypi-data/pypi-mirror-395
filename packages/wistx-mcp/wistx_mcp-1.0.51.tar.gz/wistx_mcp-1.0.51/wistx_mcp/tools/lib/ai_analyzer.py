"""AI analyzer for search results and resource collection analysis."""

import hashlib
import json
import logging
import time
from typing import Any

from wistx_mcp.config import settings
from wistx_mcp.tools.lib.retry_utils import with_timeout_and_retry
from wistx_mcp.tools.lib.gemini_client import GeminiClient

logger = logging.getLogger(__name__)


class AIAnalyzer:
    """AI analysis utility for search results and resource collections."""

    def __init__(self):
        """Initialize AI analyzer."""
        if not settings.gemini_api_key:
            logger.warning("Gemini API key not configured - AI analysis will be disabled")
            self.client = None
        else:
            self.client = GeminiClient(api_key=settings.gemini_api_key)
        self.model = "gemini-2.5-flash"
        self.max_tokens = 4000
        self.temperature = 0.3
        self._cache: dict[str, tuple[dict[str, Any], float]] = {}
        self._cache_ttl = 3600

    async def analyze_search_results(
        self,
        query: str,
        results: list[dict[str, Any]],
        resources: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any] | None:
        """Analyze search results and provide AI insights.

        Args:
            query: Original search query
            results: List of search results
            resources: List of resources (optional)

        Returns:
            Dictionary with AI analysis or None if analysis fails
        """
        if not self.client or not results:
            return None

        try:
            top_results = results[:10]
            results_summary = self._summarize_results(top_results)
            resources_summary = self._summarize_resources(resources) if resources else ""

            prompt = self._get_search_analysis_prompt(query, results_summary, resources_summary, top_results)

            response = await with_timeout_and_retry(
                self._call_llm,
                timeout_seconds=30.0,
                max_attempts=2,
                retryable_exceptions=(Exception,),
                prompt=prompt,
            )

            if not response:
                return None

            return {
                "analysis": response,
                "query_understanding": self._extract_section(response, "Query Understanding"),
                "key_findings": self._extract_section(response, "Key Findings"),
                "recommendations": self._extract_section(response, "Recommendations"),
            }
        except Exception as e:
            logger.warning("AI analysis failed for search results: %s", e, exc_info=True)
            return None

    async def analyze_resource_collection(
        self,
        resources: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        """Analyze resource collection and provide AI insights.

        Args:
            resources: List of indexed resources

        Returns:
            Dictionary with AI analysis or None if analysis fails
        """
        if not self.client or not resources:
            return None

        cache_key = self._generate_cache_key(resources)
        cached_result = self._get_from_cache(cache_key)
        if cached_result:
            logger.debug("Returning cached AI analysis for resource collection")
            return cached_result

        try:
            resources_summary = self._summarize_resources(resources)

            prompt = self._get_resource_analysis_prompt(resources_summary, resources)

            response = await with_timeout_and_retry(
                self._call_llm,
                timeout_seconds=30.0,
                max_attempts=2,
                retryable_exceptions=(Exception,),
                prompt=prompt,
            )

            if not response:
                return None

            result = {
                "analysis": response,
                "overview": self._extract_section(response, "Resource Collection Overview"),
                "patterns": self._extract_section(response, "Pattern Detection"),
                "health_analysis": self._extract_section(response, "Health Status Analysis"),
                "insights": self._extract_section(response, "Key Insights"),
                "recommendations": self._extract_section(response, "Recommendations"),
            }

            self._store_in_cache(cache_key, result)
            return result
        except Exception as e:
            logger.warning("AI analysis failed for resource collection: %s", e, exc_info=True)
            return None

    async def _call_llm(self, prompt: str) -> str | None:
        """Call Gemini API for analysis.

        Args:
            prompt: Analysis prompt

        Returns:
            AI response text or None if failed
        """
        if not self.client or not self.client.is_available():
            return None

        try:
            response_text = await self.client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            if not response_text:
                return None

            return response_text.strip()
        except Exception as e:
            logger.error("Gemini API call failed: %s", e, exc_info=True)
            return None

    def _get_search_analysis_prompt(
        self,
        query: str,
        results_summary: str,
        resources_summary: str,
        top_results: list[dict[str, Any]],
    ) -> str:
        """Build prompt for search results analysis.

        Args:
            query: Search query
            results_summary: Summary of results
            resources_summary: Summary of resources
            top_results: Top N results with content

        Returns:
            Formatted prompt
        """
        results_with_code = []
        for i, result in enumerate(top_results[:5], 1):
            title = result.get("title", "Unknown")
            summary = result.get("summary", "")
            content = result.get("content", "")[:500]
            source_url = result.get("source_url", "")
            source_type = result.get("source_type", "unknown")

            code_snippet = ""
            if content:
                code_snippet = f"\n\nCode snippet:\n```\n{content}\n```"

            results_with_code.append(
                f"Result {i}: {title}\n"
                f"Source: {source_type} ({source_url})\n"
                f"Summary: {summary}{code_snippet}"
            )

        return f"""You are an expert DevOps engineer analyzing codebase search results.

**Search Query**: {query}

**Results Summary**: {results_summary}

**Resources Searched**: {resources_summary if resources_summary else "Multiple resources"}

**Top Results**:
{chr(10).join(results_with_code)}

Provide a comprehensive analysis in markdown format with the following sections:

1. **Query Understanding**: Explain what the user is searching for and what they're trying to accomplish.

2. **Key Findings Summary**: Summarize the key findings from all results. Include:
   - Patterns detected across results
   - Counts of different types of results
   - Technologies or tools mentioned
   - Common themes or approaches

3. **Most Relevant Results**: For the top 3-5 results, explain:
   - Why each result is relevant to the query
   - What the code/config does
   - Key insights from each result
   - Include code explanations where applicable

4. **Code Explanations**: For code snippets in the top results, provide:
   - What the code does
   - Why it's relevant to the query
   - Best practices or patterns shown
   - Any potential improvements or considerations

5. **Pattern Detection**: Identify patterns across results:
   - Common approaches or patterns
   - Technologies frequently used together
   - Best practices observed
   - Potential inconsistencies or issues

6. **Recommendations**: Suggest:
   - Next steps or related searches
   - Areas to explore further
   - Potential improvements or considerations
   - Related resources or documentation

Format your response as clear markdown with proper headers and code blocks. Be concise but comprehensive."""

    def _get_resource_analysis_prompt(
        self,
        resources_summary: str,
        resources: list[dict[str, Any]],
    ) -> str:
        """Build prompt for resource collection analysis.

        Args:
            resources_summary: Summary of resources
            resources: Full resource list

        Returns:
            Formatted prompt
        """
        resource_details = []
        for resource in resources:
            name = resource.get("name", "Unknown")
            resource_type = resource.get("resource_type", "unknown")
            status = resource.get("status", "unknown")
            repo_url = resource.get("repo_url", "")
            content_url = resource.get("content_url", "")
            tags = resource.get("tags", [])
            description = resource.get("description", "")

            details = f"- **{name}** ({resource_type}): {status}"
            if repo_url:
                details += f"\n  Repository: {repo_url}"
            if content_url:
                details += f"\n  URL: {content_url}"
            if tags:
                details += f"\n  Tags: {', '.join(tags[:5])}"
            if description:
                details += f"\n  Description: {description[:100]}"

            resource_details.append(details)

        return f"""You are an expert DevOps engineer analyzing a collection of indexed resources.

**Resources Summary**: {resources_summary}

**Resource Details**:
{chr(10).join(resource_details)}

Provide a comprehensive analysis in markdown format with the following sections:

1. **Resource Collection Overview**: 
   - Total count and breakdown by type
   - Status distribution (completed, indexing, failed, pending)
   - Overall health of the collection

2. **Pattern Detection**: Identify patterns:
   - Technologies or tools most commonly indexed
   - Cloud providers or platforms used
   - Types of resources (repositories, documentation, documents)
   - Common tags or categories
   - Infrastructure patterns (Terraform, Kubernetes, etc.)

3. **Health Status Analysis**:
   - Successful indexing status
   - Resources currently indexing (with progress if available)
   - Failed resources and potential reasons
   - Resources that may need attention

4. **Key Insights**:
   - What the resource collection tells us about the user's infrastructure
   - Coverage gaps or areas for improvement
   - Strengths of the current collection
   - Potential issues or concerns

5. **Recommendations**: Suggest:
   - Resources that might benefit from re-indexing
   - Additional resources to consider indexing
   - Documentation or resources that complement existing ones
   - Best practices for resource management
   - Next steps for improving coverage

Format your response as clear markdown with proper headers. Be concise but actionable."""

    def _summarize_results(self, results: list[dict[str, Any]]) -> str:
        """Summarize search results for prompt.

        Args:
            results: List of search results

        Returns:
            Summary string
        """
        if not results:
            return "No results found"

        total = len(results)
        source_types = {}
        for result in results:
            source_type = result.get("source_type", "unknown")
            source_types[source_type] = source_types.get(source_type, 0) + 1

        source_summary = ", ".join([f"{count} {stype}" for stype, count in source_types.items()])

        return f"Found {total} results: {source_summary}"

    def _summarize_resources(self, resources: list[dict[str, Any]] | None) -> str:
        """Summarize resources for prompt.

        Args:
            resources: List of resources

        Returns:
            Summary string
        """
        if not resources:
            return "No resources"

        total = len(resources)
        by_type = {}
        by_status = {}

        for resource in resources:
            resource_type = resource.get("resource_type", "unknown")
            status = resource.get("status", "unknown")

            by_type[resource_type] = by_type.get(resource_type, 0) + 1
            by_status[status] = by_status.get(status, 0) + 1

        type_summary = ", ".join([f"{count} {rtype}" for rtype, count in by_type.items()])
        status_summary = ", ".join([f"{count} {status}" for status, count in by_status.items()])

        return f"{total} resources ({type_summary}). Status: {status_summary}"

    def _extract_section(self, markdown: str, section_name: str) -> str:
        """Extract a section from markdown text.

        Args:
            markdown: Markdown text
            section_name: Section name to extract

        Returns:
            Section content or empty string
        """
        lines = markdown.split("\n")
        in_section = False
        section_lines = []

        for line in lines:
            if section_name.lower() in line.lower() and ("#" in line or "**" in line):
                in_section = True
                continue

            if in_section:
                if line.startswith("#") and section_name.lower() not in line.lower():
                    break
                section_lines.append(line)

        return "\n".join(section_lines).strip()

    def _generate_cache_key(self, resources: list[dict[str, Any]]) -> str:
        """Generate cache key from resource collection.

        Args:
            resources: List of resources

        Returns:
            Cache key string
        """
        resource_ids = sorted([r.get("resource_id", "") for r in resources])
        resource_statuses = sorted([r.get("status", "") for r in resources])
        key_data = f"{len(resources)}:{':'.join(resource_ids)}:{':'.join(resource_statuses)}"
        return hashlib.sha256(key_data.encode()).hexdigest()

    def _get_from_cache(self, cache_key: str) -> dict[str, Any] | None:
        """Get result from cache if available and not expired.

        Args:
            cache_key: Cache key

        Returns:
            Cached result or None
        """
        if cache_key not in self._cache:
            return None

        result, timestamp = self._cache[cache_key]
        if time.time() - timestamp > self._cache_ttl:
            del self._cache[cache_key]
            return None

        return result

    def _store_in_cache(self, cache_key: str, result: dict[str, Any]) -> None:
        """Store result in cache.

        Args:
            cache_key: Cache key
            result: Result to cache
        """
        self._cache[cache_key] = (result, time.time())
        if len(self._cache) > 100:
            oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k][1])
            del self._cache[oldest_key]


ai_analyzer = AIAnalyzer()
