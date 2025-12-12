# WISTX Complex Test Prompts

This document contains very complex, realistic prompts designed to thoroughly test WISTX product features across all major domains. Each prompt is designed to exercise multiple capabilities simultaneously and represent real-world DevOps engineering scenarios.

**Note**: All prompts are designed to work with the actual WISTX MCP tools. Tool names use the `wistx_` prefix as registered in the MCP server.

## Available WISTX MCP Tools

The following tools are available for testing (22 total):

### Compliance & Security
- `wistx_get_compliance_requirements` - Get compliance controls for infrastructure resources

### Pricing & Cost
- `wistx_calculate_infrastructure_cost` - Calculate infrastructure costs with optimization suggestions

### Code & Knowledge
- `wistx_get_devops_infra_code_examples` - Get production-ready code examples
- `wistx_research_knowledge_base` - Research DevOps best practices, patterns, and strategies
- `wistx_search_devops_resources` - Search DevOps packages, tools, services, and documentation
- `wistx_read_package_file` - Read specific files from packages using SHA256 hashes

### Indexing & Search
- `wistx_index_repository` - Index GitHub repositories for user-specific search
- `wistx_index_resource` - Index documentation websites or document files
- `wistx_search_codebase` - Semantic search across indexed repositories
- `wistx_regex_search` - Pattern-based code search with pre-built templates
- `wistx_manage_resources` - List, check status, and delete indexed resources

### Architecture & Design
- `wistx_design_architecture` - Design and initialize infrastructure architectures
- `wistx_troubleshoot_issue` - Diagnose infrastructure issues with root cause analysis
- `wistx_generate_documentation` - Generate infrastructure documentation and reports

### Infrastructure Management
- `wistx_manage_infrastructure_lifecycle` - Manage infrastructure lifecycle and integration patterns
- `wistx_get_existing_infrastructure` - Analyze existing infrastructure for compliance, costs, and security
- `wistx_discover_cloud_resources` - Discover existing cloud resources and generate Terraform import context

### Virtual Filesystem
- `wistx_list_filesystem` - Navigate indexed repositories with infrastructure-aware views
- `wistx_read_file_with_context` - Read files with compliance, cost, and security context

### Intelligent Context
- `wistx_save_context_with_analysis` - Persist conversations and designs with automatic analysis
- `wistx_search_contexts_intelligently` - Search saved contexts with infrastructure awareness

### Web & Search
- `wistx_web_search` - Real-time DevOps information, CVEs, and security advisories

---

## 1. Infrastructure Engineering

### Prompt 1.1: Multi-Cloud Microservices Architecture with Compliance & Cost Optimization

**Complexity Level**: Very High  
**Estimated Tool Calls**: 8-12  
**Domain**: Infrastructure Engineering, Compliance, FinOps, Platform Engineering

**Prompt**:
```
I need to design and implement a production-grade, multi-cloud microservices architecture for a financial services application that must handle 10 million daily transactions with 99.99% uptime. The system must be:

1. **Multi-Cloud**: Primary workload on AWS (us-east-1, us-west-2), disaster recovery on GCP (us-central1), and Azure (eastus) for regulatory compliance in different regions
2. **Compliance**: Must meet PCI-DSS Level 1, HIPAA, SOC2 Type II, and NIST-800-53 requirements simultaneously
3. **Architecture**: Event-driven microservices with 15 services (user-service, payment-service, transaction-service, notification-service, analytics-service, etc.)
4. **Infrastructure Components**:
   - Kubernetes clusters (EKS on AWS, GKE on GCP, AKS on Azure) with auto-scaling
   - Managed databases: RDS PostgreSQL Multi-AZ (primary), Cloud SQL (DR), Azure Database for PostgreSQL (regulatory)
   - Message queues: AWS SQS, GCP Pub/Sub, Azure Service Bus
   - Object storage: S3, GCS, Azure Blob Storage
   - API Gateway with rate limiting and authentication
   - CDN for global content delivery
   - Monitoring and logging infrastructure (CloudWatch, Stackdriver, Azure Monitor)
   - CI/CD pipelines with GitLab CI
5. **Cost Constraints**: Total monthly budget of $50,000 with optimization targets of 30% savings
6. **Security**: End-to-end encryption, VPC isolation, network segmentation, WAF protection
7. **Integration Requirements**: 
   - Connect payment service to RDS with secure networking
   - Integrate analytics service with S3 for data lake
   - Connect notification service to message queues across all clouds
   - Set up monitoring integration across all three cloud providers

Please provide:
- Complete architecture design with visual diagrams
- Terraform code for all three cloud providers
- Compliance analysis for each resource type across all standards
- Detailed cost breakdown for AWS, GCP, and Azure with optimization recommendations
- Integration patterns with security rules and monitoring configurations
- Implementation roadmap with dependency resolution
- Risk assessment and mitigation strategies
- Disaster recovery and backup strategies
```

**Expected Features Tested**:
- `wistx_design_architecture` (multi-cloud, compliance, cost) - action="design" with multi-cloud provider
- `wistx_get_compliance_requirements` (multiple standards, multiple resources) - resource_types=["RDS", "S3", "EC2", "EKS", "Lambda", "CloudFront", "KMS"], standards=["PCI-DSS", "HIPAA", "SOC2", "NIST-800-53"]
- `wistx_calculate_infrastructure_cost` (multi-cloud comparison, optimization) - resources array with AWS, GCP, Azure resources
- `wistx_manage_infrastructure_lifecycle` (integration patterns, multi-cloud) - action="integrate" with components across clouds
- `wistx_get_devops_infra_code_examples` (Terraform, Kubernetes, multi-cloud) - query with code_types=["terraform", "kubernetes"], cloud_provider="multi-cloud"
- `wistx_research_knowledge_base` (best practices, patterns) - query with domains=["infrastructure", "compliance", "finops"]
- `wistx_generate_documentation` (architecture docs, runbooks) - document_type="architecture_diagram" and "runbook"

