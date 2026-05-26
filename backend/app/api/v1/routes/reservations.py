from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.services import reservations as reservations_service
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=ReservationResponse)
async def create_reservation(payload: ReservationCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> ReservationResponse:
    return await reservations_service.create_reservation(db, current_user, payload)


@router.get("/", response_model=list[ReservationResponse])
async def list_reservations(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[ReservationResponse]:
    return await reservations_service.list_user_reservations(db, current_user)


@router.get("/{reservation_id}", response_model=ReservationResponse)
async def get_reservation(reservation_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> ReservationResponse:
    return await reservations_service.get_reservation(db, current_user, reservation_id)


@router.put("/{reservation_id}/cancel")
async def cancel_reservation(reservation_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    return await reservations_service.cancel_reservation(db, current_user, reservation_id)


@router.put("/{reservation_id}/confirm")
async def confirm_reservation(reservation_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    return await reservations_service.confirm_reservation(db, current_user, reservation_id)


@router.put("/{reservation_id}/complete")
async def complete_reservation(reservation_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    return await reservations_service.complete_reservation(db, current_user, reservation_id)
