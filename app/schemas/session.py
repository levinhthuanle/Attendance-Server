from pydantic import BaseModel
from datetime import datetime


class SessionCreate(BaseModel):
    start_time: datetime
    end_time: datetime
    class_id: str
    teacher_id: str

class SessionOut(SessionCreate):
    session_id: str