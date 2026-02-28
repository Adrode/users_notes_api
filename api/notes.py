from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User, Note
from database import get_db
from schemas import CreateNote, UpdateNoteContent, UpdateNoteUserId

router = APIRouter()

@router.get("/todo")
def get_todo_notes(db: Session = Depends(get_db)):
  notes = db.query(Note).where(Note.is_done == False).all()
  return notes

@router.get("/{id}")
def get_note(id: int, db: Session = Depends(get_db)):
  note = db.query(Note).where(Note.id == id).first()
  return note

@router.get("/")
def get_notes(db: Session = Depends(get_db)):
  notes = db.query(Note).all()
  return notes

@router.post("/")
def add_note(create_note: CreateNote, db: Session = Depends(get_db)):
  new_note = Note(title=create_note.title, content=create_note.content, user_id=create_note.user_id)

  if not db.query(User).where(User.id == new_note.user_id).first():
    raise HTTPException(
      status_code=404,
      detail="User ID not found"
    )

  db.add(new_note)
  db.commit()
  db.refresh(new_note)
  return new_note

@router.put("/user_id/{id}")
def update_note_user_id(id: int, update_user_id: UpdateNoteUserId, db: Session = Depends(get_db)):
  note = db.query(Note).where(Note.id == id).first()

  if not note:
    raise HTTPException(
      status_code=404,
      detail="ID not found"
    )
  
  note.user_id = update_user_id.user_id
  db.commit()
  db.refresh(note)
  return note

@router.put("/{id}")
def update_note_content(id: int, update_note_content: UpdateNoteContent, db: Session = Depends(get_db)):
  updated_note = db.query(Note).where(Note.id == id).first()

  if not updated_note:
    raise HTTPException(
      status_code=404,
      detail="ID not found"
    )

  updated_note.content = update_note_content.content
  db.commit()
  db.refresh(updated_note)
  return updated_note

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