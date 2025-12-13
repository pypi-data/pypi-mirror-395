"""Credential providers for cloud discovery.

This package contains provider-specific credential implementations.
"""

from wistx_mcp.tools.lib.cloud_discovery.credential_providers.aws_assumed_role import (
    AWSAssumedRoleCredentialProvider,
    AWSCredentials,
)

__all__ = [
    "AWSAssumedRoleCredentialProvider",
    "AWSCredentials",
]

