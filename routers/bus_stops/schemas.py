"""
Bus Stop Pydantic schemas for request/response validation
"""
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BusStopBase(BaseModel):
    """Base bus stop schema with common fields"""
    stop_id: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Unique stop identifier",
    )
    location: str = Field(
        ...,
        min_length=1,
        max_length=300,
        description="Street address or intersection",
    )
    routes_served: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description='Route numbers served by this stop, e.g. "1, 5, 22"',
    )

    has_shelter: bool = Field(
        False,
        description="Whether the stop has a shelter",
    )
    has_bench: bool = Field(
        False,
        description="Whether the stop has a bench",
    )
    has_lighting: bool = Field(
        False,
        description="Whether the stop has lighting",
    )

    daily_boardings_avg: Optional[int] = Field(
        None,
        ge=0,
        description="Average number of daily boardings (non-negative)",
    )
    last_maintenance: Optional[date] = Field(
        None,
        description="Date of last maintenance at this stop",
    )


class BusStopCreate(BusStopBase):
    """Schema for creating a new bus stop"""
    pass


class BusStopUpdate(BaseModel):
    """Schema for updating a bus stop - all fields optional"""
    stop_id: Optional[str] = Field(None, min_length=1, max_length=50)
    location: Optional[str] = Field(None, min_length=1, max_length=300)
    routes_served: Optional[str] = Field(None, min_length=1, max_length=200)

    has_shelter: Optional[bool] = None
    has_bench: Optional[bool] = None
    has_lighting: Optional[bool] = None

    daily_boardings_avg: Optional[int] = Field(None, ge=0)
    last_maintenance: Optional[date] = None


class BusStopResponse(BusStopBase):
    """Schema for bus stop response"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BusStopListResponse(BaseModel):
    """Schema for list of bus stops"""
    total: int
    bus_stops: list[BusStopResponse]
