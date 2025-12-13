"""DevOps resource type definitions - CLI tools, services, and resource types."""

import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class DevOpsTool:
    """CLI tool definition."""

    name: str
    description: str
    category: str
    install_command: str
    official_url: str
    github_url: str | None = None
    popularity_score: float = 0.0
    keywords: list[str] | None = None

    def __post_init__(self):
        """Initialize keywords if not provided."""
        if self.keywords is None:
            self.keywords = []


@dataclass
class DevOpsService:
    """SaaS/Integration service definition."""

    name: str
    description: str
    category: str
    official_url: str
    integration_type: str
    popularity_score: float = 0.0
    keywords: list[str] | None = None

    def __post_init__(self):
        """Initialize keywords if not provided."""
        if self.keywords is None:
            self.keywords = []


DEVOPS_TOOLS = [
    DevOpsTool(
        name="terraform",
        description="Infrastructure as Code tool for provisioning and managing cloud resources",
        category="infrastructure-as-code",
        install_command="brew install terraform",
        official_url="https://www.terraform.io",
        github_url="https://github.com/hashicorp/terraform",
        popularity_score=0.95,
        keywords=["iac", "infrastructure", "cloud", "provisioning", "tf"],
    ),
    DevOpsTool(
        name="kubectl",
        description="Kubernetes command-line tool for cluster management and deployment",
        category="kubernetes",
        install_command="brew install kubectl",
        official_url="https://kubernetes.io/docs/tasks/tools/",
        github_url="https://github.com/kubernetes/kubectl",
        popularity_score=0.98,
        keywords=["k8s", "kubernetes", "container", "orchestration", "cluster"],
    ),
    DevOpsTool(
        name="helm",
        description="Package manager for Kubernetes applications and charts",
        category="kubernetes",
        install_command="brew install helm",
        official_url="https://helm.sh",
        github_url="https://github.com/helm/helm",
        popularity_score=0.90,
        keywords=["k8s", "kubernetes", "charts", "package", "deployment"],
    ),
    DevOpsTool(
        name="ansible",
        description="Configuration management and automation platform",
        category="configuration-management",
        install_command="pip install ansible",
        official_url="https://www.ansible.com",
        github_url="https://github.com/ansible/ansible",
        popularity_score=0.88,
        keywords=["automation", "configuration", "provisioning", "playbook"],
    ),
    DevOpsTool(
        name="docker",
        description="Containerization platform for building and running applications",
        category="containerization",
        install_command="brew install docker",
        official_url="https://www.docker.com",
        github_url="https://github.com/docker/docker",
        popularity_score=0.97,
        keywords=["container", "containers", "images", "runtime"],
    ),
    DevOpsTool(
        name="pulumi",
        description="Modern Infrastructure as Code using familiar programming languages",
        category="infrastructure-as-code",
        install_command="brew install pulumi",
        official_url="https://www.pulumi.com",
        github_url="https://github.com/pulumi/pulumi",
        popularity_score=0.75,
        keywords=["iac", "infrastructure", "code", "typescript", "python"],
    ),
    DevOpsTool(
        name="vagrant",
        description="Tool for building and managing virtual machine environments",
        category="virtualization",
        install_command="brew install vagrant",
        official_url="https://www.vagrantup.com",
        github_url="https://github.com/hashicorp/vagrant",
        popularity_score=0.70,
        keywords=["vm", "virtualization", "development", "environment"],
    ),
    DevOpsTool(
        name="packer",
        description="Tool for creating identical machine images for multiple platforms",
        category="infrastructure-as-code",
        install_command="brew install packer",
        official_url="https://www.packer.io",
        github_url="https://github.com/hashicorp/packer",
        popularity_score=0.72,
        keywords=["images", "ami", "golden", "build"],
    ),
    DevOpsTool(
        name="consul",
        description="Service networking solution for connecting and securing services",
        category="service-mesh",
        install_command="brew install consul",
        official_url="https://www.consul.io",
        github_url="https://github.com/hashicorp/consul",
        popularity_score=0.80,
        keywords=["service", "mesh", "discovery", "networking"],
    ),
    DevOpsTool(
        name="vault",
        description="Secrets management and data protection tool",
        category="security",
        install_command="brew install vault",
        official_url="https://www.vaultproject.io",
        github_url="https://github.com/hashicorp/vault",
        popularity_score=0.85,
        keywords=["secrets", "security", "encryption", "credentials"],
    ),
    DevOpsTool(
        name="nomad",
        description="Workload orchestrator for deploying applications",
        category="orchestration",
        install_command="brew install nomad",
        official_url="https://www.nomadproject.io",
        github_url="https://github.com/hashicorp/nomad",
        popularity_score=0.68,
        keywords=["orchestration", "scheduler", "workload", "deployment"],
    ),
    DevOpsTool(
        name="terraform-docs",
        description="Generate documentation from Terraform modules",
        category="documentation",
        install_command="brew install terraform-docs",
        official_url="https://terraform-docs.io",
        github_url="https://github.com/terraform-docs/terraform-docs",
        popularity_score=0.65,
        keywords=["documentation", "terraform", "modules", "docs"],
    ),
    DevOpsTool(
        name="terragrunt",
        description="Thin wrapper for Terraform that provides extra tools",
        category="infrastructure-as-code",
        install_command="brew install terragrunt",
        official_url="https://terragrunt.gruntwork.io",
        github_url="https://github.com/gruntwork-io/terragrunt",
        popularity_score=0.78,
        keywords=["terraform", "wrapper", "dry", "reusability"],
    ),
    DevOpsTool(
        name="kustomize",
        description="Template-free customization of Kubernetes YAML configurations",
        category="kubernetes",
        install_command="brew install kustomize",
        official_url="https://kustomize.io",
        github_url="https://github.com/kubernetes-sigs/kustomize",
        popularity_score=0.82,
        keywords=["k8s", "kubernetes", "yaml", "configuration"],
    ),
    DevOpsTool(
        name="skaffold",
        description="Command line tool for continuous development of Kubernetes applications",
        category="kubernetes",
        install_command="brew install skaffold",
        official_url="https://skaffold.dev",
        github_url="https://github.com/GoogleContainerTools/skaffold",
        popularity_score=0.73,
        keywords=["k8s", "kubernetes", "development", "ci-cd"],
    ),
    DevOpsTool(
        name="k9s",
        description="Terminal UI for managing Kubernetes clusters",
        category="kubernetes",
        install_command="brew install k9s",
        official_url="https://k9scli.io",
        github_url="https://github.com/derailed/k9s",
        popularity_score=0.77,
        keywords=["k8s", "kubernetes", "ui", "terminal", "management"],
    ),
    DevOpsTool(
        name="kubectx",
        description="Tool to switch between Kubernetes contexts",
        category="kubernetes",
        install_command="brew install kubectx",
        official_url="https://github.com/ahmetb/kubectx",
        github_url="https://github.com/ahmetb/kubectx",
        popularity_score=0.75,
        keywords=["k8s", "kubernetes", "context", "switch"],
    ),
    DevOpsTool(
        name="kubens",
        description="Tool to switch between Kubernetes namespaces",
        category="kubernetes",
        install_command="brew install kubens",
        official_url="https://github.com/ahmetb/kubens",
        github_url="https://github.com/ahmetb/kubens",
        popularity_score=0.74,
        keywords=["k8s", "kubernetes", "namespace", "switch"],
    ),
    DevOpsTool(
        name="kubeval",
        description="Validate Kubernetes configuration files",
        category="kubernetes",
        install_command="brew install kubeval",
        official_url="https://www.kubeval.com",
        github_url="https://github.com/instrumenta/kubeval",
        popularity_score=0.68,
        keywords=["k8s", "kubernetes", "validation", "yaml"],
    ),
    DevOpsTool(
        name="kube-score",
        description="Kubernetes object analysis with recommendations for best practices",
        category="kubernetes",
        install_command="brew install kube-score",
        official_url="https://kube-score.com",
        github_url="https://github.com/zegl/kube-score",
        popularity_score=0.70,
        keywords=["k8s", "kubernetes", "analysis", "best-practices"],
    ),
    DevOpsTool(
        name="kubescape",
        description="Kubernetes security testing and compliance scanning",
        category="security",
        install_command="brew install kubescape",
        official_url="https://kubescape.io",
        github_url="https://github.com/kubescape/kubescape",
        popularity_score=0.76,
        keywords=["k8s", "kubernetes", "security", "compliance", "scanning"],
    ),
    DevOpsTool(
        name="trivy",
        description="Security scanner for containers and other artifacts",
        category="security",
        install_command="brew install trivy",
        official_url="https://aquasecurity.github.io/trivy",
        github_url="https://github.com/aquasecurity/trivy",
        popularity_score=0.84,
        keywords=["security", "scanning", "vulnerability", "container"],
    ),
    DevOpsTool(
        name="snyk",
        description="Security platform for finding and fixing vulnerabilities",
        category="security",
        install_command="npm install -g snyk",
        official_url="https://snyk.io",
        github_url="https://github.com/snyk/snyk",
        popularity_score=0.81,
        keywords=["security", "vulnerability", "scanning", "dependencies"],
    ),
    DevOpsTool(
        name="hadolint",
        description="Dockerfile linter that checks for best practices",
        category="containerization",
        install_command="brew install hadolint",
        official_url="https://hadolint.github.io/hadolint",
        github_url="https://github.com/hadolint/hadolint",
        popularity_score=0.71,
        keywords=["docker", "dockerfile", "linter", "best-practices"],
    ),
    DevOpsTool(
        name="docker-compose",
        description="Tool for defining and running multi-container Docker applications",
        category="containerization",
        install_command="brew install docker-compose",
        official_url="https://docs.docker.com/compose",
        github_url="https://github.com/docker/compose",
        popularity_score=0.92,
        keywords=["docker", "containers", "orchestration", "multi-container"],
    ),
    DevOpsTool(
        name="podman",
        description="Daemonless container engine for developing and running containers",
        category="containerization",
        install_command="brew install podman",
        official_url="https://podman.io",
        github_url="https://github.com/containers/podman",
        popularity_score=0.72,
        keywords=["container", "docker", "alternative", "daemonless"],
    ),
    DevOpsTool(
        name="buildah",
        description="Tool for building container images",
        category="containerization",
        install_command="brew install buildah",
        official_url="https://buildah.io",
        github_url="https://github.com/containers/buildah",
        popularity_score=0.69,
        keywords=["container", "images", "build", "oci"],
    ),
    DevOpsTool(
        name="skaffold",
        description="Command line tool for continuous development of Kubernetes applications",
        category="kubernetes",
        install_command="brew install skaffold",
        official_url="https://skaffold.dev",
        github_url="https://github.com/GoogleContainerTools/skaffold",
        popularity_score=0.73,
        keywords=["k8s", "kubernetes", "development", "ci-cd"],
    ),
]


