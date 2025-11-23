from sqlalchemy import Column, String, Float, Date, Integer
from models.base import BaseModel

class Crosswalks(BaseModel):
    __tablename__ = "crosswalks"
    
    # Add your fields here
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    width_meters = Column(Float, nullable=False)
    condition = Column(String, nullable=False)
    last_inspection_date = Column(Date, nullable=True)
    year_created = Column(String, nullable=True)