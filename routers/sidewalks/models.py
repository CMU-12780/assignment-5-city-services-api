"""
Sidewalk database model
"""
from sqlalchemy import Column, String, Float, Boolean, Date, Enum as SQLEnum
from models.base import BaseModel
import enum


class SidewalkCondition(str, enum.Enum):
    """Sidewalk condition ratings"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


class Sidewalk(BaseModel):
    """
    Sidewalk infrastructure model
    Tracks sidewalk dimensions, condition, and ADA compliance
    """
    __tablename__ = "sidewalks"

    # Basic Information
    street_name = Column(String, nullable=False, index=True)
    block_number = Column(String, nullable=False)

    # Dimensions
    length_meters = Column(Float, nullable=False)
    width_meters = Column(Float, nullable=False)

    # Materials & Features
    surface_material = Column(String, nullable=False)
    condition = Column(SQLEnum(SidewalkCondition), nullable=False, default=SidewalkCondition.GOOD)
    ada_compliant = Column(Boolean, nullable=False, default=False)

    # Maintenance
    last_repair_date = Column(Date, nullable=True)

    def __repr__(self):
        return f"<Sidewalk(id={self.id}, street='{self.street_name}', condition='{self.condition}')>"
