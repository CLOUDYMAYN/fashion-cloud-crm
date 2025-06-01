from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def admin_required(function):
    def check_admin(user):
        if user.is_authenticated and user.is_admin_user():
            return True
        raise PermissionDenied

    actual_decorator = user_passes_test(check_admin)
    return actual_decorator(function)


def boss_required(function):
    def check_boss(user):
        if user.is_authenticated and user.role == "boss":
            return True
        raise PermissionDenied

    actual_decorator = user_passes_test(check_boss)
    return actual_decorator(function)
