#!/usr/bin/env python
"""
Fix common linting issues in the project.
"""
import shutil
import subprocess  # nosec B404
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent


def safe_run(cmd, **kwargs):
    if shutil.which(cmd[0]) is None:
        print(f"WARNING: {cmd[0]} not found in PATH")
        return subprocess.CompletedProcess(cmd, returncode=1)
    return subprocess.run(
        ["bandit", "-r", str(project_root)], shell=False, capture_output=True, text=True
    )


def run_black():
    print("Running black...")
    safe_run(["black", str(project_root)])


def run_isort():
    print("Running isort...")
    safe_run(["isort", str(project_root)])


def run_flake8():
    print("Running flake8...")
    result = safe_run(["flake8", str(project_root)], capture_output=True, text=True)
    if result.returncode != 0:
        print("Flake8 issues:\n" + result.stdout)
    else:
        print("No flake8 issues.")


def run_mypy():
    print("Running mypy...")
    result = safe_run(["mypy", str(project_root)], capture_output=True, text=True)
    if result.returncode != 0:
        print("Mypy issues:\n" + result.stdout)
    else:
        print("No mypy issues.")


def main():
    for tool in ["black", "isort", "flake8", "mypy"]:
        if shutil.which(tool) is None:
            print(f"WARNING: {tool} not found. Install it with 'pip install {tool}'")
            return 1
    run_black()
    run_isort()
    run_flake8()
    run_mypy()
    print("\nLinting fixes complete.")
    return 0


if __name__ == "__main__":
    exit(main())
