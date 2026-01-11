from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def wave():
    return {
        "message": "Hallo, verden!"
    }

@app.get("/repo")
def repo():
    return {
        "repository": "FastAPI"
    }

@app.get("/author")
def author():
    return {
        "author": "Sajan Sarker"
    }