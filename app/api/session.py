from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db
from typing import List
from app.schemas.session import SessionCreate, SessionOut
from app.services.session_service import create_session_service, get_all_session_service, get_current_session_service, get_session_service

router = APIRouter(prefix="/session", tags=["Session"])

@router.post("/", response_model=SessionOut)
def create_session(session_in: SessionCreate, db: Session = Depends(get_db)):
    return create_session_service(db, session_in)

@router.get("/", response_model=List[SessionOut])
def get_sessions(db: Session = Depends(get_db)):
    return get_all_session_service(db)

@router.get("/current_session/", response_model=List[SessionOut])
def get_current_session(class_id : int, db: Session = Depends(get_db)):
    return get_current_session_service(db, class_id)

@router.get("/{session_id}", response_model=SessionOut)
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = get_session_service(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session