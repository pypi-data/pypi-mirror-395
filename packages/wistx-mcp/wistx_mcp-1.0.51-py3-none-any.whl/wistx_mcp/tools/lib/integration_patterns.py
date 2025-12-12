"""Integration patterns library for infrastructure component integration."""

from typing import Any

INTEGRATION_PATTERNS: dict[str, dict[str, dict[str, Any]]] = {
    "networking": {
        "vpc_peering": {
            "description": "VPC peering enables secure, private network connectivity between two VPCs, allowing resources in different VPCs to communicate as if they were on the same network. This pattern is essential for multi-VPC architectures, cross-account connectivity, and hybrid cloud deployments. VPC peering establishes a direct network connection without traversing the public internet, providing low latency and enhanced security. The pattern includes route table configuration, security group rules, and CIDR block management to ensure proper traffic routing and access control.",
            "providers": ["aws", "gcp", "azure"],
            "components": ["vpc", "subnet", "route_table"],
            "terraform_example": """
resource "aws_vpc_peering_connection" "peer" {
  vpc_id      = var.vpc_id
  peer_vpc_id = var.peer_vpc_id
  auto_accept = true
}

resource "aws_route" "peer_route" {
  route_table_id            = var.route_table_id
  destination_cidr_block    = var.peer_cidr_block
  vpc_peering_connection_id = aws_vpc_peering_connection.peer.id
}
""",
            "dependencies": [
                "Network connectivity between VPCs",
                "VPC configuration with non-overlapping CIDR blocks",
                "Route tables configured in both VPCs",
                "Security groups or network ACLs for access control",
            ],
            "security_rules": [
                "Restrict network access to necessary ports only",
                "Use security groups/network policies for access control",
                "Enable encryption in transit (TLS/SSL)",
                "Implement network segmentation",
                "Use private endpoints where possible",
                "Audit VPC peering connections regularly",
            ],
            "monitoring_config": {
                "metrics": [
                    "VPC peering connection status",
                    "Network traffic volume between VPCs",
                    "Packet loss and latency metrics",
                    "Route table propagation status",
                ],
                "alarms": [
                    "VPC peering connection down alarm",
                    "High latency alarm (> 100ms)",
                    "Unusual traffic pattern alarm",
                ],
                "logs": [
                    "VPC Flow Logs for traffic analysis",
                    "CloudWatch Logs for connection events",
                ],
            },
            "implementation_guidance": [
                "1. Ensure VPC CIDR blocks do not overlap",
                "2. Create VPC peering connection between source and destination VPCs",
                "3. Configure route tables in both VPCs to route traffic through peering connection",
                "4. Update security groups to allow traffic from peer VPC CIDR blocks",
                "5. Test connectivity between resources in both VPCs",
                "6. Monitor peering connection status and network metrics",
            ],
            "compliance_considerations": [
                "PCI-DSS: Ensure network segmentation for cardholder data",
                "HIPAA: Encrypt all PHI in transit between VPCs",
                "SOC2: Document network access controls and peering relationships",
                "GDPR: Ensure data transfer mechanisms comply with regulations",
            ],
        },
        "vpn": {
            "description": "VPN (Virtual Private Network) connection provides secure, encrypted connectivity between on-premises networks and cloud VPCs, or between different cloud regions. This pattern enables remote access, site-to-site connectivity, and hybrid cloud architectures. VPN connections use IPsec (Internet Protocol Security) for encryption and authentication, ensuring data confidentiality and integrity. The pattern includes VPN gateway configuration, customer gateway setup, routing configuration, and security policies to establish and maintain secure network tunnels.",
            "providers": ["aws", "gcp", "azure"],
            "components": ["vpn_gateway", "customer_gateway", "vpn_connection"],
            "terraform_example": """
resource "aws_vpn_gateway" "vpn_gw" {
  vpc_id = var.vpc_id
}

resource "aws_customer_gateway" "customer_gw" {
  bgp_asn    = 65000
  ip_address = var.customer_gateway_ip
  type      = "ipsec.1"
}

resource "aws_vpn_connection" "vpn" {
  vpc_gateway_id      = aws_vpn_gateway.vpn_gw.id
  customer_gateway_id = aws_customer_gateway.customer_gw.id
  type                = "ipsec.1"
}
""",
            "dependencies": [
                "VPN gateway in cloud VPC",
                "Customer gateway device (on-premises or remote)",
                "Static IP address for customer gateway",
                "BGP ASN configuration (if using dynamic routing)",
                "Route tables configured for VPN traffic",
            ],
            "security_rules": [
                "Use strong IPsec encryption (AES-256)",
                "Enable perfect forward secrecy (PFS)",
                "Restrict VPN access to authorized networks only",
                "Use security groups/network ACLs for access control",
                "Enable VPN connection logging and monitoring",
                "Rotate VPN pre-shared keys regularly",
            ],
            "monitoring_config": {
                "metrics": [
                    "VPN tunnel status (up/down)",
                    "VPN connection latency",
                    "Data transfer volume (bytes in/out)",
                    "Tunnel utilization percentage",
                ],
                "alarms": [
                    "VPN tunnel down alarm",
                    "High latency alarm (> 200ms)",
                    "Unusual traffic pattern alarm",
                ],
                "logs": [
                    "VPN connection logs",
                    "CloudWatch Logs for connection events",
                ],
            },
            "implementation_guidance": [
                "1. Create VPN gateway and attach to VPC",
                "2. Configure customer gateway with public IP and BGP ASN",
                "3. Create VPN connection between VPN gateway and customer gateway",
                "4. Configure route tables to route traffic through VPN connection",
                "5. Update security groups to allow VPN traffic",
                "6. Test connectivity and verify tunnel status",
                "7. Monitor VPN connection metrics and logs",
            ],
            "compliance_considerations": [
                "PCI-DSS: Encrypt all cardholder data in transit via VPN",
                "HIPAA: Ensure VPN encryption meets HIPAA requirements",
                "SOC2: Document VPN access controls and monitoring",
                "NIST: Follow NIST guidelines for VPN configuration",
            ],
        },
        "privatelink": {
            "description": "AWS PrivateLink provides private connectivity between VPCs and AWS services, or between VPCs and your own services, without exposing traffic to the public internet. This pattern enhances security by keeping traffic within the AWS network, reduces data transfer costs, and simplifies network architecture. PrivateLink uses VPC endpoints (Gateway or Interface endpoints) to establish private connections to services like S3, DynamoDB, or custom services. The pattern includes endpoint configuration, route table updates, security group rules, and endpoint policies for fine-grained access control.",
            "providers": ["aws"],
            "components": ["vpc_endpoint", "service"],
            "terraform_example": """
resource "aws_vpc_endpoint" "s3" {
  vpc_id       = var.vpc_id
  service_name = "com.amazonaws.${var.region}.s3"
  vpc_endpoint_type = "Gateway"
}
""",
            "dependencies": [
                "VPC with subnets in multiple availability zones",
                "Route tables configured for endpoint traffic",
                "Security groups for Interface endpoints",
                "Endpoint service (for service provider)",
            ],
            "security_rules": [
                "Use VPC endpoint policies to restrict access",
                "Enable endpoint connection acceptance controls",
                "Use security groups for Interface endpoints",
                "Monitor endpoint traffic and connections",
                "Restrict endpoint access to authorized principals only",
            ],
            "monitoring_config": {
                "metrics": [
                    "VPC endpoint connection count",
                    "Data transfer volume through endpoint",
                    "Endpoint availability and health",
                    "Connection acceptance/rejection rate",
                ],
                "alarms": [
                    "VPC endpoint connection failure alarm",
                    "High data transfer cost alarm",
                    "Endpoint health check failure alarm",
                ],
                "logs": [
                    "VPC Flow Logs for endpoint traffic",
                    "CloudWatch Logs for endpoint events",
                ],
            },
            "implementation_guidance": [
                "1. Identify AWS services or custom services to access privately",
                "2. Create VPC endpoint (Gateway for S3/DynamoDB, Interface for others)",
                "3. Configure route tables to route traffic through endpoint",
                "4. Update security groups for Interface endpoints",
                "5. Configure endpoint policies for access control",
                "6. Test connectivity and verify traffic routes through endpoint",
                "7. Monitor endpoint metrics and costs",
            ],
            "compliance_considerations": [
                "PCI-DSS: Ensure private connectivity for cardholder data",
                "HIPAA: Use PrivateLink for PHI data transfer",
                "SOC2: Document endpoint access controls",
                "GDPR: Ensure data transfer mechanisms comply with regulations",
            ],
        },
    },
    "security": {
        "security_groups": {
            "description": "Security groups act as virtual firewalls for EC2 instances and other AWS resources, controlling inbound and outbound traffic at the instance level. This pattern implements network access control using stateful firewall rules based on IP addresses, ports, and protocols. Security groups provide a fundamental security layer for cloud resources, enabling least-privilege access principles. The pattern includes ingress and egress rule configuration, security group references for inter-group communication, and integration with network ACLs for defense-in-depth security strategies.",
            "providers": ["aws"],
            "components": ["security_group", "instance"],
            "terraform_example": """
resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Security group for web servers"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
""",
            "dependencies": [
                "VPC configuration",
                "Network ACLs (optional, for additional layer)",
                "IAM permissions for security group management",
            ],
            "security_rules": [
                "Implement least privilege access (restrict to necessary ports only)",
                "Use security group references instead of CIDR blocks when possible",
                "Enable VPC Flow Logs for security group traffic analysis",
                "Regularly audit security group rules for unused or overly permissive rules",
                "Use separate security groups for different application tiers",
                "Enable security group change tracking and alerts",
            ],
            "monitoring_config": {
                "metrics": [
                    "Security group rule count",
                    "Traffic volume per security group",
                    "Security group rule changes",
                ],
                "alarms": [
                    "Security group rule change alarm",
                    "Unusual traffic pattern alarm",
                    "Overly permissive rule detection alarm",
                ],
                "logs": [
                    "VPC Flow Logs for security group traffic",
                    "CloudTrail logs for security group changes",
                ],
            },
            "implementation_guidance": [
                "1. Identify network access requirements for resources",
                "2. Create security groups for each application tier (web, app, database)",
                "3. Configure ingress rules with least privilege (specific ports and sources)",
                "4. Configure egress rules (restrict to necessary destinations)",
                "5. Attach security groups to resources",
                "6. Test connectivity and verify rules work as expected",
                "7. Monitor security group metrics and audit rules regularly",
            ],
            "compliance_considerations": [
                "PCI-DSS: Implement strong access controls for cardholder data",
                "HIPAA: Restrict network access to authorized systems only",
                "SOC2: Document security group rules and access controls",
                "NIST: Follow least privilege principle for network access",
            ],
        },
        "iam_roles": {
            "description": "IAM roles provide secure, temporary credentials for AWS services and applications, eliminating the need for hardcoded access keys. This pattern implements role-based access control (RBAC) following the least privilege principle, allowing services to assume roles and access only the resources they need. IAM roles support cross-service authentication, enable fine-grained permissions through policies, and integrate with identity providers for federated access. The pattern includes role creation, trust policy configuration, permission policies, and role assumption for secure service-to-service communication.",
            "providers": ["aws", "gcp", "azure"],
            "components": ["iam_role", "service"],
            "terraform_example": """
resource "aws_iam_role" "lambda_role" {
  name = "lambda-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}
""",
            "dependencies": [
                "IAM service permissions",
                "Trust policy configuration",
                "Permission policies (managed or custom)",
            ],
            "security_rules": [
                "Implement least privilege access (grant minimum required permissions)",
                "Use IAM roles instead of access keys (avoid hardcoded credentials)",
                "Enable audit logging for all IAM role usage (CloudTrail)",
                "Rotate role credentials regularly",
                "Use condition keys to restrict role access (IP, time, MFA)",
                "Review and audit IAM role permissions regularly",
            ],
            "monitoring_config": {
                "metrics": [
                    "IAM role assumption count",
                    "Failed role assumption attempts",
                    "Role usage by service",
                ],
                "alarms": [
                    "Failed role assumption alarm",
                    "Unusual role usage pattern alarm",
                    "Role permission change alarm",
                ],
                "logs": [
                    "CloudTrail logs for IAM role events",
                    "CloudWatch Logs for role assumption events",
                ],
            },
            "implementation_guidance": [
                "1. Identify service authentication requirements",
                "2. Create IAM role with appropriate trust policy",
                "3. Attach permission policies following least privilege",
                "4. Configure role assumption conditions (if needed)",
                "5. Attach role to service (EC2, Lambda, ECS, etc.)",
                "6. Test service access and verify permissions",
                "7. Monitor role usage and audit permissions regularly",
            ],
            "compliance_considerations": [
                "PCI-DSS: Implement strong access controls for cardholder data",
                "HIPAA: Use role-based access control (RBAC) for PHI access",
                "SOC2: Enable audit logging for all IAM role access",
                "NIST: Follow least privilege principle for access control",
            ],
        },
        "network_policies": {
            "description": "Kubernetes Network Policies provide fine-grained network access control for pods, enabling micro-segmentation and defense-in-depth security strategies. This pattern implements pod-to-pod communication rules based on labels, namespaces, and ports, allowing administrators to define which pods can communicate with each other. Network policies work with CNI plugins (like Calico, Cilium, or Weave) to enforce rules at the network layer. The pattern includes policy definition, pod selector configuration, ingress/egress rules, and integration with service mesh for advanced traffic management.",
            "providers": ["kubernetes"],
            "components": ["network_policy", "pod"],
            "kubernetes_example": """
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
""",
            "dependencies": [
                "Kubernetes cluster with CNI plugin supporting Network Policies",
                "Pod labels for policy targeting",
                "Namespace configuration",
            ],
            "security_rules": [
                "Implement default deny-all policy, then allow specific traffic",
                "Use pod labels and namespaces for policy targeting",
                "Restrict ingress to necessary ports and sources only",
                "Restrict egress to necessary destinations and ports",
                "Regularly audit network policies for unused or overly permissive rules",
                "Use network policy testing tools to validate rules",
            ],
            "monitoring_config": {
                "metrics": [
                    "Network policy rule count",
                    "Blocked connection attempts",
                    "Policy evaluation time",
                ],
                "alarms": [
                    "High blocked connection rate alarm",
                    "Network policy change alarm",
                ],
                "logs": [
                    "CNI plugin logs for policy enforcement",
                    "Kubernetes audit logs for policy changes",
                ],
            },
            "implementation_guidance": [
                "1. Ensure CNI plugin supports Network Policies",
                "2. Create default deny-all policy for namespace",
                "3. Define pod labels for policy targeting",
                "4. Create ingress rules allowing necessary pod-to-pod communication",
                "5. Create egress rules allowing necessary outbound traffic",
                "6. Test pod connectivity and verify policies work as expected",
                "7. Monitor network policy metrics and audit rules regularly",
            ],
            "compliance_considerations": [
                "PCI-DSS: Implement network segmentation for cardholder data",
                "HIPAA: Restrict network access to authorized pods only",
                "SOC2: Document network policy rules and access controls",
                "NIST: Follow least privilege principle for network access",
            ],
        },
    },
    "service": {
        "api_gateway_lambda": {
            "description": "API Gateway to Lambda integration creates a serverless API architecture where API Gateway handles HTTP requests and routes them to Lambda functions for processing. This pattern enables scalable, cost-effective API development without managing servers, supports multiple API types (REST, HTTP, WebSocket), and provides built-in features like authentication, rate limiting, request validation, and response transformation. The pattern includes API Gateway configuration, Lambda function setup, integration mapping, deployment stages, and monitoring for production-ready serverless APIs.",
            "providers": ["aws"],
            "components": ["api_gateway", "lambda"],
            "terraform_example": """
resource "aws_api_gateway_rest_api" "api" {
  name = "my-api"
}

resource "aws_api_gateway_resource" "resource" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "hello"
}

resource "aws_api_gateway_method" "method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.resource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "integration" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.resource.id
  http_method = aws_api_gateway_method.method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.lambda.invoke_arn
}
""",
            "dependencies": [
                "Lambda function with appropriate IAM role",
                "API Gateway REST API or HTTP API",
                "Lambda function handler code",
            ],
            "security_rules": [
                "Use secure communication protocols (HTTPS only)",
                "Implement authentication and authorization (API keys, IAM, Cognito)",
                "Enable request validation and rate limiting",
                "Use API keys or OAuth tokens for access control",
                "Implement WAF rules for API protection",
                "Enable API Gateway logging and monitoring",
            ],
            "monitoring_config": {
                "metrics": [
                    "API Gateway request count",
                    "Lambda invocation count",
                    "API latency (p50, p95, p99)",
                    "Error rate (4xx, 5xx)",
                    "Integration latency",
                ],
                "alarms": [
                    "High error rate alarm (> 1% for 5 minutes)",
                    "Latency alarm (p95 > 1 second)",
                    "Lambda function error alarm",
                ],
                "logs": [
                    "API Gateway access logs",
                    "CloudWatch Logs for Lambda execution",
                    "X-Ray traces for distributed tracing",
                ],
            },
            "implementation_guidance": [
                "1. Create Lambda function with handler code",
                "2. Create API Gateway REST API or HTTP API",
                "3. Define API resources and methods",
                "4. Configure API Gateway integration with Lambda",
                "5. Set up authentication and authorization",
                "6. Deploy API to a stage",
                "7. Test API endpoints and verify integration",
                "8. Monitor API metrics and Lambda performance",
            ],
            "compliance_considerations": [
                "PCI-DSS: Secure API endpoints for cardholder data",
                "HIPAA: Encrypt API-to-Lambda communication",
                "SOC2: Implement authentication and authorization",
                "GDPR: Ensure data processing agreements are in place",
            ],
        },
        "alb_ecs": {
            "description": "Application Load Balancer (ALB) to ECS integration provides scalable, highly available load balancing for containerized applications running on ECS. This pattern distributes incoming traffic across multiple ECS tasks, enables health checks for automatic failover, supports path-based and host-based routing, and integrates with AWS services like WAF, CloudWatch, and Auto Scaling. The pattern includes ALB configuration, target group setup, ECS service integration, health check configuration, and SSL/TLS termination for secure, production-ready container deployments.",
            "providers": ["aws"],
            "components": ["alb", "ecs_service"],
            "terraform_example": """
resource "aws_lb_target_group" "tg" {
  name     = "ecs-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id
}

resource "aws_lb_listener" "listener" {
  load_balancer_arn = aws_lb.alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tg.arn
  }
}

resource "aws_ecs_service" "service" {
  name            = "my-service"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.task.arn
  desired_count   = 2

  load_balancer {
    target_group_arn = aws_lb_target_group.tg.arn
    container_name  = "my-container"
    container_port  = 80
  }
}
""",
            "dependencies": [
                "ECS cluster and service configuration",
                "ECS task definition with container definitions",
                "VPC with subnets in multiple availability zones",
                "Security groups for ALB and ECS tasks",
            ],
            "security_rules": [
                "Use HTTPS listeners with SSL/TLS certificates",
                "Implement security groups with least privilege",
                "Enable WAF for ALB protection",
                "Use private subnets for ECS tasks",
                "Enable access logging for ALB",
                "Implement health checks for automatic failover",
            ],
            "monitoring_config": {
                "metrics": [
                    "ALB request count",
                    "Target response time",
                    "Healthy/unhealthy target count",
                    "HTTP error codes (4xx, 5xx)",
                    "Active connection count",
                ],
                "alarms": [
                    "Unhealthy target alarm",
                    "High error rate alarm (> 5% for 5 minutes)",
                    "High latency alarm (p95 > 1 second)",
                ],
                "logs": [
                    "ALB access logs",
                    "CloudWatch Logs for ECS tasks",
                ],
            },
            "implementation_guidance": [
                "1. Create ALB in VPC with subnets in multiple AZs",
                "2. Create target group for ECS tasks",
                "3. Configure ALB listener with routing rules",
                "4. Create ECS service with load balancer configuration",
                "5. Configure health checks for target group",
                "6. Update security groups to allow ALB-to-task traffic",
                "7. Test load balancing and verify traffic distribution",
                "8. Monitor ALB metrics and ECS service health",
            ],
            "compliance_considerations": [
                "PCI-DSS: Use HTTPS for cardholder data transmission",
                "HIPAA: Encrypt traffic between ALB and ECS tasks",
                "SOC2: Document load balancing and health check procedures",
                "GDPR: Ensure data processing agreements are in place",
            ],
        },
        "ingress_kubernetes": {
            "description": "Kubernetes Ingress provides HTTP and HTTPS routing to services within a cluster, acting as an entry point for external traffic. This pattern enables path-based and host-based routing, SSL/TLS termination, load balancing, and integration with ingress controllers (like NGINX, Traefik, or AWS ALB Ingress Controller). Ingress resources define routing rules that ingress controllers implement, providing a declarative way to manage external access to services. The pattern includes Ingress resource definition, service configuration, ingress controller setup, and TLS certificate management for secure, production-ready Kubernetes deployments.",
            "providers": ["kubernetes"],
            "components": ["ingress", "service"],
            "kubernetes_example": """
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
spec:
  rules:
  - host: example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-service
            port:
              number: 80
""",
            "dependencies": [
                "Kubernetes cluster with ingress controller installed",
                "Kubernetes Service resources",
                "TLS certificates (for HTTPS)",
            ],
            "security_rules": [
                "Use HTTPS with TLS certificates",
                "Implement ingress annotations for security (rate limiting, WAF)",
                "Restrict ingress to necessary hosts and paths",
                "Use network policies in conjunction with ingress",
                "Enable ingress access logging",
                "Regularly rotate TLS certificates",
            ],
            "monitoring_config": {
                "metrics": [
                    "Ingress request count",
                    "Ingress response time",
                    "HTTP error codes (4xx, 5xx)",
                    "Ingress controller pod health",
                ],
                "alarms": [
                    "High error rate alarm",
                    "Ingress controller pod restart alarm",
                    "High latency alarm",
                ],
                "logs": [
                    "Ingress controller access logs",
                    "Kubernetes audit logs for ingress changes",
                ],
            },
            "implementation_guidance": [
                "1. Install and configure ingress controller (NGINX, Traefik, etc.)",
                "2. Create Kubernetes Service for application",
                "3. Create Ingress resource with routing rules",
                "4. Configure TLS certificates (cert-manager or manual)",
                "5. Test ingress routing and verify traffic reaches services",
                "6. Configure ingress annotations for security and features",
                "7. Monitor ingress metrics and controller health",
            ],
            "compliance_considerations": [
                "PCI-DSS: Use HTTPS for cardholder data transmission",
                "HIPAA: Encrypt traffic between ingress and services",
                "SOC2: Document ingress routing and security controls",
                "GDPR: Ensure data processing agreements are in place",
            ],
        },
    },
    "monitoring": {
        "cloudwatch": {
            "description": "CloudWatch monitoring integration provides comprehensive observability for AWS resources through metrics, logs, alarms, and dashboards. This pattern enables real-time monitoring, automated alerting, log aggregation, and performance analysis for cloud infrastructure and applications. CloudWatch collects metrics from AWS services automatically and allows custom metrics from applications, supports log streaming and analysis, and integrates with SNS for notifications. The pattern includes metric alarm configuration, log group setup, dashboard creation, and integration with other AWS services for end-to-end monitoring and alerting.",
            "providers": ["aws"],
            "components": ["cloudwatch", "resource"],
            "terraform_example": """
resource "aws_cloudwatch_metric_alarm" "cpu_alarm" {
  alarm_name          = "cpu-utilization"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "120"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors ec2 cpu utilization"
}
""",
            "dependencies": [
                "AWS resources generating metrics",
                "CloudWatch agent (for custom metrics)",
                "SNS topic (for alarm notifications)",
            ],
            "security_rules": [
                "Sanitize logs to remove sensitive data",
                "Encrypt CloudWatch Logs at rest",
                "Restrict access to CloudWatch dashboards",
                "Use IAM policies to control CloudWatch access",
                "Enable CloudWatch Logs encryption",
                "Implement alerting for security events",
            ],
            "monitoring_config": {
                "metrics": [
                    "Resource utilization (CPU, memory, disk)",
                    "Application performance metrics",
                    "Custom business metrics",
                    "Error rates and exceptions",
                ],
                "alarms": [
                    "High resource utilization alarms",
                    "Error rate alarms",
                    "Application performance alarms",
                    "Security event alarms",
                ],
                "logs": [
                    "Application logs",
                    "System logs",
                    "Access logs",
                    "Audit logs",
                ],
            },
            "implementation_guidance": [
                "1. Identify resources and applications to monitor",
                "2. Install CloudWatch agent for custom metrics (if needed)",
                "3. Create CloudWatch Log Groups for log aggregation",
                "4. Configure metric alarms with appropriate thresholds",
                "5. Set up SNS topics for alarm notifications",
                "6. Create CloudWatch dashboards for visualization",
                "7. Test alarms and verify notifications",
                "8. Monitor CloudWatch metrics and adjust thresholds",
            ],
            "compliance_considerations": [
                "PCI-DSS: Enable logging and monitoring for cardholder data",
                "HIPAA: Implement audit logging for PHI access",
                "SOC2: Document monitoring and alerting procedures",
                "GDPR: Ensure log retention complies with regulations",
            ],
        },
        "prometheus": {
            "description": "Prometheus monitoring integration provides open-source metrics collection, storage, and querying for Kubernetes clusters and containerized applications. This pattern enables time-series metrics collection, PromQL querying, alerting through Alertmanager, and integration with Grafana for visualization. Prometheus uses a pull-based model to scrape metrics from exporters and applications, supports service discovery in Kubernetes, and provides powerful querying capabilities. The pattern includes Prometheus server deployment, ServiceMonitor configuration, alerting rules, and integration with Grafana dashboards for comprehensive Kubernetes observability.",
            "providers": ["kubernetes"],
            "components": ["prometheus", "service"],
            "kubernetes_example": """
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: my-service-monitor
spec:
  selector:
    matchLabels:
      app: my-app
  endpoints:
  - port: metrics
    interval: 30s
""",
            "dependencies": [
                "Kubernetes cluster",
                "Prometheus operator (optional, for CRDs)",
                "Metrics exporters in applications",
            ],
            "security_rules": [
                "Sanitize metrics to remove sensitive data",
                "Encrypt Prometheus data at rest",
                "Restrict access to Prometheus UI",
                "Use RBAC for Prometheus access control",
                "Enable TLS for Prometheus communication",
                "Implement alerting for security events",
            ],
            "monitoring_config": {
                "metrics": [
                    "Application metrics (request rate, latency, errors)",
                    "Kubernetes metrics (pod, node, cluster)",
                    "Infrastructure metrics (CPU, memory, disk)",
                    "Custom business metrics",
                ],
                "alarms": [
                    "High error rate alarms",
                    "Resource utilization alarms",
                    "Application performance alarms",
                    "Security event alarms",
                ],
                "logs": [
                    "Prometheus server logs",
                    "Alertmanager logs",
                ],
            },
            "implementation_guidance": [
                "1. Deploy Prometheus server in Kubernetes cluster",
                "2. Configure ServiceMonitor resources for service discovery",
                "3. Set up metrics exporters in applications",
                "4. Configure Prometheus scrape configs",
                "5. Create alerting rules for Prometheus",
                "6. Deploy Alertmanager for alert routing",
                "7. Integrate with Grafana for visualization",
                "8. Test metrics collection and alerting",
            ],
            "compliance_considerations": [
                "PCI-DSS: Enable logging and monitoring for cardholder data",
                "HIPAA: Implement audit logging for PHI access",
                "SOC2: Document monitoring and alerting procedures",
                "GDPR: Ensure metrics retention complies with regulations",
            ],
        },
    },
}


