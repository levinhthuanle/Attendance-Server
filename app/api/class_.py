from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.deps import get_db
from app.models.enrollment import Enrollment
from app.models.student import Student
from app.models.user import User
from app.schemas.class_ import ClassInformation
from app.models.class_ import Class
from app.models.course import Course
from app.models.teacher import Teacher
from app.models.department import Department
from app.models.session import Session as SessionModel

router = APIRouter(prefix="/class", tags=["Class"])

@router.get("/{class_id}/information", response_model=ClassInformation)
async def get_class_information(
    class_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # chỉ cho phép student check lớp mà mình tham gia
    if current_user.role != "Student":
        raise HTTPException(status_code=403, detail="Access denied: not a student")

    # lấy student record
    student = db.query(Student).filter(Student.user_id == current_user.user_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # kiểm tra enrollment
    enrollment = (
        db.query(Enrollment)
        .filter(Enrollment.student_id == student.student_id,
                Enrollment.class_id == class_id)
        .first()
    )
    if not enrollment:
        raise HTTPException(status_code=403, detail="Student not enrolled in this class")

    result = (
        db.query(
            Class.class_id,
            Class.course_id,
            Class.teacher_id,
            Course.course_name,
            (User.first_name + " " + User.last_name).label("teacher_name"),
            Department.department_id,
            Department.department_name
        )
        .join(Course, Class.course_id == Course.course_id)
        .join(Teacher, Class.teacher_id == Teacher.teacher_id)
        .join(User, Teacher.user_id == User.user_id)
        .join(Department, User.department_id == Department.department_id)
        .filter(Class.class_id == class_id)
        .first()
    )

    return ClassInformation(
        class_id=result.class_id,
        course_id=result.course_id,
        teacher_id=result.teacher_id,
        course_name=result.course_name,
        teacher_name=result.teacher_name,
        department_id=result.department_id,
        department_name=result.department_name
    )
