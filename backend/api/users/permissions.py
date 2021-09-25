from rest_framework.permissions import BasePermission

METHODS = ['HEAD', 'OPTIONS']


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        allowed_methods = METHODS
        return (
            request.method in allowed_methods
            or request.user.is_admin
            or request.user.is_superuser
        )
