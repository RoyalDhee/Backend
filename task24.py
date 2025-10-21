from fastapi import FastAPI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import uvicorn
import os

load_dotenv()

# Setting app version
app = FastAPI(title="Simple Fast API", version="1.0.0")

# Creating dictionary of data
data = [{"name": "Sam LArry", "age": 20, "track": "AI Developer"},
        {"name": "Bahubali", "age": 23, "track": "Backend Developer"},
        {"name": "John Doe", "age": 25, "track": "Frontend Developer"}]

# Creating class of Items


class Item(BaseModel):
    name: str = Field(..., example="Jayboy")
    age: int = Field(..., example=20)
    track: str = Field(..., example="Devops Engineer")

# Creating Patch


@app.patch("/", description=)