def get_pattern(
    integration_type: str,
    pattern_name: str,
) -> dict[str, Any] | None:
    """Get integration pattern by type and name.

    Args:
        integration_type: Type of integration (networking, security, service, monitoring)
        pattern_name: Name of the pattern

    Returns:
        Pattern dictionary or None if not found
    """
    return INTEGRATION_PATTERNS.get(integration_type, {}).get(pattern_name)


def list_patterns(integration_type: str | None = None) -> dict[str, Any]:
    """List available integration patterns.

    Args:
        integration_type: Filter by integration type (optional)

    Returns:
        Dictionary of patterns
    """
    if integration_type:
        return INTEGRATION_PATTERNS.get(integration_type, {})
    return INTEGRATION_PATTERNS


def get_patterns_for_provider(cloud_provider: str) -> dict[str, Any]:
    """Get all patterns available for a cloud provider.

    Args:
        cloud_provider: Cloud provider (aws, gcp, azure, kubernetes)

    Returns:
        Dictionary of patterns filtered by provider
    """
    result: dict[str, Any] = {}
    for integration_type, patterns in INTEGRATION_PATTERNS.items():
        for pattern_name, pattern_data in patterns.items():
            providers = pattern_data.get("providers", [])
            if cloud_provider in providers or cloud_provider == "kubernetes":
                if integration_type not in result:
                    result[integration_type] = {}
                result[integration_type][pattern_name] = pattern_data
    return result

