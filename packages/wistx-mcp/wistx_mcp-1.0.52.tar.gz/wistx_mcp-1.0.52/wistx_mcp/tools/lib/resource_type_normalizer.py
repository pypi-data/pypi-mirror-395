"""Resource type normalization and mapping utilities."""

import logging
import re

from wistx_mcp.tools.lib.resource_type_loader import (
    get_cross_provider_equivalents,
    get_normalization_map,
)

logger = logging.getLogger(__name__)


def _build_normalization_map() -> dict[str, dict[str, str]]:
    """Build normalization maps for resource type variations.
    
    Returns:
        Dictionary mapping provider -> {normalized_key -> canonical_name}
    """
    normalization_map: dict[str, dict[str, str]] = {
        "aws": {},
        "gcp": {},
        "azure": {},
    }
    
    aws_map = normalization_map["aws"]
    gcp_map = normalization_map["gcp"]
    azure_map = normalization_map["azure"]
    
    fs_aws_map = get_normalization_map("aws")
    if fs_aws_map:
        aws_map.update(fs_aws_map)
    else:
        aws_map.update({
            "EC2": "EC2",
            "RDS": "RDS",
            "S3": "S3",
            "LAMBDA": "Lambda",
            "EKS": "EKS",
            "ECS": "ECS",
            "VPC": "VPC",
            "IAM": "IAM",
            "CLOUDFRONT": "CloudFront",
            "ROUTE53": "Route53",
            "ELASTICACHE": "ElastiCache",
            "DYNAMODB": "DynamoDB",
            "SQS": "SQS",
            "SNS": "SNS",
            "KMS": "KMS",
            "SECRETSMANAGER": "SecretsManager",
            "SECRETS_MANAGER": "SecretsManager",
            "CLOUDWATCH": "CloudWatch",
            "CLOUDWATCHLOGS": "CloudWatch Logs",
            "CLOUDWATCH_LOGS": "CloudWatch Logs",
            "ELB": "ELB",
            "ALB": "ALB",
            "NLB": "NLB",
            "EFS": "EFS",
            "EBS": "EBS",
            "REDSHIFT": "Redshift",
            "AURORA": "Aurora",
            "DOCUMENTDB": "DocumentDB",
            "NEPTUNE": "Neptune",
            "ELASTICSEARCH": "Elasticsearch",
            "OPENSEARCH": "OpenSearch",
            "MSK": "MSK",
            "MQ": "MQ",
            "EVENTBRIDGE": "EventBridge",
            "STEPFUNCTIONS": "StepFunctions",
            "APPSYNC": "AppSync",
            "APIGATEWAY": "API Gateway",
            "API_GATEWAY": "API Gateway",
            "COGNITO": "Cognito",
            "WAF": "WAF",
            "SHIELD": "Shield",
            "GUARDDUTY": "GuardDuty",
            "SECURITYHUB": "SecurityHub",
            "SECURITYGROUPS": "VPC",
            "SECURITY_GROUPS": "VPC",
            "SECURITYGROUP": "VPC",
            "SG": "VPC",
        })
    
    fs_gcp_map = get_normalization_map("gcp")
    if fs_gcp_map:
        gcp_map.update(fs_gcp_map)
    else:
        gcp_map.update({
            "GCE": "GCE",
            "COMPUTE": "GCE",
            "COMPUTEENGINE": "GCE",
            "COMPUTE_ENGINE": "GCE",
            "GOOGLECOMPUTEENGINE": "GCE",
            "GOOGLE_COMPUTE_ENGINE": "GCE",
            "CLOUDSQL": "Cloud SQL",
            "CLOUD_SQL": "Cloud SQL",
            "GKE": "GKE",
            "CLOUDSTORAGE": "Cloud Storage",
            "CLOUD_STORAGE": "Cloud Storage",
            "GCS": "Cloud Storage",
            "CLOUDFUNCTIONS": "Cloud Functions",
            "CLOUD_FUNCTIONS": "Cloud Functions",
            "CLOUDRUN": "Cloud Run",
            "CLOUD_RUN": "Cloud Run",
            "CLOUDBUILD": "Cloud Build",
            "CLOUD_BUILD": "Cloud Build",
            "CLOUDPUBSUB": "Cloud Pub/Sub",
            "CLOUD_PUB_SUB": "Cloud Pub/Sub",
            "PUBSUB": "Cloud Pub/Sub",
            "CLOUDBIGTABLE": "Cloud Bigtable",
            "CLOUD_BIGTABLE": "Cloud Bigtable",
            "CLOUDSPANNER": "Cloud Spanner",
            "CLOUD_SPANNER": "Cloud Spanner",
            "CLOUDFIRESTORE": "Cloud Firestore",
            "CLOUD_FIRESTORE": "Cloud Firestore",
            "FIRESTORE": "Cloud Firestore",
            "CLOUDDATASTORE": "Cloud Datastore",
            "CLOUD_DATASTORE": "Cloud Datastore",
            "DATASTORE": "Cloud Datastore",
            "CLOUDMEMORYSTORE": "Cloud Memorystore",
            "CLOUD_MEMORYSTORE": "Cloud Memorystore",
            "MEMORYSTORE": "Cloud Memorystore",
            "CLOUDLOADBALANCING": "Cloud Load Balancing",
            "CLOUD_LOAD_BALANCING": "Cloud Load Balancing",
            "LOADBALANCER": "Cloud Load Balancing",
            "CLOUDCDN": "Cloud CDN",
            "CLOUD_CDN": "Cloud CDN",
            "CDN": "Cloud CDN",
            "CLOUDIAM": "Cloud IAM",
            "CLOUD_IAM": "Cloud IAM",
            "IAM": "Cloud IAM",
            "CLOUDKMS": "Cloud KMS",
            "CLOUD_KMS": "Cloud KMS",
            "KMS": "Cloud KMS",
            "CLOUDSECRETMANAGER": "Cloud Secret Manager",
            "CLOUD_SECRET_MANAGER": "Cloud Secret Manager",
            "SECRETMANAGER": "Cloud Secret Manager",
            "SECRET_MANAGER": "Cloud Secret Manager",
            "CLOUDMONITORING": "Cloud Monitoring",
            "CLOUD_MONITORING": "Cloud Monitoring",
            "MONITORING": "Cloud Monitoring",
            "CLOUDLOGGING": "Cloud Logging",
            "CLOUD_LOGGING": "Cloud Logging",
            "LOGGING": "Cloud Logging",
            "CLOUDTRACE": "Cloud Trace",
            "CLOUD_TRACE": "Cloud Trace",
            "TRACE": "Cloud Trace",
            "CLOUDDEBUGGER": "Cloud Debugger",
            "CLOUD_DEBUGGER": "Cloud Debugger",
            "DEBUGGER": "Cloud Debugger",
            "CLOUDSCHEDULER": "Cloud Scheduler",
            "CLOUD_SCHEDULER": "Cloud Scheduler",
            "SCHEDULER": "Cloud Scheduler",
            "CLOUDTASKS": "Cloud Tasks",
            "CLOUD_TASKS": "Cloud Tasks",
            "TASKS": "Cloud Tasks",
            "CLOUDENDPOINTS": "Cloud Endpoints",
            "CLOUD_ENDPOINTS": "Cloud Endpoints",
            "ENDPOINTS": "Cloud Endpoints",
            "CLOUDARMOR": "Cloud Armor",
            "CLOUD_ARMOR": "Cloud Armor",
            "ARMOR": "Cloud Armor",
            "FIREWALL": "Cloud Armor",
            "CLOUDIDENTITY": "Cloud Identity",
            "CLOUD_IDENTITY": "Cloud Identity",
            "IDENTITY": "Cloud Identity",
            "CLOUDVPN": "Cloud VPN",
            "CLOUD_VPN": "Cloud VPN",
            "VPN": "Cloud VPN",
            "CLOUDINTERCONNECT": "Cloud Interconnect",
            "CLOUD_INTERCONNECT": "Cloud Interconnect",
            "INTERCONNECT": "Cloud Interconnect",
            "CLOUDNAT": "Cloud NAT",
            "CLOUD_NAT": "Cloud NAT",
            "NAT": "Cloud NAT",
            "CLOUDDNS": "Cloud DNS",
            "CLOUD_DNS": "Cloud DNS",
            "DNS": "Cloud DNS",
            "VPC": "Virtual Network",
            "VIRTUALNETWORK": "Virtual Network",
            "VIRTUAL_NETWORK": "Virtual Network",
        })
    
    fs_azure_map = get_normalization_map("azure")
    if fs_azure_map:
        azure_map.update(fs_azure_map)
    else:
        azure_map.update({
            "VIRTUALMACHINES": "Virtual Machines",
            "VIRTUAL_MACHINES": "Virtual Machines",
            "VM": "Virtual Machines",
            "VMS": "Virtual Machines",
            "VMSSCALESETS": "VM Scale Sets",
            "VM_SCALE_SETS": "VM Scale Sets",
            "SQLDATABASE": "SQL Database",
            "SQL_DATABASE": "SQL Database",
            "SQL": "SQL Database",
            "AZURESQL": "SQL Database",
            "AZURE_SQL": "SQL Database",
            "REDISCACHE": "Azure Cache for Redis",
            "REDIS_CACHE": "Azure Cache for Redis",
            "AZUREREDIS": "Azure Cache for Redis",
            "AZURE_REDIS": "Azure Cache for Redis",
            "AZURECACHEFORREDIS": "Azure Cache for Redis",
            "AZURE_CACHE_FOR_REDIS": "Azure Cache for Redis",
            "AZUREBLOBSTORAGE": "Blob Storage",
            "AZURE_BLOB_STORAGE": "Blob Storage",
            "AZUREFILESTORAGE": "File Storage",
            "AZURE_FILE_STORAGE": "File Storage",
            "AZUREQUEUESTORAGE": "Queue Storage",
            "AZURE_QUEUE_STORAGE": "Queue Storage",
            "AZURETABLESTORAGE": "Table Storage",
            "AZURE_TABLE_STORAGE": "Table Storage",
            "AZUREAPPSERVICE": "App Service",
            "AZURE_APP_SERVICE": "App Service",
            "COSMOSDB": "Cosmos DB",
            "COSMOS_DB": "Cosmos DB",
            "COSMOS": "Cosmos DB",
            "STORAGEACCOUNT": "Storage Account",
            "STORAGE_ACCOUNT": "Storage Account",
            "STORAGE": "Storage Account",
            "BLOBSTORAGE": "Blob Storage",
            "BLOB_STORAGE": "Blob Storage",
            "BLOB": "Blob Storage",
            "FILESTORAGE": "File Storage",
            "FILE_STORAGE": "File Storage",
            "QUEUESTORAGE": "Queue Storage",
            "QUEUE_STORAGE": "Queue Storage",
            "TABLESTORAGE": "Table Storage",
            "TABLE_STORAGE": "Table Storage",
            "AKS": "AKS",
            "CONTAINERINSTANCES": "Container Instances",
            "CONTAINER_INSTANCES": "Container Instances",
            "APPSERVICE": "App Service",
            "APP_SERVICE": "App Service",
            "FUNCTIONS": "Functions",
            "LOGICAPPS": "Logic Apps",
            "LOGIC_APPS": "Logic Apps",
            "SERVICEBUS": "Service Bus",
            "SERVICE_BUS": "Service Bus",
            "EVENTHUBS": "Event Hubs",
            "EVENT_HUBS": "Event Hubs",
            "EVENTGRID": "Event Grid",
            "EVENT_GRID": "Event Grid",
            "KEYVAULT": "Key Vault",
            "KEY_VAULT": "Key Vault",
            "ACTIVEDIRECTORY": "Active Directory",
            "ACTIVE_DIRECTORY": "Active Directory",
            "AD": "Active Directory",
            "APPLICATIONGATEWAY": "Application Gateway",
            "APPLICATION_GATEWAY": "Application Gateway",
            "LOADBALANCER": "Load Balancer",
            "LOAD_BALANCER": "Load Balancer",
            "FRONTDOOR": "Front Door",
            "FRONT_DOOR": "Front Door",
            "CDN": "CDN",
            "TRAFFICMANAGER": "Traffic Manager",
            "TRAFFIC_MANAGER": "Traffic Manager",
            "DNS": "DNS",
            "VIRTUALNETWORK": "Virtual Network",
            "VIRTUAL_NETWORK": "Virtual Network",
            "VPC": "Virtual Network",
            "VPNGATEWAY": "VPN Gateway",
            "VPN_GATEWAY": "VPN Gateway",
            "VPN": "VPN Gateway",
            "EXPRESSROUTE": "ExpressRoute",
            "EXPRESS_ROUTE": "ExpressRoute",
            "NETWORKSECURITYGROUP": "Network Security Group",
            "NETWORK_SECURITY_GROUP": "Network Security Group",
            "NSG": "Network Security Group",
            "APPLICATIONSECURITYGROUP": "Application Security Group",
            "APPLICATION_SECURITY_GROUP": "Application Security Group",
            "ASG": "Application Security Group",
            "FIREWALL": "Firewall",
            "DDOSPROTECTION": "DDoS Protection",
            "DDOS_PROTECTION": "DDoS Protection",
            "SECURITYCENTER": "Security Center",
            "SECURITY_CENTER": "Security Center",
            "SENTINEL": "Sentinel",
            "DEFENDER": "Defender",
            "POLICY": "Policy",
            "RESOURCEMANAGER": "Resource Manager",
            "RESOURCE_MANAGER": "Resource Manager",
            "MONITOR": "Monitor",
            "MONITORING": "Monitor",
            "LOGANALYTICS": "Log Analytics",
            "LOG_ANALYTICS": "Log Analytics",
            "LOGGING": "Log Analytics",
            "APPLICATIONINSIGHTS": "Application Insights",
            "APPLICATION_INSIGHTS": "Application Insights",
            "BACKUP": "Backup",
            "SITERECOVERY": "Site Recovery",
            "SITE_RECOVERY": "Site Recovery",
            "COSTMANAGEMENT": "Cost Management",
            "COST_MANAGEMENT": "Cost Management",
        })
    
    return normalization_map


