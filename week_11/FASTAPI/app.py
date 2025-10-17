from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn
import os


load_dotenv()

app = FastAPI(title="Simple FASTAPI App", description="This is our first version of FASTAPI and we are  trying to work on the GET request", version="1.0.0")

@app.get("/", description="This endpoint returns a welcome message")       # Adding a decorator 
def root():
    return {"Message": "Welcome to FASTAPI Application"}

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))