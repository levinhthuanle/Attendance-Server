from pydantic import BaseModel

class ClassBase(BaseModel):
    class_id: str
    course_id: str
    teacher_id: str
    
class ClassInformation(ClassBase):
    course_name: str
    teacher_name: str
    department_id: str 
    department_name: str

    class Config:
        orm_mode = True