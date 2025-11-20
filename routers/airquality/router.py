from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from . import crud
from .schemas import (
    AirqualityCreate,
    AirqualityUpdate,
    AirqualityResponse,
    AirqualityListResponse
)

router = APIRouter()

@router.get("/", response_model=AirqualityListResponse)
def list_airquality(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    items, total = crud.get_airquality(db=db, skip=skip, limit=limit)
    return AirqualityListResponse(total=total, resources=items)


@router.post("/", response_model=AirqualityResponse, status_code=status.HTTP_201_CREATED)
def create_airquality(
    sensor: AirqualityCreate,
    db: Session = Depends(get_db),
):
    return crud.create_airquality(db=db, item_data=sensor)


@router.get("/{sensor_id}", response_model=AirqualityResponse)
def get_airquality(
    sensor_id: int,
    db: Session = Depends(get_db),
):
    sensor = crud.get_airquality_item(db=db, item_id=sensor_id)
    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Airquality sensor with id {sensor_id} not found"
        )
    return sensor


@router.put("/{sensor_id}", response_model=AirqualityResponse)
def update_airquality(
    sensor_id: int,
    update_data: AirqualityUpdate,
    db: Session = Depends(get_db),
):
    updated_sensor = crud.update_airquality(db=db, item_id=sensor_id, item_data=update_data)
    if not updated_sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Airquality sensor with id {sensor_id} not found"
        )
    return updated_sensor


@router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_airquality(
    sensor_id: int,
    db: Session = Depends(get_db),
):
    deleted = crud.delete_airquality(db=db, item_id=sensor_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Airquality sensor with id {sensor_id} not found"
        )
    return None

