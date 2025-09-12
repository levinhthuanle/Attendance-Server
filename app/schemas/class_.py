from pydantic import BaseModel, ConfigDict

class ClassBase(BaseModel):
    class_id: str
    course_id: str
    teacher_id: str
    
class ClassInformation(ClassBase):
    course_name: str
    teacher_name: str
    department_id: str 
    department_name: str
    semester: str | None = None
    year: int | None = None
    

    model_config = ConfigDict(from_attributes=True)
    
class ClassCreate(ClassBase):
    semester: str | None = None
    year: int | None = None
    model_config = ConfigDict(from_attributes=True)