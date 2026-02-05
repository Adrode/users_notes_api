# ENDPOINTY

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import Base, User, Note
from database import engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
  users = db.query(User).all()
  return users

@app.post("/users")
def add_user(email: str, name: str, db: Session = Depends(get_db)):
  new_user = User(email=email, name=name)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user
# TO DO LATER: exception_handler na wypadek podania danych, które nie mogą zostać dodane do tabeli ze względu na unique albo inny contstraint