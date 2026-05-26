from datetime import datetime

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reservation import Reservation
from app.models.vehicle import Vehicle
from app.schemas.reservation import ReservationCreate
from app.models.user import User


async def has_conflict(db: AsyncSession, vehicle_id: int, start_date, end_date) -> bool:
    query = select(Reservation).where(
        Reservation.vehicle_id == vehicle_id,
        Reservation.status.in_(["pending", "confirmed"]),
        Reservation.start_date <= end_date,
        Reservation.end_date >= start_date,
    )
    result = await db.execute(query)
    return result.scalars().first() is not None


async def create_reservation(db: AsyncSession, current_user: User, payload: ReservationCreate) -> Reservation:
    if current_user.user_type != "client":
        raise PermissionError("Apenas clientes podem reservar veículos")

    if payload.start_date > payload.end_date:
        raise ValueError("Datas inválidas")

    vehicle = await db.get(Vehicle, payload.vehicle_id)
    if not vehicle or vehicle.status != "approved" or not vehicle.is_available:
        raise ValueError("Veículo indisponível para reserva")
    if vehicle.owner_id == current_user.id:
        raise ValueError("Não é possível reservar seu próprio veículo")

    if await has_conflict(db, vehicle.id, payload.start_date, payload.end_date):
        raise ValueError("O veículo já está reservado para o período solicitado")

    total_days = (payload.end_date - payload.start_date).days + 1
    total_amount = float(vehicle.daily_rate) * total_days
    reservation = Reservation(
        vehicle_id=vehicle.id,
        client_id=current_user.id,
        owner_id=vehicle.owner_id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        total_days=total_days,
        daily_rate_snapshot=vehicle.daily_rate,
        total_amount=total_amount,
    )
    db.add(reservation)
    await db.commit()
    await db.refresh(reservation)
    return reservation


async def list_user_reservations(db: AsyncSession, current_user: User) -> list[Reservation]:
    query = select(Reservation).where(
        (Reservation.client_id == current_user.id) | (Reservation.owner_id == current_user.id)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def get_reservation(db: AsyncSession, current_user: User, reservation_id: int) -> Reservation:
    reservation = await db.get(Reservation, reservation_id)
    if not reservation:
        raise ValueError("Reserva não encontrada")
    if current_user.id not in [reservation.client_id, reservation.owner_id]:
        raise PermissionError("Acesso negado")
    return reservation


async def cancel_reservation(db: AsyncSession, current_user: User, reservation_id: int) -> dict:
    reservation = await get_reservation(db, current_user, reservation_id)
    reservation.status = "cancelled"
    reservation.cancellation_reason = "Cancelado pelo usuário"
    db.add(reservation)
    await db.commit()
    return {"success": True, "message": "Reserva cancelada"}


async def confirm_reservation(db: AsyncSession, current_user: User, reservation_id: int) -> dict:
    reservation = await get_reservation(db, current_user, reservation_id)
    if reservation.owner_id != current_user.id:
        raise PermissionError("Apenas o proprietário pode confirmar")
    if reservation.status != "pending":
        raise ValueError("A reserva não está pendente")
    reservation.status = "confirmed"
    db.add(reservation)
    await db.commit()
    return {"success": True, "message": "Reserva confirmada"}


async def complete_reservation(db: AsyncSession, current_user: User, reservation_id: int) -> dict:
    reservation = await get_reservation(db, current_user, reservation_id)
    if current_user.id not in [reservation.owner_id, reservation.client_id]:
        raise PermissionError("Acesso negado")
    if reservation.status != "confirmed":
        raise ValueError("A reserva deve estar confirmada para concluir")
    reservation.status = "completed"
    db.add(reservation)
    await db.commit()
    return {"success": True, "message": "Reserva concluída"}
