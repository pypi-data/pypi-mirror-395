# Release Process for good-common

## Overview

This document explains how to create releases for the good-common library with Cython optimizations. The process is largely automated using GitHub Actions.

## Prerequisites

### 1. GitHub Repository Setup

Ensure your GitHub repository has these secrets configured:

**Settings → Secrets and variables → Actions:**

- `PYPI_API_TOKEN` - Your PyPI API token (required for production releases)
- `TEST_PYPI_API_TOKEN` - Your Test PyPI token (optional, for testing)

### 2. PyPI API Token Setup

1. Go to https://pypi.org/manage/account/token/
2. Create a new API token
3. Scope: "Entire account" or specific to "good-common" project
4. Copy the token (starts with `pypi-`)
5. Add it to GitHub secrets as `PYPI_API_TOKEN`

## Versioning Strategy

We use **semantic versioning** with git tags:

- **Patch** (1.0.1): Bug fixes, performance improvements
- **Minor** (1.1.0): New features, backward compatible
- **Major** (2.0.0): Breaking changes

Versions are automatically determined from git tags using `hatch-vcs`.

## Release Methods

### Method 1: Automated Script (Recommended)

```bash
# Navigate to good-common directory
cd libs/good-common

# Create a patch release (1.0.0 → 1.0.1)
uv python scripts/release.py patch

# Create a minor release (1.0.1 → 1.1.0)
uv python scripts/release.py minor

# Create a major release (1.1.0 → 2.0.0)
uv python scripts/release.py major

# Dry run to see what would happen
uv python scripts/release.py patch --dry-run
```

This script will:
1. ✅ Check git status is clean
2. 🧪 Run tests to ensure everything works
3. 📝 Update CHANGELOG.md (if exists)
4. 🏷️ Create and push git tag
5. 🚀 Trigger GitHub Actions CI/CD

### Method 2: Manual Process

```bash
# 1. Ensure working directory is clean
git status

# 2. Run tests locally
uv run pytest tests/good_common/utilities/test_cython_optimized.py -v

# 3. Create git tag
git tag -a v1.0.1 -m "Release v1.0.1"

# 4. Push tag to trigger CI/CD
git push origin v1.0.1
```

### Method 3: GitHub Web Interface

1. Go to your GitHub repository
2. Click "Releases" → "Create a new release"
3. Click "Choose a tag" → Type new tag (e.g., `v1.0.1`)
4. Fill in release notes
5. Click "Publish release"

## What Happens During Release

### 1. GitHub Actions Workflow Triggers

When you push a tag or create a release:

```yaml
# Triggers on:
- Git tag push (v*)
- GitHub release creation
- Manual workflow dispatch
```

### 2. Multi-Platform Builds

The CI/CD pipeline automatically:

- **Tests** on Ubuntu, macOS, Windows
- **Builds wheels** for:
  - macOS: x86_64, arm64, universal2
  - Linux: x86_64, aarch64
  - Windows: AMD64
- **Builds source distribution** with both `.pyx` and `.c` files
- **Tests** that Cython optimizations work in built wheels

### 3. Automatic PyPI Publishing

If all builds succeed:
- ✅ Uploads wheels for all platforms
- ✅ Uploads source distribution
- ✅ Makes release available on PyPI instantly

## Verifying a Release

### 1. Check GitHub Actions

Go to Actions tab and verify:
- ✅ All build jobs passed
- ✅ Publish job completed successfully
- ✅ No red X's or failures

### 2. Check PyPI

Visit https://pypi.org/project/good-common/ and verify:
- ✅ New version appears
- ✅ Multiple wheel files available
- ✅ Source distribution (.tar.gz) available

### 3. Test Installation

```bash
# Test in a clean environment
pip install good-common==1.0.1

# Verify Cython optimizations work
uv python -c "
from good_common.utilities._optimized import is_optimized
print('Optimized:', is_optimized())
"
```

## Troubleshooting

### Build Failures

**Issue**: Cython compilation fails on some platform

**Solution**:
- Check that C files are generated before building
- Verify all `.c` files are included in MANIFEST.in
- Pure Python fallback should still work

**Commands to fix**:
```bash
# Regenerate C files
uv python scripts/generate_c_files.py

# Check MANIFEST includes them
uv python -m build --sdist
tar -tf dist/*.tar.gz | grep "\.c$"
```

### PyPI Upload Failures

**Issue**: `403 Forbidden` error

**Solutions**:
- Verify `PYPI_API_TOKEN` is correct
- Check token has permission for this project
- Ensure version number hasn't been used before

### Version Issues

**Issue**: "Version already exists" error

**Problem**: You tried to release the same version twice

**Solution**:
```bash
# Delete the tag locally and remotely
git tag -d v1.0.1
git push origin :refs/tags/v1.0.1

# Create new tag with incremented version
git tag -a v1.0.2 -m "Release v1.0.2"
git push origin v1.0.2
```

## Testing Releases

### Test PyPI (Recommended before production)

```bash
# Manual dispatch to upload to Test PyPI
# Go to Actions → CI/CD Pipeline → Run workflow
```

Then test installation:
```bash
pip install -i https://test.pypi.org/simple/ good-common
```

### Local Testing

```bash
# Build locally
uv python scripts/build_and_package.py

# Install local wheel
pip install dist/good_common-*.whl

# Test
uv python -c "from good_common.utilities._optimized import is_optimized; print(is_optimized())"
```

## Release Checklist

Before releasing:

- [ ] All tests pass locally
- [ ] Cython extensions build successfully
- [ ] Performance benchmarks look reasonable
- [ ] Version number follows semantic versioning
- [ ] CHANGELOG.md updated (if applicable)
- [ ] No uncommitted changes in git

After releasing:

- [ ] GitHub Actions workflow completed successfully
- [ ] New version appears on PyPI
- [ ] Installation from PyPI works
- [ ] Cython optimizations are active in installed package
- [ ] Update any dependent projects

## Emergency Rollback

If a release has critical issues:

### 1. Yank from PyPI (hides from pip install)
```bash
pip install twine
twine check dist/*
# Login to PyPI web interface and "yank" the release
```

### 2. Create hotfix release
```bash
# Create patch with fix
git checkout main
git cherry-pick <fix-commit>
uv python scripts/release.py patch
```

## Automation Summary

This setup provides:

- 🔄 **Automated versioning** from git tags
- 🏗️ **Multi-platform wheel builds** (macOS, Linux, Windows)
- 🧪 **Comprehensive testing** before release
- 📦 **Automatic PyPI publishing** on release
- ⚡ **Cython optimizations** in all distributions
- 🛡️ **Fallback to pure Python** if compilation fails

Users get the best performance possible with zero configuration required!
