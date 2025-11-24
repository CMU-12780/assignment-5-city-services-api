"""
Public Park Router
FastAPI endpoints for public park management
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from .schemas import (
    PublicParkCreate,
    PublicParkUpdate,
    PublicParkResponse,
    PublicParkListResponse
)
from . import crud

router = APIRouter()

@router.get("/", response_model=PublicParkListResponse)
def list_public_parks(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records to return"),
    has_playground: Optional[bool] = Query(
        None,
        description="Filter by presence of playground"
    ),
    has_sports_fields: Optional[bool] = Query(
        None,
        description="Filter by presence of sports fields"
    ),
    has_restrooms: Optional[bool] = Query(
        None,
        description="Filter by presence of restrooms"
    ),
    search: Optional[str] = Query(
        None,
        description="Search by park name or address (case-insensitive)"
    ),
    db: Session = Depends(get_db)
):
    """
    List all public parks with optional filtering.

    - **skip**: Pagination offset  
    - **limit**: Maximum number of results  
    - **has_playground**: Filter parks with playgrounds  
    - **has_sports_fields**: Filter parks with sports fields  
    - **has_restrooms**: Filter parks with restroom facilities  
    - **search**: Search term for park_name or address  
    """
    parks, total = crud.get_public_parks(
        db=db,
        skip=skip,
        limit=limit,
        has_playground=has_playground,
        has_sports_fields=has_sports_fields,
        has_restrooms=has_restrooms,
        search=search
    )
    return PublicParkListResponse(total=total, parks=parks)


@router.post(
    "/",
    response_model=PublicParkResponse,
    status_code=status.HTTP_201_CREATED
)
def create_public_park(
    park: PublicParkCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new public park.

    Provide key park information including:
    - Park name and address  
    - Size in hectares  
    - Available amenities (playground, sports fields, restrooms)  
    - Optional visitor statistics and maintenance frequency  
    """
    return crud.create_public_park(db=db, park_data=park)


@router.get("/{park_id}", response_model=PublicParkResponse)
def get_public_park(
    park_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific public park by ID.
    Returns detailed information about a single park.
    """
    park = crud.get_public_park(db=db, park_id=park_id)
    if not park:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Public park with id {park_id} not found"
        )
    return park


@router.put("/{park_id}", response_model=PublicParkResponse)
def update_public_park(
    park_id: int,
    park: PublicParkUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing public park.

    All fields are optional.
    Only provided fields will be updated.
    Useful for updating amenities, visitor counts,
    or maintenance schedules.
    """
    updated_park = crud.update_public_park(
        db=db,
        park_id=park_id,
        park_data=park
    )
    if not updated_park:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Public park with id {park_id} not found"
        )
    return updated_park


@router.delete("/{park_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_public_park(
    park_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a public park.

    Permanently removes the park from the system.
    Returns **204 No Content** on success.
    """
    deleted = crud.delete_public_park(db=db, park_id=park_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Public park with id {park_id} not found"
        )
    return None
