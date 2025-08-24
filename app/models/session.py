from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.session import Base
from sqlalchemy.orm import relationship

class Session(Base):
    __tablename__ = "Session"

    session_id = Column(String(255), primary_key=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    class_id = Column(String(255), ForeignKey("Class.class_id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("Teacher.id"), nullable=False)


    teacher = relationship("Teacher", back_populates="Session")
    class_ = relationship("Class", back_populates="Session")
    records = relationship("Record", back_populates="Session")
