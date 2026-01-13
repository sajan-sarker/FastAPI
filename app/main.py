import os
import time

from pydantic import BaseModel
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .models import Course
from .database import Base, engine, get_db

app = FastAPI()

Base.metadata.create_all(bind=engine) # create the database tables

class CourseRequest(BaseModel):
    course_code: str
    name: str
    description: str | None = None 
    credits: float
    grade: str
    num_of_class: int
    attendance: int

@app.get("/courses")
def read_courses(db:Session = Depends(get_db)):
    return {
        "status": "success",
    }

@app.post("/courses")
def write_course(course: CourseRequest, db:Session=Depends(get_db)):
    new_course = Course(
        course_code=(course.course_code).upper(),
        name=(course.name).title(),
        description=course.description,
        credits=course.credits,
        grade=(course.grade).upper(),
        num_of_class=course.num_of_class,
        attendance=course.attendance
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return {
        "Course": new_course
    }