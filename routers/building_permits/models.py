"""
Building permit database model
"""
from sqlalchemy import Column, String, Float, Date, Enum as SQLEnum, Index
from models.base import BaseModel
import enum


class PermitType(str, enum.Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    DEMOLITION = "demolition"
    RENOVATION = "renovation"


class PermitStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"


class BuildingPermit(BaseModel):
    """Building permit database model"""

    __tablename__ = "building_permits"

    # Basic info
    permit_number = Column(String, nullable=False, unique=True, index=True)
    address = Column(String, nullable=False)

    permit_type = Column(SQLEnum(PermitType), nullable=False)
    status = Column(SQLEnum(PermitStatus), nullable=False, default=PermitStatus.PENDING)

    issue_date = Column(Date, nullable=True)
    expiration_date = Column(Date, nullable=True)

    estimated_cost = Column(Float, nullable=False)
    notes = Column(String, nullable=True)

    def __repr__(self) -> str:
        return f"<BuildingPermit(id={self.id}, permit_number='{self.permit_number}', status='{self.status}')>"