---

### Prompt 1.2: Kubernetes Platform Modernization with Zero-Downtime Migration

**Complexity Level**: Very High  
**Estimated Tool Calls**: 10-15  
**Domain**: Infrastructure Engineering, Platform Engineering, Cloud Engineering

**Prompt**:
```
I'm leading a platform engineering initiative to modernize our Kubernetes infrastructure from version 1.23 to 1.29 with zero-downtime migration. Current setup:

**Current State**:
- 3 EKS clusters (dev, staging, prod) running Kubernetes 1.23
- 200+ microservices deployed across namespaces
- Istio service mesh for traffic management
- Prometheus + Grafana for monitoring
- ArgoCD for GitOps deployments
- External databases (RDS, ElastiCache, S3)
- Custom operators for stateful workloads
- Multi-region setup (us-east-1, eu-west-1, ap-southeast-1)

**Requirements**:
1. **Upgrade Strategy**: Design zero-downtime upgrade path from 1.23 → 1.29 with rollback capabilities
2. **Infrastructure Changes**: 
   - Migrate to new node groups with ARM-based instances (Graviton3) for cost optimization
   - Implement Karpenter for dynamic node provisioning
   - Upgrade Istio from 1.13 to 1.20
   - Migrate from Prometheus to Prometheus Operator with Thanos for long-term storage
3. **Integration Patterns**: 
   - Connect upgraded clusters to existing RDS databases securely
   - Integrate new monitoring stack with existing alerting (PagerDuty, Slack)
   - Set up cross-cluster service discovery
   - Configure multi-cluster networking with proper security policies
4. **Compliance**: Ensure all changes meet SOC2 and CIS Kubernetes Benchmark requirements
5. **Cost Analysis**: Calculate cost impact of migration and identify 25% cost reduction opportunities
6. **Platform Capabilities**: 
   - Self-service namespace provisioning
   - Resource quota management
   - Network policy automation
   - Backup and disaster recovery automation

Please provide:
- Detailed upgrade plan with step-by-step procedures
- Infrastructure code (Terraform, Helm charts) for new cluster setup
- Integration patterns for connecting upgraded infrastructure to existing systems
- Compliance verification checklist for each component
- Cost analysis comparing current vs. new infrastructure
- Risk mitigation strategies and rollback procedures
- Platform engineering best practices for Kubernetes operations
- Monitoring and observability setup for the new platform
```

**Expected Features Tested**:
- `wistx_manage_infrastructure_lifecycle` (upgrade, optimize, monitor) - action="upgrade" with current_version/target_version, action="optimize", action="monitor"
- `wistx_design_architecture` (platform engineering, Kubernetes) - action="design", project_type="platform", architecture_type="microservices"
- `wistx_get_compliance_requirements` (Kubernetes, SOC2, CIS) - resource_types=["EKS", "Kubernetes"], standards=["SOC2", "CIS"]
- `wistx_calculate_infrastructure_cost` (cost optimization, instance comparison) - resources with different instance types for comparison
- `wistx_manage_infrastructure_lifecycle` (integration patterns, networking, security) - action="integrate", integration_type=["networking", "security", "monitoring"]
- `wistx_get_devops_infra_code_examples` (Kubernetes, Helm, Terraform, Karpenter) - query with code_types=["kubernetes", "helm", "terraform"]
- `wistx_research_knowledge_base` (Kubernetes upgrade best practices) - query with domains=["platform", "infrastructure"]
- `wistx_troubleshoot_issue` (migration issues, compatibility) - infrastructure_type="kubernetes", error_messages provided
- `wistx_generate_documentation` (runbooks, migration guides) - document_type="runbook", "deployment_guide"

---

## 2. Compliance

### Prompt 2.1: Multi-Standard Compliance Audit with Remediation Plan

**Complexity Level**: Very High  
**Estimated Tool Calls**: 12-18  
**Domain**: Compliance, Infrastructure Engineering, Security

