from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import User, Note
from database import get_db
from schemas import CreateUser

router = APIRouter()

@router.get("/notes/{id}")
def get_user_notes(id: int, db: Session = Depends(get_db)):
  user = db.query(User).where(User.id == id).first()

  if not user:
    raise HTTPException(
      status_code=404,
      detail="ID not found"
    )
  
  return {'user_name': user.name, 'notes': [{'title': element.title, 'content': element.content} for element in user.notes]}

@router.get("/notes")
def get_all_users_notes(db: Session = Depends(get_db)):
  users_notes = db.query(Note).join(User).all()
  return [
    {
      'user_name': note.user.name,
      'note_title': note.title,
      'note_content': note.content
    } for note in users_notes
  ]

@router.get("/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
  user = db.query(User).where(User.id == id).first()
  return user

@router.get("/")
def get_users(db: Session = Depends(get_db)):
  users = db.query(User).all()
  return users

@router.post("/")
def add_user(create_user: CreateUser, db: Session = Depends(get_db)):
  try:
    new_user = User(email=create_user.email, name=create_user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
  except IntegrityError:
    raise HTTPException(
      status_code=400,
      detail="Unique constraint violated"
    )

@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
  user_to_delete = db.query(User).where(User.id == id).first()

  if not user_to_delete:
    raise HTTPException(
      status_code=404,
      detail="ID not found"
    )
  
  db.delete(user_to_delete)
  db.commit()
  return user_to_delete