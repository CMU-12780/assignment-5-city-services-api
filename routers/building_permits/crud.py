"""
Building permits CRUD operations
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional

from .models import BuildingPermit, PermitType, PermitStatus
from .schemas import BuildingPermitCreate, BuildingPermitUpdate


def get_building_permits(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[PermitStatus] = None,
    permit_type: Optional[PermitType] = None,
    search: Optional[str] = None,
):
    query = db.query(BuildingPermit)

    if status is not None:
        query = query.filter(BuildingPermit.status == status)
    if permit_type is not None:
        query = query.filter(BuildingPermit.permit_type == permit_type)
    if search:
        like = f"%{search}%"
        query = query.filter(
            or_(
                BuildingPermit.permit_number.ilike(like),
                BuildingPermit.address.ilike(like),
            )
        )

    total = query.count()
    permits = query.offset(skip).limit(limit).all()
    return total, permits


def get_building_permit(db: Session, permit_id: int) -> Optional[BuildingPermit]:
    return db.query(BuildingPermit).filter(BuildingPermit.id == permit_id).first()


def get_building_permit_by_number(db: Session, permit_number: str) -> Optional[BuildingPermit]:
    return db.query(BuildingPermit).filter(BuildingPermit.permit_number == permit_number).first()


def create_building_permit(db: Session, permit: BuildingPermitCreate) -> BuildingPermit:
    db_permit = BuildingPermit(**permit.model_dump())
    db.add(db_permit)
    db.commit()
    db.refresh(db_permit)
    return db_permit


def update_building_permit(
    db: Session,
    permit_id: int,
    permit_update: BuildingPermitUpdate,
) -> Optional[BuildingPermit]:
    permit = get_building_permit(db, permit_id)
    if not permit:
        return None

    update_data = permit_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(permit, field, value)

    db.commit()
    db.refresh(permit)
    return permit


def delete_building_permit(db: Session, permit_id: int) -> bool:
    permit = get_building_permit(db, permit_id)
    if not permit:
        return False
    db.delete(permit)
    db.commit()
    return True
