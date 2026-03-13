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