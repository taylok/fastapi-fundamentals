import json

from pydantic import BaseModel


# Allows Car models to hold a list
# We can have one pydantic class which holds a collection of another
class TripInput(BaseModel):
    start: int
    end: int
    description: str


class TripOutput(TripInput):
    id: int


# BaseModel inherits __init__, __str__
# Common to have Input and Output models
class CarInput(BaseModel):
    size: str
    fuel: str | None = "electric"
    doors: int
    transmission: str | None = "auto"


# CarOutput holds a list of trips
class CarOutput(CarInput):
    id: int
    trips: list[TripOutput] = []


# The return statement loads objects from a json file which is a list of dicts,
# then we loop over that list and pass each obj to pydantic method Car.parse_obj
def load_db() -> list[CarOutput]:
    """ Load a list of Car objects from a JSON file """
    with open("cars_with_trips.json") as f:
        return [CarOutput.parse_obj(obj) for obj in json.load(f)]


# Open cars.json in write mode, convert each car into a dict
def save_db(cars: list[CarOutput]):
    with open("cars_with_trips.json", "w") as f:
        json.dump([car.dict() for car in cars], f, indent=4)
