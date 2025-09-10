from pydantic import BaseModel
from datetime import date

class TeacherBase(BaseModel):
    teacher_id: str

class TeacherFull(TeacherBase): 
    email: str
    first_name: str
    last_name: str
    DOB: date | None = None
    department_id: str | None = None
    
    class Config:
        orm_mode = True