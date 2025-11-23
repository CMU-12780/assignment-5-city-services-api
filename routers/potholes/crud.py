"""
Pothole CRUD operations
Database operations for potholes
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from .models import Pothole, PotholeSeverity, PotholeRepairStatus
from .schemas import PotholeCreate, PotholeUpdate


def get_potholes(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    severity: Optional[PotholeSeverity] = None,
    repair_status: Optional[PotholeRepairStatus] = None,
    search: Optional[str] = None
) -> tuple[list[Pothole], int]:
    """
    Get list of potholes with optional filtering

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        severity: Filter by pothole severity
        repair_status: Filter by repair status
        search: Search term for location

    Returns:
        Tuple of (list of potholes, total count)
    """
    query = db.query(Pothole)

    # Apply filters
    if severity:
        query = query.filter(Pothole.severity == severity)

    if repair_status:
        query = query.filter(Pothole.repair_status == repair_status)

    if search:
        search_term = f"%{search}%"
        query = query.filter(Pothole.location.ilike(search_term))

    # Get total count before pagination
    total = query.count()

    # Apply pagination and get results
    potholes = query.offset(skip).limit(limit).all()

    return potholes, total


def get_pothole(db: Session, pothole_id: int) -> Optional[Pothole]:
    """
    Get a specific pothole by ID

    Args:
        db: Database session
        pothole_id: Pothole ID

    Returns:
        Pothole object or None if not found
    """
    return db.query(Pothole).filter(Pothole.id == pothole_id).first()


def create_pothole(db: Session, pothole_data: PotholeCreate) -> Pothole:
    """
    Create a new pothole

    Args:
        db: Database session
        pothole_data: Pothole creation data

    Returns:
        Created pothole object
    """
    pothole = Pothole(**pothole_data.model_dump())
    db.add(pothole)
    db.commit()
    db.refresh(pothole)
    return pothole


def update_pothole(
    db: Session,
    pothole_id: int,
    pothole_data: PotholeUpdate
) -> Optional[Pothole]:
    """
    Update an existing pothole

    Args:
        db: Database session
        pothole_id: Pothole ID
        pothole_data: Pothole update data

    Returns:
        Updated pothole object or None if not found
    """
    pothole = get_pothole(db, pothole_id)
    if not pothole:
        return None

    # Update only provided fields
    update_data = pothole_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(pothole, field, value)

    db.commit()
    db.refresh(pothole)
    return pothole


def delete_pothole(db: Session, pothole_id: int) -> bool:
    """
    Delete a pothole

    Args:
        db: Database session
        pothole_id: Pothole ID

    Returns:
        True if deleted, False if not found
    """
    pothole = get_pothole(db, pothole_id)
    if not pothole:
        return False

    db.delete(pothole)
    db.commit()
    return True
