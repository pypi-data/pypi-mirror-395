"""Verify JWT token expiration configuration.

This script validates that token expiration is correctly configured
and provides information about token lifetime.
"""

import base64
import json
import sys
from datetime import datetime, timedelta

from api.config import settings


def decode_jwt_payload(token: str) -> dict | None:
    """Decode JWT token payload without verification.

    Args:
        token: JWT token string

    Returns:
        Decoded payload dictionary or None if invalid
    """
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None

        payload = parts[1]
        padding = len(payload) % 4
        if padding:
            payload += "=" * (4 - padding)

        decoded_bytes = base64.urlsafe_b64decode(payload)
        return json.loads(decoded_bytes)
    except Exception:
        return None


def verify_token_expiration_config():
    """Verify token expiration configuration.

    Returns:
        Dictionary with verification results
    """
    result = {
        "configured_minutes": settings.access_token_expire_minutes,
        "configured_seconds": settings.access_token_expire_minutes * 60,
        "status": "valid",
        "issues": [],
    }

    if settings.access_token_expire_minutes <= 0:
        result["status"] = "invalid"
        result["issues"].append("Token expiration must be greater than 0")

    if settings.access_token_expire_minutes > 1440:
        result["status"] = "warning"
        result["issues"].append("Token expiration exceeds 24 hours (security risk)")

    return result


def analyze_token(token: str) -> dict | None:
    """Analyze JWT token to extract expiration information.

    Args:
        token: JWT token string

    Returns:
        Dictionary with token analysis or None if invalid
    """
    payload = decode_jwt_payload(token)
    if not payload:
        return None

    exp = payload.get("exp")
    iat = payload.get("iat")

    if not exp:
        return {"error": "Token missing 'exp' claim"}

    exp_datetime = datetime.fromtimestamp(exp)
    now = datetime.now()

    lifetime_seconds = None
    if iat:
        lifetime_seconds = exp - iat
        iat_datetime = datetime.fromtimestamp(iat)

    result = {
        "expires_at": exp_datetime.isoformat(),
        "expires_at_timestamp": exp,
        "is_expired": exp_datetime < now,
        "time_until_expiration": None,
        "lifetime_seconds": lifetime_seconds,
        "lifetime_minutes": None,
        "issued_at": iat_datetime.isoformat() if iat else None,
        "user_id": payload.get("sub"),
    }

    if exp_datetime > now:
        time_until_expiration = exp_datetime - now
        result["time_until_expiration"] = str(time_until_expiration)
        result["time_until_expiration_seconds"] = int(time_until_expiration.total_seconds())

    if lifetime_seconds:
        result["lifetime_minutes"] = lifetime_seconds / 60

    return result


def main():
    """Main function."""
    print("=" * 70)
    print("JWT Token Expiration Verification")
    print("=" * 70)
    print()

    config_result = verify_token_expiration_config()
    print("Configuration:")
    print(f"  Token Expiration: {config_result['configured_minutes']} minutes")
    print(f"  Token Expiration: {config_result['configured_seconds']} seconds")
    print(f"  Status: {config_result['status'].upper()}")
    if config_result["issues"]:
        for issue in config_result["issues"]:
            print(f"  ⚠️  {issue}")
    print()

    if len(sys.argv) > 1:
        token = sys.argv[1]
        print("Token Analysis:")
        print(f"  Token: {token[:50]}...")
        print()

        analysis = analyze_token(token)
        if analysis:
            if "error" in analysis:
                print(f"  ❌ Error: {analysis['error']}")
            else:
                print("  Token Details:")
                if analysis.get("user_id"):
                    print(f"    User ID: {analysis['user_id']}")
                if analysis.get("issued_at"):
                    print(f"    Issued At: {analysis['issued_at']}")
                print(f"    Expires At: {analysis['expires_at']}")
                print(f"    Lifetime: {analysis.get('lifetime_minutes', 'N/A')} minutes")
                print(f"    Lifetime: {analysis.get('lifetime_seconds', 'N/A')} seconds")
                print()

                if analysis["is_expired"]:
                    print("  ⚠️  Token is EXPIRED")
                else:
                    print(f"  ✅ Token is valid")
                    if analysis.get("time_until_expiration"):
                        print(f"    Time until expiration: {analysis['time_until_expiration']}")
        else:
            print("  ❌ Invalid token format")
    else:
        print("Usage:")
        print("  python scripts/verify_token_expiration.py <jwt_token>")
        print()
        print("Example:")
        print("  python scripts/verify_token_expiration.py eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
        print()
        print("Note: This script decodes JWT tokens without verification.")
        print("      It only extracts expiration information for analysis.")

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()

