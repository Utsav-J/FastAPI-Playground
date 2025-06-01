from pydantic import BaseModel

class Blog(BaseModel):
    title:str
    body:str

class BlogResponse(BaseModel):
    title:str
    body:str
    # this will omit the id field when returning the blog
    class Config():
        orm_mode = True