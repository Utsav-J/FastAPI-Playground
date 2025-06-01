from fastapi import FastAPI,Depends,status, Response, HTTPException
from .schemas import Blog
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog',status_code=status.HTTP_201_CREATED)
def create(request: Blog, db:Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog')
def getBlogs(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code = status.HTTP_200_OK)
def getBlogs(id:int,response:Response, db:Session=Depends(get_db)):
    result = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"There is no blog of id : {id}"
            )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {
        #     "detail":f"There is no blog of id : {id}"
        # }
    return result


@app.delete('/blog/{id}', status_code = status.HTTP_204_NO_CONTENT)
def deleteBlog(id:int, db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    blog.delete(synchronize_session=False)
    db.commit()
    return {"GONE"}