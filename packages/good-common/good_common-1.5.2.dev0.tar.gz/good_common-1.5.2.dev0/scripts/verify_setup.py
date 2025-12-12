#!/usr/bin/env python
"""
Verify that the Cython setup and release process are configured correctly.
"""

import sys
import subprocess
from pathlib import Path

def check_command(cmd, description):
    """Check if a command exists."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        success = result.returncode == 0
        return success, result.stdout.strip() if success else result.stderr.strip()
    except Exception as e:
        return False, str(e)

def check_file(path, description):
    """Check if a file exists."""
    exists = Path(path).exists()
    return exists, f"Found: {path}" if exists else f"Missing: {path}"

def check_git_setup():
    """Check git configuration."""
    checks = []
    
    # Check if we're in a git repo
    success, output = check_command("git status", "Git repository")
    checks.append(("Git repository", success, output))
    
    if success:
        # Check for remote
        success, output = check_command("git remote -v", "Git remote")
        has_origin = "origin" in output if success else False
        checks.append(("Git remote origin", has_origin, output if has_origin else "No origin remote found"))
        
        # Check current branch
        success, output = check_command("git branch --show-current", "Current branch")
        checks.append(("Current branch", success, output))
    
    return checks

def main():
    print("🔍 Verifying good-common Cython setup")
    print("=" * 50)
    
    all_checks = []
    
    # File checks
    files_to_check = [
        ("pyproject.toml", "Project configuration"),
        ("setup_hybrid.py", "Hybrid setup script"),
        ("MANIFEST.in", "Package manifest"),
        ("scripts/release.py", "Release automation script"),
        (".github/workflows/ci-cd.yml", "GitHub Actions workflow"),
        ("src/good_common/utilities/_collections_cy.pyx", "Cython collections module"),
        ("src/good_common/utilities/_functional_cy.pyx", "Cython functional module"),
        ("src/good_common/utilities/_strings_cy.pyx", "Cython strings module"),
        ("benchmark_cython.py", "Benchmark script"),
        ("build_cython.sh", "Build script"),
    ]
    
    print("\n📁 File Structure:")
    for file_path, description in files_to_check:
        exists, message = check_file(file_path, description)
        status = "✅" if exists else "❌"
        print(f"{status} {description}: {message}")
        all_checks.append((description, exists, message))
    
    # Git setup
    print("\n🔗 Git Configuration:")
    git_checks = check_git_setup()
    for description, success, message in git_checks:
        status = "✅" if success else "❌"
        print(f"{status} {description}: {message}")
        all_checks.append((description, success, message))
    
    # Dependencies
    print("\n📦 Dependencies:")
    deps_to_check = [
        ("uv --version", "UV package manager"),
        ("python -c 'import cython; print(cython.__version__)'", "Cython"),
        ("python -c 'import numpy; print(numpy.__version__)'", "NumPy"),
    ]
    
    for cmd, description in deps_to_check:
        success, output = check_command(cmd, description)
        status = "✅" if success else "❌"
        print(f"{status} {description}: {output}")
        all_checks.append((description, success, output))
    
    # Build test
    print("\n🔨 Build Test:")
    
    # Check if C files exist
    c_files = list(Path("src").glob("**/*.c"))
    if c_files:
        status = "✅"
        message = f"Found {len(c_files)} C files"
    else:
        status = "⚠️"
        message = "No C files found - run 'uv run python generate_c_files.py'"
    print(f"{status} Generated C files: {message}")
    all_checks.append(("Generated C files", bool(c_files), message))
    
    # Try to import Cython modules
    print("\n⚡ Cython Optimization Status:")
    try:
        sys.path.insert(0, 'src')
        from good_common.utilities._optimized import get_optimization_status, is_optimized
        
        status_dict = get_optimization_status()
        optimized = is_optimized()
        
        for module, available in status_dict.items():
            status = "✅" if available else "❌"
            print(f"{status} {module.title()} optimizations: {'Available' if available else 'Not available'}")
            all_checks.append((f"{module.title()} optimizations", available, "Available" if available else "Not available"))
        
        overall_status = "✅" if optimized else "❌"
        print(f"{overall_status} Overall optimization status: {'Enabled' if optimized else 'Disabled'}")
        all_checks.append(("Overall optimizations", optimized, "Enabled" if optimized else "Disabled"))
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        all_checks.append(("Cython imports", False, str(e)))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, success, _ in all_checks if success)
    total = len(all_checks)
    
    print(f"✅ Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All checks passed! Your setup is ready for release.")
        print("\nTo create a release:")
        print("  python scripts/release.py patch")
        
    else:
        print(f"\n⚠️  {total - passed} issues found. Please address them before releasing:")
        for description, success, message in all_checks:
            if not success:
                print(f"   - {description}: {message}")
        
        print("\nCommon fixes:")
        print("  - Generate C files: uv run python scripts/generate_c_files.py")
        print("  - Build extensions: uv run python setup_hybrid.py build_ext --inplace")
        print("  - Install deps: uv sync")

if __name__ == "__main__":
    main()