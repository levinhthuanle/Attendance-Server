from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.session import Base
from sqlalchemy.orm import relationship

class Class(Base):
    __tablename__ = "Class"

    class_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(String(255), ForeignKey("Course.course_id"), nullable=False)
    class_name = Column(String(255), nullable=False)
    semester = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    teacher_id = Column(String(255), ForeignKey("Teacher.teacher_id"), nullable=False)

    teacher = relationship("Teacher", back_populates="classes")
    course = relationship("Course", back_populates="classes")
    sessions = relationship("Session", back_populates="class_")
    enrollments = relationship("Enrollment", back_populates="class_")