**Prompt**:
```
I'm conducting a comprehensive compliance audit for a healthcare fintech company that processes both medical records (HIPAA) and payment card data (PCI-DSS). The infrastructure spans AWS, GCP, and Azure with the following components:

**Infrastructure Inventory**:
- **AWS**: 
  - 5 RDS PostgreSQL Multi-AZ instances (patient data, payment processing)
  - 20 S3 buckets (medical images, transaction logs, backups)
  - 50 EC2 instances across 3 VPCs (application servers, API gateways)
  - 3 EKS clusters (microservices, data processing)
  - Lambda functions (event processing, data transformation)
  - CloudFront CDN (patient portal, API endpoints)
  - KMS keys for encryption
- **GCP**:
  - Cloud SQL instances (analytics database)
  - GCS buckets (data lake, ML model storage)
  - GKE clusters (ML inference workloads)
  - Cloud Functions (data pipeline triggers)
- **Azure**:
  - Azure Database for PostgreSQL (regulatory compliance region)
  - Blob Storage (archival, compliance reporting)
  - AKS clusters (disaster recovery workloads)

**Compliance Requirements**:
1. **HIPAA**: All resources handling Protected Health Information (PHI)
2. **PCI-DSS Level 1**: All resources in payment card data environment
3. **SOC2 Type II**: All infrastructure components
4. **NIST-800-53**: Security controls for federal contracts
5. **GDPR**: Data processing and storage in EU regions
6. **ISO-27001**: Information security management

**Audit Objectives**:
1. Identify all compliance gaps across all standards for each resource type
2. Prioritize remediation by severity (CRITICAL, HIGH, MEDIUM, LOW)
3. Generate remediation code (Terraform, CloudFormation, Azure ARM) for each gap
4. Create verification procedures for each remediation
5. Estimate compliance risk score for current state
6. Provide compliance report suitable for external auditors
7. Design compliance monitoring and continuous compliance strategy

**Specific Focus Areas**:
- Encryption at rest and in transit for all data stores
- Access controls and IAM policies
- Network segmentation and firewall rules
- Logging and audit trails
- Backup and disaster recovery compliance
- Data retention and deletion policies
- Incident response procedures
- Vendor management compliance

Please provide:
- Complete compliance gap analysis for all resources across all standards
- Prioritized remediation plan with code examples
- Compliance scorecard showing current vs. target state
- Automated compliance verification scripts
- Compliance report in format suitable for external audit
- Continuous compliance monitoring strategy
- Cost impact analysis of compliance remediation
```

**Expected Features Tested**:
- `wistx_get_compliance_requirements` (multiple standards, multiple resources, severity filtering) - resource_types=["RDS", "S3", "EC2", "EKS", "Lambda", "CloudFront", "KMS", "CloudSQL", "GCS", "GKE", "Azure Database", "Blob Storage", "AKS"], standards=["HIPAA", "PCI-DSS", "SOC2", "NIST-800-53", "GDPR", "ISO-27001"], severity="CRITICAL" and "HIGH"
- `wistx_get_devops_infra_code_examples` (compliance remediation code) - query with compliance_standard filter, code_types=["terraform", "cloudformation", "arm"]
- `wistx_research_knowledge_base` (compliance best practices, audit procedures) - query with domains=["compliance"], content_types=["guide", "best_practice"]
- `wistx_generate_documentation` (compliance reports, audit documentation) - document_type="compliance_report" with resource_types and compliance_standards
- `wistx_calculate_infrastructure_cost` (compliance remediation costs) - calculate costs for compliant vs non-compliant configurations
- `wistx_design_architecture` (compliant architecture patterns) - action="design" with compliance_standards parameter
- `wistx_manage_infrastructure_lifecycle` (compliance validation) - action="validate" with compliance_standards

---

### Prompt 2.2: FedRAMP Compliance for Government Cloud Infrastructure

**Complexity Level**: Very High  
**Estimated Tool Calls**: 10-14  
**Domain**: Compliance, Infrastructure Engineering, Cloud Engineering

**Prompt**:
```
I need to design and implement a FedRAMP Moderate compliant infrastructure for a government contractor building a citizen services platform. The system must meet strict federal security requirements while maintaining operational efficiency.

**Infrastructure Requirements**:
- **Primary Cloud**: AWS GovCloud (us-gov-west-1, us-gov-east-1)
- **Components**:
  - Application tier: Auto-scaling EC2 instances behind ALB
  - Database tier: RDS PostgreSQL with Multi-AZ and encryption
  - Storage: S3 buckets with versioning and lifecycle policies
  - Networking: VPC with public/private/subnet segmentation, VPN endpoints
  - Security: WAF, Security Groups, Network ACLs, GuardDuty, Inspector
  - Monitoring: CloudWatch, CloudTrail, Config
  - Identity: IAM with MFA, SSO integration
  - Backup: Automated backups with cross-region replication
  - Disaster Recovery: Multi-region failover capability

**FedRAMP Requirements**:
1. **Access Control (AC)**: Implement least privilege, MFA, session management
2. **Audit and Accountability (AU)**: Comprehensive logging, log retention, audit trails
3. **Security Assessment (CA)**: Continuous monitoring, vulnerability scanning
4. **Configuration Management (CM)**: Infrastructure as Code, change management
5. **Identification and Authentication (IA)**: Strong authentication, identity proofing
6. **Incident Response (IR)**: Incident response plan, automated response
7. **Media Protection (MP)**: Encryption, media sanitization
8. **System and Communications Protection (SC)**: Network segmentation, encryption
9. **System and Information Integrity (SI)**: Malware protection, system monitoring

**Additional Compliance**:
- NIST-800-53 controls (baseline for FedRAMP)
- FISMA requirements
- CISA guidelines
- Agency-specific requirements

**Deliverables Needed**:
1. Complete FedRAMP control mapping for all infrastructure components
2. Terraform code implementing all required controls
3. Compliance verification procedures and automated tests
4. Security documentation (SSP, SAR, POA&M templates)
5. Continuous compliance monitoring setup
6. Cost analysis for FedRAMP-compliant infrastructure
7. Implementation roadmap with milestones
8. Risk assessment and mitigation strategies

Please provide comprehensive FedRAMP compliance guidance with production-ready code examples and verification procedures.
```

