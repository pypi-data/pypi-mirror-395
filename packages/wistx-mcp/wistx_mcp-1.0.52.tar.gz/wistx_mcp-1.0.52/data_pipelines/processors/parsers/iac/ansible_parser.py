"""Ansible playbook parser."""

import yaml
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class AnsibleParser(ToolParser):
    """Parser for Ansible playbooks and roles."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract Ansible tasks/modules.
        
        Args:
            code: Ansible YAML content
            
        Returns:
            List of Ansible module names
        """
        resources = []
        try:
            playbook = yaml.safe_load(code)
            
            if isinstance(playbook, list):
                for play in playbook:
                    tasks = play.get("tasks", []) or play.get("roles", [])
                    for task in tasks:
                        if isinstance(task, dict):
                            for module_name in task.keys():
                                if module_name not in ["name", "when", "loop", "tags"]:
                                    resources.append(module_name)
            elif isinstance(playbook, dict):
                tasks = playbook.get("tasks", []) or playbook.get("roles", [])
                for task in tasks:
                    if isinstance(task, dict):
                        for module_name in task.keys():
                            if module_name not in ["name", "when", "loop", "tags"]:
                                resources.append(module_name)
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return list(set(resources))

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from Ansible.
        
        Args:
            code: Ansible YAML content
            
        Returns:
            Cloud provider name or None
        """
        code_lower = code.lower()
        
        aws_modules = ["ec2", "s3", "rds", "iam", "lambda", "cloudformation"]
        gcp_modules = ["gcp", "gce", "gcs", "gke"]
        azure_modules = ["azure", "azure_rm"]
        
        if any(module in code_lower for module in aws_modules):
            return "aws"
        if any(module in code_lower for module in gcp_modules):
            return "gcp"
        if any(module in code_lower for module in azure_modules):
            return "azure"
        
        return None

    def extract_services(self, code: str) -> list[str]:
        """Extract cloud services from Ansible.
        
        Args:
            code: Ansible YAML content
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        service_mapping = {
            "ec2": ["ec2_instance", "ec2"],
            "s3": ["s3_bucket", "s3"],
            "rds": ["rds_instance", "rds"],
            "lambda": ["lambda_function", "lambda"],
            "eks": ["eks_cluster", "eks"],
            "gke": ["gke_cluster", "gke"],
            "aks": ["azure_rm_aks", "aks"],
        }
        
        for service, patterns in service_mapping.items():
            if any(pattern in code_lower for pattern in patterns):
                if service not in services:
                    services.append(service)
        
        return services

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract Ansible-specific metadata.
        
        Args:
            code: Ansible YAML content
            
        Returns:
            Dictionary with Ansible metadata
        """
        metadata = {}
        try:
            playbook = yaml.safe_load(code)
            
            if isinstance(playbook, list):
                playbook = playbook[0] if playbook else {}
            
            metadata["hosts"] = playbook.get("hosts", [])
            metadata["become"] = playbook.get("become", False)
            metadata["vars"] = list(playbook.get("vars", {}).keys()) if isinstance(playbook.get("vars"), dict) else []
            metadata["roles"] = playbook.get("roles", [])
            metadata["tasks_count"] = len(playbook.get("tasks", []))
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return metadata

    def validate_syntax(self, code: str) -> bool:
        """Basic Ansible syntax validation.
        
        Args:
            code: Ansible YAML content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        try:
            playbook = yaml.safe_load(code)
            if not playbook:
                return False
            
            has_hosts = False
            has_tasks = False
            
            if isinstance(playbook, list):
                playbook = playbook[0] if playbook else {}
            
            if isinstance(playbook, dict):
                has_hosts = "hosts" in playbook
                has_tasks = "tasks" in playbook or "roles" in playbook
            
            return has_hosts or has_tasks
        except yaml.YAMLError:
            return False

