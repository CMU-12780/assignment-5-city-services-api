"""
Airquality CRUD operations
Database operations for air quality sensors
"""
from sqlalchemy.orm import Session
from typing import Optional, Tuple, List

from .models import Airquality
from .schemas import AirqualityCreate, AirqualityUpdate


def get_airquality(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> Tuple[List[Airquality], int]:
    """
    Get list of air quality sensors

    Args:
        db: Database session
        skip: Records to skip
        limit: Max number of records

    Returns:
        Tuple (list of sensors, total count)
    """
    query = db.query(Airquality)

    total = query.count()
    items = query.offset(skip).limit(limit).all()

    return items, total


def get_airquality_item(db: Session, item_id: int) -> Optional[Airquality]:
    """
    Get a specific air quality sensor by ID
    """
    return db.query(Airquality).filter(Airquality.id == item_id).first()


def create_airquality(db: Session, item_data: AirqualityCreate) -> Airquality:
    """
    Create a new air quality sensor record
    """
    item = Airquality(**item_data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_airquality(
    db: Session,
    item_id: int,
    item_data: AirqualityUpdate
) -> Optional[Airquality]:
    """
    Update an existing air quality sensor record
    """
    item = get_airquality_item(db, item_id)
    if not item:
        return None

    update_data = item_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


def delete_airquality(db: Session, item_id: int) -> bool:
    """
    Delete an air quality sensor record
    """
    item = get_airquality_item(db, item_id)
    if not item:
        return False

    db.delete(item)
    db.commit()
    return True
