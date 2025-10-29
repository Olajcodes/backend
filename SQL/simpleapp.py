from database import db
from fastapi import FastAPI, Depends, HTTPException # To handle ty exception error
from pydantic import BaseModel, Field
from sqlalchemy import text
import os
from dotenv import load_dotenv
import bcrypt
import uvicorn
from middleware import create_token, verify_token


load_dotenv()

app = FastAPI(title="Simple App", version="1.0.0")

expiry_time = int(os.getenv("token_time"))

class Simple(BaseModel):
    name: str = Field(..., example= "Abdullateef")
    email: str = Field(..., example= "abc@gmail.com")
    password: str = Field(..., example= "abdul123")
    userType: str = Field(..., example= "student")
    gender: str = Field(..., example= "Male")

class LoginRequest(BaseModel):
    email: str = Field(..., example= "sam@gmail.com")
    password: str = Field(..., example= "sam123")
    
class CourseRequest(BaseModel):
    title: str = Field(..., example="Backend Course")
    level: str = Field(..., example="Beginner")
    
class Enroll(BaseModel):
    courseId: int = Field(..., example=1)
    
@app.get("/", description="This endpoint returns a welcome message")       # Adding a decorator 
def root():
    return {"Message": "Welcome to my FASTAPI Application"}

@app.post("/signup")
def signUp(input: Simple):
    try:
        duplicate_query = text(""" SELECT * FROM users WHERE email = :email """)
        # Checking for an existing details
        existing = db.execute(duplicate_query, {"email": input.email}).fetchone()
        
        if existing is not None:
            print("Email already exists")
            raise HTTPException(status_code=400, detail="Email already exists")
        
        query = text("""
              INSERT INTO users (name, email, password, userType, gender)
              VALUES(:name, :email, :password, :userType, :gender)       # We used ":" as a placeholder here.
        """)
        # To encrypt our password (i.e, Hashing), we need to install bcrypt
        salt = bcrypt.gensalt()     # Salt is needed here to automatically generate random values to the enconded password created to differentiate from each other
        hashedPassword = bcrypt.hashpw(input.password.encode('utf-8'), salt)
        print(hashedPassword)       # printing this to the terminal
        
        # Mapping data
        data = {"name": input.name, "email": input.email, "password": hashedPassword, "userType": input.userType, "gender": input.gender}
        db.execute(query, data)
        db.commit()     # Did this to commit changes after inputting.
        
        return{
            "message": "User created successfully",
            "data": {"name": input.name, "email": input.email, "userType": input.userType, "gender": input.gender}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/login")
def login(input: LoginRequest):
    try:
        query = text(""" 
         SELECT * from users WHERE email = :email 
        """)
        result = db.execute(query, {"email": input.email}).fetchone()        # using `fetchone` here, because only one instance is needed for comparing
        if not result:
            raise HTTPException(status_code=404, detail= "Invalid email or Password")
        
        verified_password = bcrypt.checkpw(input.password.encode('utf-8'), result.password.encode('utf-8'))
        
        if not verified_password:
            raise HTTPException(status_code=404, detail="Invalid email or password")
        
        encoded_token = create_token({
            "id": result.id,
            "email": result.email,
            "userType": result.userType
        }, expiry_time)
        
        return {
            "Message": "Login Successful",
            "token": encoded_token
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail= str(e))
    

@app.post("/courses")
def addcourses(input: CourseRequest, user_data = Depends(verify_token)):
    try:
        print(user_data)
        if user_data.userType != 'admin':
            raise HTTPException(status_code=401, detail="You are not authorized to add a course")
        query = text(""" 
            INSERT INTO courses (title, level) 
            VALUES(:title, :level)
        """)
        db.execute(query, {"title": input.title, "level": input.level})
        db.commit()
        return {
            "Message": "Course added successfully",
            "data": {"title": input.title, "level": input.level}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/enroll")
def enroll_course(input: Enroll, details = Depends(verify_token)):
    try:
        query = text("""
            SELECT * FROM users
            WHERE id = :id
        """)
        existing = db.execute(query, {"id": details["id"]}).fetchone()
        if existing.userType != "student":
            raise HTTPException(status_code=400, detail="You are not authorized to enroll!")
        enroll_query = text("""
            INSERT INTO enrollments(userId, courseId)
            VALUES (:userId, :courseId)              
        """)
        db.execute(enroll_query, {"userId": details["id"], "courseId": input.courseId})
        db.commit()
        
        return {
            "message": "User enrolled successfully!",
            "data": {
                "UserId": details["id"],
                "courseId": input.courseId
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))