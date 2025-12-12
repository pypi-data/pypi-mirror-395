"""Tests for cookie utilities."""

import pytest
from fastapi import Response

from api.utils.cookies import (
    set_auth_cookie,
    clear_auth_cookie,
    get_auth_token_from_cookie,
    validate_token_size,
    MAX_TOKEN_SIZE,
    COOKIE_NAME,
)


def test_set_auth_cookie():
    """Test setting authentication cookie."""
    response = Response()
    token = "test-token-123"
    
    set_auth_cookie(response, token)
    
    set_cookie_header = response.headers.get("set-cookie", "")
    assert COOKIE_NAME in set_cookie_header
    assert token in set_cookie_header
    assert "HttpOnly" in set_cookie_header
    assert "SameSite=Strict" in set_cookie_header


def test_set_auth_cookie_with_domain():
    """Test setting cookie with domain."""
    response = Response()
    token = "test-token-123"
    
    set_auth_cookie(response, token, domain=".example.com")
    
    set_cookie_header = response.headers.get("set-cookie", "")
    assert "Domain=.example.com" in set_cookie_header


def test_clear_auth_cookie():
    """Test clearing authentication cookie."""
    response = Response()
    
    clear_auth_cookie(response)
    
    set_cookie_header = response.headers.get("set-cookie", "")
    assert COOKIE_NAME in set_cookie_header
    assert "Max-Age=0" in set_cookie_header


def test_validate_token_size_valid():
    """Test token size validation with valid token."""
    token = "a" * 1000
    validate_token_size(token)


def test_validate_token_size_too_large():
    """Test token size validation with oversized token."""
    token = "a" * (MAX_TOKEN_SIZE + 1)
    
    with pytest.raises(ValueError, match="exceeds cookie limit"):
        validate_token_size(token)


def test_get_auth_token_from_cookie():
    """Test getting token from cookie."""
    from unittest.mock import Mock
    
    request = Mock()
    request.cookies = {"auth_token": "test-token-123"}
    
    token = get_auth_token_from_cookie(request)
    assert token == "test-token-123"


def test_get_auth_token_from_cookie_missing():
    """Test getting token when cookie is missing."""
    from unittest.mock import Mock
    
    request = Mock()
    request.cookies = {}
    
    token = get_auth_token_from_cookie(request)
    assert token is None

