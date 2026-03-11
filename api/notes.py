from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Note
from database import get_db
from schemas import CreateNote, UpdateNoteContent
import auth, schemas, models

router = APIRouter()

# TO REDO
@router.post("/", response_model=schemas.Note)
def add_note(create_note: CreateNote, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
  new_note = Note(
    title=create_note.title,
    content=create_note.content,
    user_id=current_user.id
  )

  db.add(new_note)
  db.commit()
  db.refresh(new_note)
  return new_note

# TO REDO
@router.get("/todo")
def get_todo_notes(db: Session = Depends(get_db)):
  notes = db.query(Note).where(Note.is_done == False).all()
  return notes

# TO REDO
@router.get("/{id}")
def get_note(id: int, db: Session = Depends(get_db)):
  note = db.query(Note).where(Note.id == id).first()
  return note

# TO REDO TO GENERAL PATCH
@router.put("/content/{id}")
def update_note_content(id: int, update_content: UpdateNoteContent, db: Session = Depends(get_db)):
  note = db.query(Note).where(Note.id == id).first()

  if not note:
    raise HTTPException(
      status_code=404,
      detail="ID not found"
    )

  note.content = update_content.content
  db.commit()
  db.refresh(note)
  return note

# TO REDO
@router.delete("/{id}")
def delete_note(id: int, db: Session = Depends(get_db)):
  note_to_delete = db.query(Note).where(Note.id == id).first()

  if not note_to_delete:
    raise HTTPException(
      status_code=404,
      detail="ID not found"
    )

  db.delete(note_to_delete)
  db.commit()
  return note_to_delete

# TO DELETE / ADMIN
# @router.get("/")
# def get_notes(db: Session = Depends(get_db)):
#   notes = db.query(Note).all()
#   return notes