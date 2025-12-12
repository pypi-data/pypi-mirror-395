"""AWS Cloud Discovery Provider.

Implements resource discovery for AWS using:
1. AWS Resource Explorer (primary) - https://docs.aws.amazon.com/resource-explorer/
2. Resource Groups Tagging API (fallback) - for accounts without Resource Explorer
3. Service-specific APIs (detailed info) - EC2, RDS, S3, etc.

Security:
- Uses only temporary credentials from STS AssumeRole
- Read-only operations only
- No data modification
"""

import asyncio
import logging
import re
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from wistx_mcp.models.cloud_discovery import (
    CloudProvider,
    DiscoveredResource,
    ImportPhase,
)
from wistx_mcp.tools.lib.cloud_discovery.base_provider import (
    CloudCredentials,
    CloudDiscoveryProvider,
)
from wistx_mcp.tools.lib.cloud_discovery.terraform_mapping_loader import (
    TerraformMapping,
    TerraformMappingLoader,
    get_terraform_mapping_loader,
)

logger = logging.getLogger(__name__)


class AWSDiscoveryProvider(CloudDiscoveryProvider):
    """AWS resource discovery using Resource Explorer and service APIs.
    
    Discovery Strategy:
    1. Try AWS Resource Explorer first (unified multi-region search)
    2. Fall back to Resource Groups Tagging API
    3. Use service-specific Describe APIs for detailed configuration
    
    Supported Resource Types:
    - EC2: Instances, VPCs, Subnets, Security Groups, EIPs, etc.
    - RDS: DB Instances, DB Clusters, Subnet Groups
    - S3: Buckets
    - Lambda: Functions
    - IAM: Roles, Policies, Instance Profiles
    - ELB: Load Balancers, Target Groups, Listeners
    - ECS/EKS: Clusters, Services, Task Definitions
    - And more (see aws_terraform_mappings.json)
    """
    
    # Default regions to scan if none specified
    DEFAULT_REGIONS = [
        "us-east-1", "us-east-2", "us-west-1", "us-west-2",
        "eu-west-1", "eu-west-2", "eu-central-1",
        "ap-southeast-1", "ap-southeast-2", "ap-northeast-1",
    ]
    
    # Thread pool for running boto3 calls asynchronously
    _executor = ThreadPoolExecutor(max_workers=10)
    
    def __init__(self, mapping_loader: TerraformMappingLoader | None = None):
        """Initialize the AWS discovery provider.
        
        Args:
            mapping_loader: Optional TerraformMappingLoader instance
        """
        self._mapping_loader = mapping_loader or get_terraform_mapping_loader()
        self._mappings: dict[str, TerraformMapping] | None = None
    
    @property
    def provider(self) -> CloudProvider:
        """Return AWS as the cloud provider."""
        return CloudProvider.AWS
    
    @property
    def supported_resource_types(self) -> list[str]:
        """Return list of supported AWS CloudFormation resource types."""
        return self._get_mappings_dict().keys()
    
    def _get_mappings_dict(self) -> dict[str, TerraformMapping]:
        """Get cached mappings dictionary."""
        if self._mappings is None:
            self._mappings = self._mapping_loader.load_mappings(CloudProvider.AWS)
        return self._mappings
    
    def _create_boto3_session(self, credentials: CloudCredentials) -> Any:
        """Create a boto3 session from credentials.
        
        Args:
            credentials: CloudCredentials with AWS temporary credentials
            
        Returns:
            boto3.Session configured with the credentials
        """
        import boto3
        
        creds = credentials.credentials
        return boto3.Session(
            aws_access_key_id=creds["access_key_id"],
            aws_secret_access_key=creds["secret_access_key"],
            aws_session_token=creds["session_token"],
        )
    
    async def discover_resources(
        self,
        credentials: CloudCredentials,
        regions: list[str] | None = None,
        resource_types: list[str] | None = None,
        tag_filters: dict[str, str] | None = None,
    ) -> list[DiscoveredResource]:
        """Discover AWS resources using Resource Explorer and fallback APIs.
        
        Args:
            credentials: Temporary AWS credentials from STS AssumeRole
            regions: Regions to scan (None = default regions)
            resource_types: CloudFormation types to discover (None = all supported)
            tag_filters: Filter by tags (e.g., {"Environment": "production"})
            
        Returns:
            List of discovered resources with metadata
        """
        regions = regions or self.DEFAULT_REGIONS
        mappings = self._get_mappings_dict()
        
        # Filter resource types if specified
        if resource_types:
            target_types = [t for t in resource_types if t in mappings]
        else:
            target_types = list(mappings.keys())
        
        logger.info(
            "Starting AWS discovery: %d regions, %d resource types",
            len(regions),
            len(target_types),
        )
        
        # Try Resource Explorer first
        resources = await self._discover_via_resource_explorer(
            credentials, regions, target_types, tag_filters
        )
        
        # If Resource Explorer returned nothing, fall back to tagging API
        if not resources:
            logger.info("Resource Explorer returned no results, trying Tagging API")
            resources = await self._discover_via_tagging_api(
                credentials, regions, target_types, tag_filters
            )
        
        logger.info("Discovered %d total resources", len(resources))
        return resources

    async def _discover_via_resource_explorer(
        self,
        credentials: CloudCredentials,
        regions: list[str],
        resource_types: list[str],
        tag_filters: dict[str, str] | None,
    ) -> list[DiscoveredResource]:
        """Discover resources using AWS Resource Explorer.

        Resource Explorer provides unified multi-region search.
        It must be enabled in the account and have an aggregator index.
        """
        session = self._create_boto3_session(credentials)
        resources: list[DiscoveredResource] = []

        try:
            # Resource Explorer is region-specific, try us-east-1 first
            client = session.client("resource-explorer-2", region_name="us-east-1")

            # Build query string
            query_parts = []

            # Add resource type filters
            if resource_types:
                # Convert CloudFormation types to Resource Explorer format
                # AWS::EC2::Instance -> resourcetype:ec2:instance
                type_filters = []
                for rt in resource_types[:10]:  # Limit to prevent query overflow
                    parts = rt.replace("AWS::", "").split("::")
                    if len(parts) >= 2:
                        type_filters.append(
                            f"resourcetype:{parts[0].lower()}:{parts[1].lower()}"
                        )
                if type_filters:
                    query_parts.append(f"({' OR '.join(type_filters)})")

            # Add tag filters
            if tag_filters:
                for key, value in tag_filters.items():
                    query_parts.append(f'tag:{key}="{value}"')

            # Add region filters
            if regions:
                region_filter = " OR ".join(f'region:"{r}"' for r in regions)
                query_parts.append(f"({region_filter})")

            query = " ".join(query_parts) if query_parts else "*"

            logger.debug("Resource Explorer query: %s", query)

            # Run search in thread pool (boto3 is synchronous)
            loop = asyncio.get_event_loop()

            def search_resources():
                all_resources = []
                paginator = client.get_paginator("search")

                for page in paginator.paginate(QueryString=query):
                    for resource in page.get("Resources", []):
                        all_resources.append(resource)

                return all_resources

            raw_resources = await loop.run_in_executor(
                self._executor, search_resources
            )

            logger.info(
                "Resource Explorer found %d raw resources", len(raw_resources)
            )

            # Convert to DiscoveredResource objects
            for raw in raw_resources:
                discovered = self._convert_resource_explorer_result(raw)
                if discovered:
                    resources.append(discovered)

        except Exception as e:
            # Resource Explorer may not be enabled
            logger.warning(
                "Resource Explorer search failed (may not be enabled): %s", e
            )

        return resources

    def _convert_resource_explorer_result(
        self,
        raw: dict[str, Any],
    ) -> DiscoveredResource | None:
        """Convert Resource Explorer result to DiscoveredResource."""
        try:
            arn = raw.get("Arn", "")
            resource_type_raw = raw.get("ResourceType", "")

            # Convert resource type to CloudFormation format
            # ec2:instance -> AWS::EC2::Instance
            parts = resource_type_raw.split(":")
            if len(parts) >= 2:
                cloud_type = f"AWS::{parts[0].upper()}::{parts[1].title().replace('-', '')}"
            else:
                return None

            # Check if we support this type
            mapping = self._get_mappings_dict().get(cloud_type)
            if not mapping:
                return None

            # Extract resource ID from ARN
            resource_id = self._extract_id_from_arn(arn, cloud_type)

            # Extract tags
            tags = {}
            for prop in raw.get("Properties", []):
                if prop.get("Name") == "tags":
                    # Tags are stored as JSON string
                    import json
                    try:
                        tag_data = json.loads(prop.get("Data", "[]"))
                        for tag in tag_data:
                            tags[tag.get("Key", "")] = tag.get("Value", "")
                    except json.JSONDecodeError:
                        pass

            # Get name from tags or resource ID
            name = tags.get("Name", resource_id)

            # Extract region from ARN
            arn_parts = arn.split(":")
            region = arn_parts[3] if len(arn_parts) > 3 else "us-east-1"

            return DiscoveredResource(
                cloud_provider=CloudProvider.AWS,
                cloud_resource_type=cloud_type,
                cloud_resource_id=resource_id,
                arn=arn,
                region=region,
                name=name,
                tags=tags,
                terraform_resource_type=mapping.terraform_type,
                import_phase=mapping.import_phase,
                raw_config={},  # Will be populated by get_resource_details
            )

        except Exception as e:
            logger.warning("Failed to convert resource: %s", e)
            return None

    def _extract_id_from_arn(self, arn: str, cloud_type: str) -> str:
        """Extract resource ID from ARN based on resource type."""
        # ARN format: arn:partition:service:region:account:resource
        parts = arn.split(":")

        if len(parts) < 6:
            return arn

        resource_part = ":".join(parts[5:])

        # Handle different ARN formats
        if "/" in resource_part:
            # Format: type/id or type/name/id
            return resource_part.split("/")[-1]
        elif ":" in resource_part:
            # Format: type:id
            return resource_part.split(":")[-1]
        else:
            return resource_part

    async def _discover_via_tagging_api(
        self,
        credentials: CloudCredentials,
        regions: list[str],
        resource_types: list[str],
        tag_filters: dict[str, str] | None,
    ) -> list[DiscoveredResource]:
        """Fallback discovery using Resource Groups Tagging API.

        This works in all accounts but requires scanning each region separately.
        """
        session = self._create_boto3_session(credentials)
        resources: list[DiscoveredResource] = []

        # Map CloudFormation types to tagging API resource type filters
        resource_type_filters = self._get_tagging_api_filters(resource_types)

        if not resource_type_filters:
            logger.warning("No valid resource type filters for Tagging API")
            return resources

        # Build tag filters
        api_tag_filters = []
        if tag_filters:
            for key, value in tag_filters.items():
                api_tag_filters.append({"Key": key, "Values": [value]})

        # Scan each region in parallel
        async def scan_region(region: str) -> list[DiscoveredResource]:
            region_resources = []
            try:
                client = session.client(
                    "resourcegroupstaggingapi", region_name=region
                )

                loop = asyncio.get_event_loop()

                def get_resources():
                    all_res = []
                    paginator = client.get_paginator("get_resources")

                    params = {
                        "ResourceTypeFilters": resource_type_filters[:100],
                    }
                    if api_tag_filters:
                        params["TagFilters"] = api_tag_filters

                    for page in paginator.paginate(**params):
                        for mapping in page.get("ResourceTagMappingList", []):
                            all_res.append(mapping)

                    return all_res

                raw_resources = await loop.run_in_executor(
                    self._executor, get_resources
                )

                for raw in raw_resources:
                    discovered = self._convert_tagging_result(raw, region)
                    if discovered:
                        region_resources.append(discovered)

                logger.debug(
                    "Tagging API found %d resources in %s",
                    len(region_resources),
                    region,
                )

            except Exception as e:
                logger.warning("Tagging API failed in %s: %s", region, e)

            return region_resources

        # Run all regions in parallel
        tasks = [scan_region(region) for region in regions]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, list):
                resources.extend(result)

        return resources

    def _get_tagging_api_filters(
        self,
        resource_types: list[str],
    ) -> list[str]:
        """Convert CloudFormation types to Tagging API resource type filters.

        Tagging API uses format: service:resource-type
        e.g., ec2:instance, rds:db, s3:bucket
        """
        filters = []

        for cf_type in resource_types:
            # AWS::EC2::Instance -> ec2:instance
            match = re.match(r"AWS::(\w+)::(\w+)", cf_type)
            if match:
                service = match.group(1).lower()
                resource = match.group(2).lower()

                # Handle special cases
                if service == "elasticloadbalancingv2":
                    service = "elasticloadbalancing"

                # Map resource names
                resource_map = {
                    "dbinstance": "db",
                    "dbcluster": "cluster",
                    "dbsubnetgroup": "subgrp",
                    "securitygroup": "security-group",
                    "internetgateway": "internet-gateway",
                    "natgateway": "natgateway",
                    "routetable": "route-table",
                    "networkinterface": "network-interface",
                    "launchtemplate": "launch-template",
                    "targetgroup": "targetgroup",
                    "loadbalancer": "loadbalancer",
                    "cachesubnetgroup": "subnetgroup",
                    "replicationgroup": "replicationgroup",
                    "cachecluster": "cluster",
                    "hostedzone": "hostedzone",
                }

                resource = resource_map.get(resource, resource)
                filters.append(f"{service}:{resource}")

        return list(set(filters))  # Remove duplicates

    def _convert_tagging_result(
        self,
        raw: dict[str, Any],
        region: str,
    ) -> DiscoveredResource | None:
        """Convert Tagging API result to DiscoveredResource."""
        try:
            arn = raw.get("ResourceARN", "")

            # Parse ARN to get resource type
            # arn:aws:ec2:us-east-1:123456789012:instance/i-1234567890abcdef0
            arn_parts = arn.split(":")
            if len(arn_parts) < 6:
                return None

            service = arn_parts[2]
            resource_part = ":".join(arn_parts[5:])

            # Determine CloudFormation type from ARN
            cloud_type = self._arn_to_cloudformation_type(service, resource_part)
            if not cloud_type:
                return None

            mapping = self._get_mappings_dict().get(cloud_type)
            if not mapping:
                return None

            # Extract resource ID
            resource_id = self._extract_id_from_arn(arn, cloud_type)

            # Extract tags
            tags = {}
            for tag in raw.get("Tags", []):
                tags[tag.get("Key", "")] = tag.get("Value", "")

            name = tags.get("Name", resource_id)

            return DiscoveredResource(
                cloud_provider=CloudProvider.AWS,
                cloud_resource_type=cloud_type,
                cloud_resource_id=resource_id,
                arn=arn,
                region=region,
                name=name,
                tags=tags,
                terraform_resource_type=mapping.terraform_type,
                import_phase=mapping.import_phase,
                raw_config={},
            )

        except Exception as e:
            logger.warning("Failed to convert tagging result: %s", e)
            return None

    def _arn_to_cloudformation_type(
        self,
        service: str,
        resource_part: str,
    ) -> str | None:
        """Convert ARN service and resource to CloudFormation type."""
        # Extract resource type from resource_part
        # instance/i-123 -> instance
        # db:mydb -> db
        if "/" in resource_part:
            resource_type = resource_part.split("/")[0]
        elif ":" in resource_part:
            resource_type = resource_part.split(":")[0]
        else:
            resource_type = resource_part

        # Map service:resource to CloudFormation type
        type_map = {
            ("ec2", "instance"): "AWS::EC2::Instance",
            ("ec2", "vpc"): "AWS::EC2::VPC",
            ("ec2", "subnet"): "AWS::EC2::Subnet",
            ("ec2", "security-group"): "AWS::EC2::SecurityGroup",
            ("ec2", "internet-gateway"): "AWS::EC2::InternetGateway",
            ("ec2", "natgateway"): "AWS::EC2::NatGateway",
            ("ec2", "route-table"): "AWS::EC2::RouteTable",
            ("ec2", "elastic-ip"): "AWS::EC2::EIP",
            ("ec2", "network-interface"): "AWS::EC2::NetworkInterface",
            ("ec2", "volume"): "AWS::EC2::Volume",
            ("ec2", "key-pair"): "AWS::EC2::KeyPair",
            ("ec2", "launch-template"): "AWS::EC2::LaunchTemplate",
            ("ec2", "vpc-peering-connection"): "AWS::EC2::VPCPeeringConnection",
            ("rds", "db"): "AWS::RDS::DBInstance",
            ("rds", "cluster"): "AWS::RDS::DBCluster",
            ("rds", "subgrp"): "AWS::RDS::DBSubnetGroup",
            ("s3", "bucket"): "AWS::S3::Bucket",
            ("lambda", "function"): "AWS::Lambda::Function",
            ("iam", "role"): "AWS::IAM::Role",
            ("iam", "policy"): "AWS::IAM::Policy",
            ("iam", "instance-profile"): "AWS::IAM::InstanceProfile",
            ("elasticloadbalancing", "loadbalancer"): "AWS::ElasticLoadBalancingV2::LoadBalancer",
            ("elasticloadbalancing", "targetgroup"): "AWS::ElasticLoadBalancingV2::TargetGroup",
            ("ecs", "cluster"): "AWS::ECS::Cluster",
            ("ecs", "service"): "AWS::ECS::Service",
            ("ecs", "task-definition"): "AWS::ECS::TaskDefinition",
            ("eks", "cluster"): "AWS::EKS::Cluster",
            ("eks", "nodegroup"): "AWS::EKS::Nodegroup",
            ("dynamodb", "table"): "AWS::DynamoDB::Table",
            ("elasticache", "cluster"): "AWS::ElastiCache::CacheCluster",
            ("elasticache", "replicationgroup"): "AWS::ElastiCache::ReplicationGroup",
            ("sns", "topic"): "AWS::SNS::Topic",
            ("sqs", "queue"): "AWS::SQS::Queue",
            ("kms", "key"): "AWS::KMS::Key",
            ("kms", "alias"): "AWS::KMS::Alias",
            ("logs", "log-group"): "AWS::Logs::LogGroup",
            ("route53", "hostedzone"): "AWS::Route53::HostedZone",
            ("cloudfront", "distribution"): "AWS::CloudFront::Distribution",
            ("acm", "certificate"): "AWS::CertificateManager::Certificate",
            ("secretsmanager", "secret"): "AWS::SecretsManager::Secret",
            ("ssm", "parameter"): "AWS::SSM::Parameter",
            ("autoscaling", "autoScalingGroup"): "AWS::AutoScaling::AutoScalingGroup",
        }

        return type_map.get((service.lower(), resource_type.lower()))

    def get_terraform_resource_type(self, cloud_resource_type: str) -> str:
        """Map AWS CloudFormation type to Terraform resource type."""
        mapping = self._get_mappings_dict().get(cloud_resource_type)
        if mapping:
            return mapping.terraform_type

        # Fallback: convert AWS::Service::Resource to aws_service_resource
        match = re.match(r"AWS::(\w+)::(\w+)", cloud_resource_type)
        if match:
            service = match.group(1).lower()
            resource = re.sub(r"(?<!^)(?=[A-Z])", "_", match.group(2)).lower()
            return f"aws_{service}_{resource}"

        return cloud_resource_type.lower().replace("::", "_")

    def get_terraform_import_id(self, resource: DiscoveredResource) -> str:
        """Get the ID to use for terraform import command."""
        mapping = self._get_mappings_dict().get(resource.cloud_resource_type)

        if mapping and mapping.import_id_template:
            # Template uses {PropertyName} placeholders
            template = mapping.import_id_template

            # Common substitutions
            substitutions = {
                "{InstanceId}": resource.cloud_resource_id,
                "{VpcId}": resource.cloud_resource_id,
                "{SubnetId}": resource.cloud_resource_id,
                "{GroupId}": resource.cloud_resource_id,
                "{InternetGatewayId}": resource.cloud_resource_id,
                "{NatGatewayId}": resource.cloud_resource_id,
                "{RouteTableId}": resource.cloud_resource_id,
                "{AllocationId}": resource.cloud_resource_id,
                "{NetworkInterfaceId}": resource.cloud_resource_id,
                "{VolumeId}": resource.cloud_resource_id,
                "{KeyName}": resource.cloud_resource_id,
                "{DBInstanceIdentifier}": resource.cloud_resource_id,
                "{DBClusterIdentifier}": resource.cloud_resource_id,
                "{DBSubnetGroupName}": resource.cloud_resource_id,
                "{BucketName}": resource.cloud_resource_id,
                "{FunctionName}": resource.cloud_resource_id,
                "{RoleName}": resource.cloud_resource_id,
                "{Arn}": resource.arn or resource.cloud_resource_id,
                "{PolicyName}": resource.cloud_resource_id,
                "{InstanceProfileName}": resource.cloud_resource_id,
                "{LoadBalancerArn}": resource.arn or resource.cloud_resource_id,
                "{TargetGroupArn}": resource.arn or resource.cloud_resource_id,
                "{ListenerArn}": resource.arn or resource.cloud_resource_id,
                "{ClusterArn}": resource.arn or resource.cloud_resource_id,
                "{ServiceName}": resource.cloud_resource_id,
                "{TaskDefinitionArn}": resource.arn or resource.cloud_resource_id,
                "{Name}": resource.cloud_resource_id,
                "{NodegroupName}": resource.cloud_resource_id,
                "{TableName}": resource.cloud_resource_id,
                "{CacheClusterId}": resource.cloud_resource_id,
                "{ReplicationGroupId}": resource.cloud_resource_id,
                "{TopicArn}": resource.arn or resource.cloud_resource_id,
                "{QueueUrl}": resource.cloud_resource_id,
                "{KeyId}": resource.cloud_resource_id,
                "{AliasName}": resource.cloud_resource_id,
                "{AlarmName}": resource.cloud_resource_id,
                "{LogGroupName}": resource.cloud_resource_id,
                "{Id}": resource.cloud_resource_id,
                "{ARN}": resource.arn or resource.cloud_resource_id,
                "{LaunchTemplateId}": resource.cloud_resource_id,
                "{AutoScalingGroupName}": resource.cloud_resource_id,
                "{VpcPeeringConnectionId}": resource.cloud_resource_id,
            }

            result = template
            for placeholder, value in substitutions.items():
                result = result.replace(placeholder, value)

            return result

        # Default to resource ID
        return resource.cloud_resource_id

    async def get_available_regions(
        self,
        credentials: CloudCredentials,
    ) -> list[str]:
        """Get list of enabled AWS regions for the account."""
        session = self._create_boto3_session(credentials)

        try:
            # EC2 client can list regions
            client = session.client("ec2", region_name="us-east-1")

            loop = asyncio.get_event_loop()

            def describe_regions():
                response = client.describe_regions(
                    Filters=[{"Name": "opt-in-status", "Values": ["opt-in-not-required", "opted-in"]}]
                )
                return [r["RegionName"] for r in response.get("Regions", [])]

            regions = await loop.run_in_executor(self._executor, describe_regions)

            logger.info("Found %d enabled regions", len(regions))
            return regions

        except Exception as e:
            logger.warning("Failed to list regions, using defaults: %s", e)
            return self.DEFAULT_REGIONS

    async def get_resource_details(
        self,
        credentials: CloudCredentials,
        resource: DiscoveredResource,
    ) -> dict[str, Any]:
        """Get detailed configuration for a specific AWS resource."""
        session = self._create_boto3_session(credentials)
        region = resource.region or "us-east-1"

        # Map resource types to describe functions
        describe_handlers = {
            "AWS::EC2::Instance": self._describe_ec2_instance,
            "AWS::EC2::VPC": self._describe_vpc,
            "AWS::EC2::Subnet": self._describe_subnet,
            "AWS::EC2::SecurityGroup": self._describe_security_group,
            "AWS::RDS::DBInstance": self._describe_rds_instance,
            "AWS::S3::Bucket": self._describe_s3_bucket,
            "AWS::Lambda::Function": self._describe_lambda_function,
        }

        handler = describe_handlers.get(resource.cloud_resource_type)

        if handler:
            try:
                return await handler(session, region, resource.cloud_resource_id)
            except Exception as e:
                logger.warning(
                    "Failed to get details for %s: %s",
                    resource.cloud_resource_id,
                    e,
                )

        return {}

    async def _describe_ec2_instance(
        self, session: Any, region: str, instance_id: str
    ) -> dict[str, Any]:
        """Get EC2 instance details."""
        client = session.client("ec2", region_name=region)
        loop = asyncio.get_event_loop()

        def describe():
            response = client.describe_instances(InstanceIds=[instance_id])
            if response["Reservations"]:
                return response["Reservations"][0]["Instances"][0]
            return {}

        return await loop.run_in_executor(self._executor, describe)

    async def _describe_vpc(
        self, session: Any, region: str, vpc_id: str
    ) -> dict[str, Any]:
        """Get VPC details."""
        client = session.client("ec2", region_name=region)
        loop = asyncio.get_event_loop()

        def describe():
            response = client.describe_vpcs(VpcIds=[vpc_id])
            if response["Vpcs"]:
                return response["Vpcs"][0]
            return {}

        return await loop.run_in_executor(self._executor, describe)

    async def _describe_subnet(
        self, session: Any, region: str, subnet_id: str
    ) -> dict[str, Any]:
        """Get Subnet details."""
        client = session.client("ec2", region_name=region)
        loop = asyncio.get_event_loop()

        def describe():
            response = client.describe_subnets(SubnetIds=[subnet_id])
            if response["Subnets"]:
                return response["Subnets"][0]
            return {}

        return await loop.run_in_executor(self._executor, describe)

    async def _describe_security_group(
        self, session: Any, region: str, group_id: str
    ) -> dict[str, Any]:
        """Get Security Group details."""
        client = session.client("ec2", region_name=region)
        loop = asyncio.get_event_loop()

        def describe():
            response = client.describe_security_groups(GroupIds=[group_id])
            if response["SecurityGroups"]:
                return response["SecurityGroups"][0]
            return {}

        return await loop.run_in_executor(self._executor, describe)

    async def _describe_rds_instance(
        self, session: Any, region: str, db_id: str
    ) -> dict[str, Any]:
        """Get RDS instance details."""
        client = session.client("rds", region_name=region)
        loop = asyncio.get_event_loop()

        def describe():
            response = client.describe_db_instances(DBInstanceIdentifier=db_id)
            if response["DBInstances"]:
                return response["DBInstances"][0]
            return {}

        return await loop.run_in_executor(self._executor, describe)

    async def _describe_s3_bucket(
        self, session: Any, region: str, bucket_name: str
    ) -> dict[str, Any]:
        """Get S3 bucket details."""
        client = session.client("s3", region_name=region)
        loop = asyncio.get_event_loop()

        def describe():
            details = {"Name": bucket_name}

            try:
                location = client.get_bucket_location(Bucket=bucket_name)
                details["Location"] = location.get("LocationConstraint", "us-east-1")
            except Exception:
                pass

            try:
                tags = client.get_bucket_tagging(Bucket=bucket_name)
                details["Tags"] = tags.get("TagSet", [])
            except Exception:
                details["Tags"] = []

            return details

        return await loop.run_in_executor(self._executor, describe)

    async def _describe_lambda_function(
        self, session: Any, region: str, function_name: str
    ) -> dict[str, Any]:
        """Get Lambda function details."""
        client = session.client("lambda", region_name=region)
        loop = asyncio.get_event_loop()

        def describe():
            response = client.get_function(FunctionName=function_name)
            return response.get("Configuration", {})

        return await loop.run_in_executor(self._executor, describe)

