from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.schemas.vehicle import VehicleCreate, VehicleResponse, VehicleUpdate
from app.services import vehicles as vehicles_service
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=VehicleResponse)
async def create_vehicle(payload: VehicleCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> VehicleResponse:
    return await vehicles_service.create_vehicle(db, current_user, payload)


@router.get("/", response_model=list[VehicleResponse])
async def list_vehicles(db: AsyncSession = Depends(get_db)) -> list[VehicleResponse]:
    return await vehicles_service.list_public_vehicles(db)


@router.get("/me", response_model=list[VehicleResponse])
async def list_my_vehicles(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[VehicleResponse]:
    return await vehicles_service.list_owner_vehicles(db, current_user)


@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(vehicle_id: int, db: AsyncSession = Depends(get_db)) -> VehicleResponse:
    return await vehicles_service.get_vehicle(db, vehicle_id)


@router.put("/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(vehicle_id: int, payload: VehicleUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> VehicleResponse:
    return await vehicles_service.update_vehicle(db, current_user, vehicle_id, payload)


@router.delete("/{vehicle_id}")
async def delete_vehicle(vehicle_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    return await vehicles_service.delete_vehicle(db, current_user, vehicle_id)
