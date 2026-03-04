from rest_framework.permissions import BasePermission
from .services import user_has_permission, user_is_admin

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and user_is_admin(request.user))

def HasPermissionCode(code: str):
    class _HasPermission(BasePermission):
        def has_permission(self, request, view):
            return bool(request.user and user_has_permission(request.user, code))
    return _HasPermission