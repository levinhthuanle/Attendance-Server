
from fastapi import APIRouter, Depends, HTTPException
from app.db.deps import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.record import RecordCreate, RecordOut
from app.models.student import Student
from app.schemas.student import StudentRecordOut, StudentFull
from app.core.security import get_current_user

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

@router.get("/current", response_model=StudentFull)
async def get_current_student(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "Student":
        raise HTTPException(status_code=403, detail="Access denied: not a student")
    
    student = db.query(Student).filter(Student.user_id == current_user.user_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return StudentFull(
        student_id=student.student_id,
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        DOB=current_user.DOB,
        school_year=student.school_year,
        department_id=current_user.department_id
    )

@router.get("/attendance_records", response_model=list[RecordOut])
async def get_attendance_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "Student":
        raise HTTPException(status_code=403, detail="Access denied: not a student")

    student = db.query(Student).filter(Student.user_id == current_user.user_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student.records
