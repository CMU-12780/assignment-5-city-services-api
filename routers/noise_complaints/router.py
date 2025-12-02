from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database import get_db
from typing import Optional
from .models import NoiseComplaint
from .models import ComplaintCause
from .models import ComplaintStatus

from .schemas import NoiseComplaintUpdate, NoiseComplaintCreate, NoiseComplaintResponse, NoiseComplaintListResponse
from . import crud

router = APIRouter()

@router.get("/", response_model=NoiseComplaintListResponse)
def list_noise_complaints(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum records to return"),
    status: Optional[ComplaintStatus] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search in name or location"),
    db: Session = Depends(get_db)    
):

    complaints, total = crud.get_noise_complaints(
        db=db,
        skip=skip,
        limit=limit,
        status=status,
        search=search
        )
    return NoiseComplaintListResponse(total=total, noise_complaints=complaints)

@router.post("/", response_model=NoiseComplaintResponse, status_code=status.HTTP_201_CREATED)
def create_noise_complaint(
    complaint:NoiseComplaintCreate,
    db: Session = Depends(get_db)
    ):
    # POST new resource
    return crud.create_noise_complaint(db=db, noise_complaint_data=complaint)
    pass

@router.get("/{noise_complaint_id}", response_model=NoiseComplaintResponse)
def get_resource(noise_complaint_id: int, db: Session = Depends(get_db)):
    # GET single resource
    complaint = crud.get_noise_complaint(db=db, noise_complaint_id=noise_complaint_id)
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Complaint with id {noise_complaint_id} not found"
        )
    return complaint

@router.put("/{noise_complaint_id}", response_model=NoiseComplaintResponse)
def update_noise_complaint(noise_complaint_id: int, noise_complaint:NoiseComplaintUpdate, db: Session = Depends(get_db)):
    # PUT update resource
    updated_complaint = crud.update_noise_complaint(db=db, noise_complaint_id=noise_complaint_id, noise_complaint_data=noise_complaint)
    
    if not updated_complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Noise complaint with id {noise_complaint_id} not found"
        )
    return updated_complaint
    pass

@router.delete("/{noise_complaint_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_noise_complaint(noise_complaint_id: int, db: Session = Depends(get_db)):
    # DELETE resource
    deleted = crud.delete_noise_complaint(db=db, noise_complaint_id=noise_complaint_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Complaint with id {noise_complaint_id} not found"
        )
    return None
    pass