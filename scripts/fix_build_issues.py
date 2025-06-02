#!/usr/bin/env python
"""
Fix common build issues in the project.

This script checks and fixes common build issues in the project.
"""
import os
import sys
import subprocess
from pathlib import Path
# Get the project root directory
project_root = Path(__file__).resolve().parent.parent
def check_docker_build():
    """Check if Docker build works."""
    print("Checking Docker build...")
    result = subprocess.run(
        ["docker", "build", "-t", "crm-shop-test", "."],
        cwd=project_root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("Docker build failed:")
        print(result.stderr)
        return False
    return True
def check_requirements():
    """Check if all requirements can be installed."""
    print("Checking requirements installation...")
    # Create a temporary virtual environment
    venv_dir = project_root / ".venv-test"
    if venv_dir.exists():
        subprocess.run(["rm", "-rf", str(venv_dir)], check=False)
    subprocess.run(["python", "-m", "venv", str(venv_dir)], check=True)
    # Activate the virtual environment and install requirements
    pip = str(venv_dir / "bin" / "pip")
    result = subprocess.run(
        [pip, "install", "-r", str(project_root / "requirements.txt")],
        capture_output=True,
        text=True,
    )
    # Clean up
    subprocess.run(["rm", "-rf", str(venv_dir)], check=False)
    if result.returncode != 0:
        print("Requirements installation failed:")
        print(result.stderr)
        return False
    return True
def check_migrations():
    """Check if migrations can be applied."""
    print("Checking migrations...")
    # Set up Django environment
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm_shop.settings")
    os.environ.setdefault("DATABASE_URL", "sqlite:///test.db")
    os.environ.setdefault("SECRET_KEY", "test-secret-key")
    os.environ.setdefault("DEBUG", "True")
    # Check if migrations can be applied
    result = subprocess.run(
        ["python", "manage.py", "migrate", "--check"],
        cwd=project_root,
        capture_output=True,
        text=True,
        env=os.environ,
    )
    if result.returncode != 0:
        print("Migrations check failed:")
        print(result.stderr)
        return False
    return True
def main():
    """Run all build checks."""
    all_passed = True
    # Check Docker build
    try:
        if not check_docker_build():
            all_passed = False
    except FileNotFoundError:
        print("WARNING: Docker is not installed or not in PATH.")
        all_passed = False
    # Check requirements
    if not check_requirements():
        all_passed = False
    # Check migrations
    if not check_migrations():
        all_passed = False
    if all_passed:
        print("All build checks passed!")
        return 0
    else:
        print("Some build checks failed. Please fix the issues.")
        return 1
if __name__ == "__main__":
    sys.exit(main())