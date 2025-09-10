from pydantic import BaseModel
from datetime import date

class StudentRecordOut(BaseModel):
    student_id: str
    first_name: str
    last_name: str

class StudentBase(BaseModel):
    student_id: str

class StudentFull(StudentBase):
    email: str
    first_name: str
    last_name: str
    DOB: date | None = None
    school_year: str | None = None
    department_id: str | None = None
    