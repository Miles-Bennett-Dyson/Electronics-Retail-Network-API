from rest_framework.permissions import BasePermission


class IsActiveEmployee(BasePermission):
    """ Проверяет, является ли user активным сотрудником. """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_active
        )
