"""URL validation utilities to prevent SSRF attacks."""

import ipaddress
import logging
import socket
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

try:
    import aiodns
    AIODNS_AVAILABLE = True
except ImportError:
    AIODNS_AVAILABLE = False
    logger.warning("aiodns not available, falling back to synchronous DNS resolution")

ALLOWED_SCHEMES = {"http", "https"}
BLOCKED_HOSTNAMES = {"localhost", "127.0.0.1", "0.0.0.0", "::1", "0:0:0:0:0:0:0:1"}

SENSITIVE_PATH_PATTERNS = [
    "/etc/passwd",
    "/etc/shadow",
    "/.env",
    "/.git",
    "/admin",
    "/.aws/credentials",
    "/.ssh/id_rsa",
    "/.ssh/id_ed25519",
    "/proc/self/environ",
    "/proc/self/cmdline",
    "/windows/system32",
    "/windows/syswow64",
]


async def validate_url(
    url: str,
    allowed_schemes: set[str] | None = None,
    block_private: bool = True,
    block_localhost: bool = True,
) -> str:
    """Validate URL to prevent SSRF attacks.

    Args:
        url: URL to validate
        allowed_schemes: Set of allowed URL schemes (default: http, https)
        block_private: Block private IP addresses
        block_localhost: Block localhost variations

    Returns:
        Validated URL

    Raises:
        ValueError: If URL is invalid or blocked
    """
    if allowed_schemes is None:
        allowed_schemes = ALLOWED_SCHEMES

    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")

    url = url.strip()

    parsed = urlparse(url)

    if not parsed.scheme:
        raise ValueError(f"URL must include a scheme. Allowed schemes: {allowed_schemes}")

    if parsed.scheme.lower() not in allowed_schemes:
        raise ValueError(f"Invalid URL scheme: {parsed.scheme}. Allowed schemes: {allowed_schemes}")

    if not parsed.hostname:
        raise ValueError("URL must include a hostname")

    hostname = parsed.hostname.lower()

    if block_localhost and hostname in BLOCKED_HOSTNAMES:
        raise ValueError(f"Localhost URLs are not allowed: {hostname}")

    if block_private:
        try:
            ip = ipaddress.ip_address(hostname)

            if ip.is_private:
                raise ValueError(f"Private IP addresses are not allowed: {hostname}")

            if ip.is_loopback:
                raise ValueError(f"Loopback addresses are not allowed: {hostname}")

            if ip.is_link_local:
                raise ValueError(f"Link-local addresses are not allowed: {hostname}")

            if ip.is_reserved:
                raise ValueError(f"Reserved IP addresses are not allowed: {hostname}")
        except ValueError:
            pass

    if hostname.startswith("169.254."):
        raise ValueError("Link-local addresses (169.254.x.x) are not allowed")

    if hostname.startswith("127."):
        raise ValueError("Loopback addresses (127.x.x.x) are not allowed")

    if hostname.startswith("0."):
        raise ValueError("Invalid hostname: addresses starting with 0. are not allowed")

    _validate_url_path(parsed.path)

    if block_private or block_localhost:
        resolved_ips = []
        try:
            if AIODNS_AVAILABLE:
                resolver = aiodns.DNSResolver()
                result = await resolver.gethostbyname(hostname, socket.AF_INET)
                resolved_ips = result.addresses
            else:
                import asyncio
                loop = asyncio.get_event_loop()
                resolved_ips = await loop.run_in_executor(
                    None,
                    lambda: socket.gethostbyname_ex(hostname)[2]
                )
        except (socket.gaierror, aiodns.error.DNSError, OSError) as e:
            logger.warning("DNS resolution failed for %s: %s", hostname, e)
            raise ValueError(f"Could not resolve hostname: {hostname}") from e

        initial_ips = set(resolved_ips)

        for ip_str in resolved_ips:
            try:
                ip = ipaddress.ip_address(ip_str)

                if block_private and ip.is_private:
                    raise ValueError(
                        f"DNS rebinding detected: {hostname} resolves to private IP {ip_str}"
                    )

                if block_localhost and ip.is_loopback:
                    raise ValueError(
                        f"DNS rebinding detected: {hostname} resolves to loopback {ip_str}"
                    )

                if ip.is_link_local:
                    raise ValueError(
                        f"DNS rebinding detected: {hostname} resolves to link-local {ip_str}"
                    )

                if ip.is_reserved:
                    raise ValueError(
                        f"DNS rebinding detected: {hostname} resolves to reserved {ip_str}"
                    )
            except ValueError as e:
                if "DNS rebinding" in str(e):
                    raise
                pass

    return url


