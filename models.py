from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from database import engine

Base = declarative_base()

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  email = Column(String, nullable=False, unique=True)
  name = Column(String, nullable=False)

  notes = relationship('Note', back_populates='user', passive_deletes=True)

class Note(Base):
  __tablename__ = 'notes'
  id = Column(Integer, primary_key=True)
  title = Column(String, nullable=False)
  content = Column(String, nullable=True)
  user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))

  user = relationship('User', back_populates='notes')