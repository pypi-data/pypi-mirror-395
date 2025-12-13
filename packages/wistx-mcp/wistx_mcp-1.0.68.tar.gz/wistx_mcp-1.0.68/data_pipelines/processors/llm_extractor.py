"""LLM-based compliance control extractor using Gemini.

This module provides production-grade extraction of structured compliance controls
from unstructured documents (HTML, PDFs, markdown) using Gemini.

Features:
- Prefers markdown over plain text (better structure preservation)
- Intelligent chunking for large documents
- Deduplication of overlapping content
- Batch processing with parallel execution
"""

import hashlib
import json
import re
import asyncio
from typing import Any

from google.api_core import exceptions as google_exceptions

from ..utils.config import PipelineSettings
from ..utils.logger import setup_logger
from ..utils.circuit_breaker import CircuitBreaker, CircuitBreakerOpenError
from wistx_mcp.tools.lib.gemini_client import GeminiClient

logger = setup_logger(__name__)
settings = PipelineSettings()


class LLMControlExtractor:
    """Extract structured compliance controls from unstructured text using Gemini.

    Production-grade implementation with:
    - Markdown preference (better structure preservation)
    - Intelligent chunking for large documents
    - Deduplication of overlapping content
    - Structured output (JSON schema)
    - Batch processing
    - Rate limiting and retries
    - Error handling
    - Validation
    """

    def __init__(self, chunk_size: int = 10000, chunk_overlap: int = 500):
        """Initialize LLM control extractor.

        Args:
            chunk_size: Maximum characters per chunk (default: 10000)
            chunk_overlap: Overlap between chunks in characters (default: 500)
        """
        self.client = GeminiClient(api_key=settings.gemini_api_key)
        self.model = "gemini-2.5-flash"
        self.max_tokens = 4000
        self.temperature = 0.1
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.seen_controls: dict[str, dict[str, Any]] = {}
        self.quota_wait_seconds = 120
        self.rate_limit_wait_seconds = 60
        self.max_quota_retries = 3
        self.max_rate_limit_retries = 5
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=5,
            recovery_timeout=120.0,
            success_threshold=2,
        )

    def _chunk_content(self, content: str, is_markdown: bool = True) -> list[str]:
        """Intelligently chunk content for LLM processing.

        For markdown: chunks by headers (##, ###) to preserve structure
        For plain text: chunks by paragraphs with overlap

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
            header_pattern = r"^(#{2,3})\s+(.+)$"
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

        logger.debug("Chunked content into %d chunks (avg size: %d)", len(chunks), sum(len(c) for c in chunks) // len(chunks) if chunks else 0)
        return chunks

    def _get_control_fingerprint(self, control: dict[str, Any]) -> str:
        """Generate fingerprint for deduplication.

        Uses control_id if available, otherwise hashes key fields.

        Args:
            control: Control dictionary

        Returns:
            Fingerprint string
        """
        control_id = control.get("control_id", "").strip().lower()
        if control_id:
            return f"id:{control_id}"

        title = control.get("title", "").strip().lower()
        description = control.get("description", "").strip().lower()[:200]

        fingerprint_content = f"{title}|{description}"
        return f"hash:{hashlib.md5(fingerprint_content.encode()).hexdigest()}"

    def _deduplicate_controls(self, controls: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Deduplicate controls based on fingerprint.

        Args:
            controls: List of control dictionaries

        Returns:
            Deduplicated list of controls
        """
        seen = {}
        deduplicated = []

        for control in controls:
            fingerprint = self._get_control_fingerprint(control)

            if fingerprint in seen:
                existing = seen[fingerprint]
                existing_sources = existing.get("source_urls", [existing.get("source_url", "")])
                new_source = control.get("source_url", "")

                if new_source and new_source not in existing_sources:
                    if isinstance(existing_sources, str):
                        existing["source_urls"] = [existing_sources, new_source]
                    else:
                        existing["source_urls"].append(new_source)
                    existing["source_url"] = existing_sources[0] if isinstance(existing_sources, list) else existing_sources

                logger.debug("Skipping duplicate control: %s", fingerprint)
                continue

            seen[fingerprint] = control
            deduplicated.append(control)

        logger.info("Deduplicated %d controls to %d unique controls", len(controls), len(deduplicated))
        return deduplicated

    async def _call_llm_internal(self, prompt: str) -> str:
        """Internal method to call LLM (wrapped by circuit breaker).

        Args:
            prompt: Prompt string

        Returns:
            LLM response text
        """
        return await self.client.chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert compliance analyst. Extract structured compliance controls from documents. Always return valid JSON with a 'controls' array.",
                },
                {"role": "user", "content": prompt},
            ],
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            response_format={"type": "json_object"},
        )

    def _get_extraction_prompt(self, content: str, standard: str, source_url: str, chunk_index: int | None = None, total_chunks: int | None = None) -> str:
        """Generate extraction prompt for Gemini.

        Args:
            content: Content chunk (markdown preferred)
            standard: Compliance standard name
            source_url: Source URL/path
            chunk_index: Current chunk index (if chunked)
            total_chunks: Total number of chunks (if chunked)

        Returns:
            Formatted prompt string
        """
        chunk_info = ""
        if chunk_index is not None and total_chunks is not None:
            chunk_info = f"\n\nNote: This is chunk {chunk_index + 1} of {total_chunks} from the same document."

        return f"""You are an expert compliance analyst. Extract structured compliance controls from the following {standard} compliance document.

Source: {source_url}{chunk_info}
Standard: {standard}

Document Content:
{content}

Extract ALL compliance controls, requirements, and guidelines from this document. For each control, provide:
- control_id: MUST follow the format "{standard}-X.Y.Z" where X, Y, Z are integers (1-999).
  * Use sequential numbering based on the document structure (e.g., {standard}-1.1.1, {standard}-1.1.2, {standard}-1.2.1)
  * X = Major section number (1-12)
  * Y = Subsection number (1-99)
  * Z = Specific control number (1-99)
  * You may use fewer levels if appropriate (e.g., {standard}-1.1, {standard}-2)
  * NEVER use alphabetic prefixes or suffixes (WRONG: {standard}-LS-001, {standard}-ACCT-02, {standard}-3.4.1.C)
  * Examples of VALID IDs: {standard}-1.1.1, {standard}-2.3, {standard}-10.2.1
  * Examples of INVALID IDs: {standard}-LS-001, {standard}-ACCT-02, {standard}-A.1.1, {standard}-3.4.1.C
- title: Brief title summarizing the control
- description: Detailed description of the control
- requirement: Full requirement text
- severity: HIGH, MEDIUM, LOW, or CRITICAL (based on impact)
- category: Main category (e.g., "encryption", "access_control", "network_security", "data_protection", "vulnerability_management", "monitoring_testing", "policy_procedures")
- subcategory: Subcategory if applicable (e.g., "data-at-rest", "data-in-transit", "firewall", "logging", "encryption")
- testing_procedures: List of testing/verification procedures
- applies_to: List of cloud resources this applies to (e.g., ["AWS::RDS::DBInstance", "GCP::SQL::Instance", "Azure::SQL::Database"])
- remediation: Remediation steps and guidance

Return a JSON object with a "controls" array. Each control should match this structure:
{{
  "controls": [
    {{
      "control_id": "string (required)",
      "title": "string (required)",
      "description": "string (required)",
      "requirement": "string (required)",
      "severity": "HIGH|MEDIUM|LOW|CRITICAL (required)",
      "category": "string (required)",
      "subcategory": "string or null",
      "testing_procedures": ["string"],
      "applies_to": ["string"],
      "remediation": {{
        "summary": "string",
        "steps": ["string"],
        "code_snippets": []
      }},
      "references": []
    }}
  ]
}}

Be thorough and extract ALL controls found in this document section. If no controls are found, return {{"controls": []}}."""

    async def extract_controls(
        self,
        content: str,
        standard: str,
        source_url: str,
        prefer_markdown: bool = True,
        markdown_content: str | None = None,
        user_id: str | None = None,
        organization_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """Extract compliance controls from content using Gemini.

        Prefers markdown over plain text for better structure preservation.
        Automatically chunks large documents.

        Args:
            content: Content (text or markdown)
            standard: Compliance standard name
            source_url: Source URL or file path
            prefer_markdown: Whether to prefer markdown if available
            markdown_content: Markdown version of content (if available)
            user_id: User ID for custom controls (optional)
            organization_id: Organization ID for custom controls (optional)

        Returns:
            List of extracted control dictionaries (deduplicated)
        """
        if not content or len(content.strip()) < 100:
            logger.warning("Content too short for extraction: %s", source_url)
            return []

        is_markdown = prefer_markdown and (markdown_content is not None or content.startswith("#") or "##" in content[:500])

        if markdown_content and prefer_markdown:
            content_to_use = markdown_content
            is_markdown = True
        else:
            content_to_use = content

        chunks = self._chunk_content(content_to_use, is_markdown=is_markdown)

        if len(chunks) > 1:
            logger.info("Processing %d chunks from %s (total size: %d)", len(chunks), source_url, len(content_to_use))

        all_controls = []
        quota_retry_count = 0
        rate_limit_retry_count = 0

        for i, chunk in enumerate(chunks):
            retry_attempt = 0
            max_retries = self.max_rate_limit_retries
            
            while retry_attempt <= max_retries:
                try:
                    chunk_index = i if len(chunks) > 1 else None
                    total_chunks = len(chunks) if len(chunks) > 1 else None

                    prompt = self._get_extraction_prompt(chunk, standard, source_url, chunk_index, total_chunks)

                    logger.debug("Extracting controls from chunk %d/%d of %s (chunk size: %d)", i + 1, len(chunks), source_url, len(chunk))

                    try:
                        response_content = await self.circuit_breaker.call_async(
                            self._call_llm_internal,
                            prompt
                        )
                    except CircuitBreakerOpenError:
                        logger.error("Gemini circuit breaker is OPEN - skipping LLM extraction for chunk %d", i + 1)
                        break

                    if not response_content:
                        logger.warning("Empty response from Gemini for chunk %d of %s", i + 1, source_url)
                        break

                    try:
                        result = json.loads(response_content)
                        chunk_controls = result.get("controls", [])
                        if not isinstance(chunk_controls, list):
                            logger.warning("Invalid controls format from Gemini for chunk %d of %s", i + 1, source_url)
                            break

                        for control in chunk_controls:
                            control["source_url"] = source_url
                            if user_id:
                                control["user_id"] = user_id
                            if organization_id:
                                control["organization_id"] = organization_id

                        all_controls.extend(chunk_controls)
                        logger.debug("Extracted %d controls from chunk %d/%d", len(chunk_controls), i + 1, len(chunks))
                        
                        quota_retry_count = 0
                        rate_limit_retry_count = 0
                        break

                    except json.JSONDecodeError as e:
                        logger.error("Failed to parse Gemini response as JSON for chunk %d of %s: %s", i + 1, source_url, e)
                        logger.debug("Response content: %s", response_content[:500])
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
                                "Returning %d controls extracted so far. To get all controls, increase Gemini quota and re-run.",
                                len(all_controls),
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
                            "Gemini rate limit exceeded for chunk %d of %s (attempt %d/%d). Waiting %d seconds before retry...",
                            i + 1,
                            source_url,
                            rate_limit_retry_count,
                            self.max_rate_limit_retries,
                            wait_time,
                        )
                        await asyncio.sleep(wait_time)
                        retry_attempt += 1
                        continue
                
                except (ValueError, TypeError, KeyError, AttributeError, IOError) as e:
                    logger.error("Error extracting controls from chunk %d of %s: %s", i + 1, source_url, e, exc_info=True)
                    break
                
                if retry_attempt > max_retries:
                    logger.warning("Max retries exceeded for chunk %d of %s. Skipping chunk.", i + 1, source_url)
                    break
            
            if quota_retry_count > self.max_quota_retries:
                break

        deduplicated = self._deduplicate_controls(all_controls)
        logger.info("Extracted %d controls from %s using Gemini (%d after deduplication)", len(all_controls), source_url, len(deduplicated))

        return deduplicated

    async def extract_controls_batch(
        self, contents: list[tuple[str, str, str, bool, str | None]]
    ) -> list[dict[str, Any]]:
        """Extract controls from multiple contents in batch.

        Args:
            contents: List of tuples (content, standard, source_url, prefer_markdown, markdown_content)

        Returns:
            List of all extracted controls (deduplicated across all sources)
        """
        tasks = [
            self.extract_controls(content, standard, url, prefer_markdown, markdown)
            for content, standard, url, prefer_markdown, markdown in contents
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_controls = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error("Batch extraction failed for item %d: %s", i, result)
            elif isinstance(result, list):
                all_controls.extend(result)

        final_deduplicated = self._deduplicate_controls(all_controls)
        logger.info("Batch extraction: %d total controls, %d after deduplication", len(all_controls), len(final_deduplicated))

        return final_deduplicated
