"""AWS Assumed Role Credential Provider.

This module implements secure cross-account access using AWS STS AssumeRole
with External ID to prevent confused deputy attacks.

Security Features:
- Credentials exist ONLY in memory - never persisted
- External ID prevents confused deputy attacks
- Session names provide CloudTrail auditability
- Automatic credential refresh before expiry
- Explicit credential clearing after use
"""

import hashlib
import logging
import secrets
from datetime import datetime, timezone, timedelta
from typing import Any, NamedTuple

from wistx_mcp.models.cloud_discovery import CloudProvider
from wistx_mcp.tools.lib.cloud_discovery.base_provider import (
    CloudCredentialProvider,
    CloudCredentials,
)

logger = logging.getLogger(__name__)


class AWSCredentials(NamedTuple):
    """Temporary AWS credentials - NEVER persisted to disk."""
    
    access_key_id: str
    secret_access_key: str
    session_token: str
    expiration: datetime


class AWSAssumedRoleCredentialProvider(CloudCredentialProvider):
    """Secure credential provider using AWS STS AssumeRole.
    
    This is the ONLY supported authentication method for AWS discovery.
    Direct credentials (access keys) are NOT supported for security reasons.
    
    Security Architecture:
    1. Customer creates IAM role in their account with trust policy
    2. Trust policy requires External ID (prevents confused deputy)
    3. WISTX assumes role to get temporary credentials
    4. Credentials are used for discovery, then cleared
    
    Example Trust Policy for customer:
    {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"AWS": "arn:aws:iam::WISTX_ACCOUNT:root"},
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {"sts:ExternalId": "wistx-CUSTOMER_ID-RANDOM"}
            }
        }]
    }
    """
    
    # Refresh credentials 5 minutes before expiry
    REFRESH_BUFFER_MINUTES = 5
    
    # Default session duration (1 hour)
    DEFAULT_DURATION_SECONDS = 3600
    
    def __init__(self) -> None:
        """Initialize the credential provider."""
        self._credentials: AWSCredentials | None = None
        self._role_arn: str | None = None
        self._external_id: str | None = None
    
    @property
    def provider(self) -> CloudProvider:
        """Return the cloud provider."""
        return CloudProvider.AWS
    
    async def get_credentials(
        self,
        role_arn: str,
        external_id: str,
        session_name: str = "wistx-discovery",
        duration_seconds: int = DEFAULT_DURATION_SECONDS,
        **kwargs: Any,
    ) -> CloudCredentials:
        """Assume an IAM role and get temporary credentials.
        
        Args:
            role_arn: ARN of the IAM role to assume
            external_id: External ID for security (prevents confused deputy)
            session_name: Session name for CloudTrail auditing
            duration_seconds: How long credentials should be valid
            
        Returns:
            CloudCredentials containing temporary AWS credentials
            
        Raises:
            PermissionError: If role assumption fails
            ValueError: If required arguments are missing
            ImportError: If boto3 is not installed
        """
        # Validate inputs
        if not role_arn:
            raise ValueError("role_arn is required")
        if not external_id:
            raise ValueError("external_id is required for security")
        if not external_id.startswith("wistx-"):
            raise ValueError("external_id must start with 'wistx-'")
        
        # Check if we have valid cached credentials for the same role
        if (
            self._credentials is not None
            and self._role_arn == role_arn
            and self._external_id == external_id
            and not self.is_expired()
        ):
            logger.debug("Using cached credentials for role %s", role_arn)
            return CloudCredentials(
                provider=CloudProvider.AWS,
                credentials={
                    "access_key_id": self._credentials.access_key_id,
                    "secret_access_key": self._credentials.secret_access_key,
                    "session_token": self._credentials.session_token,
                },
                expires_at=self._credentials.expiration,
            )
        
        # Clear any existing credentials before getting new ones
        self.clear_credentials()
        
        try:
            import boto3
            from botocore.exceptions import ClientError
        except ImportError as e:
            raise ImportError(
                "boto3 is required for AWS discovery. Install with: pip install boto3"
            ) from e
        
        # Generate unique session name for CloudTrail
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        full_session_name = f"{session_name}-{timestamp}"[:64]  # Max 64 chars
        
        logger.info(
            "Assuming role %s with session %s",
            role_arn,
            full_session_name,
        )
        
        try:
            # Use default credentials (WISTX server's IAM role) to call STS
            sts_client = boto3.client("sts")

            response = sts_client.assume_role(
                RoleArn=role_arn,
                ExternalId=external_id,
                RoleSessionName=full_session_name,
                DurationSeconds=duration_seconds,
            )

            creds = response["Credentials"]

            # Store credentials in memory ONLY
            self._credentials = AWSCredentials(
                access_key_id=creds["AccessKeyId"],
                secret_access_key=creds["SecretAccessKey"],
                session_token=creds["SessionToken"],
                expiration=creds["Expiration"],
            )
            self._role_arn = role_arn
            self._external_id = external_id

            logger.info(
                "Successfully assumed role %s, expires at %s",
                role_arn,
                self._credentials.expiration.isoformat(),
            )

            return CloudCredentials(
                provider=CloudProvider.AWS,
                credentials={
                    "access_key_id": self._credentials.access_key_id,
                    "secret_access_key": self._credentials.secret_access_key,
                    "session_token": self._credentials.session_token,
                },
                expires_at=self._credentials.expiration,
            )

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            error_message = e.response.get("Error", {}).get("Message", str(e))

            # Clear any partial state
            self.clear_credentials()

            if error_code == "AccessDenied":
                raise PermissionError(
                    f"Access denied assuming role {role_arn}. "
                    f"Verify the trust policy includes the correct External ID. "
                    f"Error: {error_message}"
                ) from e
            elif error_code == "MalformedPolicyDocument":
                raise ValueError(
                    f"Invalid role ARN format: {role_arn}"
                ) from e
            else:
                raise PermissionError(
                    f"Failed to assume role {role_arn}: {error_code} - {error_message}"
                ) from e

        except Exception as e:
            self.clear_credentials()
            raise PermissionError(
                f"Unexpected error assuming role {role_arn}: {e}"
            ) from e

    def clear_credentials(self) -> None:
        """Clear cached credentials from memory.

        MUST be called after discovery is complete to ensure
        credentials don't persist longer than necessary.
        """
        if self._credentials is not None:
            logger.debug("Clearing cached AWS credentials")

        self._credentials = None
        self._role_arn = None
        self._external_id = None

    def is_expired(self) -> bool:
        """Check if current credentials are expired or about to expire."""
        if self._credentials is None:
            return True

        # Check if expired or will expire within buffer period
        buffer = timedelta(minutes=self.REFRESH_BUFFER_MINUTES)
        now = datetime.now(timezone.utc)

        # Handle timezone-aware vs naive datetime
        expiration = self._credentials.expiration
        if expiration.tzinfo is None:
            expiration = expiration.replace(tzinfo=timezone.utc)

        return now >= (expiration - buffer)

    @staticmethod
    def generate_external_id(customer_id: str) -> str:
        """Generate a secure External ID for a customer.

        Format: wistx-{customer_hash}-{random_suffix}

        The External ID is:
        - Unique per customer
        - Contains randomness for security
        - Prefixed with 'wistx-' for identification

        Args:
            customer_id: Unique identifier for the customer

        Returns:
            A secure External ID string
        """
        # Hash customer ID for privacy
        customer_hash = hashlib.sha256(
            customer_id.encode()
        ).hexdigest()[:12]

        # Add random suffix for additional security
        random_suffix = secrets.token_hex(8)

        return f"wistx-{customer_hash}-{random_suffix}"

    @staticmethod
    def get_trust_policy_template(
        wistx_account_id: str,
        external_id: str,
    ) -> dict[str, Any]:
        """Generate IAM trust policy template for customers.

        Args:
            wistx_account_id: WISTX AWS account ID
            external_id: The External ID for this customer

        Returns:
            IAM trust policy document
        """
        return {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": f"arn:aws:iam::{wistx_account_id}:root"
                    },
                    "Action": "sts:AssumeRole",
                    "Condition": {
                        "StringEquals": {
                            "sts:ExternalId": external_id
                        }
                    }
                }
            ]
        }

    @staticmethod
    def get_permission_policy_template() -> dict[str, Any]:
        """Generate IAM permission policy template for discovery.

        Returns a read-only policy with the minimum permissions
        needed for resource discovery.

        Returns:
            IAM permission policy document
        """
        return {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "ResourceExplorerAccess",
                    "Effect": "Allow",
                    "Action": [
                        "resource-explorer-2:Search",
                        "resource-explorer-2:GetView",
                        "resource-explorer-2:ListViews",
                    ],
                    "Resource": "*"
                },
                {
                    "Sid": "ResourceGroupsTagging",
                    "Effect": "Allow",
                    "Action": [
                        "tag:GetResources",
                        "tag:GetTagKeys",
                        "tag:GetTagValues",
                    ],
                    "Resource": "*"
                },
                {
                    "Sid": "EC2ReadOnly",
                    "Effect": "Allow",
                    "Action": [
                        "ec2:Describe*",
                    ],
                    "Resource": "*"
                },
                {
                    "Sid": "RDSReadOnly",
                    "Effect": "Allow",
                    "Action": [
                        "rds:Describe*",
                        "rds:ListTagsForResource",
                    ],
                    "Resource": "*"
                },
                {
                    "Sid": "S3ReadOnly",
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetBucketLocation",
                        "s3:GetBucketTagging",
                        "s3:ListAllMyBuckets",
                    ],
                    "Resource": "*"
                },
                {
                    "Sid": "IAMReadOnly",
                    "Effect": "Allow",
                    "Action": [
                        "iam:GetRole",
                        "iam:GetPolicy",
                        "iam:ListRoles",
                        "iam:ListPolicies",
                        "iam:ListRolePolicies",
                        "iam:ListAttachedRolePolicies",
                    ],
                    "Resource": "*"
                },
                {
                    "Sid": "LambdaReadOnly",
                    "Effect": "Allow",
                    "Action": [
                        "lambda:GetFunction",
                        "lambda:ListFunctions",
                        "lambda:ListTags",
                    ],
                    "Resource": "*"
                },
                {
                    "Sid": "ELBReadOnly",
                    "Effect": "Allow",
                    "Action": [
                        "elasticloadbalancing:Describe*",
                    ],
                    "Resource": "*"
                },
                {
                    "Sid": "CloudWatchReadOnly",
                    "Effect": "Allow",
                    "Action": [
                        "cloudwatch:DescribeAlarms",
                        "logs:DescribeLogGroups",
                    ],
                    "Resource": "*"
                },
                {
                    "Sid": "STSGetCallerIdentity",
                    "Effect": "Allow",
                    "Action": [
                        "sts:GetCallerIdentity",
                    ],
                    "Resource": "*"
                }
            ]
        }

