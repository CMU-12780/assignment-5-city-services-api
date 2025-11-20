from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime
from typing import Optional

from .models import HealthStatus

class TreeBase(BaseModel):
    # Fields for create/update
    name: str = Field( ..., min_length=1, max_length=200, description="Tree name")
    species: str = Field( ..., min_length=1, max_length=200, description="Tree species")
    location: str = Field( ..., min_length=1, max_length=300, description="Street Addr",)
    planted_date: Optional[date] = Field(default=None,description="Date the tree was planted")
    diameter_cm: Optional[float] = Field(default=None,gt=0,description="Tree diameter")
    height_meters: Optional[float] = Field(default=None, gt=0, description="Tree Height")
    health_status: HealthStatus = Field( ..., description="Tree Healthy")
    last_inspection: Optional[date] = Field(default=None, description="Date of last inspection")
    requires_trimming: bool = Field(default=False, description="Whether tree needs trimming")

class TreeCreate(TreeBase):
    pass

class TreeUpdate(BaseModel):
    # All fields optional
    species: Optional[str] = Field(default=None, min_length=1, max_length=200)
    location: Optional[str] = Field(default=None, min_length=1, max_length=300)
    planted_date: Optional[date] = None
    diameter_cm: Optional[float] = Field(default=None, gt=0)
    height_meters: Optional[float] = Field(default=None, gt=0)
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
    trees: list[TreeResponse]   