"""
Bus Stop database model
"""
from sqlalchemy import Column, String, Integer, Boolean, Date
from models.base import BaseModel


class BusStop(BaseModel):
    """
    Bus Stop infrastructure model
    Tracks physical amenities, ridership levels, and maintenance history
    """
    __tablename__ = "bus_stops"

    # Identification
    stop_id = Column(String, nullable=False, unique=True, index=True)
    location = Column(String, nullable=False)

    # Routes served
    routes_served = Column(String, nullable=False)  # e.g., "1, 5, 22"

    # Amenities
    has_shelter = Column(Boolean, nullable=False, default=False)
    has_bench = Column(Boolean, nullable=False, default=False)
    has_lighting = Column(Boolean, nullable=False, default=False)

    # Ridership & Maintenance
    daily_boardings_avg = Column(Integer, nullable=True)
    last_maintenance = Column(Date, nullable=True)

    def __repr__(self):
        return (
            f"<BusStop(id={self.id}, stop_id='{self.stop_id}', location='{self.location}')>"
        )
