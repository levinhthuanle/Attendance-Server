from pydantic import BaseModel

class RecordCreate(BaseModel):
    student_id: str
    status: str
    session_id: str

class RecordOut(RecordCreate):
    record_id: str