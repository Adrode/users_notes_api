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

@router.patch("/users/{id}")
def update_user(
  id: int,
  update_data: schemas.AdminUpdateUser,
  db: Session = Depends(get_db),
  admin: models.User = Depends(auth.get_current_admin)
):
  try:
    user = db.query(models.User).where(models.User.id == id).first()

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