"""
Pothole Router
FastAPI endpoints for pothole management
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from .models import PotholeSeverity, PotholeRepairStatus
from .schemas import PotholeCreate, PotholeUpdate, PotholeResponse, PotholeListResponse
from . import crud

router = APIRouter()


@router.get("/", response_model=PotholeListResponse)
def list_potholes(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum records to return"),
    severity: Optional[PotholeSeverity] = Query(None, description="Filter by severity"),
    repair_status: Optional[PotholeRepairStatus] = Query(None, description="Filter by repair status"),
    search: Optional[str] = Query(None, description="Search in location (case-insensitive)"),
    db: Session = Depends(get_db),
):
    """
    List all potholes with optional filtering
    - **skip**: Pagination offset
    - **limit**: Maximum number of results
    - **severity**: Filter by severity (minor, moderate, severe)
    - **repair_status**: Filter by repair status (reported, scheduled, in_progress, completed)
    - **search**: Search term for location (case-insensitive)
    """
    potholes, total = crud.get_potholes(
        db=db,
        skip=skip,
        limit=limit,
        severity=severity,
        repair_status=repair_status,
        search=search,
    )
    return PotholeListResponse(total=total, potholes=potholes)


@router.post("/", response_model=PotholeResponse, status_code=status.HTTP_201_CREATED)
def create_pothole(
    pothole: PotholeCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new pothole report
    Provide all required pothole information including:
    - Location
    - Reported date
    - Severity
    - Size
    - Initial repair status
    """
    return crud.create_pothole(db=db, pothole_data=pothole)


@router.get("/{pothole_id}", response_model=PotholeResponse)
def get_pothole(
    pothole_id: int,
    db: Session = Depends(get_db),
):
    pothole = crud.get_pothole(db=db, pothole_id=pothole_id)
    if not pothole:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pothole with id {pothole_id} not found",
        )
    return pothole


@router.put("/{pothole_id}", response_model=PotholeResponse)
def update_pothole(
    pothole_id: int,
    pothole: PotholeUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing pothole
    All fields are optional - only provided fields will be updated.
    """
    updated_pothole = crud.update_pothole(db=db, pothole_id=pothole_id, pothole_data=pothole)
    if not updated_pothole:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pothole with id {pothole_id} not found",
        )
    return updated_pothole


@router.delete("/{pothole_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pothole(
    pothole_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a pothole
    Permanently removes a pothole from the system.
    Returns 204 No Content on success.
    """
    deleted = crud.delete_pothole(db=db, pothole_id=pothole_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pothole with id {pothole_id} not found",
        )
    return None