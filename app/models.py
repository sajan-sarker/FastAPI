from sqlalchemy import Column, Integer, String, ForeignKey
from . database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    credits = Column(Integer, nullable=False)
    grade = Column(String, nullable=False)


