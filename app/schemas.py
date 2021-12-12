import datetime as dt
from pydantic import BaseModel, EmailStr


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


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    owner_id: int = 0


class PostResponse(BaseModel):
    pk: int
    title: str
    content: str
    published: bool
    owner: UserResponse

    class Config:
        orm_mode = True


class PostVoteResponse(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class Vote(BaseModel):
    post_id: int
    direct: int
