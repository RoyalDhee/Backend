from fastapi import FastAPI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import uvicorn
import os

load_dotenv()

app = FastAPI(title="Simple Fast API", version="1.0.0")
data = [{"name": "Sam LArry", "age": 20, "track": "AI Developer"},
        {"name": "Bahubali", "age": 23, "track": "Backend Developer"},
        {"name": "John Doe", "age": 25, "track": "Frontend Developer"}]


class Item(BaseModel):
    name: str = Field(..., example="Perpetual")
    age: int = Field(example=25)
    track: str = Field(example="Fullstack Developer")


@app.get("/", description="This endpoint just returns a particular message")
def root():
    return {"message": "Welcome to my FastAPI Application"}


@app.get("/get-data")
def get_data():
    return data


@app.post("/create-data")
def create_data(req: Item):
    data.append(req.dict())
    print(data)
    return {"Message": "Data Received", "Data": data}


@app.put("/update-data/{id}")
def update_data(id: int, req: Item):
    data[id] = req.dict()
    print(data)
    return {"Message": "Data updated", "Data": data}


@app.patch("/edit_data/{id}")
def edit_data(id: int, req: Item):
    keys = data[id].keys()
    values = data[id].values()
    for key, value in req.dict().items():
        data[id][key] = value
    print(data)
    return {"Message": "Data Edited", "Data": data}


if __name__ == "__main__":
    print(os.getenv("host"))
    print(os.getenv("port"))
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))
