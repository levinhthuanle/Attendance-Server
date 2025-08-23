from sqlalchemy import Column, String, Date
from app.db.session import Base

from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Class(Base):
    __tablename__ = "Class"

    class_id = Column(String(255), primary_key=True, index=True)
    course_id = Column(String(255), ForeignKey("Course.course_id"), nullable=False)
    semester = Column(String(255), nullable=False)
    year = Column(Date, nullable=False)

    course = relationship("Course", back_populates="classes")
    records = relationship("Record", back_populates="class_")