**Expected Features Tested**:
- `wistx_get_compliance_requirements` (FedRAMP, NIST-800-53, FISMA) - resource_types=["EC2", "RDS", "S3", "VPC", "ALB", "WAF", "CloudWatch", "CloudTrail", "IAM"], standards=["FedRAMP", "NIST-800-53"], include_remediation=True, include_verification=True
- `wistx_design_architecture` (FedRAMP-compliant design) - action="design", cloud_provider="aws", compliance_standards=["FedRAMP", "NIST-800-53"]
- `wistx_get_devops_infra_code_examples` (FedRAMP Terraform examples) - query with compliance_standard="NIST-800-53", code_types=["terraform"], cloud_provider="aws"
- `wistx_research_knowledge_base` (FedRAMP best practices, government cloud) - query with domains=["compliance", "security"], include_web_search=True
- `wistx_calculate_infrastructure_cost` (GovCloud pricing) - resources with region="us-gov-west-1" or "us-gov-east-1"
- `wistx_generate_documentation` (SSP, SAR, POA&M templates) - document_type="compliance_report" with compliance_standards=["FedRAMP"]
- `wistx_manage_infrastructure_lifecycle` (compliance validation, monitoring) - action="validate" and action="monitor" with compliance_standards

---

## 3. FinOps

### Prompt 3.1: Multi-Cloud Cost Optimization with 40% Reduction Target

**Complexity Level**: Very High  
**Estimated Tool Calls**: 15-20  
**Domain**: FinOps, Infrastructure Engineering, Cloud Engineering

**Prompt**:
```
I'm the FinOps lead for a company with $2.5M annual cloud spend across AWS, GCP, and Azure. Management has mandated a 40% cost reduction target over the next 6 months without impacting performance or availability. Current infrastructure:

**Current Infrastructure**:
- **AWS (60% of spend, $1.5M/year)**:
  - 200 EC2 instances (mix of t3, m5, c5, r5 families)
  - 15 RDS instances (db.t3.medium to db.r5.4xlarge)
  - 50 S3 buckets (500TB total, various storage classes)
  - 3 EKS clusters (150 nodes total)
  - CloudFront CDN (10TB/month transfer)
  - Data Transfer costs ($50K/year)
  - Reserved Instances: 30% coverage
- **GCP (25% of spend, $625K/year)**:
  - 80 Compute Engine VMs (n1, n2, c2 families)
  - 8 Cloud SQL instances
  - 20 GCS buckets (200TB)
  - 2 GKE clusters (80 nodes)
  - Cloud Load Balancing
- **Azure (15% of spend, $375K/year)**:
  - 60 Virtual Machines (D-series, F-series)
  - 5 Azure Database for PostgreSQL
  - 15 Blob Storage accounts (150TB)
  - 2 AKS clusters (60 nodes)

**Optimization Requirements**:
1. **Compute Optimization**:
   - Right-size all instances based on actual usage
   - Migrate to ARM-based instances (Graviton, Ampere) where possible
   - Implement Spot/Preemptible instances for non-critical workloads (target: 30% of compute)
   - Increase Reserved Instance/Savings Plan coverage to 70%
   - Implement auto-scaling to eliminate idle resources
2. **Storage Optimization**:
   - Move cold data to archival storage (S3 Glacier, GCS Coldline, Azure Archive)
   - Implement lifecycle policies automatically
   - Deduplicate and compress data
   - Optimize database storage (provisioned IOPS vs. GP3)
3. **Network Optimization**:
   - Reduce data transfer costs (VPC endpoints, CloudFront caching)
   - Optimize CDN usage
   - Implement Direct Connect/Interconnect where cost-effective
4. **Database Optimization**:
   - Right-size database instances
   - Implement read replicas for read-heavy workloads
   - Use serverless databases where appropriate (Aurora Serverless, Cloud SQL Serverless)
   - Optimize backup retention policies
5. **Container Optimization**:
   - Implement Karpenter/Kubernetes autoscaler
   - Use Spot node groups (50% of nodes)
   - Optimize pod resource requests/limits
   - Implement cluster autoscaling
6. **Multi-Cloud Strategy**:
   - Identify workloads that can be moved to cheaper cloud providers
   - Compare costs across providers for each workload type
   - Implement cloud-agnostic architecture where beneficial

**Deliverables**:
1. Detailed cost analysis for current infrastructure (by service, region, environment)
2. Cost optimization recommendations with priority ranking
3. Cost savings projections for each optimization (monthly and annual)
4. Implementation roadmap with estimated effort and ROI
5. Multi-cloud cost comparison for key workloads
6. Budget tracking setup with alerts
7. Cost allocation and chargeback model
8. FinOps best practices and governance framework
9. Automated cost optimization scripts and policies
10. Cost forecasting for next 12 months

Please provide comprehensive FinOps analysis with actionable optimization strategies.
```

**Expected Features Tested**:
- `wistx_calculate_infrastructure_cost` (multi-cloud, detailed breakdown, optimization) - resources array with AWS, GCP, Azure resources across all services, includes optimization suggestions in response
- `wistx_get_existing_infrastructure` (cost analysis, optimization opportunities) - repository_url required, include_costs=True
- `wistx_research_knowledge_base` (FinOps best practices, cost optimization patterns) - query with domains=["finops"], content_types=["best_practice", "strategy"]
- `wistx_get_devops_infra_code_examples` (cost optimization implementations) - query with code_types=["terraform", "kubernetes"]
- `wistx_design_architecture` (cost-optimized architecture) - action="optimize" with existing_architecture, requirements include cost constraints
- `wistx_manage_infrastructure_lifecycle` (optimize action, cost analysis) - action="optimize" with infrastructure_type
- `wistx_generate_documentation` (cost reports, FinOps documentation) - document_type="cost_report" with resources array

