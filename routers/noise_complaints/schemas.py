
from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional
from .models import ComplaintCause
from .models import ComplaintStatus


class NoiseComplaintBase(BaseModel):
    name: str = Field(..., max_length=200)
    location: str = Field(..., max_length=300)
    reported_date: date
    time_of_day: str = Field(..., max_length=10)
    decibel_level: Optional[float] = None
    status: ComplaintStatus
    noise_source: ComplaintCause
    resolution_date: Optional[date] = None
    notes: Optional[str] = Field(None, max_length=1000)

class NoiseComplaintCreate(NoiseComplaintBase):
    pass

class NoiseComplaintUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    location: Optional[str] = Field(None, max_length=300)
    reported_date: Optional[date] = None
    time_of_day: Optional[str] = Field(None, max_length=10)
    decibel_level: Optional[float] = None
    status: Optional[ComplaintStatus] = None
    noise_source: Optional[ComplaintCause] = None
    resolution_date: Optional[date] = None
    notes: Optional[str] = Field(None, max_length=1000)


class NoiseComplaintResponse(NoiseComplaintBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class NoiseComplaintListResponse(BaseModel):
    total: int
    noise_complaints: list[NoiseComplaintResponse]

