from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentBase, EnrollmentOut

router = APIRouter(prefix="/enrollment", tags=["Enrollment"])



@router.get("/", response_model=list[EnrollmentOut])
def get_enrollments(db: Session = Depends(get_db)):
    enrollments = db.query(Enrollment).all()
    return enrollments



@router.post("/", response_model=EnrollmentOut)
def create_enrollment(enrollment: EnrollmentBase, db: Session = Depends(get_db)):
    existing = db.query(Enrollment).filter(Enrollment.student_id == enrollment.student_id, Enrollment.class_id == enrollment.class_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Enrollment already exists")

    new_enrollment = Enrollment(
        student_id=enrollment.student_id,
        class_id=enrollment.class_id,
    )
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return new_enrollment
