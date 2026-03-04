from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone

from .models import Session

class SessionTokenAuthentication(BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        auth = get_authorization_header(request).decode("utf-8")
        if not auth:
            return None

        parts = auth.split()
        if len(parts) != 2 or parts[0] != self.keyword:
            return None

        raw_token = parts[1].strip()
        if not raw_token:
            return None

        # хэш ищем по sha256 (такая же логика как в сервисе)
        import hashlib
        h = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

        session = Session.objects.select_related("user").filter(token_hash=h).first()
        if not session:
            raise AuthenticationFailed("Неверный токен")

        if session.revoked:
            raise AuthenticationFailed("Сессия отозвана")

        if session.expires_at <= timezone.now():
            raise AuthenticationFailed("Сессия истекла")

        if not session.user.is_active:
            raise AuthenticationFailed("Пользователь деактивирован")

        return (session.user, session)