from django.urls import path
from .views import RoleListCreateView, PermissionListCreateView, AssignUserRoleView, AssignRolePermissionView

urlpatterns = [
    path("access/roles", RoleListCreateView.as_view()),
    path("access/permissions", PermissionListCreateView.as_view()),
    path("access/assign-role", AssignUserRoleView.as_view()),
    path("access/assign-permission", AssignRolePermissionView.as_view()),
]