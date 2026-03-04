from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from .services import create_session, revoke_session, revoke_all_user_sessions
from .models import User


class RegisterView(APIView):
    def post(self, request):
        s = RegisterSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        user = s.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        s = LoginSerializer(data=request.data)
        s.is_valid(raise_exception=True)

        email = s.validated_data["email"]
        password = s.validated_data["password"]

        user = User.objects.filter(email=email).first()
        if not user or not user.is_active:
            return Response({"detail": "Неверные данные или аккаунт удалён"}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({"detail": "Неверные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        token = create_session(user)
        return Response({"token": token}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        auth_header = request.headers.get("Authorization", "")
        parts = auth_header.split()
        if len(parts) == 2 and parts[0] == "Bearer":
            revoke_session(parts[1])
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        s = UserUpdateSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        for k, v in s.validated_data.items():
            setattr(request.user, k, v)
        request.user.save()
        return Response(UserSerializer(request.user).data)


class SoftDeleteMeView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        request.user.is_active = False
        request.user.save(update_fields=["is_active"])
        revoke_all_user_sessions(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)