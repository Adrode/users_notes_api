from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
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

@app.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
  user = db.query(User).filter(User.id == id).first()
  return user

@app.post("/users")
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

# NOTES ENDPOINTS

@app.get("/notes")
def get_notes(db: Session = Depends(get_db)):
  notes = db.query(Note).all()
  return notes

@app.get("/notes/{id}")
def get_note(id: int, db: Session = Depends(get_db)):
  note = db.query(Note).filter(Note.id == id).first()
  return note

@app.post("/notes")
def add_note(create_note: CreateNote, db: Session = Depends(get_db)):
  new_note = Note(title=create_note.title, content=create_note.content, user_id=create_note.user_id)
  db.add(new_note)
  db.commit()
  db.refresh(new_note)
  return new_note

@app.put("/notes/{id}")
def update_note_content(id: int, update_note_content: UpdateNoteContent, db: Session = Depends(get_db)):
  updated_note = db.query(Note).filter(Note.id == id).first()

  if not updated_note:
    raise HTTPException(
      status_code=404,
      detail="ID not found"
    )

  updated_note.content = update_note_content.content
  db.commit()
  db.refresh(updated_note)
  return updated_note

# JOINED ENDPOINTS

@app.get("/users_notes")
def get_users_notes(db: Session = Depends(get_db)):
  users_notes = db.query(User.name, Note.title, Note.content).join(Note).all()
  return [{'name': element.name, 'title': element.title, 'content': element.content} for element in users_notes]