from sqlalchemy.orm import Session
from .. import models
from fastapi import HTTPException, status
from ..hash import Hash
from ..schemas import User

def create_user(request:User, db:Session):
    encryptedPassword= Hash.bcrypt(request.password);
    new_user = models.User(name=request.name, email=request.email, password=encryptedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
def get_user_by_id(id: int, db:Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no user with id {id}")
    return user