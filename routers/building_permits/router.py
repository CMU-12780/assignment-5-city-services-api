"""
Building permits router

"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from .models import PermitType, PermitStatus
from .schemas import (
    BuildingPermitCreate,
    BuildingPermitUpdate,
    BuildingPermitResponse,
    BuildingPermitListResponse,
)
from . import crud

router = APIRouter()


@router.get(
    "/",
    response_model=BuildingPermitListResponse,
    summary="List building permits",
)
def list_building_permits(
    skip: int = 0,
    limit: int = Query(100, le=1000),
    status: Optional[PermitStatus] = Query(None),
    permit_type: Optional[PermitType] = Query(None),
    search: Optional[str] = Query(None, description="Search by permit number or address"),
    db: Session = Depends(get_db),
):
    total, permits = crud.get_building_permits(
        db=db,
        skip=skip,
        limit=limit,
        status=status,
        permit_type=permit_type,
        search=search,
    )
    return BuildingPermitListResponse(total=total, permits=permits)


@router.post(
    "/",
    response_model=BuildingPermitResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_building_permit(
    permit: BuildingPermitCreate,
    db: Session = Depends(get_db),
):
    existing = crud.get_building_permit_by_number(db, permit.permit_number)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Permit with number {permit.permit_number} already exists",
        )
    return crud.create_building_permit(db=db, permit=permit)


@router.get(
    "/{permit_id}",
    response_model=BuildingPermitResponse,
)
def get_building_permit(
    permit_id: int,
    db: Session = Depends(get_db),
):
    permit = crud.get_building_permit(db=db, permit_id=permit_id)
    if not permit:
        raise HTTPException(status_code=404, detail="Building permit not found")
    return permit


@router.put(
    "/{permit_id}",
    response_model=BuildingPermitResponse,
)
def update_building_permit(
    permit_id: int,
    permit_update: BuildingPermitUpdate,
    db: Session = Depends(get_db),
):
    permit = crud.update_building_permit(db=db, permit_id=permit_id, permit_update=permit_update)
    if not permit:
        raise HTTPException(status_code=404, detail="Building permit not found")
    return permit


@router.delete(
    "/{permit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_building_permit(
    permit_id: int,
    db: Session = Depends(get_db),
):
    deleted = crud.delete_building_permit(db=db, permit_id=permit_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Building permit not found")
    return None
