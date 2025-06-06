from pydantic import BaseModel
from typing import List
class Blog(BaseModel):
    title:str
    body:str

class User(BaseModel):
    name:str
    email:str
    password:str

class UserResponse(BaseModel):
    name:str
    email:str
    blogs: List[Blog]
    class Config():
        orm_mode=True

class BlogResponse(BaseModel):
    title:str
    body:str
    user_id:int
    creator: UserResponse
    # this will omit the id field when returning the blog
    class Config():
        orm_mode = True

class Login(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
