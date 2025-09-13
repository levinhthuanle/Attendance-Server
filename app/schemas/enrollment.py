from pydantic import BaseModel

class EnrollmentCheckResponse(BaseModel):
    student_id: str
    class_id: int
    enrolled: bool

class EnrollmentBase(BaseModel):

    student_id: str
    class_id: int
    
class EnrollmentOut(EnrollmentBase):
    enrollment_id: int