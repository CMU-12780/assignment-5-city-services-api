from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional, List
from .models import HealthStatus

class TreeBase(BaseModel):
    species: str = Field(..., min_length=1, max_length=100, description="Tree species")
    location: str = Field(..., min_length=1, max_length=300, description="Tree Location/address")
    planted_date: Optional[date] = Field(None, description="Date the tree was planted")
    diameter_cm: Optional[float] = Field(None, gt=0, description="Trunk diameter in centimeters")
    height_meters: Optional[float] = Field(None, gt=0, description="Height of the tree in meters")
    health_status: HealthStatus = Field(..., description="Current health condition")
    last_inspection: Optional[date] = Field(None, description="Date of the last inspection")
    requires_trimming: Optional[bool] = Field(False, description="If the tree requires trimming")

class TreeCreate(TreeBase):
    pass

class TreeUpdate(BaseModel):
    species: Optional[str] = Field(None, min_length=1, max_length=100)
    location: Optional[str] = Field(None, min_length=1, max_length=300)
    planted_date: Optional[date] = None
    diameter_cm: Optional[float] = Field(None, gt=0)
    height_meters: Optional[float] = Field(None, gt=0)
    health_status: Optional[HealthStatus] = None
    last_inspection: Optional[date] = None
    requires_trimming: Optional[bool] = None

class TreeResponse(TreeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TreeListResponse(BaseModel):
    total: int
    trees: List[TreeResponse]