from django.core.management.base import BaseCommand
from apps.users.models import User
from apps.access.models import Role, Permission, UserRole, RolePermission


class Command(BaseCommand):
    help = "Seed roles/permissions/users"

    def handle(self, *args, **options):
        perms = [
            ("access.manage", "Управление ролями/правами"),
            ("orders.read", "Чтение заказов"),
            ("orders.create", "Создание заказов"),
            ("reports.view", "Просмотр отчетов"),
        ]

        perm_map = {}
        for code, desc in perms:
            p, _ = Permission.objects.get_or_create(code=code, defaults={"description": desc})
            perm_map[code] = p

        admin_role, _ = Role.objects.get_or_create(name="admin")
        user_role, _ = Role.objects.get_or_create(name="user")

        for p in Permission.objects.all():
            RolePermission.objects.get_or_create(role=admin_role, permission=p)

        RolePermission.objects.get_or_create(role=user_role, permission=perm_map["orders.read"])

        admin, _ = User.objects.get_or_create(
            email="admin@example.com",
            defaults={"first_name": "Admin", "is_staff": True, "is_superuser": True},
        )
        if not admin.check_password("admin12345"):
            admin.set_password("admin12345")
            admin.save()

        user, _ = User.objects.get_or_create(email="user@example.com", defaults={"first_name": "User"})
        if not user.check_password("user12345"):
            user.set_password("user12345")
            user.save()

        UserRole.objects.get_or_create(user=admin, role=admin_role)
        UserRole.objects.get_or_create(user=user, role=user_role)

        self.stdout.write(self.style.SUCCESS("✅ Seed done"))