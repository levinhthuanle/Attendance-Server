from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.user import User
from app.schemas.teacher import TeacherFull
from app.core.security import get_current_user
from app.models.teacher import Teacher
from app.models.session import Session as SessionModel
from app.schemas.session import SessionOut
from typing import List

router = APIRouter(prefix="/teacher", tags=["Teacher"])

@router.get("/current", response_model=TeacherFull)
async def get_current_teacher(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "Teacher":
        raise HTTPException(status_code=403, detail="Access denied: not a teacher")

    teacher = db.query(Teacher).filter(Teacher.user_id == current_user.user_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    return TeacherFull(
        teacher_id=teacher.teacher_id,
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        DOB=current_user.DOB,
        department_id=current_user.department_id
    )

@router.get("/teaching_sessions/", response_model=List[SessionOut])
async def get_teaching_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "Teacher":
        raise HTTPException(status_code=403, detail="Access denied: not a teacher")

    teacher = db.query(Teacher).filter(Teacher.user_id == current_user.user_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    sessions = (
        db.query(SessionModel)
        .filter(SessionModel.teacher_id == teacher.teacher_id)
        .all()
    )

    return [SessionOut.from_orm(session) for session in sessions]