"""
Public park CRUD operations
Database operations for public parks
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .models import PublicPark
from .schemas import PublicParkCreate, PublicParkUpdate

def get_public_parks(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    has_playground: Optional[bool] = None,
    has_sports_fields: Optional[bool] = None,
    has_restrooms: Optional[bool] = None,
    search: Optional[str] = None,
) -> tuple[list[PublicPark], int]:
    """
    Get list of public parks with optional filtering and search.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        has_playground: Filter by presence of playground (True/False)
        has_sports_fields: Filter by presence of sports fields (True/False)
        has_restrooms: Filter by presence of restrooms (True/False)
        search: Search term for park_name or address

    Returns:
        Tuple of (list of public parks, total count)
    """
    query = db.query(PublicPark)

    # Apply amenity filters
    if has_playground is not None:
        query = query.filter(PublicPark.has_playground == has_playground)

    if has_sports_fields is not None:
        query = query.filter(
            PublicPark.has_sports_fields == has_sports_fields
        )

    if has_restrooms is not None:
        query = query.filter(PublicPark.has_restrooms == has_restrooms)

    # Apply search filter
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                PublicPark.park_name.ilike(search_term),
                PublicPark.address.ilike(search_term),
            )
        )

    # Get total count before pagination
    total = query.count()

    # Apply pagination and get results
    parks = query.offset(skip).limit(limit).all()

    return parks, total


def get_public_park(db: Session, park_id: int) -> Optional[PublicPark]:
    """
    Get a specific public park by ID.

    Args:
        db: Database session
        park_id: Public park ID

    Returns:
        PublicPark object or None if not found
    """
    return db.query(PublicPark).filter(PublicPark.id == park_id).first()


def create_public_park(
    db: Session,
    park_data: PublicParkCreate,
) -> PublicPark:
    """
    Create a new public park.

    Args:
        db: Database session
        park_data: Public park creation data

    Returns:
        Created PublicPark object
    """
    park = PublicPark(**park_data.model_dump())
    db.add(park)
    db.commit()
    db.refresh(park)
    return park


def update_public_park(
    db: Session,
    park_id: int,
    park_data: PublicParkUpdate,
) -> Optional[PublicPark]:
    """
    Update an existing public park.

    Args:
        db: Database session
        park_id: Public park ID
        park_data: Public park update data

    Returns:
        Updated PublicPark object or None if not found
    """
    park = get_public_park(db, park_id)
    if not park:
        return None

    # Update only provided fields
    update_data = park_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(park, field, value)

    db.commit()
    db.refresh(park)
    return park


def delete_public_park(db: Session, park_id: int) -> bool:
    """
    Delete a public park.

    Args:
        db: Database session
        park_id: Public park ID

    Returns:
        True if deleted, False if not found
    """
    park = get_public_park(db, park_id)
    if not park:
        return False

    db.delete(park)
    db.commit()
    return True
