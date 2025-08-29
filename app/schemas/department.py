from pydantic import BaseModel

class Department(BaseModel):
    department_id: str
    department_name: str