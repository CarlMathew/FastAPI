from pydantic import BaseModel, EmailStr
from fastapi import Header
from typing import Optional, Dict


class GettingID(BaseModel):
    id: int


class InsertingData(BaseModel):
    post: str
    userid: int


class DeleteData(BaseModel):
    id: int


class UpdateData(BaseModel):
    post: str
    id: int


class UserID(BaseModel):
    userid: int


class StoredProcedure(BaseModel):
    storedName: str
    parameters: Dict[str, str]


class InsertUser(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    id: int
    email: Optional[str]
    password: Optional[str]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int]


class Posting(BaseModel):
    title: str
    content: str
    published: bool


class title(BaseModel):
    title: str


class updatePost(BaseModel):
    id: int
    title: str
    content: str
