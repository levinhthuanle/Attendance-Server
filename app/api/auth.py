from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError
from app.db.deps import get_db
from app.models.user import User
from app.core import security
from app.core.config import settings
from app.schemas.user import UserLogin
from app.schemas.token import Token, TokenRefresh

from fastapi.responses import JSONResponse
from fastapi import Depends
from app.core.security import get_current_user



router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    # Tìm user theo email
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Xác thực mật khẩu
    if not security.verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Tạo access token
    access_token = security.create_access_token(
        data={"sub": str(user.user_id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Tạo refresh token
    refresh_token = security.create_refresh_token(
        data={"sub": str(user.user_id)},
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/refresh", response_model=Token)
def refresh_token(data: TokenRefresh, db: Session = Depends(get_db)):
    try:
        # Decode refresh token
        payload = security.decode_token(data.refresh_token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        # Kiểm tra user còn tồn tại
        user = db.query(User).filter(User.user_id == int(user_id)).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Tạo token mới
    new_access_token = security.create_access_token(
        data={"sub": str(user.user_id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    new_refresh_token = security.create_refresh_token(
        data={"sub": str(user.user_id)},
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )

@router.post("/logout")
def logout():

    return JSONResponse(
        status_code=200,
        content={"message": "Logged out successfully. Please discard tokens on client side."}
    )
    
    
@router.get("/me/role")
def get_current_user_role(current_user: User = Depends(get_current_user)):
    return {"role": current_user.role}