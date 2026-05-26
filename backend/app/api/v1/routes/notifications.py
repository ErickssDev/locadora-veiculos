from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.services import notifications as notifications_service
from app.models.user import User

router = APIRouter()


@router.get("/")
async def list_notifications(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    return await notifications_service.list_notifications(db, current_user)


@router.put("/{notification_id}/read")
async def mark_notification_read(notification_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    return await notifications_service.mark_read(db, current_user, notification_id)


@router.put("/read-all")
async def mark_all_read(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    return await notifications_service.mark_all_read(db, current_user)
