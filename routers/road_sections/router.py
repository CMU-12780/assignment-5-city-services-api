"""
RoadSection Router
FastAPI endpoints for road section inventory and pavement management
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database import get_db
from .models import ConditionRating, SurfaceType
from .schemas import (
    RoadSectionCreate,
    RoadSectionUpdate,
    RoadSectionResponse,
    RoadSectionListResponse,
)
from . import crud

router = APIRouter()


@router.get("/", response_model=RoadSectionListResponse)
def list_road_sections(
    skip: int = Query(
        0,
        ge=0,
        description="Number of records to skip for pagination",
    ),
    limit: int = Query(
        100,
        ge=1,
        le=500,
        description="Maximum number of records to return",
    ),
    condition_rating: Optional[ConditionRating] = Query(
        None,
        description="Filter by pavement condition rating",
    ),
    surface_type: Optional[SurfaceType] = Query(
        None,
        description="Filter by pavement surface type",
    ),
    search: Optional[str] = Query(
        None,
        description="Search by street name (case-insensitive)",
    ),
    db: Session = Depends(get_db),
) -> RoadSectionListResponse:
    """
    List road sections with optional filtering and search.

    - **skip**: Pagination offset
    - **limit**: Maximum number of results
    - **condition_rating**: Filter by pavement condition rating
    - **surface_type**: Filter by pavement surface type
    - **search**: Case-insensitive search in street_name
    """
    sections, total = crud.get_road_sections(
        db=db,
        skip=skip,
        limit=limit,
        condition_rating=condition_rating,
        surface_type=surface_type,
        search=search,
    )
    return RoadSectionListResponse(total=total, road_sections=sections)


@router.post(
    "/",
    response_model=RoadSectionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_road_section(
    section: RoadSectionCreate,
    db: Session = Depends(get_db),
) -> RoadSectionResponse:
    """
    Create a new road section.

    Provide all required fields including:
    - street_name, start_address, end_address
    - length_km, lanes_count
    - surface_type, condition_rating
    """
    return crud.create_road_section(db=db, section_data=section)


@router.get(
    "/{section_id}",
    response_model=RoadSectionResponse,
)
def get_road_section(
    section_id: int,
    db: Session = Depends(get_db),
) -> RoadSectionResponse:
    """
    Get a specific road section by ID.

    Returns detailed information about a single road section.
    """
    section = crud.get_road_section(db=db, section_id=section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Road section with id {section_id} not found",
        )
    return section


@router.put(
    "/{section_id}",
    response_model=RoadSectionResponse,
)
def update_road_section(
    section_id: int,
    section: RoadSectionUpdate,
    db: Session = Depends(get_db),
) -> RoadSectionResponse:
    """
    Update an existing road section.

    All fields are optional. Only provided fields will be updated.
    Use this to update condition rating, resurfacing date, or other attributes.
    """
    updated_section = crud.update_road_section(
        db=db,
        section_id=section_id,
        section_data=section,
    )
    if not updated_section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Road section with id {section_id} not found",
        )
    return updated_section


@router.delete(
    "/{section_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_road_section(
    section_id: int,
    db: Session = Depends(get_db),
) -> None:
    """
    Delete a road section by ID.

    Permanently removes a road section from the system.
    Returns 204 No Content on success.
    """
    deleted = crud.delete_road_section(db=db, section_id=section_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Road section with id {section_id} not found",
        )
    return None
