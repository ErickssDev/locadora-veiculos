from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    brand = Column(String(120), nullable=False, index=True)
    model = Column(String(120), nullable=False, index=True)
    year = Column(Integer, nullable=False)
    color = Column(String(64), nullable=True)
    plate = Column(String(64), nullable=True)
    category = Column(String(48), nullable=False, default="outro")
    description = Column(String(1024), nullable=True)
    daily_rate = Column(Float, nullable=False)
    city = Column(String(120), nullable=False, index=True)
    state = Column(String(120), nullable=False, index=True)
    status = Column(String(32), nullable=False, default="pending")
    is_available = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    owner = relationship("User", back_populates="vehicles")
    photos = relationship("VehiclePhoto", back_populates="vehicle", cascade="all, delete-orphan")
    documents = relationship("VehicleDocument", back_populates="vehicle", cascade="all, delete-orphan")
    reservations = relationship("Reservation", back_populates="vehicle", cascade="all, delete-orphan")
