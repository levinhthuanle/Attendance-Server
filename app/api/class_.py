from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.deps import get_db
from app.models.enrollment import Enrollment
from app.models.record import Record
from app.models.student import Student
from app.models.user import User
from app.schemas.class_ import ClassInformation, ClassCreate
from app.models.class_ import Class
from app.models.course import Course
from app.models.teacher import Teacher
from app.models.department import Department
from app.models.session import Session as SessionModel
from app.schemas.student import StudentBase
from app.schemas.session import SessionInfo
from app.schemas.record import RecordOut

router = APIRouter(prefix="/class", tags=["Class"])

@router.get("/{class_id}/information", response_model=ClassInformation)
async def get_class_information(
    class_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = (
        db.query(
            Class.class_id,
            Class.course_id,
            Class.teacher_id,
            Class.class_name,
            Course.course_name,
            (User.first_name + " " + User.last_name).label("teacher_name"),
            Department.department_id,
            Department.department_name,
            Class.semester,
            Class.year
        )
        .join(Course, Class.course_id == Course.course_id)
        .join(Teacher, Class.teacher_id == Teacher.teacher_id)
        .join(User, Teacher.user_id == User.user_id)
        .join(Department, User.department_id == Department.department_id)
        .filter(Class.class_id == int(class_id))
        .first()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Class not found")

    return ClassInformation(
        class_id=result.class_id,
        course_id=result.course_id,
        teacher_id=result.teacher_id,
        course_name=result.course_name,
        teacher_name=result.teacher_name,
        department_id=result.department_id,
        department_name=result.department_name,
        semester=result.semester,
        year=result.year
    )


@router.post("/", response_model=ClassCreate)
async def create_class(
    class_data: ClassCreate,
    db: Session = Depends(get_db)
):

    new_class = Class(
        course_id=class_data.course_id,
        teacher_id=class_data.teacher_id,
        semester=class_data.semester,
        year=class_data.year,
        class_name=class_data.class_name
    )
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class


@router.get("/{class_id}/students", response_model=list[StudentBase])
async def get_class_students(
    class_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["Teacher", "Admin", "teacher", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")

    students = (
        db.query(Student)
        .join(Enrollment, Enrollment.student_id == Student.student_id)
        .filter(Enrollment.class_id == class_id)
        .all()
    )

    if not students:
        raise HTTPException(status_code=404, detail="No students found in this class")

    return students

@router.get("/{class_id}/sessions", response_model=list[SessionInfo])
async def get_class_sessions(
    class_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["Student", "Teacher", "Admin", "teacher", "admin", "student"]:
        raise HTTPException(status_code=403, detail="Access denied")

    sessions = (
        db.query(SessionModel)
        .filter(SessionModel.class_id == class_id)
        .all()
    )

    if not sessions:
        raise HTTPException(status_code=404, detail="No sessions found for this class")

    return sessions

@router.get("/{class_id}/records", response_model=list[RecordOut])
async def get_class_records(
    class_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    if current_user.role not in ["Teacher", "Admin", "teacher", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")

    records = (
        db.query(Record)
        .join(SessionModel, Record.session_id == SessionModel.session_id)
        .filter(SessionModel.class_id == class_id)
        .all()
    )

    if not records:
        raise HTTPException(status_code=404, detail="No records found for this class")

    return records
