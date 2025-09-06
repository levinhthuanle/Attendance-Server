
from sqlalchemy import Column, String, ForeignKey
from app.db.session import Base
from sqlalchemy.orm import relationship

class Course(Base):
    __tablename__ = "Course"

    course_id = Column(String(255), primary_key=True, index=True)
    course_name = Column(String(255), nullable=False)
    department_id = Column(String(255), ForeignKey("Department.department_id"))
    
    department = relationship("Department", back_populates="courses")
    classes = relationship("Class", back_populates="course")
