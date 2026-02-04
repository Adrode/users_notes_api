from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

app = FastAPI()

engine = create_engine('postgresql://app_pg_user:app_pg_password@localhost:5432/app_pg_db')

