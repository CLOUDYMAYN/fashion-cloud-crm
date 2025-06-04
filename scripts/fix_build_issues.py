#!/usr/bin/env python
"""
Fix common build issues in the project.
"""

import os
import shutil
import subprocess  # nosec B404
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent


def safe_run(cmd, **kwargs):
    """Run a command safely using full executable path to avoid Bandit B603/B607."""
    tool_path = shutil.which(cmd[0])
    if tool_path is None:
        print(f"WARNING: {cmd[0]} not found in PATH")
        return subprocess.CompletedProcess(cmd, returncode=1)

    full_cmd = [tool_path] + cmd[1:]

    return subprocess.run(
        full_cmd,
        shell=False,  # ensures no shell injection
        capture_output=True,
        text=True,
        check=False,
        **kwargs,
    )  # nosec B603


def check_docker_build():
    print("Checking Docker build...")
    result = safe_run(["docker", "build", "-t", "crm-shop-test", "."], cwd=project_root)
    if result.returncode != 0:
        print("Docker build failed:")
        print(result.stderr)
        return False
    return True


def check_requirements():
    print("Checking requirements installation...")
    venv_dir = project_root / ".venv-test"
    if venv_dir.exists():
        shutil.rmtree(venv_dir)

    python_exec = shutil.which("python")
    if not python_exec:
        print("Python not found.")
        return False

    # Create venv
    result = safe_run([python_exec, "-m", "venv", str(venv_dir)])
    if result.returncode != 0:
        print("Virtual environment creation failed.")
        return False

    pip_exec = shutil.which("pip") or str(venv_dir / "bin" / "pip")
    result = safe_run([pip_exec, "install", "-r", str(project_root / "requirements.txt")])
    shutil.rmtree(venv_dir)

    if result.returncode != 0:
        print("Requirements installation failed:")
        print(result.stderr)
        return False
    return True


def check_migrations():
    print("Checking migrations...")
    env = os.environ.copy()
    env.update(
        {
            "DJANGO_SETTINGS_MODULE": "crm_shop.settings",
            "DATABASE_URL": "sqlite:///test.db",
            "SECRET_KEY": "test-secret-key",
            "DEBUG": "True",
        }
    )

    python_exec = shutil.which("python")
    if not python_exec:
        print("Python not found.")
        return False

    result = safe_run(
        [python_exec, "manage.py", "migrate", "--check"],
        cwd=project_root,
        env=env,
    )
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
