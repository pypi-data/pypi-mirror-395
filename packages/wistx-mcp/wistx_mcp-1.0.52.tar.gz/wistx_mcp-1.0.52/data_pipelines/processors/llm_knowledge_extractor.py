"""LLM-based knowledge article extractor using Gemini.

Extracts structured knowledge articles from unstructured content (HTML, PDFs, markdown).
Similar to LLMControlExtractor but for knowledge articles (guides, patterns, strategies).
"""

import asyncio
import json
import re
from typing import Any

from google.api_core import exceptions as google_exceptions

from ..utils.config import PipelineSettings
from ..utils.logger import setup_logger
from ..utils.circuit_breaker import CircuitBreaker, CircuitBreakerOpenError
from ..utils.global_rate_limiter import get_global_rate_limiter
from wistx_mcp.tools.lib.gemini_client import GeminiClient

logger = setup_logger(__name__)
settings = PipelineSettings()


class LLMKnowledgeExtractor:
    """Extract structured knowledge articles from unstructured text using Gemini.
    
    Production-grade implementation for knowledge articles (guides, patterns, strategies).
    """

    def __init__(self, chunk_size: int = 15000, chunk_overlap: int = 1000):
        """Initialize LLM knowledge extractor.
        
        Args:
            chunk_size: Maximum characters per chunk (default: 15000)
            chunk_overlap: Overlap between chunks in characters (default: 1000)
        """
        self.client = GeminiClient(api_key=settings.gemini_api_key)
        self.model = "gemini-2.5-flash"
        self.max_tokens = 8000
        self.temperature = 0.1
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.quota_wait_seconds = 120
        self.rate_limit_wait_seconds = 60
        self.max_quota_retries = 3
        self.max_rate_limit_retries = 5
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=5,
            recovery_timeout=120.0,
            success_threshold=2,
        )
        self._rate_limiter: Any = None

    def _chunk_content(self, content: str, is_markdown: bool = True) -> list[str]:
        """Intelligently chunk content for LLM processing.
        
        Args:
            content: Content to chunk
            is_markdown: Whether content is markdown
            
        Returns:
            List of content chunks
        """
        if len(content) <= self.chunk_size:
            return [content]

        chunks = []

        if is_markdown:
            header_pattern = r"^(#{1,3})\s+(.+)$"
            lines = content.split("\n")
            current_chunk = []
            current_size = 0

            for line in lines:
                line_size = len(line) + 1

                if re.match(header_pattern, line, re.MULTILINE):
                    if current_chunk and current_size >= self.chunk_size * 0.7:
                        chunks.append("\n".join(current_chunk))
                        overlap_lines = current_chunk[-self.chunk_overlap // 50:]
                        current_chunk = overlap_lines + [line]
                        current_size = sum(len(l) + 1 for l in current_chunk)
                    else:
                        current_chunk.append(line)
                        current_size += line_size
                else:
                    if current_size + line_size > self.chunk_size:
                        if current_chunk:
                            chunks.append("\n".join(current_chunk))
                            overlap_lines = current_chunk[-self.chunk_overlap // 50:]
                            current_chunk = overlap_lines + [line]
                            current_size = sum(len(l) + 1 for l in current_chunk)
                        else:
                            current_chunk.append(line)
                            current_size += line_size
                    else:
                        current_chunk.append(line)
                        current_size += line_size

            if current_chunk:
                chunks.append("\n".join(current_chunk))
        else:
            paragraphs = content.split("\n\n")
            current_chunk = []
            current_size = 0

            for para in paragraphs:
                para_size = len(para) + 2

                if current_size + para_size > self.chunk_size:
                    if current_chunk:
                        chunks.append("\n\n".join(current_chunk))
                        overlap_paras = current_chunk[-self.chunk_overlap // 200:]
                        current_chunk = overlap_paras + [para]
                        current_size = sum(len(p) + 2 for p in current_chunk)
                    else:
                        current_chunk.append(para)
                        current_size += para_size
                else:
                    current_chunk.append(para)
                    current_size += para_size

            if current_chunk:
                chunks.append("\n\n".join(current_chunk))

        return chunks

    def _get_extraction_prompt(
        self,
        content: str,
        domain: str,
        subdomain: str,
        source_url: str,
        chunk_index: int | None = None,
        total_chunks: int | None = None,
    ) -> str:
        """Generate extraction prompt for knowledge articles.
        
        Args:
            content: Content to extract from
            domain: Knowledge domain
            subdomain: Subdomain
            source_url: Source URL
            chunk_index: Current chunk index (if chunked)
            total_chunks: Total number of chunks
            
        Returns:
            Extraction prompt string
        """
        chunk_info = ""
        if chunk_index is not None and total_chunks:
            chunk_info = f"\n\nNote: This is chunk {chunk_index + 1} of {total_chunks}. Extract knowledge articles from this section."

        return f"""You are an expert {domain} knowledge engineer. Extract structured knowledge articles from the following content.

Domain: {domain}
Subdomain: {subdomain}
Source: {source_url}
{chunk_info}

Content:
{content[:50000]}

Extract ALL knowledge articles (guides, patterns, strategies, best practices) from this content. For each article, provide:

**IMPORTANT FILTERING RULES:**
- Do NOT extract navigation links, menu items, or single-line content
- Do NOT extract content shorter than 200 characters
- Do NOT extract titles shorter than 10 characters
- Only extract substantial knowledge articles with meaningful, detailed content
- Skip any content that is just a link or reference without explanation

For each article, provide:

1. **Title**: Clear, descriptive title
2. **Summary**: 50-200 word summary
3. **Content**: Full article content (preserve formatting)
4. **Content Type**: One of: guide, pattern, strategy, checklist, reference, best_practice
5. **Tags**: 5-10 relevant tags
6. **Categories**: Hierarchical categories
7. **Industries**: Applicable industries (REQUIRED - infer from content if not explicitly mentioned)
8. **Cloud Providers**: Any cloud providers mentioned (AWS, GCP, Azure, Oracle Cloud, IBM Cloud, Alibaba Cloud, etc.) - REQUIRED: Infer from content, services mentioned, or context. If content is cloud-agnostic but discusses cloud compliance, use ["multi-cloud"] or leave empty.
9. **Services**: Specific cloud services mentioned from ANY provider (REQUIRED - extract all cloud services referenced, e.g., S3, RDS, Cloud Storage, Blob Storage, etc.)
10. **Structured Data**: Domain-specific structured fields
11. **Cross-Domain Impacts**: Compliance, cost, security implications (REQUIRED - analyze and infer from content)

Return JSON in this format:
{{
  "articles": [
    {{
      "title": "Article title",
      "summary": "Brief summary...",
      "content": "Full article content...",
      "content_type": "guide",
      "tags": ["tag1", "tag2"],
      "categories": ["category1", "subcategory1"],
      "industries": ["healthcare", "finance"],
      "cloud_providers": ["aws"],  // REQUIRED: Any cloud providers mentioned (AWS, GCP, Azure, Oracle, IBM, Alibaba, etc.) or ["multi-cloud"] if cloud-agnostic
      "services": ["rds", "s3"],  // REQUIRED: Extract all cloud services mentioned from ANY provider
      "structured_data": {{
        "compliance_type": "guidance",
        "standard": "PCI-DSS"
      }},
      "compliance_impact": {{  // REQUIRED: Analyze compliance implications
        "standards": ["PCI-DSS"],
        "requirements": ["encryption"]
      }},
      "cost_impact": {{  // REQUIRED: Analyze cost implications (can be null if not applicable)
        "additional_cost": "5-10%",
        "optimization_opportunities": ["reserved-instances"]
      }},
      "security_impact": {{  // REQUIRED: Analyze security implications
        "threats_mitigated": ["data-breach"]
      }}
    }}
  ]
}}

Be thorough and extract ALL knowledge articles found in this content. If no articles are found, return {{"articles": []}}."""

    async def extract_articles(
        self,
        content: str,
        domain: str,
        subdomain: str,
        source_url: str,
        prefer_markdown: bool = True,
        markdown_content: str | None = None,
    ) -> list[dict[str, Any]]:
        """Extract knowledge articles from content using Gemini.
        
        Args:
            content: Content (text or markdown)
            domain: Knowledge domain
            subdomain: Subdomain
            source_url: Source URL
            prefer_markdown: Whether to prefer markdown if available
            markdown_content: Markdown version of content (if available)
            
        Returns:
            List of extracted article dictionaries
        """
        if not content or len(content.strip()) < 100:
            logger.warning("Content too short for extraction: %s", source_url)
            return []

        is_markdown = prefer_markdown and (
            markdown_content is not None or content.startswith("#") or "##" in content[:500]
        )

        if markdown_content and prefer_markdown:
            content_to_use = markdown_content
            is_markdown = True
        else:
            content_to_use = content

        chunks = self._chunk_content(content_to_use, is_markdown=is_markdown)

        if len(chunks) > 1:
            logger.info(
                "Processing %d chunks from %s (total size: %d)",
                len(chunks),
                source_url,
                len(content_to_use),
            )

        all_articles = []
        quota_retry_count = 0
        rate_limit_retry_count = 0

        for i, chunk in enumerate(chunks):
            retry_attempt = 0
            max_retries = self.max_rate_limit_retries
            
            while retry_attempt <= max_retries:
                try:
                    prompt = self._get_extraction_prompt(
                        content=chunk,
                        domain=domain,
                        subdomain=subdomain,
                        source_url=source_url,
                        chunk_index=i if len(chunks) > 1 else None,
                        total_chunks=len(chunks) if len(chunks) > 1 else None,
                    )

                    try:
                        if self._rate_limiter is None:
                            self._rate_limiter = await get_global_rate_limiter(
                                max_calls=getattr(settings, "api_rate_limit_max_calls", 100),
                                period=getattr(settings, "api_rate_limit_period_seconds", 60.0)
                            )
                            max_calls = getattr(settings, "api_rate_limit_max_calls", 100)
                            period = getattr(settings, "api_rate_limit_period_seconds", 60.0)
                            if max_calls != 100 or period != 60.0:
                                await self._rate_limiter.update_limits(max_calls=max_calls, period=period)
                        
                        await self._rate_limiter.acquire()
                        
                        llm_timeout = getattr(settings, "llm_api_timeout_seconds", 90.0)
                        response_text = await asyncio.wait_for(
                            self.circuit_breaker.call_async(
                                self.client.chat_completion,
                                messages=[{"role": "user", "content": prompt}],
                                model=self.model,
                                temperature=self.temperature,
                                max_tokens=self.max_tokens,
                                response_format={"type": "json_object"},
                            ),
                            timeout=llm_timeout
                        )
                    except asyncio.TimeoutError:
                        logger.error("LLM API timeout for chunk %d/%d of %s (timeout: %.1fs)", i + 1, len(chunks), source_url, llm_timeout)
                        break
                    except CircuitBreakerOpenError:
                        logger.error("Circuit breaker OPEN - skipping extraction for chunk %d", i + 1)
                        break

                    if not response_text:
                        logger.warning("Empty response from LLM for chunk %d", i)
                        break

                    try:
                        result = json.loads(response_text)
                        articles = result.get("articles", [])
                        if articles:
                            for article in articles:
                                article["source_url"] = source_url
                                all_articles.append(article)
                            logger.debug(
                                "Extracted %d articles from chunk %d/%d",
                                len(articles),
                                i + 1,
                                len(chunks),
                            )
                        quota_retry_count = 0
                        rate_limit_retry_count = 0
                        break
                    except json.JSONDecodeError as e:
                        logger.error("Failed to parse LLM response as JSON: %s", e)
                        logger.debug("Response text: %s", response_text[:500])
                        break

                except (google_exceptions.ResourceExhausted, google_exceptions.PermissionDenied, RuntimeError) as e:
                    error_str = str(e).lower()
                    is_quota = isinstance(e, google_exceptions.PermissionDenied) or "quota" in error_str or "permission" in error_str
                    
                    if is_quota:
                        quota_retry_count += 1
                        if quota_retry_count > self.max_quota_retries:
                            logger.error(
                                "Gemini quota exceeded after %d retries for chunk %d of %s. Skipping remaining chunks. "
                                "Please check your Gemini billing and quota limits.",
                                self.max_quota_retries,
                                i + 1,
                                source_url,
                            )
                            logger.warning(
                                "Returning %d articles extracted so far. To get all articles, increase Gemini quota and re-run.",
                                len(all_articles),
                            )
                            break
                        
                        wait_time = self.quota_wait_seconds * (2 ** (quota_retry_count - 1))
                        logger.warning(
                            "Gemini quota exceeded for chunk %d of %s (attempt %d/%d). Waiting %d seconds before retry...",
                            i + 1,
                            source_url,
                            quota_retry_count,
                            self.max_quota_retries,
                            wait_time,
                        )
                        await asyncio.sleep(wait_time)
                        retry_attempt += 1
                    else:
                        rate_limit_retry_count += 1
                        if rate_limit_retry_count > self.max_rate_limit_retries:
                            logger.error("Gemini rate limit exceeded after %d retries for chunk %d of %s: %s", self.max_rate_limit_retries, i + 1, source_url, e)
                            break
                        
                        wait_time = min(self.rate_limit_wait_seconds * (2 ** (rate_limit_retry_count - 1)), 300)
                        logger.warning(
                            "Rate limit exceeded for chunk %d of %s (attempt %d/%d). Waiting %d seconds before retry...",
                            i + 1,
                            source_url,
                            rate_limit_retry_count,
                            self.max_rate_limit_retries,
                            wait_time,
                        )
                        await asyncio.sleep(wait_time)
                        retry_attempt += 1
                        continue
                
                except asyncio.TimeoutError:
                    logger.error("Timeout extracting articles from chunk %d/%d of %s", i + 1, len(chunks), source_url)
                    break
                except (ValueError, TypeError, KeyError, AttributeError, ConnectionError) as e:
                    logger.error("Error extracting articles from chunk %d: %s", i, e)
                    break
                
                if retry_attempt > max_retries:
                    logger.warning("Max retries exceeded for chunk %d of %s. Skipping chunk.", i + 1, source_url)
                    break
            
            if quota_retry_count > self.max_quota_retries:
                break

        logger.info("Extracted %d total articles from %s", len(all_articles), source_url)
        return all_articles

