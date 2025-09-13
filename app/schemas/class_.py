from pydantic import BaseModel, ConfigDict

class ClassBase(BaseModel):
    course_id: str
    teacher_id: str
    
class ClassInformation(ClassBase):
    class_id: int
    course_name: str
    teacher_name: str
    department_id: str 
    department_name: str
    semester: str | None = None
    year: int | None = None
    class_name: str | None = None
    

    model_config = ConfigDict(from_attributes=True)
    
class ClassCreate(ClassBase):
    class_name: str | None = None
    semester: str | None = None
    year: int | None = None
    model_config = ConfigDict(from_attributes=True)