---

### Prompt 3.2: FinOps Budget Management and Forecasting for Enterprise

**Complexity Level**: Very High  
**Estimated Tool Calls**: 10-15  
**Domain**: FinOps, Infrastructure Engineering

**Prompt**:
```
I need to establish a comprehensive FinOps program for a 500-person engineering organization with $10M annual cloud spend. The company has 20 product teams, each with dev/staging/prod environments across AWS, GCP, and Azure.

**Current Challenges**:
- No centralized budget tracking
- Teams overspending by 30-50% monthly
- No cost visibility by team/product/environment
- Unpredictable monthly bills
- No cost optimization culture
- Shadow IT spending

**Requirements**:
1. **Budget Management**:
   - Set budgets for each team ($50K-$500K/month based on product)
   - Environment budgets (dev: 20%, staging: 30%, prod: 50%)
   - Service-level budgets (compute, storage, networking, databases)
   - Cloud provider budgets (AWS: 60%, GCP: 25%, Azure: 15%)
   - Quarterly and annual budgets with variance tracking
2. **Cost Allocation**:
   - Tag-based cost allocation (team, product, environment, cost center)
   - Chargeback/showback model
   - Cost center reporting
   - Project-level cost tracking
3. **Forecasting**:
   - 12-month cost forecast based on historical trends
   - Growth-based forecasting (accounting for new products, scaling)
   - Scenario planning (what-if analysis)
   - Budget vs. actual tracking with variance analysis
4. **Alerting**:
   - Budget threshold alerts (50%, 75%, 90%, 100%, 110%)
   - Anomaly detection (unusual spending patterns)
   - Cost spike alerts (day-over-day, week-over-week)
   - Team-specific alerts
5. **Optimization Tracking**:
   - Track cost savings from optimization initiatives
   - ROI calculation for optimization projects
   - Savings attribution to teams/initiatives
6. **Reporting**:
   - Executive dashboards (C-level, VP-level)
   - Team-level detailed reports
   - Cost trend analysis
   - Optimization opportunity reports

**Infrastructure to Analyze**:
- 200+ AWS accounts (multi-account setup)
- 50+ GCP projects
- 30+ Azure subscriptions
- 1000+ compute instances
- 200+ databases
- 500+ storage buckets
- 50+ Kubernetes clusters

Please provide:
- Complete budget management strategy and implementation
- Cost allocation and tagging strategy
- Forecasting models and methodology
- Alert configuration and thresholds
- Dashboard and reporting templates
- FinOps governance framework
- Cost optimization roadmap
- Team enablement and training plan
```

**Expected Features Tested**:
- `wistx_calculate_infrastructure_cost` (budget checking, multi-environment) - resources with environment_name parameter, check_budgets=True
- `wistx_get_existing_infrastructure` (cost analysis, spending patterns) - repository_url required, include_costs=True
- `wistx_research_knowledge_base` (FinOps best practices, budget management) - query with domains=["finops"], content_types=["guide", "strategy"]
- `wistx_generate_documentation` (FinOps reports, budget documentation) - document_type="cost_report"
- `wistx_manage_infrastructure_lifecycle` (cost optimization, monitoring) - action="optimize" and action="monitor"
- `wistx_design_architecture` (cost-optimized, budget-aware architecture) - action="design" with requirements including budget constraints

---

## 4. Platform Engineering

### Prompt 4.1: Self-Service Platform with Multi-Cloud Support

**Complexity Level**: Very High  
**Estimated Tool Calls**: 12-18  
**Domain**: Platform Engineering, Infrastructure Engineering, Cloud Engineering

**Prompt**:
```
I'm building a self-service internal developer platform (IDP) that enables 200+ developers to provision and manage infrastructure across AWS, GCP, and Azure without direct cloud access. The platform must provide:

**Platform Capabilities**:
1. **Self-Service Provisioning**:
   - Kubernetes namespaces with resource quotas
   - Managed databases (RDS, Cloud SQL, Azure Database)
   - Object storage buckets (S3, GCS, Azure Blob)
   - Message queues (SQS, Pub/Sub, Service Bus)
   - Load balancers and API gateways
   - Monitoring and logging setup
2. **Multi-Cloud Abstraction**:
   - Unified API for all three cloud providers
   - Cloud-agnostic resource definitions
   - Automatic cloud selection based on cost/performance
   - Cross-cloud networking and service discovery
3. **GitOps Integration**:
   - ArgoCD for application deployments
   - Terraform Cloud for infrastructure provisioning
   - Automated PR-based infrastructure changes
   - Infrastructure drift detection and remediation
4. **Developer Experience**:
   - Web UI for resource provisioning
   - CLI tool for developers
   - API for programmatic access
   - Slack/Teams integration for notifications
5. **Platform Services**:
   - Service mesh (Istio) for traffic management
   - API gateway with rate limiting and authentication
   - Observability stack (Prometheus, Grafana, Loki, Tempo)
   - CI/CD pipelines (GitLab CI, GitHub Actions)
   - Secret management (Vault, AWS Secrets Manager)
   - Image registry (ECR, GCR, ACR)
6. **Compliance and Security**:
   - Automatic compliance checks (SOC2, PCI-DSS)
   - Security scanning (vulnerability, secrets, misconfigurations)
   - Network policy enforcement
   - RBAC and IAM integration
   - Audit logging for all platform operations
7. **Cost Management**:
   - Cost allocation by team/project
   - Budget alerts and limits
   - Cost optimization recommendations
   - Showback/chargeback reporting

**Infrastructure Requirements**:
- **Control Plane**: Kubernetes cluster (EKS) for platform services
- **Data Plane**: Multiple Kubernetes clusters across clouds (EKS, GKE, AKS)
- **Storage**: Multi-cloud object storage for platform data
- **Networking**: VPN/Interconnect between clouds
- **Identity**: SSO integration (Okta, Azure AD)
- **Monitoring**: Centralized observability across all clouds

**Integration Requirements**:
- Connect platform services to cloud provider APIs
- Integrate with existing CI/CD systems
- Connect to corporate identity providers
- Integrate with ticketing systems (Jira) for approvals
- Connect to cost management tools

Please provide:
- Complete platform architecture design
- Infrastructure as Code (Terraform, Helm charts)
- API design for self-service provisioning
- Integration patterns for multi-cloud connectivity
- Compliance and security implementation
- Cost management and allocation strategy
- Developer onboarding and documentation
- Platform operations runbooks
```

