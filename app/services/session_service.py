from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.session import Session as SessionModel
from app.schemas.session import SessionCreate, SessionOut


def get_all_session_service(db: Session) -> SessionOut:
    return db.query(SessionModel).all()

def create_session_service(db: Session, session_in: SessionCreate):
    session = SessionModel(**session_in.model_dump())
    db.add(session)
    db.commit()
    db.refresh(session)
    return session