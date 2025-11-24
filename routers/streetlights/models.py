"""
Bridge database model
"""
from sqlalchemy import Column, Integer, String, Float, Date, Boolean, Enum as SQLEnum
from models.base import BaseModel
import enum


class LightType(str, enum.Enum):
    """Light Types"""
    LED = "LED"
    SODIUM = "sodium"
    HALOGEN = "halogen"


class Streetlight(BaseModel):
    """
    Streetlight infrastructure model
    Tracks streetlight information, conditions, and maintenance
    Inherits id, created_at, updated_at from BaseModel
    """
    __tablename__ = "streetlights"

    # Basic Information
    location = Column(String, nullable=False)
    pole_id = Column(String, nullable=False, index=True, unique=True)

    # Technical Specifications
    light_type = Column(SQLEnum(LightType), nullable=False)
    wattage = Column(Integer, nullable=False)
    energy_consumption_kwh = Column(Float, nullable=True)

    # Condition and Maintenance
    installation_date = Column(Date, nullable=True)
    last_maintenance = Column(Date, nullable=True)
    is_operational = Column(Boolean, nullable=False, default=True)

    # Notes
    notes = Column(String, nullable=True)

    def __repr__(self):
        return f"<Streetlight(id={self.id}, poleID='{self.pole_id}', operational='{self.is_operational}')>"
