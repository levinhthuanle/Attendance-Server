
from sqlalchemy import Column, String
from app.db.session import Base
from sqlalchemy.orm import relationship

class Department(Base):
    __tablename__ = "Department"

    department_id = Column(String, primary_key=True, index=True)
    department_name = Column(String(255), unique=True, nullable=False)

    courses = relationship("Course", back_populates="department")
    users = relationship("User", back_populates="department")
