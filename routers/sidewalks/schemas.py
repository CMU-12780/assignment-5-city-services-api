"""
Sidewalk Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional
from .models import SidewalkCondition


class SidewalkBase(BaseModel):
    """Base sidewalk schema with common fields"""
    street_name: str = Field(..., min_length=1, max_length=200, description="Street name")
    block_number: str = Field(..., min_length=1, max_length=50, description="Block or section identifier")
    length_meters: float = Field(..., gt=0, description="Sidewalk length in meters")
    width_meters: float = Field(..., gt=0, description="Sidewalk width in meters")
    surface_material: str = Field(..., min_length=1, max_length=100, description="Material type")
    condition: SidewalkCondition = Field(..., description="Condition rating")
    ada_compliant: bool = Field(..., description="ADA compliance status")
    last_repair_date: Optional[date] = Field(None, description="Last repair date")


class SidewalkCreate(SidewalkBase):
    """Schema for creating a new sidewalk"""
    pass


class SidewalkUpdate(BaseModel):
    """Schema for updating a sidewalk - all fields optional"""
    street_name: Optional[str] = Field(None, min_length=1, max_length=200)
    block_number: Optional[str] = Field(None, min_length=1, max_length=50)
    length_meters: Optional[float] = Field(None, gt=0)
    width_meters: Optional[float] = Field(None, gt=0)
    surface_material: Optional[str] = Field(None, min_length=1, max_length=100)
    condition: Optional[SidewalkCondition] = None
    ada_compliant: Optional[bool] = None
    last_repair_date: Optional[date] = None


class SidewalkResponse(SidewalkBase):
    """Schema for sidewalk response"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SidewalkListResponse(BaseModel):
    """Schema for list of sidewalks"""
    total: int
    sidewalks: list[SidewalkResponse]
