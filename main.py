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