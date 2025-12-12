"""Resource type validation utilities.

This module provides validation for infrastructure resource types across:
- Cloud Providers (AWS, GCP, Azure)
- Kubernetes and Container Orchestration
- CI/CD and DevOps Tools
- Infrastructure as Code
"""

# ============================================================================
# KUBERNETES & CONTAINER ORCHESTRATION RESOURCE TYPES
# ============================================================================
VALID_KUBERNETES_RESOURCE_TYPES = {
    # Core Workloads
    "Deployment",
    "StatefulSet",
    "DaemonSet",
    "ReplicaSet",
    "Pod",
    "Job",
    "CronJob",
    # Services & Networking
    "Service",
    "Ingress",
    "IngressClass",
    "NetworkPolicy",
    "Endpoints",
    "EndpointSlice",
    # Configuration & Storage
    "ConfigMap",
    "Secret",
    "PersistentVolume",
    "PersistentVolumeClaim",
    "StorageClass",
    "VolumeSnapshot",
    "VolumeSnapshotClass",
    # RBAC & Security
    "ServiceAccount",
    "Role",
    "RoleBinding",
    "ClusterRole",
    "ClusterRoleBinding",
    "PodSecurityPolicy",
    "NetworkPolicy",
    "LimitRange",
    "ResourceQuota",
    # Scaling & Policy
    "HorizontalPodAutoscaler",
    "VerticalPodAutoscaler",
    "PodDisruptionBudget",
    "PriorityClass",
    # Custom Resources (Common)
    "CustomResourceDefinition",
    "MutatingWebhookConfiguration",
    "ValidatingWebhookConfiguration",
}

# ArgoCD Resource Types
VALID_ARGOCD_RESOURCE_TYPES = {
    "Application",
    "ApplicationSet",
    "AppProject",
    "ArgoCD",
}

# Argo Rollouts & Workflows
VALID_ARGO_RESOURCE_TYPES = {
    "Rollout",
    "AnalysisTemplate",
    "AnalysisRun",
    "ClusterAnalysisTemplate",
    "Experiment",
    "Workflow",
    "WorkflowTemplate",
    "ClusterWorkflowTemplate",
    "CronWorkflow",
    "WorkflowEventBinding",
}

# Helm Resource Types
VALID_HELM_RESOURCE_TYPES = {
    "HelmRelease",
    "HelmRepository",
    "HelmChart",
}

# Flux CD Resource Types
VALID_FLUX_RESOURCE_TYPES = {
    "Kustomization",
    "GitRepository",
    "HelmRelease",
    "HelmRepository",
    "HelmChart",
    "Bucket",
    "OCIRepository",
    "ImageRepository",
    "ImagePolicy",
    "ImageUpdateAutomation",
    "Receiver",
    "Alert",
    "Provider",
}

# Istio Service Mesh Resource Types
VALID_ISTIO_RESOURCE_TYPES = {
    "VirtualService",
    "DestinationRule",
    "Gateway",
    "ServiceEntry",
    "Sidecar",
    "AuthorizationPolicy",
    "PeerAuthentication",
    "RequestAuthentication",
    "EnvoyFilter",
    "WorkloadEntry",
    "WorkloadGroup",
}

# Cert-Manager Resource Types
VALID_CERTMANAGER_RESOURCE_TYPES = {
    "Certificate",
    "CertificateRequest",
    "Issuer",
    "ClusterIssuer",
    "Challenge",
    "Order",
}

# External Secrets Operator
VALID_EXTERNAL_SECRETS_TYPES = {
    "ExternalSecret",
    "SecretStore",
    "ClusterSecretStore",
}

# Prometheus & Monitoring
VALID_PROMETHEUS_RESOURCE_TYPES = {
    "ServiceMonitor",
    "PodMonitor",
    "PrometheusRule",
    "Prometheus",
    "Alertmanager",
    "ThanosRuler",
}

