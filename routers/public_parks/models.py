"""
Public park database model
"""
from sqlalchemy import Column, String, Float, Integer, Boolean
from models.base import BaseModel


class PublicPark(BaseModel):
    """
    Public park infrastructure model
    Tracks park facilities, amenities, and usage statistics
    """
    __tablename__ = "public_parks"

    # Basic Information
    park_name = Column(String, nullable=False, index=True)
    address = Column(String, nullable=False)

    # Size / Area
    area_hectares = Column(Float, nullable=False)

    # Amenities
    has_playground = Column(Boolean, nullable=False, default=False)
    has_sports_fields = Column(Boolean, nullable=False, default=False)
    has_restrooms = Column(Boolean, nullable=False, default=False)

    # Usage and Maintenance
    daily_visitors_avg = Column(Integer, nullable=True)
    maintenance_frequency = Column(String, nullable=True)

    def __repr__(self):
        return (
            f"<PublicPark(id={self.id}, "
            f"park_name='{self.park_name}', "
            f"area_hectares={self.area_hectares})>"
        )
