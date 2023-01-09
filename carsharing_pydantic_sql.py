import uvicorn
from fastapi import FastAPI, HTTPException
from sqlmodel import create_engine, SQLModel, Session, select

from schemas_sql import Car, CarInput, CarOutput, TripInput, TripOutput

app = FastAPI()

# engine is representation of DB connection
engine = create_engine(
    "sqlite:///carsharing.db",  # connection string
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=True  # Log generator (not in Prod)
)


# Tell FASTApi to run this when starting up
# Is checking if DB exists and if not creates it
# Using this decorator ensures will run after all code has been loaded, useful for Model/DB migrations
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.get("/api/cars", status_code=200)
# pre 3.10,  def get_cars(size: Optional[str] = None, doors: Optional[int] = None) -> List:
def get_cars(size: str | None = None, doors: int | None = None) -> list:
    """
    Return list of cars.
    :param size: str
    :param doors: int
    :return: list
    """
    with Session(engine) as session:
        query = select(Car)
        if size:
            query = query.where(Car.size == size)
        if doors:
            query = query.where(Car.doors == doors)
        # exec() returns result obj, which we can loop over, with one python object for each row
        # all() converts all rows to python List at once
        return session.exec(query).all()


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


@app.post("/api/cars/", response_model=Car)
def add_car(car_input: CarInput) -> Car:
    """
    Add car
    :param car_input: CarInput
    :return: Car
    """
    with Session(engine) as session:    # is transactional
        new_car = Car.from_orm(car_input)
        session.add(new_car)
        session.commit()
        session.refresh(new_car)
        return new_car


# for debug, make sure we can run the code within the IDE itself
if __name__ == "__main__":
    uvicorn.run("carsharing_pydantic_sql:app", reload=True)
