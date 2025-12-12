"""Contextual Chunker implementing Anthropic's Contextual Retrieval approach.

This module implements semantic chunking with LLM-generated context prepended
to each chunk before embedding. This significantly improves retrieval accuracy
by providing context that would otherwise be lost when chunks are isolated.

Based on Anthropic's research showing 49% reduction in retrieval failures
when combining contextual embeddings with BM25 hybrid search.

Reference: https://www.anthropic.com/news/contextual-retrieval
"""

import asyncio
import hashlib
import logging
import re
from dataclasses import dataclass, field
from typing import Any

from wistx_mcp.config import settings
from wistx_mcp.tools.lib.gemini_client import GeminiClient
from wistx_mcp.tools.lib.retry_utils import with_timeout_and_retry

logger = logging.getLogger(__name__)


@dataclass
class ContextualChunk:
    """A chunk with prepended context for improved retrieval."""
    chunk_id: str
    original_content: str
    context: str
    contextualized_content: str  # context + original_content
    source_url: str
    document_title: str
    section_title: str | None = None
    chunk_index: int = 0
    total_chunks: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "chunk_id": self.chunk_id,
            "original_content": self.original_content,
            "context": self.context,
            "contextualized_content": self.contextualized_content,
            "source_url": self.source_url,
            "document_title": self.document_title,
            "section_title": self.section_title,
            "chunk_index": self.chunk_index,
            "total_chunks": self.total_chunks,
            "metadata": self.metadata,
        }