# KEDA (Kubernetes Event-driven Autoscaling)
VALID_KEDA_RESOURCE_TYPES = {
    "ScaledObject",
    "ScaledJob",
    "TriggerAuthentication",
    "ClusterTriggerAuthentication",
}

# ============================================================================
# CI/CD & DEVOPS TOOL RESOURCE TYPES
# ============================================================================
VALID_CICD_RESOURCE_TYPES = {
    # GitHub Actions
    "GitHub Actions Workflow",
    "GitHub Actions Job",
    "GitHub Actions Step",
    # GitLab CI
    "GitLab CI Pipeline",
    "GitLab CI Job",
    "GitLab CI Stage",
    # Jenkins
    "Jenkinsfile",
    "Jenkins Pipeline",
    "Jenkins Job",
    # CircleCI
    "CircleCI Config",
    "CircleCI Job",
    "CircleCI Workflow",
    # Azure DevOps
    "Azure Pipeline",
    "Azure DevOps Task",
    # Tekton
    "Pipeline",
    "Task",
    "TaskRun",
    "PipelineRun",
    "PipelineResource",
    "TriggerTemplate",
    "TriggerBinding",
    "EventListener",
}

# ============================================================================
# INFRASTRUCTURE AS CODE RESOURCE TYPES
# ============================================================================
VALID_IAC_RESOURCE_TYPES = {
    # Terraform
    "Terraform",
    "Terraform Module",
    "Terraform Resource",
    "Terraform Data Source",
    "Terraform Provider",
    # Pulumi
    "Pulumi Stack",
    "Pulumi Resource",
    # CloudFormation
    "CloudFormation",
    "CloudFormation Stack",
    "CloudFormation StackSet",
    # Ansible
    "Ansible Playbook",
    "Ansible Role",
    "Ansible Task",
    # Docker
    "Dockerfile",
    "Docker Compose Service",
    "Docker Compose Network",
    "Docker Compose Volume",
}

# ============================================================================
# COMBINED DEVOPS RESOURCE TYPES
# ============================================================================
VALID_DEVOPS_RESOURCE_TYPES = (
    VALID_KUBERNETES_RESOURCE_TYPES |
    VALID_ARGOCD_RESOURCE_TYPES |
    VALID_ARGO_RESOURCE_TYPES |
    VALID_HELM_RESOURCE_TYPES |
    VALID_FLUX_RESOURCE_TYPES |
    VALID_ISTIO_RESOURCE_TYPES |
    VALID_CERTMANAGER_RESOURCE_TYPES |
    VALID_EXTERNAL_SECRETS_TYPES |
    VALID_PROMETHEUS_RESOURCE_TYPES |
    VALID_KEDA_RESOURCE_TYPES |
    VALID_CICD_RESOURCE_TYPES |
    VALID_IAC_RESOURCE_TYPES
)

