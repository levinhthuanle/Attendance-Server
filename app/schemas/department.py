from pydantic import BaseModel

class DepartmentBase(BaseModel):
    department_id: str
    department_name: str