**Expected Features Tested**:
- `wistx_design_architecture` (platform engineering, multi-cloud) - action="initialize" or "design", project_type="platform", cloud_provider="multi-cloud"
- `wistx_manage_infrastructure_lifecycle` (integration patterns, multi-cloud) - action="integrate" with components across multiple clouds, integration_type=["networking", "security", "monitoring", "service"]
- `wistx_get_compliance_requirements` (platform compliance) - resource_types=["EKS", "GKE", "AKS", "Kubernetes"], standards=["SOC2", "PCI-DSS"]
- `wistx_calculate_infrastructure_cost` (platform costs, multi-cloud) - resources array with compute, storage, networking across AWS, GCP, Azure
- `wistx_get_devops_infra_code_examples` (platform patterns, Terraform, Kubernetes) - query with code_types=["terraform", "kubernetes", "helm"], cloud_provider="multi-cloud"
- `wistx_research_knowledge_base` (platform engineering best practices) - query with domains=["platform", "infrastructure"], content_types=["pattern", "best_practice"]
- `wistx_generate_documentation` (platform docs, runbooks) - document_type="architecture_diagram", "runbook", "deployment_guide"
- `wistx_manage_infrastructure_lifecycle` (create, monitor, optimize) - action="create", action="monitor", action="optimize" with infrastructure_type="kubernetes" or "multi_cloud"

---

### Prompt 4.2: Kubernetes Platform with Advanced Observability and SRE Practices

**Complexity Level**: Very High  
**Estimated Tool Calls**: 10-15  
**Domain**: Platform Engineering, Infrastructure Engineering, SRE

**Prompt**:
```
I'm building a production-grade Kubernetes platform for a SaaS company with 50 microservices serving 5 million users. The platform must implement SRE best practices with comprehensive observability, reliability, and performance optimization.

**Platform Requirements**:
1. **Kubernetes Infrastructure**:
   - 3 EKS clusters (dev, staging, prod) across 2 regions
   - Karpenter for dynamic node provisioning
   - Cluster autoscaling (2-200 nodes per cluster)
   - Multi-zone deployment for high availability
   - Network policies for micro-segmentation
   - Pod security policies and OPA Gatekeeper
2. **Observability Stack**:
   - **Metrics**: Prometheus with Thanos for long-term storage
   - **Logging**: Loki with Grafana for log aggregation
   - **Tracing**: Tempo with OpenTelemetry instrumentation
   - **APM**: Custom dashboards for application performance
   - **SLO/SLI Tracking**: Automated SLO monitoring and alerting
   - **Error Budget Tracking**: Track and alert on error budget consumption
3. **Service Mesh**:
   - Istio for traffic management, security, observability
   - mTLS between services
   - Circuit breakers and retry policies
   - Rate limiting and quota management
   - A/B testing and canary deployments
4. **Reliability Features**:
   - Automated health checks and self-healing
   - Graceful shutdown and zero-downtime deployments
   - Chaos engineering (Chaos Mesh integration)
   - Disaster recovery automation
   - Backup and restore procedures
5. **Performance Optimization**:
   - Resource request/limit optimization
   - HPA (Horizontal Pod Autoscaler) and VPA (Vertical Pod Autoscaler)
   - Cluster autoscaling
   - Network performance tuning
   - Storage performance optimization
6. **SRE Practices**:
   - SLI/SLO definition and monitoring
   - Error budget management
   - Incident response automation
   - On-call rotation and alerting
   - Post-mortem automation
   - Capacity planning
7. **Integration Requirements**:
   - Connect observability stack to PagerDuty for alerting
   - Integrate with Slack for notifications
   - Connect to Jira for incident tracking
   - Integrate with existing CI/CD (GitLab CI)
   - Connect to external databases (RDS, ElastiCache)

**SLO Requirements**:
- Availability: 99.95% (4.38 hours downtime/year)
- Latency: p95 < 200ms, p99 < 500ms
- Error Rate: < 0.1%
- Throughput: Handle 10K requests/second

Please provide:
- Complete platform architecture with observability integration
- Kubernetes manifests (Deployments, Services, ConfigMaps, etc.)
- Helm charts for observability stack
- SLO/SLI definitions and monitoring setup
- Integration patterns for all external systems
- SRE runbooks and incident response procedures
- Performance optimization recommendations
- Cost analysis and optimization strategies
- Compliance considerations (SOC2, CIS Kubernetes)
```

