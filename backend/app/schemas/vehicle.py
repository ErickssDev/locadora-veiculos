from datetime import datetime
from pydantic import BaseModel, Field


class VehicleBase(BaseModel):
    brand: str
    model: str
    year: int
    color: str | None = None
    plate: str | None = None
    category: str = Field(..., pattern="^(hatch|sedan|suv|pickup|van|moto|outro)$")
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
    category: str | None = None
    description: str | None = None
    daily_rate: float | None = None
    city: str | None = None
    state: str | None = None
    is_available: bool | None = None


class VehicleResponse(VehicleBase):
    id: int
    owner_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
