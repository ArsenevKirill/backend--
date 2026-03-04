from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Role, Permission, UserRole, RolePermission
from .serializers import RoleSerializer, PermissionSerializer, AssignUserRoleSerializer, AssignRolePermissionSerializer
from .permissions import IsAdmin

class RoleListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response(RoleSerializer(Role.objects.all(), many=True).data)

    def post(self, request):
        s = RoleSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        role = s.save()
        return Response(RoleSerializer(role).data, status=status.HTTP_201_CREATED)

class PermissionListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response(PermissionSerializer(Permission.objects.all(), many=True).data)

    def post(self, request):
        s = PermissionSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        perm = s.save()
        return Response(PermissionSerializer(perm).data, status=status.HTTP_201_CREATED)

class AssignUserRoleView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        s = AssignUserRoleSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        UserRole.objects.get_or_create(user_id=s.validated_data["user_id"], role_id=s.validated_data["role_id"])
        return Response(status=status.HTTP_204_NO_CONTENT)

class AssignRolePermissionView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        s = AssignRolePermissionSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        RolePermission.objects.get_or_create(
            role_id=s.validated_data["role_id"],
            permission_id=s.validated_data["permission_id"],
        )
        return Response(status=status.HTTP_204_NO_CONTENT)