DEVOPS_SERVICES = [
    DevOpsService(
        name="GitHub Actions",
        description="CI/CD platform integrated with GitHub for automated workflows",
        category="ci-cd",
        official_url="https://github.com/features/actions",
        integration_type="github",
        popularity_score=0.95,
        keywords=["github", "ci", "cd", "workflows", "automation"],
    ),
    DevOpsService(
        name="GitLab CI/CD",
        description="Built-in CI/CD in GitLab for automated testing and deployment",
        category="ci-cd",
        official_url="https://docs.gitlab.com/ee/ci/",
        integration_type="gitlab",
        popularity_score=0.85,
        keywords=["gitlab", "ci", "cd", "pipelines", "automation"],
    ),
    DevOpsService(
        name="CircleCI",
        description="Cloud-based CI/CD platform for automated testing and deployment",
        category="ci-cd",
        official_url="https://circleci.com",
        integration_type="saas",
        popularity_score=0.80,
        keywords=["ci", "cd", "cloud", "automation", "testing"],
    ),
    DevOpsService(
        name="Jenkins",
        description="Open-source automation server for building, testing, and deploying",
        category="ci-cd",
        official_url="https://www.jenkins.io",
        integration_type="self-hosted",
        popularity_score=0.88,
        keywords=["ci", "cd", "automation", "server", "self-hosted"],
    ),
    DevOpsService(
        name="Travis CI",
        description="Continuous integration platform for testing and deploying code",
        category="ci-cd",
        official_url="https://www.travis-ci.com",
        integration_type="saas",
        popularity_score=0.75,
        keywords=["ci", "testing", "automation", "cloud"],
    ),
    DevOpsService(
        name="GitHub Packages",
        description="Package hosting service integrated with GitHub",
        category="package-registry",
        official_url="https://github.com/features/packages",
        integration_type="github",
        popularity_score=0.82,
        keywords=["packages", "registry", "github", "artifacts"],
    ),
    DevOpsService(
        name="Docker Hub",
        description="Container image registry and repository",
        category="package-registry",
        official_url="https://hub.docker.com",
        integration_type="saas",
        popularity_score=0.93,
        keywords=["docker", "containers", "registry", "images"],
    ),
    DevOpsService(
        name="AWS CodePipeline",
        description="Fully managed continuous delivery service",
        category="ci-cd",
        official_url="https://aws.amazon.com/codepipeline",
        integration_type="aws",
        popularity_score=0.78,
        keywords=["aws", "ci", "cd", "pipeline", "automation"],
    ),
    DevOpsService(
        name="Azure DevOps",
        description="DevOps services for planning, developing, and deploying applications",
        category="ci-cd",
        official_url="https://azure.microsoft.com/services/devops",
        integration_type="azure",
        popularity_score=0.83,
        keywords=["azure", "devops", "ci", "cd", "pipelines"],
    ),
    DevOpsService(
        name="Google Cloud Build",
        description="Serverless CI/CD platform for building and testing code",
        category="ci-cd",
        official_url="https://cloud.google.com/build",
        integration_type="gcp",
        popularity_score=0.77,
        keywords=["gcp", "google", "ci", "cd", "build"],
    ),
]


def get_tools_by_category(category: str | None = None) -> list[DevOpsTool]:
    """Get tools filtered by category.

    Args:
        category: Category filter (optional)

    Returns:
        List of DevOpsTool objects
    """
    if category:
        return [tool for tool in DEVOPS_TOOLS if tool.category == category]
    return DEVOPS_TOOLS


def get_services_by_category(category: str | None = None) -> list[DevOpsService]:
    """Get services filtered by category.

    Args:
        category: Category filter (optional)

    Returns:
        List of DevOpsService objects
    """
    if category:
        return [service for service in DEVOPS_SERVICES if service.category == category]
    return DEVOPS_SERVICES

