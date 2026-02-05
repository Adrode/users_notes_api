# PYDANTIC SCHEMAS

from pydantic import BaseModel
from typing import Optional

class CreateUser(BaseModel):
  email: str
  name: str

class CreateNote(BaseModel):
  title: str
  content: Optional[str] = None
  user_id: Optional[int] = None

class UpdateNoteContent(BaseModel):
  content: Optional[str] = None