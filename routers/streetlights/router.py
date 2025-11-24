"""
Streetlight Router
FastAPI endpoints for streetlight management
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from .models import LightType
from .schemas import StreetlightCreate, StreetlightUpdate, StreetlightResponse, StreetlightListResponse
from . import crud

router = APIRouter()


@router.get("/", response_model=StreetlightListResponse)
def list_streetlights(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum records to return"),
    light_type: Optional[LightType] = Query(None, description="Filter by light type"),
    is_operational: Optional[bool] = Query(None, description="Filter by condition status"),
    search: Optional[str] = Query(None, description="Search in name or location"),
    db: Session = Depends(get_db)
):
    """
    List all streetlights with optional filtering
    - **skip**: Pagination offset
    - **limit**: Maximum number of results
    - **light_type**: Filter by light type (LED, Sodium, Halogen)
    - **is_operational**: Filter by condition status
    - **search**: Search term for name or location (case-insensitive)
    """
    streetlights, total = crud.get_streetlights(
        db=db,
        skip=skip,
        limit=limit,
        light_type=light_type,
        is_operational=is_operational,
        search=search
    )
    return StreetlightListResponse(total=total, streetlights=streetlights)


@router.post("/", response_model=StreetlightResponse, status_code=status.HTTP_201_CREATED)
def create_streetlight(
    streetlight: StreetlightCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new streetlight
    Provide all required streetlight information including:
    - Name and location
    - Physical dimensions (length, width)
    - Load rating
    - Current condition
    """
    return crud.create_streetlight(db=db, streetlight_data=streetlight)


@router.get("/{streetlight_id}", response_model=StreetlightResponse)
def get_streetlight(
    streetlight_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific streetlight by ID
    Returns detailed information about a single streetlight.
    """
    streetlight = crud.get_streetlight(db=db, streetlight_id=streetlight_id)
    if not streetlight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Streetlight with id {streetlight_id} not found"
        )
    return streetlight


@router.put("/{streetlight_id}", response_model=StreetlightResponse)
def update_streetlight(
    streetlight_id: int,
    streetlight: StreetlightUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing streetlight
    All fields are optional - only provided fields will be updated.
    Use this to update descriptions, condition ratings, or any other streetlight information.
    """
    updated_streetlight = crud.update_streetlight(db=db, streetlight_id=streetlight_id, streetlight_data=streetlight)
    if not updated_streetlight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Streetlight with id {streetlight_id} not found"
        )
    return updated_streetlight


@router.delete("/{streetlight_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_streetlight(
    streetlight_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a streetlight
    Permanently removes a streetlight from the system.
    Returns 204 No Content on success.
    """
    deleted = crud.delete_streetlight(db=db, streetlight_id=streetlight_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Streetlight with id {streetlight_id} not found"
        )
    return None
