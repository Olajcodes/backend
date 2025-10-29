import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi import Request, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import security

load_dotenv()

bearer = HTTPBearer()

secret_key= os.getenv("secret_key")

def create_token(details:dict, expiry:int):
    expire= datetime.now() + timedelta(minutes=expiry)

    details.update({"exp":expire})
    # sign jwt
    encoder_jwt=jwt.encode(details, secret_key)
    return encoder_jwt

def verify_token(request: HTTPAuthorizationCredentials= Security (bearer)):
    # payload = request.headers.get("Authorization")
    token= request.credentials
    
    # token = payload.split(" ")[1]
    verify_token=jwt.decode(token, secret_key, algorithms=["HS256"])
    
    # expiry_time= verify_token.get("exp")

    return{"email":verify_token.get("email"), "userType":verify_token.get("userType"), "id": verify_token.get("id")}
