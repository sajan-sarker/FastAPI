import os
from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel, HttpUrl
import psycopg2
from psycopg2.extras import RealDictCursor
import load_dotenv
load_dotenv.load_dotenv()

# define request body schema for POST method
class CourseRequest(BaseModel):
    """ Schema for course creation request, including course details. """
    """ This class uses Pydantic BaseModel for data validation. """
    course_name: str
    skills: list[str]
    duration: int
    certification: bool
    certification_link: HttpUrl | None = None
    platform: str

app = FastAPI()

# connect to PostgreSQL database
try:
    conn = psycopg2.connect(
        host=os.getenv("POSTGRE_SQL_HOST"),
        database=os.getenv("POSTGRE_SQL_DB"),
        user=os.getenv("POSTGRE_SQL_USER"),
        password=os.getenv("POSTGRE_SQL_PASSWORD"),
        cursor_factory=RealDictCursor
    )
    cursor = conn.cursor()
    print("Database connection successful")
except Exception as e:
    print("Error connecting to database:", e)

# Define a GET endpoint at the root path
# Get method is used to retrieve data from the server
@app.get("/")
def read_root():
    return {
        "Path": "/",
        "message": "Hallo, verden!"
    }

# get data from database
@app.get("/courses")
def get_courses():
    try:
        cursor.execute("select * from course")
        courses = cursor.fetchall()
        return {
            "All Courses": courses
        }
    except Exception as e:
        return {
            "error": str(e)
        }

# Define a POST endpoint at /course
# Post method is used to send data to the server/database
@app.post("/course")
def create_course(course: CourseRequest):
    cursor.execute(
        """ insert into course (name, skills, duration, certification, certification_link, platform) values (%s, %s, %s, %s, %s, %s) RETURNING * """,
        (course.course_name, course.skills, course.duration, course.certification, str(course.certification_link), course.platform)
    )
    course = cursor.fetchone()
    conn.commit()
    return {
        "data": course
    }

# define a get endpoint to fetch single course info by id
@app.get("/courses/{course_id}")
def get_course(course_id: int):
    cursor.execute(
        """ select * from course where id = %s """,
        (str(course_id), )
    )
    course = cursor.fetchone()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    return {
        "Course Details": course
    }

# define a DELETE endpoint at /course/{course_id}
# Delete method is used to delete data from the server/database
@app.delete("/course/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int):
    cursor.execute(
        """ delete from course where id = %s returning * """,
        (str(course_id, ))
    )
    deleted_course = cursor.fetchone()
    conn.commit()
    if deleted_course == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"course with id: {course_id} Not Exist")
    return Response(
        status_code=status.HTTP_404_NOT_FOUND
    )

# define a PUT endpoint at /course/{course_id}
# PUT mehtod is used to update data from server/database
@app.put("/course/{course_id}")
def update_course(course_id: int, course: CourseRequest):
    cursor.execute(
        """ UPDATE course
            SET name = %s, skills = %s, duration = %s, certification = %s, certification_link = %s, platform = %s
            WHERE id = %s
            RETURNING *
        """,
        (course.course_name, course.skills, course.duration, course.certification, str(course.certification_link), course.platform, str(course_id))
    )
    updated_course = cursor.fetchone()
    conn.commit()
    if course_id == None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Course with id: {course_id} not exist"
        )
    
    return {
        "course": updated_course
    }
