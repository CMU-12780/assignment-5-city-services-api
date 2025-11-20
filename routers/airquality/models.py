from sqlalchemy import Column, String, Float, Date, Integer
from models.base import BaseModel

class Airquality(BaseModel):
    __tablename__ = "Airquality"
    
    # Add your fields here
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    pollutant_type = Column(String, nullable=False)     # "PM2.5, CO2"
    units = Column(String, nullable=True)               # "µg/m³, ppm"
    sensing_technology = Column(String, nullable=True)  # "laser", "NDIR", etc.
    calibration_date = Column(Date, nullable=True)
    sampling_interval = Column(Integer, nullable=True)
    status = Column(String, nullable=True)              # active / offline / failed
    


