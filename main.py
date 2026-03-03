from fastapi import FastAPI
from api import users, notes, auth

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(notes.router, prefix="/notes", tags=["Notes"])