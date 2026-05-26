from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    phone = Column(String(32), nullable=True)
    user_type = Column(String(32), nullable=False, default="client")
    avatar_url = Column(String(512), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    documents = relationship("UserDocument", back_populates="user", cascade="all, delete-orphan")
    vehicles = relationship("Vehicle", back_populates="owner", cascade="all, delete-orphan")
    client_reservations = relationship("Reservation", back_populates="client", foreign_keys="Reservation.client_id")
    owner_reservations = relationship("Reservation", back_populates="owner", foreign_keys="Reservation.owner_id")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
