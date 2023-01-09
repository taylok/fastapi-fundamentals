from fastapi import APIRouter, Request, Form, Depends
from sqlmodel import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from db import get_session
from routers.cars import get_cars

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# Method signature has '*' to everything after is a kwarg. This gets around putting arguments without a default
# after arguments with a default. Normally python rules that arguments without default should come first.  It is
# common in fastapi
# The Form(...) tells fastapi to handle the form data as required (but we can put a value for default value)
# The tree dots are python class 'ellipsis', but python doesn't specify what it means.
# Call the get_cars function that we already have to get the cars.  In this case fastapi does not inject the session
# when we call get_cars like this since it is not called as a fastapi operation, so we pass session to it.
@router.post("/search", response_class=HTMLResponse)
def search(*, size: str = Form(...), doors: int = Form(...), request: Request, session: Session = Depends(get_session)):
    cars = get_cars(size=size, doors=doors, session=session)
    return templates.TemplateResponse("search_results.html", {"request": request, "cars": cars})
