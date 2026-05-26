from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification
from app.models.user import User


async def list_notifications(db: AsyncSession, current_user: User) -> dict:
    result = await db.execute(select(Notification).where(Notification.user_id == current_user.id).order_by(Notification.created_at.desc()))
    notifications = result.scalars().all()
    return {"success": True, "notifications": notifications}


async def mark_read(db: AsyncSession, current_user: User, notification_id: int) -> dict:
    result = await db.execute(
        select(Notification).where(Notification.id == notification_id, Notification.user_id == current_user.id)
    )
    notification = result.scalar_one_or_none()
    if not notification:
        return {"success": False, "detail": "Notificação não encontrada"}
    notification.is_read = True
    db.add(notification)
    await db.commit()
    return {"success": True, "message": "Notificação marcada como lida"}


async def mark_all_read(db: AsyncSession, current_user: User) -> dict:
    await db.execute(
        update(Notification)
        .where(Notification.user_id == current_user.id, Notification.is_read == False)
        .values(is_read=True)
    )
    await db.commit()
    return {"success": True, "message": "Todas as notificações marcadas como lidas"}