class ContextualChunker:
    """Semantic chunker with LLM-generated context for improved retrieval.
    
    Implements Anthropic's contextual retrieval approach:
    1. Chunk documents semantically (respecting structure)
    2. Generate context for each chunk using LLM
    3. Prepend context to chunk before embedding
    """
    
    def __init__(
        self,
        chunk_size: int = 1500,
        chunk_overlap: int = 200,
        min_chunk_size: int = 100,
        max_context_length: int = 200,
    ):
        """Initialize contextual chunker.
        
        Args:
            chunk_size: Target size for each chunk in characters
            chunk_overlap: Overlap between chunks in characters
            min_chunk_size: Minimum chunk size (smaller chunks are merged)
            max_context_length: Maximum length of generated context
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
        self.max_context_length = max_context_length
        
        if settings.gemini_api_key:
            self.llm_client = GeminiClient(api_key=settings.gemini_api_key)
        else:
            logger.warning("Gemini API key not configured - context generation disabled")
            self.llm_client = None
        
        self.model = "gemini-2.5-flash"
        self.temperature = 0.0  # Deterministic for consistency
    
    async def chunk_document(
        self,
        content: str,
        source_url: str,
        document_title: str,
        generate_context: bool = True,
        max_concurrent_context: int = 5,
    ) -> list[ContextualChunk]:
        """Chunk a document and generate context for each chunk.
        
        Args:
            content: Document content (markdown or plain text)
            source_url: Source URL of the document
            document_title: Title of the document
            generate_context: Whether to generate LLM context
            max_concurrent_context: Max concurrent context generation calls
            
        Returns:
            List of ContextualChunk objects
        """
        # Step 1: Semantic chunking
        raw_chunks = self._semantic_chunk(content)
        
        if not raw_chunks:
            logger.warning("No chunks generated for document: %s", document_title)
            return []
        
        logger.info(
            "Generated %d raw chunks for document: %s",
            len(raw_chunks),
            document_title,
        )
        
        # Step 2: Generate context for each chunk
        if generate_context and self.llm_client:
            chunks = await self._generate_contexts(
                raw_chunks,
                content,
                source_url,
                document_title,
                max_concurrent_context,
            )
        else:
            # Create chunks without LLM context
            chunks = self._create_chunks_without_context(
                raw_chunks,
                source_url,
                document_title,
            )
        
        return chunks
    
    def _semantic_chunk(self, content: str) -> list[dict[str, Any]]:
        """Perform semantic chunking that respects document structure.
        
        Args:
            content: Document content
            
        Returns:
            List of raw chunk dictionaries with content and metadata
        """
        chunks = []
        
        # Detect if content is markdown
        is_markdown = self._is_markdown(content)
        
        if is_markdown:
            chunks = self._chunk_markdown(content)
        else:
            chunks = self._chunk_plain_text(content)
        
        # Merge small chunks
        chunks = self._merge_small_chunks(chunks)

        return chunks

    def _is_markdown(self, content: str) -> bool:
        """Detect if content is markdown."""
        markdown_indicators = [
            r"^#{1,6}\s",  # Headers
            r"^\*\s",      # Unordered lists
            r"^\d+\.\s",   # Ordered lists
            r"```",        # Code blocks
            r"\[.*\]\(.*\)",  # Links
        ]

        for pattern in markdown_indicators:
            if re.search(pattern, content, re.MULTILINE):
                return True
        return False

    def _chunk_markdown(self, content: str) -> list[dict[str, Any]]:
        """Chunk markdown content respecting structure."""
        chunks = []
        current_section = None
        current_content = []
        current_size = 0

        lines = content.split("\n")

        for line in lines:
            # Check for headers
            header_match = re.match(r"^(#{1,6})\s+(.+)$", line)

            if header_match:
                # Save current chunk if exists
                if current_content and current_size >= self.min_chunk_size:
                    chunks.append({
                        "content": "\n".join(current_content),
                        "section_title": current_section,
                    })
                    current_content = []
                    current_size = 0

                current_section = header_match.group(2)
                current_content.append(line)
                current_size += len(line)
            else:
                # Check if adding this line exceeds chunk size
                if current_size + len(line) > self.chunk_size and current_content:
                    chunks.append({
                        "content": "\n".join(current_content),
                        "section_title": current_section,
                    })
                    # Keep overlap
                    overlap_lines = current_content[-3:] if len(current_content) > 3 else []
                    current_content = overlap_lines + [line]
                    current_size = sum(len(l) for l in current_content)
                else:
                    current_content.append(line)
                    current_size += len(line)

        # Don't forget the last chunk
        if current_content:
            chunks.append({
                "content": "\n".join(current_content),
                "section_title": current_section,
            })

        return chunks

    def _chunk_plain_text(self, content: str) -> list[dict[str, Any]]:
        """Chunk plain text content by paragraphs."""
        chunks = []
        paragraphs = content.split("\n\n")

        current_content = []
        current_size = 0

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            if current_size + len(para) > self.chunk_size and current_content:
                chunks.append({
                    "content": "\n\n".join(current_content),
                    "section_title": None,
                })
                current_content = [para]
                current_size = len(para)
            else:
                current_content.append(para)
                current_size += len(para)

        if current_content:
            chunks.append({
                "content": "\n\n".join(current_content),
                "section_title": None,
            })

        return chunks

    def _merge_small_chunks(self, chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Merge chunks that are too small."""
        if not chunks:
            return chunks

        merged = []
        current = chunks[0]

        for next_chunk in chunks[1:]:
            current_size = len(current["content"])
            next_size = len(next_chunk["content"])

            if current_size < self.min_chunk_size and current_size + next_size <= self.chunk_size:
                # Merge chunks
                current["content"] = current["content"] + "\n\n" + next_chunk["content"]
                if next_chunk.get("section_title"):
                    current["section_title"] = next_chunk["section_title"]
            else:
                if current_size >= self.min_chunk_size:
                    merged.append(current)
                current = next_chunk

        # Add last chunk
        if len(current["content"]) >= self.min_chunk_size:
            merged.append(current)
        elif merged:
            # Merge with previous if too small
            merged[-1]["content"] += "\n\n" + current["content"]
        else:
            merged.append(current)

        return merged

    async def _generate_contexts(
        self,
        raw_chunks: list[dict[str, Any]],
        full_document: str,
        source_url: str,
        document_title: str,
        max_concurrent: int,
    ) -> list[ContextualChunk]:
        """Generate context for each chunk using LLM."""
        semaphore = asyncio.Semaphore(max_concurrent)
        total_chunks = len(raw_chunks)

        async def generate_single_context(idx: int, chunk_data: dict) -> ContextualChunk:
            async with semaphore:
                context = await self._generate_chunk_context(
                    chunk_data["content"],
                    full_document[:5000],  # First 5000 chars for context
                    document_title,
                )

                chunk_id = self._generate_chunk_id(source_url, idx)
                contextualized = f"{context}\n\n{chunk_data['content']}"

                return ContextualChunk(
                    chunk_id=chunk_id,
                    original_content=chunk_data["content"],
                    context=context,
                    contextualized_content=contextualized,
                    source_url=source_url,
                    document_title=document_title,
                    section_title=chunk_data.get("section_title"),
                    chunk_index=idx,
                    total_chunks=total_chunks,
                )

        tasks = [generate_single_context(i, chunk) for i, chunk in enumerate(raw_chunks)]
        chunks = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions
        valid_chunks = []
        for chunk in chunks:
            if isinstance(chunk, Exception):
                logger.warning("Context generation failed: %s", chunk)
            else:
                valid_chunks.append(chunk)

        return valid_chunks

    async def _generate_chunk_context(
        self,
        chunk_content: str,
        document_summary: str,
        document_title: str,
    ) -> str:
        """Generate context for a single chunk using LLM.

        This is the core of Anthropic's contextual retrieval approach.
        """
        prompt = f"""<document>
{document_summary}
</document>

Here is the chunk we want to situate within the whole document:
<chunk>
{chunk_content}
</chunk>

Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk. Answer only with the succinct context and nothing else. Keep it under {self.max_context_length} characters."""

        try:
            response = await with_timeout_and_retry(
                self._call_llm,
                timeout_seconds=15.0,
                max_attempts=2,
                retryable_exceptions=(Exception,),
                prompt=prompt,
            )

            if response:
                # Truncate if too long
                return response[:self.max_context_length]
            return f"From {document_title}:"
        except Exception as e:
            logger.warning("Context generation failed: %s", e)
            return f"From {document_title}:"

    async def _call_llm(self, prompt: str) -> str | None:
        """Call the LLM with the given prompt."""
        if not self.llm_client:
            return None

        messages = [{"role": "user", "content": prompt}]

        response = await self.llm_client.chat_completion(
            messages=messages,
            model=self.model,
            temperature=self.temperature,
            max_tokens=300,
        )

        return response

    def _generate_chunk_id(self, source_url: str, chunk_index: int) -> str:
        """Generate a unique chunk ID."""
        content = f"{source_url}:{chunk_index}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _create_chunks_without_context(
        self,
        raw_chunks: list[dict[str, Any]],
        source_url: str,
        document_title: str,
    ) -> list[ContextualChunk]:
        """Create chunks without LLM-generated context."""
        total_chunks = len(raw_chunks)
        chunks = []

        for idx, chunk_data in enumerate(raw_chunks):
            chunk_id = self._generate_chunk_id(source_url, idx)
            # Use document title as basic context
            basic_context = f"From {document_title}:"
            if chunk_data.get("section_title"):
                basic_context = f"From {document_title}, section '{chunk_data['section_title']}':"

            chunks.append(ContextualChunk(
                chunk_id=chunk_id,
                original_content=chunk_data["content"],
                context=basic_context,
                contextualized_content=f"{basic_context}\n\n{chunk_data['content']}",
                source_url=source_url,
                document_title=document_title,
                section_title=chunk_data.get("section_title"),
                chunk_index=idx,
                total_chunks=total_chunks,
            ))

        return chunks

