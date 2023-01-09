import json

from pydantic import BaseModel


# BaseModel inherits __init__, __str__
# Common to have Input and Output models
class CarInput(BaseModel):
    size: str
    fuel: str | None = "electric"
    doors: int
    transmission: str | None = "auto"


class CarOutput(CarInput):
    id: int


# The return statement loads objects from a json file which is a list of dicts,
# then we loop over that list and pass each obj to pydantic method Car.parse_obj
def load_db() -> list[CarOutput]:
    """ Load a list of Car objects from a JSON file """
    with open("cars.json") as f:
        return [CarOutput.parse_obj(obj) for obj in json.load(f)]


# Open cars.json in write mode, convert each car into a dict
def save_db(cars: list[CarOutput]):
    with open("cars.json", "w") as f:
        json.dump([car.dict() for car in cars], f, indent=4)
