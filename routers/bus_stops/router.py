"""
Bus Stop Router
FastAPI endpoints for bus stop management
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database import get_db
from .schemas import (
    BusStopCreate,
    BusStopUpdate,
    BusStopResponse,
    BusStopListResponse,
)
from . import crud

router = APIRouter()


@router.get("/", response_model=BusStopListResponse)
def list_bus_stops(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum records to return"),
    has_shelter: Optional[bool] = Query(
        None,
        description="Filter by presence of shelter",
    ),
    has_bench: Optional[bool] = Query(
        None,
        description="Filter by presence of bench",
    ),
    has_lighting: Optional[bool] = Query(
        None,
        description="Filter by presence of lighting",
    ),
    search: Optional[str] = Query(
        None,
        description="Search in stop_id or location (case-insensitive)",
    ),
    db: Session = Depends(get_db),
):
    """
    List all bus stops with optional filtering
    - **skip**: Pagination offset
    - **limit**: Maximum number of results
    - **has_shelter**: Filter by presence of shelter
    - **has_bench**: Filter by presence of bench
    - **has_lighting**: Filter by presence of lighting
    - **search**: Search term for stop_id or location (case-insensitive)
    """
    bus_stops, total = crud.get_bus_stops(
        db=db,
        skip=skip,
        limit=limit,
        has_shelter=has_shelter,
        has_bench=has_bench,
        has_lighting=has_lighting,
        search=search,
    )
    return BusStopListResponse(total=total, bus_stops=bus_stops)


@router.post(
    "/",
    response_model=BusStopResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_bus_stop(
    bus_stop: BusStopCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new bus stop
    Provide all required bus stop information including:
    - Stop identifier (stop_id)
    - Location (address or intersection)
    - Routes served
    - Amenities (shelter, bench, lighting)
    - Ridership and maintenance data if available
    """
    return crud.create_bus_stop(db=db, bus_stop_data=bus_stop)


@router.get("/{bus_stop_id}", response_model=BusStopResponse)
def get_bus_stop(
    bus_stop_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a specific bus stop by ID
    Returns detailed information about a single bus stop.
    """
    bus_stop = crud.get_bus_stop(db=db, bus_stop_id=bus_stop_id)
    if not bus_stop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bus stop with id {bus_stop_id} not found",
        )
    return bus_stop


@router.put("/{bus_stop_id}", response_model=BusStopResponse)
def update_bus_stop(
    bus_stop_id: int,
    bus_stop: BusStopUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing bus stop
    All fields are optional - only provided fields will be updated.
    Use this to update amenities, ridership metrics, or maintenance information.
    """
    updated_bus_stop = crud.update_bus_stop(
        db=db,
        bus_stop_id=bus_stop_id,
        bus_stop_data=bus_stop,
    )
    if not updated_bus_stop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bus stop with id {bus_stop_id} not found",
        )
    return updated_bus_stop


@router.delete("/{bus_stop_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bus_stop(
    bus_stop_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a bus stop
    Permanently removes a bus stop from the system.
    Returns 204 No Content on success.
    """
    deleted = crud.delete_bus_stop(db=db, bus_stop_id=bus_stop_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bus stop with id {bus_stop_id} not found",
        )
    return None
