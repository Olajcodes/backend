from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os


load_dotenv()

app = FastAPI