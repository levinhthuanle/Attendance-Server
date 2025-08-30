from fastapi import APIRouter, Depends, HTTPException

from app.db.deps import get_db
from sqlalchemy.orm import Session

from app.models.student import Student

router = APIRouter(prefix="/student", tags=["Student"])

@router.get("/")
async def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students

@router.get("/check")
async def check():
    return "Success"