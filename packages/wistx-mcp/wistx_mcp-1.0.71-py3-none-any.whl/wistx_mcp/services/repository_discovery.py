"""Repository discovery service for finding high-quality templates on GitHub."""

import logging
from datetime import datetime, timedelta
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class RepositoryDiscoveryService:
    """Service for discovering high-quality repositories on GitHub."""

    def __init__(self, github_token: str | None = None):
        """Initialize repository discovery service.

        Args:
            github_token: GitHub personal access token (optional, increases rate limits)
        """
        self.github_token = github_token
        self.base_url = "https://api.github.com"

    async def discover_repositories(
        self,
        queries: list[str],
        min_stars: int = 500,
        min_quality_score: float = 70.0,
        max_results: int = 10000,
    ) -> list[dict[str, Any]]:
        """Discover high-quality repositories matching criteria.

        Args:
            queries: List of GitHub search queries
            min_stars: Minimum star count
            min_quality_score: Minimum quality score (0-100)
            max_results: Maximum number of results

        Returns:
            List of repository dictionaries with quality scores
        """
        all_repos: dict[str, dict[str, Any]] = {}

        for query in queries:
            try:
                repos = await self._search_github(query, min_stars)
                for repo in repos:
                    repo_id = repo["id"]
                    if repo_id not in all_repos:
                        quality_score = self._calculate_quality_score(repo)
                        if quality_score >= min_quality_score:
                            repo["quality_score"] = quality_score
                            all_repos[repo_id] = repo
            except Exception as e:
                logger.warning("Failed to search query '%s': %s", query, e)

        repos_list = list(all_repos.values())
        repos_list.sort(key=lambda x: x["quality_score"], reverse=True)

        logger.info(
            "Discovered %d high-quality repositories (min_score=%.1f)",
            len(repos_list),
            min_quality_score,
        )

        return repos_list[:max_results]

    async def _search_github(
        self,
        query: str,
        min_stars: int = 500,
        per_page: int = 100,
    ) -> list[dict[str, Any]]:
        """Search GitHub repositories.

        Args:
            query: GitHub search query
            min_stars: Minimum star count
            per_page: Results per page

        Returns:
            List of repository dictionaries
        """
        url = f"{self.base_url}/search/repositories"
        params = {
            "q": f"{query} stars:>={min_stars}",
            "sort": "stars",
            "order": "desc",
            "per_page": min(per_page, 100),
        }

        headers = {}
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"

        all_repos = []
        page = 1

        while len(all_repos) < 1000:
            params["page"] = page

            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params, headers=headers, timeout=30.0)
                    response.raise_for_status()
                    data = response.json()

                    repos = data.get("items", [])
                    if not repos:
                        break

                    all_repos.extend(repos)

                    if len(repos) < per_page:
                        break

                    page += 1

                    if page > 10:
                        break

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 422:
                    break
                logger.warning("GitHub API error: %s", e.response.status_code)
                break
            except Exception as e:
                logger.warning("Failed to search GitHub: %s", e)
                break

        return all_repos

    def _calculate_quality_score(self, repo: dict[str, Any]) -> float:
        """Calculate quality score for repository.

        Args:
            repo: Repository dictionary from GitHub API

        Returns:
            Quality score (0-100)
        """
        score = 0.0

        stars = repo.get("stargazers_count", 0)
        score += min(stars / 1000 * 30, 30)

        updated_at_str = repo.get("updated_at")
        if updated_at_str:
            try:
                updated_at = datetime.fromisoformat(updated_at_str.replace("Z", "+00:00"))
                days_since_update = (datetime.now(updated_at.tzinfo) - updated_at).days
                if days_since_update <= 30:
                    score += 20
                elif days_since_update <= 90:
                    score += 15
                elif days_since_update <= 180:
                    score += 10
                elif days_since_update <= 365:
                    score += 5
            except Exception:
                pass

        if repo.get("has_wiki") or repo.get("has_pages"):
            score += 15

        license_info = repo.get("license")
        if license_info and license_info.get("key") in ["mit", "apache-2.0", "bsd-3-clause"]:
            score += 10

        if self._has_production_structure(repo):
            score += 15

        open_issues = repo.get("open_issues_count", 0)
        if open_issues < 50:
            score += 10

        language = repo.get("language", "").lower()
        if language in ["yaml", "hcl", "python", "go", "typescript"]:
            score += 5

        return min(score, 100.0)

    def _has_production_structure(self, repo: dict[str, Any]) -> bool:
        """Check if repository has production-ready structure.

        Args:
            repo: Repository dictionary

        Returns:
            True if has production structure indicators
        """
        name_lower = repo.get("name", "").lower()
        description_lower = repo.get("description", "").lower()

        production_indicators = [
            "production",
            "production-ready",
            "best-practices",
            "enterprise",
            "production-grade",
            "battle-tested",
        ]

        return any(indicator in name_lower or indicator in description_lower for indicator in production_indicators)

    async def get_repository_details(self, repo_url: str) -> dict[str, Any]:
        """Get detailed repository information.

        Args:
            repo_url: Repository URL

        Returns:
            Detailed repository dictionary
        """
        owner_repo = repo_url.replace("https://github.com/", "").replace(".git", "")
        owner, repo = owner_repo.split("/", 1)

        url = f"{self.base_url}/repos/{owner}/{repo}"

        headers = {}
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=30.0)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error("Failed to get repository details: %s", e)
            raise

