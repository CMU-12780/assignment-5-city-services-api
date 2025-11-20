"""
CRUD operations for water quality samples
"""
from sqlalchemy.orm import Session
from typing import Optional
from .models import WaterQualitySample, WaterQualityStatus
from .schemas import WaterQualityCreate, WaterQualityUpdate
from sqlalchemy import or_


def get_samples(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    status: Optional[WaterQualityStatus] = None,
    search: Optional[str] = None
) -> tuple[list[WaterQualitySample], int]:
    """
    Retrieve water quality samples with optional filters
    """
    query = db.query(WaterQualitySample)

    if status:
        query = query.filter(WaterQualitySample.status == status)

    if start_date:
        query = query.filter(WaterQualitySample.sample_date >= start_date)

    if end_date:
        query = query.filter(WaterQualitySample.sample_date <= end_date)

    if search:
        term = f"%{search}%"
        query = query.filter(
            or_(
                WaterQualitySample.site_name.ilike(term),
                WaterQualitySample.location.ilike(term)
            )
        )

    total = query.count()
    samples = query.offset(skip).limit(limit).all()
    return samples, total


def get_sample(db: Session, sample_id: int) -> Optional[WaterQualitySample]:
    return db.query(WaterQualitySample).filter(WaterQualitySample.id == sample_id).first()


def create_sample(db: Session, sample_data: WaterQualityCreate) -> WaterQualitySample:
    sample = WaterQualitySample(**sample_data.model_dump())
    db.add(sample)
    db.commit()
    db.refresh(sample)
    return sample


def update_sample(db: Session, sample_id: int, sample_data: WaterQualityUpdate) -> Optional[WaterQualitySample]:
    sample = get_sample(db, sample_id)
    if not sample:
        return None

    update_data = sample_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(sample, field, value)

    db.commit()
    db.refresh(sample)
    return sample


def delete_sample(db: Session, sample_id: int) -> bool:
    sample = get_sample(db, sample_id)
    if not sample:
        return False
    db.delete(sample)
    db.commit()
    return True
