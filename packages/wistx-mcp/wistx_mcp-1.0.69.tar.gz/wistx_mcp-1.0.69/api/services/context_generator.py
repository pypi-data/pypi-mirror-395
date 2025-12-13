"""Context generator service for contextual retrieval.

Generates chunk-specific explanatory context to prepend before embedding,
improving retrieval accuracy per Anthropic's contextual retrieval research.
"""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Any, Optional

from anthropic import AsyncAnthropic, RateLimitError

from api.config import settings
from wistx_mcp.tools.lib.retry_utils import retry_on_failure, with_timeout
from data_pipelines.models.knowledge_article import KnowledgeArticle
from data_pipelines.models.compliance import ComplianceControl
from data_pipelines.models.cost_data import FOCUSCostData
from api.exceptions import ValidationError, ExternalServiceError

logger = logging.getLogger(__name__)


class RateLimitTracker:
    """Track Anthropic API rate limits from response headers."""

    def __init__(self):
        self.output_tokens_remaining = 8000
        self.output_tokens_limit = 8000
        self.output_tokens_reset: Optional[datetime] = None
        self.requests_remaining = 50
        self.requests_limit = 50
        self.requests_reset: Optional[datetime] = None
        self.retry_after: Optional[float] = None
        self.lock = asyncio.Lock()

    def update_from_headers(self, headers: dict[str, Any]) -> None:
        """Update rate limit state from API response headers."""
        try:
            self.output_tokens_remaining = int(
                headers.get("anthropic-ratelimit-output-tokens-remaining", 8000)
            )
            self.output_tokens_limit = int(
                headers.get("anthropic-ratelimit-output-tokens-limit", 8000)
            )
            reset_str = headers.get("anthropic-ratelimit-output-tokens-reset")
            if reset_str:
                self.output_tokens_reset = datetime.fromisoformat(
                    reset_str.replace("Z", "+00:00")
                )

            self.requests_remaining = int(
                headers.get("anthropic-ratelimit-requests-remaining", 50)
            )
            self.requests_limit = int(
                headers.get("anthropic-ratelimit-requests-limit", 50)
            )

            retry_after = headers.get("retry-after")
            if retry_after:
                self.retry_after = float(retry_after)
        except (ValueError, TypeError, AttributeError) as e:
            logger.debug("Error parsing rate limit headers: %s", e)

    def can_make_request(self, estimated_output_tokens: int = 1000) -> bool:
        """Check if request can be made based on token budget."""
        if self.output_tokens_remaining < estimated_output_tokens:
            return False
        if self.requests_remaining < 1:
            return False
        return True

    def get_wait_time(self) -> float:
        """Get recommended wait time before next request."""
        if self.retry_after:
            return self.retry_after
        if self.output_tokens_reset:
            now = datetime.now(timezone.utc)
            wait = (self.output_tokens_reset - now).total_seconds()
            return max(0, wait)
        return 0


_rate_limit_tracker = RateLimitTracker()


