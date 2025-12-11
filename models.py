from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class School(Base):
    __tablename__ = "schools"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(200))
    email = Column(String(100), unique=True)
    
    students = relationship("Student", back_populates="school")

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    email = Column(String(100), unique=True)
    school_id = Column(Integer, ForeignKey("schools.id"))
    
    school = relationship("School", back_populates="students")