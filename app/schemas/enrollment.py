from pydantic import BaseModel

class EnrollmentCheckResponse(BaseModel):
    student_id: str
    class_id: str
    enrolled: bool

class EnrollmentBase(BaseModel):

    student_id: str
    class_id: str
    
class EnrollmentOut(EnrollmentBase):
    enrollment_id: str