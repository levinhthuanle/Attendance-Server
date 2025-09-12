from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import create_user_service
from app.core.security import get_current_user as get_current_user_dep

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/", response_model=UserOut)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(db, user_in)



@router.get("/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/current", response_model=UserOut)
def get_current_user(current_user: User = Depends(get_current_user_dep)):
    return current_user