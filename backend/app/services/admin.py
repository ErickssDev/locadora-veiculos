from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification
from app.models.reservation import Reservation
from app.models.user import User
from app.models.vehicle import Vehicle


async def get_dashboard(db: AsyncSession) -> dict:
    total_users = await db.scalar(select(func.count()).select_from(User))
    total_vehicles = await db.scalar(select(func.count()).select_from(Vehicle))
    total_reservations = await db.scalar(select(func.count()).select_from(Reservation))
    estimated_revenue = await db.scalar(select(func.coalesce(func.sum(Reservation.total_amount), 0.0)))
    return {
        "success": True,
        "data": {
            "total_users": total_users,
            "total_vehicles": total_vehicles,
            "total_reservations": total_reservations,
            "estimated_revenue": float(estimated_revenue or 0.0),
        },
    }


async def list_users(db: AsyncSession) -> dict:
    result = await db.execute(select(User).order_by(User.created_at.desc()))
    return {"success": True, "users": result.scalars().all()}


async def list_vehicles(db: AsyncSession) -> dict:
    result = await db.execute(select(Vehicle).order_by(Vehicle.created_at.desc()))
    return {"success": True, "vehicles": result.scalars().all()}


async def list_reservations(db: AsyncSession) -> dict:
    result = await db.execute(select(Reservation).order_by(Reservation.created_at.desc()))
    return {"success": True, "reservations": result.scalars().all()}
