"""Integration analyzer for detecting missing connections and dependency issues."""

import asyncio
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


class IntegrationAnalyzer:
    """Analyzer for detecting integration issues in infrastructure code."""

    async def analyze(
        self,
        infrastructure_code: str,
        cloud_provider: str | None = None,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Analyze infrastructure code for integration issues.

        Args:
            infrastructure_code: Infrastructure code to analyze
            cloud_provider: Cloud provider (aws, gcp, azure)
            api_key: Optional API key for codebase-wide regex search

        Returns:
            Dictionary with analysis results:
            - missing_connections: List of missing connections
            - dependency_issues: List of dependency issues
            - security_gaps: List of security gaps
            - recommendations: List of recommendations
            - regex_security_issues: List of security issues found via regex search
        """
        missing_connections = []
        dependency_issues = []
        security_gaps = []
        recommendations = []
        regex_security_issues = []

        if cloud_provider == "aws":
            missing_connections.extend(self._analyze_aws_connections(infrastructure_code))
            dependency_issues.extend(self._analyze_aws_dependencies(infrastructure_code))
            security_gaps.extend(self._analyze_aws_security(infrastructure_code))

        if cloud_provider == "kubernetes" or "kubernetes" in infrastructure_code.lower():
            missing_connections.extend(self._analyze_k8s_connections(infrastructure_code))
            dependency_issues.extend(self._analyze_k8s_dependencies(infrastructure_code))
            security_gaps.extend(self._analyze_k8s_security(infrastructure_code))

        if api_key:
            try:
                from wistx_mcp.tools import regex_search
                from wistx_mcp.tools.lib.retry_utils import with_timeout

                code_type_map = {
                    "aws": "terraform",
                    "gcp": "terraform",
                    "azure": "terraform",
                    "kubernetes": "kubernetes",
                }
                code_type = code_type_map.get(cloud_provider or "", "terraform")

                security_templates = ["api_key", "password", "secret_key", "aws_access_key"]
                compliance_templates = []
                if cloud_provider == "aws":
                    compliance_templates = ["unencrypted_storage", "public_access", "publicly_accessible"]

                parallel_results, parallel_gaps = await self._perform_regex_searches_parallel(
                    security_templates=security_templates,
                    compliance_templates=compliance_templates,
                    cloud_provider=cloud_provider,
                    api_key=api_key,
                    code_type=code_type,
                    timeout_per_search=10.0,
                )
                
                regex_security_issues.extend(parallel_results)
                security_gaps.extend(parallel_gaps)

            except ImportError:
                logger.warning("regex_search module not available, using basic analysis only")
            except Exception as e:
                logger.warning("Regex search integration failed: %s", e, exc_info=True)

        if missing_connections:
            recommendations.append("Add missing connections between components")
        if dependency_issues:
            recommendations.append("Resolve dependency issues")
        if security_gaps:
            recommendations.append("Address security gaps")

        result = {
            "missing_connections": missing_connections,
            "dependency_issues": dependency_issues,
            "security_gaps": security_gaps,
            "recommendations": recommendations,
        }

        if regex_security_issues:
            result["regex_security_issues"] = regex_security_issues

        return result

    def _analyze_aws_connections(self, code: str) -> list[str]:
        """Analyze AWS infrastructure for missing connections.

        Args:
            code: Infrastructure code

        Returns:
            List of missing connection issues
        """
        issues = []

        if "aws_instance" in code and "aws_security_group" not in code:
            issues.append("EC2 instances without security groups")

        if "aws_lambda_function" in code and "aws_api_gateway" not in code:
            if "aws_apigatewayv2" not in code:
                issues.append("Lambda functions without API Gateway integration")

        if "aws_ecs_service" in code and "aws_lb" not in code:
            if "aws_lb_target_group" not in code:
                issues.append("ECS services without load balancer")

        if "aws_rds_instance" in code:
            if "aws_db_subnet_group" not in code:
                issues.append("RDS instances without subnet group")
            if "aws_security_group" not in code or "db" not in code.lower():
                issues.append("RDS instances without database security group")

        return issues

    def _analyze_aws_dependencies(self, code: str) -> list[str]:
        """Analyze AWS infrastructure for dependency issues.

        Args:
            code: Infrastructure code

        Returns:
            List of dependency issues
        """
        issues = []

        if "aws_subnet" in code and "aws_vpc" not in code:
            issues.append("Subnets without VPC reference")

        if "aws_route_table" in code and "aws_vpc" not in code:
            issues.append("Route tables without VPC reference")

        if "aws_internet_gateway" in code and "aws_vpc" not in code:
            issues.append("Internet gateway without VPC attachment")

        return issues

    def _analyze_aws_security(self, code: str) -> list[str]:
        """Analyze AWS infrastructure for security gaps.

        Args:
            code: Infrastructure code

        Returns:
            List of security gaps
        """
        gaps = []

        if "aws_instance" in code:
            if re.search(r'user_data\s*=', code, re.IGNORECASE):
                if re.search(r'password\s*=\s*["\']', code, re.IGNORECASE):
                    gaps.append("Hardcoded passwords in user_data")
            if "aws_iam_role" not in code:
                gaps.append("EC2 instances without IAM roles")

        if "aws_s3_bucket" in code:
            if "aws_s3_bucket_public_access_block" not in code:
                gaps.append("S3 buckets without public access block")
            if "aws_s3_bucket_versioning" not in code:
                gaps.append("S3 buckets without versioning")

        if "aws_rds_instance" in code:
            if "publicly_accessible" in code and "true" in code.lower():
                gaps.append("Publicly accessible RDS instances")

        return gaps

    def _analyze_k8s_connections(self, code: str) -> list[str]:
        """Analyze Kubernetes manifests for missing connections.

        Args:
            code: Kubernetes manifest code

        Returns:
            List of missing connection issues
        """
        issues = []

        try:
            import yaml

            documents = list(yaml.safe_load_all(code))

            services = []
            deployments = []
            ingresses = []

            for doc in documents:
                if not doc:
                    continue
                kind = doc.get("kind", "")
                metadata = doc.get("metadata", {})
                name = metadata.get("name", "unknown")

                if kind == "Service":
                    services.append({"name": name, "doc": doc})
                elif kind == "Deployment":
                    deployments.append({"name": name, "doc": doc})
                elif kind == "Ingress":
                    ingresses.append({"name": name, "doc": doc})

            deployment_names = {d["name"] for d in deployments}
            service_selectors = set()

            for service in services:
                spec = service["doc"].get("spec", {})
                selector = spec.get("selector", {})
                if selector:
                    app_label = selector.get("app") or selector.get("name")
                    if app_label:
                        service_selectors.add(app_label)

            for deployment in deployments:
                metadata = deployment["doc"].get("metadata", {})
                labels = metadata.get("labels", {})
                app_label = labels.get("app") or labels.get("name") or deployment["name"]

                if app_label not in service_selectors:
                    issues.append(f"Deployment '{deployment['name']}' has no matching Service")

            for service in services:
                spec = service["doc"].get("spec", {})
                if not spec.get("selector"):
                    issues.append(f"Service '{service['name']}' missing selector")

                service_type = spec.get("type", "ClusterIP")
                if service_type == "ClusterIP" and not ingresses:
                    issues.append(f"Service '{service['name']}' has no Ingress or LoadBalancer")

        except ImportError:
            logger.warning("yaml library not available, using basic analysis")
            if "kind: Deployment" in code or "kind: Pod" in code:
                if "kind: Service" not in code:
                    issues.append("Deployments/Pods without Service")

            if "kind: Service" in code:
                if "kind: Ingress" not in code:
                    if "type: LoadBalancer" not in code and "type: NodePort" not in code:
                        issues.append("Services without Ingress or LoadBalancer")
        except Exception as e:
            logger.warning("Failed to parse Kubernetes manifests: %s", e)
            if "kind: Deployment" in code or "kind: Pod" in code:
                if "kind: Service" not in code:
                    issues.append("Deployments/Pods without Service")

        return issues

    def _analyze_k8s_dependencies(self, code: str) -> list[str]:
        """Analyze Kubernetes manifests for dependency issues.

        Args:
            code: Kubernetes manifest code

        Returns:
            List of dependency issues
        """
        issues = []

        if "kind: Deployment" in code:
            if "image:" not in code:
                issues.append("Deployments without container images")

        if "kind: Service" in code:
            if "selector:" not in code:
                issues.append("Services without selectors")

        return issues

    def _analyze_k8s_security(self, code: str) -> list[str]:
        """Analyze Kubernetes manifests for security gaps.

        Args:
            code: Kubernetes manifest code

        Returns:
            List of security gaps
        """
        gaps = []

        if "kind: Deployment" in code or "kind: Pod" in code:
            if "securityContext:" not in code:
                gaps.append("Pods without security context")
            if "runAsNonRoot:" not in code:
                gaps.append("Pods not running as non-root")
            if "readOnlyRootFilesystem:" not in code:
                gaps.append("Pods without read-only root filesystem")

        if "kind: NetworkPolicy" not in code:
            gaps.append("Missing network policies for pod isolation")

        if "kind: Secret" in code:
            if "type: Opaque" in code:
                gaps.append("Using generic Opaque secrets - consider specific secret types")

        return gaps

    def validate_integration(
        self,
        components: list[dict[str, Any]],
        integration_type: str,
    ) -> dict[str, Any]:
        """Validate integration between components.

        Args:
            components: List of component dictionaries
            integration_type: Type of integration (networking, security, service, monitoring)

        Returns:
            Dictionary with validation results:
            - valid: Whether integration is valid
            - issues: List of validation issues
            - fixes: List of recommended fixes
        """
        issues = []
        fixes = []

        component_types = [comp.get("type", "").lower() for comp in components]

        if integration_type == "networking":
            if "vpc" not in component_types and "aws" in str(component_types):
                issues.append("Missing VPC for networking integration")
                fixes.append("Add VPC resource")

        if integration_type == "security":
            if "security_group" not in component_types and "aws" in str(component_types):
                issues.append("Missing security groups for security integration")
                fixes.append("Add security group resources")

        if integration_type == "service":
            if "service" not in component_types and "kubernetes" in str(component_types):
                issues.append("Missing Kubernetes Service for service integration")
                fixes.append("Add Service resource")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "fixes": fixes,
        }

    async def analyze_with_ai(
        self,
        infrastructure_code: str,
        cloud_provider: str | None = None,
    ) -> dict[str, Any]:
        """Use AI analyzer for deeper analysis.

        Args:
            infrastructure_code: Infrastructure code to analyze
            cloud_provider: Cloud provider

        Returns:
            Dictionary with AI analysis results
        """
        try:
            from wistx_mcp.tools.lib.ai_analyzer import AIAnalyzer

            analyzer = AIAnalyzer()

            if not analyzer.client:
                logger.warning("AI analyzer not available, using basic analysis")
                return self.analyze(infrastructure_code, cloud_provider)

            analysis_prompt = f"""
            Analyze this infrastructure code for integration issues:

            {infrastructure_code[:2000]}

            Cloud Provider: {cloud_provider or "unknown"}

            Identify and return JSON format with:
            1. missing_connections: Array of missing connections between components
            2. dependency_issues: Array of dependency problems
            3. security_gaps: Array of security issues
            4. recommendations: Array of recommendations

            Focus on integration patterns, missing connections, and security gaps.
            """

            ai_response = await analyzer._call_llm(analysis_prompt)

            if ai_response:
                import json
                import re

                json_match = re.search(r"\{.*\}", ai_response, re.DOTALL)
                if json_match:
                    ai_result = json.loads(json_match.group())
                    return {
                        "missing_connections": ai_result.get("missing_connections", []),
                        "dependency_issues": ai_result.get("dependency_issues", []),
                        "security_gaps": ai_result.get("security_gaps", []),
                        "recommendations": ai_result.get("recommendations", []),
                    }

            return self.analyze(infrastructure_code, cloud_provider)
        except Exception as e:
            logger.warning("AI analysis failed, falling back to basic analysis: %s", e)
            return self.analyze(infrastructure_code, cloud_provider)

    async def _perform_regex_searches_parallel(
        self,
        security_templates: list[str],
        compliance_templates: list[str],
        cloud_provider: str | None,
        api_key: str,
        code_type: str,
        timeout_per_search: float = 10.0,
    ) -> tuple[list[dict[str, Any]], list[str]]:
        """Perform regex searches in parallel with timeout protection.
        
        Args:
            security_templates: List of security template names to search
            compliance_templates: List of compliance template names to search
            cloud_provider: Cloud provider name
            api_key: API key for regex search
            code_type: Code type for filtering
            timeout_per_search: Timeout per individual search
            
        Returns:
            Tuple of (regex_security_issues list, security_gaps list)
        """
        regex_security_issues = []
        security_gaps = []
        
        async def search_template(template: str, is_compliance: bool = False) -> dict[str, Any] | None:
            """Search a single template with timeout protection."""
            try:
                from wistx_mcp.tools import regex_search
                from wistx_mcp.tools.lib.retry_utils import with_timeout
                
                file_types = [".tf"] if is_compliance else [".tf", ".yaml", ".yml"]
                code_type_filter = code_type if code_type != "kubernetes" else None
                
                regex_results = await with_timeout(
                    regex_search.regex_search_codebase,
                    timeout_seconds=timeout_per_search,
                    template=template,
                    api_key=api_key,
                    file_types=file_types,
                    code_type=code_type_filter,
                    include_context=True,
                    limit=5,
                )
                
                matches = regex_results.get("matches", [])
                if matches:
                    return {
                        "type": template,
                        "count": len(matches),
                        "matches": matches[:3],
                        "is_compliance": is_compliance,
                    }
            except asyncio.TimeoutError:
                logger.warning("Regex search timed out for template: %s", template)
            except Exception as e:
                logger.warning("Regex search failed for template %s: %s", template, e)
            return None
        
        search_tasks = []
        for template in security_templates:
            search_tasks.append(search_template(template, is_compliance=False))
        
        if cloud_provider == "aws":
            for template in compliance_templates:
                search_tasks.append(search_template(template, is_compliance=True))
        
        try:
            results = await asyncio.wait_for(
                asyncio.gather(*search_tasks, return_exceptions=True),
                timeout=30.0,
            )
            
            for result in results:
                if isinstance(result, Exception):
                    logger.warning("Regex search task failed: %s", result)
                    continue
                
                if result:
                    regex_security_issues.append(result)
                    template_name = result["type"].replace("_", " ")
                    if result.get("is_compliance"):
                        security_gaps.append(f"Found {result['count']} {template_name} violations")
                    else:
                        security_gaps.append(f"Found {result['count']} {template_name} issues in codebase")
        
        except asyncio.TimeoutError:
            logger.warning("Overall regex search timeout exceeded")
        
        return regex_security_issues, security_gaps

