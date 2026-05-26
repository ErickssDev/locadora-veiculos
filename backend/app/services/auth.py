from datetime import datetime, timedelta

from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
    decode_token,
)
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    ResetPasswordRequest,
    TokenResponse,
    UserRegister,
)
from app.utils.email import send_email


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_refresh_token_record(db: AsyncSession, user: User, token: str) -> RefreshToken:
    payload = decode_token(token)
    expires_at = datetime.utcfromtimestamp(int(payload["exp"]))
    refresh_record = RefreshToken(
        user_id=user.id,
        token=token,
        expires_at=expires_at,
        revoked=False,
    )
    db.add(refresh_record)
    await db.commit()
    await db.refresh(refresh_record)
    return refresh_record


async def register_user(db: AsyncSession, payload: UserRegister) -> TokenResponse:
    existing = await get_user_by_email(db, payload.email)
    if existing:
        raise ValueError("E-mail já cadastrado")

    user = User(
        name=payload.name,
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        phone=payload.phone,
        user_type=payload.user_type,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))
    await create_refresh_token_record(db, user, refresh_token)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        message="Usuário registrado com sucesso.",
    )


async def login_user(db: AsyncSession, payload: LoginRequest) -> TokenResponse:
    user = await get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise ValueError("Credenciais inválidas")

    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))
    await create_refresh_token_record(db, user, refresh_token)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        message="Login realizado com sucesso.",
    )


async def refresh_tokens(db: AsyncSession, refresh_token: str) -> TokenResponse:
    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise JWTError("Token inválido")
        user_id = int(payload["sub"])
    except JWTError as exc:
        raise ValueError("Refresh token inválido") from exc

    result = await db.execute(select(RefreshToken).where(RefreshToken.token == refresh_token))
    record = result.scalar_one_or_none()
    if not record or record.revoked or record.expires_at < datetime.utcnow():
        raise ValueError("Refresh token expirado ou revogado")

    await revoke_refresh_token(db, refresh_token)
    user = await db.get(User, user_id)
    if not user or not user.is_active:
        raise ValueError("Usuário inválido")

    access_token = create_access_token(str(user.id))
    new_refresh = create_refresh_token(str(user.id))
    await create_refresh_token_record(db, user, new_refresh)

    return TokenResponse(access_token=access_token, refresh_token=new_refresh)


async def revoke_refresh_token(db: AsyncSession, refresh_token: str) -> None:
    result = await db.execute(select(RefreshToken).where(RefreshToken.token == refresh_token))
    record = result.scalar_one_or_none()
    if record:
        record.revoked = True
        db.add(record)
        await db.commit()


async def logout(db: AsyncSession, refresh_token: str) -> None:
    await revoke_refresh_token(db, refresh_token)


async def forgot_password(db: AsyncSession, email: str) -> None:
    user = await get_user_by_email(db, email)
    if not user:
        return

    reset_token = create_refresh_token(str(user.id))
    reset_url = f"{settings.frontend_url}/reset-password?token={reset_token}"
    await send_email(
        subject="Recuperação de senha",
        recipient=user.email,
        body=f"Use este link para redefinir sua senha: {reset_url}",
    )


async def reset_password(db: AsyncSession, token: str, new_password: str) -> None:
    try:
        payload = decode_token(token)
        if payload.get("type") != "refresh":
            raise JWTError("Token de redefinição inválido")
        user_id = int(payload["sub"])
    except JWTError as exc:
        raise ValueError("Token de redefinição inválido") from exc

    user = await db.get(User, user_id)
    if not user:
        raise ValueError("Usuário não encontrado")

    user.hashed_password = get_password_hash(new_password)
    db.add(user)
    await db.commit()
