from passlib.context import CryptContext
from sqlmodel import SQLModel, Field, Relationship, Column, VARCHAR

# SQLModel is pydantic
# https://sqlmodel.tiangolo.com

# python -m pip install "passlib[bcrypt]"
pwd_context = CryptContext(schemes=["bcrypt"])


# Adding Authentication: output schema prevents leaking of password hashes
class UserOutput(SQLModel):
    id: int
    username: str


# Add Unique and Index to the username field, via SQLModel and SQLAlchemy, sa_ stands for sqlalchemy
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column("username", VARCHAR, unique=True, index=True))
    password_hash: str

    def set_password(self, password):
        """ Setting the passwords actually sets password_hash """
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        """ Verify given password by hashing and comparing to password_hash """
        return pwd_context.verify(password, self.password_hash)


# Allows Car models to hold a list
# We can have one pydantic class which holds a collection of another
class TripInput(SQLModel):
    start: int
    end: int
    description: str


class TripOutput(TripInput):
    id: int


# Trip Entity, referenced by Car
# Relations are lazily loaded with SQLModel by default, when retrieving cars
class Trip(TripInput, table=True):
    id: int | None = Field(default=None, primary_key=True)
    car_id: int = Field(foreign_key="car.id")
    # Type hint is in string literals because the Car type is below our Trip class in our file
    car: "Car" = Relationship(back_populates="trips")


# BaseModel inherits __init__, __str__
# Common to have Input and Output models
class CarInput(SQLModel):
    size: str
    fuel: str | None = "electric"
    doors: int
    transmission: str | None = "auto"

    class Config:
        schema_extra = {
            "example": {
                "size": "m",
                "doors": 5,
                "transmission": "manual",
                "fuel": "hybrid"
            }
        }


# Car Entity
class Car(CarInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    trips: list[Trip] = Relationship(back_populates="car")


# CarOutput holds a list of trips: in the SQLModel setup is a Schema
class CarOutput(CarInput):
    id: int
    trips: list[TripOutput] = []
