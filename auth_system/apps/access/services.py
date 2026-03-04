from .models import UserRole, RolePermission

def get_user_permission_codes(user) -> set[str]:
    role_ids = UserRole.objects.filter(user=user).values_list("role_id", flat=True)
    codes = RolePermission.objects.filter(role_id__in=role_ids).select_related("permission") \
        .values_list("permission__code", flat=True)
    return set(codes)

def user_has_permission(user, code: str) -> bool:
    return code in get_user_permission_codes(user)

def user_is_admin(user) -> bool:
    # простое правило: роль "admin" или право "access.manage"
    from .models import Role
    admin_role = Role.objects.filter(name="admin").first()
    if admin_role and UserRole.objects.filter(user=user, role=admin_role).exists():
        return True
    return user_has_permission(user, "access.manage")