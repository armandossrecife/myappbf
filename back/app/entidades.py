from pydantic import BaseModel

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