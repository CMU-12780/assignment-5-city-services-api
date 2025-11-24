"""
Streetlight CRUD operations
Database operations for streetlights
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from .models import Streetlight, LightType
from .schemas import StreetlightCreate, StreetlightUpdate


def get_streetlights(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    light_type: Optional[LightType] = None,
    is_operational: Optional[bool] = None,
    search: Optional[str] = None,
) -> tuple[int, list[Streetlight], int]:
    """
    Get list of streetlights with optional filtering

    Args:
        db: Database session
        skip: Number of records to skip
        light_type: Filter by enum type of lights
        is_operational: Filter by condition of streetlight
        search: Search term for pole_id or location

    Returns:
        Tuple of (list of streetlights, total count)
    """
    query = db.query(Streetlight)

    # Apply filters
    if light_type:
        query = query.filter(Streetlight.light_type == light_type)

    if is_operational:
        query = query.filter(Streetlight.is_operational == is_operational)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Streetlight.pole_id.ilike(search_term),
                Streetlight.location.ilike(search_term)
            )
        )

    # Get total count before pagination
    total = query.count()

    # Apply pagination and get results
    streetlights = query.offset(skip).limit(limit).all()

    return streetlights, total


def get_streetlight(db: Session, streetlight_id: int) -> Optional[Streetlight]:
    """
    Get a specific streetlight by ID

    Args:
        db: Database session
        streetlight_id: Streetlight ID

    Returns:
        Streetlight object or None if not found
    """
    return db.query(Streetlight).filter(Streetlight.id == streetlight_id).first()


def create_streetlight(db: Session, streetlight_data: StreetlightCreate) -> Streetlight:
    """
    Create a new streetlight

    Args:
        db: Database session
        streetlight_data: Streetlight creation data

    Returns:
        Created streetlight object
    """
    streetlight = Streetlight(**streetlight_data.model_dump())
    db.add(streetlight)
    db.commit()
    db.refresh(streetlight)
    return streetlight


def update_streetlight(
    db: Session,
    streetlight_id: int,
    streetlight_data: StreetlightUpdate
) -> Optional[Streetlight]:
    """
    Update an existing streetlight

    Args:
        db: Database session
        streetlight_id: Streetlight ID
        streetlight_data: Streetlight update data

    Returns:
        Updated streetlight object or None if not found
    """
    streetlight = get_streetlight(db, streetlight_id)
    if not streetlight:
        return None

    # Update only provided fields
    update_data = streetlight_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(streetlight, field, value)

    db.commit()
    db.refresh(streetlight)
    return streetlight


def delete_streetlight(db: Session, streetlight_id: int) -> bool:
    """
    Delete a streetlight

    Args:
        db: Database session
        streetlight_id: Streetlight ID

    Returns:
        True if deleted, False if not found
    """
    streetlight = get_streetlight(db, streetlight_id)
    if not streetlight:
        return False

    db.delete(streetlight)
    db.commit()
    return True
