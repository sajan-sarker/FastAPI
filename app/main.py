import os
import time

from fastapi import FastAPI, Depends
from sqlalchemy.orm import session

from . import models
from .database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine) # create the database tables

@app.get("/courses")
def read_courses(db:session = Depends(get_db)):
    return {
        "status": "success",
    }