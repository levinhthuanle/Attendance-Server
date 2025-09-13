import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.session import Base

from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Record(Base):
    __tablename__ = "Record"

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(255), ForeignKey("Student.student_id"), nullable=False)
    status = Column(String(255), nullable=False)
    session_id = Column(Integer, ForeignKey("Session.session_id"), nullable=False)


    student = relationship("Student", back_populates="records")
    session = relationship("Session", back_populates="records")