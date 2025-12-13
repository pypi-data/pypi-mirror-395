"""Startup validation script to check required environment variables before app starts."""

import os
import sys

REQUIRED_ENV_VARS = [
    "MONGODB_URI",
]

OPTIONAL_BUT_RECOMMENDED = [
    "GOOGLE_OAUTH_CLIENT_ID",
    "GITHUB_OAUTH_CLIENT_ID",
    "JWT_SECRET_KEY",
]


def check_environment() -> bool:
    """Check if required environment variables are set."""
    missing = []
    for var in REQUIRED_ENV_VARS:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print("ERROR: Missing required environment variables:", file=sys.stderr)
        for var in missing:
            print(f"  - {var}", file=sys.stderr)
        print("\nThese must be set before the application can start.", file=sys.stderr)
        return False
    
    missing_recommended = []
    for var in OPTIONAL_BUT_RECOMMENDED:
        if not os.getenv(var):
            missing_recommended.append(var)
    
    if missing_recommended:
        print("WARNING: Missing recommended environment variables:", file=sys.stderr)
        for var in missing_recommended:
            print(f"  - {var}", file=sys.stderr)
        print("", file=sys.stderr)
    
    print("Environment check passed. Starting application...")
    return True


if __name__ == "__main__":
    if not check_environment():
        sys.exit(1)

