"""Section summarizer service - generates section-level summaries."""

import logging
from typing import Any

from api.config import settings

logger = logging.getLogger(__name__)


class SectionSummarizer:
    """Generates section-level summaries using AI."""

    def __init__(self):
        """Initialize section summarizer."""
        self.llm_client = None
        self.model = "claude-opus-4-1"

    async def generate_section_summary(
        self,
        section_title: str,
        articles: list[dict[str, Any]],
    ) -> str:
        """Generate section-level summary.

        Args:
            section_title: Section title
            articles: List of article dictionaries in section

        Returns:
            Generated summary
        """
        article_summaries = []
        for article in articles[:10]:
            title = article.get("title", "")
            summary = article.get("summary", "")
            article_summaries.append(f"- **{title}**: {summary}")

        prompt = f"""Generate a comprehensive section-level summary for:

Section Title: {section_title}

Components in this section:
{chr(10).join(article_summaries)}

Requirements:
1. Provide a high-level overview of what this section covers
2. Explain the relationships between components
3. Describe the overall purpose and functionality
4. Keep it concise (150-300 words)
5. Use clear, professional language

Summary:"""

        try:
            from anthropic import AsyncAnthropic

            anthropic_api_key = getattr(settings, "anthropic_api_key", None)
            if anthropic_api_key:
                client = AsyncAnthropic(api_key=anthropic_api_key)
                response = await client.messages.create(
                    model=self.model,
                    max_tokens=500,
                    messages=[{
                        "role": "user",
                        "content": prompt,
                    }],
                )
                summary = response.content[0].text if response.content else ""
                return summary.strip() if summary else self._fallback_summary(section_title, articles)
            else:
                logger.warning("ANTHROPIC_API_KEY not set, using fallback summary")
                return self._fallback_summary(section_title, articles)
        except Exception as e:
            logger.warning("Error generating section summary with AI: %s", e)
            return self._fallback_summary(section_title, articles)

    def _fallback_summary(
        self,
        section_title: str,
        articles: list[dict[str, Any]],
    ) -> str:
        """Generate fallback summary without AI.

        Args:
            section_title: Section title
            articles: List of articles

        Returns:
            Fallback summary
        """
        component_count = len(articles)
        component_names = [a.get("title", "") for a in articles[:5]]
        components_list = ", ".join(component_names)

        summary = (
            f"This section covers {section_title} and includes {component_count} components. "
            f"Key components include: {components_list}."
        )

        if component_count > 5:
            summary += f" And {component_count - 5} additional components."

        return summary


section_summarizer = SectionSummarizer()

