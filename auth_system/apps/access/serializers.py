from rest_framework import serializers
from .models import Role, Permission, UserRole, RolePermission
from apps.users.models import User

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "name")

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ("id", "code", "description")

class AssignUserRoleSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role_id = serializers.IntegerField()

class AssignRolePermissionSerializer(serializers.Serializer):
    role_id = serializers.IntegerField()
    permission_id = serializers.IntegerField()