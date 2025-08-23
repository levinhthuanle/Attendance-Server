from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.session import Base

from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Record(Base):
    __tablename__ = "Record"

    record_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("Student.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("Teacher.id"), nullable=False)
    status = Column(String(255), nullable=False)
    class_id = Column(String(255), ForeignKey("Class.class_id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    student = relationship("Student", back_populates="records")
    teacher = relationship("Teacher", back_populates="records")
    class_ = relationship("Class", back_populates="records")
