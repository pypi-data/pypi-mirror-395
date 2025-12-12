"""GitHub code examples collector.

Collects infrastructure code examples from GitHub repositories for all DevOps/Cloud tools.
"""

import asyncio
import base64
import logging
import re
import time
from pathlib import Path
from typing import Any, AsyncIterator

import httpx
from github import Github
from github.GithubException import GithubException, RateLimitExceededException

from data_pipelines.collectors.base_collector_universal import BaseCollector
from data_pipelines.collectors.collection_result import CollectionResult
from data_pipelines.collectors.validation_models import RawCodeExample
from wistx_mcp.tools.lib.retry_utils import with_timeout_and_retry
from data_pipelines.processors.parsers.automation import BashParser, PowerShellParser
from data_pipelines.processors.parsers.cd import ArgoCDParser, FluxParser, SpinnakerParser
from data_pipelines.processors.parsers.cicd import (
    ArgoWorkflowsParser,
    CircleCIParser,
    GitHubActionsParser,
    GitLabCIParser,
    JenkinsParser,
    TektonParser,
)
from data_pipelines.processors.parsers.container import DockerParser, HelmParser, KubernetesParser
from data_pipelines.processors.parsers.iac import (
    AnsibleParser,
    ARMParser,
    BicepParser,
    CDK8sParser,
    CDKParser,
    CloudFormationParser,
    OpenTofuParser,
    PulumiParser,
    TerraformParser,
)
from data_pipelines.processors.parsers.monitoring import (
    DatadogParser,
    GrafanaParser,
    OpenTelemetryParser,
    PrometheusParser,
)
from data_pipelines.processors.parsers.platform import BackstageParser, CrossplaneParser, KarpenterParser
from data_pipelines.processors.parsers.serverless import SAMParser, ServerlessParser
from data_pipelines.utils.config import PipelineSettings

logger = logging.getLogger(__name__)
settings = PipelineSettings()


INFRASTRUCTURE_DIRS = [
    "infra", "infrastructure", "terraform", "terragrunt", "opentofu",
    "pulumi", "cdk", "cloudformation", "cfn", "bicep", "arm",
    "k8s", "kubernetes", "helm", "charts", "argocd", "argo",
    "flux", "crossplane", "karpenter", "docker", "ci", "cd",
    "pipelines", ".github/workflows", ".gitlab", ".circleci",
    "monitoring", "prometheus", "grafana", "datadog", "opentelemetry",
    "scripts", "ansible", "puppet", "chef", "backstage",
]

EXCLUDE_DIRS = [
    "node_modules", ".git", "__pycache__", ".venv", "venv",
    "dist", "build", "target", ".idea", ".vscode", "vendor",
    "test", "tests", "spec", "docs", "documentation",
]

MAX_FILE_SIZE = 500000


