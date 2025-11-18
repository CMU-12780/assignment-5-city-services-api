"""
RoadSection CRUD operations
Database operations for road sections
"""

from typing import Optional, Tuple, List

from sqlalchemy.orm import Session
from sqlalchemy import or_

from .models import RoadSection, ConditionRating, SurfaceType
from .schemas import RoadSectionCreate, RoadSectionUpdate


def get_road_sections(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    condition_rating: Optional[ConditionRating] = None,
    surface_type: Optional[SurfaceType] = None,
    search: Optional[str] = None,
) -> Tuple[List[RoadSection], int]:
    """
    Get list of road sections with optional filtering

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        condition_rating: Optional filter by pavement condition rating
        surface_type: Optional filter by pavement surface type
        search: Optional search term for street name

    Returns:
        Tuple of (list of road sections, total count)
    """
    query = db.query(RoadSection)

    if condition_rating:
        query = query.filter(RoadSection.condition_rating == condition_rating)

    if surface_type:
        query = query.filter(RoadSection.surface_type == surface_type)

    if search:
        search_term = f"%{search}%"
        query = query.filter(RoadSection.street_name.ilike(search_term))

    total = query.count()

    road_sections = query.offset(skip).limit(limit).all()

    return road_sections, total


def get_road_section(db: Session, section_id: int) -> Optional[RoadSection]:
    """
    Get a specific road section by ID

    Args:
        db: Database session
        section_id: RoadSection ID

    Returns:
        RoadSection object or None if not found
    """
    return (
        db.query(RoadSection)
        .filter(RoadSection.id == section_id)
        .first()
    )


def create_road_section(
    db: Session,
    section_data: RoadSectionCreate,
) -> RoadSection:
    """
    Create a new road section

    Args:
        db: Database session
        section_data: RoadSection creation data

    Returns:
        Created RoadSection object
    """
    section = RoadSection(**section_data.model_dump())
    db.add(section)
    db.commit()
    db.refresh(section)
    return section


def update_road_section(
    db: Session,
    section_id: int,
    section_data: RoadSectionUpdate,
) -> Optional[RoadSection]:
    """
    Update an existing road section

    Args:
        db: Database session
        section_id: RoadSection ID
        section_data: RoadSection update data

    Returns:
        Updated RoadSection object or None if not found
    """
    section = get_road_section(db, section_id)
    if not section:
        return None

    update_data = section_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(section, field, value)

    db.commit()
    db.refresh(section)
    return section


def delete_road_section(db: Session, section_id: int) -> bool:
    """
    Delete a road section

    Args:
        db: Database session
        section_id: RoadSection ID

    Returns:
        True if deleted, False if not found
    """
    section = get_road_section(db, section_id)
    if not section:
        return False

    db.delete(section)
    db.commit()
    return True
