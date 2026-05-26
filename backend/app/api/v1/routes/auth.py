from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    LogoutRequest,
    ResetPasswordRequest,
    RefreshRequest,
    TokenResponse,
    UserRegister,
)
from app.services import auth as auth_service

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def register(payload: UserRegister, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    return await auth_service.register_user(db, payload)


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    return await auth_service.login_user(db, payload)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    return await auth_service.refresh_tokens(db, payload.refresh_token)


@router.post("/forgot-password")
async def forgot_password(payload: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)) -> dict:
    await auth_service.forgot_password(db, payload.email)
    return {"success": True, "message": "E-mail de recuperação enviado se o usuário existir."}


@router.post("/reset-password")
async def reset_password(payload: ResetPasswordRequest, db: AsyncSession = Depends(get_db)) -> dict:
    await auth_service.reset_password(db, payload.token, payload.new_password)
    return {"success": True, "message": "Senha redefinida com sucesso."}


@router.post("/logout")
async def logout(payload: LogoutRequest, db: AsyncSession = Depends(get_db)) -> dict:
    await auth_service.logout(db, payload.refresh_token)
    return {"success": True, "message": "Logout realizado com sucesso."}
