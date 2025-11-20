"""
Traffic Signal CRUD operations
Database operations for traffic signals
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from .models import TrafficSignal, SignalType
from .schemas import TrafficSignalCreate, TrafficSignalUpdate

def get_traffic_signals(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    signal_type: Optional[SignalType] = None,
    search: Optional[str] = None
) -> tuple[list[TrafficSignal], int]:
    """
    Get list of traffic signals with optional filtering

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        signal_type: Filter by signal type
        search: Search term for intersection name

    Returns:
        Tuple of (list of traffic signals, total count)
    """
    query = db.query(TrafficSignal)

    if signal_type:
        query = query.filter(TrafficSignal.signal_type == signal_type)

    if search:
        search_term = f"%{search}%"
        query = query.filter(TrafficSignal.intersection_name.ilike(search_term))

    total = query.count()
    traffic_signals = query.offset(skip).limit(limit).all()

    return traffic_signals, total

def get_traffic_signal(db: Session, signal_id: int) -> Optional[TrafficSignal]:
    """
    Get a specific traffic signal by ID

    Args:
        db: Database session
        signal_id: Traffic Signal ID

    Returns:
        TrafficSignal object or None if not found
    """
    return db.query(TrafficSignal).filter(TrafficSignal.id == signal_id).first()

def create_traffic_signal(db: Session, signal_data: TrafficSignalCreate) -> TrafficSignal:
    """
    Create a new traffic signal

    Args:
        db: Database session
        signal_data: Traffic signal creation data

    Returns:
        Created traffic signal object
    """
    traffic_signal = TrafficSignal(**signal_data.model_dump())
    db.add(traffic_signal)
    db.commit()
    db.refresh(traffic_signal)
    return traffic_signal

def update_traffic_signal(
    db: Session,
    signal_id: int,
    signal_data: TrafficSignalUpdate
) -> Optional[TrafficSignal]:
    """
    Update an existing traffic signal

    Args:
        db: Database session
        signal_id: Traffic Signal ID
        signal_data: Traffic signal update data

    Returns:
        Updated traffic signal object or None if not found
    """
    traffic_signal = get_traffic_signal(db, signal_id)
    if not traffic_signal:
        return None

    update_data = signal_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(traffic_signal, field, value)

    db.commit()
    db.refresh(traffic_signal)
    return traffic_signal

def delete_traffic_signal(db: Session, signal_id: int) -> bool:
    """
    Delete a traffic signal

    Args:
        db: Database session
        signal_id: Traffic Signal ID

    Returns:
        True if deleted, False if not found
    """
    traffic_signal = get_traffic_signal(db, signal_id)
    if not traffic_signal:
        return False

    db.delete(traffic_signal)
    db.commit()
    return True
