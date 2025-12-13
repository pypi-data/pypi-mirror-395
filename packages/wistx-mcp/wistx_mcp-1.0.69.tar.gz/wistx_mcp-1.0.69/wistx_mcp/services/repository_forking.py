"""Repository forking service for forking templates to wistx-templates organization."""

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class RepositoryForkingService:
    """Service for forking repositories to GitHub organization."""

    def __init__(self, github_token: str, organization: str = "wistx-templates"):
        """Initialize repository forking service.

        Args:
            github_token: GitHub personal access token (required)
            organization: Target GitHub organization
        """
        if not github_token:
            raise ValueError("GitHub token is required for forking")

        self.github_token = github_token
        self.organization = organization
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

    async def fork_to_organization(
        self,
        repo_url: str,
        new_name: str | None = None,
    ) -> dict[str, Any]:
        """Fork repository to organization.

        Args:
            repo_url: Source repository URL
            new_name: New repository name (optional)

        Returns:
            Dictionary with fork information

        Raises:
            ValueError: If fork fails
        """
        owner_repo = repo_url.replace("https://github.com/", "").replace(".git", "")
        owner, repo = owner_repo.split("/", 1)

        if not new_name:
            new_name = f"{repo}-{owner}"

        url = f"{self.base_url}/repos/{owner}/{repo}/forks"
        payload = {
            "organization": self.organization,
            "name": new_name,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=self.headers, timeout=60.0)
                response.raise_for_status()
                fork_data = response.json()

                logger.info(
                    "Forked repository: %s/%s -> %s/%s",
                    owner,
                    repo,
                    self.organization,
                    new_name,
                )

                return {
                    "fork_url": fork_data["html_url"],
                    "fork_name": new_name,
                    "original_url": repo_url,
                    "original_owner": owner,
                    "original_repo": repo,
                    "organization": self.organization,
                }

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 422:
                existing_fork = await self._check_existing_fork(owner, repo)
                if existing_fork:
                    logger.info("Repository already forked: %s", existing_fork["html_url"])
                    return {
                        "fork_url": existing_fork["html_url"],
                        "fork_name": existing_fork["name"],
                        "original_url": repo_url,
                        "already_exists": True,
                    }
            raise ValueError(f"Failed to fork repository: {e.response.status_code}") from e
        except Exception as e:
            logger.error("Failed to fork repository %s: %s", repo_url, e)
            raise ValueError(f"Failed to fork repository: {e}") from e

    async def _check_existing_fork(self, owner: str, repo: str) -> dict[str, Any] | None:
        """Check if repository already exists in organization.

        Args:
            owner: Original repository owner
            repo: Original repository name

        Returns:
            Fork repository dictionary or None
        """
        url = f"{self.base_url}/repos/{self.organization}/{repo}-{owner}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers, timeout=30.0)
                if response.status_code == 200:
                    return response.json()
        except Exception:
            pass

        return None

    async def list_organization_forks(self) -> list[dict[str, Any]]:
        """List all forks in organization.

        Returns:
            List of repository dictionaries
        """
        url = f"{self.base_url}/orgs/{self.organization}/repos"
        params = {"type": "all", "per_page": 100}

        all_repos = []
        page = 1

        while True:
            params["page"] = page

            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params, headers=self.headers, timeout=30.0)
                    response.raise_for_status()
                    repos = response.json()

                    if not repos:
                        break

                    all_repos.extend(repos)

                    if len(repos) < 100:
                        break

                    page += 1

            except Exception as e:
                logger.error("Failed to list organization repos: %s", e)
                break

        return all_repos

