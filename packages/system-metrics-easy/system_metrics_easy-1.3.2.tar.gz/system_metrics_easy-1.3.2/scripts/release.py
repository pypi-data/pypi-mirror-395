#!/usr/bin/env python3
"""
Release script for system-metrics-easy
Helps create version tags and manage releases
"""

import subprocess
import sys
import re
from pathlib import Path


def get_current_version():
    """Get current version from pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print("❌ pyproject.toml not found")
        return None

    content = pyproject_path.read_text()
    match = re.search(r'version = "([^"]+)"', content)
    if match:
        return match.group(1)
    return None


def update_version(new_version):
    """Update version in pyproject.toml and setup.py"""
    # Update pyproject.toml
    pyproject_path = Path("pyproject.toml")
    if pyproject_path.exists():
        content = pyproject_path.read_text()
        content = re.sub(r'version = "[^"]+"', f'version = "{new_version}"', content)
        pyproject_path.write_text(content)
        print(f"✅ Updated pyproject.toml to version {new_version}")

    # Update setup.py
    setup_path = Path("setup.py")
    if setup_path.exists():
        content = setup_path.read_text()
        content = re.sub(r'version="[^"]+"', f'version="{new_version}"', content)
        setup_path.write_text(content)
        print(f"✅ Updated setup.py to version {new_version}")


def create_release(version):
    """Create a new release"""
    if not version.startswith("v"):
        version = f"v{version}"

    print(f"🚀 Creating release {version}")

    # Update version files
    clean_version = version.lstrip("v")
    update_version(clean_version)

    # Add changes
    subprocess.run(["git", "add", "pyproject.toml", "setup.py"], check=True)

    # Check if there are changes to commit
    result = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True)
    if result.returncode == 0:
        print("ℹ️  No changes to commit (version already up to date)")
    else:
        # Commit changes
        subprocess.run(
            ["git", "commit", "-m", f"chore: bump version to {clean_version}"],
            check=True,
        )
        print(f"✅ Committed version bump to {clean_version}")

    # Create tag
    subprocess.run(["git", "tag", version], check=True)

    # Get current branch
    result = subprocess.run(
        ["git", "branch", "--show-current"], capture_output=True, text=True
    )
    current_branch = result.stdout.strip()

    # Push
    subprocess.run(["git", "push", "origin", current_branch], check=True)
    subprocess.run(["git", "push", "origin", version], check=True)

    print(f"✅ Release {version} created and pushed!")
    print("📦 GitHub Actions will automatically publish to PyPI")


def main():
    if len(sys.argv) != 2 or sys.argv[1] in ["--help", "-h", "help"]:
        print("Usage: python scripts/release.py <version>")
        print("Example: python scripts/release.py 1.0.0")
        print("Example: python scripts/release.py v1.0.0")
        print("")
        print("This script will:")
        print("1. Update version in pyproject.toml and setup.py")
        print("2. Commit the changes")
        print("3. Create a git tag")
        print("4. Push to GitHub")
        print("5. Trigger GitHub Actions to publish to PyPI")
        sys.exit(
            0 if len(sys.argv) == 2 and sys.argv[1] in ["--help", "-h", "help"] else 1
        )

    version = sys.argv[1]
    create_release(version)


if __name__ == "__main__":
    main()
