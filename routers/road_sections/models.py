"""
RoadSection database model
"""
from sqlalchemy import Column, String, Float, Integer, Date, Enum as SQLEnum
from models.base import BaseModel
import enum


class SurfaceType(str, enum.Enum):
    """Supported pavement surface types"""
    ASPHALT = "asphalt"
    CONCRETE = "concrete"
    GRAVEL = "gravel"
    BRICK = "brick"


class ConditionRating(str, enum.Enum):
    """Pavement condition rating categories"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    FAILED = "failed"


class RoadSection(BaseModel):
    """
    RoadSection infrastructure model
    Tracks road inventory, pavement condition, and maintenance history
    """
    __tablename__ = "road_sections"

    # Inventory and geometry
    street_name = Column(String, nullable=False, index=True)
    start_address = Column(String, nullable=False)
    end_address = Column(String, nullable=False)
    length_km = Column(Float, nullable=False)
    lanes_count = Column(Integer, nullable=False)

    # Pavement characteristics
    surface_type = Column(SQLEnum(SurfaceType), nullable=False)
    condition_rating = Column(SQLEnum(ConditionRating), nullable=False)

    # Maintenance and traffic
    last_resurfaced = Column(Date, nullable=True)
    average_daily_traffic = Column(Integer, nullable=True)

    def __repr__(self) -> str:
        return (
            f"<RoadSection(id={self.id}, street_name='{self.street_name}', "
            f"condition_rating='{self.condition_rating}')>"
        )
