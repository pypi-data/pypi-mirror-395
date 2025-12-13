"""Official Documentation Registry for WISTX domains.

Maps technologies to their official documentation URLs for on-demand research.
Focused on DevOps, Infrastructure, Compliance, FinOps, and Platform Engineering.

This registry is used by the SourceDiscoveryService to find authoritative
documentation sources when users don't provide explicit URLs.
"""

from typing import TypedDict


class DocSource(TypedDict, total=False):
    """Documentation source configuration."""
    base_url: str
    docs_path: str
    api_path: str | None
    github_repo: str | None
    priority: int  # 1 = highest priority


# Infrastructure as Code
IAC_DOCS = {
    "terraform": DocSource(
        base_url="developer.hashicorp.com",
        docs_path="/terraform/docs",
        api_path="/terraform/language",
        github_repo="hashicorp/terraform",
        priority=1,
    ),
    "opentofu": DocSource(
        base_url="opentofu.org",
        docs_path="/docs",
        github_repo="opentofu/opentofu",
        priority=1,
    ),
    "pulumi": DocSource(
        base_url="pulumi.com",
        docs_path="/docs",
        api_path="/registry",
        github_repo="pulumi/pulumi",
        priority=1,
    ),
    "cloudformation": DocSource(
        base_url="docs.aws.amazon.com",
        docs_path="/AWSCloudFormation/latest/UserGuide",
        api_path="/AWSCloudFormation/latest/APIReference",
        priority=1,
    ),
    "bicep": DocSource(
        base_url="learn.microsoft.com",
        docs_path="/en-us/azure/azure-resource-manager/bicep",
        github_repo="Azure/bicep",
        priority=1,
    ),
    "ansible": DocSource(
        base_url="docs.ansible.com",
        docs_path="/ansible/latest",
        github_repo="ansible/ansible",
        priority=1,
    ),
    "crossplane": DocSource(
        base_url="docs.crossplane.io",
        docs_path="/latest",
        github_repo="crossplane/crossplane",
        priority=1,
    ),
    "cdk": DocSource(
        base_url="docs.aws.amazon.com",
        docs_path="/cdk/v2/guide",
        api_path="/cdk/api/v2",
        github_repo="aws/aws-cdk",
        priority=1,
    ),
    "cdktf": DocSource(
        base_url="developer.hashicorp.com",
        docs_path="/terraform/cdktf",
        github_repo="hashicorp/terraform-cdk",
        priority=1,
    ),
}

# Kubernetes & Containers
KUBERNETES_DOCS = {
    "kubernetes": DocSource(
        base_url="kubernetes.io",
        docs_path="/docs",
        api_path="/docs/reference/kubernetes-api",
        github_repo="kubernetes/kubernetes",
        priority=1,
    ),
    "k8s": DocSource(
        base_url="kubernetes.io",
        docs_path="/docs",
        priority=1,
    ),
    "helm": DocSource(
        base_url="helm.sh",
        docs_path="/docs",
        github_repo="helm/helm",
        priority=1,
    ),
    "kustomize": DocSource(
        base_url="kubectl.docs.kubernetes.io",
        docs_path="/references/kustomize",
        github_repo="kubernetes-sigs/kustomize",
        priority=1,
    ),
    "karpenter": DocSource(
        base_url="karpenter.sh",
        docs_path="/docs",
        github_repo="aws/karpenter",
        priority=1,
    ),
    "istio": DocSource(
        base_url="istio.io",
        docs_path="/latest/docs",
        github_repo="istio/istio",
        priority=1,
    ),
    "linkerd": DocSource(
        base_url="linkerd.io",
        docs_path="/2/docs",
        github_repo="linkerd/linkerd2",
        priority=1,
    ),
    "cilium": DocSource(
        base_url="docs.cilium.io",
        docs_path="/en/stable",
        github_repo="cilium/cilium",
        priority=1,
    ),
    "argocd": DocSource(
        base_url="argo-cd.readthedocs.io",
        docs_path="/en/stable",
        github_repo="argoproj/argo-cd",
        priority=1,
    ),
    "flux": DocSource(
        base_url="fluxcd.io",
        docs_path="/flux",
        github_repo="fluxcd/flux2",
        priority=1,
    ),
}

# Containers
CONTAINER_DOCS = {
    "docker": DocSource(
        base_url="docs.docker.com",
        docs_path="/",
        github_repo="docker/docs",
        priority=1,
    ),
    "containerd": DocSource(
        base_url="containerd.io",
        docs_path="/docs",
        github_repo="containerd/containerd",
        priority=1,
    ),
    "podman": DocSource(
        base_url="docs.podman.io",
        docs_path="/en/latest",
        github_repo="containers/podman",
        priority=1,
    ),
}

