#!/usr/bin/env python
"""
Fix common linting issues in the project.

This script automatically fixes common linting issues in the project.
"""

import os
import subprocess
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).resolve().parent.parent


def run_black():
    """Run black to format Python code."""
    print("Running black to format Python code...")
    subprocess.run(["black", str(project_root)], check=False)


def run_isort():
    """Run isort to sort imports."""
    print("Running isort to sort imports...")
    subprocess.run(["isort", str(project_root)], check=False)


def run_flake8():
    """Run flake8 to check for linting errors."""
    print("Running flake8 to check for linting errors...")
    result = subprocess.run(
        ["flake8", str(project_root)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print("Flake8 found issues:")
        print(result.stdout)
    else:
        print("No flake8 issues found!")


def run_mypy():
    """Run mypy to check for type errors."""
    print("Running mypy to check for type errors...")
    result = subprocess.run(
        ["mypy", str(project_root)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print("Mypy found issues:")
        print(result.stdout)
    else:
        print("No mypy issues found!")


def main():
    """Run all linting tools."""
    # Make sure the required tools are installed
    for tool in ["black", "isort", "flake8", "mypy"]:
        try:
            subprocess.run([tool, "--version"], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            print(f"WARNING: {tool} is not installed. Install it with 'pip install {tool}'.")
            return 1

    # Run the tools
    run_black()
    run_isort()
    run_flake8()
    run_mypy()

    print("\nLinting fixes completed. Please review the changes and commit them.")
    return 0


if __name__ == "__main__":
    exit(main())