def _validate_url_path(path: str) -> None:
    """Validate URL path to prevent directory traversal and sensitive path access.

    Args:
        path: URL path component

    Raises:
        ValueError: If path contains dangerous patterns
    """
    if not path:
        return

    path_lower = path.lower()

    if ".." in path or "%2e%2e" in path_lower or "%2E%2E" in path:
        raise ValueError("Path traversal detected in URL path: '..' sequences are not allowed")

    if "//" in path:
        raise ValueError("Double slashes in URL path are not allowed")

    for sensitive in SENSITIVE_PATH_PATTERNS:
        if sensitive.lower() in path_lower:
            raise ValueError(f"Access to sensitive path blocked: {sensitive}")

    if len(path) > 2048:
        raise ValueError(f"URL path too long: {len(path)} characters (max: 2048)")


async def revalidate_url_before_request(
    url: str,
    initial_ips: set[str] | None = None,
    block_private: bool = True,
    block_localhost: bool = True,
) -> None:
    """Re-validate URL DNS resolution before making request to prevent DNS rebinding.
    
    Args:
        url: URL to re-validate
        initial_ips: Set of IPs from initial validation (if available)
        block_private: Block private IP addresses
        block_localhost: Block localhost variations
    
    Raises:
        ValueError: If DNS rebinding is detected
    """
    parsed = urlparse(url)
    hostname = parsed.hostname
    
    if not hostname:
        return
    
    try:
        if AIODNS_AVAILABLE:
            resolver = aiodns.DNSResolver()
            result = await resolver.gethostbyname(hostname, socket.AF_INET)
            current_ips = set(result.addresses)
        else:
            import asyncio
            loop = asyncio.get_event_loop()
            resolved = await loop.run_in_executor(
                None,
                lambda: socket.gethostbyname_ex(hostname)[2]
            )
            current_ips = set(resolved)
        
        if initial_ips and current_ips != initial_ips:
            logger.warning("DNS rebinding detected: %s changed from %s to %s", hostname, initial_ips, current_ips)
            raise ValueError(f"DNS rebinding detected: {hostname} IP changed")
        
        for ip_str in current_ips:
            try:
                ip = ipaddress.ip_address(ip_str)
                
                if block_private and ip.is_private:
                    raise ValueError(f"DNS rebinding detected: {hostname} resolves to private IP {ip_str}")
                
                if block_localhost and ip.is_loopback:
                    raise ValueError(f"DNS rebinding detected: {hostname} resolves to loopback {ip_str}")
                
                if ip.is_link_local:
                    raise ValueError(f"DNS rebinding detected: {hostname} resolves to link-local {ip_str}")
                
                if ip.is_reserved:
                    raise ValueError(f"DNS rebinding detected: {hostname} resolves to reserved {ip_str}")
            except ValueError as e:
                if "DNS rebinding" in str(e):
                    raise
    except (socket.gaierror, aiodns.error.DNSError, OSError) as e:
        logger.warning("DNS re-validation failed for %s: %s", hostname, e)
        raise ValueError(f"Could not re-validate hostname: {hostname}") from e


async def validate_github_url(url: str) -> str:
    """Validate GitHub repository URL.

    Args:
        url: GitHub URL to validate

    Returns:
        Validated URL

    Raises:
        ValueError: If URL is not a valid GitHub URL
    """
    validated = await validate_url(url, allowed_schemes={"http", "https"})

    parsed = urlparse(validated)
    hostname = parsed.hostname.lower()

    if hostname not in {"github.com", "www.github.com"}:
        raise ValueError(f"Invalid GitHub URL: must be from github.com, got {hostname}")

    if not parsed.path or parsed.path == "/":
        raise ValueError("GitHub URL must include repository path (e.g., /owner/repo)")

    path_parts = [p for p in parsed.path.split("/") if p]

    if len(path_parts) < 2:
        raise ValueError("GitHub URL must include owner and repository name")

    return validated

