from datetime import datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_token(subject: str, token_type: str, expires_delta: timedelta) -> str:
    payload: dict[str, Any] = {
        "sub": str(subject),
        "type": token_type,
        "exp": datetime.utcnow() + expires_delta,
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def create_access_token(subject: str) -> str:
    expires = timedelta(minutes=settings.access_token_expire_minutes)
    return create_token(subject, "access", expires)


def create_refresh_token(subject: str) -> str:
    expires = timedelta(days=settings.refresh_token_expire_days)
    return create_token(subject, "refresh", expires)


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError as exc:
        raise JWTError("Token inválido ou expirado") from exc
