from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from typing import Optional
from .models import SidewalkCondition

class YourResourceBase(BaseModel):
    name: str
    location: str
    material: str
    width_meters: float
    length_meters: float
    number: int
    condition: SidewalkCondition
    last_inspection_date: Optional[date] = None
    slope_percent: Optional[float] = None
    lighting_level: Optional[str] = None

class YourResourceCreate(YourResourceBase):
    pass

class YourResourceUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    material: Optional[str] = None
    width_meters: Optional[float] = None
    length_meters: Optional[float] = None
    number: Optional[int] = None
    condition: Optional[SidewalkCondition] = None
    last_inspection_date: Optional[date] = None
    slope_percent: Optional[float] = None
    lighting_level: Optional[str] = None

class YourResourceResponse(YourResourceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class YourResourceListResponse(BaseModel):
    total: int
    resources: list[YourResourceResponse]
