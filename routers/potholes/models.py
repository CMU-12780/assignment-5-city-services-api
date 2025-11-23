"""
Pothole database model
"""
from sqlalchemy import Column, String, Float, Date, Enum as SQLEnum
from models.base import BaseModel
import enum


class PotholeSeverity(str, enum.Enum):
    """Pothole severity ratings"""
    MINOR = "minor"
    MODERATE = "moderate"
    SEVERE = "severe"


class PotholeRepairStatus(str, enum.Enum):
    """Pothole repair status values"""
    REPORTED = "reported"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Pothole(BaseModel):
    """
    Pothole infrastructure model
    Tracks pothole reports, severity, and repair lifecycle
    """
    __tablename__ = "potholes"

    # Basic information
    location = Column(String, nullable=False, index=True)
    reported_date = Column(Date, nullable=False)

    # Characteristics
    severity = Column(SQLEnum(PotholeSeverity), nullable=False)
    size_diameter_cm = Column(Float, nullable=False)

    # Repair tracking
    repair_status = Column(SQLEnum(PotholeRepairStatus), nullable=False, default=PotholeRepairStatus.REPORTED)
    repair_date = Column(Date, nullable=True)
    repair_cost = Column(Float, nullable=True)

    notes = Column(String, nullable=True)

    def __repr__(self):
        return f"<Pothole(id={self.id}, location='{self.location}', severity='{self.severity}', repair_status='{self.repair_status}')>"
