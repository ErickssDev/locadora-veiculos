from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class VehicleCategory(str, Enum):
    hatch = "hatch"
    sedan = "sedan"
    suv = "suv"
    pickup = "pickup"
    van = "van"
    moto = "moto"
    outro = "outro"


class VehicleBase(BaseModel):
    brand: str
    model: str
    year: int
    color: str | None = None
    plate: str | None = None
    category: VehicleCategory = Field(..., description="Categoria do veículo")
    description: str | None = None
    daily_rate: float
    city: str
    state: str
    is_available: bool = True


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    brand: str | None = None
    model: str | None = None
    year: int | None = None
    color: str | None = None
    plate: str | None = None
    category: VehicleCategory | None = None
    description: str | None = None
    daily_rate: float | None = None
    city: str | None = None
    state: str | None = None
    is_available: bool | None = None


class VehicleResponse(VehicleBase):
    category: str
    id: int
    owner_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
