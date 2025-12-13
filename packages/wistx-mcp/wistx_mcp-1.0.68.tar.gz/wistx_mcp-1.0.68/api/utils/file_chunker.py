"""File chunking utility for intelligent content splitting."""

import logging
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class FileChunker:
    """Intelligent file chunker for code and documentation files."""

    def __init__(self, chunk_size: int = 15000, chunk_overlap: int = 1000):
        """Initialize file chunker.

        Args:
            chunk_size: Maximum characters per chunk (default: 15000)
            chunk_overlap: Overlap between chunks in characters (default: 1000)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_file(self, content: str, file_path: Path) -> list[dict[str, Any]]:
        """Chunk file content intelligently based on file type.

        Args:
            content: File content to chunk
            file_path: Path to file (for determining chunking strategy)

        Returns:
            List of chunks with metadata:
            {
                "chunk_index": 0,
                "content": "...",
                "start_line": 1,
                "end_line": 50,
                "parent_file": "path/to/file.py"
            }
        """
        if len(content) <= self.chunk_size:
            return [
                {
                    "chunk_index": 0,
                    "content": content,
                    "start_line": 1,
                    "end_line": len(content.split("\n")),
                    "parent_file": str(file_path),
                }
            ]

        extension = file_path.suffix.lower()

        if extension in [".md", ".rst", ".txt", ".markdown"]:
            return self._chunk_markdown(content, file_path)
        elif extension in [".py", ".js", ".ts", ".tsx", ".jsx", ".tf", ".yaml", ".yml", ".json"]:
            return self._chunk_code(content, file_path)
        else:
            return self._chunk_generic(content, file_path)

    def _chunk_code(self, content: str, file_path: Path) -> list[dict[str, Any]]:
        """Chunk code files line-by-line preserving structure.

        Args:
            content: Code content
            file_path: File path

        Returns:
            List of chunks
        """
        lines = content.split("\n")
        chunks = []
        current_chunk = []
        current_size = 0
        start_line = 1

        for i, line in enumerate(lines, 1):
            line_size = len(line) + 1

            if current_size + line_size > self.chunk_size:
                if current_chunk:
                    chunks.append({
                        "chunk_index": len(chunks),
                        "content": "\n".join(current_chunk),
                        "start_line": start_line,
                        "end_line": i - 1,
                        "parent_file": str(file_path),
                    })
                    overlap_lines = current_chunk[-self.chunk_overlap // 50:]
                    current_chunk = overlap_lines + [line]
                    current_size = sum(len(l) + 1 for l in current_chunk)
                    start_line = i - len(overlap_lines)
                else:
                    current_chunk.append(line)
                    current_size += line_size
            else:
                current_chunk.append(line)
                current_size += line_size

        if current_chunk:
            chunks.append({
                "chunk_index": len(chunks),
                "content": "\n".join(current_chunk),
                "start_line": start_line,
                "end_line": len(lines),
                "parent_file": str(file_path),
            })

        logger.debug(
            "Chunked code file %s into %d chunks",
            file_path,
            len(chunks),
        )
        return chunks

    def _chunk_markdown(self, content: str, file_path: Path) -> list[dict[str, Any]]:
        """Chunk markdown files header-aware preserving sections.

        Args:
            content: Markdown content
            file_path: File path

        Returns:
            List of chunks
        """
        header_pattern = r"^(#{1,3})\s+(.+)$"
        lines = content.split("\n")
        chunks = []
        current_chunk = []
        current_size = 0
        start_line = 1

        for i, line in enumerate(lines, 1):
            line_size = len(line) + 1

            if re.match(header_pattern, line, re.MULTILINE):
                if current_chunk and current_size >= self.chunk_size * 0.7:
                    chunks.append({
                        "chunk_index": len(chunks),
                        "content": "\n".join(current_chunk),
                        "start_line": start_line,
                        "end_line": i - 1,
                        "parent_file": str(file_path),
                    })
                    overlap_lines = current_chunk[-self.chunk_overlap // 50:]
                    current_chunk = overlap_lines + [line]
                    current_size = sum(len(l) + 1 for l in current_chunk)
                    start_line = i - len(overlap_lines)
                else:
                    current_chunk.append(line)
                    current_size += line_size
            else:
                if current_size + line_size > self.chunk_size:
                    if current_chunk:
                        chunks.append({
                            "chunk_index": len(chunks),
                            "content": "\n".join(current_chunk),
                            "start_line": start_line,
                            "end_line": i - 1,
                            "parent_file": str(file_path),
                        })
                        overlap_lines = current_chunk[-self.chunk_overlap // 50:]
                        current_chunk = overlap_lines + [line]
                        current_size = sum(len(l) + 1 for l in current_chunk)
                        start_line = i - len(overlap_lines)
                    else:
                        current_chunk.append(line)
                        current_size += line_size
                else:
                    current_chunk.append(line)
                    current_size += line_size

        if current_chunk:
            chunks.append({
                "chunk_index": len(chunks),
                "content": "\n".join(current_chunk),
                "start_line": start_line,
                "end_line": len(lines),
                "parent_file": str(file_path),
            })

        logger.debug(
            "Chunked markdown file %s into %d chunks",
            file_path,
            len(chunks),
        )
        return chunks

    def _chunk_generic(self, content: str, file_path: Path) -> list[dict[str, Any]]:
        """Chunk generic files paragraph-based.

        Args:
            content: File content
            file_path: File path

        Returns:
            List of chunks
        """
        paragraphs = content.split("\n\n")
        chunks = []
        current_chunk = []
        current_size = 0
        start_line = 1
        current_line = 1

        for para in paragraphs:
            para_size = len(para) + 2
            para_lines = para.count("\n") + 1

            if current_size + para_size > self.chunk_size:
                if current_chunk:
                    chunks.append({
                        "chunk_index": len(chunks),
                        "content": "\n\n".join(current_chunk),
                        "start_line": start_line,
                        "end_line": current_line - 1,
                        "parent_file": str(file_path),
                    })
                    overlap_paras = current_chunk[-self.chunk_overlap // 200:]
                    current_chunk = overlap_paras + [para]
                    current_size = sum(len(p) + 2 for p in current_chunk)
                    start_line = current_line - len(overlap_paras) * para_lines
                else:
                    current_chunk.append(para)
                    current_size += para_size
            else:
                current_chunk.append(para)
                current_size += para_size

            current_line += para_lines

        if current_chunk:
            chunks.append({
                "chunk_index": len(chunks),
                "content": "\n\n".join(current_chunk),
                "start_line": start_line,
                "end_line": current_line - 1,
                "parent_file": str(file_path),
            })

        logger.debug(
            "Chunked generic file %s into %d chunks",
            file_path,
            len(chunks),
        )
        return chunks

