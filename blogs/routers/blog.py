from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import List
from ..schemas import BlogResponse, Blog
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..repository import blog

router = APIRouter(
    prefix='/blog',
    tags=['blogs']
)

# GET ALL BLOGS
@router.get('/', response_model = List[BlogResponse])
def getBlogs(db:Session=Depends(get_db)):
    return blog.get_all(db)

# CREATE A BLOG
@router.post('/',status_code=status.HTTP_201_CREATED)
def create(request: Blog, db:Session=Depends(get_db)):
    return blog.create_blog(request, db)


# get specific blog by id
@router.get('/{id}', status_code = status.HTTP_200_OK, response_model=BlogResponse)
def getBlogs(id:int,response:Response, db:Session=Depends(get_db)):
    return blog.get_blog_by_id(id, db)

# DELETE A SPECIFIC BLOG
@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def deleteBlog(id:int, db:Session=Depends(get_db)):
    return blog.delete_blog(id,db)

# EDIT A BLOG
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def editBlog(id:int,request:Blog, db:Session=Depends(get_db)):
    return blog.update_blog(id, request, db)
