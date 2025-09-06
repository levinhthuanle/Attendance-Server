from fastapi import APIRouter, Depends, HTTPException

from app.db.deps import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.record import RecordCreate, RecordOut
from app.models.student import Student
from app.schemas.student import StudentRecordOut

router = APIRouter(prefix="/student", tags=["Student"])

@router.get("/", response_model=list[StudentRecordOut])
async def get_students(db: Session = Depends(get_db)):
    students = (
        db.query(
            Student.student_id,
            User.first_name,
            User.last_name
        )
        .join(User, Student.user_id == User.user_id)
        .all()
    )
    return [
        StudentRecordOut(
            student_id=s.student_id,
            first_name=s.first_name,
            last_name=s.last_name
        )
        for s in students
    ]

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