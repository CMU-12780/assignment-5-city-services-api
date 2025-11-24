"""
Bridge Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional
from .models import LightType


class StreetlightBase(BaseModel):
    """Base streetlight schema with common fields"""
    location: str = Field(..., min_length=1, max_length=300, description="Streetlight location/address")
    pole_id: str = Field(..., min_length=1, max_length=200, description="Streetlight pole ID")
    light_type: LightType = Field(..., description="Type of light in the streetlight")
    wattage: int = Field(..., ge=0, description="Wattage of streetlight")
    energy_consumption_kwh: Optional[float] = Field(..., gt=0, description="Energy consumption of the streetlight in kw/h")
    installation_date: Optional[date] = Field(None, description="Date of installation")
    last_maintenance: Optional[date] = Field(None, description="Date of last maintenance")
    is_operational: bool = Field(True, description="If streetlight is operational or not")
    notes: Optional[str] = Field(None, max_length=1000, description="Additional notes")


class StreetlightCreate(StreetlightBase):
    """Schema for creating a new streetlight"""
    pass


class StreetlightUpdate(BaseModel):
    """Schema for updating an existing streetlight - all fields optional"""
    location: Optional[str] = Field(None, min_length=1, max_length=300)
    pole_id: Optional[str] = Field(None, min_length=1, max_length=200)
    light_type: Optional[LightType] = None
    wattage: Optional[int] = Field(None, ge=0)
    energy_consumption_kwh: Optional[float] = Field(None, gt=0)
    installation_date: Optional[date] = None
    last_maintenance: Optional[date] = None
    is_operational: Optional[bool] = None
    notes: Optional[str] = Field(None, max_length=1000)



class StreetlightResponse(StreetlightBase):
    """Schema for a streetlight response"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StreetlightListResponse(BaseModel):
    """Schema for list of streetlights"""
    total: int
    streetlights: list[StreetlightResponse]
