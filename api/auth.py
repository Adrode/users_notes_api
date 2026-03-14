from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas, auth
from database import get_db

router = APIRouter()

@router.post("/register", response_model=schemas.User)
def register(
  user_data: schemas.CreateUser,
  db: Session = Depends(get_db)
):
  if auth.get_user_by_email(db, user_data.email):
    raise HTTPException(
      status_code=400,
      detail="Email not available"
    )
  
  user = models.User(
    email=user_data.email,
    name=user_data.name,
    hashed_password=auth.hash_password(user_data.password)
  )
  db.add(user)
  db.commit()
  db.refresh(user)
  return user

@router.post("/login", response_model=schemas.Token)
def login(
  form_data: OAuth2PasswordRequestForm = Depends(),
  db: Session = Depends(get_db)
):
  user = auth.authenticate_user(db, form_data.username, form_data.password)
  if not user:
    raise HTTPException(
      status_code=401,
      detail="Incorrect email or password",
      headers={"WWW-Authenticate": "Bearer"}
    )
  token = auth.create_access_token(
    data={"sub": user.email}
  )
  return {"access_token": token, "token_type": "bearer"}