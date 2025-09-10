from pydantic import BaseModel

class EnrollmentCheckResponse(BaseModel):
    student_id: str
    class_id: str
    enrolled: bool
