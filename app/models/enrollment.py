import uuid
from sqlalchemy import Column, String, ForeignKey
from app.db.session import Base
from sqlalchemy.orm import relationship

class Enrollment(Base):
    __tablename__ = "Enrollment"

    enrollment_id = Column(String(255), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String(255), ForeignKey("Student.student_id"), nullable=False)
    class_id = Column(String(255), ForeignKey("Class.class_id"), nullable=False)

    student = relationship("Student", back_populates="enrollments")
    class_ = relationship("Class", back_populates="enrollments")