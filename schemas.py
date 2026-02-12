# PYDANTIC SCHEMAS

from pydantic import BaseModel, EmailStr
from typing import Optional

class CreateUser(BaseModel):
  email: EmailStr
  name: str

class CreateNote(BaseModel):
  title: str
  content: Optional[str] = None
  user_id: Optional[int] = None

class UpdateNoteContent(BaseModel):
  content: Optional[str] = None

class UpdateNoteUserId(BaseModel):
  user_id: Optional[int] = None