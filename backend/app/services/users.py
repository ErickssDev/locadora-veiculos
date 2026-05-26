from fastapi import UploadFile
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.user_document import UserDocument
from app.utils.cloudinary import delete_file, upload_file
from app.schemas.user import UserUpdate


async def update_user_profile(db: AsyncSession, current_user: User, payload: UserUpdate) -> User:
    if payload.name is not None:
        current_user.name = payload.name
    if payload.phone is not None:
        current_user.phone = payload.phone
    if payload.avatar_url is not None:
        current_user.avatar_url = payload.avatar_url

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user


def serialize_document(document: UserDocument) -> dict:
    return {
        "id": document.id,
        "user_id": document.user_id,
        "document_type": document.document_type,
        "file_url": document.file_url,
        "public_id": document.public_id,
        "status": document.status,
        "created_at": document.created_at,
    }


async def upload_user_document(db: AsyncSession, current_user: User, file: UploadFile, document_type: str) -> dict:
    content = await file.read()
    upload = await upload_file(content, folder="users/documents", filename=file.filename)
    document = UserDocument(
        user_id=current_user.id,
        document_type=document_type,
        file_url=upload["url"],
        public_id=upload["public_id"],
    )
    db.add(document)
    await db.commit()
    await db.refresh(document)
    return {"success": True, "document": serialize_document(document)}


async def list_user_documents(db: AsyncSession, current_user: User) -> dict:
    result = await db.execute(select(UserDocument).where(UserDocument.user_id == current_user.id))
    documents = [serialize_document(document) for document in result.scalars().all()]
    return {"success": True, "documents": documents}


async def delete_user_document(db: AsyncSession, current_user: User, document_id: int) -> dict:
    result = await db.execute(
        select(UserDocument).where(UserDocument.id == document_id, UserDocument.user_id == current_user.id)
    )
    document = result.scalar_one_or_none()
    if not document:
        return {"success": False, "detail": "Documento não encontrado"}
    await delete_file(document.public_id)
    await db.execute(delete(UserDocument).where(UserDocument.id == document.id))
    await db.commit()
    return {"success": True, "message": "Documento removido"}