def _build_cross_provider_map() -> dict[str, dict[str, str]]:
    """Build cross-provider resource type mappings.
    
    Loads from filesystem first, falls back to hardcoded mappings.
    
    Returns:
        Dictionary mapping {aws_type -> {target_provider -> equivalent_type}}
    """
    fs_map = get_cross_provider_equivalents("aws")
    if fs_map:
        return fs_map
    
    return {
        "VPC": {"gcp": "Virtual Network", "azure": "Virtual Network"},
        "IAM": {"gcp": "Cloud IAM", "azure": "Active Directory"},
        "KMS": {"gcp": "Cloud KMS", "azure": "Key Vault"},
        "SecretsManager": {"gcp": "Cloud Secret Manager", "azure": "Key Vault"},
        "CloudWatch": {"gcp": "Cloud Monitoring", "azure": "Monitor"},
        "CloudWatch Logs": {"gcp": "Cloud Logging", "azure": "Log Analytics"},
        "ELB": {"gcp": "Cloud Load Balancing", "azure": "Load Balancer"},
        "ALB": {"gcp": "Cloud Load Balancing", "azure": "Load Balancer"},
        "NLB": {"gcp": "Cloud Load Balancing", "azure": "Load Balancer"},
        "WAF": {"gcp": "Cloud Armor", "azure": "Front Door"},
        "RDS": {"gcp": "Cloud SQL", "azure": "SQL Database"},
        "EC2": {"gcp": "GCE", "azure": "Virtual Machines"},
        "EKS": {"gcp": "GKE", "azure": "AKS"},
        "Lambda": {"gcp": "Cloud Functions", "azure": "Functions"},
        "S3": {"gcp": "Cloud Storage", "azure": "Storage Account"},
        "Route53": {"gcp": "Cloud DNS", "azure": "DNS"},
    }


