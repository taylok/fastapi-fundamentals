from fastapi import APIRouter, Request, Depends, Form, Cookie
from sqlmodel import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from db import get_session
from routers.cars import get_cars

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# Cookies is very similar for Headers if you wish to access them
@router.get("/", response_class=HTMLResponse)
def home(request: Request, cars_cookie: str | None = Cookie(None)):
    # Has the agent visited page before?
    print(cars_cookie)
    # We have to pass a dict containing the request, otherwise FASTApi will give an error
    return templates.TemplateResponse("home.html", {"request": request})


# Arguments without a default in python have to come first, but we like fastapi objects to come first
# and stuff that the user inputs to come later, so that is why the parameter list starts with *.
# It turns everything that comes after the * into a keyword argument. Now order doesn't matter.
# The three dots inside Form means required field, ... belongs to python elipsis class which has no real meaning.
@router.post("/search", response_class=HTMLResponse)
def search(*, size: str = Form(...), doors: int = Form(...), request: Request, session: Session = Depends(get_session)):
    # We call our already coded get_cars, but we do not get the benefit of DI,
    # so have to pass session on to the function
    cars = get_cars(size=size, doors=doors, session=session)
    return templates.TemplateResponse("search_results.html", {"request": request, "cars": cars})
