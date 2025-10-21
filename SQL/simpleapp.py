from database import db
from fastapi import FastAPI, HTTPException # To handle ty exception error
from pydantic import BaseModel, Field
from sqlalchemy import text
import os
from dotenv import load_dotenv
import bcrypt
import uvicorn

load_dotenv()

app = FastAPI(title="Simple App", version="1.0.0")

class Simple(BaseModel):
    name: str = Field(..., examples=["Abdullateef"])
    email: str = Field(..., examples=["abc@gmail.com"])
    password: str = Field(..., examples=["abdul123"])
    
@app.get("/", description="This endpoint returns a welcome message")       # Adding a decorator 
def root():
    return {"Message": "Welcome to my FASTAPI Application"}

@app.post("/signup")
def signUp(input: Simple):
    try:
        duplicate_query = text("""
            SELECT * FROM users
            WHERE email = :email
                               """)
        # Checking for an existing details
        existing = db.execute(duplicate_query, {"email": input.email})
        if existing:
            print("Email already exists")
            # raise HTTPException(status_code=400, detail="Email already exists")
        
        query = text("""
              INSERT INTO users (name, email, password)
              VALUES(:name, :email, :password)       # We used ":" as a placeholder here.
        """)
        # To encrypt our password, we need to install bcrypt
        salt = bcrypt.gensalt()     # Salt is needed here to automatically generate random values to the enconded password created to differentiate from each other
        hashedPassword = bcrypt.hashpw(input.password.encode('utf-8'), salt)
        print(hashedPassword)
        
        db.execute(query, {"name": input.name, "email": input.email, "password": hashedPassword})
        db.commit()     # Did this to commit changes after inputting.
        
        return{
            "message": "User created successfully",
            "data": {"name": input.name, "email": input.email}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=0)
    
if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))