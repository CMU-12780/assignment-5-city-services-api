"""
Building permit Pydantic schemas
"""
from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional
from .models import PermitType, PermitStatus


class BuildingPermitBase(BaseModel):
    permit_number: str = Field(..., min_length=1, max_length=50, description="Unique permit number")
    address: str = Field(..., min_length=1, max_length=300, description="Property address")
    permit_type: PermitType
    status: PermitStatus = PermitStatus.PENDING
    issue_date: Optional[date] = None
    expiration_date: Optional[date] = None
    estimated_cost: float = Field(..., ge=0, description="Estimated project cost")
    notes: Optional[str] = None


class BuildingPermitCreate(BuildingPermitBase):
    """Schema for creating a new building permit"""
    pass


class BuildingPermitUpdate(BaseModel):
    """Schema for updating an existing building permit"""
    permit_number: Optional[str] = None
    address: Optional[str] = None
    permit_type: Optional[PermitType] = None
    status: Optional[PermitStatus] = None
    issue_date: Optional[date] = None
    expiration_date: Optional[date] = None
    estimated_cost: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None


class BuildingPermitResponse(BuildingPermitBase):
    """Schema for building permit response"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BuildingPermitListResponse(BaseModel):
    total: int
    permits: list[BuildingPermitResponse]
