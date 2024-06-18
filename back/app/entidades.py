from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
  id: int
  username: str
  email: str
  password: str

class UserLogin(BaseModel):
  username: str
  password: str

class Note(BaseModel):
  id: int
  description: str
  insertion_date: datetime
  edition_date: datetime