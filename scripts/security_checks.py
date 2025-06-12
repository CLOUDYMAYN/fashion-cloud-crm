#!/usr/bin/env python
"""
Security checks for Django CRM Shop.

This script performs security checks on the Django CRM Shop project.
"""

import os
import shutil
import subprocess  # nosec B404
import sys
from pathlib import Path

import django
from django.conf import settings

# Add the project root to the path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# Import Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm_shop.settings")
django.setup()


def check_debug_mode():
    """Check if DEBUG is set to False in production."""
    if settings.DEBUG:
        print("WARNING: DEBUG is set to True. This should be False in production.")
        return False
    return True


def check_secret_key():
    """Check if SECRET_KEY is properly set."""
    if not settings.SECRET_KEY or len(settings.SECRET_KEY) < 32:  # nosec B105
        print("WARNING: SECRET_KEY is not properly set.")
        return False
    return True


def check_allowed_hosts():
    """Check if ALLOWED_HOSTS is properly set."""
    if settings.ALLOWED_HOSTS == ["*"] or not settings.ALLOWED_HOSTS:
        print("WARNING: ALLOWED_HOSTS is not properly set.")
        return False
    return True


def check_secure_settings():
    """Check if secure settings are properly set."""
    secure_settings = True
    if not settings.SESSION_COOKIE_SECURE:
        print("WARNING: SESSION_COOKIE_SECURE is not set to True.")
        secure_settings = False
    if not settings.CSRF_COOKIE_SECURE:
        print("WARNING: CSRF_COOKIE_SECURE is not set to True.")
        secure_settings = False
    if not settings.SECURE_SSL_REDIRECT:
        print("WARNING: SECURE_SSL_REDIRECT is not set to True.")
        secure_settings = False
    return secure_settings


def run_bandit():
    """Run Bandit security check on the project."""
    bandit_path = shutil.which("bandit")
    if not bandit_path:
        print("WARNING: Bandit is not installed.")
        return False
    result = subprocess.run(
        [bandit_path, "-r", str(project_root)],
        shell=False,
        capture_output=True,
        text=True,
        check=False,
    )  # nosec B603 B607
    if result.returncode != 0:
        print("WARNING: Bandit found security issues:")
        print(result.stdout)
        return False
    return True


def run_safety():
    """Run Safety check on installed dependencies."""
    safety_path = shutil.which("safety")
    if not safety_path:
        print("WARNING: Safety is not installed.")
        return False
    result = subprocess.run(
        [safety_path, "check", "--full-report"],
        shell=False,
        capture_output=True,
        text=True,
        check=False,
    )  # nosec B603 B607
    if result.returncode != 0:
        print("WARNING: Safety found security issues in dependencies:")
        print(result.stdout)
        return False
    return True


def main():
    """Run all security checks."""
    checks = [
        check_debug_mode,
        check_secret_key,
        check_allowed_hosts,
        check_secure_settings,
        run_bandit,
        run_safety,
    ]
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
    if all_passed:
        print("✅ All security checks passed!")
        return 0
    else:
        print("❌ Some security checks failed. Please review the warnings above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
