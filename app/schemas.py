import datetime as dt
from pydantic import BaseModel, EmailStr


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class PostResponse(BaseModel):
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    email: str
    created_at: dt.date

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
