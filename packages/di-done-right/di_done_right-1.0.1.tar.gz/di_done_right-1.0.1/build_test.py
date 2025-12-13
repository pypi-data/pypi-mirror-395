#!/usr/bin/env python3
"""
Quick build test script for the di-done-right package.
Run this before publishing to PyPI.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"\n🔍 {description}")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ Success: {description}")
        if result.stdout.strip():
            print(f"Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {description}")
        print(f"Error: {e.stderr.strip()}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        return False


def main():
    """Run pre-publish checks."""
    print("🚀 Pre-publish checks for di-done-right")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ pyproject.toml not found. Run this from the project root.")
        return False
    
    # Check if required files exist
    required_files = [
        "di_container/__init__.py",
        "LICENSE",
        "README.md",
        "MANIFEST.in"
    ]
    
    print("\n📁 Checking required files:")
    all_files_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_files_exist = False
    
    if not all_files_exist:
        return False
    
    # Clean previous builds
    if Path("dist").exists():
        print("\n🧹 Cleaning previous builds...")
        import shutil
        shutil.rmtree("dist")
    
    # Run checks
    checks = [
        (["python", "-c", "import di_container; print('Package imports successfully')"], 
         "Import test"),
        (["python", "-m", "pytest", "tests/", "-v"], 
         "Test suite"),
        (["python", "-m", "build"], 
         "Build package"),
        (["python", "-c", "import twine"], 
         "Check twine availability"),
    ]
    
    success_count = 0
    for cmd, description in checks:
        if run_command(cmd, description):
            success_count += 1
    
    # Final summary
    print(f"\n📊 Results: {success_count}/{len(checks)} checks passed")
    
    if success_count == len(checks):
        print("\n🎉 All checks passed! Your package is ready for PyPI.")
        print("\nNext steps:")
        print("1. Update author info in pyproject.toml")
        print("2. Create PyPI account and get API token")
        print("3. Run: twine upload dist/*")
        return True
    else:
        print("\n⚠️  Some checks failed. Please fix issues before publishing.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
