"""Pytest configuration and fixtures for wistx_mcp tests."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from typing import Any

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient


@pytest.fixture
def mock_mongodb_client():
    """Mock MongoDB client."""
    client = MagicMock(spec=MongoDBClient)
    client.connect = AsyncMock(return_value=None)
    client.close = AsyncMock(return_value=None)
    return client


@pytest.fixture
def mock_vector_search():
    """Mock vector search."""
    search = MagicMock()
    search.search_knowledge_articles = AsyncMock(return_value=[])
    search.search_code_examples = AsyncMock(return_value=[])
    return search


@pytest.fixture
def mock_web_search_client():
    """Mock web search client."""
    client = MagicMock()
    client.search_devops = AsyncMock(return_value={"results": [], "answer": ""})
    client.search_by_domain = AsyncMock(return_value={"results": [], "answer": ""})
    client.close = AsyncMock(return_value=None)
    return client


@pytest.fixture
def mock_security_client():
    """Mock security client."""
    client = MagicMock()
    client.search_cves = AsyncMock(return_value=[])
    client.search_advisories = AsyncMock(return_value=[])
    client.search_kubernetes_security = AsyncMock(return_value=[])
    client.close = AsyncMock(return_value=None)
    return client


@pytest.fixture
def mock_api_client():
    """Mock API client."""
    client = MagicMock()
    client.get_compliance_requirements = AsyncMock(return_value={"controls": []})
    client.get_current_user = AsyncMock(return_value={"user_id": "test-user"})
    return client


@pytest.fixture
def sample_infrastructure_code():
    """Sample infrastructure code for testing."""
    return """
resource "aws_instance" "web" {
  ami           = "ami-12345678"
  instance_type = "t3.medium"
}

resource "aws_security_group" "web" {
  name = "web-sg"
}
"""


@pytest.fixture
def sample_kubernetes_manifest():
    """Sample Kubernetes manifest for testing."""
    return """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: nginx:latest
"""

