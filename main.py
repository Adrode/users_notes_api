from fastapi import FastAPI
from api import users, notes, auth, admin

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(notes.router, prefix="/notes", tags=["Notes"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"]) 