from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import InvalidRequestError
from models import Note
from database import get_db
import auth, schemas, models

router = APIRouter()

@router.post("/", response_model=schemas.Note)
def add_note(
    create_note: schemas.CreateNote,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
  ):
  new_note = Note(
    title=create_note.title,
    content=create_note.content,
    user_id=current_user.id
  )

  db.add(new_note)
  db.commit()
  db.refresh(new_note)
  return new_note

@router.get("/", response_model=list[schemas.Note])
def get_notes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
  ):
  notes = db.query(Note).where(Note.user_id == current_user.id).all()
  return notes

# TO REDO
# @router.get("/todo")
# def get_todo_notes(db: Session = Depends(get_db)):
#   notes = db.query(Note).where(Note.is_done == False).all()
#   return notes

# # TO REDO
# @router.get("/{id}")
# def get_note(id: int, db: Session = Depends(get_db)):
#   note = db.query(Note).where(Note.id == id).first()
#   return note

@router.patch("/{id}", response_model=schemas.Note)
def update_note_content(
    id: int,
    update_data: schemas.UpdateNote,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
  ):
  note = db.query(Note).where(Note.id == id).first()

  if not note:
    raise HTTPException(
      status_code=404,
      detail="Not found"
    )

  if not note.user_id == current_user.id:
    raise HTTPException(
      status_code=401,
      detail="Not authorized"
    )

  update = update_data.model_dump(exclude_unset=True) # model_dump robi dict z obiektu, exclude_unset odrzuca właściwości które mają wartość None
  for key, value in update.items():
    setattr(note, key, value) # (object, właściwość do zmiany, nowa wartość)
  # powyższe do zanotowania
  db.commit()
  db.refresh(note)
  return note

# TO REDO
@router.delete("/{id}", response_model=schemas.Note)
def delete_note(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)  
  ):
  note = db.query(Note).where(Note.id == id).first()

  if not note:
    raise HTTPException(
      status_code=404,
      detail="ID not found"
    )
  
  if not note.user_id == current_user.id:
    raise HTTPException(
      status_code=401,
      detail="Not authorized"
    )

  db.delete(note)
  db.commit()
  return note