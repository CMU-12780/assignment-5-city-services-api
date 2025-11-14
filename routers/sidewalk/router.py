from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database import get_db
from typing import Optional
from . import crud, schemas
from .models import SidewalkCondition

router = APIRouter()

@router.get("/", response_model=schemas.YourResourceListResponse)
def list_resources(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    condition: Optional[SidewalkCondition] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    sidewalks, total = crud.get_resources(db=db, skip=skip, limit=limit, condition=condition, search=search)
    return schemas.YourResourceListResponse(total=total, resources=sidewalks)

@router.post("/", response_model=schemas.YourResourceResponse, status_code=status.HTTP_201_CREATED)
def create_resource(resource: schemas.YourResourceCreate, db: Session = Depends(get_db)):
    return crud.create_resource(db=db, resource_data=resource)

@router.get("/{resource_id}", response_model=schemas.YourResourceResponse)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = crud.get_resource(db=db, resource_id=resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail=f"Sidewalk {resource_id} not found")
    return resource

@router.put("/{resource_id}", response_model=schemas.YourResourceResponse)
def update_resource(resource_id: int, resource: schemas.YourResourceUpdate, db: Session = Depends(get_db)):
    updated_resource = crud.update_resource(db=db, resource_id=resource_id, resource_data=resource)
    if not updated_resource:
        raise HTTPException(status_code=404, detail=f"Sidewalk {resource_id} not found")
    return updated_resource

@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_resource(db=db, resource_id=resource_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Sidewalk {resource_id} not found")
    return None
