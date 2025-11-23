from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from . import crud
from .schemas import (
    CrosswalkCreate, 
    CrosswalkUpdate, 
    CrosswalkResponse, 
    CrosswalkListResponse
)

router = APIRouter()


@router.get("/", response_model=CrosswalkListResponse)
def list_crosswalks(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum records to return"),
    db: Session = Depends(get_db)
):
    crosswalks, total = crud.get_crosswalks(db, skip=skip, limit=limit)
    return CrosswalkListResponse(total=total, crosswalks=crosswalks)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CrosswalkResponse)
def create_crosswalk(
    crosswalk: CrosswalkCreate, 
    db: Session = Depends(get_db)
):
    return crud.create_crosswalk(db=db, crosswalk_data=crosswalk)


@router.get("/{crosswalk_id}", response_model=CrosswalkResponse)
def get_crosswalk(
    crosswalk_id: int, 
    db: Session = Depends(get_db)
):
    crosswalk = crud.get_crosswalk(db, crosswalk_id)
    if not crosswalk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Crosswalk with id {crosswalk_id} not found"
        )
    return crosswalk


@router.put("/{crosswalk_id}", response_model=CrosswalkResponse)
def update_crosswalk(
    crosswalk_id: int, 
    crosswalk: CrosswalkUpdate, 
    db: Session = Depends(get_db)
):
    updated_crosswalk = crud.update_crosswalk(
        db=db, 
        crosswalk_id=crosswalk_id, 
        crosswalk_data=crosswalk
    )
    if not updated_crosswalk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Crosswalk with id {crosswalk_id} not found"
        )
    return updated_crosswalk


@router.delete("/{crosswalk_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_crosswalk(
    crosswalk_id: int, 
    db: Session = Depends(get_db)
):
    deleted = crud.delete_crosswalk(db=db, crosswalk_id=crosswalk_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Crosswalk with id {crosswalk_id} not found"
        )
    return None