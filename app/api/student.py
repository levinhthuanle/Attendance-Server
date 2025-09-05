from fastapi import APIRouter, Depends, HTTPException

from app.db.deps import get_db
from sqlalchemy.orm import Session
from app.schemas.record import RecordCreate, RecordOut
from app.models.student import Student

router = APIRouter(prefix="/student", tags=["Student"])

@router.get("/")
async def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students

@router.get("/{student_id}/records", response_model=list[RecordOut])
async def get_student_records(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student.records

@router.post("/record", response_model=RecordOut)
async def create_student_record(record: RecordCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == record.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.records.append(record)
    db.commit()
    db.refresh(student)
    return student.records