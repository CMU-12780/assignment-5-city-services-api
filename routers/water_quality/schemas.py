"""
Pydantic schemas for water quality samples
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime
from typing import Optional
from .models import WaterQualityStatus


class WaterQualityBase(BaseModel):
    site_name: str = Field(..., min_length=1, max_length=200)
    location: str = Field(..., min_length=1, max_length=300)
    sample_date: date

    ph: Optional[float] = Field(None, description="pH value")
    turbidity_ntu: Optional[float] = Field(None, description="Turbidity in NTU")
    dissolved_oxygen_mg_l: Optional[float] = Field(None, description="Dissolved oxygen (mg/L)")
    nitrates_mg_l: Optional[float] = Field(None, description="Nitrates (mg/L)")
    e_coli_count: Optional[int] = Field(None, description="E. coli count (CFU)")

    status: WaterQualityStatus = Field(..., description="Overall sample status")
    notes: Optional[str] = Field(None, max_length=1000)


class WaterQualityCreate(WaterQualityBase):
    """Schema for creating a new water quality sample"""
    pass


class WaterQualityUpdate(BaseModel):
    """Schema for updating a sample - all fields optional"""
    site_name: Optional[str] = Field(None, min_length=1, max_length=200)
    location: Optional[str] = Field(None, min_length=1, max_length=300)
    sample_date: Optional[date] = None

    ph: Optional[float] = None
    turbidity_ntu: Optional[float] = None
    dissolved_oxygen_mg_l: Optional[float] = None
    nitrates_mg_l: Optional[float] = None
    e_coli_count: Optional[int] = None

    status: Optional[WaterQualityStatus] = None
    notes: Optional[str] = Field(None, max_length=1000)


class WaterQualityResponse(WaterQualityBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WaterQualityListResponse(BaseModel):
    total: int
    samples: list[WaterQualityResponse]
