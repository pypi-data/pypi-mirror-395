#!/usr/bin/env python
"""
Automated release script for good-common.
This script helps create releases with proper versioning.
"""

import sys
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, check=True, capture_output=True):
    """Run a shell command."""
    print(f"Running: {cmd}")
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=capture_output,
        text=True,
        cwd=Path(__file__).parent.parent
    )
    if check and result.returncode != 0:
        print(f"Error: Command failed with exit code {result.returncode}")
        if result.stderr:
            print(f"stderr: {result.stderr}")
        sys.exit(1)
    return result

def get_current_version():
    """Get the current version from git tags."""
    try:
        result = run_command("git describe --tags --abbrev=0")
        return result.stdout.strip().lstrip('v')
    except Exception:
        return "0.3.5"

def get_next_version(current_version, bump_type):
    """Calculate the next version based on bump type."""
    parts = current_version.split('.')
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    if bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    elif bump_type == 'patch':
        patch += 1

    return f"{major}.{minor}.{patch}"

def create_changelog_entry(version, changes):
    """Add entry to CHANGELOG.md if it exists."""
    changelog_path = Path("CHANGELOG.md")
    if not changelog_path.exists():
        return

    import datetime
    today = datetime.date.today().strftime("%Y-%m-%d")

    new_entry = f"""
## [{version}] - {today}

### Added
- Performance optimizations with Cython
- Automated CI/CD pipeline

### Changed
- Improved build system with wheel distribution

### Fixed
- Various bug fixes and performance improvements

"""

    # Read existing content
    content = changelog_path.read_text()

    # Insert new entry after the header
    lines = content.split('\n')
    header_end = 0
    for i, line in enumerate(lines):
        if line.startswith('## ['):
            header_end = i
            break

    lines.insert(header_end, new_entry.strip())
    changelog_path.write_text('\n'.join(lines))

def main():
    parser = argparse.ArgumentParser(description='Create a new release')
    parser.add_argument(
        'bump_type',
        choices=['patch', 'minor', 'major'],
        help='Type of version bump'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without actually doing it'
    )
    parser.add_argument(
        '--skip-tests',
        action='store_true',
        help='Skip running tests before release'
    )
    parser.add_argument(
        '--yes', '-y',
        action='store_true',
        help='Skip confirmation prompt'
    )

    args = parser.parse_args()

    print("🚀 Starting release process...")
    print("="*50)

    # Check we're in the right directory
    if not Path("pyproject.toml").exists():
        print("Error: Must run from the good-common directory")
        sys.exit(1)

    # Check git status
    result = run_command("git status --porcelain")
    if result.stdout.strip() and not args.dry_run:
        print("Error: Working directory is not clean. Commit your changes first.")
        sys.exit(1)

    # Get current and next version
    current_version = get_current_version()
    next_version = get_next_version(current_version, args.bump_type)

    print(f"Current version: {current_version}")
    print(f"Next version: {next_version}")
    print(f"Bump type: {args.bump_type}")

    if args.dry_run:
        print("\n🔍 DRY RUN - No changes will be made")
        return

    # Confirm with user
    if not args.yes:
        confirm = input(f"\nCreate release v{next_version}? (y/N): ")
        if confirm.lower() != 'y':
            print("Release cancelled.")
            return
    else:
        print(f"\n✅ Auto-confirming release v{next_version}")

    # Run tests unless skipped
    if not args.skip_tests:
        print("\n📋 Running tests...")
        run_command("uv sync", capture_output=False)
        run_command("uv run python scripts/generate_c_files.py", capture_output=False)
        run_command("uv run python setup_hybrid.py build_ext --inplace", capture_output=False)
        run_command("uv run pytest tests/good_common/utilities/test_cython_optimized.py", capture_output=False)

    # Create changelog entry (optional)
    print("\n📝 Updating changelog...")
    create_changelog_entry(next_version, "Automated release")

    # Commit any changes
    run_command("git add -A")
    run_command(f'git commit -m "Prepare release v{next_version}"', check=False)

    # Create and push tag
    print(f"\n🏷️  Creating git tag v{next_version}...")
    run_command(f'git tag -a v{next_version} -m "Release v{next_version}"')

    print("\n📤 Pushing to remote...")
    run_command("git push origin main")
    run_command(f"git push origin v{next_version}")

    print(f"""
    ✅ Release v{next_version} created successfully!

    Next steps:
    1. Go to GitHub and create a release from the tag v{next_version}
    2. The CI/CD pipeline will automatically build and publish to PyPI
    3. Monitor the GitHub Actions for any issues

    GitHub Release URL:
    https://github.com/goodkiwillc/good-common/releases/new?tag=v{next_version}
    """)

if __name__ == "__main__":
    main()
