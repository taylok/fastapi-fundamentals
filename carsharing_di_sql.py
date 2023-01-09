import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import create_engine, SQLModel, Session, select

from schemas_sql import Car, CarInput, TripInput, TripOutput, Trip, CarOutput

app = FastAPI()
# This example uses dependency injection instead of creating a session in every REST function

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


# def get_session(): return Session(engine)
# This variant turns get session into a generator, yield gives control to
# caller and returns here to finish the with block, effectively wrapping the
# whole call (e.g. get_cars()) in the with block. If exception occurs the session
# will automatically roll back, giving some protection against data corruption
def get_session():
    with Session(engine) as session:
        yield session


@app.get("/api/cars", status_code=200)
# pre 3.10,  def get_cars(size: Optional[str] = None, doors: Optional[int] = None) -> List:
# Tell FASTApi in order to work properly my function needs a session object, we pass session as a value to Depends()
# FASTApi will get_session() for us whenever this function runs.
# This is good for testing, so we can pass a mock session object
def get_cars(size: str | None = None, doors: int | None = None, session: Session = Depends(get_session)) -> list:
    """
    Return list of cars.
    :param session:
    :param size: str
    :param doors: int
    :return: list
    """
    query = select(Car)
    if size:
        query = query.where(Car.size == size)
    if doors:
        query = query.where(Car.doors == doors)
    # exec() returns result obj, which we can loop over, with one python object for each row
    # all() converts all rows to python List at once
    return session.exec(query).all()


# response_model=Car will not show Relationship
# response_model=CarOutput will who Relationships
@app.get("/api/cars/{id}", response_model=CarOutput)
def get_car_by_id(id: int, session: Session = Depends(get_session)) -> Car:
    """
    Get a specific car
    :param session:
    :param id: int
    :return: CarOutput
    """
    car = session.get(Car, id)  # like select but returns single object
    if car:
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with Id {id}.")


@app.post("/api/cars/", response_model=Car)
def add_car(car_input: CarInput, session: Session = Depends(get_session)) -> Car:
    """
    Add car
    :param session:
    :param car_input: CarInput
    :return: Car
    """
    new_car = Car.from_orm(car_input)
    session.add(new_car)
    session.commit()
    session.refresh(new_car)
    return new_car


@app.delete("/api/cars/{id}", status_code=204)
def remove_car(id: int, session: Session = Depends(get_session)) -> None:
    """
    Remove car
    :param session:
    :param id: int
    :return: status_code
    """
    car = session.get(Car, id)  # like select but returns single object
    if car:
        session.delete(car)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No car with Id {id}.")


@app.put("/api/cars/{id}", response_model=Car)
def change_car(id: int, new_data: CarInput, session: Session = Depends(get_session)) -> Car:
    """
    Change car
    :param session:
    :param id: int
    :param new_data: CarInput
    :return: CarOutput
    """
    car = session.get(Car, id)
    if car:
        # There are other ways to copy all the data from input to car
        car.fuel = new_data.fuel
        car.transmission = new_data.transmission
        car.size = new_data.size
        car.doors = new_data.doors
        session.commit()
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")


@app.post("/api/cars/{car_id}/trips")
def add_trip(car_id: int, trip_input: TripInput, session: Session = Depends(get_session)) -> Trip:
    """
    Add trip to car
    :param trip_input: TripInput
    :param session:
    :param car_id: int
    :return: Trip
    """
    car = session.get(Car, car_id)
    if car:
        new_trip = Trip.from_orm(trip_input, update={'car_id': car_id})
        car.trips.append(new_trip)
        session.commit()
        session.refresh(new_trip)
        return new_trip
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")


# for debug, make sure we can run the code within the IDE itself
if __name__ == "__main__":
    uvicorn.run("carsharing_di_sql:app", reload=True)
