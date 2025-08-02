from fastapi import FastAPI
import json

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