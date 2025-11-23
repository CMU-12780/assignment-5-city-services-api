from sqlalchemy import Column, String, Float, Date, Integer, Enum as SQLEnum
from models.base import BaseModel
import enum 

class BikeLaneCondition(str, enum.Enum):
    """Bike Lane condition ratings"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"

class BikeLaneType(str, enum.Enum):
    """Bike Lane types"""
    PROTECTED = "protected"
    BUFFERED = "buffered"
    SHARED = "shared"
    CONVENTIONAL = "conventional"

class BikeLane(BaseModel):
    __tablename__ = "bike_lanes"

    
    # Add your fields here
    street_name = Column(String, nullable=False, index=True)
    start_location = Column(String, nullable=False)
    end_location = Column(String, nullable=False)
    length_km = Column(Float, nullable=False)
    lane_type = Column(SQLEnum(BikeLaneType), nullable=False)
    surface_condition = Column(SQLEnum(BikeLaneCondition), nullable=False)
    incidents_lat_year = Column(Integer, default=0)
    last_resurfaced = Column(Date, nullable=True)

    def __repr__(self):
        return f"<BikeLane(id={self.id}, street_name='{self.street_name}', lane_type='{self.lane_type}')>" 