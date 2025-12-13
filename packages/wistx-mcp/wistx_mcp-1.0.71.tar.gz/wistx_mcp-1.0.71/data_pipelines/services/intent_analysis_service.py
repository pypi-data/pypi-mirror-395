"""Intent Analysis Service for on-demand knowledge research.

Extracts technologies, tasks, and research queries from user input
to enable intelligent source discovery when no URL is provided.

Uses Anthropic's contextual retrieval approach for WISTX's domain focus:
DevOps, Infrastructure, Compliance, FinOps, and Platform Engineering.
"""

import json
import logging
from typing import Any

from wistx_mcp.config import settings
from wistx_mcp.tools.lib.gemini_client import GeminiClient
from wistx_mcp.tools.lib.retry_utils import with_timeout_and_retry

logger = logging.getLogger(__name__)


# WISTX domain-specific technology categories
WISTX_TECHNOLOGY_CATEGORIES = {
    "iac": [
        "terraform", "opentofu", "pulumi", "cloudformation", "bicep",
        "ansible", "crossplane", "cdk", "cdktf",
    ],
    "kubernetes": [
        "kubernetes", "k8s", "helm", "kustomize", "karpenter",
        "istio", "linkerd", "cilium", "argocd", "flux",
    ],
    "containers": [
        "docker", "containerd", "podman", "buildah", "kaniko",
    ],
    "ci_cd": [
        "github actions", "gitlab ci", "jenkins", "circleci",
        "tekton", "argo workflows", "spinnaker",
    ],
    "monitoring": [
        "prometheus", "grafana", "datadog", "newrelic", "dynatrace",
        "opentelemetry", "jaeger", "loki", "tempo",
    ],
    "cloud": [
        "aws", "azure", "gcp", "alibaba cloud", "oracle cloud",
    ],
    "security": [
        "vault", "opa", "kyverno", "falco", "trivy", "snyk",
        "checkov", "tfsec", "terrascan",
    ],
    "finops": [
        "kubecost", "infracost", "cloudhealth", "spot.io",
        "cost explorer", "billing", "reserved instances",
    ],
    "compliance": [
        "pci-dss", "hipaa", "soc2", "gdpr", "iso-27001",
        "nist", "cis", "fedramp",
    ],
}


class IntentAnalysisResult:
    """Result of intent analysis."""
    
    def __init__(
        self,
        technologies: list[str],
        task_type: str,
        task_description: str,
        research_queries: list[str],
        knowledge_gaps: list[str],
        confidence: float,
        raw_response: dict[str, Any] | None = None,
    ):
        self.technologies = technologies
        self.task_type = task_type
        self.task_description = task_description
        self.research_queries = research_queries
        self.knowledge_gaps = knowledge_gaps
        self.confidence = confidence
        self.raw_response = raw_response
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "technologies": self.technologies,
            "task_type": self.task_type,
            "task_description": self.task_description,
            "research_queries": self.research_queries,
            "knowledge_gaps": self.knowledge_gaps,
            "confidence": self.confidence,
        }


