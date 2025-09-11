from fastapi import APIRouter, Depends, HTTPException

from app.api.users import get_current_user
from app.db.deps import get_db
from app.models.record import Record
from sqlalchemy.orm import Session
from app.models.user import User
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

@router.get("/{session_id}", response_model=list[RecordOut])
async def get_session_records(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user.role not in ["Teacher", "Admin"]:
        raise HTTPException(status_code=403, detail="Access denied")

    records = (
        db.query(Record)
        .filter(Record.session_id == session_id)
        .all()
    )

    if not records:
        raise HTTPException(status_code=404, detail="No attendance records found for this session")

    return records
