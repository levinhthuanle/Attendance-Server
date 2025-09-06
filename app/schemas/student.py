from pydantic import BaseModel

class StudentRecordOut(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    