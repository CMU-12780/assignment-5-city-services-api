from sqlalchemy import Column, String, Float, Date, Boolean, Enum, Index
from models.base import BaseModel
import enum

class HealthStatus(str, enum.Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    DEAD = "dead"

class Tree(BaseModel):
    __tablename__ = "trees"
    species = Column(String, nullable=False)
    location = Column(String, nullable=False)
    planted_date = Column(Date)
    diameter_cm = Column(Float)
    height_meters = Column(Float)
    health_status = Column(Enum(HealthStatus), nullable=False)
    last_inspection = Column(Date)
    requires_trimming = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Tree(id={self.id}, name='{self.name}', condition='{self.condition}')>"
