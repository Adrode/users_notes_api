from pydantic import BaseModel, EmailStr
from typing import Optional

class CreateUser(BaseModel):
  email: EmailStr
  name: str
  password: str

class User(BaseModel):
  id: int
  email: EmailStr
  name: str

  class Config:
    from_attributes: True

class CreateNote(BaseModel):
  title: str
  content: Optional[str] = None

class Note(BaseModel):
  id: int
  title: str
  content: str
  is_done: bool

  class Config:
    from_attributes: True

class UpdateNote(BaseModel):
  title: Optional[str] = None
  content: Optional[str] = None
  is_done: Optional[bool] = False

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  email: str | None = None