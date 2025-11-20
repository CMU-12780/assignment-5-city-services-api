"""
Traffic Signal Router
FastAPI endpoints for traffic signal management
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from .models import SignalType
from .schemas import TrafficSignalCreate, TrafficSignalUpdate, TrafficSignalResponse, TrafficSignalListResponse
from . import crud

router = APIRouter()

@router.get("/", response_model=TrafficSignalListResponse)
def list_traffic_signals(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum records to return"),
    signal_type: Optional[SignalType] = Query(None, description="Filter by signal type"),
    search: Optional[str] = Query(None, description="Search in intersection name"),
    db: Session = Depends(get_db)
):
    """
    List all traffic signals with optional filtering
    - **skip**: Pagination offset
    - **limit**: Maximum number of results
    - **signal_type**: Filter by signal type (standard, pedestrian, bicycle)
    - **search**: Search term for intersection name (case-insensitive)
    """
    traffic_signals, total = crud.get_traffic_signals(
        db=db,
        skip=skip,
        limit=limit,
        signal_type=signal_type,
        search=search
    )
    return TrafficSignalListResponse(total=total, traffic_signals=traffic_signals)

@router.post("/", response_model=TrafficSignalResponse, status_code=status.HTTP_201_CREATED)
def create_traffic_signal(
    traffic_signal: TrafficSignalCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new traffic signal
    Provide all required traffic signal information including:
    - Intersection name and location
    - Signal type
    - Cycle length
    """
    return crud.create_traffic_signal(db=db, signal_data=traffic_signal)

@router.get("/{signal_id}", response_model=TrafficSignalResponse)
def get_traffic_signal(
    signal_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific traffic signal by ID
    Returns detailed information about a single traffic signal.
    """
    traffic_signal = crud.get_traffic_signal(db=db, signal_id=signal_id)
    if not traffic_signal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Traffic signal with id {signal_id} not found"
        )
    return traffic_signal

@router.put("/{signal_id}", response_model=TrafficSignalResponse)
def update_traffic_signal(
    signal_id: int,
    traffic_signal: TrafficSignalUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing traffic signal
    All fields are optional - only provided fields will be updated.
    Use this to update maintenance dates, malfunction counts, or any other traffic signal information.
    """
    updated_signal = crud.update_traffic_signal(db=db, signal_id=signal_id, signal_data=traffic_signal)
    if not updated_signal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Traffic signal with id {signal_id} not found"
        )
    return updated_signal

@router.delete("/{signal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_traffic_signal(
    signal_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a traffic signal
    Permanently removes a traffic signal from the system.
    Returns 204 No Content on success.
    """
    deleted = crud.delete_traffic_signal(db=db, signal_id=signal_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Traffic signal with id {signal_id} not found"
        )
    return None
