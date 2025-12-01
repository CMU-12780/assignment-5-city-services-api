from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import or_
from .models import NoiseComplaint, ComplaintStatus, ComplaintCause
from .schemas import noise_complaints_CREATE, noise_complaints_Update

def get_noise_complaints(db: Session, skip: int = 0, limit: int = 100, status: Optional[ComplaintStatus] = None,
    search: Optional[str] = None) -> tuple[list[NoiseComplaint], int]:
    query = db.query(NoiseComplaint)

    # Apply filters
    if status:
        query = query.filter(NoiseComplaint.status == status)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                NoiseComplaint.name.ilike(search_term),
                NoiseComplaint.location.ilike(search_term)
            )
        )

    # Get total count before pagination
    total = query.count()

    # Apply pagination and get results
    complaints = query.offset(skip).limit(limit).all()

    return complaints, total

def get_noise_complaint(db: Session, noise_complaint_id: int) -> Optional[NoiseComplaint]:
    # Implementation
    return db.query(NoiseComplaint).filter(NoiseComplaint.id == noise_complaint_id).first()
    pass

def create_noise_complaint(db: Session, noise_complaint_data: NoiseComplaintCreate)->NoiseComplaint:
    # Implementation
    complaint = NoiseComplaint(**noise_complaint_data.model_dump())
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return complaint

    pass

def update_noise_complaint(db: Session, noise_complaint_id: int, noise_complaint_data: NoiseComplaintUpdate)->Optional[NoiseComplaint]:
    # Implementation
    noise_complaint = get_noise_complaint(db, noise_complaint_id)
    if not noise_complaint:
        return None

    # Update only provided fields
    update_data = noise_complaint_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(noise_complaint, field, value)

    db.commit()
    db.refresh(noise_complaint)
    return noise_complaint

    pass

def delete_noise_complaint(db: Session, noise_complaint_id: int) -> bool:
    # Implementation
    noise_complaint = get_noise_complaint(db, noise_complaint_id)
    if not noise_complaint:
        return False

    db.delete(noise_complaint)
    db.commit()
    return True

    pass 