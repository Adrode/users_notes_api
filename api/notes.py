from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import auth, schemas, models

router = APIRouter()

note_exception = HTTPException(
  status_code=404,
  detail="Not found"
)

user_id_exception = HTTPException(
  status_code=401,
  detail="Not authorized"
)

@router.post("/", response_model=schemas.Note)
def add_note(
  create_note: schemas.CreateNote,
  db: Session = Depends(get_db),
  current_user: models.User = Depends(auth.get_current_user)
):
  new_note = models.Note(
    title=create_note.title,
    content=create_note.content,
    user_id=current_user.id
  )

  db.add(new_note)
  db.commit()
  db.refresh(new_note)
  return new_note

@router.get("/{id}", response_model=schemas.Note)
def get_note(
  id: int,
  db: Session = Depends(get_db),
  current_user: models.User = Depends(auth.get_current_user)  
):
  note = db.query(models.Note).where(models.Note.id == id).first()

  if not note:
    raise note_exception
  
  if not note.user_id == current_user.id:
    raise user_id_exception
  
  return note

@router.get("/", response_model=list[schemas.Note])
def get_notes(
  db: Session = Depends(get_db),
  current_user: models.User = Depends(auth.get_current_user)
):
  notes = db.query(models.Note).where(models.Note.user_id == current_user.id).all()
  return notes

@router.patch("/is_done/{id}", response_model=schemas.Note)
def update_note_is_done(
  id: int,
  update_data: schemas.UpdateNoteIsDone,
  db: Session = Depends(get_db),
  current_user: models.User = Depends(auth.get_current_user)
):
  note = db.query(models.Note).where(models.Note.id == id).first()

  if not note:
    raise note_exception
  
  if not note.user_id == current_user.id:
    raise user_id_exception
  
  note.is_done = update_data.is_done
  db.commit()
  db.refresh(note)
  return note

@router.patch("/{id}", response_model=schemas.Note)
def update_note(
  id: int,
  update_data: schemas.UpdateNote,
  db: Session = Depends(get_db),
  current_user: models.User = Depends(auth.get_current_user)
):
  note = db.query(models.Note).where(models.Note.id == id).first()

  if not note:
    raise note_exception
  
  if not note.user_id == current_user.id:
    raise user_id_exception

  update = update_data.model_dump(exclude_unset=True) # model_dump robi dict z obiektu, exclude_unset usuwa pola których nie było w request body
  for key, value in update.items():
    setattr(note, key, value) # (object, właściwość do zmiany, nowa wartość)
  # powyższe do zanotowania
  db.commit()
  db.refresh(note)
  return note

@router.delete("/{id}", response_model=schemas.Note)
def delete_note(
  id: int,
  db: Session = Depends(get_db),
  current_user: models.User = Depends(auth.get_current_user)  
):
  note = db.query(models.Note).where(models.Note.id == id).first()

  if not note:
    raise note_exception
  
  if not note.user_id == current_user.id:
    raise user_id_exception

  db.delete(note)
  db.commit()
  return note