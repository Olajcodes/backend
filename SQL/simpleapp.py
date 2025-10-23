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
    userType: str = Field(..., examples=["student"])
    
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
            raise HTTPException(status_code=400, detail="Email already exists")
        
        query = text("""
              INSERT INTO users (name, email, password)
              VALUES(:name, :email, :password)       # We used ":" as a placeholder here.
        """)
        # To encrypt our password, we need to install bcrypt
        salt = bcrypt.gensalt()     # Salt is needed here to automatically generate random values to the enconded password created to differentiate from each other
        hashedPassword = bcrypt.hashpw(input.password.encode('utf-8'), salt)
        print(hashedPassword)
        
        db.execute(query, {"name": input.name, "email": input.email, "password": hashedPassword, "userType": input.userType})
        db.commit()     # Did this to commit changes after inputting.
        
        return{
            "message": "User created successfully",
            "data": {"name": input.name, "email": input.email, "userType": input.userType}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=0)
    
# TO build a login endpoint, let's create a class for it
class LoginRequest(BaseModel):
    email: str = Field(..., examples=["sam@gmail.com"])
    password: str = Field(..., examples=["sam123"])
@app.post("/login")
def login(input: LoginRequest):
    try:
        query = text("""
            SELECT * from users WHERE email = :email
                     """)
        result = db.execute(query, {"email": input.email}).fetchone()        # using `fetchone` here, because only one instance is needed for comparing

        if not result:
            
            raise HTTPException(status_code=401, detail= "Invalid email or Password")
        verified_password = bcrypt.checkpw(input.password.encode('utf-8'), result.password.encode('utf-8'))
        
        if not verified_password:
            raise HTTPException(status_code=404, detail="Invalid email or password")
        
        return {
            "Message": "Login Successful"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail= str(e))
    
if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))