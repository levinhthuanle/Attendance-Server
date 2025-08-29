from fastapi import APIRouter, Depends, HTTPException

from app.db.deps import get_db
from app.models.record import Record
from sqlalchemy.orm import Session
from app.schemas.record import RecordCreate, RecordOut

router = APIRouter(prefix="/record", tags=["Record"])

@router.post("/", response_model=RecordOut)
def create_record(record: RecordCreate, db: Session = Depends(get_db)):
    db_record = Record(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@router.get("/", response_model=list[RecordOut])
def get_records(db: Session = Depends(get_db)):
    records = db.query(Record).all()
    return records