"""
Crosswalk Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional

class CrosswalkBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Name of the crosswalk identifier")
    location: str = Field(..., min_length=1, max_length=300, description="Crosswalk location/intersection")
    width_meters: float = Field(..., gt=0, description="Width in meters")
    condition: str = Field(..., min_length=1, max_length=100, description="Current condition rating")
    last_inspection_date: Optional[date] = Field(None, description="Date of last inspection")
    year_created: Optional[str] = Field(None, max_length=4, description="Year crosswalk was created/painted")

class CrosswalkCreate(CrosswalkBase):
    pass

class CrosswalkUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    location: Optional[str] = Field(None, min_length=1, max_length=300)
    width_meters: Optional[float] = Field(None, gt=0)
    condition: Optional[str] = Field(None, min_length=1, max_length=100)
    last_inspection_date: Optional[date] = None
    year_created: Optional[str] = Field(None, max_length=4)

class CrosswalkResponse(CrosswalkBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CrosswalkListResponse(BaseModel):
    total: int
    crosswalks: list[CrosswalkResponse]