from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import List
from ..schemas import BlogResponse, Blog
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
router = APIRouter()

# CREATE A BLOG
@router.post('/blog',status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: Blog, db:Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title,body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# GET ALL BLOGS
@router.get('/blog', response_model = List[BlogResponse], tags=['blogs'])
def getBlogs(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

# get specific blog by id
@router.get('/blog/{id}', status_code = status.HTTP_200_OK, response_model=BlogResponse, tags=['blogs'])
def getBlogs(id:int,response:Response, db:Session=Depends(get_db)):
    result = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"There is no blog of id : {id}"
            )
    return result

# DELETE A SPECIFIC BLOG
@router.delete('/blog/{id}', status_code = status.HTTP_204_NO_CONTENT, tags=['blogs'])
def deleteBlog(id:int, db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    blog.delete(synchronize_session=False)
    db.commit()
    return {"GONE"}

# EDIT A BLOG
@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def editBlog(id:int,request:Blog, db:Session=Depends(get_db)):
    res = db.query(models.Blog).filter(models.Blog.id == id)
    if not res.first():
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="There is no such blog")
    res.update({models.Blog.title:request.title, models.Blog.body:request.body}, synchronize_session=False)
    db.commit()
    return res
