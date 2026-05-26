from datetime import date, datetime
from pydantic import BaseModel, Field


class ReservationCreate(BaseModel):
    vehicle_id: int
    start_date: date
    end_date: date


class ReservationResponse(BaseModel):
    id: int
    vehicle_id: int
    client_id: int
    owner_id: int
    start_date: date
    end_date: date
    total_days: int
    daily_rate_snapshot: float
    total_amount: float
    status: str
    cancellation_reason: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