class GitHubCodeExamplesCollector(BaseCollector):
    """Collect code examples from GitHub for all DevOps/Cloud tools."""

    def __init__(
        self,
        github_token: str | None = None,
        min_stars: int = 200,
        max_repos_per_query: int = 1667,
        max_files_per_repo: int = 999999,
        max_depth: int = 5,
        **kwargs,
    ):
        """Initialize GitHub code examples collector.

        Args:
            github_token: GitHub API token (optional, increases rate limit)
            min_stars: Minimum stars for repositories
            max_repos_per_query: Maximum repositories to process per search query
            max_files_per_repo: Maximum files to process per repository
            max_depth: Maximum directory depth for recursive traversal
            **kwargs: Additional arguments for BaseCollector
        """
        super().__init__(
            collector_name="github-code-examples",
            version="1.0",
            data_type="code",
            rate_limit=(30, 60) if github_token else (10, 60),
            **kwargs,
        )
        self.github_token = github_token or getattr(settings, "github_internal_token", None)
        self.min_stars = min_stars
        self.max_repos_per_query = max_repos_per_query
        self.max_files_per_repo = max_files_per_repo
        self.max_depth = max_depth
        self.enable_structure_extraction = getattr(settings, "github_enable_structure_extraction", True)
        self.enable_quality_evaluation = getattr(settings, "github_enable_quality_evaluation", True)
        self.max_concurrent_repos = getattr(settings, "github_max_concurrent_repos", 5)
        
        self.parsers = {
            "terraform": TerraformParser(),
            "opentofu": OpenTofuParser(),
            "pulumi": PulumiParser(),
            "ansible": AnsibleParser(),
            "cloudformation": CloudFormationParser(),
            "bicep": BicepParser(),
            "arm": ARMParser(),
            "cdk": CDKParser(),
            "cdk8s": CDK8sParser(),
            "github_actions": GitHubActionsParser(),
            "gitlab_ci": GitLabCIParser(),
            "jenkins": JenkinsParser(),
            "circleci": CircleCIParser(),
            "argo_workflows": ArgoWorkflowsParser(),
            "tekton": TektonParser(),
            "argocd": ArgoCDParser(),
            "flux": FluxParser(),
            "spinnaker": SpinnakerParser(),
            "kubernetes": KubernetesParser(),
            "docker": DockerParser(),
            "helm": HelmParser(),
            "prometheus": PrometheusParser(),
            "grafana": GrafanaParser(),
            "datadog": DatadogParser(),
            "opentelemetry": OpenTelemetryParser(),
            "crossplane": CrossplaneParser(),
            "karpenter": KarpenterParser(),
            "backstage": BackstageParser(),
            "sam": SAMParser(),
            "serverless": ServerlessParser(),
            "bash": BashParser(),
            "powershell": PowerShellParser(),
        }
        
        self._github_client: Github | None = None
        self._httpx_client: httpx.AsyncClient | None = None

    def _get_httpx_client(self) -> httpx.AsyncClient:
        """Get or create httpx async client."""
        if self._httpx_client is None:
            headers = {}
            if self.github_token:
                headers["Authorization"] = f"token {self.github_token}"
            self._httpx_client = httpx.AsyncClient(
                headers=headers,
                timeout=httpx.Timeout(30.0, connect=10.0),
                limits=httpx.Limits(max_keepalive_connections=20, max_connections=100),
            )
        return self._httpx_client

    async def _wait_for_rate_limit_reset(self, response: httpx.Response) -> None:
        """Wait for GitHub API rate limit to reset.
        
        Args:
            response: HTTP response with rate limit headers
        """
        reset_timestamp = response.headers.get("X-RateLimit-Reset")
        if reset_timestamp:
            try:
                reset_time = int(reset_timestamp)
                current_time = int(time.time())
                wait_seconds = max(0, reset_time - current_time)
                if wait_seconds > 0:
                    logger.warning(
                        "GitHub rate limit exhausted. Waiting %d seconds until reset...",
                        wait_seconds,
                    )
                    await asyncio.sleep(wait_seconds + 1)
            except (ValueError, TypeError) as e:
                logger.debug("Failed to parse rate limit reset time: %s", e)
                await asyncio.sleep(60)


    def _get_github_client(self) -> Github:
        """Get or create GitHub client."""
        if self._github_client is None:
            if self.github_token:
                self._github_client = Github(self.github_token)
            else:
                self._github_client = Github()
        return self._github_client

    async def _search_github_async(self, query: str, max_examples: int | None = None) -> list[dict[str, Any]]:
        """Search GitHub repositories using async HTTP client.
        
        Args:
            query: GitHub search query
            max_examples: Maximum examples needed (used to calculate per_page)
            
        Returns:
            List of repository data dictionaries
        """
        url = "https://api.github.com/search/repositories"
        
        if max_examples:
            estimated_files_per_repo = min(self.max_files_per_repo, 20)
            repos_needed = max(10, (max_examples // estimated_files_per_repo) + 2)
            per_page = min(30, repos_needed)
        else:
            per_page = min(30, self.max_repos_per_query or 30)
        
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": per_page,
        }
        
        async def _search() -> list[dict[str, Any]]:
            client = self._get_httpx_client()
            response = await client.get(url, params=params)
            
            if response.status_code == 403:
                error_msg = response.text
                if "rate limit" in error_msg.lower():
                    await self._wait_for_rate_limit_reset(response)
                    return await _search()
            
            response.raise_for_status()
            
            rate_limit_remaining = response.headers.get("X-RateLimit-Remaining")
            if rate_limit_remaining and int(rate_limit_remaining) < 10:
                logger.warning("GitHub rate limit low: %s remaining", rate_limit_remaining)
            
            data = response.json()
            return data.get("items", [])
        
        try:
            repos_data = await with_timeout_and_retry(
                _search,
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
            return repos_data
        except Exception as e:
            logger.error("Failed to search GitHub for query %s: %s", query, e)
            return []

    def get_source_urls(self) -> list[str]:
        """Get GitHub search queries for all DevOps/Cloud tools.
        
        Returns:
            List of GitHub search query strings
        """
        queries = []
        
        queries.extend([
            f"terraform aws stars:>={self.min_stars} language:hcl",
            f"terraform gcp modules stars:>={self.min_stars}",
            f"terraform azure stars:>={self.min_stars}",
            f"terraform modules stars:>={self.min_stars}",
            f"terraform examples stars:>={self.min_stars}",
            f"pulumi aws stars:>={self.min_stars}",
            f"pulumi kubernetes stars:>={self.min_stars}",
            f"pulumi azure stars:>={self.min_stars}",
            f"pulumi gcp stars:>={self.min_stars}",
            f"ansible aws stars:>={self.min_stars} language:yaml",
            f"ansible playbook stars:>={self.min_stars}",
            f"cloudformation template stars:>={self.min_stars} language:yaml",
            f"cloudformation stack stars:>={self.min_stars}",
            f"aws-cdk typescript stars:>={self.min_stars}",
            f"aws-cdk python stars:>={self.min_stars}",
            f"aws-cdk java stars:>={self.min_stars}",
            f"aws-cdk go stars:>={self.min_stars}",
            f"bicep azure stars:>={self.min_stars}",
            f"arm template azure stars:>={self.min_stars}",
            f"kubernetes yaml stars:>={self.min_stars} language:yaml",
            f"kubernetes manifests stars:>={self.min_stars}",
            f"helm chart stars:>={self.min_stars}",
            f"helm values stars:>={self.min_stars}",
            f"dockerfile production stars:>={self.min_stars}",
            f"docker compose stars:>={self.min_stars}",
            f"github actions workflow stars:>={self.min_stars} path:.github/workflows",
            f"github actions ci cd stars:>={self.min_stars}",
            f"gitlab ci yaml stars:>={self.min_stars}",
            f"gitlab pipeline stars:>={self.min_stars}",
            f"jenkins pipeline groovy stars:>={self.min_stars}",
            f"jenkinsfile stars:>={self.min_stars}",
            f"circleci config stars:>={self.min_stars} path:.circleci",
            f"circleci pipeline stars:>={self.min_stars}",
            f"argo workflows yaml stars:>={self.min_stars}",
            f"argo cd application stars:>={self.min_stars}",
            f"tekton pipeline stars:>={self.min_stars}",
            f"tekton task stars:>={self.min_stars}",
            f"argocd application stars:>={self.min_stars}",
            f"argocd app stars:>={self.min_stars}",
            f"flux kustomization stars:>={self.min_stars}",
            f"flux helmrelease stars:>={self.min_stars}",
            f"spinnaker pipeline stars:>={self.min_stars}",
            f"spinnaker config stars:>={self.min_stars}",
            f"prometheus config stars:>={self.min_stars}",
            f"prometheus rules stars:>={self.min_stars}",
            f"grafana dashboard stars:>={self.min_stars}",
            f"grafana provisioning stars:>={self.min_stars}",
            f"datadog monitor stars:>={self.min_stars}",
            f"datadog dashboard stars:>={self.min_stars}",
            f"opentelemetry collector stars:>={self.min_stars}",
            f"opentelemetry config stars:>={self.min_stars}",
            f"crossplane composition stars:>={self.min_stars}",
            f"crossplane provider stars:>={self.min_stars}",
            f"karpenter nodepool stars:>={self.min_stars}",
            f"karpenter provisioner stars:>={self.min_stars}",
            f"backstage component stars:>={self.min_stars}",
            f"backstage catalog stars:>={self.min_stars}",
            f"sam template stars:>={self.min_stars}",
            f"sam yaml stars:>={self.min_stars}",
            f"serverless framework stars:>={self.min_stars}",
            f"serverless yml stars:>={self.min_stars}",
        ])
        
        return queries

    def _detect_code_type(self, file_path: str, file_content: str) -> str | None:
        """Detect DevOps/Cloud tool type from file path and content.
        
        Uses all registered parsers to detect code type.
        
        Args:
            file_path: File path
            file_content: File content (first 2000 chars for better detection)
            
        Returns:
            Code type or None
        """
        path_lower = file_path.lower()
        content_preview = file_content[:2000]
        content_lower = content_preview.lower()
        
        detection_order = [
            ("github_actions", lambda: ".github/workflows/" in path_lower and any(ext in path_lower for ext in [".yml", ".yaml"]) and any(p in content_lower for p in ["name:", "on:", "jobs:"])),
            ("gitlab_ci", lambda: "gitlab-ci" in path_lower and any(p in content_lower for p in ["stages:", "image:", "script:"])),
            ("jenkins", lambda: "jenkinsfile" in path_lower and any(p in content_lower for p in ["pipeline", "agent", "stages"])),
            ("circleci", lambda: ".circleci/config" in path_lower and any(p in content_lower for p in ["version:", "jobs:", "workflows:"])),
            ("docker", lambda: ("dockerfile" in path_lower or "docker-compose" in path_lower) and any(p in content_lower for p in ["FROM", "RUN", "COPY"])),
            ("terraform", lambda: any(path_lower.endswith(ext) for ext in [".tf", ".tfvars", ".hcl"]) and any(p in content_lower for p in ["provider", "resource", "data", "module"])),
            ("opentofu", lambda: any(path_lower.endswith(ext) for ext in [".tf", ".tfvars", ".hcl"]) and ("opentofu" in content_lower or "tofu" in content_lower)),
            ("pulumi", lambda: ("pulumi" in content_lower or "@pulumi" in content_lower) and any(p in content_lower for p in ["pulumi.aws", "pulumi.gcp", "pulumi.azure"])),
            ("ansible", lambda: any(path_lower.endswith(ext) for ext in [".yml", ".yaml"]) and any(p in content_lower for p in ["hosts:", "tasks:", "ansible.builtin"])),
            ("cloudformation", lambda: any(path_lower.endswith(ext) for ext in [".yaml", ".yml", ".json"]) and ("AWSTemplateFormatVersion" in content_preview or "Type: AWS::" in content_preview)),
            ("bicep", lambda: path_lower.endswith(".bicep") and any(p in content_lower for p in ["@description", "resource", "module"])),
            ("arm", lambda: path_lower.endswith(".json") and ("$schema" in content_preview and "contentVersion" in content_preview)),
            ("cdk", lambda: ("aws-cdk" in content_lower or "aws_cdk" in content_lower) and any(p in content_lower for p in ["cdk.Stack", "cdk.Construct"])),
            ("cdk8s", lambda: ("cdk8s" in content_lower or "cdk8s" in content_lower) and ("k8s." in content_lower or "import * as k8s" in content_preview)),
            ("kubernetes", lambda: any(path_lower.endswith(ext) for ext in [".yaml", ".yml"]) and any(p in content_preview for p in ["apiVersion:", "kind:", "metadata:"])),
            ("helm", lambda: ("Chart.yaml" in path_lower or "values.yaml" in path_lower) and ("apiVersion: v2" in content_preview or "name:" in content_preview)),
            ("prometheus", lambda: any(path_lower.endswith(ext) for ext in [".yml", ".yaml"]) and any(p in content_lower for p in ["scrape_configs:", "job_name:", "targets:"])),
            ("grafana", lambda: any(path_lower.endswith(ext) for ext in [".json", ".yaml", ".yml"]) and any(p in content_lower for p in ["dashboard", "panels", "targets"])),
            ("datadog", lambda: any(path_lower.endswith(ext) for ext in [".yaml", ".yml", ".json"]) and any(p in content_lower for p in ["init_config:", "instances:", "logs:"])),
            ("opentelemetry", lambda: any(path_lower.endswith(ext) for ext in [".yaml", ".yml", ".json"]) and any(p in content_lower for p in ["receivers:", "processors:", "exporters:", "service:"])),
            ("argocd", lambda: any(path_lower.endswith(ext) for ext in [".yaml", ".yml"]) and "apiVersion: argoproj.io/v1alpha1" in content_preview and "kind: Application" in content_preview),
            ("flux", lambda: any(path_lower.endswith(ext) for ext in [".yaml", ".yml"]) and ("apiVersion: kustomize.toolkit.fluxcd.io" in content_preview or "apiVersion: fluxcd.io" in content_preview)),
            ("spinnaker", lambda: any(path_lower.endswith(ext) for ext in [".json", ".yaml", ".yml"]) and any(p in content_lower for p in ["application:", "pipelines:", "stages:"])),
            ("argo_workflows", lambda: any(path_lower.endswith(ext) for ext in [".yaml", ".yml"]) and "apiVersion: argoproj.io/v1alpha1" in content_preview and "kind: Workflow" in content_preview),
            ("tekton", lambda: any(path_lower.endswith(ext) for ext in [".yaml", ".yml"]) and "apiVersion: tekton.dev" in content_preview),
            ("crossplane", lambda: any(path_lower.endswith(ext) for ext in [".yaml", ".yml"]) and "apiVersion: apiextensions.crossplane.io" in content_preview),
            ("karpenter", lambda: any(path_lower.endswith(ext) for ext in [".yaml", ".yml"]) and "apiVersion: karpenter.sh" in content_preview),
            ("backstage", lambda: any(path_lower.endswith(ext) for ext in [".yaml", ".yml"]) and "apiVersion: backstage.io/v1alpha1" in content_preview),
            ("sam", lambda: any(path_lower.endswith(ext) for ext in [".yaml", ".yml", "template.yaml"]) and "Transform: AWS::Serverless" in content_preview),
            ("serverless", lambda: ("serverless.yml" in path_lower or "serverless.yaml" in path_lower) and any(p in content_lower for p in ["service:", "provider:", "functions:"])),
            ("bash", lambda: (path_lower.endswith(".sh") or path_lower.endswith(".bash")) and ("#!/bin/bash" in content_preview or "#!/usr/bin/env bash" in content_preview) and any(p in content_lower for p in ["terraform", "kubectl", "aws", "gcloud", "az"])),
            ("powershell", lambda: any(path_lower.endswith(ext) for ext in [".ps1", ".psm1", ".psd1"]) and ("#!/usr/bin/env pwsh" in content_preview or "New-Az" in content_preview)),
        ]
        
        for code_type, check_func in detection_order:
            try:
                if check_func():
                    return code_type
            except Exception:
                continue
        
        return None

    async def collect(self, max_examples: int | None = None) -> CollectionResult:
        """Collect code examples from GitHub.
        
        Args:
            max_examples: Maximum number of examples to collect (None for all)
        
        Returns:
            CollectionResult with collected code examples
        """
        logger.info("Starting GitHub code examples collection...")
        if max_examples:
            logger.info("Target: %d code examples", max_examples)
        
        logger.info(
            "Structure extraction: %s, Quality evaluation: %s",
            "enabled" if self.enable_structure_extraction else "disabled",
            "enabled" if self.enable_quality_evaluation else "disabled",
        )
        if not self.enable_structure_extraction:
            logger.warning(
                "Structure extraction is disabled. Quality templates will NOT be created. "
                "Set GITHUB_ENABLE_STRUCTURE_EXTRACTION=true to enable."
            )
        elif not self.enable_quality_evaluation:
            logger.warning(
                "Quality evaluation is disabled. Quality templates will NOT be created. "
                "Set GITHUB_ENABLE_QUALITY_EVALUATION=true to enable."
            )
        
        if not self.github_token:
            logger.warning(
                "No GitHub token configured. API requests will be rate-limited and may fail with 403 errors. "
                "Set GITHUB_INTERNAL_TOKEN environment variable to increase rate limits."
            )
        else:
            try:
                client = self._get_httpx_client()
                test_response = await client.get("https://api.github.com/user")
                if test_response.status_code == 401:
                    logger.error(
                        "GitHub token is invalid or expired. API requests will fail with 403 errors."
                    )
                elif test_response.status_code == 403:
                    logger.warning(
                        "GitHub token may lack required permissions. API requests may fail with 403 errors."
                    )
                elif test_response.status_code == 200:
                    logger.debug("GitHub token validated successfully")
            except Exception as e:
                logger.warning("Failed to validate GitHub token: %s", e)
        
        result = CollectionResult(
            collector_name=self.collector_name,
            version="1.0",
            success=False,
            items=[],
            errors=[],
            metrics=self.metrics,
        )
        
        queries = self.get_source_urls()
        github_client = self._get_github_client()
        
        total_repo_count = 0
        repo_semaphore = asyncio.Semaphore(self.max_concurrent_repos)
        
        async def process_repo_with_semaphore(repo_data: dict[str, Any]) -> list[dict[str, Any]]:
            async with repo_semaphore:
                repo_name = repo_data.get("full_name", "unknown")
                try:
                    logger.debug("Processing repository: %s", repo_name)
                    
                    result = await with_timeout_and_retry(
                        self._process_repository_from_data,
                        timeout_seconds=300.0,
                        max_attempts=2,
                        initial_delay=2.0,
                        max_delay=10.0,
                        retryable_exceptions=(
                            httpx.HTTPStatusError,
                            httpx.RequestError,
                            httpx.TimeoutException,
                            ConnectionError,
                            TimeoutError,
                            GithubException,
                        ),
                        repo_data=repo_data,
                    )
                    logger.debug("Completed repository: %s (%d examples)", repo_name, len(result))
                    return result
                except asyncio.TimeoutError:
                    logger.warning("Repository processing timed out after 300 seconds: %s", repo_name)
                    return []
                except Exception as e:
                    logger.warning("Error processing repository %s: %s", repo_name, e)
                    return []
        
        for query in queries:
            try:
                if max_examples and len(result.items) >= max_examples:
                    logger.info("Reached max_examples limit (%d), stopping collection", max_examples)
                    break
                
                if not max_examples and self.max_repos_per_query and total_repo_count >= self.max_repos_per_query:
                    logger.info("Reached max_repos limit (%d), stopping collection", self.max_repos_per_query)
                    break
                
                logger.info("Searching GitHub: %s", query)
                
                repos_data = await self._search_github_async(query, max_examples=max_examples)
                
                if not repos_data:
                    logger.warning("No repositories found for query: %s", query)
                    continue
                
                logger.info("Found %d repositories for query: %s", len(repos_data), query)
                
                repos_to_process = []
                for repo_data in repos_data:
                    if max_examples and len(result.items) >= max_examples:
                        break
                    
                    if not max_examples and self.max_repos_per_query and total_repo_count >= self.max_repos_per_query:
                        break
                    
                    repos_to_process.append(repo_data)
                    total_repo_count += 1
                
                if not repos_to_process:
                    logger.debug("No repositories to process for query: %s", query)
                    continue
                
                logger.info("Processing %d repositories with concurrency limit of %d", len(repos_to_process), self.max_concurrent_repos)
                
                repo_tasks = []
                for repo_data in repos_to_process:
                    repo_tasks.append(process_repo_with_semaphore(repo_data))
                
                if repo_tasks:
                    logger.info("Waiting for %d repository processing tasks to complete...", len(repo_tasks))
                    repo_results = await asyncio.gather(*repo_tasks, return_exceptions=True)
                    logger.info("Completed processing %d repositories", len(repo_results))
                else:
                    repo_results = []
                
                for i, repo_result in enumerate(repo_results):
                    if max_examples and len(result.items) >= max_examples:
                        break
                    
                    if isinstance(repo_result, Exception):
                        repo_data = repos_to_process[i] if i < len(repos_to_process) else {}
                        repo_name = repo_data.get("full_name", "unknown")
                        repo_url = repo_data.get("html_url", "")
                        
                        logger.warning("Failed to process repository %s: %s", repo_name, repo_result)
                        result.add_error(
                            url=repo_url,
                            error_type="repository_processing",
                            error_message=f"Failed to process repository {repo_name}: {str(repo_result)}",
                        )
                        continue
                    
                    examples = repo_result
                    result.items.extend(examples)
                    
                    if len(result.items) % 10 == 0:
                        logger.info("Collected %d code examples from %d repositories so far...", len(result.items), total_repo_count)
                    
                    if max_examples and len(result.items) >= max_examples:
                        result.items = result.items[:max_examples]
                        logger.info("Reached max_examples limit (%d), truncating to %d examples", max_examples, len(result.items))
                        break
                
                if max_examples and len(result.items) >= max_examples:
                    break
                
                if not max_examples and self.max_repos_per_query and total_repo_count >= self.max_repos_per_query:
                    break
                
                await asyncio.sleep(1)
            
            except RateLimitExceededException:
                logger.warning("GitHub rate limit exceeded. Waiting...")
                await asyncio.sleep(60)
                continue
            
            except Exception as e:
                logger.error("Error processing query %s: %s", query, e)
                result.add_error(
                    url=query,
                    error_type="query_processing",
                    error_message=f"Error processing query {query}: {str(e)}",
                )
                continue
        
        result.metrics.total_items_collected = len(result.items)
        result.finalize()
        logger.info("Collection complete: %d examples collected, %d errors", len(result.items), len(result.errors))
        
        if self._httpx_client:
            await self._httpx_client.aclose()
            self._httpx_client = None
        
        return result

    async def collect_paginated(
        self,
        batch_size: int = 100,
        max_examples: int | None = None,
    ) -> AsyncIterator[list[dict[str, Any]]]:
        """Collect code examples from GitHub in batches (memory-efficient).
        
        Yields batches of code examples as they are collected, avoiding
        loading all repositories into memory at once.
        
        Args:
            batch_size: Number of repositories to process per batch (default: 100)
            max_examples: Maximum number of examples to collect (None for all)
            
        Yields:
            Batches of code example dictionaries
        """
        
        logger.info("Starting paginated GitHub code examples collection...")
        if max_examples:
            logger.info("Target: %d code examples (batch size: %d)", max_examples, batch_size)
        else:
            logger.info("Batch size: %d repositories per batch", batch_size)
        
        queries = self.get_source_urls()
        total_repo_count = 0
        total_examples_collected = 0
        repo_semaphore = asyncio.Semaphore(self.max_concurrent_repos)
        
        async def process_repo_with_semaphore(repo_data: dict[str, Any]) -> list[dict[str, Any]]:
            async with repo_semaphore:
                repo_name = repo_data.get("full_name", "unknown")
                try:
                    logger.debug("Processing repository: %s", repo_name)
                    
                    result = await with_timeout_and_retry(
                        self._process_repository_from_data,
                        timeout_seconds=300.0,
                        max_attempts=2,
                        initial_delay=2.0,
                        max_delay=10.0,
                        retryable_exceptions=(
                            httpx.HTTPStatusError,
                            httpx.RequestError,
                            httpx.TimeoutException,
                            ConnectionError,
                            TimeoutError,
                            GithubException,
                        ),
                        repo_data=repo_data,
                    )
                    logger.debug("Completed repository: %s (%d examples)", repo_name, len(result))
                    return result
                except asyncio.TimeoutError:
                    logger.warning("Repository processing timed out after 300 seconds: %s", repo_name)
                    return []
                except Exception as e:
                    logger.warning("Error processing repository %s: %s", repo_name, e)
                    return []
        
        for query in queries:
            try:
                if max_examples and total_examples_collected >= max_examples:
                    logger.info("Reached max_examples limit (%d), stopping collection", max_examples)
                    break
                
                if not max_examples and self.max_repos_per_query and total_repo_count >= self.max_repos_per_query:
                    logger.info("Reached max_repos limit (%d), stopping collection", self.max_repos_per_query)
                    break
                
                logger.info("Searching GitHub: %s", query)
                
                repos_data = await self._search_github_async(query, max_examples=max_examples)
                
                if not repos_data:
                    logger.warning("No repositories found for query: %s", query)
                    continue
                
                logger.info("Found %d repositories for query: %s", len(repos_data), query)
                
                repos_to_process = []
                for repo_data in repos_data:
                    if max_examples and total_examples_collected >= max_examples:
                        break
                    
                    if not max_examples and self.max_repos_per_query and total_repo_count >= self.max_repos_per_query:
                        break
                    
                    repos_to_process.append(repo_data)
                    total_repo_count += 1
                
                if not repos_to_process:
                    logger.debug("No repositories to process for query: %s", query)
                    continue
                
                for i in range(0, len(repos_to_process), batch_size):
                    if max_examples and total_examples_collected >= max_examples:
                        break
                    
                    batch_repos = repos_to_process[i:i+batch_size]
                    logger.info(
                        "Processing batch %d-%d of %d repositories (batch size: %d)",
                        i + 1,
                        min(i + batch_size, len(repos_to_process)),
                        len(repos_to_process),
                        len(batch_repos)
                    )
                    
                    repo_tasks = [process_repo_with_semaphore(repo_data) for repo_data in batch_repos]
                    
                    if repo_tasks:
                        repo_results = await asyncio.gather(*repo_tasks, return_exceptions=True)
                    else:
                        repo_results = []
                    
                    batch_examples = []
                    for repo_result in repo_results:
                        if max_examples and total_examples_collected >= max_examples:
                            break
                        
                        if isinstance(repo_result, Exception):
                            continue
                        
                        examples = repo_result
                        batch_examples.extend(examples)
                        total_examples_collected += len(examples)
                        
                        if max_examples and total_examples_collected >= max_examples:
                            batch_examples = batch_examples[:max_examples - (total_examples_collected - len(examples))]
                            break
                    
                    if batch_examples:
                        logger.info(
                            "Collected batch: %d examples (total: %d/%s)",
                            len(batch_examples),
                            total_examples_collected,
                            max_examples if max_examples else "unlimited"
                        )
                        yield batch_examples
                    
                    if max_examples and total_examples_collected >= max_examples:
                        logger.info("Reached max_examples limit (%d), stopping collection", max_examples)
                        break
                
                if max_examples and total_examples_collected >= max_examples:
                    break
                
                if not max_examples and self.max_repos_per_query and total_repo_count >= self.max_repos_per_query:
                    break
                
                await asyncio.sleep(1)
            
            except RateLimitExceededException:
                logger.warning("GitHub rate limit exceeded. Waiting...")
                await asyncio.sleep(60)
                continue
            
            except Exception as e:
                logger.error("Error processing query %s: %s", query, e)
                continue
        
        logger.info("Paginated collection complete: %d examples collected", total_examples_collected)
        
        if self._httpx_client:
            await self._httpx_client.aclose()
            self._httpx_client = None

    async def _extract_repository_structure(self, repo: Any) -> dict[str, Any] | None:
        """Extract repository file tree structure.
        
        Extracts the repository structure once per repository and reuses it
        for all code examples from that repository. Fails gracefully if extraction
        fails to avoid impacting code examples collection.
        
        Args:
            repo: GitHub repository object
            
        Returns:
            Repository structure dictionary or None if extraction fails
        """
        if not self.enable_structure_extraction:
            logger.debug("Structure extraction disabled, skipping repository")
            return None
        
        repo_name = "unknown"
        try:
            from wistx_mcp.tools.lib.github_tree_fetcher import GitHubTreeFetcher
            
            tree_fetcher = GitHubTreeFetcher(github_token=self.github_token)
            loop = asyncio.get_event_loop()
            
            def get_repo_info():
                return {
                    "html_url": repo.html_url,
                    "default_branch": repo.default_branch,
                    "full_name": repo.full_name,
                }
            
            repo_info = await loop.run_in_executor(None, get_repo_info)
            repo_name = repo_info["full_name"]
            repo_url = repo_info["html_url"]
            default_branch = repo_info["default_branch"]
            
            logger.info("Starting structure extraction for repository: %s", repo_name)
            logger.debug("Fetching tree for %s (branch: %s)", repo_name, default_branch)
            
            result = await tree_fetcher.fetch_tree(
                repo_url=repo_url,
                branch=default_branch,
                include_content=False,
                max_file_size=0,
                include_patterns=None,
                exclude_patterns=[
                    "**/node_modules/**",
                    "**/.git/**",
                    "**/__pycache__/**",
                    "**/.venv/**",
                    "**/venv/**",
                    "**/dist/**",
                    "**/build/**",
                    "**/target/**",
                    "**/.idea/**",
                    "**/.vscode/**",
                    "**/vendor/**",
                ],
                max_depth=self.max_depth,
            )
            
            if result and "structure" in result:
                metadata = result.get("metadata", {})
                total_files = metadata.get("total_files", 0)
                logger.info(
                    "Extracted repository structure for %s (%d files, %d directories)",
                    repo_name,
                    total_files,
                    metadata.get("total_directories", 0),
                )
                
                if self.enable_quality_evaluation:
                    logger.info("Starting quality evaluation for repository: %s", repo_name)
                    repo_data = {
                        "html_url": repo_info["html_url"],
                        "full_name": repo_info["full_name"],
                    }
                    await self._evaluate_and_store_quality_template(result, repo_data)
                else:
                    logger.debug("Quality evaluation disabled, skipping for %s", repo_name)
                
                return result["structure"]
            else:
                logger.warning("Tree fetch returned no structure for %s", repo_name)
            
        except ImportError as e:
            logger.warning(
                "GitHubTreeFetcher not available, skipping structure extraction for %s: %s",
                repo_name,
                e,
            )
        except Exception as e:
            logger.warning(
                "Failed to extract repository structure for %s: %s",
                repo_name,
                e,
                exc_info=True,
            )
        
        return None

    async def _extract_repository_structure_from_data(self, repo_data: dict[str, Any]) -> dict[str, Any] | None:
        """Extract repository file tree structure from repo_data.
        
        Args:
            repo_data: Repository data from GitHub API
            
        Returns:
            Repository structure dictionary or None if extraction fails
        """
        if not self.enable_structure_extraction:
            logger.debug("Structure extraction disabled, skipping for %s", repo_data.get("full_name", "unknown"))
            return None
        
        repo_name = repo_data.get("full_name", "unknown")
        
        if not self.github_token:
            logger.warning(
                "No GitHub token configured. Structure extraction may fail with 403 errors for %s",
                repo_name,
            )
        
        logger.info("Starting structure extraction for repository: %s", repo_name)
        
        try:
            from wistx_mcp.tools.lib.github_tree_fetcher import GitHubTreeFetcher
            
            tree_fetcher = GitHubTreeFetcher(github_token=self.github_token)
            repo_url = repo_data.get("html_url", "")
            default_branch = repo_data.get("default_branch", "main")
            
            logger.debug("Fetching tree for %s (branch: %s)", repo_name, default_branch)
            result = await tree_fetcher.fetch_tree(
                repo_url=repo_url,
                branch=default_branch,
                include_content=False,
                max_file_size=0,
                include_patterns=None,
                exclude_patterns=[
                    "**/node_modules/**",
                    "**/.git/**",
                    "**/__pycache__/**",
                    "**/.venv/**",
                    "**/venv/**",
                    "**/dist/**",
                    "**/build/**",
                    "**/target/**",
                    "**/.idea/**",
                    "**/.vscode/**",
                    "**/vendor/**",
                ],
                max_depth=self.max_depth,
            )
            
            if result and "structure" in result:
                metadata = result.get("metadata", {})
                total_files = metadata.get("total_files", 0)
                logger.info(
                    "Extracted repository structure for %s (%d files, %d directories)",
                    repo_name,
                    total_files,
                    metadata.get("total_directories", 0),
                )
                
                if self.enable_quality_evaluation:
                    logger.info("Starting quality evaluation for repository: %s", repo_name)
                    await self._evaluate_and_store_quality_template(result, repo_data)
                else:
                    logger.debug("Quality evaluation disabled, skipping for %s", repo_name)
                
                return result["structure"]
            else:
                logger.warning("Tree fetch returned no structure for %s", repo_name)
            
        except ImportError as e:
            logger.warning(
                "GitHubTreeFetcher not available, skipping structure extraction for %s: %s",
                repo_name,
                e,
            )
        except Exception as e:
            logger.warning(
                "Failed to extract repository structure for %s: %s",
                repo_name,
                e,
                exc_info=True,
            )
        
        return None

    async def _evaluate_and_store_quality_template(
        self, tree_result: dict[str, Any], repo_data: dict[str, Any]
    ) -> None:
        """Evaluate repository tree quality and store as quality template if score meets threshold.
        
        Args:
            tree_result: Repository tree result from GitHubTreeFetcher
            repo_data: Repository data from GitHub API
        """
        if not self.enable_quality_evaluation:
            logger.debug("Quality evaluation disabled, skipping for %s", repo_data.get("full_name", "unknown"))
            return
        
        repo_name = repo_data.get("full_name", "unknown")
        logger.info("Evaluating quality for repository: %s", repo_name)
        
        try:
            from wistx_mcp.services.quality_scorer import QualityScorer
            from wistx_mcp.services.template_storage_service import TemplateStorageService
            from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
            
            logger.debug("Initializing QualityScorer for %s", repo_name)
            scorer = QualityScorer()
            logger.debug("Scoring repository tree for %s", repo_name)
            quality_score_result = scorer.score_repository_tree(tree_result)
            
            logger.info(
                "Quality score for %s: %.2f (threshold: %.2f, meets_threshold: %s)",
                repo_name,
                quality_score_result.overall_score,
                QualityScorer.STORAGE_THRESHOLD,
                quality_score_result.meets_threshold,
            )
            
            if quality_score_result.meets_threshold:
                async with MongoDBClient() as mongodb_client:
                    await mongodb_client.connect()
                    
                    if mongodb_client.database is None:
                        logger.debug("MongoDB not connected, skipping template storage")
                        return
                    
                    repo_url = repo_data.get("html_url", "")
                    
                    collection = mongodb_client.database["quality_templates"]
                    existing_template = await collection.find_one({
                        "source_repo_url": repo_url,
                        "type": "repository_tree",
                    })
                    
                    existing_score = existing_template.get("quality_score", 0) if existing_template else 0
                    
                    if existing_template and quality_score_result.overall_score <= existing_score:
                        logger.debug(
                            "Template already exists for %s with equal or higher score (%.2f >= %.2f), skipping",
                            repo_data.get("full_name", "unknown"),
                            existing_score,
                            quality_score_result.overall_score,
                        )
                        return
                    
                    if existing_template:
                        logger.info(
                            "Updating existing template for %s (old score: %.2f, new score: %.2f)",
                            repo_data.get("full_name", "unknown"),
                            existing_score,
                            quality_score_result.overall_score,
                        )
                    
                    storage_service = TemplateStorageService(mongodb_client)
                    
                    metadata = tree_result.get("metadata", {})
                    tags = []
                    if metadata.get("languages"):
                        tags.extend(metadata["languages"][:5])
                    
                    categories = []
                    languages = metadata.get("languages", [])
                    if any("terraform" in lang.lower() or "tf" in lang.lower() for lang in languages):
                        categories.append("terraform")
                    if any("yaml" in lang.lower() or "yml" in lang.lower() for lang in languages):
                        categories.append("kubernetes")
                    
                    try:
                        if existing_template:
                            await collection.update_one(
                                {"template_id": existing_template["template_id"]},
                                {
                                    "$set": {
                                        "quality_score": quality_score_result.overall_score,
                                        "score_breakdown": quality_score_result.score_breakdown,
                                        "content": tree_result.get("structure", {}),
                                        "metadata": metadata,
                                        "tags": tags,
                                        "categories": categories,
                                    }
                                }
                            )
                            template_id = existing_template["template_id"]
                            logger.info(
                                "Updated quality template for %s: id=%s, score=%.2f",
                                repo_data.get("full_name", "unknown"),
                                template_id,
                                quality_score_result.overall_score,
                            )
                        else:
                            template_id = await storage_service.store_template(
                                template_type="repository_tree",
                                content=tree_result.get("structure", {}),
                                quality_score=quality_score_result.overall_score,
                                score_breakdown=quality_score_result.score_breakdown,
                                metadata=metadata,
                                source_repo_url=repo_url,
                                tags=tags,
                                categories=categories,
                                visibility="global",
                            )
                            logger.info(
                                "Stored quality template for %s: id=%s, score=%.2f",
                                repo_data.get("full_name", "unknown"),
                                template_id,
                                quality_score_result.overall_score,
                            )
                    except Exception as e:
                        logger.warning(
                            "Failed to store quality template for %s: %s",
                            repo_data.get("full_name", "unknown"),
                            e,
                        )
            else:
                logger.debug(
                    "Repository %s quality score %.2f below threshold (%.2f), not storing template",
                    repo_data.get("full_name", "unknown"),
                    quality_score_result.overall_score,
                    QualityScorer.STORAGE_THRESHOLD,
                )
        except ImportError as e:
            logger.warning(
                "Quality evaluation services not available, skipping template storage for %s: %s",
                repo_name,
                e,
            )
        except Exception as e:
            logger.warning(
                "Failed to evaluate/store quality template for %s: %s",
                repo_name,
                e,
                exc_info=True,
            )

    async def _discover_files_recursive_async(
        self,
        repo_full_name: str,
        path: str,
        branch: str,
        depth: int,
    ) -> list[dict[str, Any]]:
        """Recursively discover files in repository using GitHub REST API.
        
        Args:
            repo_full_name: Repository full name (owner/repo)
            path: Current directory path
            branch: Branch name
            depth: Current depth level
            
        Returns:
            List of file dictionaries with path and content
        """
        files = []
        
        if depth > self.max_depth:
            return files
        
        try:
            client = self._get_httpx_client()
            url = f"https://api.github.com/repos/{repo_full_name}/contents/{path}"
            params = {"ref": branch} if branch else {}
            
            response = await client.get(url, params=params)
            
            if response.status_code == 404:
                return files
            
            if response.status_code == 403:
                error_msg = response.text
                if "rate limit" in error_msg.lower():
                    remaining = response.headers.get("X-RateLimit-Remaining", "unknown")
                    logger.warning(
                        "GitHub API rate limit exceeded for %s/%s. Remaining: %s",
                        repo_full_name,
                        path,
                        remaining,
                    )
                    await self._wait_for_rate_limit_reset(response)
                    return await self._discover_files_recursive_async(
                        repo_full_name, path, branch, depth
                    )
                else:
                    logger.warning(
                        "GitHub API returned 403 Forbidden for %s/%s. Token may be invalid or lack required permissions.",
                        repo_full_name,
                        path,
                    )
                return files
            
            response.raise_for_status()
            contents = response.json()
            
            if not isinstance(contents, list):
                contents = [contents]
            
            for item in contents:
                if item.get("type") == "file":
                    if self._should_process_file(item.get("path", "")):
                        try:
                            file_path = item.get("path", "")
                            file_content = None
                            
                            if item.get("content"):
                                try:
                                    file_content = base64.b64decode(item["content"]).decode("utf-8")
                                except Exception as e:
                                    logger.debug("Failed to decode base64 content for %s: %s", file_path, e)
                            
                            if not file_content:
                                file_url = f"https://api.github.com/repos/{repo_full_name}/contents/{file_path}"
                                file_params = {"ref": branch} if branch else {}
                                file_response = await client.get(file_url, params=file_params)
                                
                                if file_response.status_code == 404:
                                    logger.debug("File not found (404): %s", file_path)
                                    continue
                                
                                if file_response.status_code == 403:
                                    error_msg = file_response.text
                                    if "rate limit" in error_msg.lower():
                                        await self._wait_for_rate_limit_reset(file_response)
                                        file_response = await client.get(file_url, params=file_params)
                                        if file_response.status_code == 404:
                                            continue
                                
                                file_response.raise_for_status()
                                file_data = file_response.json()
                                
                                if file_data.get("content"):
                                    file_content = base64.b64decode(file_data["content"]).decode("utf-8")
                                elif file_data.get("download_url"):
                                    download_response = await client.get(file_data["download_url"])
                                    if download_response.status_code == 404:
                                        logger.debug("Download URL returned 404 for %s", file_path)
                                        continue
                                    
                                    if download_response.status_code == 403:
                                        error_msg = download_response.text
                                        if "rate limit" in error_msg.lower():
                                            await self._wait_for_rate_limit_reset(download_response)
                                            download_response = await client.get(file_data["download_url"])
                                            if download_response.status_code == 404:
                                                continue
                                    
                                    download_response.raise_for_status()
                                    file_content = download_response.text
                            
                            if file_content:
                                files.append({
                                    "path": file_path,
                                    "content": file_content,
                                })
                        except Exception as e:
                            logger.debug("Skipping file %s: %s", item.get("path", ""), e)
                            continue
                
                elif item.get("type") == "dir":
                    if self._should_process_directory(item.get("path", "")):
                        sub_files = await self._discover_files_recursive_async(
                            repo_full_name,
                            item.get("path", ""),
                            branch,
                            depth + 1,
                        )
                        files.extend(sub_files)
        
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                logger.warning(
                    "Failed to access directory %s/%s: 403 Forbidden. GitHub token may be invalid or lack permissions.",
                    repo_full_name,
                    path,
                )
            else:
                logger.debug("Failed to access directory %s/%s: %s", repo_full_name, path, e)
        except Exception as e:
            logger.debug("Failed to access directory %s/%s: %s", repo_full_name, path, e)
        
        return files

    async def _process_repository_from_data(self, repo_data: dict[str, Any]) -> list[dict[str, Any]]:
        """Process repository from GitHub API data dictionary.
        
        Uses GitHub REST API directly via httpx instead of PyGithub to avoid 403 errors.
        
        Args:
            repo_data: Repository data from GitHub API
            
        Returns:
            List of code example dictionaries
        """
        repo_full_name = repo_data.get("full_name", "unknown/unknown")
        repo_props = {
            "name": repo_data.get("name", "unknown"),
            "description": repo_data.get("description") or "",
            "full_name": repo_full_name,
            "html_url": repo_data.get("html_url", ""),
            "stargazers_count": repo_data.get("stargazers_count", 0),
            "default_branch": repo_data.get("default_branch", "main"),
        }
        
        try:
            repository_structure = None
            if self.enable_structure_extraction:
                logger.debug("Structure extraction enabled, attempting extraction for %s", repo_props["full_name"])
                repository_structure = await self._extract_repository_structure_from_data(repo_data)
            else:
                logger.debug("Structure extraction disabled, skipping for %s", repo_props["full_name"])
            
            default_branch = repo_props["default_branch"]
            files_to_process = await self._discover_files_recursive_async(
                repo_full_name,
                "",
                default_branch,
                0,
            )
            
            logger.debug("Found %d files to process in repository %s", len(files_to_process), repo_props["full_name"])
            
            examples = []
            file_count = 0
            
            for file_info in files_to_process:
                if file_count >= self.max_files_per_repo:
                    break
                
                file_path = file_info["path"]
                
                try:
                    file_content = file_info["content"]
                    
                    if len(file_content.encode("utf-8")) > MAX_FILE_SIZE:
                        logger.debug("Skipping large file: %s (%d bytes)", file_path, len(file_content))
                        continue
                    
                    code_type = self._detect_code_type(file_path, file_content)
                    
                    if not code_type:
                        continue
                    
                    parser = self.parsers.get(code_type)
                    if not parser:
                        continue
                    
                    if not parser.validate_syntax(file_content):
                        continue
                    
                    cloud_provider = parser.extract_cloud_provider(file_content)
                    services = parser.extract_services(file_content)
                    resources = parser.extract_resources(file_content)
                    metadata = parser.extract_metadata(file_content)
                    
                    example = {
                        "title": f"{repo_props['name']} - {Path(file_path).name}",
                        "description": repo_props["description"] or f"{code_type} code example from {repo_props['full_name']}",
                        "code": file_content,
                        "code_type": code_type,
                        "cloud_provider": cloud_provider or "unknown",
                        "services": services,
                        "resources": resources,
                        "github_url": repo_props["html_url"],
                        "stars": repo_props["stargazers_count"],
                        "quality_score": min(repo_props["stargazers_count"] // 10, 80),
                        "metadata": metadata,
                        "file_path": file_path,
                        "repository_structure": repository_structure,
                    }
                    
                    try:
                        validated = RawCodeExample(**example)
                        examples.append(validated.model_dump())
                        file_count += 1
                    except Exception as e:
                        logger.debug("Validation failed for example: %s", e)
                        continue
                
                except Exception as e:
                    logger.debug("Skipping file %s: %s", file_path, e)
                    continue
            
            return examples
            
        except Exception as e:
            logger.warning("Failed to process repository %s: %s", repo_full_name, e)
            return []

    async def _process_repository(self, repo: Any) -> list[dict[str, Any]]:
        """Process a single repository and extract code examples.
        
        Uses recursive directory traversal to find infrastructure files.
        
        Args:
            repo: GitHub repository object
            
        Returns:
            List of code example dictionaries
        """
        examples = []
        file_count = 0
        repository_structure = None
        
        try:
            loop = asyncio.get_event_loop()
            
            def get_repo_properties():
                return {
                    "name": repo.name,
                    "description": repo.description,
                    "full_name": repo.full_name,
                    "html_url": repo.html_url,
                    "stargazers_count": repo.stargazers_count,
                    "default_branch": repo.default_branch,
                }
            
            repo_props = await loop.run_in_executor(None, get_repo_properties)
            
            if self.enable_structure_extraction:
                repository_structure = await self._extract_repository_structure(repo)
            
            default_branch = repo_props["default_branch"]
            
            def get_root_contents():
                return repo.get_contents("", ref=default_branch)
            
            root_contents = await asyncio.wait_for(
                loop.run_in_executor(None, get_root_contents),
                timeout=30.0
            )
            
            logger.debug("Discovering files in repository %s...", repo_props["full_name"])
            files_to_process = await self._discover_files_recursive(repo, root_contents, "", 0)
            logger.debug("Found %d files to process in repository %s", len(files_to_process), repo_props["full_name"])
            
            for file_info in files_to_process:
                if file_count >= self.max_files_per_repo:
                    break
                
                file_path = file_info["path"]
                
                try:
                    file_content = file_info["content"]
                    
                    if len(file_content.encode("utf-8")) > MAX_FILE_SIZE:
                        logger.debug("Skipping large file: %s (%d bytes)", file_path, len(file_content))
                        continue
                    
                    code_type = self._detect_code_type(file_path, file_content)
                    
                    if not code_type:
                        continue
                    
                    parser = self.parsers.get(code_type)
                    if not parser:
                        continue
                    
                    if not parser.validate_syntax(file_content):
                        continue
                    
                    cloud_provider = parser.extract_cloud_provider(file_content)
                    services = parser.extract_services(file_content)
                    resources = parser.extract_resources(file_content)
                    metadata = parser.extract_metadata(file_content)
                    
                    example = {
                        "title": f"{repo_props['name']} - {Path(file_path).name}",
                        "description": repo_props["description"] or f"{code_type} code example from {repo_props['full_name']}",
                        "code": file_content,
                        "code_type": code_type,
                        "cloud_provider": cloud_provider or "unknown",
                        "services": services,
                        "resources": resources,
                        "github_url": repo_props["html_url"],
                        "stars": repo_props["stargazers_count"],
                        "quality_score": min(repo_props["stargazers_count"] // 10, 80),
                        "metadata": metadata,
                        "file_path": file_path,
                        "repository_structure": repository_structure,
                    }
                    
                    try:
                        validated = RawCodeExample(**example)
                        examples.append(validated.model_dump())
                        file_count += 1
                    except Exception as e:
                        logger.debug("Validation failed for example: %s", e)
                        continue
                
                except (UnicodeDecodeError, GithubException, Exception) as e:
                    logger.debug("Skipping file %s: %s", file_path, e)
                    continue
            
        except asyncio.TimeoutError:
            logger.warning("Repository processing timed out: %s", repo_props.get("full_name", "unknown"))
            return []
        except GithubException as e:
            logger.warning("Failed to process repository %s: %s", repo_props.get("full_name", "unknown"), e)
            return []
        except Exception as e:
            logger.warning("Error processing repository %s: %s", repo_props.get("full_name", "unknown"), e)
            return []
        
        return examples

    async def _discover_files_recursive(
        self,
        repo: Any,
        contents: list[Any],
        current_path: str,
        depth: int,
    ) -> list[dict[str, Any]]:
        """Recursively discover files in repository.
        
        Args:
            repo: GitHub repository object
            contents: List of content items from GitHub API
            current_path: Current directory path
            depth: Current depth level
            
        Returns:
            List of file dictionaries with path and content
        """
        files = []
        
        if depth > self.max_depth:
            return files
        
        for item in contents:
            if item.type == "file":
                if self._should_process_file(item.path):
                    try:
                        file_content = item.decoded_content.decode("utf-8")
                        files.append({
                            "path": item.path,
                            "content": file_content,
                        })
                    except (UnicodeDecodeError, Exception) as e:
                        logger.debug("Skipping file %s: %s", item.path, e)
                        continue
            
            elif item.type == "dir":
                if self._should_process_directory(item.path):
                    try:
                        loop = asyncio.get_event_loop()
                        
                        def get_sub_contents():
                            return repo.get_contents(item.path)
                        
                        sub_contents = await asyncio.wait_for(
                            loop.run_in_executor(None, get_sub_contents),
                            timeout=30.0
                        )
                        sub_files = await self._discover_files_recursive(
                            repo,
                            sub_contents,
                            item.path,
                            depth + 1,
                        )
                        files.extend(sub_files)
                    except asyncio.TimeoutError:
                        logger.warning("Directory access timed out: %s", item.path)
                        continue
                    except GithubException as e:
                        logger.debug("Failed to access directory %s: %s", item.path, e)
                        continue
                    except Exception as e:
                        logger.debug("Error accessing directory %s: %s", item.path, e)
                        continue
        
        return files

    def _should_process_file(self, file_path: str) -> bool:
        """Check if file should be processed.
        
        Args:
            file_path: File path
            
        Returns:
            True if file should be processed
        """
        path_lower = file_path.lower()
        
        for exclude_dir in EXCLUDE_DIRS:
            if f"/{exclude_dir}/" in path_lower or path_lower.startswith(f"{exclude_dir}/"):
                return False
        
        file_name = Path(file_path).name.lower()
        
        valid_extensions = [
            ".tf", ".tfvars", ".hcl", ".yaml", ".yml", ".json",
            ".py", ".ts", ".js", ".go", ".cs", ".java",
            ".sh", ".bash", ".ps1", ".psm1", ".psd1",
            ".bicep", ".dockerfile",
        ]
        
        valid_filenames = [
            "dockerfile", "docker-compose.yml", "docker-compose.yaml",
            "jenkinsfile", "chart.yaml", "values.yaml",
            "serverless.yml", "serverless.yaml", "template.yaml",
        ]
        
        if any(file_name == fn or file_name.startswith(fn) for fn in valid_filenames):
            return True
        
        if any(path_lower.endswith(ext) for ext in valid_extensions):
            return True
        
        return False

    def _should_process_directory(self, dir_path: str) -> bool:
        """Check if directory should be processed.
        
        Args:
            dir_path: Directory path
            
        Returns:
            True if directory should be processed
        """
        path_lower = dir_path.lower()
        
        for exclude_dir in EXCLUDE_DIRS:
            if exclude_dir in path_lower:
                return False
        
        for infra_dir in INFRASTRUCTURE_DIRS:
            if infra_dir in path_lower:
                return True
        
        return True

    def parse_data(self, response: Any, url: str) -> list[dict[str, Any]]:
        """Parse data from response (not used for GitHub collector).
        
        Args:
            response: Response object (not used)
            url: URL (not used)
            
        Returns:
            Empty list (parsing done in collect method)
        """
        return []

    def get_validation_model(self):
        """Get Pydantic model for validation.
        
        Returns:
            RawCodeExample model class
        """
        return RawCodeExample

    def get_deduplication_key(self, item: dict[str, Any]) -> str:
        """Get deduplication key for code example.
        
        Args:
            item: Code example dictionary
            
        Returns:
            Deduplication key
        """
        github_url = item.get("github_url", "")
        file_path = item.get("file_path", "")
        code_type = item.get("code_type", "")
        return f"{github_url}:{file_path}:{code_type}"

