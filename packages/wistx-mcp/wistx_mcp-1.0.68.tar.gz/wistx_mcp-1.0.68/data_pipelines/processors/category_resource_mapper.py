"""Category-based resource mapping for compliance controls.

Maps compliance control categories/subcategories to cloud resources across
AWS, Azure, Google Cloud Platform, and Oracle Cloud Infrastructure.
"""


class CategoryResourceMapper:
    """Maps compliance control categories to cloud resources.

    Provides inference of applicable cloud resources based on control categories
    and subcategories, supporting AWS, Azure, GCP, and Oracle Cloud.
    """

    def __init__(self):
        """Initialize resource mapper with comprehensive mappings."""
        self.mapping = self._build_mapping()

    def _build_mapping(self) -> dict[str, dict[str | None, list[str]]]:
        """Build comprehensive category-to-resource mapping.

        Returns:
            Nested dictionary: category -> subcategory -> list of resource IDs
        """
        return {
            "network_security": {
                "firewall": [
                    "AWS::EC2::SecurityGroup",
                    "AWS::EC2::NetworkAcl",
                    "AWS::WAF::WebACL",
                    "AWS::WAFv2::WebACL",
                    "Azure::Network::NetworkSecurityGroup",
                    "Azure::Network::ApplicationGateway",
                    "Azure::Network::Firewall",
                    "Azure::Network::DdosProtectionPlan",
                    "GCP::Compute::Firewall",
                    "GCP::Compute::Network",
                    "GCP::Compute::BackendService",
                    "OCI::Network::SecurityList",
                    "OCI::Network::NetworkSecurityGroup",
                    "OCI::Network::Firewall",
                ],
                "network_segmentation": [
                    "AWS::EC2::VPC",
                    "AWS::EC2::Subnet",
                    "AWS::EC2::RouteTable",
                    "Azure::Network::VirtualNetwork",
                    "Azure::Network::Subnet",
                    "Azure::Network::RouteTable",
                    "GCP::Compute::Network",
                    "GCP::Compute::Subnetwork",
                    "GCP::Compute::Route",
                    "OCI::Network::Vcn",
                    "OCI::Network::Subnet",
                    "OCI::Network::RouteTable",
                ],
                "load_balancing": [
                    "AWS::ElasticLoadBalancing::LoadBalancer",
                    "AWS::ElasticLoadBalancingV2::LoadBalancer",
                    "AWS::ElasticLoadBalancingV2::TargetGroup",
                    "Azure::Network::LoadBalancer",
                    "Azure::Network::ApplicationGateway",
                    "Azure::Network::TrafficManagerProfile",
                    "GCP::Compute::LoadBalancer",
                    "GCP::Compute::BackendService",
                    "GCP::Compute::UrlMap",
                    "OCI::LoadBalancer::LoadBalancer",
                    "OCI::LoadBalancer::BackendSet",
                ],
                "dns": [
                    "AWS::Route53::HostedZone",
                    "AWS::Route53::RecordSet",
                    "Azure::Network::DnsZone",
                    "GCP::DNS::ManagedZone",
                    "GCP::DNS::RecordSet",
                    "OCI::DNS::Zone",
                    "OCI::DNS::Record",
                ],
                None: [
                    "AWS::EC2::*",
                    "AWS::Network::*",
                    "Azure::Network::*",
                    "GCP::Compute::*",
                    "OCI::Network::*",
                ],
            },
            "data_protection": {
                "data_at_rest": [
                    "AWS::S3::Bucket",
                    "AWS::EBS::Volume",
                    "AWS::EFS::FileSystem",
                    "AWS::FSx::FileSystem",
                    "AWS::RDS::DBInstance",
                    "AWS::DynamoDB::Table",
                    "AWS::ElastiCache::CacheCluster",
                    "AWS::Redshift::Cluster",
                    "Azure::Storage::Account",
                    "Azure::Storage::Blob",
                    "Azure::Storage::FileShare",
                    "Azure::SQL::Database",
                    "Azure::CosmosDB::DatabaseAccount",
                    "Azure::Redis::Cache",
                    "GCP::Storage::Bucket",
                    "GCP::Storage::Object",
                    "GCP::SQL::Instance",
                    "GCP::Firestore::Database",
                    "GCP::Bigtable::Instance",
                    "GCP::Memorystore::Instance",
                    "OCI::ObjectStorage::Bucket",
                    "OCI::FileStorage::FileSystem",
                    "OCI::Database::AutonomousDatabase",
                    "OCI::Database::DBSystem",
                    "OCI::NoSQL::Table",
                ],
                "data_in_transit": [
                    "AWS::ElasticLoadBalancing::LoadBalancer",
                    "AWS::ElasticLoadBalancingV2::LoadBalancer",
                    "AWS::CloudFront::Distribution",
                    "AWS::ApiGateway::RestApi",
                    "AWS::ApiGatewayV2::Api",
                    "AWS::VPN::Connection",
                    "Azure::Network::ApplicationGateway",
                    "Azure::CDN::Profile",
                    "Azure::ApiManagement::Service",
                    "Azure::Network::VirtualNetworkGateway",
                    "GCP::Compute::LoadBalancer",
                    "GCP::CloudCDN::BackendBucket",
                    "GCP::ApiGateway::Api",
                    "GCP::Compute::VpnTunnel",
                    "OCI::LoadBalancer::LoadBalancer",
                    "OCI::ApiGateway::Api",
                    "OCI::Network::VirtualCircuit",
                ],
                "encryption": [
                    "AWS::KMS::Key",
                    "AWS::KMS::Alias",
                    "AWS::SecretsManager::Secret",
                    "AWS::CloudHSM::Hsm",
                    "Azure::KeyVault::Vault",
                    "Azure::KeyVault::Key",
                    "Azure::KeyVault::Secret",
                    "GCP::KMS::KeyRing",
                    "GCP::KMS::CryptoKey",
                    "GCP::SecretManager::Secret",
                    "OCI::KMS::Vault",
                    "OCI::KMS::Key",
                    "OCI::Vault::Secret",
                ],
                None: [
                    "AWS::S3::*",
                    "AWS::RDS::*",
                    "AWS::EBS::*",
                    "AWS::DynamoDB::*",
                    "Azure::Storage::*",
                    "Azure::SQL::*",
                    "Azure::CosmosDB::*",
                    "GCP::Storage::*",
                    "GCP::SQL::*",
                    "GCP::Firestore::*",
                    "OCI::ObjectStorage::*",
                    "OCI::Database::*",
                ],
            },
            "access_control": {
                "access_restrictions": [
                    "AWS::IAM::Role",
                    "AWS::IAM::Policy",
                    "AWS::IAM::Group",
                    "AWS::IAM::InstanceProfile",
                    "Azure::Authorization::RoleDefinition",
                    "Azure::Authorization::RoleAssignment",
                    "Azure::Management::Lock",
                    "GCP::IAM::Role",
                    "GCP::IAM::Policy",
                    "GCP::IAM::ServiceAccount",
                    "OCI::Identity::Policy",
                    "OCI::Identity::Group",
                    "OCI::Identity::Compartment",
                ],
                "identification": [
                    "AWS::IAM::User",
                    "AWS::Cognito::UserPool",
                    "AWS::Cognito::UserPoolClient",
                    "AWS::SSO::PermissionSet",
                    "Azure::AD::User",
                    "Azure::AD::Application",
                    "Azure::AD::ServicePrincipal",
                    "GCP::IAM::ServiceAccount",
                    "GCP::Identity::User",
                    "GCP::Identity::Group",
                    "OCI::Identity::User",
                    "OCI::Identity::ApiKey",
                ],
                "multi_factor": [
                    "AWS::IAM::VirtualMfaDevice",
                    "AWS::IAM::User",
                    "Azure::AD::ConditionalAccessPolicy",
                    "Azure::AD::User",
                    "GCP::IAM::ServiceAccountKey",
                    "GCP::Identity::User",
                    "OCI::Identity::MfaTotpDevice",
                    "OCI::Identity::User",
                ],
                None: [
                    "AWS::IAM::*",
                    "AWS::Cognito::*",
                    "Azure::Authorization::*",
                    "Azure::AD::*",
                    "GCP::IAM::*",
                    "GCP::Identity::*",
                    "OCI::Identity::*",
                ],
            },
            "monitoring_testing": {
                "logging": [
                    "AWS::CloudWatch::LogGroup",
                    "AWS::CloudTrail::Trail",
                    "AWS::Config::ConfigurationRecorder",
                    "AWS::CloudWatch::LogStream",
                    "Azure::Monitor::LogProfile",
                    "Azure::Monitor::DiagnosticSetting",
                    "Azure::OperationalInsights::Workspace",
                    "GCP::Logging::LogSink",
                    "GCP::Logging::LogBucket",
                    "GCP::Logging::LogView",
                    "OCI::Logging::LogGroup",
                    "OCI::Logging::Log",
                ],
                "monitoring": [
                    "AWS::CloudWatch::Alarm",
                    "AWS::CloudWatch::Dashboard",
                    "AWS::CloudWatch::Metric",
                    "Azure::Monitor::MetricAlert",
                    "Azure::Monitor::ActionGroup",
                    "Azure::Monitor::ActivityLogAlert",
                    "GCP::Monitoring::AlertPolicy",
                    "GCP::Monitoring::NotificationChannel",
                    "GCP::Monitoring::UptimeCheckConfig",
                    "OCI::Monitoring::Alarm",
                    "OCI::Monitoring::Metric",
                ],
                "security_testing": [
                    "AWS::Inspector::AssessmentTemplate",
                    "AWS::SecurityHub::Hub",
                    "AWS::GuardDuty::Detector",
                    "Azure::Security::Assessment",
                    "Azure::SecurityCenter::SecurityContact",
                    "Azure::SecurityCenter::AutoProvisioningSetting",
                    "GCP::SecurityCommandCenter::Finding",
                    "GCP::SecurityCommandCenter::Source",
                    "GCP::SecurityCommandCenter::NotificationConfig",
                    "OCI::VulnerabilityScanning::HostScanTarget",
                    "OCI::CloudGuard::DetectorRecipe",
                ],
                None: [
                    "AWS::CloudWatch::*",
                    "AWS::CloudTrail::*",
                    "AWS::Config::*",
                    "Azure::Monitor::*",
                    "GCP::Logging::*",
                    "GCP::Monitoring::*",
                    "OCI::Logging::*",
                    "OCI::Monitoring::*",
                ],
            },
            "vulnerability_management": {
                "antivirus": [
                    "AWS::EC2::Instance",
                    "AWS::ECS::TaskDefinition",
                    "AWS::EKS::Pod",
                    "Azure::Compute::VirtualMachine",
                    "Azure::Container::ContainerGroup",
                    "Azure::ContainerService::ManagedCluster",
                    "GCP::Compute::Instance",
                    "GCP::Run::Service",
                    "GCP::GKE::Pod",
                    "OCI::Compute::Instance",
                    "OCI::ContainerEngine::NodePool",
                ],
                "patch_management": [
                    "AWS::SSM::PatchBaseline",
                    "AWS::SystemsManager::PatchGroup",
                    "AWS::EC2::Instance",
                    "Azure::Compute::VirtualMachineExtension",
                    "Azure::Compute::VirtualMachine",
                    "GCP::Compute::Instance",
                    "GCP::OSConfig::PatchDeployment",
                    "OCI::OSManagement::ManagedInstance",
                    "OCI::Compute::Instance",
                ],
                "secure_systems": [
                    "AWS::EC2::Instance",
                    "AWS::ECS::Cluster",
                    "AWS::EKS::Cluster",
                    "AWS::Lambda::Function",
                    "Azure::Compute::VirtualMachine",
                    "Azure::ContainerService::ManagedCluster",
                    "Azure::Functions::FunctionApp",
                    "GCP::Compute::Instance",
                    "GCP::GKE::Cluster",
                    "GCP::CloudFunctions::Function",
                    "OCI::Compute::Instance",
                    "OCI::ContainerEngine::Cluster",
                    "OCI::Functions::Function",
                ],
                None: [
                    "AWS::EC2::*",
                    "AWS::ECS::*",
                    "AWS::EKS::*",
                    "Azure::Compute::*",
                    "Azure::ContainerService::*",
                    "GCP::Compute::*",
                    "GCP::GKE::*",
                    "OCI::Compute::*",
                    "OCI::ContainerEngine::*",
                ],
            },
            "policy_procedures": {
                "security_policies": [
                    "AWS::IAM::Policy",
                    "AWS::Config::ConfigRule",
                    "AWS::Organizations::Policy",
                    "Azure::Policy::PolicyDefinition",
                    "Azure::Policy::PolicyAssignment",
                    "Azure::Management::Lock",
                    "GCP::IAM::Policy",
                    "GCP::ResourceManager::OrganizationPolicy",
                    "GCP::ResourceManager::Folder",
                    "OCI::Identity::Policy",
                    "OCI::Identity::Compartment",
                ],
                "compliance": [
                    "AWS::Config::ConfigurationRecorder",
                    "AWS::SecurityHub::Hub",
                    "AWS::AuditManager::Assessment",
                    "Azure::Policy::PolicyDefinition",
                    "Azure::SecurityCenter::SecurityContact",
                    "GCP::SecurityCommandCenter::Source",
                    "GCP::SecurityCommandCenter::NotificationConfig",
                    "OCI::CloudGuard::DetectorRecipe",
                    "OCI::CloudGuard::ResponderRecipe",
                ],
                None: [
                    "AWS::IAM::*",
                    "AWS::Config::*",
                    "AWS::Organizations::*",
                    "Azure::Policy::*",
                    "GCP::IAM::*",
                    "GCP::ResourceManager::*",
                    "OCI::Identity::*",
                ],
            },
            "application_security": {
                "api_security": [
                    "AWS::ApiGateway::RestApi",
                    "AWS::ApiGatewayV2::Api",
                    "AWS::ApiGateway::Authorizer",
                    "Azure::ApiManagement::Service",
                    "Azure::ApiManagement::Api",
                    "GCP::ApiGateway::Api",
                    "GCP::ApiGateway::Gateway",
                    "OCI::ApiGateway::Api",
                    "OCI::ApiGateway::Deployment",
                ],
                "container_security": [
                    "AWS::ECS::TaskDefinition",
                    "AWS::EKS::Pod",
                    "AWS::ECR::Repository",
                    "Azure::Container::ContainerGroup",
                    "Azure::ContainerRegistry::Registry",
                    "GCP::Run::Service",
                    "GCP::GKE::Pod",
                    "GCP::ArtifactRegistry::Repository",
                    "OCI::ContainerEngine::NodePool",
                    "OCI::Artifacts::ContainerRepository",
                ],
                "serverless": [
                    "AWS::Lambda::Function",
                    "AWS::Lambda::LayerVersion",
                    "Azure::Functions::FunctionApp",
                    "GCP::CloudFunctions::Function",
                    "GCP::CloudRun::Service",
                    "OCI::Functions::Function",
                ],
                None: [
                    "AWS::ApiGateway::*",
                    "AWS::ECS::*",
                    "AWS::Lambda::*",
                    "Azure::ApiManagement::*",
                    "Azure::Container::*",
                    "Azure::Functions::*",
                    "GCP::ApiGateway::*",
                    "GCP::Run::*",
                    "GCP::CloudFunctions::*",
                    "OCI::ApiGateway::*",
                    "OCI::ContainerEngine::*",
                    "OCI::Functions::*",
                ],
            },
            "backup_recovery": {
                "backup": [
                    "AWS::Backup::BackupPlan",
                    "AWS::Backup::BackupVault",
                    "AWS::RDS::DBInstance",
                    "AWS::S3::Bucket",
                    "Azure::Backup::BackupVault",
                    "Azure::Backup::BackupPolicy",
                    "Azure::SQL::Database",
                    "Azure::Storage::Account",
                    "GCP::Compute::Snapshot",
                    "GCP::SQL::Backup",
                    "GCP::Storage::Bucket",
                    "OCI::Database::Backup",
                    "OCI::ObjectStorage::Bucket",
                ],
                "disaster_recovery": [
                    "AWS::DynamoDB::GlobalTable",
                    "AWS::RDS::DBInstance",
                    "AWS::Route53::HealthCheck",
                    "Azure::SiteRecovery::ReplicationPolicy",
                    "Azure::SQL::Database",
                    "GCP::Compute::Instance",
                    "GCP::SQL::Instance",
                    "OCI::Database::AutonomousDatabase",
                    "OCI::Compute::Instance",
                ],
                None: [
                    "AWS::Backup::*",
                    "AWS::RDS::*",
                    "AWS::S3::*",
                    "Azure::Backup::*",
                    "Azure::SQL::*",
                    "Azure::Storage::*",
                    "GCP::Compute::*",
                    "GCP::SQL::*",
                    "GCP::Storage::*",
                    "OCI::Database::*",
                    "OCI::ObjectStorage::*",
                ],
            },
        }

    def infer_resources(
        self, category: str | None, subcategory: str | None = None
    ) -> list[str]:
        """Infer cloud resources from category and subcategory.

        Args:
            category: Control category (e.g., "network_security")
            subcategory: Control subcategory (e.g., "firewall") or None

        Returns:
            List of cloud resource identifiers
        """
        if not category:
            return []

        category_lower = category.lower().replace("-", "_").replace(" ", "_")
        subcategory_lower = (
            subcategory.lower().replace("-", "_").replace(" ", "_")
            if subcategory
            else None
        )

        if category_lower not in self.mapping:
            return []

        category_map = self.mapping[category_lower]

        if subcategory_lower and subcategory_lower in category_map:
            return category_map[subcategory_lower].copy()

        if None in category_map:
            return category_map[None].copy()

        return []

    def get_all_for_category(self, category: str) -> list[str]:
        """Get all resources for a category across all subcategories.

        Args:
            category: Control category

        Returns:
            List of all resource identifiers for the category
        """
        category_lower = category.lower().replace("-", "_").replace(" ", "_")

        if category_lower not in self.mapping:
            return []

        all_resources = set()
        for subcategory_resources in self.mapping[category_lower].values():
            all_resources.update(subcategory_resources)

        return sorted(list(all_resources))

    def expand_wildcards(self, resources: list[str]) -> list[str]:
        """Expand wildcard resources (e.g., AWS::*).

        Currently returns as-is. Future enhancement: expand to all resources.

        Args:
            resources: List of resource identifiers (may include wildcards)

        Returns:
            List with wildcards expanded (currently returns as-is)
        """
        return resources

    def is_generic(self, resource: str) -> bool:
        """Check if a resource identifier is generic (wildcard).

        Args:
            resource: Resource identifier

        Returns:
            True if resource is generic (ends with ::*)
        """
        return resource.endswith("::*") or resource == "*"

