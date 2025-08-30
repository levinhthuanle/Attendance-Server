from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.department import Department
from app.schemas.department import Department as DepartmentOut

router = APIRouter(prefix="/department", tags=["Department"])

@router.get("/", response_model=list[DepartmentOut])
async def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()

@router.get("/{department_id}", response_model=DepartmentOut)
async def get_department(department_id: str, db: Session = Depends(get_db)):
    department = db.query(Department).filter(Department.department_id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@router.post("/", response_model=DepartmentOut)
async def create_department(department: DepartmentOut, db: Session = Depends(get_db)):
    db.add(department)
    db.commit()
    db.refresh(department)
    return department