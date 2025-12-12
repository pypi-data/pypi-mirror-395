#!/usr/bin/env python
"""
Alternative release script that updates pyproject.toml version.
Use this if you prefer static versioning over dynamic git-tag versioning.
"""

import re
import sys
from pathlib import Path
from scripts.release import get_current_version, get_next_version, run_command

def update_pyproject_version(new_version):
    """Update version in pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    
    # Replace dynamic version with static
    content = re.sub(
        r'dynamic = \["version"\]',
        f'version = "{new_version}"',
        content
    )
    
    # Remove hatch.version section if it exists
    content = re.sub(
        r'\[tool\.hatch\.version\].*?\n(?=\[|\Z)',
        '',
        content,
        flags=re.DOTALL | re.MULTILINE
    )
    
    pyproject_path.write_text(content)
    print(f"Updated pyproject.toml version to {new_version}")

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ['patch', 'minor', 'major']:
        print("Usage: python scripts/release_static.py [patch|minor|major]")
        sys.exit(1)
    
    bump_type = sys.argv[1]
    
    current_version = get_current_version()
    next_version = get_next_version(current_version, bump_type)
    
    print(f"Updating version: {current_version} → {next_version}")
    
    # Update pyproject.toml
    update_pyproject_version(next_version)
    
    # Commit the version change
    run_command("git add pyproject.toml")
    run_command(f'git commit -m "Bump version to {next_version}"')
    
    # Create and push tag
    run_command(f'git tag -a v{next_version} -m "Release v{next_version}"')
    run_command("git push origin main")
    run_command(f"git push origin v{next_version}")
    
    print(f"✅ Released v{next_version} with updated pyproject.toml")

if __name__ == "__main__":
    main()