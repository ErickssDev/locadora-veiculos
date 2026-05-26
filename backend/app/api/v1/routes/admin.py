from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, require_admin
from app.services import admin as admin_service

router = APIRouter()


@router.get("/dashboard")
async def dashboard(db: AsyncSession = Depends(get_db), _: None = Depends(require_admin)) -> dict:
    return await admin_service.get_dashboard(db)


@router.get("/users")
async def list_users(db: AsyncSession = Depends(get_db), _: None = Depends(require_admin)) -> dict:
    return await admin_service.list_users(db)


@router.get("/vehicles")
async def list_vehicles(db: AsyncSession = Depends(get_db), _: None = Depends(require_admin)) -> dict:
    return await admin_service.list_vehicles(db)


@router.get("/reservations")
async def list_reservations(db: AsyncSession = Depends(get_db), _: None = Depends(require_admin)) -> dict:
    return await admin_service.list_reservations(db)
