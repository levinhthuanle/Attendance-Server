from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.course import Course  
from app.schemas.course import CourseBase

router = APIRouter(prefix="/course", tags=["Course"])


@router.get("/", response_model=list[CourseBase])
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses


@router.post("/", response_model=CourseBase)
def create_course(course: CourseBase, db: Session = Depends(get_db)):
    existing = db.query(Course).filter(Course.course_id == course.course_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Course already exists")

    new_course = Course(
        course_id=course.course_id,
        course_name=course.course_name,
        department_id=course.department_id,
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course
