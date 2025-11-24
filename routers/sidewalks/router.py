"""
Sidewalk Router
FastAPI endpoints for sidewalk management
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from .models import SidewalkCondition
from .schemas import (
    SidewalkCreate,
    SidewalkUpdate,
    SidewalkResponse,
    SidewalkListResponse,
)
from . import crud

router = APIRouter()


@router.get("/", response_model=SidewalkListResponse)
def list_sidewalks(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records to return"),
    condition: Optional[SidewalkCondition] = Query(None, description="Filter by condition"),
    ada_compliant: Optional[bool] = Query(None, description="Filter by ADA compliance"),
    search: Optional[str] = Query(None, description="Search street name"),
    db: Session = Depends(get_db)
):
    """
    List all sidewalks with optional filtering:
    - condition: excellent, good, fair, poor
    - ada_compliant: true/false
    - search: street name match
    """
    sidewalks, total = crud.get_sidewalks(
        db=db, skip=skip, limit=limit, condition=condition,
        ada_compliant=ada_compliant, search=search
    )
    return SidewalkListResponse(total=total, sidewalks=sidewalks)


@router.post("/", response_model=SidewalkResponse, status_code=status.HTTP_201_CREATED)
def create_sidewalk(sidewalk: SidewalkCreate, db: Session = Depends(get_db)):
    """Create a new sidewalk record"""
    return crud.create_sidewalk(db=db, data=sidewalk)


@router.get("/{sidewalk_id}", response_model=SidewalkResponse)
def get_sidewalk(sidewalk_id: int, db: Session = Depends(get_db)):
    """Get a specific sidewalk by its ID"""
    item = crud.get_sidewalk(db=db, sidewalk_id=sidewalk_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sidewalk with id {sidewalk_id} not found"
        )
    return item


@router.put("/{sidewalk_id}", response_model=SidewalkResponse)
def update_sidewalk(
    sidewalk_id: int,
    sidewalk: SidewalkUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing sidewalk record"""
    updated = crud.update_sidewalk(db=db, sidewalk_id=sidewalk_id, data=sidewalk)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sidewalk with id {sidewalk_id} not found"
        )
    return updated


@router.delete("/{sidewalk_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sidewalk(sidewalk_id: int, db: Session = Depends(get_db)):
    """Delete a sidewalk record"""
    deleted = crud.delete_sidewalk(db=db, sidewalk_id=sidewalk_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sidewalk with id {sidewalk_id} not found"
        )
    return None
