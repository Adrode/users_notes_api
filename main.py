from fastapi import FastAPI
from api import users
from api import notes

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(notes.router, prefix="/notes", tags=["Notes"])