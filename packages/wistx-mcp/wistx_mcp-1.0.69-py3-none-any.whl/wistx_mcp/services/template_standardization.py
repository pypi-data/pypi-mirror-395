"""Template standardization service for adding template.json to forked repositories."""

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


class TemplateStandardizationService:
    """Service for standardizing forked repositories with template.json."""

    def __init__(self, github_token: str | None = None):
        """Initialize template standardization service.

        Args:
            github_token: GitHub token for API access (optional)
        """
        self.github_token = github_token

    async def add_template_metadata(
        self,
        repo_url: str,
        original_repo: dict[str, Any],
        template_metadata: dict[str, Any] | None = None,
        github_token: str | None = None,
    ) -> dict[str, Any]:
        """Add template.json metadata to repository.

        Args:
            repo_url: GitHub repository URL (fork URL)
            original_repo: Original repository information
            template_metadata: Additional template metadata
            github_token: GitHub token for API access

        Returns:
            Template dictionary with metadata
        """
        structure = await self._extract_repository_structure_from_github(repo_url, github_token)

        metadata = template_metadata or {}
        inferred_metadata = self._infer_template_metadata(original_repo, structure)

        template_data = {
            "metadata": {
                "name": metadata.get("name") or inferred_metadata.get("name", original_repo.get("name", "")),
                "description": metadata.get("description") or original_repo.get("description", ""),
                "version": metadata.get("version", "1.0.0"),
                "project_type": metadata.get("project_type") or inferred_metadata.get("project_type", "unknown"),
                "architecture_type": metadata.get("architecture_type") or inferred_metadata.get("architecture_type"),
                "cloud_provider": metadata.get("cloud_provider") or inferred_metadata.get("cloud_provider"),
                "tags": metadata.get("tags", []) or inferred_metadata.get("tags", []),
                "compliance_standards": metadata.get("compliance_standards", []),
                "source": {
                    "original_repo": original_repo.get("html_url", ""),
                    "original_owner": original_repo.get("owner", {}).get("login", ""),
                    "original_license": original_repo.get("license", {}).get("spdx_id", ""),
                    "attribution": f"Based on work by @{original_repo.get('owner', {}).get('login', '')}",
                    "forked_at": metadata.get("forked_at"),
                },
                "changelog": metadata.get("changelog", [
                    f"Forked from {original_repo.get('html_url', '')}",
                    "Added template.json metadata",
                    "Validated against WISTX standards",
                ]),
            },
            "structure": structure,
        }

        logger.info("Extracted template structure from repository: %s", repo_url)

        return template_data

    async def _extract_repository_structure_from_github(
        self,
        repo_url: str,
        github_token: str | None = None,
    ) -> dict[str, str]:
        """Extract repository structure from GitHub using API.

        Args:
            repo_url: GitHub repository URL
            github_token: GitHub token for API access

        Returns:
            Dictionary mapping file paths to content
        """
        import httpx
        import base64
        from urllib.parse import urlparse

        parsed_url = urlparse(repo_url)
        path_parts = parsed_url.path.strip("/").split("/")
        owner = path_parts[0]
        repo = path_parts[1].replace(".git", "")

        headers = {}
        if github_token:
            headers["Authorization"] = f"token {github_token}"

        structure: dict[str, str] = {}

        async def fetch_tree(sha: str, path: str = "") -> None:
            """Recursively fetch repository tree."""
            url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{sha}?recursive=1"

            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, headers=headers, timeout=30.0)
                    response.raise_for_status()
                    tree_data = response.json()

                    for item in tree_data.get("tree", []):
                        if item["type"] == "blob":
                            file_path = item["path"]
                            if self._should_include_file(file_path):
                                content = await self._fetch_file_content(
                                    owner,
                                    repo,
                                    file_path,
                                    github_token,
                                )
                                if content:
                                    structure[file_path] = content

            except Exception as e:
                logger.warning("Failed to fetch tree for %s: %s", repo_url, e)

        try:
            ref_url = f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/main"
            async with httpx.AsyncClient() as client:
                response = await client.get(ref_url, headers=headers, timeout=30.0)
                if response.status_code == 404:
                    ref_url = f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/master"
                    response = await client.get(ref_url, headers=headers, timeout=30.0)

                response.raise_for_status()
                ref_data = response.json()
                commit_sha = ref_data["object"]["sha"]

            commit_url = f"https://api.github.com/repos/{owner}/{repo}/git/commits/{commit_sha}"
            async with httpx.AsyncClient() as client:
                response = await client.get(commit_url, headers=headers, timeout=30.0)
                response.raise_for_status()
                commit_data = response.json()
                tree_sha = commit_data["tree"]["sha"]

            await fetch_tree(tree_sha)

        except Exception as e:
            logger.error("Failed to extract structure from GitHub: %s", e)

        return structure

    async def _fetch_file_content(
        self,
        owner: str,
        repo: str,
        file_path: str,
        github_token: str | None = None,
    ) -> str | None:
        """Fetch file content from GitHub.

        Args:
            owner: Repository owner
            repo: Repository name
            file_path: File path
            github_token: GitHub token

        Returns:
            File content or None
        """
        import httpx
        import base64

        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

        headers = {}
        if github_token:
            headers["Authorization"] = f"token {github_token}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=30.0)
                response.raise_for_status()
                data = response.json()

                if data.get("encoding") == "base64":
                    content = base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
                    return content
        except Exception as e:
            logger.debug("Failed to fetch file %s: %s", file_path, e)

        return None

    def _should_include_file(self, file_path: str) -> bool:
        """Check if file should be included in template structure.

        Args:
            file_path: File path

        Returns:
            True if file should be included
        """
        skip_extensions = {".pyc", ".pyo", ".DS_Store", ".swp", ".swo"}
        skip_dirs = {".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build", ".idea"}

        if any(file_path.endswith(ext) for ext in skip_extensions):
            return False

        if any(f"/{dir}/" in file_path or file_path.startswith(f"{dir}/") for dir in skip_dirs):
            return False

        if file_path.startswith(".") and file_path not in [".gitignore", ".dockerignore"]:
            return False

        max_size = 100 * 1024
        return True


    async def _extract_repository_structure(
        self,
        repo_path: Path,
        max_depth: int = 10,
    ) -> dict[str, str]:
        """Extract repository structure as dictionary.

        Args:
            repo_path: Path to repository
            max_depth: Maximum directory depth

        Returns:
            Dictionary mapping file paths to content
        """
        structure: dict[str, str] = {}

        skip_dirs = {".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build"}
        skip_files = {".DS_Store", "*.pyc", "*.pyo"}

        def should_skip(path: Path) -> bool:
            parts = path.parts
            return any(part in skip_dirs for part in parts) or any(
                path.name.endswith(ext) for ext in [".pyc", ".pyo", ".DS_Store"]
            )

        for root, dirs, files in os.walk(repo_path):
            root_path = Path(root)

            if should_skip(root_path):
                continue

            depth = len(root_path.relative_to(repo_path).parts)
            if depth > max_depth:
                continue

            rel_root = root_path.relative_to(repo_path)

            for file in files:
                file_path = root_path / file

                if should_skip(file_path):
                    continue

                try:
                    content = file_path.read_text(encoding="utf-8", errors="ignore")
                    rel_path = str(rel_root / file)
                    structure[rel_path] = content
                except Exception as e:
                    logger.debug("Failed to read file %s: %s", file_path, e)

        return structure

    def _infer_template_metadata(
        self,
        repo: dict[str, Any],
        structure: dict[str, str],
    ) -> dict[str, Any]:
        """Infer template metadata from repository and structure.

        Args:
            repo: Repository dictionary
            structure: Repository structure

        Returns:
            Inferred metadata dictionary
        """
        name = repo.get("name", "").lower()
        description = (repo.get("description", "") or "").lower()
        topics = [t.lower() for t in repo.get("topics", [])]

        metadata: dict[str, Any] = {
            "name": repo.get("name", ""),
            "tags": topics[:10],
        }

        if "kubernetes" in name or "k8s" in name or "kubernetes" in topics:
            metadata["project_type"] = "kubernetes"
            if "microservices" in name or "microservices" in topics:
                metadata["architecture_type"] = "microservices"
            elif "serverless" in name or "serverless" in topics:
                metadata["architecture_type"] = "serverless"
        elif "terraform" in name or "terraform" in topics:
            metadata["project_type"] = "terraform"
        elif "devops" in name or "ci-cd" in name or "devops" in topics:
            metadata["project_type"] = "devops"
        elif "platform" in name or "platform" in topics:
            metadata["project_type"] = "platform"

        if "aws" in name or "aws" in topics:
            metadata["cloud_provider"] = "aws"
        elif "gcp" in name or "google" in name or "gcp" in topics:
            metadata["cloud_provider"] = "gcp"
        elif "azure" in name or "azure" in topics:
            metadata["cloud_provider"] = "azure"

        return metadata

