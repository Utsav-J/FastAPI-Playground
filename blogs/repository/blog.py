from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models
from ..schemas import Blog

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create_blog(request:Blog,db:Session):
    new_blog = models.Blog(title=request.title,body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete_blog(id:int,db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"There is no such blog with id: {id}")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"GONE"}

def update_blog(id:int, request:Blog, db:Session):
    res = db.query(models.Blog).filter(models.Blog.id == id)
    if not res.first():
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="There is no such blog")
    res.update({models.Blog.title:request.title, models.Blog.body:request.body}, synchronize_session=False)
    db.commit()
    return res

def get_blog_by_id(id:int, db:Session):
    result = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"There is no blog of id : {id}"
            )
    return result