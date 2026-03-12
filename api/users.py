from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User, Note
from database import get_db
import models, schemas, auth

router = APIRouter()

@router.get("/me")
def get_me(current_user: models.User = Depends(auth.get_current_user)):
  return current_user

@router.delete("/me")
def delete_me(
    password: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
  ):
  user = db.query(User).where(User.id == current_user.id).first()

  if not auth.verify_password(password, current_user.hashed_password):
    raise HTTPException(
      status_code=401,
      detail="Not authorized"
    )
  
  db.delete(user)
  db.commit()
  return user

# TO DELETE / ADMIN ENDPOINTS
# @router.get("/all/notes")
# def get_all_users_notes(db: Session = Depends(get_db)):
#   users_notes = db.query(Note).join(User).all()
#   return [
#     {
#       'user_name': note.user.name,
#       'note_title': note.title,
#       'note_content': note.content
#     } for note in users_notes
#   ]

# TO DELETE / ADMIN ENDPOINTS
# @router.get("/")
# def get_users(db: Session = Depends(get_db)):
#   users = db.query(User).all()
#   return users

# TO DELETE
#@router.post("/")
#def add_user(create_user: CreateUser, db: Session = Depends(get_db)):
#  try:
#    new_user = User(email=create_user.email, name=create_user.name)
#    db.add(new_user)
#    db.commit()
#    db.refresh(new_user)
#    return new_user
#  except IntegrityError:
#    raise HTTPException(
#      status_code=400,
#      detail="Unique constraint violated"
#    )