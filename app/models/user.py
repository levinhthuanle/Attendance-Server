from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(255)) # Student, Teacher, Admin
    first_name = Column(String(255))
    last_name = Column(String(255))
    department_id = Column(String, ForeignKey("Department.department_id"))
    DOB = Column(Date)

    department = relationship("Department", back_populates="users")

