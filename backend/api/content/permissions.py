from rest_framework import permissions
from users.models import UserRole

METHODS = ['POST', 'PATCH', 'DELETE']
ROLES = [UserRole.ADMIN]


class CustomPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in METHODS and (
                request.user.role in ROLES or obj.author == request.user
            )
            or request.method in permissions.SAFE_METHODS
        )
