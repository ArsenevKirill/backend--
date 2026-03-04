import hashlib
import secrets
from datetime import timedelta
from django.utils import timezone
from .models import Session

SESSION_TTL_DAYS = 7

def hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def create_session(user) -> str:
    raw = secrets.token_urlsafe(32)
    Session.objects.create(
        user=user,
        token_hash=hash_token(raw),
        expires_at=timezone.now() + timedelta(days=SESSION_TTL_DAYS),
    )
    return raw

def revoke_session(raw: str) -> bool:
    h = hash_token(raw)
    return Session.objects.filter(token_hash=h, revoked=False).update(revoked=True) > 0

def revoke_all_user_sessions(user) -> int:
    return Session.objects.filter(user=user, revoked=False).update(revoked=True)