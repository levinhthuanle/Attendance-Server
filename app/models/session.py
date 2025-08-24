from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.session import Base
from sqlalchemy.orm import relationship
import uuid

class Session(Base):
    __tablename__ = "Session"

    session_id = Column(String(255), primary_key=True, default=lambda: str(uuid.uuid4()))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    class_id = Column(String(255), ForeignKey("Class.class_id"), nullable=False)
    teacher_id = Column(String(255), ForeignKey("Teacher.teacher_id"), nullable=False)
    
    teacher = relationship("Teacher", back_populates="sessions")
    class_ = relationship("Class", back_populates="sessions")
    records = relationship("Record", back_populates="session")
