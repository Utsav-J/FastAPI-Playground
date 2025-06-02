from fastapi import APIRouter, Depends
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import User, UserResponse
from ..repository import user

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.post('/')
def createUser(request:User, db:Session=Depends(get_db)):
    return user.create_user(request, db)

@router.get('/{id}',response_model=UserResponse)
def getUser(id:int, db:Session=Depends(get_db)):
    return user.get_user_by_id(id, db)