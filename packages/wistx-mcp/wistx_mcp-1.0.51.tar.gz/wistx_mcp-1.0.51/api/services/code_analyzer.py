"""Code analyzer service - analyzes infrastructure code and generates analysis documents.

Uses Claude Opus for analysis generation and integrates with compliance and cost tools.
"""

import asyncio
import difflib
import hashlib
import json
import logging
from asyncio import TimeoutError as AsyncTimeoutError
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

try:
    from anthropic import AsyncAnthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    AsyncAnthropic = None

from api.config import settings
from api.services.compliance_service import ComplianceService
from api.models.v1_requests import ComplianceRequirementsRequest
from wistx_mcp.tools import pricing
from wistx_mcp.tools.lib.retry_utils import with_retry
from wistx_mcp.tools.lib.metrics import track_tool_metrics
from data_pipelines.models.knowledge_article import (
    ContentType,
    Domain,
    KnowledgeArticle,
)

logger = logging.getLogger(__name__)


class CodeAnalyzer:
    """Analyzes infrastructure code and generates analysis documents.
    
    Performs component-level analysis using Claude Opus, integrating with
    compliance and cost tools for accurate analysis.
    """

    def __init__(self):
        """Initialize code analyzer with compliance and cost services."""
        self.compliance_service = ComplianceService()
        self.pricing_tool = pricing
        
        if not ANTHROPIC_AVAILABLE:
            logger.warning(
                "anthropic package not installed. Code analysis will fail. "
                "Install with: pip install anthropic"
            )
            self.llm_client = None
            self.model = None
        else:
            anthropic_api_key = getattr(settings, "anthropic_api_key", None)
            if not anthropic_api_key:
                logger.warning(
                    "ANTHROPIC_API_KEY not set. Code analysis will fail. "
                    "Set ANTHROPIC_API_KEY in .env file."
                )
                self.llm_client = None
                self.model = None
            else:
                self.llm_client = AsyncAnthropic(api_key=anthropic_api_key)
                self.model = "claude-opus-4-1"
        self.temperature = 0.1
        self.max_tokens = 8000
        
        if "opus" in self.model.lower():
            self.llm_timeout_seconds = 120.0
        else:
            self.llm_timeout_seconds = 60.0
        self.max_file_size_mb = 10
        self.max_content_length = 100000
        self.max_component_content_length = 50000
        self.code_similarity_threshold = 0.7

    def _validate_component_info(self, component_info: dict[str, Any]) -> None:
        """Validate component info structure.
        
        Args:
            component_info: Component information dictionary
            
        Raises:
            ValueError: If validation fails
        """
        required_fields = ["name", "type", "start_line", "end_line"]
        from api.exceptions import ValidationError
        
        for field in required_fields:
            if field not in component_info:
                raise ValidationError(
                    message=f"Missing required field in component_info: {field}",
                    user_message=f"Missing required field: {field}",
                    error_code="MISSING_REQUIRED_FIELD",
                    details={"field": field, "required_fields": required_fields}
                )
        
        start_line = component_info["start_line"]
        end_line = component_info["end_line"]
        
        if not isinstance(start_line, int) or start_line < 1:
            raise ValidationError(
                message=f"start_line must be positive integer, got: {start_line}",
                user_message="Invalid start line number",
                error_code="INVALID_START_LINE",
                details={"start_line": start_line}
            )
        
        if not isinstance(end_line, int) or end_line < start_line:
            raise ValidationError(
                message=f"end_line ({end_line}) must be >= start_line ({start_line})",
                user_message="End line must be greater than or equal to start line",
                error_code="INVALID_END_LINE",
                details={"start_line": start_line, "end_line": end_line}
            )
        
        if not isinstance(component_info.get("name"), str) or not component_info["name"]:
            raise ValidationError(
                message="component name must be non-empty string",
                user_message="Component name is required",
                error_code="INVALID_COMPONENT_NAME",
                details={"name": component_info.get("name")}
            )
        
        if not isinstance(component_info.get("type"), str) or not component_info["type"]:
            raise ValidationError(
                message="component type must be non-empty string",
                user_message="Component type is required",
                error_code="INVALID_COMPONENT_TYPE",
                details={"type": component_info.get("type")}
            )

    def _validate_repo_context(self, repo_context: dict[str, Any]) -> None:
        """Validate repository context.
        
        Args:
            repo_context: Repository context dictionary
            
        Raises:
            ValueError: If validation fails
        """
        required_fields = ["repo_url", "branch", "commit_sha", "resource_id", "user_id"]
        from api.exceptions import ValidationError
        
        for field in required_fields:
            if field not in repo_context:
                raise ValidationError(
                    message=f"Missing required field in repo_context: {field}",
                    user_message=f"Missing required field: {field}",
                    error_code="MISSING_REQUIRED_FIELD",
                    details={"field": field, "required_fields": required_fields}
                )
        
        if not repo_context["commit_sha"] or len(repo_context["commit_sha"]) < 7:
            raise ValidationError(
                message="commit_sha must be valid SHA (at least 7 characters)",
                user_message="Invalid commit SHA. Must be at least 7 characters.",
                error_code="INVALID_COMMIT_SHA",
                details={"commit_sha": repo_context.get("commit_sha")}
            )
        
        if not repo_context["branch"]:
            raise ValueError("branch must be non-empty string")

    def _detect_excessive_code_copying(
        self,
        analysis_content: str,
        original_code: str,
    ) -> bool:
        """Detect if analysis contains excessive verbatim copying of original code.

        We allow relevant code snippets for illustration, but flag if:
        - A single code block is >90% similar to large portions of original code
        - Multiple code blocks together reproduce >50% of the original code

        Args:
            analysis_content: Analysis markdown content
            original_code: Original component code

        Returns:
            True if excessive code copying detected, False otherwise
        """
        if not original_code or len(original_code.strip()) < 50:
            return False

        analysis_lines = analysis_content.split("\n")

        code_blocks = []
        in_code_block = False
        current_block = []

        for line in analysis_lines:
            if line.strip().startswith("```"):
                if in_code_block:
                    if current_block:
                        code_blocks.append("\n".join(current_block))
                    current_block = []
                    in_code_block = False
                else:
                    in_code_block = True
            elif in_code_block:
                current_block.append(line)

        if current_block:
            code_blocks.append("\n".join(current_block))

        # Check for single large verbatim copy (>90% similarity on large blocks)
        for code_block in code_blocks:
            if len(code_block.strip()) < 100:  # Small snippets are OK
                continue

            similarity = difflib.SequenceMatcher(
                None,
                code_block.lower(),
                original_code.lower(),
            ).ratio()

            # Only flag if very high similarity on large blocks
            if similarity > 0.9:
                logger.warning(
                    "Excessive code copying detected (similarity: %.2f)",
                    similarity,
                )
                return True

        # Check if combined code blocks reproduce majority of original
        all_code = "\n".join(code_blocks)
        if len(all_code) > len(original_code) * 0.5:
            combined_similarity = difflib.SequenceMatcher(
                None,
                all_code.lower(),
                original_code.lower(),
            ).ratio()

            if combined_similarity > 0.7:
                logger.warning(
                    "Combined code blocks reproduce too much original code (similarity: %.2f)",
                    combined_similarity,
                )
                return True

        return False

    def _sanitize_analysis_content(
        self,
        content: str,
        original_code: str,
        source_url: str,
    ) -> str:
        """Remove code snippets from analysis content.
        
        Args:
            content: Analysis markdown content
            original_code: Original component code
            source_url: Source URL for reference
            
        Returns:
            Sanitized content without code snippets
        """
        lines = content.split("\n")
        sanitized_lines = []
        in_code_block = False
        code_block_start = -1
        
        for i, line in enumerate(lines):
            if line.strip().startswith("```"):
                if in_code_block:
                    code_block = "\n".join(lines[code_block_start:i+1])
                    
                    similarity = difflib.SequenceMatcher(
                        None,
                        code_block.lower(),
                        original_code.lower(),
                    ).ratio()
                    
                    if similarity > self.code_similarity_threshold:
                        logger.info(
                            "Removing code block from analysis (similarity: %.2f)",
                            similarity,
                        )
                        sanitized_lines.append(
                            f"\n> **Note**: Code removed for security. "
                            f"View source at: {source_url}\n"
                        )
                    else:
                        sanitized_lines.extend(lines[code_block_start:i+1])
                    
                    in_code_block = False
                    code_block_start = -1
                else:
                    in_code_block = True
                    code_block_start = i
            elif not in_code_block:
                sanitized_lines.append(line)
        
        return "\n".join(sanitized_lines)

    def calculate_file_hash(self, file_content: str) -> str:
        """Calculate SHA-256 hash of file content.
        
        Args:
            file_content: File content string
            
        Returns:
            SHA-256 hash as hexadecimal string
        """
        return hashlib.sha256(file_content.encode("utf-8")).hexdigest()

    async def should_reanalyze_file(
        self,
        file_path: Path,
        file_content: str,
        resource_id: str,
    ) -> tuple[bool, str]:
        """Check if file needs re-analysis based on content hash.
        
        Args:
            file_path: File path
            file_content: File content
            resource_id: Resource ID
            
        Returns:
            Tuple of (should_reanalyze, current_hash)
        """
        current_hash = self.calculate_file_hash(file_content)
        
        from api.database.mongodb import mongodb_manager
        
        db = mongodb_manager.get_database()
        existing = db.knowledge_articles.find_one(
            {
                "resource_id": resource_id,
                "source_url": {"$regex": str(file_path.name)},
                "source_type": "repository-analysis",
            },
            {"source_hash": 1}
        )
        
        if not existing:
            return True, current_hash
        
        existing_hash = existing.get("source_hash")
        if existing_hash != current_hash:
            logger.info(
                "File changed: %s (hash: %s -> %s)",
                file_path,
                existing_hash[:8] if existing_hash else "none",
                current_hash[:8],
            )
            return True, current_hash
        
        logger.debug("File unchanged: %s (hash: %s)", file_path, current_hash[:8])
        return False, current_hash

    async def generate_source_urls(
        self,
        repo_url: str,
        branch: str,
        commit_sha: str,
        relative_path: Path,
        start_line: int,
        end_line: int,
    ) -> dict[str, str]:
        """Generate source URLs for component (dual URL strategy).
        
        Args:
            repo_url: Repository URL
            branch: Branch name
            commit_sha: Commit SHA (for snapshot URL)
            relative_path: Relative file path
            start_line: Start line number
            end_line: End line number
            
        Returns:
            Dictionary with snapshot_url, latest_url, and file_url
        """
        repo_url_clean = repo_url.rstrip("/").replace(".git", "")
        relative_path_str = str(relative_path).replace("\\", "/")
        
        snapshot_url = f"{repo_url_clean}/blob/{commit_sha}/{relative_path_str}#L{start_line}-L{end_line}"
        latest_url = f"{repo_url_clean}/blob/{branch}/{relative_path_str}#L{start_line}-L{end_line}"
        file_url = f"{repo_url_clean}/blob/{branch}/{relative_path_str}"
        
        return {
            "snapshot_url": snapshot_url,
            "latest_url": latest_url,
            "file_url": file_url,
        }

    @track_tool_metrics(tool_name="code_analyzer.extract_resources")
    async def extract_resources(
        self,
        file_path: Path,
        file_content: str,
    ) -> dict[str, Any]:
        """Extract resource types and specs from infrastructure code.
        
        Uses LLM to identify resources in various formats:
        - Terraform: aws_instance, aws_rds_instance, etc.
        - Kubernetes: Deployment, Service, ConfigMap, etc.
        - Docker: FROM, RUN commands (infer base images)
        - CloudFormation: AWS::EC2::Instance, etc.
        
        Args:
            file_path: File path
            file_content: File content
            
        Returns:
            Dictionary with resource_types, cloud_providers, services, resources, resource_specs
        """
        if not self.llm_client:
            logger.warning("LLM client not available, using fallback extraction")
            return self._fallback_extract_resources(file_path, file_content)
        
        prompt = f"""Extract infrastructure resources from this {file_path.suffix} file.

File: {file_path}
Content:
{file_content[:30000]}

Extract:
1. Resource types (e.g., "RDS", "EC2", "Kubernetes Deployment", "Docker container")
2. Resource specifications (instance types, sizes, configurations)
3. Cloud providers (AWS, GCP, Azure, etc.)
4. Services (S3, RDS, EKS, GKE, etc.)

Return JSON:
{{
    "resource_types": ["RDS", "EC2", "S3"],
    "cloud_providers": ["aws"],
    "services": ["rds", "ec2", "s3"],
    "resources": [
        {{
            "name": "web_server",
            "type": "EC2",
            "instance_type": "t3.medium",
            "cloud": "aws",
            "service": "ec2",
            "quantity": 2,
            "start_line": 15,
            "end_line": 25
        }}
    ],
    "resource_specs": [
        {{"cloud": "aws", "service": "ec2", "instance_type": "t3.medium", "quantity": 2}},
        {{"cloud": "aws", "service": "rds", "instance_type": "db.t3.medium", "quantity": 1}}
    ]
}}
"""
        
        try:
            response = await self.llm_client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}],
            )
            
            response_text = response.content[0].text if response.content else ""
            
            if not response_text:
                logger.warning("Empty response from LLM for resource extraction")
                return self._fallback_extract_resources(file_path, file_content)
            
            try:
                result = json.loads(response_text)
                return result
            except json.JSONDecodeError as e:
                logger.warning("Failed to parse LLM response as JSON: %s", e)
                return self._fallback_extract_resources(file_path, file_content)
                
        except Exception as e:
            logger.error("Error extracting resources with LLM: %s", e, exc_info=True)
            return self._fallback_extract_resources(file_path, file_content)

    def _fallback_extract_resources(
        self,
        file_path: Path,
        file_content: str,
    ) -> dict[str, Any]:
        """Fallback resource extraction using pattern matching.

        Args:
            file_path: File path
            file_content: File content

        Returns:
            Dictionary with extracted resources
        """
        import re

        resource_types = []
        cloud_providers = []
        services = []
        resources = []
        resource_specs = []

        content_lower = file_content.lower()

        if ".tf" in file_path.suffix.lower():
            # Detect cloud providers
            if "aws_" in content_lower:
                cloud_providers.append("aws")
            if "google_" in content_lower or "gcp_" in content_lower:
                cloud_providers.append("gcp")
            if "azurerm_" in content_lower or "azure_" in content_lower:
                cloud_providers.append("azure")

            # Comprehensive Terraform resource patterns
            terraform_resources = [
                # AWS Resources
                ("aws_instance", "EC2", "ec2", "aws"),
                ("aws_rds_instance", "RDS", "rds", "aws"),
                ("aws_db_instance", "RDS", "rds", "aws"),
                ("aws_s3_bucket", "S3", "s3", "aws"),
                ("aws_eks_cluster", "EKS", "eks", "aws"),
                ("aws_eks_node_group", "EKS Node Group", "eks", "aws"),
                ("aws_lambda_function", "Lambda", "lambda", "aws"),
                ("aws_vpc", "VPC", "vpc", "aws"),
                ("aws_subnet", "Subnet", "vpc", "aws"),
                ("aws_security_group", "Security Group", "vpc", "aws"),
                ("aws_lb", "Load Balancer", "elb", "aws"),
                ("aws_alb", "Application Load Balancer", "elb", "aws"),
                ("aws_elb", "Elastic Load Balancer", "elb", "aws"),
                ("aws_ecs_cluster", "ECS Cluster", "ecs", "aws"),
                ("aws_ecs_service", "ECS Service", "ecs", "aws"),
                ("aws_ecs_task_definition", "ECS Task", "ecs", "aws"),
                ("aws_dynamodb_table", "DynamoDB", "dynamodb", "aws"),
                ("aws_sqs_queue", "SQS Queue", "sqs", "aws"),
                ("aws_sns_topic", "SNS Topic", "sns", "aws"),
                ("aws_cloudfront_distribution", "CloudFront", "cloudfront", "aws"),
                ("aws_route53", "Route53", "route53", "aws"),
                ("aws_iam_role", "IAM Role", "iam", "aws"),
                ("aws_iam_policy", "IAM Policy", "iam", "aws"),
                ("aws_kms_key", "KMS Key", "kms", "aws"),
                ("aws_elasticache", "ElastiCache", "elasticache", "aws"),

                # Azure Resources
                ("azurerm_kubernetes_cluster", "AKS Cluster", "aks", "azure"),
                ("azurerm_kubernetes_node_pool", "AKS Node Pool", "aks", "azure"),
                ("azurerm_resource_group", "Resource Group", "resource_group", "azure"),
                ("azurerm_virtual_machine", "Virtual Machine", "vm", "azure"),
                ("azurerm_virtual_network", "Virtual Network", "vnet", "azure"),
                ("azurerm_subnet", "Subnet", "vnet", "azure"),
                ("azurerm_network_security_group", "NSG", "nsg", "azure"),
                ("azurerm_storage_account", "Storage Account", "storage", "azure"),
                ("azurerm_storage_container", "Blob Container", "storage", "azure"),
                ("azurerm_sql_server", "SQL Server", "sql", "azure"),
                ("azurerm_sql_database", "SQL Database", "sql", "azure"),
                ("azurerm_cosmosdb_account", "Cosmos DB", "cosmosdb", "azure"),
                ("azurerm_function_app", "Function App", "functions", "azure"),
                ("azurerm_app_service", "App Service", "app_service", "azure"),
                ("azurerm_app_service_plan", "App Service Plan", "app_service", "azure"),
                ("azurerm_container_registry", "Container Registry", "acr", "azure"),
                ("azurerm_key_vault", "Key Vault", "keyvault", "azure"),
                ("azurerm_application_gateway", "Application Gateway", "appgw", "azure"),
                ("azurerm_load_balancer", "Load Balancer", "lb", "azure"),
                ("azurerm_public_ip", "Public IP", "network", "azure"),
                ("azurerm_dns_zone", "DNS Zone", "dns", "azure"),
                ("azurerm_redis_cache", "Redis Cache", "redis", "azure"),
                ("azurerm_service_bus_namespace", "Service Bus", "servicebus", "azure"),
                ("azurerm_eventhub_namespace", "Event Hub", "eventhub", "azure"),
                ("azurerm_log_analytics_workspace", "Log Analytics", "monitor", "azure"),
                ("azurerm_application_insights", "App Insights", "monitor", "azure"),

                # GCP Resources
                ("google_compute_instance", "GCE", "compute", "gcp"),
                ("google_compute_network", "VPC Network", "vpc", "gcp"),
                ("google_compute_subnetwork", "Subnetwork", "vpc", "gcp"),
                ("google_compute_firewall", "Firewall Rule", "firewall", "gcp"),
                ("google_sql_database_instance", "Cloud SQL", "sql", "gcp"),
                ("google_container_cluster", "GKE Cluster", "gke", "gcp"),
                ("google_container_node_pool", "GKE Node Pool", "gke", "gcp"),
                ("google_storage_bucket", "Cloud Storage", "gcs", "gcp"),
                ("google_pubsub_topic", "Pub/Sub Topic", "pubsub", "gcp"),
                ("google_pubsub_subscription", "Pub/Sub Subscription", "pubsub", "gcp"),
                ("google_bigquery_dataset", "BigQuery Dataset", "bigquery", "gcp"),
                ("google_bigquery_table", "BigQuery Table", "bigquery", "gcp"),
                ("google_cloud_function", "Cloud Function", "functions", "gcp"),
                ("google_cloud_run_service", "Cloud Run", "cloudrun", "gcp"),

                # Common/Generic
                ("random_pet", "Random Pet Name", "random", "terraform"),
                ("random_id", "Random ID", "random", "terraform"),
                ("random_string", "Random String", "random", "terraform"),
                ("null_resource", "Null Resource", "null", "terraform"),
                ("local_file", "Local File", "local", "terraform"),
            ]

            # Extract resources with line numbers
            lines = file_content.split("\n")
            for i, line in enumerate(lines, 1):
                for tf_pattern, resource_type, service, cloud in terraform_resources:
                    # Match resource "type" "name" pattern
                    pattern = rf'resource\s+"{tf_pattern}"\s+"([^"]+)"'
                    match = re.search(pattern, line)
                    if match:
                        resource_name = match.group(1)
                        resource_types.append(resource_type)
                        if service not in services:
                            services.append(service)
                        if cloud not in cloud_providers and cloud != "terraform":
                            cloud_providers.append(cloud)

                        # Find resource end (matching brace)
                        end_line = self._find_resource_end(lines, i - 1)

                        resources.append({
                            "name": resource_name,
                            "type": resource_type,
                            "cloud": cloud,
                            "service": service,
                            "start_line": i,
                            "end_line": end_line,
                        })

            # Extract resource specs from content (VM sizes, etc.)
            resource_specs = self._extract_resource_specs(file_content, cloud_providers)

        elif file_path.suffix.lower() in [".yaml", ".yml"]:
            if "apiVersion:" in content_lower and "kind:" in content_lower:
                resource_types.append("Kubernetes")
                if "kind: deployment" in content_lower:
                    resource_types.append("Kubernetes Deployment")
                if "kind: service" in content_lower:
                    resource_types.append("Kubernetes Service")
                if "kind: ingress" in content_lower:
                    resource_types.append("Kubernetes Ingress")
                if "kind: configmap" in content_lower:
                    resource_types.append("Kubernetes ConfigMap")
                if "kind: secret" in content_lower:
                    resource_types.append("Kubernetes Secret")
                if "kind: statefulset" in content_lower:
                    resource_types.append("Kubernetes StatefulSet")
                if "kind: daemonset" in content_lower:
                    resource_types.append("Kubernetes DaemonSet")

        elif file_path.name.lower() in ["dockerfile", "docker-compose.yml", "docker-compose.yaml"]:
            resource_types.append("Docker Container")
            if "from" in content_lower:
                services.append("docker")

        return {
            "resource_types": list(set(resource_types)),
            "cloud_providers": list(set(cloud_providers)),
            "services": list(set(services)),
            "resources": resources,
            "resource_specs": resource_specs,
        }

    def _find_resource_end(self, lines: list[str], start_idx: int) -> int:
        """Find the end line of a Terraform resource block."""
        brace_count = 0
        for i in range(start_idx, len(lines)):
            brace_count += lines[i].count("{") - lines[i].count("}")
            if brace_count == 0 and i > start_idx:
                return i + 1
        return len(lines)

    def _extract_resource_specs(
        self, content: str, cloud_providers: list[str]
    ) -> list[dict[str, Any]]:
        """Extract resource specifications (VM sizes, etc.) from content."""
        import re
        specs = []

        # Azure VM sizes
        azure_vm_pattern = r'vm_size\s*=\s*"([^"]+)"'
        for match in re.finditer(azure_vm_pattern, content, re.IGNORECASE):
            specs.append({
                "cloud": "azure",
                "service": "vm",
                "instance_type": match.group(1),
                "quantity": 1,
            })

        # AWS instance types
        aws_instance_pattern = r'instance_type\s*=\s*"([^"]+)"'
        for match in re.finditer(aws_instance_pattern, content, re.IGNORECASE):
            specs.append({
                "cloud": "aws",
                "service": "ec2",
                "instance_type": match.group(1),
                "quantity": 1,
            })

        # GCP machine types
        gcp_machine_pattern = r'machine_type\s*=\s*"([^"]+)"'
        for match in re.finditer(gcp_machine_pattern, content, re.IGNORECASE):
            specs.append({
                "cloud": "gcp",
                "service": "compute",
                "instance_type": match.group(1),
                "quantity": 1,
            })

        # Node counts
        node_count_pattern = r'node_count\s*=\s*(\d+)'
        for match in re.finditer(node_count_pattern, content, re.IGNORECASE):
            # Update last spec with quantity if it exists
            if specs:
                specs[-1]["quantity"] = int(match.group(1))

        return specs

    async def get_compliance_for_resources(
        self,
        resource_types: list[str],
        standards: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        """Get compliance requirements using existing compliance service.
        
        Args:
            resource_types: List of resource types
            standards: Optional list of compliance standards to check
            
        Returns:
            Dictionary with compliance controls and summary
        """
        if not resource_types:
            return {
                "controls": [],
                "summary": {"total": 0, "by_standard": {}, "by_severity": {}},
                "by_standard": {},
                "by_severity": {},
            }
        
        try:
            request = ComplianceRequirementsRequest(
                resource_types=resource_types,
                standards=standards,
                include_remediation=True,
                include_verification=True,
            )
            
            response = await self.compliance_service.get_compliance_requirements(request)
            
            def _serialize_remediation(remediation: Any) -> dict | None:
                """Safely serialize remediation data."""
                if remediation is None:
                    return None
                if isinstance(remediation, dict):
                    return remediation
                if hasattr(remediation, "model_dump"):
                    return remediation.model_dump()
                if hasattr(remediation, "__dict__"):
                    return remediation.__dict__
                return {"value": str(remediation)}

            return {
                "controls": [
                    {
                        "control_id": c.control_id,
                        "standard": c.standard,
                        "title": c.title,
                        "description": c.description,
                        "severity": c.severity,
                        "applies_to": c.applies_to or [],
                        "remediation": _serialize_remediation(c.remediation),
                    }
                    for c in response.controls
                ],
                "summary": {
                    "total": response.summary.total,
                    "by_standard": response.summary.by_standard,
                    "by_severity": response.summary.by_severity,
                },
                "by_standard": response.summary.by_standard,
                "by_severity": response.summary.by_severity,
            }
        except Exception as e:
            logger.error("Error getting compliance requirements: %s", e, exc_info=True)
            return {
                "controls": [],
                "summary": {"total": 0, "by_standard": {}, "by_severity": {}},
                "by_standard": {},
                "by_severity": {},
                "error": str(e),
            }

    async def calculate_costs_for_resources(
        self,
        resources: list[dict[str, Any]],
        track_missing: bool = True,
    ) -> dict[str, Any]:
        """Calculate costs using existing pricing tool.
        
        Args:
            resources: List of resource specifications
            track_missing: Track resources without pricing data
            
        Returns:
            Dictionary with cost breakdown and optimizations
        """
        if not resources:
            return {
                "total_monthly": 0.0,
                "total_annual": 0.0,
                "breakdown": [],
                "optimizations": [],
                "missing_pricing_count": 0,
                "missing_resources": [],
            }
        
        try:
            result = await self.pricing_tool.calculate_infrastructure_cost(resources)
            
            missing_resources = []
            for resource in resources:
                found = any(
                    b.get("resource", "").startswith(f"{resource.get('cloud')}:{resource.get('service')}")
                    for b in result.get("breakdown", [])
                )
                if not found:
                    missing_resources.append(resource)
            
            if track_missing and missing_resources:
                await self._track_missing_pricing(missing_resources)
            
            return {
                "total_monthly": result.get("total_monthly", 0.0),
                "total_annual": result.get("total_annual", 0.0),
                "breakdown": result.get("breakdown", []),
                "optimizations": result.get("optimizations", []),
                "missing_pricing_count": len(missing_resources),
                "missing_resources": missing_resources,
            }
        except Exception as e:
            logger.error("Error calculating costs: %s", e, exc_info=True)
            return {
                "total_monthly": 0.0,
                "total_annual": 0.0,
                "breakdown": [],
                "optimizations": [],
                "missing_pricing_count": len(resources),
                "missing_resources": resources,
                "error": str(e),
            }

    async def _track_missing_pricing(
        self,
        missing_resources: list[dict[str, Any]],
    ) -> None:
        """Track missing pricing data for continuous improvement.
        
        Args:
            missing_resources: List of resources without pricing data
        """
        try:
            from api.services.pricing_data_tracker import pricing_data_tracker
            
            for resource in missing_resources:
                await pricing_data_tracker.track_missing_pricing(
                    resource_spec=resource,
                    context={
                        "source": "repository_indexing",
                        "timestamp": datetime.utcnow().isoformat(),
                    },
                )
        except ImportError:
            logger.debug("PricingDataTracker not available, skipping missing data tracking")
        except Exception as e:
            logger.warning("Error tracking missing pricing data: %s", e)

    def is_infrastructure_file(self, file_path: Path) -> bool:
        """Check if file is an infrastructure file that should be analyzed holistically.

        Args:
            file_path: File path to check

        Returns:
            True if file should use holistic analysis
        """
        suffix = file_path.suffix.lower()
        name = file_path.name.lower()

        # Infrastructure-as-code files that benefit from holistic analysis
        infra_extensions = {".tf", ".tfvars", ".hcl"}
        infra_names = {"dockerfile", "docker-compose.yml", "docker-compose.yaml"}

        return suffix in infra_extensions or name in infra_names

    @track_tool_metrics(tool_name="code_analyzer.analyze_infrastructure_file")
    async def analyze_infrastructure_file(
        self,
        file_path: Path,
        file_content: str,
        repo_context: dict[str, Any],
    ) -> KnowledgeArticle:
        """Analyze an entire infrastructure file holistically.

        Unlike analyze_component which analyzes individual resources in isolation,
        this method analyzes the entire file as a unit to capture:
        - Resource relationships and dependencies
        - Aggregate cost analysis
        - Full compliance scope
        - Cross-resource security posture

        Args:
            file_path: File path
            file_content: Full file content
            repo_context: Repository context (repo_url, branch, commit_sha, resource_id, user_id)

        Returns:
            KnowledgeArticle with comprehensive file analysis
        """
        self._validate_repo_context(repo_context)

        # Extract ALL resources from the entire file
        extracted_resources = await self.extract_resources(file_path, file_content)

        # Get compliance for all resource types in the file
        all_resource_types = extracted_resources.get("resource_types", [])
        compliance_data = await self.get_compliance_for_resources(
            resource_types=all_resource_types,
            standards=repo_context.get("compliance_standards") or [],
        )

        # Calculate aggregate costs for all resources
        cost_data = await self.calculate_costs_for_resources(
            resources=extracted_resources.get("resource_specs", []),
            track_missing=True,
        )

        # Check budgets if cost data available
        budget_status = None
        if cost_data.get("total_monthly", 0) > 0:
            try:
                from api.services.budget_service import budget_service
                budget_status = await budget_service.check_budgets(
                    user_id=repo_context["user_id"],
                    estimated_cost=cost_data["total_monthly"],
                    scope={
                        "cloud_providers": extracted_resources.get("cloud_providers", []),
                        "project_id": repo_context.get("project_id"),
                    },
                )
            except Exception as e:
                logger.warning("Failed to check budgets: %s", e, exc_info=True)

        # Truncate if needed
        analysis_content = file_content
        if len(file_content) > self.max_content_length:
            logger.warning(
                "File content truncated: %s (%d chars > %d)",
                file_path,
                len(file_content),
                self.max_content_length,
            )
            analysis_content = file_content[:self.max_content_length]

        # Generate holistic analysis
        analysis = await self._generate_holistic_analysis(
            file_path=file_path,
            file_content=analysis_content,
            repo_context=repo_context,
            extracted_resources=extracted_resources,
            compliance_data=compliance_data,
            cost_data=cost_data,
            budget_status=budget_status,
        )

        # Generate URLs
        if file_path.is_absolute():
            relative_path = file_path.relative_to(Path(repo_context.get("repo_path", "")))
        else:
            relative_path = file_path

        urls = await self.generate_source_urls(
            repo_url=repo_context["repo_url"],
            branch=repo_context["branch"],
            commit_sha=repo_context["commit_sha"],
            relative_path=relative_path,
            start_line=1,
            end_line=len(file_content.split("\n")),
        )

        file_hash = self.calculate_file_hash(file_content)

        # Record spending
        if cost_data.get("total_monthly", 0) > 0:
            try:
                from api.services.budget_service import budget_service
                await budget_service.record_spending(
                    user_id=repo_context["user_id"],
                    amount_usd=cost_data["total_monthly"],
                    source_type="repository-analysis",
                    source_id=repo_context["resource_id"],
                    component_id=None,
                    cloud_provider=extracted_resources.get("cloud_providers", [None])[0],
                    project_id=repo_context.get("project_id"),
                    service=extracted_resources.get("services", [None])[0],
                    resource_type=extracted_resources.get("resource_types", [None])[0],
                    resource_spec=extracted_resources.get("resource_specs", [None])[0],
                )
            except Exception as e:
                logger.warning("Failed to record spending: %s", e, exc_info=True)

        # Detect domain and content type
        domain = self._detect_domain(file_path, file_content)
        content_type = ContentType.REFERENCE
        file_type = self._detect_file_type(file_path, file_content)

        # Create article title from file name
        article_title = f"{file_path.stem} - {file_type} Infrastructure"

        return KnowledgeArticle(
            id=f"{repo_context['resource_id']}-{file_hash[:12]}",
            title=article_title,
            summary=analysis.get("summary", f"Analysis of {file_path.name}"),
            content=analysis.get("markdown", ""),
            domain=domain,
            content_type=content_type,
            tags=extracted_resources.get("resource_types", []) + [file_type.lower()],
            source_url=urls["snapshot_url"],
            source_file=str(relative_path),
            source_lines=f"1-{len(file_content.split(chr(10)))}",
            repository_url=repo_context["repo_url"],
            branch=repo_context["branch"],
            commit_sha=repo_context["commit_sha"],
            resource_id=repo_context["resource_id"],
            user_id=repo_context["user_id"],
            last_updated=datetime.utcnow(),
            metadata={
                "file_type": file_type,
                "file_hash": file_hash,
                "resource_count": len(extracted_resources.get("resources", [])),
                "cloud_providers": extracted_resources.get("cloud_providers", []),
                "services": extracted_resources.get("services", []),
                "compliance_summary": compliance_data.get("summary", {}),
                "cost_summary": {
                    "monthly": cost_data.get("total_monthly", 0),
                    "annual": cost_data.get("total_annual", 0),
                },
                "security": analysis.get("security", {}),
                "holistic_analysis": True,
            },
        )

    async def _generate_holistic_analysis(
        self,
        file_path: Path,
        file_content: str,
        repo_context: dict[str, Any],
        extracted_resources: dict[str, Any],
        compliance_data: dict[str, Any],
        cost_data: dict[str, Any],
        budget_status: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Generate holistic infrastructure analysis using Claude Opus.

        Args:
            file_path: File path
            file_content: Full file content
            repo_context: Repository context
            extracted_resources: All extracted resources
            compliance_data: Compliance data from tool
            cost_data: Cost data from tool
            budget_status: Budget status (optional)

        Returns:
            Dictionary with analysis (summary, markdown, security)
        """
        if not self.llm_client:
            logger.warning("LLM client not available, using fallback holistic analysis")
            return self._fallback_holistic_analysis(
                file_path, file_content, extracted_resources, compliance_data, cost_data
            )

        file_type = self._detect_file_type(file_path, file_content)
        resource_count = len(extracted_resources.get("resources", []))

        prompt = f"""You are an expert infrastructure analyst. Analyze this ENTIRE infrastructure file and generate a comprehensive, professional analysis document.

IMPORTANT: This is a HOLISTIC analysis - analyze ALL resources in the file together, understanding their relationships and dependencies.

File: {file_path}
File Type: {file_type}
Total Resources: {resource_count}
Cloud Providers: {', '.join(extracted_resources.get('cloud_providers', ['Unknown']))}

=== COMPLETE FILE CONTENT ===
{file_content}
=== END FILE CONTENT ===

=== EXTRACTED RESOURCES ===
{json.dumps(extracted_resources, indent=2)}
=== END RESOURCES ===

=== COMPLIANCE REQUIREMENTS ===
{json.dumps(compliance_data, indent=2)}
=== END COMPLIANCE ===

=== COST ANALYSIS ===
{json.dumps(cost_data, indent=2)}
=== END COST ===

Generate a comprehensive infrastructure analysis. Your output should be actionable and help developers continue development.

## CONTENT REQUIREMENTS:

### 1. Infrastructure Overview
- Brief description of what this infrastructure deploys
- List all resources and their purposes
- Architecture summary

### 2. Resource Inventory
Create a TABLE of all resources:
| Resource | Type | Purpose | Key Configuration |
|----------|------|---------|-------------------|
| resource_name | resource_type | what it does | key settings |

### 3. Resource Dependencies
- Create a Mermaid diagram showing resource relationships:
```mermaid
graph TD
    A[Resource Group] --> B[AKS Cluster]
    B --> C[Node Pool]
```
- Explain dependency chain

### 4. Configuration Analysis
For EACH major resource, analyze:
- Key configuration settings
- Instance types/sizes
- Network configuration
- Storage configuration
- Authentication/authorization settings

### 5. Security Posture
Analyze security across ALL resources:
- Authentication methods (Service Principal, Managed Identity, etc.)
- RBAC configuration
- Network security (NSGs, firewall rules)
- Encryption settings
- Secrets management

Provide a security assessment TABLE:
| Security Control | Status | Finding | Recommendation |
|-----------------|--------|---------|----------------|
| RBAC Enabled | Yes/No | Details | Suggestion |

### 6. Compliance Mapping
Use compliance_data provided. Map controls to resources:
| Resource | Control | Status | Gap |
|----------|---------|--------|-----|
| resource | SOC2-XX | Compliant/Gap | Details |

### 7. Cost Analysis
Use cost_data provided. Show AGGREGATE costs:
| Resource | Type | Monthly Cost | Annual Cost |
|----------|------|--------------|-------------|
| resource | instance_type | $XX.XX | $XXX.XX |
| **TOTAL** | | **$XX.XX** | **$XXX.XX** |

- Cost optimization opportunities
- Right-sizing recommendations
- Budget status: {json.dumps(budget_status, indent=2) if budget_status else "No budgets configured"}

### 8. Best Practices Assessment
| Category | Practice | Status | Notes |
|----------|----------|--------|-------|
| High Availability | Multiple nodes/zones | Yes/No | Details |
| Disaster Recovery | Backup configured | Yes/No | Details |
| Monitoring | Logging enabled | Yes/No | Details |
| Tagging | Resources tagged | Yes/No | Details |

### 9. Recommendations
Prioritized list with:
1. **Critical** - Security/compliance issues
2. **High** - Performance/reliability improvements
3. **Medium** - Best practice alignment
4. **Low** - Nice-to-have optimizations

For each recommendation:
- Description
- Implementation approach
- Example code/config if helpful
- Expected impact

### 10. Development Continuity
Help developers continue working:
- What to add next (common extensions)
- Missing configurations to consider
- Integration points with other services

## FORMATTING GUIDELINES:
- Use tables for all structured data
- Use Mermaid diagrams for architecture
- Use code blocks with appropriate language tags
- NO emojis - professional language only
- Be specific - reference actual values from the file

Return JSON:
{{
    "summary": "2-3 sentence professional summary covering all resources",
    "markdown": "Full markdown analysis document",
    "security": {{
        "overall_score": "Good/Fair/Poor",
        "strengths": ["list of security strengths"],
        "concerns": ["list of security concerns with severity"],
        "recommendations": ["prioritized security recommendations"]
    }}
}}
"""

        try:
            async def call_llm():
                async with asyncio.timeout(self.llm_timeout_seconds):
                    return await self.llm_client.messages.create(
                        model=self.model,
                        max_tokens=self.max_tokens,
                        temperature=self.temperature,
                        messages=[{"role": "user", "content": prompt}],
                    )

            response = await with_retry(
                call_llm,
                max_attempts=3,
                initial_delay=1.0,
                max_delay=10.0,
                backoff_multiplier=2.0,
                retryable_exceptions=(TimeoutError, ConnectionError, RuntimeError),
            )

            response_text = response.content[0].text if response.content else ""

            if not response_text:
                logger.warning("Empty response from LLM for holistic analysis")
                return self._fallback_holistic_analysis(
                    file_path, file_content, extracted_resources, compliance_data, cost_data
                )

            try:
                # Try to parse JSON
                result = json.loads(response_text)
                return result
            except json.JSONDecodeError:
                # Try to extract JSON from response
                json_match = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                if json_match >= 0 and json_end > json_match:
                    try:
                        result = json.loads(response_text[json_match:json_end])
                        return result
                    except json.JSONDecodeError:
                        pass
                logger.warning("Failed to parse LLM response as JSON for holistic analysis")
                return self._fallback_holistic_analysis(
                    file_path, file_content, extracted_resources, compliance_data, cost_data
                )

        except AsyncTimeoutError:
            logger.error("LLM call timed out for holistic analysis")
            return self._fallback_holistic_analysis(
                file_path, file_content, extracted_resources, compliance_data, cost_data
            )
        except Exception as e:
            logger.error("Error generating holistic analysis: %s", e, exc_info=True)
            return self._fallback_holistic_analysis(
                file_path, file_content, extracted_resources, compliance_data, cost_data
            )

    def _fallback_holistic_analysis(
        self,
        file_path: Path,
        file_content: str,
        extracted_resources: dict[str, Any],
        compliance_data: dict[str, Any],
        cost_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Generate fallback holistic analysis when LLM is unavailable."""
        file_type = self._detect_file_type(file_path, file_content)
        resources = extracted_resources.get("resources", [])
        resource_types = extracted_resources.get("resource_types", [])
        cloud_providers = extracted_resources.get("cloud_providers", ["Unknown"])

        summary = (
            f"Infrastructure file containing {len(resources)} {cloud_providers[0]} resources "
            f"including {', '.join(resource_types[:3])}. "
            f"Estimated monthly cost: ${cost_data.get('total_monthly', 0):.2f}."
        )

        # Build resource inventory table
        resource_table = "| Resource | Type | Cloud |\n|----------|------|-------|\n"
        for res in resources:
            resource_table += f"| {res.get('name', 'unnamed')} | {res.get('type', 'unknown')} | {res.get('cloud', 'unknown')} |\n"

        # Build cost table
        cost_table = "| Resource | Monthly Cost |\n|----------|-------------|\n"
        for item in cost_data.get("breakdown", []):
            cost_table += f"| {item.get('resource', 'unknown')} | ${item.get('monthly', 0):.2f} |\n"
        cost_table += f"| **Total** | **${cost_data.get('total_monthly', 0):.2f}** |\n"

        # Build compliance table
        compliance_table = "| Control | Standard | Severity |\n|---------|----------|----------|\n"
        for ctrl in compliance_data.get("controls", [])[:10]:
            compliance_table += f"| {ctrl.get('control_id', 'N/A')} | {ctrl.get('standard', 'N/A')} | {ctrl.get('severity', 'N/A')} |\n"

        markdown = f"""# {file_path.name}

## Infrastructure Overview

**Type:** {file_type}
**Cloud Providers:** {', '.join(cloud_providers)}
**Total Resources:** {len(resources)}

{summary}

## Resource Inventory

{resource_table}

## Cost Analysis

{cost_table}

**Annual Estimate:** ${cost_data.get('total_annual', 0):.2f}

## Compliance Requirements

{compliance_table}

## Security Considerations

Review the following for {file_type} deployments:
- Authentication and authorization configuration
- Network security and access controls
- Encryption for data at rest and in transit
- Secret management practices
- Logging and monitoring

## Recommendations

1. Review resource configurations against cloud provider best practices
2. Implement proper tagging strategy for cost allocation
3. Enable monitoring and alerting
4. Document infrastructure dependencies
5. Set up automated compliance scanning
"""

        return {
            "summary": summary,
            "markdown": markdown,
            "security": {
                "overall_score": "Review Required",
                "strengths": [],
                "concerns": ["Manual security review recommended"],
                "recommendations": ["Complete security assessment with LLM analysis"],
            },
        }

    @track_tool_metrics(tool_name="code_analyzer.analyze_component")
    async def analyze_component(
        self,
        file_path: Path,
        file_content: str,
        component_info: dict[str, Any],
        repo_context: dict[str, Any],
    ) -> KnowledgeArticle:
        """Analyze a single infrastructure component and generate analysis document.

        Args:
            file_path: File path
            file_content: Full file content
            component_info: Component information (name, type, start_line, end_line)
            repo_context: Repository context (repo_url, branch, commit_sha, resource_id, user_id)

        Returns:
            KnowledgeArticle with component analysis

        Raises:
            ValueError: If validation fails
        """
        self._validate_component_info(component_info)
        self._validate_repo_context(repo_context)
        
        component_content = self._extract_component_content(
            file_content,
            component_info["start_line"],
            component_info["end_line"],
        )
        
        extracted_resources = await self.extract_resources(
            file_path,
            component_content,
        )
        
        component_resource_types = [component_info.get("type", "Unknown")]
        if extracted_resources.get("resource_types"):
            component_resource_types.extend(extracted_resources["resource_types"])
        
        compliance_data = await self.get_compliance_for_resources(
            resource_types=component_resource_types,
            standards=repo_context.get("compliance_standards") or [],
        )
        
        cost_data = await self.calculate_costs_for_resources(
            resources=extracted_resources.get("resource_specs", []),
            track_missing=True,
        )

        budget_status = None
        if cost_data.get("total_monthly", 0) > 0:
            try:
                from api.services.budget_service import budget_service
                
                budget_status = await budget_service.check_budgets(
                    user_id=repo_context["user_id"],
                    estimated_cost=cost_data["total_monthly"],
                    scope={
                        "cloud_providers": extracted_resources.get("cloud_providers", []),
                        "project_id": repo_context.get("project_id"),
                    },
                )
            except Exception as e:
                logger.warning("Failed to check budgets: %s", e, exc_info=True)
        
        file_size_mb = len(file_content.encode("utf-8")) / (1024 * 1024)
        if file_size_mb > self.max_file_size_mb:
            raise ValueError(
                f"File too large: {file_size_mb:.2f} MB (max: {self.max_file_size_mb} MB)"
            )
        
        if len(file_content) > self.max_content_length:
            logger.warning(
                "File content truncated: %s (%d chars > %d)",
                file_path,
                len(file_content),
                self.max_content_length,
            )
            file_content = file_content[:self.max_content_length]
        
        if len(component_content) > self.max_component_content_length:
            logger.warning(
                "Component content truncated: %s (%d chars > %d)",
                component_info.get("name"),
                len(component_content),
                self.max_component_content_length,
            )
            component_content = component_content[:self.max_component_content_length]

        analysis = await self._generate_component_analysis(
            file_path=file_path,
            file_content=file_content,
            component_content=component_content,
            component_info=component_info,
            repo_context=repo_context,
            extracted_resources=extracted_resources,
            compliance_data=compliance_data,
            cost_data=cost_data,
            budget_status=budget_status,
        )
        
        if file_path.is_absolute():
            relative_path = file_path.relative_to(Path(repo_context.get("repo_path", "")))
        else:
            relative_path = file_path
        
        urls = await self.generate_source_urls(
            repo_url=repo_context["repo_url"],
            branch=repo_context["branch"],
            commit_sha=repo_context["commit_sha"],
            relative_path=relative_path,
            start_line=component_info["start_line"],
            end_line=component_info["end_line"],
        )
        
        file_hash = self.calculate_file_hash(file_content)

        if cost_data.get("total_monthly", 0) > 0:
            try:
                from api.services.budget_service import budget_service
                
                await budget_service.record_spending(
                    user_id=repo_context["user_id"],
                    amount_usd=cost_data["total_monthly"],
                    source_type="repository-analysis",
                    source_id=repo_context["resource_id"],
                    component_id=None,
                    cloud_provider=extracted_resources.get("cloud_providers", [None])[0],
                    project_id=repo_context.get("project_id"),
                    service=extracted_resources.get("services", [None])[0],
                    resource_type=extracted_resources.get("resource_types", [None])[0],
                    resource_spec=extracted_resources.get("resource_specs", [None])[0],
                )
            except Exception as e:
                logger.warning("Failed to record spending: %s", e, exc_info=True)

        analysis_markdown = analysis.get("markdown", "")

        if self._detect_excessive_code_copying(analysis_markdown, component_content):
            logger.warning(
                "Excessive code copying detected in analysis for component %s, sanitizing",
                component_info.get("name"),
            )
            analysis_markdown = self._sanitize_analysis_content(
                analysis_markdown,
                component_content,
                urls["snapshot_url"],
            )
            analysis["markdown"] = analysis_markdown
        
        domain = self._detect_domain(file_path, component_content)
        content_type = ContentType.REFERENCE
        
        article_id = f"repo_{repo_context['resource_id']}_{file_path.stem}_{component_info.get('name', 'component')}_{hash(str(file_path) + str(component_info['start_line'])) % 100000}"
        
        summary = analysis.get("summary", "")
        if len(summary) < 50:
            component_name = component_info.get('name', 'Component')
            component_type = component_info.get('type', 'Component')
            summary = f"Infrastructure component analysis for {component_name} ({component_type}). {summary}".strip()
            if len(summary) < 50:
                summary = f"This is a {component_type} component named {component_name} in the infrastructure repository. It defines the configuration and deployment settings for this component."
        
        article = KnowledgeArticle(
            article_id=article_id,
            domain=domain,
            subdomain="infrastructure-analysis",
            content_type=content_type,
            title=f"{component_info.get('name', 'Component')} - {file_path.name}",
            summary=summary,
            content=analysis_markdown,
            source_url=urls["snapshot_url"],
            source_urls=urls,
            commit_sha=repo_context["commit_sha"],
            branch=repo_context["branch"],
            analyzed_at=datetime.utcnow(),
            source_hash=file_hash,
            user_id=repo_context["user_id"],
            visibility="user",
            source_type="repository-analysis",
            resource_id=repo_context["resource_id"],
            structured_data={
                "component_name": component_info.get("name"),
                "component_type": component_info.get("type"),
                "file_path": str(file_path),
                "start_line": component_info["start_line"],
                "end_line": component_info["end_line"],
                "resources": extracted_resources.get("resources", []),
                "budget_status": budget_status,
            },
            compliance_impact=compliance_data,
            cost_impact=cost_data,
            security_impact=analysis.get("security", {}),
            tags=[file_path.suffix[1:] if file_path.suffix else "code"],
            cloud_providers=extracted_resources.get("cloud_providers", []),
            services=extracted_resources.get("services", []),
        )
        
        try:
            from api.services.context_generator import context_generator
            
            contextual_description = await context_generator.generate_context(
                article=article,
                repo_context=repo_context,
            )
            
            article.contextual_description = contextual_description
            article.context_generated_at = datetime.utcnow()
            article.context_version = "1.0"
        except Exception as e:
            logger.warning(
                "Failed to generate contextual description for article %s: %s",
                article_id,
                e,
                exc_info=True,
            )
        
        return article

    def _extract_component_content(
        self,
        file_content: str,
        start_line: int,
        end_line: int,
    ) -> str:
        """Extract component content from file.
        
        Args:
            file_content: Full file content
            start_line: Start line number (1-indexed)
            end_line: End line number (1-indexed)
            
        Returns:
            Component content string
        """
        lines = file_content.split("\n")
        if start_line < 1:
            start_line = 1
        if end_line > len(lines):
            end_line = len(lines)
        
        return "\n".join(lines[start_line - 1 : end_line])

    async def _generate_component_analysis(
        self,
        file_path: Path,
        file_content: str,
        component_content: str,
        component_info: dict[str, Any],
        repo_context: dict[str, Any],
        extracted_resources: dict[str, Any],
        compliance_data: dict[str, Any],
        cost_data: dict[str, Any],
        budget_status: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Generate component analysis using Claude Opus.
        
        Args:
            file_path: File path
            file_content: Full file content
            component_content: Component-specific content
            component_info: Component information
            repo_context: Repository context
            extracted_resources: Extracted resources
            compliance_data: Compliance data from tool
            cost_data: Cost data from tool
            budget_status: Budget status (optional)
            
        Returns:
            Dictionary with analysis (summary, markdown, security)
        """
        if not self.llm_client:
            logger.warning("LLM client not available, using fallback analysis")
            return self._fallback_analysis(component_info, compliance_data, cost_data)
        
        file_type = self._detect_file_type(file_path, component_content)
        
        prompt = f"""You are an expert infrastructure analyst. Analyze this infrastructure component and generate a comprehensive, professional analysis document.

File: {file_path}
Component: {component_info.get('name', 'Unknown')}
Type: {component_info.get('type', 'Unknown')}
File Type: {file_type}
Lines: {component_info['start_line']}-{component_info['end_line']}

Component Content:
{component_content[:20000]}

Extracted Resources:
{json.dumps(extracted_resources, indent=2)}

Compliance Requirements (from WISTX compliance database):
{json.dumps(compliance_data, indent=2)}

Cost Analysis (from WISTX pricing database):
{json.dumps(cost_data, indent=2)}

Generate a detailed, professional analysis document. Your output should be rich and comprehensive, utilizing all appropriate markdown features.

## CONTENT REQUIREMENTS:

### 1. Component Overview
- Brief description of what this component does
- Architecture context and purpose

### 2. Configuration Analysis
- Key configuration details with explanations
- Include RELEVANT CODE SNIPPETS where they help illustrate:
  - Important configuration patterns found in the component
  - Key resource definitions
  - Critical settings that affect behavior
- Format code blocks with appropriate language tags (```yaml, ```terraform, ```json, etc.)

### 3. Compliance Mapping
Use compliance_data provided above. Present as a TABLE:
| Control | Status | Finding |
|---------|--------|---------|
| SOC2-XX | Compliant/Partial/Non-Compliant | Details |

### 4. Cost Analysis
Use cost_data provided above. Include:
- Cost breakdown TABLE:
| Resource | Type | Monthly Cost |
|----------|------|--------------|
| resource_name | instance_type | $XX.XX |

- Total monthly cost
- Cost optimization opportunities
- Budget status: {json.dumps(budget_status, indent=2) if budget_status else "No budgets configured"}

### 5. Architecture Diagram (if applicable)
Include a Mermaid diagram showing component relationships:
```mermaid
graph TD
    A[Component] --> B[Dependency]
```

### 6. Security Posture
- Security strengths (list with explanations)
- Security concerns (list with severity)
- Recommendations with priority

### 7. Best Practices Assessment
Present as a checklist TABLE:
| Practice | Status | Notes |
|----------|--------|-------|
| Resource limits defined | Yes/No/Partial | Details |

### 8. Recommendations
Prioritized list of improvements with:
- Implementation code snippets showing BEST PRACTICE patterns (not copying user code)
- Expected impact
- Effort estimate

## FORMATTING GUIDELINES:
- Use tables for structured comparisons and data
- Use code blocks with language tags for all code/config snippets
- Use Mermaid diagrams for architecture visualization
- Use task lists (- [ ] / - [x]) for checklists
- Use blockquotes for important notes
- Use headers (##, ###) for clear section organization
- DO NOT use emojis - use professional language only

## CODE SNIPPET POLICY:
- You MAY include code snippets that illustrate:
  - Key configurations FROM the analyzed component (properly formatted)
  - Best practice examples showing recommended patterns
  - Comparison snippets showing current vs recommended approach
- Format all code with appropriate syntax highlighting (```yaml, ```python, ```terraform, etc.)
- Keep snippets concise and relevant

## DATA USAGE:
- Use compliance_data provided (from WISTX compliance tool) - do not generate generic compliance info
- Use cost_data provided (from WISTX pricing tool) - do not estimate costs manually
- Reference specific controls, costs, and findings from the provided data

Return JSON:
{{
    "summary": "Brief 2-3 sentence professional summary",
    "markdown": "Full markdown analysis document with tables, code snippets, and diagrams as appropriate",
    "security": {{
        "strengths": ["strength1", "strength2"],
        "concerns": ["concern1", "concern2"],
        "recommendations": ["recommendation1", "recommendation2"]
    }}
}}
"""
        
        try:
            async def call_llm():
                async with asyncio.timeout(self.llm_timeout_seconds):
                    return await self.llm_client.messages.create(
                        model=self.model,
                        max_tokens=self.max_tokens,
                        temperature=self.temperature,
                        messages=[{"role": "user", "content": prompt}],
                    )
            
            response = await with_retry(
                call_llm,
                max_attempts=3,
                initial_delay=1.0,
                max_delay=10.0,
                backoff_multiplier=2.0,
                retryable_exceptions=(TimeoutError, ConnectionError, RuntimeError),
            )
            
            response_text = response.content[0].text if response.content else ""
            
            if not response_text:
                logger.warning("Empty response from LLM for component analysis")
                return self._fallback_analysis(component_info, compliance_data, cost_data)
            
            try:
                result = json.loads(response_text)
                return result
            except json.JSONDecodeError as e:
                logger.warning("Failed to parse LLM response as JSON: %s", e)
                return self._fallback_analysis(component_info, compliance_data, cost_data)
                
        except AsyncTimeoutError:
            logger.error("LLM call timed out after %.1f seconds", self.llm_timeout_seconds)
            return self._fallback_analysis(component_info, compliance_data, cost_data)
        except Exception as e:
            logger.error("Error generating component analysis: %s", e, exc_info=True)
            return self._fallback_analysis(component_info, compliance_data, cost_data)

    def _fallback_analysis(
        self,
        component_info: dict[str, Any],
        compliance_data: dict[str, Any],
        cost_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Generate detailed analysis when LLM is unavailable.

        Provides meaningful, structured analysis based on component metadata,
        best practices for the resource type, and available compliance/cost data.

        Args:
            component_info: Component information including name, type, content
            compliance_data: Compliance data (may contain errors)
            cost_data: Cost data (may be empty for abstract resources)

        Returns:
            Structured analysis dictionary with summary, markdown, and security
        """
        comp_name = component_info.get('name', 'Unknown Component')
        comp_type = component_info.get('type', 'Unknown')
        content = component_info.get('content', '')

        # Generate intelligent summary based on component type
        summary = self._generate_component_summary(comp_name, comp_type, content)

        # Build comprehensive markdown analysis
        markdown = self._build_analysis_markdown(
            comp_name, comp_type, content, compliance_data, cost_data
        )

        # Generate security insights based on component type
        security = self._generate_security_insights(comp_type, content)

        return {
            "summary": summary,
            "markdown": markdown,
            "security": security,
        }

    def _generate_component_summary(
        self, name: str, comp_type: str, content: str
    ) -> str:
        """Generate an intelligent summary for the component."""
        type_descriptions = {
            "Deployment": "Kubernetes Deployment managing containerized application workloads with declarative updates and self-healing capabilities",
            "StatefulSet": "Kubernetes StatefulSet managing stateful applications with persistent storage and ordered deployment",
            "DaemonSet": "Kubernetes DaemonSet ensuring pod instances run on all (or selected) cluster nodes",
            "Service": "Kubernetes Service providing stable network endpoint and load balancing for pod workloads",
            "Ingress": "Kubernetes Ingress managing external HTTP/S access to services with routing rules",
            "ConfigMap": "Kubernetes ConfigMap storing non-confidential configuration data as key-value pairs",
            "Secret": "Kubernetes Secret storing sensitive data like passwords, tokens, and certificates",
            "Application": "ArgoCD Application defining the desired state of a Kubernetes application for GitOps deployment",
            "AppProject": "ArgoCD AppProject defining RBAC and resource restrictions for applications",
            "HelmRelease": "Helm Release managing the lifecycle of a Helm chart deployment",
            "Pipeline": "CI/CD Pipeline defining automated build, test, and deployment workflows",
            "Dockerfile": "Docker image definition specifying container build instructions",
            "Terraform": "Terraform Infrastructure as Code defining cloud resources declaratively",
        }

        base_desc = type_descriptions.get(comp_type, f"{comp_type} infrastructure component")
        return f"{name}: {base_desc}"

    def _build_analysis_markdown(
        self,
        name: str,
        comp_type: str,
        content: str,
        compliance_data: dict[str, Any],
        cost_data: dict[str, Any],
    ) -> str:
        """Build comprehensive markdown analysis document."""
        markdown = f"""# {name}

## Component Overview

**Type:** {comp_type}
**Category:** {self._get_component_category(comp_type)}

{self._generate_component_summary(name, comp_type, content)}

## Configuration Analysis

{self._analyze_configuration(comp_type, content)}

## Best Practices Assessment

{self._generate_best_practices(comp_type, content)}

## Compliance Considerations

{self._format_compliance_section(compliance_data, comp_type)}

## Cost Analysis

{self._format_cost_section(cost_data, comp_type)}

## Recommendations

{self._generate_recommendations(comp_type, content)}
"""
        return markdown

    def _get_component_category(self, comp_type: str) -> str:
        """Get the category for a component type."""
        categories = {
            "Deployment": "Kubernetes Workloads",
            "StatefulSet": "Kubernetes Workloads",
            "DaemonSet": "Kubernetes Workloads",
            "ReplicaSet": "Kubernetes Workloads",
            "Pod": "Kubernetes Workloads",
            "Job": "Kubernetes Workloads",
            "CronJob": "Kubernetes Workloads",
            "Service": "Kubernetes Networking",
            "Ingress": "Kubernetes Networking",
            "NetworkPolicy": "Kubernetes Networking",
            "ConfigMap": "Kubernetes Configuration",
            "Secret": "Kubernetes Configuration",
            "PersistentVolumeClaim": "Kubernetes Storage",
            "StorageClass": "Kubernetes Storage",
            "ServiceAccount": "Kubernetes RBAC",
            "Role": "Kubernetes RBAC",
            "RoleBinding": "Kubernetes RBAC",
            "ClusterRole": "Kubernetes RBAC",
            "Application": "ArgoCD GitOps",
            "AppProject": "ArgoCD GitOps",
            "HelmRelease": "Helm Package Management",
            "Pipeline": "CI/CD Automation",
            "Dockerfile": "Container Build",
            "Terraform": "Infrastructure as Code",
        }
        return categories.get(comp_type, "Infrastructure")

    def _analyze_configuration(self, comp_type: str, content: str) -> str:
        """Analyze configuration without exposing raw code."""
        analysis_points = []
        content_lower = content.lower()

        # Kubernetes-specific analysis
        if comp_type in ["Deployment", "StatefulSet", "DaemonSet"]:
            if "replicas:" in content_lower:
                analysis_points.append("• **Replicas:** Replica count is configured for availability")
            if "resources:" in content_lower:
                analysis_points.append("• **Resource Management:** CPU/memory limits are defined")
            if "livenessprobe:" in content_lower or "readinessprobe:" in content_lower:
                analysis_points.append("• **Health Checks:** Liveness/readiness probes configured")
            if "securitycontext:" in content_lower:
                analysis_points.append("• **Security Context:** Pod security settings defined")
            if "serviceaccountname:" in content_lower:
                analysis_points.append("• **Service Account:** Custom service account assigned")

        elif comp_type == "Service":
            if "type: loadbalancer" in content_lower:
                analysis_points.append("• **Type:** LoadBalancer - externally accessible via cloud LB")
            elif "type: nodeport" in content_lower:
                analysis_points.append("• **Type:** NodePort - accessible on each node's IP")
            elif "type: clusterip" in content_lower or "type:" not in content_lower:
                analysis_points.append("• **Type:** ClusterIP - internal cluster access only")

        elif comp_type == "Ingress":
            if "tls:" in content_lower:
                analysis_points.append("• **TLS:** HTTPS/TLS termination configured")
            if "annotations:" in content_lower:
                analysis_points.append("• **Annotations:** Custom ingress controller settings defined")

        elif comp_type == "Application":
            if "syncpolicy:" in content_lower:
                analysis_points.append("• **Sync Policy:** Automated sync configuration present")
            if "automated:" in content_lower:
                analysis_points.append("• **Automation:** Auto-sync and/or auto-prune enabled")

        elif comp_type in ["Dockerfile", "Docker"]:
            if "from" in content_lower:
                analysis_points.append("• **Base Image:** Container base image specified")
            if "healthcheck" in content_lower:
                analysis_points.append("• **Health Check:** Container health check configured")
            if "user" in content_lower:
                analysis_points.append("• **Non-root User:** Security best practice may be followed")

        if not analysis_points:
            analysis_points.append(f"• Standard {comp_type} configuration detected")
            analysis_points.append("• Review configuration for organization-specific requirements")

        return "\n".join(analysis_points)

    def _generate_best_practices(self, comp_type: str, content: str) -> str:
        """Generate best practices assessment as a table."""
        content_lower = content.lower()
        practices = []

        if comp_type in ["Deployment", "StatefulSet", "DaemonSet"]:
            # Check for resource limits
            if "limits:" in content_lower and "requests:" in content_lower:
                practices.append(("Resource Limits", "Compliant", "Both requests and limits defined"))
            elif "resources:" in content_lower:
                practices.append(("Resource Limits", "Partial", "Ensure both requests and limits are set"))
            else:
                practices.append(("Resource Limits", "Missing", "Add CPU/memory limits for stability"))

            # Check for health probes
            has_liveness = "livenessprobe:" in content_lower
            has_readiness = "readinessprobe:" in content_lower
            if has_liveness and has_readiness:
                practices.append(("Health Probes", "Compliant", "Both liveness and readiness probes configured"))
            elif has_liveness or has_readiness:
                practices.append(("Health Probes", "Partial", "Add both probe types"))
            else:
                practices.append(("Health Probes", "Missing", "Add for improved reliability"))

            # Check for PDB
            if "poddisruptionbudget" in content_lower:
                practices.append(("Pod Disruption Budget", "Compliant", "Configured for high availability"))
            else:
                practices.append(("Pod Disruption Budget", "Recommended", "Consider adding for production workloads"))

            # Check for security context
            if "securitycontext:" in content_lower:
                practices.append(("Security Context", "Compliant", "Pod security settings defined"))
            else:
                practices.append(("Security Context", "Missing", "Add securityContext for hardening"))

        elif comp_type == "Secret":
            practices.append(("Secret Management", "Review", "Consider external secrets operator or sealed secrets"))
            practices.append(("Secret Rotation", "Recommended", "Implement secret rotation policy"))

        elif comp_type == "Ingress":
            if "tls:" in content_lower:
                practices.append(("TLS Configuration", "Compliant", "HTTPS traffic supported"))
            else:
                practices.append(("TLS Configuration", "Missing", "Enable TLS for secure communication"))

        elif comp_type == "Application":
            if "syncpolicy:" in content_lower and "automated:" in content_lower:
                practices.append(("GitOps Automation", "Compliant", "Auto-sync enabled for continuous deployment"))
            else:
                practices.append(("GitOps Automation", "Recommended", "Consider enabling auto-sync for CD"))

        if not practices:
            practices.append((f"{comp_type} Standards", "Review", "Review against organizational standards"))
            practices.append(("Compliance", "Review", "Ensure alignment with security requirements"))

        # Format as table
        lines = ["| Practice | Status | Notes |", "|----------|--------|-------|"]
        for practice, status, notes in practices:
            status_icon = {"Compliant": "Compliant", "Partial": "Partial", "Missing": "Missing", "Recommended": "Recommended", "Review": "Review"}.get(status, status)
            lines.append(f"| {practice} | {status_icon} | {notes} |")

        return "\n".join(lines)

    def _format_compliance_section(
        self, compliance_data: dict[str, Any], comp_type: str
    ) -> str:
        """Format compliance section with tables, handling errors gracefully."""
        # Check for error in compliance data
        if compliance_data.get("error"):
            return f"""**Status:** Compliance mapping in progress

| Consideration | Requirement |
|---------------|-------------|
| Access Control | Ensure proper RBAC and authentication |
| Data Protection | Encrypt sensitive data at rest and in transit |
| Audit Logging | Enable comprehensive audit trails |
| Change Management | Follow change control procedures |

> For detailed compliance mapping for {comp_type}, contact your compliance team."""

        controls = compliance_data.get("controls", [])
        if controls:
            summary = compliance_data.get("summary", {})
            by_standard = summary.get("by_standard", {})

            lines = [f"**{len(controls)} compliance controls identified**\n"]

            # Format as table if we have standards breakdown
            if by_standard:
                lines.append("| Standard | Controls |")
                lines.append("|----------|----------|")
                for standard, count in by_standard.items():
                    lines.append(f"| {standard} | {count} |")
                lines.append("")

            # Show first few controls as a table
            if len(controls) > 0:
                lines.append("### Key Controls\n")
                lines.append("| Control ID | Description | Status |")
                lines.append("|------------|-------------|--------|")
                for ctrl in controls[:5]:  # Show first 5 controls
                    ctrl_id = ctrl.get("control_id", "N/A")
                    desc = ctrl.get("description", "No description")[:50]
                    status = ctrl.get("status", "Review Required")
                    lines.append(f"| {ctrl_id} | {desc}... | {status} |")

            return "\n".join(lines)

        return f"""**Status:** No specific compliance controls mapped

| Guidance | Description |
|----------|-------------|
| Access Control | Follow least privilege access principles |
| Encryption | Enable encryption for sensitive data |
| Audit Logging | Maintain audit logs for all changes |
| Documentation | Document security configurations |

> Review {comp_type} against organizational compliance requirements."""

    def _format_cost_section(
        self, cost_data: dict[str, Any], comp_type: str
    ) -> str:
        """Format cost section with tables, handling abstract resources gracefully."""
        total = cost_data.get("total_monthly", 0)

        if total > 0:
            breakdown = cost_data.get("breakdown", {})
            lines = [f"**Estimated Monthly Cost:** ${total:.2f}\n"]

            if breakdown:
                lines.append("### Cost Breakdown\n")
                lines.append("| Resource | Monthly Cost |")
                lines.append("|----------|--------------|")
                for item, cost in breakdown.items():
                    lines.append(f"| {item} | ${cost:.2f} |")
                lines.append(f"| **Total** | **${total:.2f}** |")
                lines.append("")

            optimizations = cost_data.get("optimizations", [])
            if optimizations:
                lines.append("### Optimization Opportunities\n")
                lines.append("| Recommendation | Potential Savings |")
                lines.append("|----------------|-------------------|")
                for opt in optimizations[:3]:
                    lines.append(f"| {opt} | Review required |")

            return "\n".join(lines)

        # Handle abstract Kubernetes resources
        abstract_types = {
            "Deployment", "StatefulSet", "DaemonSet", "ReplicaSet", "Pod",
            "Service", "Ingress", "ConfigMap", "Secret", "Application",
            "HelmRelease", "Pipeline"
        }

        if comp_type in abstract_types:
            return f"""**Status:** Indirect cost component

{comp_type} resources don't have direct cloud costs but influence overall infrastructure costs:

| Cost Factor | Impact |
|-------------|--------|
| Compute | Pod resource requests affect node sizing and cluster costs |
| Networking | Service type and ingress configuration impact network costs |
| Storage | PVC requests and storage class selection affect storage costs |

> For accurate cost analysis, review associated cloud resources and cluster costs."""

        return "Cost estimation not available for this resource type."

    def _generate_security_insights(
        self, comp_type: str, content: str
    ) -> dict[str, list[str]]:
        """Generate security insights based on component type and content."""
        content_lower = content.lower()
        strengths = []
        concerns = []
        recommendations = []

        # Kubernetes workload security
        if comp_type in ["Deployment", "StatefulSet", "DaemonSet", "Pod"]:
            if "securitycontext:" in content_lower:
                strengths.append("Security context configured for pod/container security")
            else:
                concerns.append("No security context defined")
                recommendations.append("Add securityContext with runAsNonRoot: true")

            if "runasnonroot: true" in content_lower:
                strengths.append("Configured to run as non-root user")
            elif "runasuser:" in content_lower:
                strengths.append("Specific user ID configured")
            else:
                recommendations.append("Configure runAsNonRoot: true for security")

            if "readonlyrootfilesystem: true" in content_lower:
                strengths.append("Read-only root filesystem enabled")
            else:
                recommendations.append("Consider setting readOnlyRootFilesystem: true")

        elif comp_type == "Secret":
            concerns.append("Secrets stored in cluster - consider external secret management")
            recommendations.append("Use external-secrets-operator or sealed-secrets")
            recommendations.append("Implement secret rotation policy")

        elif comp_type == "Service":
            if "type: loadbalancer" in content_lower:
                concerns.append("LoadBalancer type exposes service externally")
                recommendations.append("Ensure proper network security groups/firewall rules")

        elif comp_type == "Ingress":
            if "tls:" in content_lower:
                strengths.append("TLS encryption enabled")
            else:
                concerns.append("No TLS configuration - traffic may be unencrypted")
                recommendations.append("Enable TLS with valid certificates")

        elif comp_type == "Application":
            if "allowempty: true" in content_lower:
                concerns.append("AllowEmpty enabled - could delete all resources")
                recommendations.append("Review prune settings for safety")
            strengths.append("GitOps deployment provides audit trail")

        # Generic recommendations if none specific
        if not recommendations:
            recommendations.append("Review against security benchmarks (CIS, NIST)")
            recommendations.append("Ensure proper RBAC configuration")

        return {
            "strengths": strengths if strengths else ["Standard security configuration"],
            "concerns": concerns if concerns else [],
            "recommendations": recommendations,
        }

    def _generate_recommendations(self, comp_type: str, content: str) -> str:
        """Generate actionable recommendations."""
        content_lower = content.lower()
        recs = []

        if comp_type in ["Deployment", "StatefulSet", "DaemonSet"]:
            if "replicas: 1" in content_lower or "replicas:" not in content_lower:
                recs.append("1. **High Availability:** Consider running multiple replicas for production")
            if "poddisruptionbudget" not in content_lower:
                recs.append("2. **Resilience:** Add PodDisruptionBudget to ensure availability during updates")
            if "topologyspreadconstraints:" not in content_lower:
                recs.append("3. **Distribution:** Consider topology spread constraints for zone redundancy")

        elif comp_type == "Service":
            recs.append("1. **Monitoring:** Set up service-level monitoring and alerting")
            recs.append("2. **Documentation:** Document service dependencies and SLAs")

        elif comp_type == "Application":
            recs.append("1. **Sync Windows:** Consider sync windows for production deployments")
            recs.append("2. **Notifications:** Configure notifications for sync failures")
            recs.append("3. **Health Checks:** Add application health checks in ArgoCD")

        if not recs:
            recs.append(f"1. Review {comp_type} configuration against team standards")
            recs.append("2. Ensure proper monitoring and alerting is configured")
            recs.append("3. Document any custom configurations or dependencies")

        return "\n".join(recs)

    def _detect_file_type(
        self,
        file_path: Path,
        content: str,
    ) -> str:
        """Detect file type from path and content.
        
        Args:
            file_path: File path
            content: File content
            
        Returns:
            File type string
        """
        suffix = file_path.suffix.lower()
        content_lower = content.lower()
        
        if suffix == ".tf" or suffix == ".tfvars" or suffix == ".hcl":
            return "Terraform"
        elif suffix in [".yaml", ".yml"]:
            if "apiVersion:" in content_lower and "kind:" in content_lower:
                return "Kubernetes"
            elif "AWSTemplateFormatVersion" in content_lower:
                return "CloudFormation"
            elif "serverless:" in content_lower:
                return "Serverless Framework"
            else:
                return "YAML Configuration"
        elif file_path.name.lower() == "dockerfile":
            return "Docker"
        elif file_path.name.lower() in ["docker-compose.yml", "docker-compose.yaml"]:
            return "Docker Compose"
        elif ".github/workflows" in str(file_path):
            return "GitHub Actions"
        elif file_path.name.lower() == ".gitlab-ci.yml":
            return "GitLab CI"
        elif file_path.name.lower() == "jenkinsfile":
            return "Jenkins"
        else:
            return "Infrastructure Configuration"

    def _detect_domain(
        self,
        file_path: Path,
        content: str,
    ) -> Domain:
        """Detect domain from file path and content.
        
        Args:
            file_path: File path
            content: File content
            
        Returns:
            Domain enum
        """
        path_str = str(file_path).lower()
        content_lower = content.lower()
        
        if "terraform" in path_str or file_path.suffix == ".tf":
            return Domain.INFRASTRUCTURE
        if "kubernetes" in path_str or "k8s" in path_str or ("apiVersion:" in content_lower and "kind:" in content_lower):
            return Domain.DEVOPS
        if "security" in path_str or "auth" in path_str:
            return Domain.SECURITY
        if "cost" in path_str or "billing" in path_str:
            return Domain.FINOPS
        if "compliance" in content_lower or "pci" in content_lower or "hipaa" in content_lower:
            return Domain.COMPLIANCE
        
        return Domain.DEVOPS

    @track_tool_metrics(tool_name="code_analyzer.extract_components")
    async def extract_components_from_file(
        self,
        file_path: Path,
        file_content: str,
    ) -> list[dict[str, Any]]:
        """Extract components from infrastructure file.
        
        Uses LLM to identify individual components/resources within a file.
        
        Args:
            file_path: File path
            file_content: File content
            
        Returns:
            List of component dictionaries with name, type, start_line, end_line
        """
        if not self.llm_client:
            logger.warning("LLM client not available, using fallback component extraction")
            return self._fallback_extract_components(file_path, file_content)
        
        prompt = f"""Extract individual infrastructure components/resources from this {file_path.suffix} file.

File: {file_path}
Content:
{file_content[:50000]}

For each component/resource, identify:
1. Component name/identifier
2. Component type (e.g., "aws_instance", "Kubernetes Deployment", "Docker container")
3. Start line number
4. End line number

Return JSON:
{{
    "components": [
        {{
            "name": "web_server",
            "type": "aws_instance",
            "start_line": 15,
            "end_line": 25
        }},
        {{
            "name": "database",
            "type": "aws_rds_instance",
            "start_line": 30,
            "end_line": 45
        }}
    ]
}}
"""
        
        try:
            response = await self.llm_client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}],
            )
            
            response_text = response.content[0].text if response.content else ""
            
            if not response_text:
                logger.warning("Empty response from LLM for component extraction")
                return self._fallback_extract_components(file_path, file_content)
            
            try:
                result = json.loads(response_text)
                return result.get("components", [])
            except json.JSONDecodeError as e:
                logger.warning("Failed to parse LLM response as JSON: %s", e)
                return self._fallback_extract_components(file_path, file_content)
                
        except Exception as e:
            logger.error("Error extracting components with LLM: %s", e, exc_info=True)
            return self._fallback_extract_components(file_path, file_content)

    def _fallback_extract_components(
        self,
        file_path: Path,
        file_content: str,
    ) -> list[dict[str, Any]]:
        """Fallback component extraction using pattern matching.
        
        Args:
            file_path: File path
            file_content: File content
            
        Returns:
            List of component dictionaries
        """
        components = []
        lines = file_content.split("\n")
        
        if file_path.suffix.lower() == ".tf":
            current_component = None
            brace_count = 0
            
            for i, line in enumerate(lines, 1):
                if "resource" in line.lower() and '"' in line:
                    if current_component:
                        components.append({
                            "name": current_component.get("name", "resource"),
                            "type": current_component.get("type", "resource"),
                            "start_line": current_component["start_line"],
                            "end_line": i - 1,
                        })
                    
                    parts = line.split('"')
                    if len(parts) >= 3:
                        current_component = {
                            "name": parts[3] if len(parts) > 3 else "resource",
                            "type": parts[1] if len(parts) > 1 else "resource",
                            "start_line": i,
                        }
                        brace_count = line.count("{") - line.count("}")
                
                if current_component:
                    brace_count += line.count("{") - line.count("}")
                    if brace_count == 0 and "}" in line:
                        components.append({
                            "name": current_component["name"],
                            "type": current_component["type"],
                            "start_line": current_component["start_line"],
                            "end_line": i,
                        })
                        current_component = None
        
        elif file_path.suffix.lower() in [".yaml", ".yml"]:
            if "kind:" in file_content.lower():
                current_kind = None
                current_name = None
                start_line = None
                
                for i, line in enumerate(lines, 1):
                    if line.strip().startswith("kind:"):
                        if current_kind and current_name:
                            components.append({
                                "name": current_name,
                                "type": current_kind,
                                "start_line": start_line or i,
                                "end_line": i - 1,
                            })
                        current_kind = line.split(":")[-1].strip()
                        start_line = i
                    elif line.strip().startswith("name:") and current_kind:
                        current_name = line.split(":")[-1].strip()
                
                if current_kind and current_name:
                    components.append({
                        "name": current_name,
                        "type": current_kind,
                        "start_line": start_line or len(lines),
                        "end_line": len(lines),
                    })
        
        if not components:
            components.append({
                "name": file_path.stem,
                "type": "file",
                "start_line": 1,
                "end_line": len(lines),
            })
        
        return components


code_analyzer = CodeAnalyzer()

