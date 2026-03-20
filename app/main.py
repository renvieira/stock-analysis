from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def primeiro_endpoint():
    return {"message": "Hello World!"}
