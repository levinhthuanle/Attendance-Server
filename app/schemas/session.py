from pydantic import BaseModel, ConfigDict
from datetime import datetime

class SessionCreate(BaseModel):
    start_time: datetime
    end_time: datetime
    class_id: str
    teacher_id: str

class SessionOut(SessionCreate):
    session_id: str
    model_config = ConfigDict(from_attributes=True)
    
class AttendanceRequest(BaseModel):
    session_id: str
    status: str = "Present"   

class SessionInfo(BaseModel):
    session_id: str
    start_time: datetime
    end_time: datetime

    class Config:
        orm_mode = True