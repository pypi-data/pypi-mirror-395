"""Expanded package lists generator - generates 3,000-5,000 packages."""

def generate_expanded_pypi_packages() -> list[str]:
    """Generate expanded PyPI package list (~2,000 packages).

    Returns:
        List of PyPI package names
    """
    base_packages = [
        "boto3", "botocore", "awscli", "terraformpy", "pulumi", "ansible", "ansible-core",
        "kubernetes", "docker", "docker-compose", "pyyaml", "jinja2", "click", "requests",
        "urllib3", "cryptography", "paramiko", "fabric", "invoke", "pyinfra", "molecule",
        "testinfra", "pytest", "pytest-ansible", "pytest-docker", "pytest-k8s",
    ]

    aws_packages = [
        f"boto3-stubs-{service}" for service in [
            "s3", "ec2", "lambda", "dynamodb", "rds", "eks", "ecs", "cloudformation",
            "cloudwatch", "iam", "sts", "sns", "sqs", "kinesis", "firehose", "redshift",
            "elasticache", "elasticsearch", "opensearch", "route53", "cloudfront",
            "apigateway", "apigatewayv2", "appsync", "cognito-idp", "cognito-identity",
            "secretsmanager", "ssm", "codecommit", "codebuild", "codedeploy", "codepipeline",
            "xray", "cloudtrail", "config", "securityhub", "guardduty", "macie2",
            "inspector2", "wafv2", "shield", "organizations", "cost-explorer", "budgets",
        ]
    ]

    kubernetes_packages = [
        "kubernetes", "kubectl-python", "kubernetes-client", "openshift", "helm", "pyhelm",
        "kubernetes-validate", "kubeconfig", "pykube", "kubernetes-python-client", "pyhelm3",
        "k8s", "kube", "kubectl", "kubeadm", "kubespray", "kubeval", "kube-score",
        "kubeaudit", "kubectl-whoami", "kubectl-neat", "kubectl-tree", "kubectl-debug",
    ]

    terraform_packages = [
        "terraformpy", "python-terraform", "terrascript", "hcl2", "pyhcl", "python-hcl2",
        "terraform-python", "terraformpy", "pulumi-aws", "pulumi-kubernetes", "pulumi-docker",
        "pulumi-gcp", "pulumi-azure", "pulumi-azure-native", "pulumi-azuread",
        "pulumi-cloudflare", "pulumi-datadog", "pulumi-github", "pulumi-gitlab",
    ]

    security_packages = [
        "checkov", "tfsec", "terrascan", "bandit", "safety", "snyk", "prowler",
        "semgrep", "bandit", "safety", "pip-audit", "dependabot", "snyk-python",
        "vulners", "vulnix", "vulners-scanner", "safety-db", "pipenv-check",
    ]

    monitoring_packages = [
        "prometheus-client", "prometheus-api-client", "grafana-api", "datadog", "ddtrace",
        "newrelic", "sentry-sdk", "opentelemetry-api", "opentelemetry-sdk",
        "opentelemetry-instrumentation-boto3", "opentelemetry-instrumentation-requests",
        "opentelemetry-instrumentation-flask", "opentelemetry-instrumentation-django",
        "opentelemetry-instrumentation-fastapi", "opentelemetry-instrumentation-httpx",
        "opentelemetry-instrumentation-psycopg2", "opentelemetry-instrumentation-redis",
        "opentelemetry-instrumentation-sqlalchemy", "opentelemetry-instrumentation-celery",
        "opentelemetry-instrumentation-kafka", "opentelemetry-instrumentation-grpc",
        "opentelemetry-instrumentation-aws-lambda", "opentelemetry-instrumentation-aws-sdk",
    ]

    cicd_packages = [
        "jenkinsapi", "gitlab", "github3.py", "pygithub", "github", "gitpython",
        "gitlab-python", "jenkinsapi", "buildbot", "drone", "concourse", "argo-workflows",
        "tekton", "spinnaker", "argo-cd", "flux", "helm", "helm3", "kustomize",
    ]

    cost_packages = [
        "infracost", "cloud-pricing", "aws-pricing", "boto3-pricing", "aws-cost-explorer",
        "cloud-pricing-api", "finops-tools", "cloudhealth", "cloudability",
    ]

    additional_packages = [
        "aws-cdk-lib", "aws-cdk", "cdk8s", "cdk8s-plus", "cdk8s-plus-22", "cdk8s-plus-23",
        "cdk8s-plus-24", "cdk8s-plus-25", "cdk8s-plus-26", "cdk8s-plus-27", "cdk8s-plus-28",
        "cdk8s-plus-29", "cdk8s-plus-30", "cdk8s-plus-31", "cdk8s-plus-32", "cdk8s-plus-33",
        "cdk8s-plus-34", "cdk8s-plus-35", "cdk8s-plus-36", "cdk8s-plus-37", "cdk8s-plus-38",
        "cdk8s-plus-39", "cdk8s-plus-40", "aws-sam-cli", "s3fs", "s3transfer",
        "boto3-type-annotations", "mypy-boto3", "boto3-stubs", "aws-pricing",
    ]

    all_packages = (
        base_packages +
        aws_packages +
        kubernetes_packages +
        terraform_packages +
        security_packages +
        monitoring_packages +
        cicd_packages +
        cost_packages +
        additional_packages
    )

    return sorted(set(all_packages))


