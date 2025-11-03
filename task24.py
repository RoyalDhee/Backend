from fastapi import FastAPI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import uvicorn
import os
from typing import Optional

load_dotenv()

# Setting app version
app = FastAPI(title="Simple Fast API", version="1.0.0")

# Creating dictionary of data
data = [{"name": "Sam Larry", "age": 20, "track": "AI Developer"},
        {"name": "Shola John", "age": 23, "track": "Backend Developer"},
        {"name": "Dazzy Doe", "age": 25, "track": "Frontend Developer"}]

# Creating class of Items


class Item(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    name: Optional[str] = None


# Creating Patch
@app.patch("/edit_data", description="This is to update the database")
def edit_data(id: int, req: Item):
    try:
        existing = data[id]
    except IndexError:
        return {"Message": "Record not found"}

    try:
        updates = req.model_dump(exclude_unset=True)
    except AttributeError:
        updates = req.model_dump(exclude_unset=True)

    if updates:
        existing.update(updates)
        data[id] = existing
        print(data)
        return {"Message": "Data edited", "Data": data}
    else:
        return {"Message": "No fields to update", "Data": data}


# Create delete endpoint
@app.delete("/delete-data/{id}")
def delete_data(id: int):
    try:
        del data[id]
        print(data)
        return {"Message": "Data Deleted", "Data": data}
    except IndexError:
        return {f"Message": "Record not found"}


if __name__ == "__main__":
    print(os.getenv("host"))
    print(os.getenv("port"))
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))
