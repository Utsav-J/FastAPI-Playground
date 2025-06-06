from fastapi import HTTPException,status, APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..hash import Hash
from fastapi.security import OAuth2PasswordRequestForm
from .token import create_access_token
router = APIRouter(
    tags=['auth']
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm=Depends(), db:Session= Depends(get_db)):
    # sample user: first@first.com , string
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    if not Hash.verify(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid password')
    # generate a JWT token and return that
    access_token = create_access_token(data={"sub": user.email})
    return {'access_token':access_token, 'token_type':"bearer"}