try:
    from wistx_mcp.tools.lib.resource_type_loader import get_resource_types, get_all_resource_types

    def _load_resource_types_from_filesystem() -> tuple[set[str] | None, set[str] | None, set[str] | None]:
        """Load resource types from filesystem, fallback to hardcoded."""
        try:
            aws_types = get_resource_types("aws")
            gcp_types = get_resource_types("gcp")
            azure_types = get_resource_types("azure")
            return aws_types, gcp_types, azure_types
        except Exception:
            return None, None, None

    _fs_aws, _fs_gcp, _fs_azure = _load_resource_types_from_filesystem()

    if _fs_aws and _fs_gcp and _fs_azure:
        VALID_AWS_RESOURCE_TYPES = _fs_aws
        VALID_GCP_RESOURCE_TYPES = _fs_gcp
        VALID_AZURE_RESOURCE_TYPES = _fs_azure
        try:
            _cloud_types = get_all_resource_types()
            VALID_RESOURCE_TYPES = _cloud_types | VALID_DEVOPS_RESOURCE_TYPES
        except Exception:
            VALID_RESOURCE_TYPES = VALID_AWS_RESOURCE_TYPES | VALID_GCP_RESOURCE_TYPES | VALID_AZURE_RESOURCE_TYPES | VALID_DEVOPS_RESOURCE_TYPES
    else:
        VALID_AWS_RESOURCE_TYPES = {
            "EC2",
            "RDS",
            "S3",
            "Lambda",
            "EKS",
            "ECS",
            "VPC",
            "IAM",
            "CloudFront",
            "Route53",
            "ElastiCache",
            "DynamoDB",
            "SQS",
            "SNS",
            "KMS",
            "SecretsManager",
            "CloudWatch",
            "ELB",
            "ALB",
            "NLB",
            "EFS",
            "EBS",
            "Redshift",
            "Aurora",
            "DocumentDB",
            "Neptune",
            "Elasticsearch",
            "OpenSearch",
            "MSK",
            "MQ",
            "EventBridge",
            "StepFunctions",
            "AppSync",
            "API Gateway",
            "Cognito",
            "WAF",
            "Shield",
            "GuardDuty",
            "SecurityHub",
            "Inspector",
            "Macie",
            "Config",
            "CloudTrail",
            "Systems Manager",
            "CodeBuild",
            "CodeDeploy",
            "CodePipeline",
            "CloudFormation",
            "Terraform",
        }
        
        VALID_GCP_RESOURCE_TYPES = {
            "GCE",
            "Cloud SQL",
            "GKE",
            "Cloud Storage",
            "Cloud Functions",
            "Cloud Run",
            "Cloud Build",
            "Cloud Pub/Sub",
            "Cloud Bigtable",
            "Cloud Spanner",
            "Cloud Firestore",
            "Cloud Datastore",
            "Cloud Memorystore",
            "Cloud Load Balancing",
            "Cloud CDN",
            "Cloud IAM",
            "Cloud KMS",
            "Cloud Secret Manager",
            "Cloud Monitoring",
            "Cloud Logging",
            "Cloud Trace",
            "Cloud Debugger",
            "Cloud Scheduler",
            "Cloud Tasks",
            "Cloud Endpoints",
            "Cloud Armor",
            "Cloud Identity",
            "Cloud Resource Manager",
            "Cloud Billing",
            "Cloud Asset",
            "Cloud Security Command Center",
            "Cloud DLP",
            "Cloud IAP",
            "Cloud VPN",
            "Cloud Interconnect",
            "Cloud NAT",
            "Cloud DNS",
            "Cloud Domains",
        }
        
        VALID_AZURE_RESOURCE_TYPES = {
            "Virtual Machines",
            "VM Scale Sets",
        "SQL Database",
        "Azure Cache for Redis",
        "Cosmos DB",
            "Storage Account",
            "Blob Storage",
            "File Storage",
            "Queue Storage",
            "Table Storage",
            "AKS",
            "Container Instances",
            "App Service",
            "Functions",
            "Logic Apps",
            "Service Bus",
            "Event Hubs",
            "Event Grid",
            "Key Vault",
            "Active Directory",
            "Application Gateway",
            "Load Balancer",
            "Front Door",
            "CDN",
            "Traffic Manager",
            "DNS",
            "Virtual Network",
            "VPN Gateway",
            "ExpressRoute",
            "Network Security Group",
            "Application Security Group",
            "Firewall",
            "DDoS Protection",
            "Security Center",
            "Sentinel",
            "Defender",
            "Policy",
            "Resource Manager",
            "Monitor",
            "Log Analytics",
            "Application Insights",
            "Backup",
            "Site Recovery",
            "Cost Management",
        }
        
        VALID_RESOURCE_TYPES = VALID_AWS_RESOURCE_TYPES | VALID_GCP_RESOURCE_TYPES | VALID_AZURE_RESOURCE_TYPES | VALID_DEVOPS_RESOURCE_TYPES
