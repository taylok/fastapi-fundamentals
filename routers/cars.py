from fastapi import Depends, HTTPException, APIRouter, Response
from sqlmodel import Session, select
from starlette import status

from db import get_session
from routers.auth import get_current_user
from schemas import Car, CarOutput, CarInput, TripInput, Trip, User

# Use APIRouter, part of app, and register api operations with the Router
# So we don't need to import app from carsharing anymore
# Allows us to group related operations together
# router = APIRouter()
router = APIRouter(prefix="/api/cars")


# @router.get("/api/cars", status_code=200)
@router.get("/", status_code=200)
# pre 3.10,  def get_cars(size: Optional[str] = None, doors: Optional[int] = None) -> List:
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


# @router.get("/api/cars/{id}", response_model=CarOutput)
@router.get("/{id}", response_model=CarOutput)
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


# @router.post("/api/cars/", response_model=Car)
# fastapi operation asks for a logged-in user because of dependency
@router.post("/", response_model=Car, status_code=200)
def add_car(*, car_input: CarInput, session: Session = Depends(get_session), user: User = Depends(get_current_user),
            response: Response) -> Car:
    """
    Add car
    :param user:
    :param response:
    :param session:
    :param car_input: CarInput
    :return: Car
    """
    new_car = Car.from_orm(car_input)
    session.add(new_car)
    session.commit()
    session.refresh(new_car)
    # Artificially override default status for demo
    response.status_code = status.HTTP_201_CREATED
    return new_car


# @router.delete("/api/cars/{id}", status_code=204)
@router.delete("/{id}", status_code=204)
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


# @router.put("/api/cars/{id}", response_model=Car)
@router.put("/{id}", response_model=Car)
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


# @router.post("/api/cars/{car_id}/trips")
@router.post("/{car_id}/trips")
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
        if new_trip.end < new_trip.start:
            raise BadTripException("Trip end before start")
        car.trips.append(new_trip)
        session.commit()
        session.refresh(new_trip)
        return new_trip
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")


class BadTripException(Exception):
    pass
