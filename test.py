import fastapi
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Holaa..."}

@app.get("/bye")
def bye():
    return {"message": "Bye..."}

@app.get("/version")
def version():
    version_info = {
        "fastapi": fastapi.__version__
    }
    return version_info