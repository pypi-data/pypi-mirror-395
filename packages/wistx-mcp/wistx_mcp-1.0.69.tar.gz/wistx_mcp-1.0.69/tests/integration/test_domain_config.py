"""Integration tests for domain configuration."""

import pytest
from api.utils.domain_config import (
    get_cookie_domain,
    should_use_subdomain_cookies,
    get_frontend_domain,
    get_backend_domain,
)


def test_get_cookie_domain_development():
    """Test cookie domain in development (should be None)."""
    from api.config import settings
    
    original_debug = settings.debug
    try:
        settings.debug = True
        domain = get_cookie_domain()
        assert domain is None
    finally:
        settings.debug = original_debug


def test_get_frontend_domain():
    """Test getting frontend domain."""
    domain = get_frontend_domain()
    assert isinstance(domain, str)
    assert len(domain) > 0


def test_get_backend_domain():
    """Test getting backend domain."""
    domain = get_backend_domain()
    assert isinstance(domain, str)
    assert len(domain) > 0


def test_should_use_subdomain_cookies():
    """Test subdomain cookie detection."""
    result = should_use_subdomain_cookies()
    assert isinstance(result, bool)

