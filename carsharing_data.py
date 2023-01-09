from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI()
# No real SQL database yet so just list of dicts
db = [
    {"id": 1, "size": "s", "fuel": "gasoline", "doors": 3, "transmission": "auto"},
    {"id": 2, "size": "s", "fuel": "electric", "doors": 3, "transmission": "auto"},
    {"id": 3, "size": "s", "fuel": "gasoline", "doors": 5, "transmission": "manual"},
    {"id": 4, "size": "m", "fuel": "electric", "doors": 3, "transmission": "auto"},
    {"id": 5, "size": "m", "fuel": "hybrid", "doors": 5, "transmission": "auto"},
    {"id": 6, "size": "m", "fuel": "gasoline", "doors": 5, "transmission": "manual"},
    {"id": 7, "size": "l", "fuel": "diesel", "doors": 5, "transmission": "manual"},
    {"id": 8, "size": "l", "fuel": "electric", "doors": 5, "transmission": "auto"},
    {"id": 9, "size": "l", "fuel": "hybrid", "doors": 5, "transmission": "auto"}
]


# @app.get("/api/cars")
# def get_cars():
#     return db

# This is how we can filter the list of dicts
# @app.get("/api/cars")
# def get_cars(size):
#     return [car for car in db if car['size'] == size]

# Make size have a default, so we can check if it is present and user doesn't want filter
# @app.get("/api/cars")
# def get_cars(size=None):
#     if size:
#         return [car for car in db if car['size'] == size]
#     else:
#         return db

# We can have more than one query parameter
# Lets add hints to the parameters ( | means OR)
@app.get("/api/cars")
# pre 3.10,  def get_cars(size: Optional[str] = None, doors: Optional[int] = None) -> List:
def get_cars(size: str | None = None, doors: int | None = None) -> list:
    result = db
    if size:
        return [car for car in db if car['size'] == size]
    if doors:
        return [car for car in db if car['doors'] >= doors]
    return result


# Get a specific car
@app.get("/api/cars/{id}")
def get_car_by_id(id: int) -> dict:
    result = [car for car in db if car['id'] == id]
    # debug line
    # print(f"in get_car_by_id, id = {id}")
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail=f"No car with Id {id}.")


# for debug, make sure we can run the code within the IDE itself
if __name__ == "__main__":
    uvicorn.run("carsharing_data:app", reload=True)
