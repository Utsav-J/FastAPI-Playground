import uvicorn 
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def index():
    return {
        'name': "Utsav",
        'age': 20
    }

@app.get('/blogs')
def blogs(limit=5, published:bool=True, sort: Optional[str]=None):
    if published:
        return {
        'data': f"{limit} blogs from the database"
        }
    else:
        return {
            'data': 'unpublished shi'
        }

@app.get('/about')
def about():
    return {
        'data': "About Page"
    }

@app.get('/blog/{id}')
def getBlog(id:int):
    return {
        'data': id
    }


class Blog(BaseModel):
    title:str
    body:str
    published: Optional[str]

@app.post('/blog')
def createBlog(blog:Blog):
    return {'data': f'{blog.title} CREATED'}


# if __name__ == '__main__':
#     uvicorn.run(app,host='127.0.0.1', port=9000)