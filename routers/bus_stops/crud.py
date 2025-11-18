"""
Bus Stop CRUD operations
Database operations for bus stops
"""
from typing import Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from .models import BusStop
from .schemas import BusStopCreate, BusStopUpdate


def get_bus_stops(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    has_shelter: Optional[bool] = None,
    has_bench: Optional[bool] = None,
    has_lighting: Optional[bool] = None,
    search: Optional[str] = None,
) -> tuple[list[BusStop], int]:
    """
    Get list of bus stops with optional filtering

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        has_shelter: Filter by presence of shelter
        has_bench: Filter by presence of bench
        has_lighting: Filter by presence of lighting
        search: Search term for stop_id or location

    Returns:
        Tuple of (list of bus stops, total count)
    """
    query = db.query(BusStop)

    # Apply amenity filters
    if has_shelter is not None:
        query = query.filter(BusStop.has_shelter == has_shelter)

    if has_bench is not None:
        query = query.filter(BusStop.has_bench == has_bench)

    if has_lighting is not None:
        query = query.filter(BusStop.has_lighting == has_lighting)

    # Apply search filter
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                BusStop.stop_id.ilike(search_term),
                BusStop.location.ilike(search_term),
            )
        )

    # Get total count before pagination
    total = query.count()

    # Apply pagination and get results
    bus_stops = query.offset(skip).limit(limit).all()

    return bus_stops, total


def get_bus_stop(db: Session, bus_stop_id: int) -> Optional[BusStop]:
    """
    Get a specific bus stop by ID

    Args:
        db: Database session
        bus_stop_id: Bus stop ID

    Returns:
        BusStop object or None if not found
    """
    return db.query(BusStop).filter(BusStop.id == bus_stop_id).first()


def create_bus_stop(db: Session, bus_stop_data: BusStopCreate) -> BusStop:
    """
    Create a new bus stop

    Args:
        db: Database session
        bus_stop_data: Bus stop creation data

    Returns:
        Created BusStop object
    """
    bus_stop = BusStop(**bus_stop_data.model_dump())
    db.add(bus_stop)
    db.commit()
    db.refresh(bus_stop)
    return bus_stop


def update_bus_stop(
    db: Session,
    bus_stop_id: int,
    bus_stop_data: BusStopUpdate,
) -> Optional[BusStop]:
    """
    Update an existing bus stop

    Args:
        db: Database session
        bus_stop_id: Bus stop ID
        bus_stop_data: Bus stop update data

    Returns:
        Updated BusStop object or None if not found
    """
    bus_stop = get_bus_stop(db, bus_stop_id)
    if not bus_stop:
        return None

    # Update only provided fields
    update_data = bus_stop_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(bus_stop, field, value)

    db.commit()
    db.refresh(bus_stop)
    return bus_stop


def delete_bus_stop(db: Session, bus_stop_id: int) -> bool:
    """
    Delete a bus stop

    Args:
        db: Database session
        bus_stop_id: Bus stop ID

    Returns:
        True if deleted, False if not found
    """
    bus_stop = get_bus_stop(db, bus_stop_id)
    if not bus_stop:
        return False

    db.delete(bus_stop)
    db.commit()
    return True
