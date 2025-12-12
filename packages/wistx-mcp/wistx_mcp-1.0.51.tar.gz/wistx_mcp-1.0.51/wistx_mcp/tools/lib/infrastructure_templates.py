"""Infrastructure templates for common patterns."""

from typing import Any

INFRASTRUCTURE_TEMPLATES: dict[str, dict[str, Any]] = {
    "kubernetes": {
        "eks_cluster": {
            "description": "AWS EKS cluster template",
            "terraform": """
resource "aws_eks_cluster" "cluster" {
  name     = var.cluster_name
  role_arn = aws_iam_role.cluster.arn
  version  = var.k8s_version

  vpc_config {
    subnet_ids = var.subnet_ids
  }

  depends_on = [
    aws_iam_role_policy_attachment.cluster_AmazonEKSClusterPolicy,
  ]
}

resource "aws_eks_node_group" "nodes" {
  cluster_name    = aws_eks_cluster.cluster.name
  node_group_name = "default"
  node_role_arn   = aws_iam_role.nodes.arn
  subnet_ids      = var.subnet_ids

  scaling_config {
    desired_size = var.desired_size
    max_size     = var.max_size
    min_size     = var.min_size
  }
}
""",
            "kubernetes": None,
        },
        "gke_cluster": {
            "description": "GCP GKE cluster template",
            "terraform": """
resource "google_container_cluster" "cluster" {
  name     = var.cluster_name
  location = var.region

  node_config {
    machine_type = var.machine_type
    disk_size_gb = var.disk_size
  }

  node_pool {
    name       = "default-pool"
    node_count = var.node_count
  }
}
""",
            "kubernetes": None,
        },
        "aks_cluster": {
            "description": "Azure AKS cluster template",
            "terraform": """
resource "azurerm_kubernetes_cluster" "cluster" {
  name                = var.cluster_name
  location            = var.resource_group_location
  resource_group_name = var.resource_group_name
  dns_prefix          = var.cluster_name

  default_node_pool {
    name       = "default"
    node_count = var.node_count
    vm_size    = var.vm_size
  }

  identity {
    type = "SystemAssigned"
  }
}
""",
            "kubernetes": None,
        },
    },
    "multi_cloud": {
        "hybrid_cloud": {
            "description": "Hybrid cloud setup with AWS and GCP",
            "terraform": """
# AWS Resources
resource "aws_vpc" "aws_vpc" {
  cidr_block = var.aws_cidr
}

# GCP Resources
resource "google_compute_network" "gcp_network" {
  name = var.gcp_network_name
}

# Cross-cloud VPN
resource "aws_vpn_gateway" "aws_vpn" {
  vpc_id = aws_vpc.aws_vpc.id
}

resource "google_compute_vpn_gateway" "gcp_vpn" {
  name    = "gcp-vpn-gateway"
  network = google_compute_network.gcp_network.id
}
""",
        },
        "multi_cloud_kubernetes": {
            "description": "Multi-cloud Kubernetes federation",
            "terraform": """
# EKS Cluster
resource "aws_eks_cluster" "eks" {
  name     = "eks-cluster"
  role_arn = aws_iam_role.eks.arn
  vpc_config {
    subnet_ids = var.aws_subnets
  }
}

# GKE Cluster
resource "google_container_cluster" "gke" {
  name     = "gke-cluster"
  location = var.gcp_region
  node_config {
    machine_type = "e2-medium"
  }
}

# AKS Cluster
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "aks-cluster"
  location            = var.azure_location
  resource_group_name = var.resource_group_name
  default_node_pool {
    name       = "default"
    node_count = 1
  }
}
""",
        },
    },
    "compliance": {
        "soc2_cluster": {
            "description": "SOC2 compliant Kubernetes cluster",
            "terraform": """
# EKS Cluster with SOC2 compliance
resource "aws_eks_cluster" "soc2_cluster" {
  name     = var.cluster_name
  role_arn = aws_iam_role.cluster.arn

  vpc_config {
    subnet_ids = var.subnet_ids
  }

  enabled_cluster_log_types = [
    "api",
    "audit",
    "authenticator",
    "controllerManager",
    "scheduler"
  ]

  encryption_config {
    provider {
      key_arn = aws_kms_key.eks.arn
    }
    resources = ["secrets"]
  }
}

resource "aws_kms_key" "eks" {
  description             = "EKS cluster encryption key"
  deletion_window_in_days = 10
}
""",
        },
        "hipaa_cluster": {
            "description": "HIPAA compliant infrastructure",
            "terraform": """
# HIPAA compliant RDS instance
resource "aws_db_instance" "hipaa_db" {
  identifier     = var.db_identifier
  engine         = "postgres"
  engine_version = "13.7"
  instance_class = var.instance_class

  storage_encrypted = true
  kms_key_id        = aws_kms_key.db.arn

  backup_retention_period = 35
  backup_window          = "03:00-04:00"
  maintenance_window     = "mon:04:00-mon:05:00"

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
}

resource "aws_kms_key" "db" {
  description             = "Database encryption key"
  deletion_window_in_days = 10
}
""",
        },
    },
}


def get_template(
    infrastructure_type: str,
    template_name: str,
) -> dict[str, Any] | None:
    """Get infrastructure template by type and name.

    Args:
        infrastructure_type: Type of infrastructure (kubernetes, multi_cloud, compliance)
        template_name: Name of the template

    Returns:
        Template dictionary or None if not found
    """
    return INFRASTRUCTURE_TEMPLATES.get(infrastructure_type, {}).get(template_name)


def list_templates(infrastructure_type: str | None = None) -> dict[str, Any]:
    """List available infrastructure templates.

    Args:
        infrastructure_type: Filter by infrastructure type (optional)

    Returns:
        Dictionary of templates
    """
    if infrastructure_type:
        return INFRASTRUCTURE_TEMPLATES.get(infrastructure_type, {})
    return INFRASTRUCTURE_TEMPLATES

