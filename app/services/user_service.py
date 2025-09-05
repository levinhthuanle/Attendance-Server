from app.schemas.user import UserCreate, UserOut
from app.models.user import User
from app.models.student import Student
from app.models.teacher import Teacher
from app.core.security import get_password_hash
from fastapi import HTTPException

def create_user_service(db, user_in: UserCreate) -> UserOut:

    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    new_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        department_id=user_in.department_id,
        DOB=user_in.DOB
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    if user_in.role == "Student" or user_in.role == "student":
        new_student = Student(
            user_id=new_user.user_id,
            student_id=user_in.student_id,
            school_year=user_in.school_year
        )
        db.add(new_student)
    elif user_in.role == "Teacher" or user_in.role == "teacher":
        new_teacher = Teacher(
            user_id=new_user.user_id,
            teacher_id=user_in.teacher_id
        )
        db.add(new_teacher)
    db.commit()

    return new_user