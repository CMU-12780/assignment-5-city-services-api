from enum import Enum as PyEnum

from sqlalchemy import Column, String, Float, Date, Integer, Enum, Boolean
from models.base import BaseModel


class HealthStatus(PyEnum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    DEAD = "dead"

class Tree(BaseModel):
    __tablename__ = "trees"
    
    # Add your fields here
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    # ... add 5-8 relevant fields
    species = Column(String, nullable=False)
    planted_date = Column(Date, nullable=True)
    diameter_cm = Column(Float, nullable=True)
    height_meters = Column(Float, nullable=True)
    health_status = Column(
        Enum(HealthStatus),
        nullable=False,
    )
    last_inspection = Column(Date, nullable=True)   
    requires_trimming = Column(Boolean, nullable=False, default=False)