class ContextGenerator:
    """Generate contextual descriptions for knowledge articles.

    Uses Anthropic Claude for LLM-based context generation.
    Requires ANTHROPIC_API_KEY to be set. Fails fast if unavailable.
    """

    def __init__(self):
        """Initialize context generator."""
        anthropic_api_key = getattr(settings, "anthropic_api_key", None)
        if not anthropic_api_key:
            raise ValidationError(
                message="ANTHROPIC_API_KEY not set",
                user_message="Context generation requires Anthropic API key. Please contact support.",
                error_code="ANTHROPIC_KEY_NOT_SET",
                details={"service": "context_generator"}
            )
        self.llm_client = AsyncAnthropic(api_key=anthropic_api_key)
        
        self.model = "claude-opus-4-1"
        self.temperature = 0.1
        self.max_tokens = 1000
        
        if "opus" in self.model.lower():
            self.timeout_seconds = 90.0
        else:
            self.timeout_seconds = 30.0
        
        self.max_context_length = 2000

    async def generate_context(
        self,
        article: KnowledgeArticle,
        repo_context: Optional[dict[str, Any]] = None,
    ) -> str:
        """Generate contextual description for a knowledge article.

        Args:
            article: Knowledge article to generate context for
            repo_context: Optional repository context (for repository-based articles)

        Returns:
            Contextual description string (max 2000 chars)

        Raises:
            ValueError: If LLM client is not available
            RuntimeError: If context generation fails
        """
        if not self.llm_client:
            raise ValidationError(
                message="LLM client not available",
                user_message="Context generation service is not available. Please contact support.",
                error_code="LLM_CLIENT_NOT_AVAILABLE",
                details={"service": "context_generator"}
            )

        context = await self._generate_with_llm(article, repo_context)
        if context and len(context) <= self.max_context_length:
            return context
        elif context:
            logger.warning(
                "Generated context too long (%d chars), truncating to %d",
                len(context),
                self.max_context_length,
            )
            return context[:self.max_context_length]
        
        raise ExternalServiceError(
            message="Failed to generate context for knowledge article",
            user_message="Failed to generate context. Please try again later.",
            error_code="CONTEXT_GENERATION_FAILED",
            details={"article_id": article.id if hasattr(article, 'id') else None}
        )

    @retry_on_failure(max_attempts=2, initial_delay=1.0, max_delay=5.0)
    async def _generate_with_llm(
        self,
        article: KnowledgeArticle,
        repo_context: Optional[dict[str, Any]] = None,
    ) -> str:
        """Generate context using Claude Opus.

        Args:
            article: Knowledge article
            repo_context: Optional repository context

        Returns:
            Generated contextual description
        """
        if not self.llm_client:
            raise ValueError("LLM client not available")

        prompt = self._build_context_prompt(article, repo_context)

        async def _make_api_call():
            return await self.llm_client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                timeout=self.timeout_seconds,
            )

        response = await with_timeout(_make_api_call, timeout_seconds=self.timeout_seconds)

        if not response.content or len(response.content) == 0:
            raise ValueError("Empty response from LLM")

        context_text = ""
        for block in response.content:
            if hasattr(block, "text"):
                context_text += block.text
            elif isinstance(block, str):
                context_text += block

        if not context_text.strip():
            raise ValueError("Empty context text from LLM")

        return context_text.strip()

    def _generate_with_template(
        self,
        article: KnowledgeArticle,
        repo_context: Optional[dict[str, Any]] = None,
    ) -> str:
        """Generate context using template-based approach.

        Args:
            article: Knowledge article
            repo_context: Optional repository context

        Returns:
            Template-generated contextual description
        """
        parts = []

        if repo_context:
            repo_name = repo_context.get("repo_url", "").split("/")[-1].replace(".git", "")
            branch = repo_context.get("branch", "main")
            parts.append(
                f"This knowledge article is from repository '{repo_name}' (branch: {branch})."
            )

        domain_str = article.domain.value if hasattr(article.domain, "value") else str(article.domain)
        subdomain_str = article.subdomain
        parts.append(
            f"Domain: {domain_str} ({subdomain_str}). Content type: {article.content_type.value if hasattr(article.content_type, 'value') else article.content_type}."
        )

        if article.cloud_providers:
            providers_str = ", ".join(article.cloud_providers)
            parts.append(f"Cloud providers: {providers_str}.")

        if article.services:
            services_str = ", ".join(article.services[:5])
            parts.append(f"Services: {services_str}.")

        if article.compliance_impact:
            standards = article.compliance_impact.get("standards", [])
            if standards:
                standards_str = ", ".join(standards[:3])
                parts.append(f"Applicable compliance standards: {standards_str}.")

        if article.cost_impact:
            total_monthly = article.cost_impact.get("total_monthly")
            if total_monthly:
                parts.append(f"Estimated monthly cost: ${total_monthly:.2f}.")

        if article.security_impact:
            security_summary = article.security_impact.get("summary", "")
            if security_summary:
                parts.append(f"Security considerations: {security_summary[:100]}.")

        if article.structured_data:
            component_type = article.structured_data.get("component_type")
            component_name = article.structured_data.get("component_name")
            if component_type and component_name:
                parts.append(
                    f"This analysis covers a {component_type} component ({component_name})."
                )

        if article.source_url:
            if "github.com" in article.source_url:
                parts.append("Source: GitHub repository.")
            elif article.source_url.startswith("http"):
                parts.append("Source: External documentation.")

        context = " ".join(parts)

        if len(context) > self.max_context_length:
            context = context[:self.max_context_length - 3] + "..."

        return context

    def _build_context_prompt(
        self,
        article: KnowledgeArticle,
        repo_context: Optional[dict[str, Any]] = None,
    ) -> str:
        """Build prompt for LLM context generation.

        Args:
            article: Knowledge article
            repo_context: Optional repository context

        Returns:
            Prompt string
        """
        domain_str = article.domain.value if hasattr(article.domain, "value") else str(article.domain)
        content_type_str = article.content_type.value if hasattr(article.content_type, "value") else str(article.content_type)

        prompt_parts = [
            "Generate a concise contextual description (100-300 words, max 2000 chars) for this knowledge article.",
            "The description will be prepended before embedding to improve retrieval accuracy.",
            "",
            "Article Details:",
            f"- Title: {article.title}",
            f"- Domain: {domain_str} ({article.subdomain})",
            f"- Content Type: {content_type_str}",
            f"- Summary: {article.summary[:200]}",
        ]

        if repo_context:
            repo_name = repo_context.get("repo_url", "").split("/")[-1].replace(".git", "")
            branch = repo_context.get("branch", "main")
            commit_sha = repo_context.get("commit_sha", "")
            prompt_parts.extend([
                f"- Repository: {repo_name} (branch: {branch})",
                f"- Commit: {commit_sha[:8] if commit_sha else 'N/A'}",
            ])

        if article.source_url:
            prompt_parts.append(f"- Source URL: {article.source_url}")

        if article.structured_data:
            component_type = article.structured_data.get("component_type")
            component_name = article.structured_data.get("component_name")
            file_path = article.structured_data.get("file_path")
            if component_type:
                prompt_parts.append(f"- Component Type: {component_type}")
            if component_name:
                prompt_parts.append(f"- Component Name: {component_name}")
            if file_path:
                prompt_parts.append(f"- File Path: {file_path}")

        prompt_parts.extend([
            "",
            "Structured Data:",
        ])

        if article.compliance_impact:
            standards = article.compliance_impact.get("standards", [])
            if standards:
                prompt_parts.append(f"- Compliance Standards: {', '.join(standards)}")

        if article.cost_impact:
            total_monthly = article.cost_impact.get("total_monthly")
            if total_monthly:
                prompt_parts.append(f"- Estimated Monthly Cost: ${total_monthly:.2f}")

        if article.security_impact:
            security_summary = article.security_impact.get("summary", "")
            if security_summary:
                prompt_parts.append(f"- Security Summary: {security_summary[:200]}")

        if article.cloud_providers:
            prompt_parts.append(f"- Cloud Providers: {', '.join(article.cloud_providers)}")

        if article.services:
            prompt_parts.append(f"- Services: {', '.join(article.services[:10])}")

        prompt_parts.extend([
            "",
            "Generate a contextual description that:",
            "1. Situates this article within its repository/project context (if applicable)",
            "2. Explains the component's purpose and role (if applicable)",
            "3. Highlights key domain-specific aspects (compliance, cost, security)",
            "4. Mentions relationships to other components or resources",
            "5. Provides context for better semantic understanding",
            "",
            "The description should be natural, informative, and help the embedding model",
            "understand the article's context and purpose. Keep it concise (100-300 words).",
        ])

        return "\n".join(prompt_parts)

    async def generate_context_for_compliance_control(
        self,
        control: ComplianceControl,
    ) -> str:
        """Generate contextual description for a compliance control.

        Args:
            control: Compliance control to generate context for

        Returns:
            Contextual description string (max 2000 chars)

        Raises:
            ValueError: If LLM client is not available
            RuntimeError: If context generation fails
        """
        if not self.llm_client:
            raise ValidationError(
                message="LLM client not available",
                user_message="Context generation service is not available. Please contact support.",
                error_code="LLM_CLIENT_NOT_AVAILABLE",
                details={"service": "context_generator"}
            )

        context = await self._generate_compliance_context_with_llm(control)
        if context and len(context) <= self.max_context_length:
            return context
        elif context:
            logger.warning(
                "Generated context too long (%d chars), truncating to %d",
                len(context),
                self.max_context_length,
            )
            return context[:self.max_context_length]
        
        raise RuntimeError("Failed to generate context for compliance control")

    @retry_on_failure(max_attempts=2, initial_delay=1.0, max_delay=5.0)
    async def _generate_compliance_context_with_llm(
        self,
        control: ComplianceControl,
    ) -> str:
        """Generate context using Claude Opus for compliance control.

        Args:
            control: Compliance control

        Returns:
            Generated contextual description
        """
        if not self.llm_client:
            raise ValueError("LLM client not available")

        prompt = self._build_compliance_context_prompt(control)

        async def _make_api_call():
            return await self.llm_client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                timeout=self.timeout_seconds,
            )

        response = await with_timeout(_make_api_call, timeout_seconds=self.timeout_seconds)

        if not response.content or len(response.content) == 0:
            raise ValueError("Empty response from LLM")

        context_text = ""
        for block in response.content:
            if hasattr(block, "text"):
                context_text += block.text
            elif isinstance(block, str):
                context_text += block

        if not context_text.strip():
            raise ValueError("Empty context text from LLM")

        return context_text.strip()

    def _generate_compliance_context_with_template(
        self,
        control: ComplianceControl,
    ) -> str:
        """Generate context using template-based approach for compliance control.

        Args:
            control: Compliance control

        Returns:
            Template-generated contextual description
        """
        parts = []

        parts.append(
            f"This is a {control.standard} compliance control ({control.version}). "
            f"Control ID: {control.control_id}."
        )

        if control.severity:
            parts.append(f"Severity level: {control.severity}.")

        if control.category:
            parts.append(f"Category: {control.category}.")
            if control.subcategory:
                parts.append(f"Subcategory: {control.subcategory}.")

        if control.applies_to:
            cloud_providers = control.get_cloud_providers()
            if cloud_providers:
                providers_str = ", ".join(cloud_providers)
                parts.append(f"Applies to cloud providers: {providers_str}.")

            resource_types = [r for r in control.applies_to[:5]]
            if resource_types:
                resources_str = ", ".join(resource_types)
                parts.append(f"Applies to resource types: {resources_str}.")

        if control.remediation and isinstance(control.remediation, dict):
            remediation_summary = control.remediation.get("summary", "")
            if remediation_summary:
                parts.append(f"Remediation approach: {remediation_summary[:150]}.")

        if control.verification:
            verification_methods = control.verification.get("methods", [])
            if verification_methods:
                methods_str = ", ".join(verification_methods[:3])
                parts.append(f"Verification methods: {methods_str}.")

        context = " ".join(parts)

        if len(context) > self.max_context_length:
            context = context[:self.max_context_length - 3] + "..."

        return context

    def _build_compliance_context_prompt(
        self,
        control: ComplianceControl,
    ) -> str:
        """Build prompt for LLM context generation for compliance control.

        Args:
            control: Compliance control

        Returns:
            Prompt string
        """
        prompt_parts = [
            "Generate a concise contextual description (100-300 words, max 2000 chars) for this compliance control.",
            "The description will be prepended before embedding to improve retrieval accuracy.",
            "",
            "Control Details:",
            f"- Standard: {control.standard} ({control.version})",
            f"- Control ID: {control.control_id}",
            f"- Title: {control.title}",
            f"- Severity: {control.severity}",
            f"- Description: {control.description[:200]}",
        ]

        if control.category:
            prompt_parts.append(f"- Category: {control.category}")
            if control.subcategory:
                prompt_parts.append(f"- Subcategory: {control.subcategory}")

        if control.requirement:
            prompt_parts.append(f"- Requirement: {control.requirement[:200]}")

        if control.applies_to:
            cloud_providers = control.get_cloud_providers()
            if cloud_providers:
                prompt_parts.append(f"- Cloud Providers: {', '.join(cloud_providers)}")
            prompt_parts.append(f"- Applies To: {', '.join(control.applies_to[:10])}")

        if control.remediation:
            remediation_summary = control.remediation.summary if hasattr(control.remediation, "summary") else str(control.remediation)
            prompt_parts.append(f"- Remediation Summary: {remediation_summary[:200]}")

        if control.verification:
            verification_methods = control.verification.get("methods", []) if isinstance(control.verification, dict) else []
            if verification_methods:
                prompt_parts.append(f"- Verification Methods: {', '.join(verification_methods[:5])}")

        prompt_parts.extend([
            "",
            "Generate a contextual description that:",
            "1. Situates this control within its compliance standard and framework",
            "2. Explains the control's purpose and security/compliance objectives",
            "3. Highlights which cloud resources and services it applies to",
            "4. Mentions severity and impact level",
            "5. Provides context for better semantic understanding during retrieval",
            "",
            "The description should be natural, informative, and help the embedding model",
            "understand the control's context and purpose. Keep it concise (100-300 words).",
        ])

        return "\n".join(prompt_parts)

    async def generate_context_for_cost_data(
        self,
        cost_record: FOCUSCostData,
    ) -> str:
        """Generate contextual description for cost data record.

        Args:
            cost_record: FOCUS cost data record

        Returns:
            Contextual description string (max 2000 chars)

        Raises:
            ValueError: If LLM client is not available
            RuntimeError: If context generation fails
        """
        if not self.llm_client:
            raise ValidationError(
                message="LLM client not available",
                user_message="Context generation service is not available. Please contact support.",
                error_code="LLM_CLIENT_NOT_AVAILABLE",
                details={"service": "context_generator"}
            )

        context = await self._generate_cost_context_with_llm(cost_record)
        if context and len(context) <= self.max_context_length:
            return context
        elif context:
            logger.warning(
                "Generated context too long (%d chars), truncating to %d",
                len(context),
                self.max_context_length,
            )
            return context[:self.max_context_length]
        
        raise RuntimeError("Failed to generate context for cost data record")

    async def _generate_cost_context_with_llm(
        self,
        cost_record: FOCUSCostData,
    ) -> str:
        """Generate context using Claude for cost data.

        Args:
            cost_record: FOCUS cost data record

        Returns:
            Generated contextual description

        Raises:
            ValueError: If LLM client is not available
            RuntimeError: If context generation fails after retries
        """
        if not self.llm_client:
            raise ValueError("LLM client not available")

        prompt = self._build_cost_context_prompt(cost_record)
        max_attempts = 3
        last_exception = None

        for attempt in range(max_attempts):
            try:
                async with _rate_limit_tracker.lock:
                    if not _rate_limit_tracker.can_make_request(self.max_tokens):
                        wait_time = _rate_limit_tracker.get_wait_time()
                        if wait_time > 0:
                            logger.warning(
                                "Rate limit approaching, waiting %.1fs before request",
                                wait_time,
                            )
                            await asyncio.sleep(wait_time)

                async def _make_api_call():
                    return await self.llm_client.messages.create(
                        model=self.model,
                        max_tokens=self.max_tokens,
                        temperature=self.temperature,
                        messages=[
                            {
                                "role": "user",
                                "content": prompt,
                            }
                        ],
                        timeout=self.timeout_seconds,
                    )

                response = await with_timeout(
                    _make_api_call, timeout_seconds=self.timeout_seconds
                )

                break

            except RateLimitError as e:
                last_exception = e
                retry_after = 60.0

                if hasattr(e, "response") and hasattr(e.response, "headers"):
                    headers = e.response.headers
                    _rate_limit_tracker.update_from_headers(headers)
                    retry_after_header = headers.get("retry-after")
                    if retry_after_header:
                        retry_after = float(retry_after_header)

                if attempt < max_attempts - 1:
                    logger.warning(
                        "Rate limit hit (attempt %d/%d). Waiting %.1fs...",
                        attempt + 1,
                        max_attempts,
                        retry_after,
                    )
                    await asyncio.sleep(retry_after)
                else:
                    logger.error(
                        "Rate limit exceeded after %d attempts",
                        max_attempts,
                    )

            except Exception as e:
                last_exception = e
                if attempt < max_attempts - 1:
                    logger.warning(
                        "Context generation failed (attempt %d/%d): %s. Retrying...",
                        attempt + 1,
                        max_attempts,
                        str(e),
                    )
                    await asyncio.sleep(1.0 * (attempt + 1))
                else:
                    logger.error(
                        "Context generation failed after %d attempts: %s",
                        max_attempts,
                        str(e),
                    )

        if last_exception:
            raise RuntimeError(
                f"Failed to generate context after {max_attempts} attempts: {last_exception}"
            ) from last_exception

        if not response.content or len(response.content) == 0:
            raise ValueError("Empty response from LLM")

        context_text = ""
        for block in response.content:
            if hasattr(block, "text"):
                context_text += block.text
            elif isinstance(block, str):
                context_text += block

        if not context_text.strip():
            raise ValueError("Empty context text from LLM")

        return context_text.strip()

    def _generate_cost_context_with_template(
        self,
        cost_record: FOCUSCostData,
    ) -> str:
        """Generate context using template-based approach for cost data.

        Args:
            cost_record: FOCUS cost data record

        Returns:
            Template-generated contextual description
        """
        parts = []

        parts.append(
            f"This {cost_record.provider.upper()} {cost_record.service_name} "
            f"{cost_record.resource_type} instance in {cost_record.region_name} "
            f"costs ${cost_record.list_unit_price} per {cost_record.pricing_unit}."
        )

        if cost_record.service_category:
            parts.append(f"Service category: {cost_record.service_category}.")

        if cost_record.pricing_category:
            pricing_info = {
                "OnDemand": "on-demand pricing with no commitment",
                "Reserved": "reserved instance pricing with 1-3 year commitment (30-50% savings)",
                "Spot": "spot instance pricing with up to 70% savings (interruptible)",
                "Committed": "committed use discounts for sustained usage",
                "SavingsPlan": "savings plan with flexible commitment",
            }
            pricing_desc = pricing_info.get(cost_record.pricing_category, cost_record.pricing_category)
            parts.append(f"Pricing model: {pricing_desc}.")

        if cost_record.sku_description:
            parts.append(f"Description: {cost_record.sku_description[:150]}.")

        use_cases = self._infer_use_cases(cost_record)
        if use_cases:
            parts.append(f"Typical use cases: {', '.join(use_cases)}.")

        optimization_opportunities = self._identify_optimization_opportunities(cost_record)
        if optimization_opportunities:
            parts.append(f"Optimization opportunities: {', '.join(optimization_opportunities)}.")

        if cost_record.tags:
            environment = cost_record.tags.get("Environment") or cost_record.tags.get("environment")
            if environment:
                parts.append(f"Environment: {environment}.")

        context = " ".join(parts)

        if len(context) > self.max_context_length:
            context = context[:self.max_context_length - 3] + "..."

        return context

    def _build_cost_context_prompt(
        self,
        cost_record: FOCUSCostData,
    ) -> str:
        """Build prompt for LLM context generation for cost data.

        Args:
            cost_record: FOCUS cost data record

        Returns:
            Prompt string
        """
        prompt_parts = [
            "Generate a concise contextual description (100-200 words, max 2000 chars) for this cloud cost record.",
            "The description will be prepended before embedding to improve retrieval accuracy.",
            "",
            "Focus on:",
            "1. Use case scenarios (what workloads is this optimized for?)",
            "2. Cost optimization opportunities (reserved instances, spot, etc.)",
            "3. Comparison with alternatives (similar resources, different regions)",
            "4. Performance characteristics (if available)",
            "5. Cost efficiency context (cost per unit of performance)",
            "",
            "Cost Record Details:",
            f"- Provider: {cost_record.provider.upper()}",
            f"- Service: {cost_record.service_name}",
            f"- Resource Type: {cost_record.resource_type}",
            f"- Region: {cost_record.region_name} ({cost_record.region_id})",
            f"- Price: ${cost_record.list_unit_price} per {cost_record.pricing_unit}",
            f"- Pricing Model: {cost_record.pricing_category}",
            f"- Service Category: {cost_record.service_category}",
        ]

        if cost_record.service_subcategory:
            prompt_parts.append(f"- Service Subcategory: {cost_record.service_subcategory}")

        if cost_record.sku_description:
            prompt_parts.append(f"- SKU Description: {cost_record.sku_description}")

        if cost_record.charge_description:
            prompt_parts.append(f"- Charge Description: {cost_record.charge_description}")

        if cost_record.tags:
            environment = cost_record.tags.get("Environment") or cost_record.tags.get("environment")
            if environment:
                prompt_parts.append(f"- Environment: {environment}")

        prompt_parts.extend([
            "",
            "Generate a contextual description that emphasizes:",
            "- Cost optimization opportunities (reserved instances, spot instances, savings plans)",
            "- Use case matching (what workloads benefit from this resource)",
            "- Comparison context (how this compares to similar resources or regions)",
            "- Cost efficiency (cost per performance unit if applicable)",
            "",
            "The description should be natural, informative, and help the embedding model",
            "understand the cost context and optimization opportunities. Keep it concise (100-200 words).",
        ])

        return "\n".join(prompt_parts)

    def _infer_use_cases(self, cost_record: FOCUSCostData) -> list[str]:
        """Infer use cases from cost record.

        Args:
            cost_record: FOCUS cost data record

        Returns:
            List of inferred use cases
        """
        use_cases = []

        service_name_lower = cost_record.service_name.lower()
        resource_type_lower = cost_record.resource_type.lower()

        if "ec2" in service_name_lower or "compute" in service_name_lower:
            if "gpu" in resource_type_lower or "p3" in resource_type_lower or "p4" in resource_type_lower:
                use_cases.append("machine learning training")
                use_cases.append("deep learning workloads")
            elif "t3" in resource_type_lower or "t4g" in resource_type_lower:
                use_cases.append("web applications")
                use_cases.append("development environments")
            elif "m5" in resource_type_lower or "m6" in resource_type_lower:
                use_cases.append("general-purpose applications")
                use_cases.append("databases")
            elif "c5" in resource_type_lower or "c6" in resource_type_lower:
                use_cases.append("compute-intensive workloads")
                use_cases.append("high-performance computing")

        if "rds" in service_name_lower or "database" in service_name_lower:
            use_cases.append("relational databases")
            use_cases.append("transactional workloads")

        if "s3" in service_name_lower or "storage" in service_name_lower:
            use_cases.append("object storage")
            use_cases.append("data archiving")

        if "lambda" in service_name_lower or "function" in service_name_lower:
            use_cases.append("serverless applications")
            use_cases.append("event-driven workloads")

        return use_cases[:3]

    def _identify_optimization_opportunities(self, cost_record: FOCUSCostData) -> list[str]:
        """Identify optimization opportunities.

        Args:
            cost_record: FOCUS cost data record

        Returns:
            List of optimization opportunities
        """
        opportunities = []

        if cost_record.pricing_category == "OnDemand":
            opportunities.append("consider reserved instances for 30-50% savings")
            opportunities.append("evaluate spot instances for fault-tolerant workloads (up to 70% savings)")

        if cost_record.service_category == "Compute":
            opportunities.append("rightsizing opportunities based on actual usage")
            opportunities.append("auto-scaling to match demand")

        if cost_record.provider == "aws":
            opportunities.append("AWS Savings Plans for flexible commitment")

        if cost_record.provider == "gcp":
            opportunities.append("Committed Use Discounts for sustained usage")

        if cost_record.provider == "azure":
            opportunities.append("Azure Reserved Instances for 1-3 year commitments")

        return opportunities[:3]


context_generator = ContextGenerator()

