import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey

Base = sqlalchemy.orm.declarative_base()

class UserDB(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, autoincrement=True)
  username = Column(String, unique=True, index=True)
  email = Column(String, unique=True, index=True)
  password_hash = Column(String)

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    name = Column(String(length=250), nullable=False)

class UserFilesDB(Base):
    __tablename__ = "user_files"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    file_id = Column(Integer, ForeignKey('files.id'))

class ImageProfile(Base):
    __tablename__ = "image_profile"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    name = Column(String(250), nullable=False)
    # Optional: Add a field to store the image file path
    file_path = Column(String(250))

class NoteDB(Base):
  __tablename__ = "notes"
  id = Column(Integer, primary_key=True, autoincrement=True)
  description = Column(String(1024))
  user_id = Column(Integer, ForeignKey("users.id"))