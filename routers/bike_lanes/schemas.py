from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime 
from typing import Optional

from .models import BikeLaneCondition, BikeLaneType, BikeLane

class BikeLaneBase(BaseModel):
    # Fields for create/update
    
    street_name: str = Field(..., min_length=1, max_length=200, description="Street name where the bike lane is located") 
    start_location: str = Field(..., min_length=1, max_length=300, description="Starting point of the bike lane")
    end_location: str = Field(..., min_length=1, max_length=300, description="Ending point of the bike lane")
    length_km: float = Field(..., gt=0, description="Length of the bike lane in kilometers")
    lane_type: BikeLaneType = Field(..., description="Type of the bike lane")
    surface_condition: BikeLaneCondition = Field(..., description="Surface condition of the bike lane")
    incidents_lat_year: Optional[int] = Field(0, ge=0, description="Number of incidents in the last year")
    last_resurfaced: Optional[date] = Field(None, description="Date when the bike lane was last resurfaced")


class BikeLaneCreate(BikeLaneBase):
    pass

class BikeLaneUpdate(BaseModel):
    # All fields optional
    street_name: Optional[str] = Field(None, min_length=1, max_length=200)
    start_location: Optional[str] = Field(None, min_length=1, max_length=300)
    end_location: Optional[str] = Field(None, min_length=1, max_length=300)
    length_km: Optional[float] = Field(None, gt=0)
    lane_type: Optional[BikeLaneType] = None
    surface_condition: Optional[BikeLaneCondition] = None
    incidents_lat_year: Optional[int] = Field(None, ge=0)
    last_resurfaced: Optional[date] = None

class BikeLaneResponse(BikeLaneBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class BikeLaneListResponse(BaseModel):
    total: int
    resources: list[BikeLaneResponse]