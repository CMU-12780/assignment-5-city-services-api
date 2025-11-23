"""
Crosswalk CRUD operations
Database operations for crosswalks
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from .models import Crosswalks
from .schemas import CrosswalkCreate, CrosswalkUpdate


def get_crosswalks(db: Session, skip: int = 0, limit: int = 100):
    query = db.query(Crosswalks)
    
    total = query.count()
    
    crosswalks = query.offset(skip).limit(limit).all()
    
    return crosswalks, total


def get_crosswalk(db: Session, crosswalk_id: int):
    return db.query(Crosswalks).filter(Crosswalks.id == crosswalk_id).first()


def create_crosswalk(db: Session, crosswalk_data: CrosswalkCreate):
    db_crosswalk = Crosswalks(**crosswalk_data.model_dump())
    
    db.add(db_crosswalk)
    db.commit()
    db.refresh(db_crosswalk)
    return db_crosswalk


def update_crosswalk(db: Session, crosswalk_id: int, crosswalk_data: CrosswalkUpdate):
    db_crosswalk = get_crosswalk(db, crosswalk_id)
    if not db_crosswalk:
        return None

    update_data = crosswalk_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_crosswalk, field, value)

    db.commit()
    db.refresh(db_crosswalk)
    return db_crosswalk


def delete_crosswalk(db: Session, crosswalk_id: int):
    db_crosswalk = get_crosswalk(db, crosswalk_id)
    if not db_crosswalk:
        return False

    db.delete(db_crosswalk)
    db.commit()
    return True