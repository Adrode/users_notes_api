from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
import models, schemas, auth

router = APIRouter()

@router.get("/users")
def get_users(
  db: Session = Depends(get_db),
  admin: models.User = Depends(auth.get_current_admin)
):
  return db.query(models.User).all()

@router.post("/users")
def add_user(
  create_user: schemas.CreateUser,
  db: Session = Depends(get_db),
  admin: models.User = Depends(auth.get_current_admin)
):
  try:
    user = models.User(
      email=create_user.email,
      name=create_user.name,
      hashed_password=auth.hash_password(create_user.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
  except IntegrityError:
    raise HTTPException(
      status_code=400,
      detail="Bad request"
    )

@router.patch("/users/{id}")
def update_user(
  id: int,
  update_data: schemas.AdminUpdateUser,
  db: Session = Depends(get_db),
  admin: models.User = Depends(auth.get_current_admin)
):
  try:
    user = db.query(models.User).where(models.User.id == id).first()

    if not user:
      raise HTTPException(
        status_code=404,
        detail="Not found"
      )

    update = update_data.model_dump(exclude_unset=True)
    for key, value in update.items():
      setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user
  except IntegrityError:
    raise HTTPException(
      status_code=400,
      detail="Bad request"
    )
  
@router.delete("/users/{id}")
def delete_user(
  id: int,
  db: Session = Depends(get_db),
  admin: models.User = Depends(auth.get_current_admin)
):
  user = db.query(models.User).where(models.User.id == id).first()

  db.delete(user)
  db.commit()
  return user

@router.get("/notes")
def get_notes(
  db: Session = Depends(get_db),
  admin: models.User = Depends(auth.get_current_admin)
):
  return db.query(models.Note).join(models.User).all()

@router.get("/notes/{user_id}")
def get_notes_by_user_id(
  user_id: int,
  db: Session = Depends(get_db),
  admin: models.User = Depends(auth.get_current_admin)
):
  user = db.query(models.User).where(models.User.id == user_id).first()
  
  if not user:
    raise HTTPException(
      status_code=404,
      detail="Not found"
    )

  return {
    "username": user.name,
    "notes": user.notes
  }

@router.post("/notes")
def add_note(
  create_note: schemas.CreateNote,
  db: Session = Depends(get_db),
  admin: models.User = Depends(auth.get_current_admin)
):
  try:
    note = models.Note(
      title=create_note.title,
      content=create_note.content,
      user_id=create_note.user_id
    )

    db.add(note)
    db.commit()
    db.refresh(note)
    return note
  except IntegrityError:
    raise HTTPException(
      status_code=400,
      detail="Bad request"
    )

@router.patch("/notes/{id}")
def update_note(
  id: int,
  update_data: schemas.AdminUpdateNote,
  db: Session = Depends(get_db),
  admin: models.User = Depends(auth.get_current_admin)
):
  try:
    note = db.query(models.Note).where(models.Note.id == id).first()

    if not note:
      raise HTTPException(
        status_code=404,
        detail="Not found"
      )
    
    update = update_data.model_dump(exclude_unset=True)
    for key, value in update.items():
      setattr(note, key, value)
    db.commit()
    db.refresh(note)
    return note
  except IntegrityError:
    raise HTTPException(
      status_code=400,
      detail="Bad request"
    )

@router.delete("/notes/{id}")
def delete_note(
  id: int,
  db: Session = Depends(get_db),
  admin: models.User = Depends(auth.get_current_admin)
):
  note = db.query(models.Note).where(models.Note.id == id).first()

  if not note:
    raise HTTPException(
      status_code=404,
      detail="Not found"
    )
  
  db.delete(note)
  db.commit()
  return note