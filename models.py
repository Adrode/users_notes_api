from sqlalchemy import Integer, String, Boolean, Column, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from database import Base

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  email = Column(String, nullable=False, unique=True)
  name = Column(String, nullable=False)
  hashed_password = Column(String(255), nullable=False)
  is_active = Column(Boolean, default=True, nullable=False)
  is_admin = Column(Boolean, default=False, nullable=False)

  notes = relationship('Note', back_populates='user', passive_deletes=True)

class Note(Base):
  __tablename__ = 'notes'
  id = Column(Integer, primary_key=True)
  title = Column(String, nullable=False, index=True)
  content = Column(String, nullable=True)
  user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
  is_done = Column(Boolean, nullable=False, default=False)

  user = relationship('User', back_populates='notes')