_NORMALIZATION_MAP = _build_normalization_map()
_CROSS_PROVIDER_MAP = _build_cross_provider_map()


def normalize_resource_type(
    resource_type: str,
    cloud_provider: str | list[str] | None = None,
) -> str:
    """Normalize a resource type to canonical form.
    
    Handles:
    - Case-insensitive matching
    - Abbreviation expansion (CLOUDSQL -> Cloud SQL)
    - Cross-provider mapping (VPC -> Virtual Network for GCP)
    - Fuzzy matching for common variations
    - Multi-cloud projects (uses first provider from list)
    
    Args:
        resource_type: Input resource type (may be abbreviated or variant)
        cloud_provider: Target cloud provider (aws, gcp, azure) or list of providers for multi-cloud projects
        
    Returns:
        Normalized resource type name
    """
    if not resource_type or not isinstance(resource_type, str):
        return resource_type
    
    original = resource_type.strip()
    normalized_key = re.sub(r"[_\s-]+", "", original.upper())
    
    provider_normalized = None
    if cloud_provider:
        if isinstance(cloud_provider, list):
            if len(cloud_provider) > 0 and isinstance(cloud_provider[0], str):
                provider_normalized = cloud_provider[0].strip().lower()
            else:
                provider_normalized = None
        elif isinstance(cloud_provider, str):
            provider_normalized = cloud_provider.strip().lower()
        else:
            provider_normalized = None
    
    normalized_result = None
    
    if provider_normalized and provider_normalized in _NORMALIZATION_MAP:
        provider_map = _NORMALIZATION_MAP[provider_normalized]
        
        if normalized_key in provider_map:
            normalized_result = provider_map[normalized_key]
        else:
            for aws_type, target_map in _CROSS_PROVIDER_MAP.items():
                aws_normalized = re.sub(r"[_\s-]+", "", aws_type.upper())
                if normalized_key == aws_normalized:
                    if provider_normalized in target_map:
                        mapped = target_map[provider_normalized]
                        logger.debug(
                            "Mapped AWS resource type '%s' to %s equivalent '%s'",
                            original,
                            provider_normalized.upper(),
                            mapped,
                        )
                        normalized_result = mapped
                        break
    
    if not normalized_result:
        for provider_map in _NORMALIZATION_MAP.values():
            if normalized_key in provider_map:
                normalized_result = provider_map[normalized_key]
                break
    
    if normalized_result and provider_normalized:
        normalized_result_key = re.sub(r"[_\s-]+", "", normalized_result.upper())
        for aws_type, target_map in _CROSS_PROVIDER_MAP.items():
            aws_normalized = re.sub(r"[_\s-]+", "", aws_type.upper())
            if normalized_result_key == aws_normalized:
                if provider_normalized in target_map:
                    final_mapped = target_map[provider_normalized]
                    logger.debug(
                        "Cross-provider mapped '%s' (normalized from '%s') to %s equivalent '%s'",
                        normalized_result,
                        original,
                        provider_normalized.upper(),
                        final_mapped,
                    )
                    return final_mapped
    
    return normalized_result if normalized_result else original


def normalize_resource_types(
    resource_types: list[str],
    cloud_provider: str | list[str] | None = None,
) -> list[str]:
    """Normalize a list of resource types.
    
    Args:
        resource_types: List of resource types to normalize
        cloud_provider: Target cloud provider (aws, gcp, azure) or list of providers for multi-cloud projects
        
    Returns:
        List of normalized resource types
    """
    if not resource_types:
        return []
    
    normalized = []
    for rt in resource_types:
        normalized_rt = normalize_resource_type(rt, cloud_provider)
        normalized.append(normalized_rt)
    
    return normalized

