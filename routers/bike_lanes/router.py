from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from typing import Optional

from .models import BikeLaneCondition, BikeLaneType
from .schemas import BikeLaneCreate, BikeLaneUpdate, BikeLaneResponse, BikeLaneListResponse
from . import crud

router = APIRouter()

@router.get("/", response_model=BikeLaneListResponse)
def list_lanes(skip: int = Query(0, ge=0, description="Number of records to skip"),
               limit: int = Query(100, ge=1, le=500, description="Maximum records to return"),
               condition: Optional[BikeLaneCondition] = Query(None, description="Filter by surface condition"),
               lane_type: Optional[BikeLaneType] = Query(None, description="Filter by lane type"),
               search: Optional[str] = Query(None, description="Search in street name or locations"),
               db: Session = Depends(get_db)):
    bike_lanes, total = crud.get_lanes(
        db=db,
        skip=skip,
        limit=limit,
        condition=condition,
        lane_type=lane_type,
        search=search
    )
    return BikeLaneListResponse(total=total, resources=bike_lanes)
    # GET all resources
    

@router.post("/", response_model = BikeLaneResponse, status_code=status.HTTP_201_CREATED)
def create_lane(
    bike_lane: BikeLaneCreate,
    db: Session = Depends(get_db)):
    # POST new resource
    return crud.create_lane(db=db, bike_lane_data=bike_lane)

@router.get("/{bike_lane_id}", response_model=BikeLaneResponse)
def get_bike_lane(bike_lane_id: int
                  , db: Session = Depends(get_db)
                  ):
    # GET single resource
    bike_lane = crud.get_lane(db=db, bike_lane_id = bike_lane_id)
    if not bike_lane:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
            , detail=f"Bike lane with id {bike_lane_id} not found")
    
    return bike_lane

@router.put("/{bike_lane_id}")
def update_resource(bike_lane_id: int,
                    bike_lane_update: BikeLaneUpdate,
                    db: Session = Depends(get_db)):
    # PUT update resource
    updated_bike_lane = crud.update_lane(
        db=db, bike_lane_id=bike_lane_id, bike_lane_data=bike_lane_update)
    if not updated_bike_lane:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bike lane with id {bike_lane_id} not found"
        )  
    return updated_bike_lane

@router.delete("/{bike_lane_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bike_lane(bike_lane_id: int, 
                     db: Session = Depends(get_db)):
    # DELETE resource
    deleted = crud.delete_lane(db=db, bike_lane_id=bike_lane_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bike lane with id {bike_lane_id} not found"
        )
    return None