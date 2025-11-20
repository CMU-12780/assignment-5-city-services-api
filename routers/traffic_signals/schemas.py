from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional
from .models import SignalType

class TrafficSignalBase(BaseModel):
    """Base traffic signal schema with common fields"""
    intersection_name: str = Field(..., min_length=1, max_length=200, description="Intersection name")
    location: str = Field(..., min_length=1, max_length=300, description="Full address")
    signal_type: SignalType = Field(..., description="Type of traffic signal")
    cycle_length_seconds: int = Field(..., gt=0, description="Total signal cycle time in seconds")
    last_maintenance: Optional[date] = Field(None, description="Last service date")
    next_maintenance: Optional[date] = Field(None, description="Scheduled maintenance date")
    malfunction_count: Optional[int] = Field(0, ge=0, description="Number of reported malfunctions")
    has_turn_arrow: Optional[bool] = Field(False, description="Dedicated turn signal present")

class TrafficSignalCreate(TrafficSignalBase):
    """Schema for creating a new traffic signal"""
    pass

class TrafficSignalUpdate(BaseModel):
    """Schema for updating a traffic signal - all fields optional"""
    intersection_name: Optional[str] = Field(None, min_length=1, max_length=200)
    location: Optional[str] = Field(None, min_length=1, max_length=300)
    signal_type: Optional[SignalType] = None
    cycle_length_seconds: Optional[int] = Field(None, gt=0)
    last_maintenance: Optional[date] = None
    next_maintenance: Optional[date] = None
    malfunction_count: Optional[int] = Field(None, ge=0)
    has_turn_arrow: Optional[bool] = None

class TrafficSignalResponse(TrafficSignalBase):
    """Schema for traffic signal response"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TrafficSignalListResponse(BaseModel):
    """Schema for list of traffic signals"""
    total: int
    traffic_signals: list[TrafficSignalResponse]
