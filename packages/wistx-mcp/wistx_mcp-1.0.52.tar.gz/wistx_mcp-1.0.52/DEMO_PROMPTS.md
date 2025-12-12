# WISTX Demo Prompts

## 🎯 4 Real-Life Prompts for Customer Demos

### Prompt 1: Compliance Requirements Check
**Use Case:** DevOps engineer needs to ensure infrastructure meets compliance standards before deployment

**Prompt:**
```
I'm building a new payment processing system on AWS that will handle credit card transactions. 
I need to ensure my infrastructure meets PCI-DSS Level 1 requirements. 

Can you check the compliance requirements for:
- RDS PostgreSQL database (will store encrypted cardholder data)
- S3 buckets (for storing transaction logs)
- EKS cluster (for running the payment API)
- Lambda functions (for processing webhooks)

Please provide:
1. Critical and high severity controls for each resource
2. Specific remediation guidance for any gaps
3. Verification procedures to ensure compliance
```

**Why this works:**
- Real-world scenario (payment processing)
- Multiple resource types (shows breadth)
- Specific compliance standard (PCI-DSS)
- Actionable output (remediation + verification)
- Shows compliance expertise

---

### Prompt 2: Infrastructure Cost Calculation & Optimization
**Use Case:** FinOps team needs to estimate costs and find optimization opportunities

**Prompt:**
```
I'm planning a multi-cloud infrastructure deployment and need cost estimates:

AWS:
- 3x RDS PostgreSQL db.t3.medium instances in us-east-1
- 2x EKS clusters with 10x m5.large nodes each in us-west-2
- 5TB S3 storage in us-east-1

GCP:
- 2x Cloud SQL PostgreSQL db-standard-2 instances in us-central1
- 1x GKE cluster with 8x n1-standard-2 nodes in us-east1

Azure:
- 1x Azure Database for PostgreSQL (General Purpose, 2 vCores) in eastus

Please:
1. Calculate monthly and annual costs for each cloud provider
2. Provide a cost breakdown by service
3. Suggest cost optimization opportunities (reserved instances, spot instances, etc.)
4. Compare total costs across providers
```

**Why this works:**
- Multi-cloud scenario (shows flexibility)
- Real resource types and regions
- FinOps focus (cost optimization)
- Actionable recommendations
- Shows pricing expertise across all major clouds

---

### Prompt 3: Architecture Design with Compliance Built-In
**Use Case:** Platform engineer designing new infrastructure that must be compliant from day one

**Prompt:**
```
I need to design a HIPAA-compliant healthcare data platform on AWS that will:
- Store PHI (Protected Health Information) for 100,000+ patients
- Process real-time analytics on patient data
- Handle API requests from mobile apps and web portals
- Support multi-region disaster recovery
- Scale to handle 10x growth over 2 years

Requirements:
- Must comply with HIPAA
- Must have encryption at rest and in transit
- Must support audit logging
- Must have automated backups
- Must support compliance reporting

Please design the architecture with:
1. Specific AWS services and configurations
2. Security controls and encryption setup
3. Compliance controls mapped to HIPAA requirements
4. Cost estimates for the initial deployment
5. Terraform code examples for key components
```

**Why this works:**
- End-to-end architecture design
- Compliance-first approach
- Real constraints (HIPAA, scalability)
- Includes code examples
- Shows integration of multiple WISTX capabilities

---

### Prompt 4: Production-Ready Code Examples Search
**Use Case:** DevOps engineer needs reference implementations for specific infrastructure patterns

**Prompt:**
```
I'm implementing a secure, compliant Kubernetes deployment for a financial services application. 
I need production-ready code examples for:

1. Kubernetes deployment with:
   - Network policies for pod-to-pod communication
   - Secrets management using external secrets operator
   - Pod security standards (restricted mode)
   - Resource limits and requests
   - Horizontal pod autoscaling

2. Terraform code for:
   - EKS cluster with encryption enabled
   - Node groups with appropriate instance types
   - VPC configuration with private subnets
   - Security groups following least privilege

3. Dockerfile best practices for:
   - Multi-stage builds
   - Non-root user
   - Minimal base images
   - Security scanning

Please provide code examples that:
- Are production-ready (not just tutorials)
- Follow security best practices
- Include compliance considerations (SOC2, CIS benchmarks)
- Have quality scores above 80
```

**Why this works:**
- Multiple code types (Kubernetes, Terraform, Docker)
- Production-focused (not just learning)
- Security and compliance emphasis
- Quality filtering
- Shows code example curation

---

## 🎬 Demo Flow Recommendations

### Quick Demo (5-10 minutes)
Use **Prompt 1** (Compliance Requirements) - Shows immediate value, quick results

### Standard Demo (15-20 minutes)
1. Start with **Prompt 1** (Compliance) - 5 min
2. Show **Prompt 2** (Cost Calculation) - 5 min
3. End with **Prompt 4** (Code Examples) - 5 min

### Deep Dive Demo (30-45 minutes)
1. **Prompt 3** (Architecture Design) - 15 min
   - Show how WISTX guides through entire design process
   - Highlight compliance integration
   - Show cost estimates
2. **Prompt 1** (Compliance Deep Dive) - 10 min
   - Show remediation guidance
   - Show verification procedures
3. **Prompt 2** (Cost Optimization) - 10 min
   - Show multi-cloud comparison
   - Show optimization recommendations
4. **Prompt 4** (Code Examples) - 5 min
   - Show production-ready examples
   - Show quality filtering

---

## 💡 Key Selling Points to Highlight

### During Prompt 1 (Compliance)
- ✅ "No more searching through compliance docs manually"
- ✅ "Get specific controls mapped to your resources"
- ✅ "Remediation guidance included"
- ✅ "Works across PCI-DSS, HIPAA, SOC2, NIST, ISO 27001"

### During Prompt 2 (Cost)
- ✅ "Real-time pricing from AWS/GCP/Azure"
- ✅ "Multi-cloud cost comparison"
- ✅ "Optimization suggestions built-in"
- ✅ "No more manual calculator spreadsheets"

### During Prompt 3 (Architecture)
- ✅ "Compliance built-in from day one"
- ✅ "End-to-end guidance, not just snippets"
- ✅ "Includes code examples"
- ✅ "Cost estimates included"

### During Prompt 4 (Code Examples)
- ✅ "Production-ready, not tutorials"
- ✅ "Curated from real-world repos"
- ✅ "Quality-scored examples"
- ✅ "Compliance-aware code"

---

## 🎯 Target Audience Mapping

| Prompt | Best For | Key Value Prop |
|--------|----------|----------------|
| Prompt 1 | Compliance Officers, Security Engineers | "Stop compliance guesswork" |
| Prompt 2 | FinOps Teams, CTOs, CFOs | "Accurate cost estimates instantly" |
| Prompt 3 | Platform Engineers, Architects | "Design compliant infrastructure faster" |
| Prompt 4 | DevOps Engineers, SREs | "Find production-ready code examples" |

---

## 📝 Customization Tips

### For Enterprise Customers
- Add more compliance standards (FedRAMP, NIST-800-53)
- Emphasize audit trail and documentation
- Show integration with existing tools

### For Startups
- Focus on Prompt 2 (cost optimization)
- Emphasize speed and automation
- Show how to avoid costly mistakes

### For Healthcare/Finance
- Emphasize Prompt 1 and Prompt 3
- Focus on HIPAA/PCI-DSS
- Show security-first approach

### For Multi-Cloud Teams
- Emphasize Prompt 2 (multi-cloud comparison)
- Show cloud-agnostic best practices
- Highlight cost optimization across clouds




