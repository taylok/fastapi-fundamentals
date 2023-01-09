from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException

from schemas import load_db, CarInput, save_db, CarOutput

app = FastAPI()
# No real SQL database yet so just load pydantic model from json file
db = load_db()


# https://pydantic-docs.helpmanual.io

# Fix returns for object syntax
@app.get("/api/cars")
# pre 3.10,  def get_cars(size: Optional[str] = None, doors: Optional[int] = None) -> List:
def get_cars(size: str | None = None, doors: int | None = None) -> list:
    result = db
    if size:
        return [car for car in db if car.size == size]
    if doors:
        return [car for car in db if car.doors >= doors]
    return result


# Get a specific car
@app.get("/api/cars/{id}")
def get_car_by_id(id: int) -> dict:
    result = [car for car in db if car.id == id]
    # debug line
    # print(f"in get_car_by_id, id = {id}")
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail=f"No car with Id {id}.")


# Takes a pydantic parameter, and is expected to be passed in the request Body
# response_model necessary on type hint for the output. response_model is an
# argument of the decorator
@app.post("/api/cars/", response_model=CarOutput)
def add_car(car: CarInput) -> CarOutput:
    new_car = CarOutput(size=car.size, doors=car.doors,
                        fuel=car.fuel, transmission=car.transmission,
                        id=len(db) + 1)
    db.append(new_car)
    save_db(db)
    return new_car


# for debug, make sure we can run the code within the IDE itself
if __name__ == "__main__":
    uvicorn.run("carsharing_pydantic:app", reload=True)
