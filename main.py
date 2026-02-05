# ENDPOINTY

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import Base, User, Note
from database import engine, get_db
from schemas import CreateUser, CreateNote, UpdateNoteContent

Base.metadata.create_all(bind=engine)

app = FastAPI()

# USERS ENDPOINTS

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
  users = db.query(User).all()
  return users

@app.post("/users")
def add_user(create_user: CreateUser, db: Session = Depends(get_db)):
  new_user = User(email=create_user.email, name=create_user.name)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user
# TO DO LATER: exception_handler na wypadek podania danych, które nie mogą zostać dodane do tabeli ze względu na unique albo inny contstraint

# NOTES ENDPOINTS

@app.get("/notes")
def get_notes(db: Session = Depends(get_db)):
  notes = db.query(Note).all()
  return notes

@app.post("/notes")
def add_note(create_note: CreateNote, db: Session = Depends(get_db)):
  new_note = Note(title=create_note.title, content=create_note.content, user_id=create_note.user_id)
  db.add(new_note)
  db.commit()
  db.refresh(new_note)
  return new_note