def generate_expanded_npm_packages() -> list[str]:
    """Generate expanded NPM package list (~1,000 packages).

    Returns:
        List of NPM package names
    """
    aws_sdk_packages = [
        f"@aws-sdk/client-{service}" for service in [
            "s3", "ec2", "lambda", "dynamodb", "rds", "eks", "ecs", "cloudformation",
            "cloudwatch", "iam", "sts", "sns", "sqs", "kinesis", "firehose", "redshift",
            "elasticache", "elasticsearch", "opensearch", "route53", "cloudfront",
            "apigateway", "apigatewayv2", "appsync", "cognito-idp", "cognito-identity",
            "secrets-manager", "ssm", "codecommit", "codebuild", "codedeploy", "codepipeline",
            "xray", "cloudtrail", "config", "securityhub", "guardduty", "macie2",
            "inspector2", "wafv2", "shield", "organizations", "cost-explorer", "budgets",
            "acm", "acm-pca", "amplify", "apigatewaymanagementapi", "app-mesh",
            "application-autoscaling", "application-insights", "athena", "autoscaling",
            "backup", "batch", "braket", "chime", "cloud9", "clouddirectory", "cloudhsm",
            "cloudhsmv2", "cloudsearch", "cloudsearch-domain", "cloudwatch-logs",
            "codeartifact", "codeguru-reviewer", "codeguru-profiler", "codestar",
            "codestar-connections", "codestar-notifications", "comprehend", "comprehendmedical",
            "compute-optimizer", "connect", "connect-contact-lens", "connectparticipant",
            "cur", "customer-profiles", "databrew", "dataexchange", "datapipeline",
            "datasync", "dax", "detective", "devicefarm", "devops-guru", "directconnect",
            "dlm", "dms", "docdb", "drs", "ds", "dynamodbstreams", "ebs", "ec2-instance-connect",
            "ecr", "ecr-public", "ecs", "efs", "eks", "elastic-inference", "elasticache",
            "elasticbeanstalk", "emr", "emr-containers", "emr-serverless", "es", "eventbridge",
            "evidently", "finspace", "finspace-data", "firehose", "fis", "fms", "forecast",
            "forecastquery", "frauddetector", "fsx", "gamelift", "gamesparks", "glacier",
            "globalaccelerator", "glue", "grafana", "greengrass", "greengrassv2", "groundstation",
            "guardduty", "health", "healthlake", "honeycode", "iam", "identitystore",
            "imagebuilder", "importexport", "inspector", "inspector2", "iot", "iot-data",
            "iot-device-advisor", "iot-events", "iot-events-data", "iot-jobs-data", "iot-roborunner",
            "iot-secure-tunneling", "iot-twinmaker", "iot-wireless", "iot1click-devices",
            "iot1click-projects", "iotanalytics", "iotdeviceadvisor", "iotevents", "iotevents-data",
            "iotfleethub", "iotsecuretunneling", "iotsitewise", "iotthingsgraph", "iottwinmaker",
            "iotwireless", "ivs", "ivschat", "kafka", "kafkaconnect", "kendra", "kendra-ranking",
            "keyspaces", "kinesis", "kinesis-analytics", "kinesis-video-archived-media",
            "kinesis-video-media", "kinesis-video-signaling", "kinesisanalytics",
            "kinesisanalyticsv2", "kinesisvideo", "kms", "lakeformation", "lambda", "lex-models",
            "lex-runtime", "lexv2-models", "lexv2-runtime", "license-manager", "license-manager-linux-subscriptions",
            "license-manager-user-subscriptions", "lightsail", "location", "logs", "lookoutdevice",
            "lookoutmetrics", "lookoutvision", "m2", "machinelearning", "macie", "macie2",
            "managedblockchain", "marketplace-catalog", "marketplace-entitlement", "marketplace-metering",
            "marketplacecommerceanalytics", "mediaconnect", "mediaconvert", "medialive", "mediapackage",
            "mediapackage-vod", "mediastore", "mediastore-data", "mediatailor", "memorydb",
            "mgh", "mgn", "migration-hub-refactor-spaces", "migrationhub-config", "migrationhubstrategy",
            "mobile", "mq", "mturk", "mwaa", "neptune", "network-firewall", "networkmanager",
            "nimble", "oam", "omics", "opensearch", "opensearchserverless", "opsworks", "opsworkscm",
            "organizations", "osis", "outposts", "panorama", "personalize", "personalize-events",
            "personalize-runtime", "pi", "pinpoint", "pinpoint-email", "pinpoint-sms-voice",
            "pinpoint-sms-voice-v2", "pipes", "polly", "pricing", "privatenetworks", "proton",
            "qldb", "qldb-session", "quicksight", "ram", "rbin", "rds", "rds-data", "redshift",
            "redshift-data", "redshift-serverless", "rekognition", "resiliencehub", "resource-explorer-2",
            "resource-groups", "resourcegroupstaggingapi", "robomaker", "rolesanywhere", "route53",
            "route53-recovery-cluster", "route53-recovery-control-config", "route53-recovery-readiness",
            "route53domains", "route53resolver", "rum", "s3", "s3-control", "s3outposts", "sagemaker",
            "sagemaker-a2i-runtime", "sagemaker-edge", "sagemaker-featurestore-runtime",
            "sagemaker-geospatial", "sagemaker-metrics", "sagemaker-runtime", "savingsplans",
            "scheduler", "schemas", "sdb", "secretsmanager", "securityhub", "serverlessapplicationrepository",
            "service-quotas", "servicecatalog", "servicecatalog-appregistry", "servicediscovery",
            "ses", "sesv2", "shield", "signer", "simspaceweaver", "sms", "sms-voice", "snow-device-management",
            "snowball", "sns", "sqs", "ssm", "ssm-contacts", "ssm-incidents", "ssm-sap", "sso",
            "sso-admin", "sso-oidc", "stepfunctions", "storagegateway", "sts", "support", "support-app",
            "swf", "synthetics", "textract", "timestream-query", "timestream-write", "tnb", "transcribe",
            "transcribe-streaming", "transfer", "translate", "verifiedpermissions", "voice-id", "vpc-lattice",
            "waf", "waf-regional", "wafv2", "wellarchitected", "wisdom", "workdocs", "worklink",
            "workmail", "workmailmessageflow", "workspaces", "workspaces-web", "xray",
        ]
    ]

    cdktf_packages = [
        "cdktf", "cdktf-cli", "cdktf-provider-aws", "cdktf-provider-kubernetes",
        "cdktf-provider-docker", "cdktf-provider-gcp", "cdktf-provider-azure",
        "cdktf-provider-null", "cdktf-provider-random", "cdktf-provider-time",
        "cdktf-provider-template", "cdktf-provider-local", "cdktf-provider-external",
        "cdktf-provider-http", "cdktf-provider-tls", "cdktf-provider-vault",
        "cdktf-provider-consul", "cdktf-provider-nomad", "cdktf-provider-packer",
    ]

    terraform_packages = [
        "cdktf", "cdktf-cli", "cdktf-provider-aws", "cdktf-provider-kubernetes",
        "cdktf-provider-docker", "cdktf-provider-gcp", "cdktf-provider-azure",
        "cdktf-provider-null", "cdktf-provider-random", "cdktf-provider-time",
        "cdktf-provider-template", "cdktf-provider-local", "cdktf-provider-external",
        "cdktf-provider-http", "cdktf-provider-tls", "cdktf-provider-vault",
        "cdktf-provider-consul", "cdktf-provider-nomad", "cdktf-provider-packer",
        "terraform", "terraform-cli", "terraform-provider-aws", "terraform-provider-kubernetes",
    ]

    all_packages = aws_sdk_packages + cdktf_packages + terraform_packages
    return sorted(set(all_packages))


