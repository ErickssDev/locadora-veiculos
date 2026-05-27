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
    users = result.scalars().all()

    users_serialized = []
    for u in users:
        users_serialized.append(
            {
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "phone": u.phone,
                "user_type": u.user_type,
                "avatar_url": u.avatar_url,
                "is_active": bool(u.is_active),
                "is_verified": bool(u.is_verified),
                "created_at": u.created_at.isoformat() if u.created_at else None,
                "updated_at": u.updated_at.isoformat() if u.updated_at else None,
            }
        )

    return {"success": True, "users": users_serialized}


async def list_vehicles(db: AsyncSession) -> dict:
    result = await db.execute(select(Vehicle).order_by(Vehicle.created_at.desc()))
    vehicles = result.scalars().all()

    vehicles_serialized = []
    for v in vehicles:
        vehicles_serialized.append(
            {
                "id": v.id,
                "owner_id": v.owner_id,
                "brand": v.brand,
                "model": v.model,
                "year": v.year,
                "color": v.color,
                "plate": v.plate,
                "category": v.category,
                "description": v.description,
                "daily_rate": float(v.daily_rate or 0.0),
                "city": v.city,
                "state": v.state,
                "status": v.status,
                "is_available": bool(v.is_available),
                "created_at": v.created_at.isoformat() if v.created_at else None,
                "updated_at": v.updated_at.isoformat() if v.updated_at else None,
            }
        )

    return {"success": True, "vehicles": vehicles_serialized}


async def list_reservations(db: AsyncSession) -> dict:
    result = await db.execute(select(Reservation).order_by(Reservation.created_at.desc()))
    reservations = result.scalars().all()

    reservations_serialized = []
    for r in reservations:
        reservations_serialized.append(
            {
                "id": r.id,
                "vehicle_id": r.vehicle_id,
                "client_id": r.client_id,
                "owner_id": r.owner_id,
                "start_date": r.start_date.isoformat() if r.start_date else None,
                "end_date": r.end_date.isoformat() if r.end_date else None,
                "total_days": r.total_days,
                "daily_rate_snapshot": float(r.daily_rate_snapshot or 0.0),
                "total_amount": float(r.total_amount or 0.0),
                "status": r.status,
                "cancellation_reason": r.cancellation_reason,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "updated_at": r.updated_at.isoformat() if r.updated_at else None,
            }
        )

    return {"success": True, "reservations": reservations_serialized}