class IntentAnalysisService:
    """Service for analyzing user intent to enable intelligent source discovery."""
    
    def __init__(self):
        """Initialize intent analysis service."""
        if not settings.gemini_api_key:
            logger.warning("Gemini API key not configured - intent analysis will be limited")
            self.client = None
        else:
            self.client = GeminiClient(api_key=settings.gemini_api_key)
        self.model = "gemini-2.5-flash"
        self.max_tokens = 2000
        self.temperature = 0.1
    
    async def analyze_intent(
        self,
        user_query: str,
        context: str | None = None,
    ) -> IntentAnalysisResult:
        """Analyze user intent to extract technologies and research needs.
        
        Args:
            user_query: The user's research query or task description
            context: Optional additional context about the user's project
            
        Returns:
            IntentAnalysisResult with extracted information
        """
        # First, try keyword-based extraction for quick results
        keyword_result = self._extract_technologies_from_keywords(user_query)
        
        # If we have a client, enhance with LLM analysis
        if self.client:
            try:
                llm_result = await self._analyze_with_llm(user_query, context)
                if llm_result:
                    # Merge keyword and LLM results
                    return self._merge_results(keyword_result, llm_result)
            except Exception as e:
                logger.warning("LLM intent analysis failed, using keyword extraction: %s", e)
        
        return keyword_result

    def _extract_technologies_from_keywords(self, query: str) -> IntentAnalysisResult:
        """Extract technologies using keyword matching.

        Args:
            query: User query to analyze

        Returns:
            IntentAnalysisResult with keyword-extracted technologies
        """
        query_lower = query.lower()
        found_technologies = []

        for category, techs in WISTX_TECHNOLOGY_CATEGORIES.items():
            for tech in techs:
                if tech.lower() in query_lower:
                    found_technologies.append(tech)

        # Deduplicate while preserving order
        seen = set()
        unique_techs = []
        for tech in found_technologies:
            if tech.lower() not in seen:
                seen.add(tech.lower())
                unique_techs.append(tech)

        # Generate basic research queries from found technologies
        research_queries = []
        for tech in unique_techs[:5]:  # Limit to top 5
            research_queries.append(f"{tech} documentation")
            research_queries.append(f"{tech} best practices")

        return IntentAnalysisResult(
            technologies=unique_techs,
            task_type="implementation" if unique_techs else "research",
            task_description=query,
            research_queries=research_queries,
            knowledge_gaps=[],
            confidence=0.5 if unique_techs else 0.3,
        )

    async def _analyze_with_llm(
        self,
        user_query: str,
        context: str | None = None,
    ) -> IntentAnalysisResult | None:
        """Analyze intent using LLM for deeper understanding.

        Args:
            user_query: User query to analyze
            context: Optional additional context

        Returns:
            IntentAnalysisResult or None if analysis fails
        """
        prompt = self._build_analysis_prompt(user_query, context)

        try:
            response = await with_timeout_and_retry(
                self._call_llm,
                timeout_seconds=30.0,
                max_attempts=2,
                retryable_exceptions=(Exception,),
                prompt=prompt,
            )

            if not response:
                return None

            return self._parse_llm_response(response)
        except Exception as e:
            logger.warning("LLM analysis failed: %s", e)
            return None

    def _build_analysis_prompt(self, user_query: str, context: str | None) -> str:
        """Build the analysis prompt for the LLM."""
        context_section = f"\nAdditional Context: {context}" if context else ""

        return f"""Analyze the following user query for a DevOps/Infrastructure/Platform Engineering context.
Extract the technologies, task type, and generate research queries.

User Query: {user_query}{context_section}

WISTX focuses on: DevOps, Infrastructure as Code, Kubernetes, CI/CD, Monitoring,
Cloud Platforms (AWS/Azure/GCP), Security, FinOps, and Compliance.

Respond in JSON format:
{{
    "technologies": ["list of specific technologies mentioned or implied"],
    "task_type": "one of: implementation, troubleshooting, optimization, migration, security, compliance, research",
    "task_description": "concise description of what the user is trying to accomplish",
    "research_queries": ["list of 3-5 specific search queries to find relevant documentation"],
    "knowledge_gaps": ["list of topics the user might need to learn about"],
    "confidence": 0.0-1.0
}}

Be specific about technologies (e.g., "Terraform" not just "IaC").
Generate research queries that would find official documentation and best practices."""

    async def _call_llm(self, prompt: str) -> str | None:
        """Call the LLM with the given prompt."""
        if not self.client:
            return None

        messages = [{"role": "user", "content": prompt}]

        response = await self.client.chat_completion(
            messages=messages,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            response_format={"type": "json_object"},
        )

        return response

    def _parse_llm_response(self, response: str) -> IntentAnalysisResult | None:
        """Parse LLM response into IntentAnalysisResult."""
        try:
            data = json.loads(response)
            return IntentAnalysisResult(
                technologies=data.get("technologies", []),
                task_type=data.get("task_type", "research"),
                task_description=data.get("task_description", ""),
                research_queries=data.get("research_queries", []),
                knowledge_gaps=data.get("knowledge_gaps", []),
                confidence=data.get("confidence", 0.7),
                raw_response=data,
            )
        except json.JSONDecodeError as e:
            logger.warning("Failed to parse LLM response as JSON: %s", e)
            return None

    def _merge_results(
        self,
        keyword_result: IntentAnalysisResult,
        llm_result: IntentAnalysisResult,
    ) -> IntentAnalysisResult:
        """Merge keyword and LLM results, preferring LLM but keeping keyword findings."""
        # Combine technologies, LLM first then keyword additions
        all_techs = list(llm_result.technologies)
        seen = {t.lower() for t in all_techs}
        for tech in keyword_result.technologies:
            if tech.lower() not in seen:
                all_techs.append(tech)
                seen.add(tech.lower())

        return IntentAnalysisResult(
            technologies=all_techs,
            task_type=llm_result.task_type,
            task_description=llm_result.task_description or keyword_result.task_description,
            research_queries=llm_result.research_queries or keyword_result.research_queries,
            knowledge_gaps=llm_result.knowledge_gaps,
            confidence=llm_result.confidence,
            raw_response=llm_result.raw_response,
        )

