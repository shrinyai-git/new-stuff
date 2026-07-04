from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def hello_world():
    return "Hello, World!"


@app.get("/hello")
def hello():
    return {"message": hello_world()}


