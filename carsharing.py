import uvicorn
from fastapi import FastAPI
from sqlmodel import SQLModel

from db import engine
from routers import cars, web

app = FastAPI()
app.include_router(cars.router)
app.include_router(web.router)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)
