"""
Pothole Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional
from .models import PotholeSeverity, PotholeRepairStatus


class PotholeBase(BaseModel):
    """Base pothole schema with common fields"""
    location: str = Field(..., min_length=1, max_length=300, description="Location/address of the pothole")
    reported_date: date = Field(..., description="Date when the pothole was reported")
    severity: PotholeSeverity = Field(..., description="Pothole severity rating")
    size_diameter_cm: float = Field(..., gt=0, description="Diameter of the pothole in centimeters")
    repair_status: PotholeRepairStatus = Field(..., description="Repair status of the pothole")
    repair_date: Optional[date] = Field(None, description="Date pothole was repaired (if applicable)")
    repair_cost: Optional[float] = Field(None, ge=0, description="Repair cost")
    notes: Optional[str] = Field(None, max_length=1000, description="Additional notes about the pothole")

class PotholeCreate(PotholeBase):
    """Schema for creating a new pothole"""
    pass

class PotholeUpdate(BaseModel):
    """Schema for updating a pothole - all fields optional"""
    location: Optional[str] = Field(None, min_length=1, max_length=300)
    reported_date: Optional[date] = None
    severity: Optional[PotholeSeverity] = None
    size_diameter_cm: Optional[float] = Field(None, gt=0)
    repair_status: Optional[PotholeRepairStatus] = None
    repair_date: Optional[date] = None
    repair_cost: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = Field(None, max_length=1000)

class PotholeResponse(PotholeBase):
    """Schema for pothole response"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PotholeListResponse(BaseModel):
    """Schema for list of potholes"""
    total: int
    potholes: list[PotholeResponse]