except ImportError:
    VALID_AWS_RESOURCE_TYPES = {
        "EC2",
        "RDS",
        "S3",
        "Lambda",
        "EKS",
        "ECS",
        "VPC",
        "IAM",
        "CloudFront",
        "Route53",
        "ElastiCache",
        "DynamoDB",
        "SQS",
        "SNS",
        "KMS",
        "SecretsManager",
        "CloudWatch",
        "ELB",
        "ALB",
        "NLB",
        "EFS",
        "EBS",
        "Redshift",
        "Aurora",
        "DocumentDB",
        "Neptune",
        "Elasticsearch",
        "OpenSearch",
        "MSK",
        "MQ",
        "EventBridge",
        "StepFunctions",
        "AppSync",
        "API Gateway",
        "Cognito",
        "WAF",
        "Shield",
        "GuardDuty",
        "SecurityHub",
        "Inspector",
        "Macie",
        "Config",
        "CloudTrail",
        "Systems Manager",
        "CodeBuild",
        "CodeDeploy",
        "CodePipeline",
        "CloudFormation",
        "Terraform",
    }
    
    VALID_GCP_RESOURCE_TYPES = {
        "GCE",
        "Cloud SQL",
        "GKE",
        "Cloud Storage",
        "Cloud Functions",
        "Cloud Run",
        "Cloud Build",
        "Cloud Pub/Sub",
        "Cloud Bigtable",
        "Cloud Spanner",
        "Cloud Firestore",
        "Cloud Datastore",
        "Cloud Memorystore",
        "Cloud Load Balancing",
        "Cloud CDN",
        "Cloud IAM",
        "Cloud KMS",
        "Cloud Secret Manager",
        "Cloud Monitoring",
        "Cloud Logging",
        "Cloud Trace",
        "Cloud Debugger",
        "Cloud Scheduler",
        "Cloud Tasks",
        "Cloud Endpoints",
        "Cloud Armor",
        "Cloud Identity",
        "Cloud Resource Manager",
        "Cloud Billing",
        "Cloud Asset",
        "Cloud Security Command Center",
        "Cloud DLP",
        "Cloud IAP",
        "Cloud VPN",
        "Cloud Interconnect",
            "Cloud NAT",
            "Cloud DNS",
            "Cloud Domains",
        }
    
    VALID_AZURE_RESOURCE_TYPES = {
        "Virtual Machines",
        "VM Scale Sets",
        "SQL Database",
        "Azure Cache for Redis",
        "Cosmos DB",
        "Storage Account",
        "Blob Storage",
        "File Storage",
        "Queue Storage",
        "Table Storage",
        "AKS",
        "Container Instances",
        "App Service",
        "Functions",
        "Logic Apps",
        "Service Bus",
        "Event Hubs",
        "Event Grid",
        "Key Vault",
        "Active Directory",
        "Application Gateway",
        "Load Balancer",
        "Front Door",
        "CDN",
        "Traffic Manager",
        "DNS",
        "Virtual Network",
        "VPN Gateway",
        "ExpressRoute",
        "Network Security Group",
        "Application Security Group",
        "Firewall",
        "DDoS Protection",
        "Security Center",
        "Sentinel",
        "Defender",
        "Policy",
        "Resource Manager",
        "Monitor",
        "Log Analytics",
        "Application Insights",
        "Backup",
        "Site Recovery",
        "Cost Management",
    }
    
    VALID_RESOURCE_TYPES = VALID_AWS_RESOURCE_TYPES | VALID_GCP_RESOURCE_TYPES | VALID_AZURE_RESOURCE_TYPES | VALID_DEVOPS_RESOURCE_TYPES


def validate_resource_types(resource_types: list[str]) -> tuple[list[str], list[str]]:
    """Validate resource types against known resource type lists.

    Args:
        resource_types: List of resource types to validate

    Returns:
        Tuple of (valid_types, invalid_types)
    """
    valid_types = []
    invalid_types = []

    valid_types_upper = {rt.upper() for rt in VALID_RESOURCE_TYPES}
    
    for resource_type in resource_types:
        if not resource_type or not resource_type.strip():
            continue

        normalized = resource_type.strip().upper()

        if normalized in valid_types_upper:
            valid_types.append(resource_type.strip())
        else:
            invalid_types.append(resource_type.strip())

    return valid_types, invalid_types
