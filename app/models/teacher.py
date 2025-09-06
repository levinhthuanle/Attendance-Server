from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from app.db.session import Base


class Teacher(Base):
    __tablename__ = "Teacher"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=False, unique=True)
    teacher_id = Column(String(255), unique=True, nullable=False)
    
    user = relationship("User")
    sessions = relationship("Session", back_populates="teacher") 
    classes = relationship("Class", back_populates="teacher")