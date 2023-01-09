from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException

from schemas_nested import load_db, CarInput, save_db, CarOutput, TripInput, TripOutput

app = FastAPI()
# No real SQL database yet so just load pydantic model from json file
db = load_db()


@app.get("/api/cars", status_code=200)
# pre 3.10,  def get_cars(size: Optional[str] = None, doors: Optional[int] = None) -> List:
def get_cars(size: str | None = None, doors: int | None = None) -> list:
    """
    Return list of cars.
    """
    result = db
    if size:
        return [car for car in db if car.size == size]
    if doors:
        return [car for car in db if car.doors >= doors]
    return result


@app.get("/api/cars/{id}")
def get_car_by_id(id: int) -> dict:
    """
    Get a specific car
    :param id: int
    :return: dict
    """
    result = [car for car in db if car.id == id]
    # debug line
    # print(f"in get_car_by_id, id = {id}")
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail=f"No car with Id {id}.")


@app.post("/api/cars", response_model=CarOutput)
def add_car(car: CarInput) -> CarOutput:
    """
    Add car
    :param car: CarInput
    :return: CarOutput
    """
    new_car = CarOutput(size=car.size, doors=car.doors,
                        fuel=car.fuel, transmission=car.transmission,
                        id=len(db) + 1)
    db.append(new_car)
    save_db(db)
    return new_car


@app.delete("/api/cars/{id}", status_code=204)
def remove_car(id: int) -> None:
    """
    Remove car
    :param id: int
    :return: status_code
    """
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        db.remove(car)
        save_db(db)
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")


@app.put("/api/cars/{id}", response_model=CarOutput)
def change_car(id: int, new_data: CarInput) -> CarOutput:
    """
    Change car
    :param id: int
    :param new_data: CarInput
    :return: CarOutput
    """
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        car.fuel = new_data.fuel
        car.transmission = new_data.transmission
        car.size = new_data.size
        car.doors = new_data.doors
        save_db(db)
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")


@app.post("/api/cars/{car_id}/trips")
def add_trip(car_id: int, trip: TripInput) -> TripOutput:
    """
    Add trip to car
    :param car_id: int
    :param trip: TripInput
    :return: TripOutput
    """
    matches = [car for car in db if car.id == car_id]
    if matches:
        car = matches[0]
        new_trip = TripOutput(id=len(car.trips) + 1,
                              start=trip.start, end=trip.end,
                              description=trip.description)
        car.trips.append(new_trip)
        save_db(db)
        return new_trip
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")


# for debug, make sure we can run the code within the IDE itself
if __name__ == "__main__":
    uvicorn.run("carsharing_pydantic_nested:app", reload=True)
