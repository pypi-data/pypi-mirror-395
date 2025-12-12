"""GitHub integration service for repository indexing."""

import asyncio
import fnmatch
import logging
import tempfile
from pathlib import Path
from typing import Any, Callable, Optional

from urllib.parse import urlparse

from github import Github
from github.GithubException import GithubException
from git import Repo
from git.exc import GitCommandError
from pinecone import Pinecone

from bson import ObjectId

from api.database.mongodb import mongodb_manager
from api.config import settings
from api.models.indexing import ResourceStatus
from data_pipelines.models.knowledge_article import ContentType, Domain, KnowledgeArticle
from data_pipelines.processors.embedding_generator import EmbeddingGenerator
from wistx_mcp.tools.lib.retry_utils import with_timeout_and_retry
from api.exceptions import ValidationError, AuthenticationError, ExternalServiceError

logger = logging.getLogger(__name__)


class GitHubService:
    """Service for GitHub repository indexing."""

    def __init__(self):
        """Initialize GitHub service."""
        self.embedding_generator = EmbeddingGenerator()
        self._pinecone_client: Optional[Pinecone] = None
        self._pinecone_index: Optional[Any] = None

    async def get_repository_info(
        self,
        repo_url: str,
        github_token: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get repository information including visibility and metadata.

        Args:
            repo_url: GitHub repository URL
            github_token: Optional token (uses internal token for public repos if None)

        Returns:
            Dictionary with repository information:
            {
                "owner": str,
                "name": str,
                "is_private": bool,
                "default_branch": str,
                "clone_url": str,
                "description": Optional[str],
                "stars": int,
                "forks": int,
            }

        Raises:
            ValueError: If repository URL is invalid
            GithubException: If GitHub API fails
        """
        repo_info = self._parse_repo_url(repo_url)
        if not repo_info:
            raise ValueError(f"Invalid repository URL: {repo_url}")

        token = github_token or settings.github_internal_token
        github_client = self._get_github_client(token)

        async def get_repo():
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None,
                github_client.get_repo,
                f"{repo_info['owner']}/{repo_info['name']}",
            )

        try:
            repo = await with_timeout_and_retry(
                get_repo,
                timeout_seconds=10.0,
                max_attempts=3,
                retryable_exceptions=(RuntimeError, ConnectionError, TimeoutError),
            )

            return {
                "owner": repo_info["owner"],
                "name": repo_info["name"],
                "is_private": repo.private,
                "default_branch": repo.default_branch,
                "clone_url": repo.clone_url,
                "description": repo.description,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "full_name": repo.full_name,
            }
        except GithubException as e:
            logger.error(
                "Failed to get repository info for %s/%s: %s (status: %s)",
                repo_info["owner"],
                repo_info["name"],
                e,
                e.status if hasattr(e, "status") else "unknown",
            )
            raise

    async def validate_repository_access(
        self,
        repo_url: str,
        github_token: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Validate access to repository with smart token selection.

        Uses internal token for public repositories and provided token for private repositories.
        This method intelligently selects the appropriate token based on repository visibility.

        Args:
            repo_url: GitHub repository URL
            github_token: Optional user-provided token (for backward compatibility)
            user_id: User ID (for future OAuth token lookup)

        Returns:
            Dictionary with validation results:
            {
                "accessible": bool,
                "is_private": bool,
                "requires_oauth": bool,  # True if private repo needs OAuth
                "token_source": str,  # "internal", "provided", or None
                "error": Optional[str],  # Error message if not accessible
            }
        """
        try:
            repo_info = await self.get_repository_info(repo_url, github_token)
            is_private = repo_info["is_private"]

            if not is_private:
                logger.info(
                    "Public repository detected: %s/%s - using internal token",
                    repo_info["owner"],
                    repo_info["name"],
                )
                return {
                    "accessible": True,
                    "is_private": False,
                    "requires_oauth": False,
                    "token_source": "internal",
                    "repository_info": repo_info,
                }

            logger.info(
                "Private repository detected: %s/%s - checking access",
                repo_info["owner"],
                repo_info["name"],
            )

            if github_token:
                logger.info("Using provided token for private repository")
                return {
                    "accessible": True,
                    "is_private": True,
                    "requires_oauth": False,
                    "token_source": "provided",
                    "repository_info": repo_info,
                }

            if user_id:
                logger.debug("Checking for OAuth token for user: %s", user_id)
                oauth_token = await self._get_user_oauth_token(user_id)
                if oauth_token:
                    try:
                        test_info = await self.get_repository_info(repo_url, oauth_token)
                        logger.info("OAuth token validated successfully for private repository")
                        return {
                            "accessible": True,
                            "is_private": True,
                            "requires_oauth": False,
                            "token_source": "oauth",
                            "repository_info": test_info,
                        }
                    except GithubException:
                        logger.warning("OAuth token validation failed for user: %s", user_id)

            logger.warning(
                "Private repository %s/%s requires authentication but no valid token provided",
                repo_info["owner"],
                repo_info["name"],
            )
            return {
                "accessible": False,
                "is_private": True,
                "requires_oauth": True,
                "token_source": None,
                "error": "Private repository requires GitHub OAuth authorization",
                "repository_info": repo_info,
            }

        except ValueError as e:
            logger.error("Invalid repository URL: %s", repo_url)
            return {
                "accessible": False,
                "is_private": False,
                "requires_oauth": False,
                "token_source": None,
                "error": str(e),
            }
        except GithubException as e:
            status_code = getattr(e, "status", None)
            if status_code == 404:
                logger.warning("Repository not found: %s", repo_url)
                return {
                    "accessible": False,
                    "is_private": False,
                    "requires_oauth": False,
                    "token_source": None,
                    "error": "Repository not found or access denied",
                }
            elif status_code == 403:
                logger.warning("Access denied to repository: %s", repo_url)
                return {
                    "accessible": False,
                    "is_private": True,
                    "requires_oauth": True,
                    "token_source": None,
                    "error": "Access denied. Private repository requires authentication",
                }
            else:
                logger.error("GitHub API error validating repository access: %s", e)
                return {
                    "accessible": False,
                    "is_private": False,
                    "requires_oauth": False,
                    "token_source": None,
                    "error": f"GitHub API error: {str(e)}",
                }
        except (RuntimeError, ConnectionError, TimeoutError) as e:
            logger.error("Network error validating repository access: %s", e, exc_info=True)
            return {
                "accessible": False,
                "is_private": False,
                "requires_oauth": False,
                "token_source": None,
                "error": "Network error connecting to GitHub",
            }
        except Exception as e:
            logger.error("Unexpected error validating repository access: %s", e, exc_info=True)
            return {
                "accessible": False,
                "is_private": False,
                "requires_oauth": False,
                "token_source": None,
                "error": "Unexpected error validating repository access",
            }

    async def _get_user_oauth_token(self, user_id: str) -> Optional[str]:
        """Get user's GitHub OAuth token.

        Args:
            user_id: User ID

        Returns:
            Decrypted OAuth token or None
        """
        try:
            from api.services.oauth_service import oauth_service
            return await oauth_service.get_github_token(user_id)
        except ImportError:
            logger.debug("OAuth service not available (Phase 2 not implemented)")
            return None
        except Exception as e:
            logger.warning("Error getting OAuth token for user %s: %s", user_id, e)
            return None

    async def list_user_repositories(
        self,
        user_id: str,
        include_private: bool = True,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """List user's GitHub repositories.

        Uses the user's OAuth token to fetch their repositories from GitHub API.
        This allows users to discover and select repositories to index.

        Args:
            user_id: User ID
            include_private: Include private repositories
            limit: Maximum number of repositories to return

        Returns:
            List of repository dictionaries with metadata

        Raises:
            ValueError: If user doesn't have GitHub OAuth token
            GithubException: If GitHub API fails
        """
        oauth_token = await self._get_user_oauth_token(user_id)
        if not oauth_token:
            raise AuthenticationError(
                message="GitHub OAuth token not found",
                user_message="GitHub OAuth token not found. Please connect your GitHub account in settings.",
                error_code="GITHUB_TOKEN_NOT_FOUND",
                details={"user_id": user_id}
            )

        github_client = self._get_github_client(oauth_token)

        async def get_user_repos():
            loop = asyncio.get_event_loop()
            user = await loop.run_in_executor(None, github_client.get_user)

            repos = []
            repo_type = "all" if include_private else "public"

            def fetch_repos():
                repo_list = []
                try:
                    repos_iter = user.get_repos(
                        type=repo_type,
                        sort="updated",
                        direction="desc",
                    )
                    count = 0
                    for repo in repos_iter:
                        if count >= limit:
                            break
                        repo_list.append(repo)
                        count += 1
                except Exception as e:
                    logger.warning("Error fetching repositories: %s", e)
                    raise
                return repo_list

            user_repos = await loop.run_in_executor(None, fetch_repos)

            for repo in user_repos:
                repo_data = {
                    "id": repo.id,
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "private": repo.private,
                    "html_url": repo.html_url,
                    "description": repo.description,
                    "default_branch": repo.default_branch,
                    "stars": repo.stargazers_count,
                    "forks": repo.forks_count,
                    "updated_at": repo.updated_at.isoformat() if repo.updated_at else None,
                    "language": repo.language,
                    "topics": [],
                }

                repos.append(repo_data)

            return repos

        try:
            repos = await with_timeout_and_retry(
                get_user_repos,
                timeout_seconds=60.0,
                max_attempts=2,
                retryable_exceptions=(RuntimeError, ConnectionError, TimeoutError),
            )

            logger.info(
                "Retrieved %d repositories for user %s (private: %s)",
                len(repos),
                user_id,
                include_private,
            )

            return repos

        except RuntimeError as e:
            if "timed out" in str(e).lower():
                logger.error("GitHub API timeout listing repositories for user %s: %s", user_id, e)
                raise ExternalServiceError(
                    message="Request timed out while fetching repositories",
                    user_message="Request timed out while fetching repositories. Please try again.",
                    error_code="GITHUB_API_TIMEOUT",
                    details={"user_id": user_id}
                ) from e
            raise ExternalServiceError(
                message=f"Failed to retrieve repositories: {str(e)}",
                user_message="Failed to retrieve repositories from GitHub. Please try again later.",
                error_code="GITHUB_API_ERROR",
                details={"user_id": user_id, "error": str(e)}
            ) from e
        except GithubException as e:
            logger.error("GitHub API error listing repositories for user %s: %s", user_id, e)
            raise ExternalServiceError(
                message=f"Failed to retrieve repositories: {str(e)}",
                user_message="Failed to retrieve repositories from GitHub. Please try again later.",
                error_code="GITHUB_API_ERROR",
                details={"user_id": user_id, "error": str(e)}
            ) from e
        except Exception as e:
            logger.error("Unexpected error listing repositories for user %s: %s", user_id, e, exc_info=True)
            raise ExternalServiceError(
                message=f"Failed to retrieve repositories: {str(e)}",
                user_message="An unexpected error occurred. Please try again later.",
                error_code="GITHUB_SERVICE_ERROR",
                details={"user_id": user_id, "error": str(e)}
            ) from e

    async def list_user_organizations(
        self,
        user_id: str,
    ) -> list[dict[str, Any]]:
        """List user's GitHub organizations.

        Uses the user's OAuth token to fetch their organizations from GitHub API.

        Args:
            user_id: User ID

        Returns:
            List of organization dictionaries with metadata

        Raises:
            ValueError: If user doesn't have GitHub OAuth token
            GithubException: If GitHub API fails
        """
        oauth_token = await self._get_user_oauth_token(user_id)
        if not oauth_token:
            raise AuthenticationError(
                message="GitHub OAuth token not found",
                user_message="GitHub OAuth token not found. Please connect your GitHub account in settings.",
                error_code="GITHUB_TOKEN_NOT_FOUND",
                details={"user_id": user_id}
            )

        github_client = self._get_github_client(oauth_token)

        async def get_user_orgs():
            loop = asyncio.get_event_loop()
            user = await loop.run_in_executor(None, github_client.get_user)

            def fetch_orgs():
                org_list = []
                try:
                    orgs_iter = user.get_orgs()
                    for org in orgs_iter:
                        org_list.append(org)
                except Exception as e:
                    logger.warning("Error fetching organizations: %s", e)
                    raise
                return org_list

            user_orgs = await loop.run_in_executor(None, fetch_orgs)

            organizations = []
            for org in user_orgs:
                org_data = {
                    "login": org.login,
                    "name": org.name or org.login,
                    "avatar_url": org.avatar_url,
                    "description": org.description,
                    "role": getattr(org, "role", None) or "member",
                    "selected": False,
                }
                organizations.append(org_data)

            return organizations

        try:
            organizations = await with_timeout_and_retry(
                get_user_orgs,
                timeout_seconds=10.0,
                max_attempts=3,
                retryable_exceptions=(RuntimeError, ConnectionError, TimeoutError),
            )

            from api.services.oauth_service import oauth_service
            selected_orgs = await oauth_service.get_selected_organizations(user_id)

            for org in organizations:
                org["selected"] = org["login"] in selected_orgs

            await oauth_service.update_github_organizations(user_id, organizations)

            return organizations

        except GithubException as e:
            logger.error("GitHub API error listing organizations: %s", e, exc_info=True)
            raise
        except Exception as e:
            logger.error("Unexpected error listing organizations: %s", e, exc_info=True)
            raise

    async def list_organization_repositories(
        self,
        user_id: str,
        org_login: str,
        include_private: bool = True,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """List repositories for a specific GitHub organization.

        Args:
            user_id: User ID
            org_login: Organization login name
            include_private: Include private repositories
            limit: Maximum number of repositories to return

        Returns:
            List of repository dictionaries with metadata

        Raises:
            ValueError: If user doesn't have GitHub OAuth token or org access
            GithubException: If GitHub API fails
        """
        oauth_token = await self._get_user_oauth_token(user_id)
        if not oauth_token:
            raise AuthenticationError(
                message="GitHub OAuth token not found",
                user_message="GitHub OAuth token not found. Please connect your GitHub account in settings.",
                error_code="GITHUB_TOKEN_NOT_FOUND",
                details={"user_id": user_id}
            )

        github_client = self._get_github_client(oauth_token)

        async def get_org_repos():
            loop = asyncio.get_event_loop()

            def fetch_org_repos():
                repo_list = []
                try:
                    org = github_client.get_organization(org_login)
                    repo_type = "all" if include_private else "public"
                    repos_iter = org.get_repos(
                        type=repo_type,
                        sort="updated",
                        direction="desc",
                    )
                    count = 0
                    for repo in repos_iter:
                        if count >= limit:
                            break
                        repo_list.append(repo)
                        count += 1
                except Exception as e:
                    logger.warning("Error fetching organization repositories: %s", e)
                    raise
                return repo_list

            org_repos = await loop.run_in_executor(None, fetch_org_repos)

            repos = []
            for repo in org_repos:
                repo_data = {
                    "id": repo.id,
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "private": repo.private,
                    "html_url": repo.html_url,
                    "description": repo.description,
                    "default_branch": repo.default_branch,
                    "stars": repo.stargazers_count,
                    "forks": repo.forks_count,
                    "updated_at": repo.updated_at.isoformat() if repo.updated_at else None,
                    "language": repo.language,
                    "organization": org_login,
                }
                repos.append(repo_data)

            return repos

        try:
            repos = await with_timeout_and_retry(
                get_org_repos,
                timeout_seconds=10.0,
                max_attempts=3,
                retryable_exceptions=(RuntimeError, ConnectionError, TimeoutError),
            )

            return repos

        except GithubException as e:
            logger.error(
                "GitHub API error listing organization repositories: %s",
                e,
                exc_info=True,
            )
            raise
        except Exception as e:
            logger.error(
                "Unexpected error listing organization repositories: %s",
                e,
                exc_info=True,
            )
            raise

    async def index_repository(
        self,
        resource_id: str,
        repo_url: str,
        branch: str,
        user_id: str,
        github_token: Optional[str] = None,
        include_patterns: Optional[list[str]] = None,
        exclude_patterns: Optional[list[str]] = None,
        compliance_standards: Optional[list[str]] = None,
        environment_name: Optional[str] = None,
        progress_callback: Optional[Callable[[float], None]] = None,
        activity_callback: Optional[Callable[[str, str, Optional[str], Optional[dict]], None]] = None,
    ) -> None:
        """Index a GitHub repository with smart token selection.

        Token Selection Logic:
        1. Get repository info to determine visibility (public/private)
        2. If public: Use internal token (no user token needed)
        3. If private: Use provided token or OAuth token (if available)

        Args:
            resource_id: Resource ID
            repo_url: GitHub repository URL
            branch: Branch name
            user_id: User ID
            github_token: Optional GitHub token (for backward compatibility with private repos)
            include_patterns: File path patterns to include (glob patterns)
            exclude_patterns: File path patterns to exclude (glob patterns)
            progress_callback: Callback for progress updates (0-100)
            activity_callback: Callback for activity logging (activity_type, message, file_path, details)

        Raises:
            ValueError: If repository URL is invalid or access denied
            GithubException: If GitHub API fails
        """
        repo_info_data = await self.get_repository_info(repo_url, github_token)
        is_private = repo_info_data["is_private"]

        token_to_use = None
        token_source = "none"

        if is_private:
            if github_token:
                token_to_use = github_token
                token_source = "provided"
                logger.info("Using provided token for private repository indexing")
            else:
                oauth_token = await self._get_user_oauth_token(user_id)
                if oauth_token:
                    token_to_use = oauth_token
                    token_source = "oauth"
                    logger.info("Using OAuth token for private repository indexing")
                else:
                    raise ValueError(
                        "Private repository requires GitHub authentication. "
                        "Please provide a GitHub token or authorize GitHub OAuth access."
                    )
        else:
            token_to_use = settings.github_internal_token
            token_source = "internal"
            logger.info(
                "Using internal token for public repository indexing: %s/%s",
                repo_info_data["owner"],
                repo_info_data["name"],
            )

        if not token_to_use:
            raise ValueError(
                "No GitHub token available. "
                "Internal token must be configured for public repositories."
            )

        repo_info = self._parse_repo_url(repo_url)
        if not repo_info:
            raise ValueError(f"Invalid repository URL: {repo_url}")

        github_client = self._get_github_client(token_to_use)
        
        async def get_repo():
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None,
                github_client.get_repo,
                f"{repo_info['owner']}/{repo_info['name']}",
            )
        
        repo = await with_timeout_and_retry(
            get_repo,
            timeout_seconds=10.0,
            max_attempts=3,
            retryable_exceptions=(RuntimeError, ConnectionError, TimeoutError),
        )

        if progress_callback:
            await progress_callback(20.0)

        with tempfile.TemporaryDirectory() as temp_dir:
            clone_url = repo.clone_url
            
            if token_to_use and token_source != "internal":
                parsed = urlparse(clone_url)
                clone_url = f"{parsed.scheme}://{token_to_use}@{parsed.netloc}{parsed.path}"
                logger.debug("Using authenticated clone URL for private repository")
            else:
                logger.debug("Using public clone URL (no authentication needed)")

            default_branch = repo.default_branch
            branch_to_use = branch or default_branch
            
            logger.info(
                "Cloning repository: %s (requested branch: %s, default branch: %s, visibility: %s, token_source: %s)",
                repo_url,
                branch or "not specified",
                default_branch,
                "private" if is_private else "public",
                token_source,
            )

            async def clone_repo(branch_name: str):
                loop = asyncio.get_event_loop()
                repo_path = Path(temp_dir) / repo.name
                return await loop.run_in_executor(
                    None,
                    lambda b=branch_name: Repo.clone_from(clone_url, str(repo_path), branch=b, depth=1),
                )
            
            repo_path = Path(temp_dir) / repo.name
            cloned_repo = None
            last_error = None
            
            branches_to_try = [branch_to_use]
            if default_branch not in branches_to_try:
                branches_to_try.append(default_branch)
            if "main" not in branches_to_try:
                branches_to_try.append("main")
            if "master" not in branches_to_try:
                branches_to_try.append("master")
            
            for attempt_branch in branches_to_try:
                try:
                    cloned_repo = await with_timeout_and_retry(
                        lambda b=attempt_branch: clone_repo(b),
                        timeout_seconds=60.0,
                        max_attempts=2,
                        retryable_exceptions=(RuntimeError, ConnectionError, TimeoutError),
                    )
                    if cloned_repo:
                        if attempt_branch != branch_to_use:
                            logger.info(
                                "Successfully cloned fallback branch '%s' (requested: '%s')",
                                attempt_branch,
                                branch or "not specified",
                            )
                        else:
                            logger.info("Successfully cloned branch: %s", attempt_branch)
                        break
                except (GitCommandError, Exception) as e:
                    last_error = e
                    error_msg = str(e).lower()
                    is_branch_not_found = (
                        isinstance(e, GitCommandError) and
                        ("remote branch" in error_msg and "not found" in error_msg)
                    ) or (
                        "remote branch" in error_msg and "not found" in error_msg
                    )
                    
                    if is_branch_not_found:
                        logger.warning(
                            "Branch '%s' not found, trying next branch...",
                            attempt_branch,
                        )
                        if attempt_branch == branches_to_try[-1]:
                            logger.error(
                                "Failed to clone repository: no valid branch found after trying: %s",
                                branches_to_try,
                            )
                            raise RuntimeError(
                                f"Repository has no valid branch. Tried: {branches_to_try}. "
                                f"Default branch is: {default_branch}"
                            ) from e
                        continue
                    elif attempt_branch == branches_to_try[-1]:
                        logger.error(
                            "Failed to clone repository after trying all branches: %s",
                            branches_to_try,
                        )
                        raise
                    else:
                        logger.warning(
                            "Failed to clone branch '%s': %s. Trying next branch...",
                            attempt_branch,
                            str(e)[:200],
                        )
                        continue
            
            if cloned_repo is None:
                if last_error:
                    raise RuntimeError(
                        f"Failed to clone repository: tried branches {branches_to_try}. "
                        f"Last error: {last_error}"
                    ) from last_error
                else:
                    raise RuntimeError(
                        f"Failed to clone repository: no valid branch found. "
                        f"Tried: {branches_to_try}"
                    )
            
            commit_sha = cloned_repo.head.commit.hexsha
            logger.info("Cloned repository at commit: %s", commit_sha[:8])

            # Log activity: repo cloned
            if activity_callback:
                await activity_callback(
                    "repo_cloned",
                    f"Successfully cloned repository at commit {commit_sha[:8]}",
                    None,
                    {"commit_sha": commit_sha, "branch": branch_to_use},
                )

            if progress_callback:
                await progress_callback(40.0)

            from api.services.indexing_service import indexing_service

            existing_resource = await indexing_service.get_resource(resource_id, user_id)
            if existing_resource and existing_resource.status == ResourceStatus.COMPLETED:
                last_commit = getattr(existing_resource, "last_commit_sha", None)
                if last_commit == commit_sha:
                    logger.info(
                        "Repository unchanged since last index (commit: %s), skipping re-index",
                        commit_sha[:8],
                    )
                    if progress_callback:
                        await progress_callback(100.0)
                    return

            supported_extensions = {
                ".py",
                ".ts",
                ".js",
                ".tsx",
                ".jsx",
                ".tf",
                ".hcl",
                ".tfvars",
                ".yaml",
                ".yml",
                ".json",
                ".md",
                ".rst",
                ".txt",
                ".sh",
                ".bash",
                ".zsh",
                ".toml",
            }

            supported_filenames = {
                "Dockerfile",
                "docker-compose.yml",
                "docker-compose.yaml",
                ".gitlab-ci.yml",
                "Jenkinsfile",
                "Makefile",
                "Vagrantfile",
                "Pulumi.yaml",
                "Pulumi.yml",
                "serverless.yml",
                "serverless.yaml",
                "template.yaml",
                "template.yml",
                "sam.yaml",
                "sam.yml",
                ".dockerignore",
                ".gitignore",
            }

            files = self._get_code_files(
                repo_path,
                supported_extensions,
                supported_filenames,
                include_patterns=include_patterns,
                exclude_patterns=exclude_patterns,
            )
            total_files = len(files)

            # Log activity: files discovered
            if activity_callback:
                await activity_callback(
                    "files_discovered",
                    f"Discovered {total_files} files to process",
                    None,
                    {"total_files": total_files},
                )

            if progress_callback:
                await progress_callback(45.0)

            articles_created, files_processed, total_size_mb, failed_files = await self._process_files_parallel(
                files=files,
                repo_path=repo_path,
                repo_url=repo_url,
                branch=branch,
                commit_sha=commit_sha,
                user_id=user_id,
                resource_id=resource_id,
                compliance_standards=compliance_standards,
                environment_name=environment_name,
                progress_callback=progress_callback,
                activity_callback=activity_callback,
            )

            if progress_callback:
                await progress_callback(95.0)

            # Log activity: analysis completed
            if activity_callback:
                await activity_callback(
                    "analysis_completed",
                    f"Completed analysis: {files_processed} files processed, {articles_created} articles created",
                    None,
                    {
                        "files_processed": files_processed,
                        "articles_created": articles_created,
                        "total_size_mb": total_size_mb,
                        "failed_count": len(failed_files) if failed_files else 0,
                    },
                )

            db = mongodb_manager.get_database()
            collection = db.indexed_resources

            update_data = {
                "articles_indexed": articles_created,
                "files_processed": files_processed,
                "total_files": total_files,
                "storage_mb": total_size_mb,
            }

            if failed_files:
                update_data["error_details"] = {
                    "failed_files": failed_files,
                    "failed_count": len(failed_files),
                }

            update_data["last_commit_sha"] = commit_sha

            collection.update_one(
                {"_id": resource_id},
                {"$set": update_data},
            )

            if progress_callback:
                await progress_callback(100.0)

            logger.info(
                "Indexed repository: %s - %d files, %d articles, %.2f MB",
                repo_url,
                files_processed,
                articles_created,
                total_size_mb,
            )

    def _parse_repo_url(self, repo_url: str) -> Optional[dict[str, str]]:
        """Parse GitHub repository URL.

        Args:
            repo_url: Repository URL

        Returns:
            Dictionary with owner and name, or None if invalid
        """
        try:
            parsed = urlparse(repo_url)
            path_parts = parsed.path.strip("/").split("/")

            if len(path_parts) >= 2:
                return {
                    "owner": path_parts[0],
                    "name": path_parts[1].replace(".git", ""),
                }

            return None
        except Exception as e:
            logger.error("Error parsing repo URL: %s", e)
            return None

    def _get_github_client(self, github_token: Optional[str] = None) -> Github:
        """Get GitHub API client.

        Args:
            github_token: GitHub token (optional)

        Returns:
            Github client instance
        """
        if github_token:
            return Github(github_token)
        return Github()

    def _get_code_files(
        self,
        repo_path: Path,
        extensions: set[str],
        filenames: set[str],
        include_patterns: Optional[list[str]] = None,
        exclude_patterns: Optional[list[str]] = None,
    ) -> list[Path]:
        """Get code files from repository with DevOps-focused filtering.

        Args:
            repo_path: Repository root path
            extensions: Set of file extensions to include
            filenames: Set of filenames to include (without extension)
            include_patterns: File path patterns to include (glob patterns)
            exclude_patterns: File path patterns to exclude (glob patterns)

        Returns:
            List of file paths that should be indexed
        """
        files = []
        ignore_dirs = {".git", "__pycache__", "node_modules", ".venv", "venv", ".env"}

        default_include_paths = [
            "infra/",
            "infrastructure/",
            "terraform/",
            "terragrunt/",
            "opentofu/",
            "pulumi/",
            "cdk/",
            "cloudformation/",
            "cfn/",
            "serverless/",
            "k8s/",
            "kubernetes/",
            "helm/",
            "charts/",
            "argocd/",
            "argo/",
            "flux/",
            "crossplane/",
            "docker/",
            "ci/",
            "cd/",
            "pipelines/",
            "scripts/",
            "ansible/",
            "puppet/",
            "chef/",
            "bicep/",
            ".github/workflows/",
            ".gitlab/",
            "docs/",
            "documentation/",
        ]

        default_exclude_paths = [
            "src/",
            "app/",
            "lib/",
            "components/",
            "pages/",
            "dist/",
            "build/",
            "target/",
        ]

        for file_path in repo_path.rglob("*"):
            if not file_path.is_file():
                continue

            relative = file_path.relative_to(repo_path)
            path_str = str(relative).replace("\\", "/")

            if any(part in ignore_dirs for part in relative.parts):
                continue

            file_name = file_path.name
            file_extension = file_path.suffix.lower()

            if file_extension not in extensions and file_name not in filenames:
                continue

            if not self._should_index_file(
                path_str,
                file_path,
                include_patterns=include_patterns,
                exclude_patterns=exclude_patterns,
                default_include_paths=default_include_paths,
                default_exclude_paths=default_exclude_paths,
            ):
                continue

            files.append(file_path)

        logger.info(
            "Found %d files to index (from %s)",
            len(files),
            repo_path,
        )
        return files

    def _should_index_file(
        self,
        path_str: str,
        file_path: Path,
        include_patterns: Optional[list[str]] = None,
        exclude_patterns: Optional[list[str]] = None,
        default_include_paths: Optional[list[str]] = None,
        default_exclude_paths: Optional[list[str]] = None,
    ) -> bool:
        """Determine if file should be indexed based on patterns and content.

        Args:
            path_str: Relative file path as string
            file_path: Full file path
            include_patterns: User-specified include patterns (highest priority)
            exclude_patterns: User-specified exclude patterns (highest priority)
            default_include_paths: Default DevOps paths to include
            default_exclude_paths: Default application paths to exclude

        Returns:
            True if file should be indexed, False otherwise
        """
        path_lower = path_str.lower()

        if include_patterns:
            if not any(fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(path_lower, pattern.lower()) for pattern in include_patterns):
                return False

        if exclude_patterns:
            if any(fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(path_lower, pattern.lower()) for pattern in exclude_patterns):
                return False

        if default_exclude_paths:
            if any(path_lower.startswith(exclude_path.lower()) for exclude_path in default_exclude_paths):
                return False

        if default_include_paths:
            if any(path_lower.startswith(include_path.lower()) for include_path in default_include_paths):
                return True

        if file_path.name in ["README.md", "README.txt", "README.rst"]:
            return True

        if file_path.suffix.lower() in [".tf", ".hcl", ".tfvars", ".yaml", ".yml", ".bicep", ".json"]:
            return True

        if file_path.name in [
            "Dockerfile",
            "docker-compose.yml",
            "docker-compose.yaml",
            ".gitlab-ci.yml",
            "Jenkinsfile",
            "Pulumi.yaml",
            "Pulumi.yml",
            "serverless.yml",
            "serverless.yaml",
            "template.yaml",
            "template.yml",
            "sam.yaml",
            "sam.yml",
        ]:
            return True

        try:
            content_preview = file_path.read_text(encoding="utf-8", errors="ignore")[:5000]
            if self._is_devops_content(content_preview):
                return True
        except Exception:
            pass

        return False

    def _is_devops_content(self, content: str) -> bool:
        """Detect if file content is DevOps-related.

        Args:
            content: File content preview (first 5000 chars)

        Returns:
            True if content appears to be DevOps-related
        """
        content_lower = content.lower()

        terraform_keywords = ["resource ", "provider ", "module ", "terraform ", "variable ", "output "]
        if any(keyword in content_lower for keyword in terraform_keywords):
            return True

        kubernetes_keywords = ["apiVersion:", "kind:", "metadata:", "spec:", "kubectl", "namespace:"]
        if any(keyword in content_lower for keyword in kubernetes_keywords):
            return True

        docker_keywords = ["FROM ", "RUN ", "CMD ", "ENTRYPOINT ", "EXPOSE ", "ENV ", "WORKDIR "]
        if any(keyword in content_lower for keyword in docker_keywords):
            return True

        cicd_keywords = ["workflow:", "pipeline:", "stage:", "job:", "steps:", "actions:", "on:"]
        if any(keyword in content_lower for keyword in cicd_keywords):
            return True

        ansible_keywords = ["- hosts:", "tasks:", "playbook", "ansible", "become:"]
        if any(keyword in content_lower for keyword in ansible_keywords):
            return True

        pulumi_keywords = [
            "new pulumi",
            "pulumi.",
            "pulumi.Config",
            "pulumi.export",
            "pulumi.getStack",
            "pulumi.getProject",
            "pulumi.StackReference",
            "Pulumi.yaml",
        ]
        if any(keyword in content_lower for keyword in pulumi_keywords):
            return True

        cloudformation_keywords = [
            "AWSTemplateFormatVersion",
            "Resources:",
            "AWS::",
            "CloudFormation",
            "Transform: AWS::Serverless",
        ]
        if any(keyword in content_lower for keyword in cloudformation_keywords):
            return True

        serverless_keywords = [
            "service:",
            "provider:",
            "functions:",
            "serverless.yml",
            "serverless.yaml",
            "serverless framework",
        ]
        if any(keyword in content_lower for keyword in serverless_keywords):
            return True

        cdk_keywords = [
            "from aws_cdk",
            "from constructs",
            "@aws-cdk/",
            "new Stack",
            "CfnOutput",
            "cdk.json",
        ]
        if any(keyword in content_lower for keyword in cdk_keywords):
            return True

        bicep_keywords = [
            "@description",
            "resource ",
            "module ",
            "param ",
            "var ",
            "output ",
        ]
        if any(keyword in content_lower for keyword in bicep_keywords):
            return True

        argocd_keywords = [
            "apiVersion: argoproj.io",
            "kind: Application",
            "kind: AppProject",
            "argocd",
        ]
        if any(keyword in content_lower for keyword in argocd_keywords):
            return True

        flux_keywords = [
            "apiVersion: kustomize.toolkit.fluxcd.io",
            "kind: Kustomization",
            "kind: GitRepository",
            "fluxcd",
        ]
        if any(keyword in content_lower for keyword in flux_keywords):
            return True

        crossplane_keywords = [
            "apiVersion: crossplane.io",
            "kind: CompositeResourceDefinition",
            "kind: Composition",
            "crossplane",
        ]
        if any(keyword in content_lower for keyword in crossplane_keywords):
            return True

        return False

    async def _process_files_parallel(
        self,
        files: list[Path],
        repo_path: Path,
        repo_url: str,
        branch: str,
        commit_sha: str,
        user_id: str,
        resource_id: str,
        compliance_standards: Optional[list[str]] = None,
        environment_name: Optional[str] = None,
        progress_callback: Optional[Callable[[float], None]] = None,
        activity_callback: Optional[Callable[[str, str, Optional[str], Optional[dict]], None]] = None,
    ) -> tuple[int, int, float, list[dict[str, Any]]]:
        """Process files in parallel batches with checkpoint-based resume capability.

        Args:
            files: List of file paths to process
            repo_path: Repository root path
            repo_url: Repository URL
            branch: Branch name
            commit_sha: Commit SHA
            user_id: User ID
            resource_id: Resource ID
            compliance_standards: Optional compliance standards
            environment_name: Optional environment name
            progress_callback: Progress callback
            activity_callback: Activity logging callback

        Returns:
            Tuple of (articles_created, files_processed, total_size_mb, failed_files)
        """
        from api.services.indexing_service import indexing_service
        import hashlib

        processed_files = await indexing_service._get_processed_files(resource_id, commit_sha)
        processed_paths = {
            f["file_path"]: f
            for f in processed_files
            if f.get("status") == "completed" and f.get("commit_sha") == commit_sha
        }

        files_to_process = []
        skipped_count = 0

        for file_path in files:
            relative_path = str(file_path.relative_to(repo_path))

            if relative_path in processed_paths:
                existing = processed_paths[relative_path]
                try:
                    file_content = file_path.read_text(encoding="utf-8", errors="ignore")
                    current_hash = hashlib.sha256(file_content.encode()).hexdigest()

                    if existing.get("file_hash") == current_hash:
                        skipped_count += 1
                        logger.debug("Skipping unchanged file: %s", relative_path)
                        continue
                except Exception as e:
                    logger.warning("Error checking file hash for %s: %s", relative_path, e)

            files_to_process.append(file_path)

        if not files_to_process:
            logger.info(
                "All files already processed for resource %s (commit: %s)",
                resource_id,
                commit_sha[:8],
            )
            return indexing_service._aggregate_processed_stats(processed_files)

        logger.info(
            "Processing %d files (%d already processed, %d skipped)",
            len(files_to_process),
            len(processed_paths),
            skipped_count,
        )

        batch_size = 20
        semaphore = asyncio.Semaphore(batch_size)
        checkpoint_interval = 50

        async def process_file_with_semaphore(file_path: Path) -> dict[str, Any]:
            async with semaphore:
                return await self._process_single_file(
                    file_path,
                    repo_path,
                    repo_url,
                    branch,
                    commit_sha,
                    user_id,
                    resource_id,
                    compliance_standards,
                    environment_name,
                )

        tasks = [process_file_with_semaphore(fp) for fp in files_to_process]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_articles = []
        files_processed = 0
        total_size_mb = 0.0
        failed_files = []

        for i, result in enumerate(results):
            file_path = files_to_process[i]
            relative_path = str(file_path.relative_to(repo_path))
            current_progress = 45.0 + ((i + 1) / len(files_to_process) * 45)

            if isinstance(result, Exception):
                logger.warning("Error processing file %s: %s", relative_path, result)
                failed_files.append({
                    "file": relative_path,
                    "error": str(result),
                })

                # Log activity: file failed
                if activity_callback:
                    await activity_callback(
                        "file_failed",
                        f"Failed to process: {str(result)[:100]}",
                        relative_path,
                        {
                            "error": str(result),
                            "file_index": i + 1,
                            "total_files": len(files_to_process),
                        },
                    )

                try:
                    file_content = file_path.read_text(encoding="utf-8", errors="ignore")
                    file_hash = hashlib.sha256(file_content.encode()).hexdigest()
                    await indexing_service._save_file_checkpoint(
                        resource_id=resource_id,
                        file_path=relative_path,
                        commit_sha=commit_sha,
                        file_hash=file_hash,
                        status="failed",
                        error=str(result),
                    )
                except Exception as e:
                    logger.warning("Error saving failed checkpoint: %s", e)

            elif isinstance(result, dict):
                articles = result.get("articles", [])
                file_size_mb = result.get("file_size_mb", 0.0)

                if articles:
                    all_articles.extend(articles)
                    files_processed += 1
                    total_size_mb += file_size_mb

                    # Log activity: file processed with articles
                    if activity_callback:
                        await activity_callback(
                            "file_processed",
                            f"Processed: {len(articles)} component{'s' if len(articles) != 1 else ''} extracted",
                            relative_path,
                            {
                                "articles_created": len(articles),
                                "file_size_mb": round(file_size_mb, 3),
                                "file_index": i + 1,
                                "total_files": len(files_to_process),
                                "progress": round(current_progress, 1),
                            },
                        )
                else:
                    # Log activity: file skipped (no extractable components)
                    if activity_callback:
                        await activity_callback(
                            "file_skipped",
                            "Skipped: no extractable components",
                            relative_path,
                            {
                                "reason": "no_components",
                                "file_index": i + 1,
                                "total_files": len(files_to_process),
                            },
                        )

                try:
                    file_content = file_path.read_text(encoding="utf-8", errors="ignore")
                    file_hash = hashlib.sha256(file_content.encode()).hexdigest()
                    await indexing_service._save_file_checkpoint(
                        resource_id=resource_id,
                        file_path=relative_path,
                        commit_sha=commit_sha,
                        file_hash=file_hash,
                        articles_created=len(articles),
                        file_size_mb=file_size_mb,
                        status="completed",
                    )

                    from api.services.filesystem_integration import create_filesystem_entry_for_file

                    db = mongodb_manager.get_database()
                    resource_collection = db.indexed_resources
                    resource_doc = resource_collection.find_one({"_id": resource_id})
                    if resource_doc:
                        organization_id = str(resource_doc.get("organization_id")) if resource_doc.get("organization_id") else None
                        compliance_standards = resource_doc.get("compliance_standards")
                        environment_name = resource_doc.get("environment_name")

                        await create_filesystem_entry_for_file(
                            resource_id=resource_id,
                            user_id=user_id,
                            file_path=file_path,
                            relative_path=relative_path,
                            file_content=file_content,
                            articles=articles,
                            organization_id=organization_id,
                            compliance_standards=compliance_standards,
                            environment_name=environment_name,
                        )
                except Exception as e:
                    logger.warning("Error saving checkpoint or creating filesystem entry: %s", e)

            if (i + 1) % checkpoint_interval == 0:
                progress = 45.0 + ((i + 1) / len(files_to_process) * 45)
                if progress_callback:
                    await progress_callback(min(progress, 90.0))

                # Log activity: checkpoint saved
                if activity_callback:
                    await activity_callback(
                        "checkpoint_saved",
                        f"Checkpoint: {i + 1}/{len(files_to_process)} files processed ({files_processed} successful)",
                        None,
                        {
                            "processed": i + 1,
                            "total": len(files_to_process),
                            "successful": files_processed,
                            "articles_so_far": len(all_articles),
                        },
                    )

                logger.info(
                    "Checkpoint saved: %d/%d files processed",
                    i + 1,
                    len(files_to_process),
                )

        if all_articles:
            await self._generate_and_store_articles_batch(all_articles)

            logger.info(
                "Generated %d analysis articles from %d files",
                len(all_articles),
                files_processed,
            )

        return len(all_articles), files_processed, total_size_mb, failed_files

    async def _process_single_file(
        self,
        file_path: Path,
        repo_path: Path,
        repo_url: str,
        branch: str,
        commit_sha: str,
        user_id: str,
        resource_id: str,
        compliance_standards: Optional[list[str]] = None,
        environment_name: Optional[str] = None,
    ) -> dict[str, Any]:
        """Process a single file and create analysis articles (component-level).

        Args:
            file_path: Absolute file path
            repo_path: Repository root path
            repo_url: Repository URL
            branch: Branch name
            commit_sha: Commit SHA
            user_id: User ID
            resource_id: Resource ID
            compliance_standards: Optional compliance standards to check

        Returns:
            Dictionary with articles, file_size_mb
        """
        try:
            from api.services.code_analyzer import code_analyzer

            relative_path = file_path.relative_to(repo_path)
            file_content = file_path.read_text(encoding="utf-8", errors="ignore")
            file_size_mb = len(file_content.encode("utf-8")) / (1024 * 1024)

            should_reanalyze, _file_hash = await code_analyzer.should_reanalyze_file(
                file_path=relative_path,
                file_content=file_content,
                resource_id=resource_id,
            )

            if not should_reanalyze:
                logger.debug("File unchanged, skipping re-analysis: %s (hash: %s)", relative_path, _file_hash[:8])
                return {
                    "articles": [],
                    "file_size_mb": file_size_mb,
                }

            repo_context = {
                "repo_url": repo_url,
                "branch": branch,
                "commit_sha": commit_sha,
                "resource_id": resource_id,
                "user_id": user_id,
                "compliance_standards": compliance_standards,
                "environment_name": environment_name,
                "repo_path": str(repo_path),
            }

            # Use holistic analysis for infrastructure files (Terraform, Docker, etc.)
            if code_analyzer.is_infrastructure_file(relative_path):
                logger.info(
                    "Using holistic analysis for infrastructure file: %s",
                    relative_path,
                )
                try:
                    article = await code_analyzer.analyze_infrastructure_file(
                        file_path=relative_path,
                        file_content=file_content,
                        repo_context=repo_context,
                    )
                    return {
                        "articles": [article],
                        "file_size_mb": file_size_mb,
                    }
                except Exception as e:
                    logger.warning(
                        "Holistic analysis failed for %s, falling back to component analysis: %s",
                        relative_path,
                        e,
                        exc_info=True,
                    )
                    # Fall through to component-level analysis

            # Component-level analysis for non-infrastructure files or as fallback
            components = await code_analyzer.extract_components_from_file(
                file_path=relative_path,
                file_content=file_content,
            )

            if not components:
                logger.debug("No components extracted from file: %s", relative_path)
                return {
                    "articles": [],
                    "file_size_mb": file_size_mb,
                }

            articles = []
            for component_info in components:
                try:
                    article = await code_analyzer.analyze_component(
                        file_path=relative_path,
                        file_content=file_content,
                        component_info=component_info,
                        repo_context=repo_context,
                    )
                    articles.append(article)
                except Exception as e:
                    logger.warning(
                        "Error analyzing component %s in file %s: %s",
                        component_info.get("name"),
                        relative_path,
                        e,
                        exc_info=True,
                    )
                    continue

            return {
                "articles": articles,
                "file_size_mb": file_size_mb,
            }

        except Exception as e:
            logger.warning("Error processing file %s: %s", file_path, e, exc_info=True)
            raise

    def _detect_domain(self, file_path: Path, content: str) -> Domain:
        """Detect domain from file path and content.

        Args:
            file_path: File path
            content: File content

        Returns:
            Domain enum
        """
        path_str = str(file_path).lower()

        if "terraform" in path_str or file_path.suffix == ".tf":
            return Domain.INFRASTRUCTURE
        if "kubernetes" in path_str or "k8s" in path_str:
            return Domain.DEVOPS
        if "security" in path_str or "auth" in path_str:
            return Domain.SECURITY
        if "cost" in path_str or "billing" in path_str:
            return Domain.FINOPS

        content_lower = content.lower()
        if "compliance" in content_lower or "pci" in content_lower or "hipaa" in content_lower:
            return Domain.COMPLIANCE

        return Domain.DEVOPS

    def _detect_content_type(self, file_path: Path) -> ContentType:
        """Detect content type from file path.

        Args:
            file_path: File path

        Returns:
            ContentType enum
        """
        if file_path.suffix == ".md" or file_path.suffix == ".rst":
            return ContentType.GUIDE
        if file_path.suffix == ".tf":
            return ContentType.REFERENCE
        return ContentType.REFERENCE

    def _extract_summary(self, content: str, extension: str = "") -> str:
        """Extract summary from file content.

        Args:
            content: File content
            extension: File extension (kept for API compatibility, not used in extraction)

        Returns:
            Summary string
        """
        _ = extension
        lines = content.split("\n")[:20]
        summary = "\n".join(lines)

        if len(summary) > 500:
            summary = summary[:500] + "..."

        return summary or "Code file from repository"

    async def _generate_and_store_articles_batch(
        self,
        articles: list[KnowledgeArticle],
    ) -> None:
        """Generate embeddings in batch and store articles.

        Args:
            articles: List of KnowledgeArticle objects (without embeddings)
        """
        if not articles:
            return

        texts_to_embed = [article.to_searchable_text() for article in articles]

        embedding_batch_size = 100
        articles_with_embeddings = []

        for i in range(0, len(texts_to_embed), embedding_batch_size):
            batch_texts = texts_to_embed[i:i + embedding_batch_size]
            batch_articles = articles[i:i + embedding_batch_size]

            try:
                embeddings = await self.embedding_generator.generate_embeddings_batch(batch_texts)

                for article, embedding in zip(batch_articles, embeddings):
                    article.embedding = embedding
                    articles_with_embeddings.append(article)

            except Exception as e:
                logger.error("Error generating batch embeddings: %s", e, exc_info=True)
                for article in batch_articles:
                    try:
                        embeddings_single = await self.embedding_generator.generate_embeddings_batch([article.to_searchable_text()])
                        if embeddings_single:
                            article.embedding = embeddings_single[0]
                            articles_with_embeddings.append(article)
                    except Exception as e2:
                        logger.warning("Failed to generate embedding for article %s: %s", article.article_id, e2)

        if articles_with_embeddings:
            await self._store_articles_batch(articles_with_embeddings)

    async def _store_articles_batch(self, articles: list[KnowledgeArticle]) -> None:
        """Store articles in batch (MongoDB + Pinecone).

        Args:
            articles: List of KnowledgeArticle objects with embeddings
        """
        if not articles:
            return

        db = mongodb_manager.get_database()
        mongo_collection = db.knowledge_articles

        pinecone_index = self._get_pinecone_index()

        mongo_operations = []
        pinecone_vectors = []

        for article in articles:
            article_dict = article.model_dump()
            article_dict["_id"] = article.article_id
            if article.user_id:
                article_dict["user_id"] = ObjectId(article.user_id)
            if article.organization_id:
                article_dict["organization_id"] = ObjectId(article.organization_id)

            mongo_operations.append(article_dict)

            if article.embedding:
                metadata = {
                    "article_id": article.article_id,
                    "domain": article.domain.value,
                    "subdomain": article.subdomain,
                    "content_type": article.content_type.value,
                    "title": article.title,
                    "source_url": article.source_url,
                    "visibility": article.visibility,
                    "source_type": article.source_type,
                }

                if article.user_id:
                    metadata["user_id"] = article.user_id
                if article.organization_id:
                    metadata["organization_id"] = article.organization_id
                if article.resource_id:
                    metadata["resource_id"] = article.resource_id

                pinecone_vectors.append({
                    "id": article.article_id,
                    "values": article.embedding,
                    "metadata": metadata,
                })

        if mongo_operations:
            for op in mongo_operations:
                mongo_collection.replace_one(
                    {"_id": op["_id"]},
                    op,
                    upsert=True,
                )

        if pinecone_vectors:
            pinecone_batch_size = 100
            for i in range(0, len(pinecone_vectors), pinecone_batch_size):
                batch = pinecone_vectors[i:i + pinecone_batch_size]
                try:
                    pinecone_index.upsert(vectors=batch)
                except Exception as e:
                    logger.error("Error upserting Pinecone batch: %s", e, exc_info=True)

    async def _store_article(self, article: KnowledgeArticle) -> None:
        """Store a single article (MongoDB + Pinecone).

        Generates embeddings if not present, then stores the article.

        Args:
            article: KnowledgeArticle object to store
        """
        if not article.embedding:
            await self._generate_and_store_articles_batch([article])
        else:
            await self._store_articles_batch([article])

    def _get_pinecone_index(self):
        """Get Pinecone index instance (singleton).

        Returns:
            Pinecone index instance
        """
        if self._pinecone_index is None:
            if self._pinecone_client is None:
                self._pinecone_client = Pinecone(api_key=settings.pinecone_api_key)
            self._pinecone_index = self._pinecone_client.Index(settings.pinecone_index_name)
        return self._pinecone_index


github_service = GitHubService()

