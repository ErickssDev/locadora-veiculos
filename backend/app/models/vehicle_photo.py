from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class VehiclePhoto(Base):
    __tablename__ = "vehicle_photos"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)
    file_url = Column(String(512), nullable=False)
    public_id = Column(String(255), nullable=False)
    is_cover = Column(Integer, default=0, nullable=False)
    display_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    vehicle = relationship("Vehicle", back_populates="photos")
