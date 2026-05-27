from enum import Enum
from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate


async def create_vehicle(db: AsyncSession, current_user: User, payload: VehicleCreate) -> Vehicle:
    if current_user.user_type != "owner":
        raise PermissionError("Apenas owners podem cadastrar veículos")

    category = payload.category.value if isinstance(payload.category, Enum) else payload.category
    vehicle = Vehicle(
        owner_id=current_user.id,
        brand=payload.brand,
        model=payload.model,
        year=payload.year,
        color=payload.color,
        plate=payload.plate,
        category=category,
        description=payload.description,
        daily_rate=payload.daily_rate,
        city=payload.city,
        state=payload.state,
        status="approved",
        is_available=payload.is_available,
    )
    db.add(vehicle)
    await db.commit()
    await db.refresh(vehicle)
    return vehicle


async def get_vehicle(db: AsyncSession, vehicle_id: int) -> Vehicle:
    result = await db.execute(select(Vehicle).where(Vehicle.id == vehicle_id))
    vehicle = result.scalar_one_or_none()
    if not vehicle:
        raise ValueError("Veículo não encontrado")
    return vehicle


async def update_vehicle(db: AsyncSession, current_user: User, vehicle_id: int, payload: VehicleUpdate) -> Vehicle:
    result = await db.execute(select(Vehicle).where(Vehicle.id == vehicle_id, Vehicle.owner_id == current_user.id))
    vehicle = result.scalar_one_or_none()
    if not vehicle:
        raise PermissionError("Veículo não encontrado ou acesso negado")

    for field, value in payload.model_dump(exclude_unset=True).items():
        if field == "category" and isinstance(value, Enum):
            value = value.value
        setattr(vehicle, field, value)

    db.add(vehicle)
    await db.commit()
    await db.refresh(vehicle)
    return vehicle


async def delete_vehicle(db: AsyncSession, current_user: User, vehicle_id: int) -> dict:
    result = await db.execute(select(Vehicle).where(Vehicle.id == vehicle_id, Vehicle.owner_id == current_user.id))
    vehicle = result.scalar_one_or_none()
    if not vehicle:
        raise PermissionError("Veículo não encontrado ou acesso negado")

    await db.execute(delete(Vehicle).where(Vehicle.id == vehicle.id))
    await db.commit()
    return {"success": True, "message": "Veículo excluído"}


async def list_owner_vehicles(db: AsyncSession, current_user: User) -> list[Vehicle]:
    result = await db.execute(select(Vehicle).where(Vehicle.owner_id == current_user.id))
    return result.scalars().all()


async def list_public_vehicles(db: AsyncSession, filters: dict | None = None) -> list[Vehicle]:
    filters = filters or {}
    query = select(Vehicle).where(Vehicle.status == "approved", Vehicle.is_available == True)
    if brand := filters.get("brand"):
        query = query.where(Vehicle.brand.ilike(f"%{brand}%"))
    if model := filters.get("model"):
        query = query.where(Vehicle.model.ilike(f"%{model}%"))
    if year := filters.get("year"):
        query = query.where(Vehicle.year == int(year))
    if city := filters.get("city"):
        query = query.where(Vehicle.city.ilike(f"%{city}%"))
    if state := filters.get("state"):
        query = query.where(Vehicle.state.ilike(f"%{state}%"))
    return (await db.execute(query)).scalars().all()
