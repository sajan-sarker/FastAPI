from fastapi import FastAPI, Path, HTTPException, Query
import json

# Path function used to provide metadata, rules, and documentations for path parameters
# HTTPException is used to raise custom errors with specific status codes
# Query is used to handle query parameters in the API

app = FastAPI()

def load_data():
    with open("./data/students.json", "r") as file:
        data = json.load(file)
        return data

@app.get("/")
def home():
    return {"message": "Student Management System API"}

@app.get("/about")
def about():
    return {"message": "This API manages student data."}

@app.get("/view")
def view_students():
    data = load_data()
    return data

@app.get('/student/{student_id}')
def view_student(student_id: str = Path(..., description="The ID of the student to view", example="s001")):
    # load all the data
    data = load_data()
    if student_id in data:
        return data[student_id]
    raise HTTPException(status_code=404, detail="Student not found")

@app.get('/sort')
def sort_students(sort_by: str = Query(..., description="Filed to sort by name", example="id"), order: str = Query("asc", description="Order to sort by, either 'asc' or 'desc'")):
    valid_fields = ["name", "age", "id", "grade"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. valid fields are:: {", ".join(valid_fields)}")
    
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Order must be either 'asc' or 'desc'")
    
    data = load_data()

    order_by = True if order == "desc" else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=order_by)
    return sorted_data