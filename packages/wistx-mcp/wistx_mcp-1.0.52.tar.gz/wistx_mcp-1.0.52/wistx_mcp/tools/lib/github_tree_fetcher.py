"""GitHub tree fetcher - extract repository structure from GitHub API."""

import asyncio
import base64
import logging
import re
import time
from typing import Any
from urllib.parse import urlparse

import httpx

from wistx_mcp.tools.lib.retry_utils import with_timeout_and_retry

logger = logging.getLogger(__name__)


class GitHubTreeFetcher:
    """Fetcher for GitHub repository tree structure."""

    def __init__(self, github_token: str | None = None):
        """Initialize GitHub tree fetcher.

        Args:
            github_token: GitHub token for authentication
        """
        self.github_token = github_token
        self.headers = {}
        if github_token:
            self.headers["Authorization"] = f"token {github_token}"
        self._last_request_time = 0.0
        self._min_request_interval = 0.1
        self._rate_limit_remaining = None
        self._rate_limit_reset = None

    def _parse_repo_url(self, repo_url: str) -> tuple[str, str]:
        """Parse repository URL to extract owner and repo.

        Args:
            repo_url: Repository URL

        Returns:
            Tuple of (owner, repo)

        Raises:
            ValueError: If URL is invalid
        """
        parsed = urlparse(repo_url)
        path_parts = parsed.path.strip("/").split("/")

        if len(path_parts) >= 2:
            owner = path_parts[0]
            repo = path_parts[1].replace(".git", "")
            return owner, repo
        raise ValueError(f"Invalid repository URL: {repo_url}")

    async def _handle_rate_limit(self, response: httpx.Response) -> None:
        """Handle GitHub API rate limit headers.

        Args:
            response: HTTP response from GitHub API
        """
        if "X-RateLimit-Remaining" in response.headers:
            self._rate_limit_remaining = int(response.headers["X-RateLimit-Remaining"])
        if "X-RateLimit-Reset" in response.headers:
            self._rate_limit_reset = int(response.headers["X-RateLimit-Reset"])

        if response.status_code == 403 and self._rate_limit_remaining == 0:
            reset_time = self._rate_limit_reset or int(time.time()) + 3600
            wait_time = max(0, reset_time - int(time.time()))
            if wait_time > 0:
                logger.warning(
                    "GitHub API rate limit exceeded. Waiting %d seconds until reset.",
                    wait_time,
                )
                await asyncio.sleep(min(wait_time, 3600))

    async def _make_request(self, url: str) -> httpx.Response:
        """Make HTTP request with rate limiting and retry logic.

        Args:
            url: Request URL

        Returns:
            HTTP response

        Raises:
            httpx.HTTPStatusError: If API call fails after retries
        """
        elapsed = time.time() - self._last_request_time
        if elapsed < self._min_request_interval:
            await asyncio.sleep(self._min_request_interval - elapsed)

        async def _request() -> httpx.Response:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers, timeout=30.0)
                self._last_request_time = time.time()
                await self._handle_rate_limit(response)
                return response

        response = await with_timeout_and_retry(
            _request,
            timeout_seconds=30.0,
            max_attempts=3,
            initial_delay=1.0,
            max_delay=10.0,
            retryable_exceptions=(
                httpx.HTTPStatusError,
                httpx.RequestError,
                httpx.TimeoutException,
                ConnectionError,
                TimeoutError,
            ),
        )

        return response

    async def _get_branch_sha(self, owner: str, repo: str, branch: str) -> str:
        """Get branch SHA.

        Args:
            owner: Repository owner
            repo: Repository name
            branch: Branch name

        Returns:
            Branch SHA

        Raises:
            httpx.HTTPStatusError: If API call fails
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/{branch}"

        response = await self._make_request(url)
        if response.status_code == 404:
            master_url = f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/master"
            response = await self._make_request(master_url)
        response.raise_for_status()
        data = response.json()
        return data["object"]["sha"]

    async def _get_tree_recursive(self, owner: str, repo: str, sha: str) -> list[dict[str, Any]]:
        """Get tree recursively.

        Args:
            owner: Repository owner
            repo: Repository name
            sha: Tree SHA

        Returns:
            List of tree items

        Raises:
            httpx.HTTPStatusError: If API call fails
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{sha}?recursive=1"

        response = await self._make_request(url)
        response.raise_for_status()
        data = response.json()
        return data.get("tree", [])

    async def _fetch_file_content(self, owner: str, repo: str, file_path: str) -> str | None:
        """Fetch file content from GitHub API.

        Args:
            owner: Repository owner
            repo: Repository name
            file_path: File path in repository

        Returns:
            File content or None if fetch fails
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

        try:
            response = await self._make_request(url)
            response.raise_for_status()
            data = response.json()

            if data.get("encoding") == "base64":
                content = base64.b64decode(data["content"]).decode("utf-8")
                return content
            return data.get("content", "")
        except Exception as e:
            logger.warning("Failed to fetch file content for %s: %s", file_path, e)
            return None

    def _match_pattern(self, path: str, pattern: str) -> bool:
        """Match path against glob pattern.

        Args:
            path: File path
            pattern: Glob pattern

        Returns:
            True if path matches pattern
        """
        import fnmatch

        return fnmatch.fnmatch(path, pattern)

    def _filter_tree(
        self,
        tree: list[dict[str, Any]],
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        max_depth: int = 10,
    ) -> list[dict[str, Any]]:
        """Filter tree based on patterns and depth.

        Args:
            tree: List of tree items
            include_patterns: Include patterns (glob)
            exclude_patterns: Exclude patterns (glob)
            max_depth: Maximum directory depth

        Returns:
            Filtered tree items
        """
        filtered = []

        for item in tree:
            path = item.get("path", "")

            depth = path.count("/")
            if depth > max_depth:
                continue

            if exclude_patterns:
                if any(self._match_pattern(path, pattern) for pattern in exclude_patterns):
                    continue

            if include_patterns:
                if not any(self._match_pattern(path, pattern) for pattern in include_patterns):
                    continue

            filtered.append(item)

        return filtered

    async def _build_structure(
        self,
        tree: list[dict[str, Any]],
        include_content: bool = False,
        max_file_size: int = 100000,
        owner: str = "",
        repo: str = "",
    ) -> dict[str, Any]:
        """Build nested structure from flat tree.

        Args:
            tree: List of tree items
            include_content: Whether to include file contents
            max_file_size: Maximum file size to include content
            owner: Repository owner (for fetching content)
            repo: Repository name (for fetching content)

        Returns:
            Nested structure dictionary
        """
        structure = {
            "type": "directory",
            "name": "root",
            "path": "",
            "children": [],
        }

        files_to_fetch = []
        for item in tree:
            if item["type"] == "blob":
                path_parts = item["path"].split("/")
                if include_content and item.get("size", 0) <= max_file_size:
                    files_to_fetch.append((structure, path_parts, item, owner, repo))
                else:
                    await self._add_file_to_structure(
                        structure,
                        path_parts,
                        item,
                        include_content=False,
                        max_file_size=max_file_size,
                        owner=owner,
                        repo=repo,
                    )

        if files_to_fetch:
            await self._fetch_files_concurrently(
                files_to_fetch,
                include_content,
                max_file_size,
            )

        return structure

    async def _fetch_files_concurrently(
        self,
        files_to_fetch: list[tuple[dict[str, Any], list[str], dict[str, Any], str, str]],
        include_content: bool,
        max_file_size: int,
    ) -> None:
        """Fetch multiple files concurrently.

        Args:
            files_to_fetch: List of tuples (structure, path_parts, item, owner, repo)
            include_content: Whether to include content
            max_file_size: Maximum file size
        """
        semaphore = asyncio.Semaphore(10)

        async def fetch_and_add(
            structure: dict[str, Any],
            path_parts: list[str],
            item: dict[str, Any],
            owner: str,
            repo: str,
        ) -> None:
            async with semaphore:
                if include_content:
                    content = await self._fetch_file_content(owner, repo, "/".join(path_parts))
                    if content:
                        item["_content"] = content
                await self._add_file_to_structure(
                    structure,
                    path_parts,
                    item,
                    include_content=include_content,
                    max_file_size=max_file_size,
                    owner=owner,
                    repo=repo,
                )

        tasks = [
            fetch_and_add(structure, path_parts, item, owner, repo)
            for structure, path_parts, item, owner, repo in files_to_fetch
        ]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def _add_file_to_structure(
        self,
        structure: dict[str, Any],
        path_parts: list[str],
        item: dict[str, Any],
        include_content: bool = False,
        max_file_size: int = 100000,
        owner: str = "",
        repo: str = "",
    ) -> None:
        """Add file to nested structure.

        Args:
            structure: Current structure node
            path_parts: Path parts
            item: Tree item
            include_content: Whether to include content
            max_file_size: Maximum file size
            owner: Repository owner
            repo: Repository name
        """
        current = structure

        for i, part in enumerate(path_parts[:-1]):
            found = False
            for child in current.get("children", []):
                if child["name"] == part and child["type"] == "directory":
                    current = child
                    found = True
                    break

            if not found:
                new_dir = {
                    "type": "directory",
                    "name": part,
                    "path": "/".join(path_parts[: i + 1]),
                    "children": [],
                }
                current.setdefault("children", []).append(new_dir)
                current = new_dir

        file_node = {
            "type": "file",
            "name": path_parts[-1],
            "path": "/".join(path_parts),
            "size": item.get("size", 0),
        }

        if include_content and item.get("size", 0) <= max_file_size:
            content = item.get("_content")
            if content:
                file_node["content"] = content

        current.setdefault("children", []).append(file_node)

    def _calculate_metadata(self, tree: list[dict[str, Any]]) -> dict[str, Any]:
        """Calculate metadata from tree.

        Args:
            tree: List of tree items

        Returns:
            Metadata dictionary
        """
        files = [item for item in tree if item["type"] == "blob"]
        directories = [item for item in tree if item["type"] == "tree"]

        total_size = sum(item.get("size", 0) for item in files)

        languages = set()
        for item in files:
            path = item.get("path", "")
            if "." in path:
                ext = path.split(".")[-1].lower()
                if ext:
                    languages.add(ext)

        return {
            "total_files": len(files),
            "total_directories": len(directories),
            "total_size": total_size,
            "languages": sorted(list(languages)),
        }

    async def fetch_tree(
        self,
        repo_url: str,
        branch: str = "main",
        include_content: bool = False,
        max_file_size: int = 100000,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        max_depth: int = 10,
    ) -> dict[str, Any]:
        """Fetch repository tree structure.

        Args:
            repo_url: Repository URL
            branch: Branch name
            include_content: Include file contents
            max_file_size: Max file size for content
            include_patterns: Include patterns
            exclude_patterns: Exclude patterns
            max_depth: Max depth

        Returns:
            Tree structure dictionary
        """
        owner, repo = self._parse_repo_url(repo_url)

        branch_sha = await self._get_branch_sha(owner, repo, branch)

        tree_data = await self._get_tree_recursive(owner, repo, branch_sha)

        filtered_tree = self._filter_tree(
            tree_data,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
            max_depth=max_depth,
        )

        structure = await self._build_structure(
            filtered_tree,
            include_content=include_content,
            max_file_size=max_file_size,
            owner=owner,
            repo=repo,
        )

        metadata = self._calculate_metadata(filtered_tree)
        metadata["repo_url"] = repo_url
        metadata["branch"] = branch

        return {
            "structure": structure,
            "metadata": metadata,
        }

    def format_as_tree(self, tree_data: dict[str, Any]) -> str:
        """Format tree as text tree structure.

        Args:
            tree_data: Tree data dictionary

        Returns:
            Formatted tree string
        """
        structure = tree_data.get("structure", {})
        return self._format_node(structure, prefix="", is_last=True)

    def _format_node(self, node: dict[str, Any], prefix: str, is_last: bool) -> str:
        """Format node recursively.

        Args:
            node: Node dictionary
            prefix: Prefix string
            is_last: Whether this is the last child

        Returns:
            Formatted string
        """
        lines = []

        connector = "└── " if is_last else "├── "
        lines.append(f"{prefix}{connector}{node['name']}")

        children = node.get("children", [])
        for i, child in enumerate(children):
            is_child_last = i == len(children) - 1
            child_prefix = prefix + ("    " if is_last else "│   ")
            child_lines = self._format_node(child, child_prefix, is_child_last).split("\n")
            lines.extend(child_lines)

        return "\n".join(lines)

    def format_as_markdown(self, tree_data: dict[str, Any]) -> str:
        """Format tree as markdown.

        Args:
            tree_data: Tree data dictionary

        Returns:
            Markdown string
        """
        structure = tree_data.get("structure", {})
        metadata = tree_data.get("metadata", {})

        markdown = f"# Repository Structure\n\n"
        markdown += f"**Repository**: {metadata.get('repo_url', '')}\n\n"
        markdown += f"**Branch**: {metadata.get('branch', 'main')}\n\n"
        markdown += f"**Files**: {metadata.get('total_files', 0)}\n\n"
        markdown += f"**Directories**: {metadata.get('total_directories', 0)}\n\n"
        markdown += f"**Total Size**: {metadata.get('total_size', 0)} bytes\n\n"

        if metadata.get("languages"):
            markdown += f"**Languages**: {', '.join(metadata['languages'][:10])}\n\n"

        markdown += "## Structure\n\n"
        markdown += "```\n"
        markdown += self.format_as_tree(tree_data)
        markdown += "\n```\n"

        return markdown

