"""Script to populate and deduplicate resource types from JSON files."""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "resource_types"


def deduplicate_and_enhance_aws() -> None:
    """Deduplicate and enhance AWS resource types."""
    file_path = DATA_DIR / "aws.json"
    
    with open(file_path, "r") as f:
        data = json.load(f)
    
    resource_types = list(set(data["resource_types"]))
    resource_types.sort()
    
    additional_types = [
        "Batch",
        "Elastic Beanstalk",
        "Fargate",
        "Outposts",
        "Snowball",
        "Snowmobile",
        "Storage Gateway",
        "Transfer Family",
        "DataSync",
        "Backup",
        "Elastic Disaster Recovery",
        "Resilience Hub",
        "Application Recovery Controller",
        "Route 53",
        "Route 53 Resolver",
        "PrivateLink",
        "Direct Connect",
        "Transit Gateway",
        "Cloud WAN",
        "Global Accelerator",
        "App Mesh",
        "Cloud Map",
        "Service Discovery",
        "Elastic Load Balancing",
        "Network Load Balancer",
        "Application Load Balancer",
        "Classic Load Balancer",
        "Gateway Load Balancer",
        "VPC",
        "VPN",
        "WAF",
        "Shield",
        "Firewall Manager",
        "Network Firewall",
        "Route 53 Resolver DNS Firewall",
        "GuardDuty",
        "Security Hub",
        "Inspector",
        "Macie",
        "Config",
        "CloudTrail",
        "Artifact",
        "Certificate Manager",
        "Secrets Manager",
        "Key Management Service",
        "CloudHSM",
        "Directory Service",
        "Cognito",
        "IAM",
        "IAM Identity Center",
        "Resource Access Manager",
        "Organizations",
        "Control Tower",
        "Service Control Policies",
        "Tag Policies",
        "Resource Groups",
        "Tag Editor",
        "Systems Manager",
        "Systems Manager Parameter Store",
        "Systems Manager Session Manager",
        "Systems Manager Patch Manager",
        "Systems Manager State Manager",
        "Systems Manager Automation",
        "Systems Manager Run Command",
        "Systems Manager Inventory",
        "Systems Manager Maintenance Windows",
        "Systems Manager Distributor",
        "Systems Manager Change Manager",
        "Systems Manager Application Manager",
        "Systems Manager Incident Manager",
        "Systems Manager OpsCenter",
        "CloudWatch",
        "CloudWatch Logs",
        "CloudWatch Metrics",
        "CloudWatch Alarms",
        "CloudWatch Dashboards",
        "CloudWatch Insights",
        "CloudWatch Synthetics",
        "CloudWatch RUM",
        "CloudWatch Evidently",
        "CloudWatch Contributor Insights",
        "CloudWatch Anomaly Detection",
        "X-Ray",
        "ServiceLens",
        "CloudTrail",
        "Config",
        "Trusted Advisor",
        "Personal Health Dashboard",
        "Systems Manager Explorer",
        "Systems Manager OpsCenter",
        "Cost Explorer",
        "Budgets",
        "Cost Anomaly Detection",
        "Reserved Instance Reporting",
        "Savings Plans",
        "Billing",
        "Marketplace",
        "Support",
        "Well-Architected Tool",
        "Migration Hub",
        "Application Discovery Service",
        "Database Migration Service",
        "Server Migration Service",
        "VMware Cloud on AWS",
        "Snow Family",
        "DataSync",
        "Storage Gateway",
        "Transfer Family",
    ]
    
    resource_types.extend(additional_types)
    resource_types = sorted(list(set(resource_types)))
    
    data["resource_types"] = resource_types
    
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"AWS: {len(resource_types)} unique resource types")


def deduplicate_and_enhance_gcp() -> None:
    """Deduplicate and enhance GCP resource types."""
    file_path = DATA_DIR / "gcp.json"
    
    with open(file_path, "r") as f:
        data = json.load(f)
    
    resource_types = list(set(data["resource_types"]))
    resource_types.sort()
    
    additional_types = [
        "App Engine",
        "Cloud Run",
        "Cloud Functions",
        "GKE",
        "Cloud Build",
        "Cloud Deploy",
        "Artifact Registry",
        "Container Registry",
        "Cloud Source Repositories",
        "Cloud Scheduler",
        "Cloud Tasks",
        "Cloud Workflows",
        "Cloud Endpoints",
        "API Gateway",
        "Cloud Armor",
        "Cloud CDN",
        "Cloud Load Balancing",
        "Cloud DNS",
        "Cloud Domains",
        "Cloud Interconnect",
        "Cloud VPN",
        "Cloud NAT",
        "VPC",
        "Virtual Private Cloud",
        "Cloud Router",
        "Cloud Firewall",
        "Cloud IDS",
        "Cloud Security Command Center",
        "Cloud DLP",
        "Cloud IAP",
        "Cloud Identity",
        "Cloud IAM",
        "Cloud KMS",
        "Cloud Secret Manager",
        "Cloud Resource Manager",
        "Cloud Asset",
        "Cloud Billing",
        "Cloud Cost Management",
        "Cloud Monitoring",
        "Cloud Logging",
        "Cloud Trace",
        "Cloud Debugger",
        "Cloud Profiler",
        "Cloud Error Reporting",
        "Cloud Source Repositories",
        "Cloud Build",
        "Cloud Deploy",
        "Artifact Registry",
        "Container Registry",
    ]
    
    resource_types.extend(additional_types)
    resource_types = sorted(list(set(resource_types)))
    
    data["resource_types"] = resource_types
    
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"GCP: {len(resource_types)} unique resource types")


def deduplicate_and_enhance_azure() -> None:
    """Deduplicate and enhance Azure resource types."""
    file_path = DATA_DIR / "azure.json"
    
    with open(file_path, "r") as f:
        data = json.load(f)
    
    resource_types = list(set(data["resource_types"]))
    resource_types.sort()
    
    additional_types = [
        "Azure Arc",
        "Azure Purview",
        "Azure Synapse Analytics",
        "Azure Databricks",
        "Azure HDInsight",
        "Azure Stream Analytics",
        "Azure Data Factory",
        "Azure Data Lake",
        "Azure Data Share",
        "Azure Data Explorer",
        "Azure Time Series Insights",
        "Azure Digital Twins",
        "Azure IoT Hub",
        "Azure IoT Central",
        "Azure Sphere",
        "Azure Maps",
        "Azure Cognitive Services",
        "Azure Machine Learning",
        "Azure Bot Service",
        "Azure Search",
        "Azure Form Recognizer",
        "Azure Video Analyzer",
        "Azure Media Services",
        "Azure Communication Services",
        "Azure SignalR",
        "Azure Notification Hubs",
        "Azure API Management",
        "Azure Service Fabric",
        "Azure Spring Cloud",
        "Azure Container Apps",
        "Azure Static Web Apps",
        "Azure Red Hat OpenShift",
        "Azure Kubernetes Service",
        "Azure Container Instances",
        "Azure Batch",
        "Azure Service Bus",
        "Azure Event Hubs",
        "Azure Event Grid",
        "Azure Relay",
        "Azure Queue Storage",
        "Azure Service Bus Queues",
        "Azure Service Bus Topics",
    ]
    
    resource_types.extend(additional_types)
    resource_types = sorted(list(set(resource_types)))
    
    data["resource_types"] = resource_types
    
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Azure: {len(resource_types)} unique resource types")


if __name__ == "__main__":
    print("Deduplicating and enhancing resource types...")
    deduplicate_and_enhance_aws()
    deduplicate_and_enhance_gcp()
    deduplicate_and_enhance_azure()
    print("Done!")

