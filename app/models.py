from sqlalchemy import Column, Integer, String, ForeignKey, Float
from . database import Base
class Course(Base):
    __tablename__ = "courses"

    course_code = Column(String, unique=True, index=True, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    credits = Column(Float, nullable=False)
    grade = Column(String, nullable=False)
    num_of_class = Column(Integer, nullable=False)
    attendance= Column(Integer, nullable=False)