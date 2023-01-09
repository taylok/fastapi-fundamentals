from datetime import datetime

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def welcome():
    """ Return a friendly welcome message """
    return {'message': "Welcome to the Car Sharing Service!"}


@app.get("/name")
def welcome(name):
    """ Return a friendly welcome message """
    return {'message': f"Welcome, {name} ,to the Car Sharing Service!"}


@app.get("/date")
def date():
    """ Return current date/time """
    return {'date': datetime.now()}
