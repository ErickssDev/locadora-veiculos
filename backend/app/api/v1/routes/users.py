from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.user import UserProfile, UserUpdate
from app.services import users as users_service

router = APIRouter()


@router.get("/me", response_model=UserProfile)
async def read_me(current_user: User = Depends(get_current_user)) -> UserProfile:
    return current_user


@router.put("/me", response_model=UserProfile)
async def update_me(payload: UserUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> UserProfile:
    return await users_service.update_user_profile(db, current_user, payload)


@router.post("/me/documents")
async def upload_document(file: UploadFile = File(...), document_type: str = "other", db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    return await users_service.upload_user_document(db, current_user, file, document_type)


@router.get("/me/documents")
async def list_documents(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    return await users_service.list_user_documents(db, current_user)


@router.delete("/me/documents/{document_id}")
async def delete_document(document_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    return await users_service.delete_user_document(db, current_user, document_id)
