#!/usr/bin/env python
"""
Fix common build issues in the project.
"""
import os
import subprocess  # nosec B404
import sys
from pathlib import Path
import shutil

project_root = Path(__file__).resolve().parent.parent


def safe_run(cmd, **kwargs):
    if shutil.which(cmd[0]) is None:
        print(f"WARNING: {cmd[0]} not found in PATH")
        return subprocess.CompletedProcess(cmd, returncode=1)
    return subprocess.run(cmd, **kwargs)


def check_docker_build():
    print("Checking Docker build...")
    result = safe_run(["docker", "build", "-t", "crm-shop-test", "."], cwd=project_root, capture_output=True, text=True)
    if result.returncode != 0:
        print("Docker build failed:")
        print(result.stderr)
        return False
    return True


def check_requirements():
    print("Checking requirements installation...")
    venv_dir = project_root / ".venv-test"
    if venv_dir.exists():
        safe_run(["rm", "-rf", str(venv_dir)])
    safe_run(["python", "-m", "venv", str(venv_dir)], check=True)
    pip = str(venv_dir / "bin" / "pip")
    result = safe_run([pip, "install", "-r", str(project_root / "requirements.txt")], capture_output=True, text=True)
    safe_run(["rm", "-rf", str(venv_dir)])
    if result.returncode != 0:
        print("Requirements installation failed:")
        print(result.stderr)
        return False
    return True


def check_migrations():
    print("Checking migrations...")
    os.environ.update({
        "DJANGO_SETTINGS_MODULE": "crm_shop.settings",
        "DATABASE_URL": "sqlite:///test.db",
        "SECRET_KEY": "test-secret-key",
        "DEBUG": "True",
    })
    result = safe_run(["python", "manage.py", "migrate", "--check"], cwd=project_root, capture_output=True, text=True, env=os.environ)
    if result.returncode != 0:
        print("Migrations check failed:")
        print(result.stderr)
        return False
    return True


def main():
    all_passed = True
    if not check_docker_build():
        all_passed = False
    if not check_requirements():
        all_passed = False
    if not check_migrations():
        all_passed = False
    print("All build checks passed!" if all_passed else "Some build checks failed.")
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
