from sqlalchemy import Column, String, Integer, Boolean, Date, Enum as SQLEnum
from models.base import BaseModel
import enum

class SignalType(str, enum.Enum):
    STANDARD = "standard"
    PEDESTRIAN = "pedestrian"
    BICYCLE = "bicycle"

class TrafficSignal(BaseModel):
    """
    Traffic Signal infrastructure model
    Tracks traffic signal details and maintenance
    """
    __tablename__ = "traffic_signals"

    intersection_name = Column(String, nullable=False, index=True)
    location = Column(String, nullable=False)
    signal_type = Column(SQLEnum(SignalType), nullable=False)
    cycle_length_seconds = Column(Integer, nullable=False)
    last_maintenance = Column(Date, nullable=True)
    next_maintenance = Column(Date, nullable=True)
    malfunction_count = Column(Integer, default=0)
    has_turn_arrow = Column(Boolean, default=False)

    def __repr__(self):
        return f"<TrafficSignal(id={self.id}, intersection_name='{self.intersection_name}', signal_type='{self.signal_type}')>"
