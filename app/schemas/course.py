from pydantic import BaseModel

class CourseBase(BaseModel):
    course_id: str
    course_name: str
    department_id: str | None = None