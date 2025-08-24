from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Student(Base):
    __tablename__ = "Student"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=False, unique=True)
    student_id = Column(String(255), unique=True, nullable=False)
    school_year = Column(String(255))

    user = relationship("User")
    records = relationship("Record", back_populates="student")


