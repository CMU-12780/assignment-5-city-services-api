from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from .models import BikeLane, BikeLaneCondition, BikeLaneType 
from .schemas import BikeLaneCreate, BikeLaneUpdate

def get_lanes(db: Session,
                   skip: int = 0, 
                   limit: int = 100,
                   condition: Optional[BikeLaneCondition] = None,
                   lane_type: Optional[BikeLaneType] = None,
                   search: Optional[str] = None) -> tuple[list[BikeLane], int]:
    # Implementation

    query = db.query(BikeLane)

    # Apply filters
    if condition:
        query = query.filter(BikeLane.surface_condition == condition)

    if lane_type:
        query = query.filter(BikeLane.lane_type == lane_type)  

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_ ( 
                BikeLane.street_name.ilike(search_term),
                BikeLane.start_location.ilike(search_term),
                BikeLane.end_location.ilike(search_term)
            )
        )
    
    # Get total count before pagination
    total = query.count()   
    # Apply pagination and get results
    lanes = query.offset(skip).limit(limit).all()

    return lanes, total

def get_lane(db: Session, bike_lane_id: int) -> Optional[BikeLane]:
    """
    Get a specific bike lane by ID

    Args:
        db: Database session
        bridge_id: Bike lane ID

    Returns:
        Bike lane object or None if not found
    """

    return db.query(BikeLane).filter(BikeLane.id == bike_lane_id).first()

def create_lane(db: Session, bike_lane_data: YourResourceCreate):
    # Implementation
    bike_lane = BikeLane(**bike_lane_data.model_dump())
    db.add(bike_lane)
    db.commit()
    db.refresh(bike_lane)
    return bike_lane

def update_lane(db: Session, bike_lane_id: int, bike_lane_data: YourResourceUpdate):
    bike_lane = get_lane(db, bike_lane_id)
    if not bike_lane:
        return None 
    
    # Update only provided fields

    update_data = bike_lane_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(bike_lane, field, value)

    db.commit()
    db.refresh(bike_lane)
    return bike_lane

def delete_lane(db: Session, bike_lane_id: int):
    bike_lane = get_lane(db, bike_lane_id)
    if not bike_lane:
        return None 
    
    db.delete(bike_lane)
    db.commit()
    return True