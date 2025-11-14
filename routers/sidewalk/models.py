from sqlalchemy import Column, String, Float, Date, Integer, Enum
from models.base import BaseModel
import enum

class SidewalkCondition(str, enum.Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"

class YourResource(BaseModel):
    __tablename__ = "sidewalk"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    material = Column(String, nullable=False)
    width_meters = Column(Float, nullable=False)
    length_meters = Column(Float, nullable=False)
    number = Column(Integer, nullable=False)
    condition = Column(Enum(SidewalkCondition), nullable=False)
    last_inspection_date = Column(Date, nullable=True)
    slope_percent = Column(Float, nullable=True)
    lighting_level = Column(String, nullable=True)
