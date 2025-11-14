from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from .models import YourResource, SidewalkCondition
from .schemas import YourResourceCreate, YourResourceUpdate

def get_resources(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    condition: Optional[SidewalkCondition] = None,
    search: Optional[str] = None
):
    query = db.query(YourResource)
    if condition:
        query = query.filter(YourResource.condition == condition)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                YourResource.name.ilike(search_term),
                YourResource.location.ilike(search_term),
            )
        )
    total = query.count()
    resources = query.offset(skip).limit(limit).all()
    return resources, total

def get_resource(db: Session, resource_id: int) -> Optional[YourResource]:
    return db.query(YourResource).filter(YourResource.id == resource_id).first()

def create_resource(db: Session, resource_data: YourResourceCreate) -> YourResource:
    resource = YourResource(**resource_data.model_dump())
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource

def update_resource(db: Session, resource_id: int, resource_data: YourResourceUpdate):
    resource = get_resource(db, resource_id)
    if not resource:
        return None
    update_data = resource_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(resource, field, value)
    db.commit()
    db.refresh(resource)
    return resource

def delete_resource(db: Session, resource_id: int):
    resource = get_resource(db, resource_id)
    if not resource:
        return False
    db.delete(resource)
    db.commit()
    return True
