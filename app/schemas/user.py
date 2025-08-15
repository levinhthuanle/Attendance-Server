from pydantic import BaseModel, EmailStr
from datetime import date

class UserBase(BaseModel):
    email: str
    role: str | None = None # Student, Teacher, Admin
    first_name: str | None = None
    last_name: str | None = None
    department_id: str | None = None
    DOB: date | None = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(UserBase):
    user_id: int

    class Config:
        orm_mode = True

