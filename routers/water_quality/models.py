"""
Water Quality database model
"""
from sqlalchemy import Column, String, Float, Date, Integer, Enum as SQLEnum
from models.base import BaseModel
import enum


class WaterQualityStatus(str, enum.Enum):
    """Sample status ratings"""
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    UNSAFE = "unsafe"


class WaterQualitySample(BaseModel):
    """
    Water quality sample model
    Tracks sensor/site samples and common water quality metrics
    """
    __tablename__ = "water_quality_samples"

    site_name = Column(String, nullable=False, index=True)
    location = Column(String, nullable=False)
    sample_date = Column(Date, nullable=False)

    # Chemistry / sensor measurements
    ph = Column(Float, nullable=True)
    turbidity_ntu = Column(Float, nullable=True)
    dissolved_oxygen_mg_l = Column(Float, nullable=True)
    nitrates_mg_l = Column(Float, nullable=True)
    e_coli_count = Column(Integer, nullable=True)

    status = Column(SQLEnum(WaterQualityStatus), nullable=False, default=WaterQualityStatus.GOOD)

    notes = Column(String, nullable=True)

    def __repr__(self):
        return f"<WaterQualitySample(id={self.id}, site='{self.site_name}', date={self.sample_date})>"