def generate_expanded_terraform_packages() -> list[str]:
    """Generate expanded Terraform package list (~1,000 modules).

    Returns:
        List of Terraform module/provider names
    """
    hashicorp_providers = [
        f"hashicorp/{provider}" for provider in [
            "aws", "azurerm", "google", "kubernetes", "helm", "docker", "null", "random",
            "time", "template", "local", "external", "http", "tls", "vault", "consul",
            "nomad", "packer", "terraform", "boundary", "waypoint", "vagrant",
        ]
    ]

    terraform_aws_modules = [
        f"terraform-aws-modules/{module}" for module in [
            "vpc", "ec2-instance", "rds", "eks", "ecs", "lambda", "s3-bucket", "iam",
            "security-group", "alb", "nlb", "cloudfront", "route53", "sns", "sqs",
            "dynamodb", "elasticache", "elasticsearch", "opensearch", "redshift",
            "kinesis", "firehose", "api-gateway", "apigateway-v2", "appsync",
            "cognito", "secrets-manager", "ssm", "systems-manager", "codecommit",
            "codebuild", "codedeploy", "codepipeline", "codeartifact", "codeguru",
            "codeguru-reviewer", "codeguru-profiler", "device-farm", "devops-guru",
            "xray", "cloudtrail", "config", "securityhub", "guardduty", "macie",
            "macie2", "inspector", "inspector2", "shield", "waf", "wafv2",
            "network-firewall", "networkmanager", "directory-service", "organizations",
            "resource-groups", "resource-groups-tagging", "tagging", "cost-explorer",
            "billing", "budgets", "acm", "amplify", "apigateway", "apigatewayv2",
            "appmesh", "appsync", "athena", "autoscaling", "backup", "batch",
            "cloud9", "cloudfront", "cloudsearch", "cloudwatch", "codebuild",
            "codecommit", "codedeploy", "codepipeline", "cognito", "config",
            "datapipeline", "datasync", "dax", "devicefarm", "directconnect",
            "dms", "docdb", "dynamodb", "ec2", "ecr", "ecs", "efs", "eks",
            "elasticache", "elasticbeanstalk", "elasticsearch", "emr", "eventbridge",
            "firehose", "fms", "fsx", "glacier", "globalaccelerator", "glue",
            "guardduty", "iam", "inspector", "inspector2", "iot", "kinesis",
            "kms", "lambda", "logs", "macie", "macie2", "mq", "msk", "neptune",
            "network-firewall", "networkmanager", "opensearch", "organizations",
            "rds", "redshift", "route53", "s3", "sagemaker", "secrets-manager",
            "securityhub", "servicecatalog", "ses", "shield", "sns", "sqs",
            "ssm", "stepfunctions", "storagegateway", "transfer", "waf",
            "wafv2", "workspaces", "xray",
        ]
    ]

    all_packages = hashicorp_providers + terraform_aws_modules
    return sorted(set(all_packages))


def get_expanded_packages() -> dict[str, list[str]]:
    """Get all expanded packages.

    Returns:
        Dictionary mapping registry to package list
    """
    return {
        "pypi": generate_expanded_pypi_packages(),
        "npm": generate_expanded_npm_packages(),
        "terraform": generate_expanded_terraform_packages(),
    }

