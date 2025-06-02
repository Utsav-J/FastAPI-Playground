from fastapi import APIRouter, Depends, status, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import User, UserResponse
from ..hash import Hash
from .. import models
router = APIRouter()


@router.post('/user', tags=['user'])
def createUser(request:User, db:Session=Depends(get_db)):
    encryptedPassword= Hash.bcrypt(request.password);
    new_user = models.User(name=request.name, email=request.email, password=encryptedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/user/{id}',response_model=UserResponse, tags=['user'])
def getUser(id:int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no user with id {id}")
    return user