# CI/CD
CICD_DOCS = {
    "github actions": DocSource(
        base_url="docs.github.com",
        docs_path="/en/actions",
        priority=1,
    ),
    "gitlab ci": DocSource(
        base_url="docs.gitlab.com",
        docs_path="/ee/ci",
        priority=1,
    ),
    "jenkins": DocSource(
        base_url="www.jenkins.io",
        docs_path="/doc",
        github_repo="jenkinsci/jenkins",
        priority=1,
    ),
    "circleci": DocSource(
        base_url="circleci.com",
        docs_path="/docs",
        priority=1,
    ),
    "tekton": DocSource(
        base_url="tekton.dev",
        docs_path="/docs",
        github_repo="tektoncd/pipeline",
        priority=1,
    ),
    "argo workflows": DocSource(
        base_url="argo-workflows.readthedocs.io",
        docs_path="/en/latest",
        github_repo="argoproj/argo-workflows",
        priority=1,
    ),
}

# Monitoring & Observability
MONITORING_DOCS = {
    "prometheus": DocSource(
        base_url="prometheus.io",
        docs_path="/docs",
        github_repo="prometheus/prometheus",
        priority=1,
    ),
    "grafana": DocSource(
        base_url="grafana.com",
        docs_path="/docs/grafana/latest",
        github_repo="grafana/grafana",
        priority=1,
    ),
    "datadog": DocSource(
        base_url="docs.datadoghq.com",
        docs_path="/",
        priority=1,
    ),
    "opentelemetry": DocSource(
        base_url="opentelemetry.io",
        docs_path="/docs",
        github_repo="open-telemetry/opentelemetry-specification",
        priority=1,
    ),
    "jaeger": DocSource(
        base_url="www.jaegertracing.io",
        docs_path="/docs",
        github_repo="jaegertracing/jaeger",
        priority=1,
    ),
    "loki": DocSource(
        base_url="grafana.com",
        docs_path="/docs/loki/latest",
        github_repo="grafana/loki",
        priority=1,
    ),
}

# Cloud Providers
CLOUD_DOCS = {
    "aws": DocSource(
        base_url="docs.aws.amazon.com",
        docs_path="/",
        priority=1,
    ),
    "azure": DocSource(
        base_url="learn.microsoft.com",
        docs_path="/en-us/azure",
        priority=1,
    ),
    "gcp": DocSource(
        base_url="cloud.google.com",
        docs_path="/docs",
        priority=1,
    ),
}

# Security Tools
SECURITY_DOCS = {
    "vault": DocSource(
        base_url="developer.hashicorp.com",
        docs_path="/vault/docs",
        github_repo="hashicorp/vault",
        priority=1,
    ),
    "opa": DocSource(
        base_url="www.openpolicyagent.org",
        docs_path="/docs/latest",
        github_repo="open-policy-agent/opa",
        priority=1,
    ),
    "kyverno": DocSource(
        base_url="kyverno.io",
        docs_path="/docs",
        github_repo="kyverno/kyverno",
        priority=1,
    ),
    "falco": DocSource(
        base_url="falco.org",
        docs_path="/docs",
        github_repo="falcosecurity/falco",
        priority=1,
    ),
    "trivy": DocSource(
        base_url="aquasecurity.github.io",
        docs_path="/trivy",
        github_repo="aquasecurity/trivy",
        priority=1,
    ),
    "checkov": DocSource(
        base_url="www.checkov.io",
        docs_path="/docs",
        github_repo="bridgecrewio/checkov",
        priority=1,
    ),
}

# FinOps Tools
FINOPS_DOCS = {
    "kubecost": DocSource(
        base_url="docs.kubecost.com",
        docs_path="/",
        github_repo="kubecost/cost-analyzer-helm-chart",
        priority=1,
    ),
    "infracost": DocSource(
        base_url="www.infracost.io",
        docs_path="/docs",
        github_repo="infracost/infracost",
        priority=1,
    ),
}


# Combined registry for easy lookup
OFFICIAL_DOCS_REGISTRY: dict[str, DocSource] = {
    **IAC_DOCS,
    **KUBERNETES_DOCS,
    **CONTAINER_DOCS,
    **CICD_DOCS,
    **MONITORING_DOCS,
    **CLOUD_DOCS,
    **SECURITY_DOCS,
    **FINOPS_DOCS,
}


def get_doc_source(technology: str) -> DocSource | None:
    """Get documentation source for a technology.

    Args:
        technology: Technology name (case-insensitive)

    Returns:
        DocSource configuration or None if not found
    """
    return OFFICIAL_DOCS_REGISTRY.get(technology.lower())


def get_docs_url(technology: str) -> str | None:
    """Get the full documentation URL for a technology.

    Args:
        technology: Technology name (case-insensitive)

    Returns:
        Full documentation URL or None if not found
    """
    source = get_doc_source(technology)
    if not source:
        return None

    base = source["base_url"]
    path = source.get("docs_path", "")
    return f"https://{base}{path}"


def get_all_technologies() -> list[str]:
    """Get list of all registered technologies.

    Returns:
        List of technology names
    """
    return list(OFFICIAL_DOCS_REGISTRY.keys())

