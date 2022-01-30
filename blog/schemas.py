from typing import List, Optional
from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowBlogInUser(Blog):
    class Config():
        orm_mode = True


class ShowUserInBlog(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[ShowBlogInUser]

    class Config():
        orm_mode = True


class ShowBlog(Blog):
    title: str
    body: str
    author: ShowUserInBlog

    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None