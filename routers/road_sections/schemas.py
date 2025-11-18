"""
RoadSection Pydantic schemas for request/response validation
"""

from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field

from .models import SurfaceType, ConditionRating


class RoadSectionBase(BaseModel):
    """Base schema with common RoadSection fields"""
    street_name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Street name of the road section",
    )
    start_address: str = Field(
        ...,
        min_length=1,
        max_length=300,
        description="Section start address or description",
    )
    end_address: str = Field(
        ...,
        min_length=1,
        max_length=300,
        description="Section end address or description",
    )
    length_km: float = Field(
        ...,
        gt=0,
        description="Length of the road section in kilometers",
    )
    lanes_count: int = Field(
        ...,
        ge=1,
        description="Number of lanes in this road section",
    )
    surface_type: SurfaceType = Field(
        ...,
        description="Pavement surface type",
    )
    condition_rating: ConditionRating = Field(
        ...,
        description="Current pavement condition rating",
    )
    last_resurfaced: Optional[date] = Field(
        None,
        description="Date of last resurfacing",
    )
    average_daily_traffic: Optional[int] = Field(
        None,
        ge=0,
        description="Average daily traffic volume (vehicles per day)",
    )


class RoadSectionCreate(RoadSectionBase):
    """Schema for creating a new RoadSection"""
    pass


class RoadSectionUpdate(BaseModel):
    """
    Schema for updating an existing RoadSection
    All fields are optional to support partial updates
    """
    street_name: Optional[str] = Field(None, min_length=1, max_length=200)
    start_address: Optional[str] = Field(None, min_length=1, max_length=300)
    end_address: Optional[str] = Field(None, min_length=1, max_length=300)
    length_km: Optional[float] = Field(None, gt=0)
    lanes_count: Optional[int] = Field(None, ge=1)
    surface_type: Optional[SurfaceType] = None
    condition_rating: Optional[ConditionRating] = None
    last_resurfaced: Optional[date] = None
    average_daily_traffic: Optional[int] = Field(None, ge=0)


class RoadSectionResponse(RoadSectionBase):
    """Schema for RoadSection responses"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RoadSectionListResponse(BaseModel):
    """Schema for a list of RoadSections with total count"""
    total: int
    road_sections: List[RoadSectionResponse]
