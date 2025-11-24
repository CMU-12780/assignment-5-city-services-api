"""
Sidewalk CRUD operations
Database operations for sidewalks
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from .models import Sidewalk, SidewalkCondition
from .schemas import SidewalkCreate, SidewalkUpdate


def get_sidewalks(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    condition: Optional[SidewalkCondition] = None,
    ada_compliant: Optional[bool] = None,
    search: Optional[str] = None
) -> tuple[list[Sidewalk], int]:
    """
    Get list of sidewalks with optional filtering
    """
    query = db.query(Sidewalk)

    # Apply filters
    if condition:
        query = query.filter(Sidewalk.condition == condition)

    if ada_compliant is not None:
        query = query.filter(Sidewalk.ada_compliant == ada_compliant)

    if search:
        search_term = f"%{search}%"
        query = query.filter(Sidewalk.street_name.ilike(search_term))

    total = query.count()
    sidewalks = query.offset(skip).limit(limit).all()
    return sidewalks, total


def get_sidewalk(db: Session, sidewalk_id: int) -> Optional[Sidewalk]:
    """Get a specific sidewalk by ID"""
    return db.query(Sidewalk).filter(Sidewalk.id == sidewalk_id).first()


def create_sidewalk(db: Session, data: SidewalkCreate) -> Sidewalk:
    """Create a new sidewalk"""
    sidewalk = Sidewalk(**data.model_dump())
    db.add(sidewalk)
    db.commit()
    db.refresh(sidewalk)
    return sidewalk


def update_sidewalk(db: Session, sidewalk_id: int, data: SidewalkUpdate) -> Optional[Sidewalk]:
    """Update an existing sidewalk"""
    sidewalk = get_sidewalk(db, sidewalk_id)
    if not sidewalk:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(sidewalk, field, value)

    db.commit()
    db.refresh(sidewalk)
    return sidewalk


def delete_sidewalk(db: Session, sidewalk_id: int) -> bool:
    """Delete a sidewalk"""
    sidewalk = get_sidewalk(db, sidewalk_id)
    if not sidewalk:
        return False

    db.delete(sidewalk)
    db.commit()
    return True
