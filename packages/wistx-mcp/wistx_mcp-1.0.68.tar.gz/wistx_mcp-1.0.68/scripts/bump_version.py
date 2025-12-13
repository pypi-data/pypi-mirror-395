#!/usr/bin/env python3
"""Bump version in pyproject.toml and api/config.py based on version type (patch, minor, major)."""

import re
import sys
from pathlib import Path


def get_current_version(pyproject_path: Path) -> str:
    """Get current version from pyproject.toml."""
    content = pyproject_path.read_text()
    match = re.search(r'^version\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
    if not match:
        raise ValueError("Could not find version in pyproject.toml")
    return match.group(1)


def get_api_version(api_config_path: Path) -> str:
    """Get current API version from api/config.py."""
    if not api_config_path.exists():
        return None
    content = api_config_path.read_text()
    match = re.search(r'api_version:\s*str\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        return None
    return match.group(1)


def bump_version(version: str, version_type: str) -> str:
    """Bump version based on type (patch, minor, major)."""
    parts = version.split(".")
    if len(parts) != 3:
        raise ValueError(f"Invalid version format: {version}. Expected format: X.Y.Z")
    
    major, minor, patch = map(int, parts)
    
    if version_type == "patch":
        patch += 1
    elif version_type == "minor":
        minor += 1
        patch = 0
    elif version_type == "major":
        major += 1
        minor = 0
        patch = 0
    else:
        raise ValueError(f"Invalid version type: {version_type}. Must be 'patch', 'minor', or 'major'")
    
    return f"{major}.{minor}.{patch}"


def update_version_in_pyproject(pyproject_path: Path, new_version: str) -> None:
    """Update version in pyproject.toml."""
    content = pyproject_path.read_text()
    updated_content = re.sub(
        r'^(version\s*=\s*["\'])([^"\']+)(["\'])',
        lambda m: m.group(1) + new_version + m.group(3),
        content,
        flags=re.MULTILINE
    )
    pyproject_path.write_text(updated_content)
    print(f"✅ Updated version in {pyproject_path} to {new_version}")


def update_version_in_api_config(api_config_path: Path, new_version: str) -> None:
    """Update API version in api/config.py."""
    if not api_config_path.exists():
        print(f"⚠️  api/config.py not found at {api_config_path}, skipping API version update")
        return
    
    content = api_config_path.read_text()
    updated_content = re.sub(
        r'(api_version:\s*str\s*=\s*["\'])([^"\']+)(["\'])',
        lambda m: m.group(1) + new_version + m.group(3),
        content,
    )
    
    if updated_content == content:
        print(f"⚠️  Could not find api_version in {api_config_path}, skipping API version update")
        return
    
    api_config_path.write_text(updated_content)
    print(f"✅ Updated API version in {api_config_path} to {new_version}")


def main():
    """Main function."""
    repo_root = Path(__file__).parent.parent
    pyproject_path = repo_root / "pyproject.toml"
    api_config_path = repo_root / "api" / "config.py"
    
    if not pyproject_path.exists():
        print(f"❌ pyproject.toml not found at {pyproject_path}")
        sys.exit(1)
    
    try:
        if len(sys.argv) == 2 and sys.argv[1] == "--get-current":
            current_version = get_current_version(pyproject_path)
            print(current_version)
            sys.exit(0)
        
        if len(sys.argv) == 2 and sys.argv[1] == "--get-api-version":
            api_version = get_api_version(api_config_path)
            if api_version:
                print(api_version)
            else:
                print("", file=sys.stderr)
                sys.exit(1)
            sys.exit(0)
        
        if len(sys.argv) != 2:
            print("Usage: python bump_version.py <patch|minor|major>")
            print("       python bump_version.py --get-current")
            print("       python bump_version.py --get-api-version")
            sys.exit(1)
        
        version_type = sys.argv[1].lower()
        if version_type not in ["patch", "minor", "major"]:
            print(f"❌ Invalid version type: {version_type}")
            print("Usage: python bump_version.py <patch|minor|major>")
            sys.exit(1)
        
        current_version = get_current_version(pyproject_path)
        print(f"📋 Current version (pyproject.toml): {current_version}")
        
        current_api_version = get_api_version(api_config_path)
        if current_api_version:
            print(f"📋 Current API version (api/config.py): {current_api_version}")
            if current_api_version != current_version:
                print(f"⚠️  Warning: API version ({current_api_version}) differs from pyproject.toml version ({current_version})")
        
        new_version = bump_version(current_version, version_type)
        print(f"🚀 New version ({version_type}): {new_version}")
        
        update_version_in_pyproject(pyproject_path, new_version)
        update_version_in_api_config(api_config_path, new_version)
        
        print(f"\n✅ Version bumped successfully!")
        print(f"   {current_version} → {new_version}")
        print(f"\n💡 Next steps:")
        print(f"   1. Review changes: git diff {pyproject_path} {api_config_path}")
        print(f"   2. Commit: git add {pyproject_path} {api_config_path} && git commit -m 'chore: bump version to {new_version}'")
        print(f"   3. Tag: git tag v{new_version}")
        print(f"   4. Push: git push && git push --tags")
        
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