**Expected Features Tested**:
- `wistx_design_architecture` (Kubernetes platform, observability) - action="design", project_type="kubernetes", architecture_type="microservices"
- `wistx_manage_infrastructure_lifecycle` (integration patterns, monitoring) - action="integrate" with integration_type="monitoring", action="monitor"
- `wistx_get_devops_infra_code_examples` (Kubernetes, Prometheus, Istio, SRE) - query with code_types=["kubernetes", "prometheus", "grafana"], services=["eks", "prometheus", "istio"]
- `wistx_research_knowledge_base` (SRE best practices, observability patterns) - query with domains=["sre", "platform"], content_types=["best_practice", "pattern"]
- `wistx_calculate_infrastructure_cost` (platform costs, optimization) - resources with EKS nodes, monitoring stack components
- `wistx_get_compliance_requirements` (Kubernetes compliance) - resource_types=["EKS", "Kubernetes"], standards=["SOC2", "CIS"]
- `wistx_generate_documentation` (SRE runbooks, platform docs) - document_type="runbook", "deployment_guide"
- `wistx_manage_infrastructure_lifecycle` (monitor, optimize) - action="monitor" and action="optimize" with infrastructure_type="kubernetes"

---

## 5. Cloud Engineering

### Prompt 5.1: Multi-Cloud Disaster Recovery and Business Continuity

**Complexity Level**: Very High  
**Estimated Tool Calls**: 12-18  
**Domain**: Cloud Engineering, Infrastructure Engineering, Platform Engineering

**Prompt**:
```
I need to design and implement a comprehensive multi-cloud disaster recovery (DR) and business continuity plan for a critical financial services application with RTO of 15 minutes and RPO of 5 minutes.

**Current Infrastructure (Primary - AWS)**:
- **Compute**: 100 EC2 instances across 3 AZs in us-east-1
- **Databases**: 
  - 5 RDS PostgreSQL Multi-AZ instances (primary databases)
  - 3 ElastiCache Redis clusters (caching layer)
  - 2 DocumentDB clusters (NoSQL data)
- **Storage**: 
  - 20 S3 buckets (500TB total, various storage classes)
  - 10 EBS volumes (50TB total)
- **Networking**: 
  - VPC with public/private subnets across 3 AZs
  - Application Load Balancer
  - CloudFront CDN
- **Kubernetes**: 2 EKS clusters (50 nodes each)
- **Message Queues**: SQS, SNS, EventBridge
- **Monitoring**: CloudWatch, X-Ray

**DR Requirements**:
1. **Multi-Cloud DR Strategy**:
   - **Secondary Site**: GCP (us-central1) - Hot standby
   - **Tertiary Site**: Azure (eastus) - Warm standby
   - Cross-cloud replication for all data
   - Automated failover and failback procedures
2. **Data Replication**:
   - Real-time database replication (RDS → Cloud SQL → Azure Database)
   - S3 → GCS → Azure Blob Storage replication
   - Cross-region and cross-cloud replication
   - Data consistency verification
3. **Network Design**:
   - VPN/Interconnect between clouds
   - DNS failover (Route53 → Cloud DNS → Azure DNS)
   - Global load balancing across clouds
   - Network segmentation and security
4. **Automation**:
   - Automated DR testing (monthly)
   - Failover automation (one-click or automated)
   - Health check and monitoring across all sites
   - Automated failback procedures
5. **Compliance**:
   - Meet PCI-DSS requirements for DR
   - SOC2 compliance for DR procedures
   - Data residency requirements (some data must stay in specific regions)
6. **Cost Optimization**:
   - Minimize DR infrastructure costs (use smaller instances, spot/preemptible)
   - Optimize data transfer costs
   - Right-size DR resources
7. **Integration Requirements**:
   - Connect DR sites to primary monitoring systems
   - Integrate with incident management (PagerDuty)
   - Connect to backup systems
   - Integrate with change management

**Testing Requirements**:
- Monthly automated DR tests
- Quarterly full DR drills
- Annual business continuity exercises
- Automated test result reporting

Please provide:
- Complete multi-cloud DR architecture design
- Data replication strategies and implementation
- Network connectivity design (VPN, Interconnect, Direct Connect)
- Automated failover/failback procedures
- DR testing automation and procedures
- Cost analysis for DR infrastructure
- Compliance verification for DR setup
- Runbooks for DR operations
- Integration patterns for monitoring and alerting
```

**Expected Features Tested**:
- `wistx_design_architecture` (multi-cloud DR, business continuity) - action="design", cloud_provider="multi-cloud", architecture_type="event-driven"
- `wistx_manage_infrastructure_lifecycle` (backup, restore, integration patterns) - action="backup" with backup_type="full", action="restore", action="integrate" for cross-cloud connectivity
- `wistx_calculate_infrastructure_cost` (DR costs, multi-cloud) - resources across AWS, GCP, Azure for DR sites
- `wistx_get_compliance_requirements` (DR compliance, PCI-DSS, SOC2) - resource_types=["RDS", "S3", "EC2", "CloudSQL", "GCS", "Azure Database", "Blob Storage"], standards=["PCI-DSS", "SOC2"]
- `wistx_get_devops_infra_code_examples` (DR patterns, multi-cloud, replication) - query with code_types=["terraform"], cloud_provider="multi-cloud"
- `wistx_research_knowledge_base` (DR best practices, business continuity) - query with domains=["infrastructure", "compliance"], content_types=["best_practice", "strategy"]
- `wistx_generate_documentation` (DR runbooks, procedures) - document_type="runbook", "deployment_guide"
- `wistx_manage_infrastructure_lifecycle` (backup, restore, monitor) - action="backup", action="restore", action="monitor" with infrastructure_type="multi_cloud"

