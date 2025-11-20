
from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional


class AirqualityBase(BaseModel):
    """Base schema for air quality sensors with common fields"""
    name: str = Field(..., min_length=1, max_length=200, description="Sensor name or label")
    location: str = Field(..., min_length=1, max_length=300, description="Sensor installation location")
    pollutant_type: str = Field(..., min_length=1, max_length=100, description="Primary pollutant measured (e.g., PM2.5, CO2)")
    units: Optional[str] = Field(None, max_length=50, description="Measurement units (e.g., µg/m³, ppm)")
    sensing_technology: Optional[str] = Field(None, max_length=200, description="Sensor technology (e.g., laser, NDIR)")
    calibration_date: Optional[date] = Field(None, description="Last calibration date")
    sampling_interval: Optional[int] = Field(None, ge=1, description="Sampling interval in seconds")
    status: Optional[str] = Field(None, max_length=50, description="Sensor status (active, offline, failed)")


class AirqualityCreate(AirqualityBase):
    """Schema for creating a new air quality sensor"""
    pass


class AirqualityUpdate(BaseModel):
    """Schema for updating an air quality sensor — all fields optional"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    location: Optional[str] = Field(None, min_length=1, max_length=300)
    pollutant_type: Optional[str] = Field(None, min_length=1, max_length=100)
    units: Optional[str] = Field(None, max_length=50)
    sensing_technology: Optional[str] = Field(None, max_length=200)
    calibration_date: Optional[date] = None
    sampling_interval: Optional[int] = Field(None, ge=1)
    status: Optional[str] = Field(None, max_length=50)


class AirqualityResponse(AirqualityBase):
    """Schema returned when reading air quality sensor data"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AirqualityListResponse(BaseModel):
    """Schema for list view response"""
    total: int
    resources: list[AirqualityResponse]
