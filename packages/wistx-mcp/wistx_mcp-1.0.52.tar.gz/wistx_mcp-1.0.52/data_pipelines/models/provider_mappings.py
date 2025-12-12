"""Provider-specific to FOCUS mapping models."""

from typing import Any
import re

from pydantic import BaseModel, Field


class ProviderMapping(BaseModel):
    """Maps provider-specific data to FOCUS standard."""

    provider: str = Field(..., description="Cloud provider")
    provider_service_name: str = Field(..., description="Provider-specific service name")
    provider_resource_type: str = Field(..., description="Provider-specific resource type")
    provider_sku: str = Field(..., description="Provider-specific SKU")

    focus_service_category: str = Field(..., description="FOCUS service category")
    focus_service_name: str = Field(..., description="FOCUS service name")
    focus_service_subcategory: str | None = Field(default=None, description="FOCUS service subcategory")
    focus_resource_type: str = Field(..., description="FOCUS resource type")
    focus_pricing_category: str = Field(..., description="FOCUS pricing category")

    normalized_specs: dict[str, Any] = Field(default_factory=dict, description="Normalized specifications")


class ServiceCategoryMapper:
    """Maps provider services to FOCUS service categories using heuristics and fallback mapping.
    
    This uses pattern matching on service names/descriptions rather than maintaining
    a hardcoded list of all services. This approach:
    1. Scales automatically as providers add new services
    2. Reduces maintenance burden
    3. Uses a small curated mapping only for ambiguous cases
    """

    SERVICE_CATEGORY_PATTERNS = {
        "Compute": [
            r"compute|ec2|lambda|function|container|kubernetes|k8s|vm|virtual.?machine|instance|server|fargate|batch|beanstalk|lightsail|app.?stream|workspace|game",
            r"^ec2|^lambda|^ecs|^eks|^fargate|^batch|^lightsail",
        ],
        "Storage": [
            r"storage|s3|ebs|efs|fsx|glacier|disk|volume|filestore|blob|bucket|object.?storage|archive|backup",
            r"^s3|^ebs|^efs|^fsx|^glacier|^storage",
        ],
        "Database": [
            r"database|db|rds|dynamodb|aurora|redshift|cosmos|spanner|bigtable|firestore|datastore|sql|mysql|postgres|mongo|redis|cache|nosql|timestream|documentdb|neptune",
            r"^rds|^dynamodb|^aurora|^redshift|^cosmos|^spanner|^bigtable|^firestore|^datastore",
        ],
        "Network": [
            r"network|vpc|vnet|cdn|dns|route53|load.?balancer|gateway|vpn|nat|firewall|waf|front.?door|traffic.?manager|expressroute|directconnect|interconnect|private.?link|transit",
            r"^vpc|^cdn|^dns|^route53|^cloudfront|^apigateway|^alb|^nlb|^elb",
        ],
        "Analytics": [
            r"analytics|athena|kinesis|emr|quicksight|dataflow|dataproc|databricks|synapse|stream.?analytics|hdinsight|bigquery|data.?factory|data.?lake|event.?hub|pub.?sub",
            r"^athena|^kinesis|^emr|^quicksight|^dataflow|^dataproc|^bigquery",
        ],
        "Security": [
            r"security|iam|kms|vault|secrets|guard|waf|shield|macie|inspector|cognito|defender|sentinel|key.?vault|certificate|identity|access.?control|policy|compliance",
            r"^iam|^kms|^secrets|^guard|^waf|^shield|^macie|^inspector|^cognito",
        ],
        "Management": [
            r"monitor|logging|cloudwatch|cloudtrail|config|advisor|backup|migrate|automation|resource.?manager|cost.?management|billing|tag|organizations|control.?tower",
            r"^cloudwatch|^cloudtrail|^config|^advisor|^backup|^monitor|^logging",
        ],
        "Integration": [
            r"integration|api.?gateway|event.?bridge|event.?grid|service.?bus|sns|sqs|ses|mq|logic.?apps|workflow|step.?functions|appsync|connect|chime|pinpoint",
            r"^apigateway|^eventbridge|^eventgrid|^servicebus|^sns|^sqs|^ses|^mq|^appsync",
        ],
        "AI/ML": [
            r"ai|ml|machine.?learning|sagemaker|rekognition|comprehend|translate|polly|transcribe|textract|lex|personalize|forecast|kendra|bedrock|cognitive|vision|speech|translator|openai",
            r"^sagemaker|^rekognition|^comprehend|^translate|^polly|^transcribe|^textract|^lex|^bedrock",
        ],
        "DevOps": [
            r"devops|ci.?cd|pipeline|codecommit|codebuild|codedeploy|codepipeline|artifact|registry|ecr|container.?registry|build|deploy|proton|amplify",
            r"^codecommit|^codebuild|^codedeploy|^codepipeline|^ecr|^artifact",
        ],
    }

    SERVICE_CATEGORY_MAP = {
        "aws": {
            "AmazonEC2": "Compute",
            "AWSLambda": "Compute",
            "AmazonS3": "Storage",
            "AmazonRDS": "Database",
            "AmazonVPC": "Network",
            "AmazonCloudFront": "Network",
            "AmazonRoute53": "Network",
            "AmazonGuardDuty": "Security",
            "AWSCloudWatch": "Management",
            "AmazonSNS": "Integration",
            "AmazonSageMaker": "AI/ML",
            "AmazonCodeCommit": "DevOps",
        },
        "gcp": {
            "Compute Engine": "Compute",
            "Cloud Functions": "Compute",
            "Cloud Storage": "Storage",
            "Cloud SQL": "Database",
            "BigQuery": "Analytics",
            "Cloud Load Balancing": "Network",
            "Cloud IAM": "Security",
            "Cloud Monitoring": "Management",
            "Cloud Pub/Sub": "Integration",
            "Cloud AI Platform": "AI/ML",
            "Cloud Build": "DevOps",
        },
        "azure": {
            "Virtual Machines": "Compute",
            "Azure Functions": "Compute",
            "Storage": "Storage",
            "SQL Database": "Database",
            "Azure Synapse Analytics": "Analytics",
            "Load Balancer": "Network",
            "Azure Key Vault": "Security",
            "Monitor": "Management",
            "Azure Service Bus": "Integration",
            "Azure Machine Learning": "AI/ML",
            "Azure DevOps": "DevOps",
        },
        "oracle": {
            "Compute": "Compute",
            "Object Storage": "Storage",
            "Autonomous Database": "Database",
            "Load Balancer": "Network",
            "Vault": "Security",
            "Monitoring": "Management",
            "Streaming": "Analytics",
            "API Gateway": "Integration",
            "Data Science": "AI/ML",
        },
        "alibaba": {
            "ECS": "Compute",
            "OSS": "Storage",
            "RDS": "Database",
            "SLB": "Network",
            "WAF": "Security",
            "CloudMonitor": "Management",
            "MaxCompute": "Analytics",
            "Message Queue": "Integration",
            "Machine Learning Platform": "AI/ML",
        },
    }

    @classmethod
    def get_service_category(cls, provider: str, service_name: str, service_description: str | None = None) -> str:
        """Get FOCUS service category for provider service using heuristics.
        
        Args:
            provider: Cloud provider (aws/gcp/azure/oracle/alibaba)
            service_name: Provider-specific service name
            service_description: Optional service description for better matching
            
        Returns:
            FOCUS service category (defaults to "Compute" if no match found)
        """
        service_lower = service_name.lower()
        search_text = service_lower
        if service_description:
            search_text += " " + service_description.lower()
        
        provider_map = cls.SERVICE_CATEGORY_MAP.get(provider.lower(), {})
        
        if service_name in provider_map:
            return provider_map[service_name]
        
        category_scores = {}
        for category, patterns in cls.SERVICE_CATEGORY_PATTERNS.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, search_text, re.IGNORECASE))
                score += matches
            if score > 0:
                category_scores[category] = score
        
        if category_scores:
            return max(category_scores.items(), key=lambda x: x[1])[0]
        
        return "Compute"