---

### Prompt 5.2: Cloud Resource Discovery and Terraform Import Automation

**Complexity Level**: Very High  
**Estimated Tool Calls**: 8-12  
**Domain**: Cloud Engineering, Infrastructure Engineering

**Prompt**:
```
I've inherited an AWS account with 500+ manually created resources that need to be converted to Infrastructure as Code (Terraform). The resources span multiple regions and services, and I need to discover, analyze, and import them all into Terraform with proper dependency resolution.

**Resource Inventory (Estimated)**:
- **Compute**: 150 EC2 instances across 5 regions
- **Databases**: 25 RDS instances, 10 ElastiCache clusters, 5 DocumentDB clusters
- **Storage**: 100 S3 buckets, 50 EBS volumes, 10 EFS file systems
- **Networking**: 10 VPCs, 50 subnets, 20 route tables, 15 security groups, 5 NAT gateways, 3 VPN connections
- **Load Balancing**: 10 ALBs, 5 NLBs, 3 Classic Load Balancers
- **Kubernetes**: 3 EKS clusters with associated node groups
- **IAM**: 200 IAM roles, 150 IAM policies, 50 users
- **Other**: CloudFront distributions, API Gateway APIs, Lambda functions, SQS queues, SNS topics, EventBridge rules, KMS keys, Secrets Manager secrets

**Requirements**:
1. **Discovery**:
   - Discover all resources across all regions
   - Identify resource dependencies and relationships
   - Map resources to environments (dev, staging, prod) using tags
   - Identify resources already managed by Terraform (in state files)
   - Group resources by logical applications/services
2. **Analysis**:
   - Compliance analysis (PCI-DSS, SOC2) for discovered resources
   - Cost analysis for all discovered resources
   - Security analysis (publicly accessible resources, misconfigurations)
   - Best practices review
   - Identify optimization opportunities
3. **Terraform Generation**:
   - Generate Terraform code for all resources
   - Proper dependency resolution (VPCs before subnets, subnets before instances, etc.)
   - Resource naming conventions
   - Tag management
   - State file organization (by environment, by service)
   - Import commands with correct order
4. **Import Strategy**:
   - Dependency-ordered import plan
   - Batch import scripts
   - Validation after import
   - State file management
5. **Post-Import**:
   - Refactor Terraform code for best practices
   - Implement modules for reusable patterns
   - Add compliance controls
   - Cost optimization
   - Documentation generation

**Constraints**:
- Some resources are in use 24/7 and cannot have downtime
- Some resources have complex dependencies (e.g., EKS clusters with node groups, autoscaling groups)
- Need to maintain existing resource IDs and configurations
- Must preserve all tags and metadata

Please provide:
- Complete resource discovery and analysis
- Terraform code generation with dependency resolution
- Import plan with step-by-step procedures
- Compliance and security analysis
- Cost analysis and optimization recommendations
- Best practices refactoring suggestions
- Documentation for all discovered resources
```

**Expected Features Tested**:
- `wistx_discover_cloud_resources` (AWS resource discovery, Terraform generation) - role_arn and external_id or connection_name, regions array, resource_types filter, include_compliance=True, include_pricing=True, generate_diagrams=True
- `wistx_get_existing_infrastructure` (infrastructure analysis, compliance, costs) - repository_url required (if Terraform code exists), include_compliance=True, include_costs=True
- `wistx_get_compliance_requirements` (compliance for discovered resources) - resource_types from discovery results, standards=["PCI-DSS", "SOC2"]
- `wistx_calculate_infrastructure_cost` (cost analysis for discovered resources) - resources array built from discovered resources
- `wistx_get_devops_infra_code_examples` (Terraform import patterns, best practices) - query with code_types=["terraform"], cloud_provider="aws"
- `wistx_research_knowledge_base` (Terraform import best practices) - query with domains=["infrastructure"], content_types=["guide", "best_practice"]
- `wistx_generate_documentation` (infrastructure documentation) - document_type="architecture_diagram", infrastructure_code from discovery
- `wistx_manage_infrastructure_lifecycle` (analyze, optimize) - action="analyze" with infrastructure_code, action="optimize"

---

## Usage Instructions

### For Testing
1. Use these prompts in your AI coding assistant (Claude Desktop, Cursor, etc.) with WISTX MCP server connected
2. Monitor which tools are called and in what order
3. Verify that responses are comprehensive and accurate
4. Check that all requested information is provided
5. Validate that code examples are production-ready
6. Ensure compliance analysis covers all standards mentioned
7. Verify cost calculations are accurate and include optimizations

### For Product Validation
1. Test each prompt to ensure all features work correctly
2. Verify tool integration and data flow
3. Check response quality and completeness
4. Validate that complex multi-tool workflows execute properly
5. Ensure error handling works for edge cases
6. Test performance with large result sets
7. Verify compliance with rate limits and quotas

### For Documentation
1. Use these prompts as examples in product documentation
2. Reference them in marketing materials
3. Include in user onboarding and training
4. Use as benchmarks for product capabilities

---

## Notes

- Each prompt is designed to test multiple features simultaneously
- Prompts are based on real-world DevOps engineering scenarios
- All prompts require comprehensive responses with code examples
- Prompts test both individual tool capabilities and tool orchestration
- Complexity levels are intentionally high to stress-test the system
- Estimated tool calls are conservative - actual usage may vary

