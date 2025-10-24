from fastapi import FastAPI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import Optional
import uvicorn
import os


load_dotenv()

app = FastAPI(title="Simple FASTAPI App", description="This is our first version of FASTAPI and we are  trying to work on the GET request", version="1.0.0")

data = [{"name": "Sam Larry", "age": 20, "track": "AI Developer"},
         {"name": "Bahubali", "age": 21, "track": "Backend Developer"},
         {"name": "John Doe", "age": 22, "track": "Frontend Developer"}]

class Item(BaseModel):
    name: str = Field(..., example="Abdullateef")
    age: int = Field(..., example=25)
    track: str = Field(..., example="Fullstack Developer")

@app.get("/", description="This endpoint returns a welcome message")       # Adding a decorator 
def root():
    return {"Message": "Welcome to my FASTAPI Application"}

@app.get("/get-data")
def get_data():
    return data

@app.post("/create-data")
def create_data(req: Item):
    data.append(req.model_dump())
    print(data)
    return {"Message": "Data Received", "Data": data}

@app.put("/update-data/{id}")
def update_data(id: int, req: Item):
    data[id] = req.model_dump()
    print(data)
    return {"Message": "Data Updated", "Data": data}

# Creating class to validate patching
class validate_patch(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    track: Optional[str] = None

# Implementing the update(PATCH) function
@app.patch("/patch-data/{id}")
def patch_data(id: int, req: validate_patch):
    if id >= len(data):
        return {"Error": "Index out of range."}
    data[id].update(req.model_dump(exclude_unset=True))
    return {"Message": "Data Edited", "data": data}
    
    
# Implementing the delete(REMOVE) function
@app.delete("/delete-data/{id}")
def delete_data(id: int):
    if id >= len(data):
        return {"Error": "Index out of range."}
    data.pop(id)
    return {"Message": "Data Deleted", "data": data}

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))