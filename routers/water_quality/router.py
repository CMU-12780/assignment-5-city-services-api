"""
Water Quality Router
FastAPI endpoints for water quality sample management
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from .schemas import (
    WaterQualityCreate,
    WaterQualityUpdate,
    WaterQualityResponse,
    WaterQualityListResponse,
)
from . import crud
from .models import WaterQualityStatus

router = APIRouter()


@router.get("/", response_model=WaterQualityListResponse)
def list_samples(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    start_date: Optional[str] = Query(None, description="Start sample date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End sample date (YYYY-MM-DD)"),
    status: Optional[WaterQualityStatus] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search site name or location"),
    db: Session = Depends(get_db)
):
    """List water quality samples with optional filtering"""
    samples, total = crud.get_samples(
        db=db,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        status=status,
        search=search,
    )
    return WaterQualityListResponse(total=total, samples=samples)


@router.post("/", response_model=WaterQualityResponse, status_code=status.HTTP_201_CREATED)
def create_sample(sample: WaterQualityCreate, db: Session = Depends(get_db)):
    """Create a new water quality sample"""
    return crud.create_sample(db=db, sample_data=sample)


@router.get("/{sample_id}", response_model=WaterQualityResponse)
def get_sample(sample_id: int, db: Session = Depends(get_db)):
    """Get a specific water quality sample by ID"""
    s = crud.get_sample(db=db, sample_id=sample_id)
    if not s:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sample with id {sample_id} not found")
    return s


@router.put("/{sample_id}", response_model=WaterQualityResponse)
def update_sample(sample_id: int, sample: WaterQualityUpdate, db: Session = Depends(get_db)):
    """Update an existing water quality sample"""
    updated = crud.update_sample(db=db, sample_id=sample_id, sample_data=sample)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sample with id {sample_id} not found")
    return updated


@router.delete("/{sample_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sample(sample_id: int, db: Session = Depends(get_db)):
    """Delete a water quality sample"""
    deleted = crud.delete_sample(db=db, sample_id=sample_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sample with id {sample_id} not found")
    return None
