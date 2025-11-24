"""
Public park Pydantic schemas for request/response validation
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class PublicParkBase(BaseModel):
    """Base public park schema with common fields"""

    park_name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Public park name",
    )
    address: str = Field(
        ...,
        min_length=1,
        max_length=300,
        description="Park address/location",
    )
    area_hectares: float = Field(
        ...,
        gt=0,
        description="Park size in hectares",
    )

    has_playground: bool = Field(
        default=False,
        description="Whether the park has a playground",
    )
    has_sports_fields: bool = Field(
        default=False,
        description="Whether the park has sports fields/courts",
    )
    has_restrooms: bool = Field(
        default=False,
        description="Whether the park has public restroom facilities",
    )

    daily_visitors_avg: Optional[int] = Field(
        default=None,
        ge=0,
        description="Average daily visitor count (non-negative)",
    )
    maintenance_frequency: Optional[str] = Field(
        default=None,
        max_length=100,
        description='Maintenance schedule, e.g. "weekly", "monthly"',
    )


class PublicParkCreate(PublicParkBase):
    """Schema for creating a new public park"""
    pass


class PublicParkUpdate(BaseModel):
    """Schema for updating a public park - all fields optional"""

    park_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
    )
    address: Optional[str] = Field(
        None,
        min_length=1,
        max_length=300,
    )
    area_hectares: Optional[float] = Field(
        None,
        gt=0,
    )

    has_playground: Optional[bool] = None
    has_sports_fields: Optional[bool] = None
    has_restrooms: Optional[bool] = None

    daily_visitors_avg: Optional[int] = Field(
        None,
        ge=0,
    )
    maintenance_frequency: Optional[str] = Field(
        None,
        max_length=100,
    )


class PublicParkResponse(PublicParkBase):
    """Schema for public park response"""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PublicParkListResponse(BaseModel):
    """Schema for list of public parks"""

    total: int
    parks: list[PublicParkResponse]
