from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
import models, schemas, auth

router = APIRouter()

is_admin_exception = HTTPException(
  status_code=401,
  detail="Not authorized"
)

@router.get("/users")
def get_users(
  db: Session = Depends(get_db),
  current_user: models.User = Depends(auth.get_current_user)
):
  if not current_user.is_admin:
    raise is_admin_exception
  return db.query(models.User).all()

@router.patch("/users")
def update_user(
  id: int,
  update_data: schemas.AdminUpdateUser,
  db: Session = Depends(get_db),
  current_user: models.User = Depends(auth.get_current_user)
):
  try:
    if not current_user.is_admin:
      raise is_admin_exception
    
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
  
@router.delete("/users")
def delete_user(
  id: int,
  db: Session = Depends(get_db),
  current_user: models.User = Depends(auth.get_current_user)
):
  if not current_user.is_admin:
    raise is_admin_exception
  
  user = db.query(models.User).where(models.User.id == id).first()

  db.delete(user)
  db.commit()
  return user