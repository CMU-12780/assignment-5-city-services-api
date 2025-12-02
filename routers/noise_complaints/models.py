
from sqlalchemy import Column, String, Float, Date, Integer, Enum as SQLEnum
from models.base import BaseModel
import enum


class ComplaintStatus(str, enum.Enum):
    """Complaint status ratings"""
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"


class ComplaintCause(str, enum.Enum):
    """Complaint status ratings"""
    CONSTRUCTION = "construction"
    TRAFFIC = "traffic"
    COMMERCIAL = "commercial"
    RESIDENTIAL = "residential"
    OTHER = "other"

 
class NoiseComplaint(BaseModel):
    __tablename__ = "noise_complaints"
    
    name = Column(String, nullable=False)
    location = Column(String, index=True, nullable=False)
    reported_date = Column(Date, nullable=False)
    time_of_day = Column(String, nullable=False)
    decibel_level = Column(Float)
    status = Column(SQLEnum(ComplaintStatus), nullable=False, default=ComplaintStatus.OPEN)
    noise_source=Column(SQLEnum(ComplaintCause), nullable=False, default=ComplaintCause.OTHER)
    resolution_date = Column(Date)
    notes = Column(String)

    def __repr__(self):
        return f"<NoiseComplaint(name={self.name}, id='{self.id}', status='{self.status}')>"
    
#**Key Requirements:**  
#- Inherit from `BaseModel` (gives you `id`, `created_at`, `updated_at`)
#- Include at least 5-8 meaningful fields
#- Use appropriate data types (String, Float, Integer, Date, etc.)
#- Consider using Enums for categorical data (like condition ratings)

