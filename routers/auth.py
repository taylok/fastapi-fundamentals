from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from starlette import status

from db import get_session
from schemas import User, UserOutput

URL_PREFIX = "/auth"
router = APIRouter(prefix=URL_PREFIX)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{URL_PREFIX}/token")


# This function has DI
def get_current_user(token: str = Depends(oauth2_scheme),
                     session: Session = Depends(get_session)) -> UserOutput:
    # For demo the token just contains username
    query = select(User).where(User.username == token)
    user = session.exec(query).first()
    if user:
        return UserOutput.from_orm(user)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or password incorrect",
                            headers={"WWW-Authenticate": "Bearer"},)


# Operation at /token, registered with router which has prefix /auth/token
# Depends() means fastapi will try to create an OAuth2 password request form
# In reality we would use JWT but this is just demo
@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    query = select(User).where(User.username == form_data.username)
    user = session.exec(query).first()
    if user and user.verify_password(form_data.password):
        return {"access_token": user.username, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")


