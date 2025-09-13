import uuid
from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.session import Base
from sqlalchemy.orm import relationship

class Enrollment(Base):
    __tablename__ = "Enrollment"

    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String, ForeignKey("Student.student_id"), nullable=False)
    class_id = Column(Integer, ForeignKey("Class.class_id"), nullable=False)

    student = relationship("Student", back_populates="enrollments")
    class_ = relationship("Class", back_populates="enrollments")