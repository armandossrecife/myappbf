from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import utilidades
import banco
import entidades

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_db():
  db = banco.SessionLocal()
  try:
    yield db
  finally:
    db.close()

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
  username = utilidades.verify_token(token)
  user = banco.get_user(db, username)
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
  return user

@app.post("/login")
async def login(user_login: entidades.UserLogin, db: Session = Depends(get_db)):
  user = banco.authenticate_user(db, user_login.username, user_login.password)
  if not user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
  access_token = utilidades.create_access_token(data={"sub": user.username})
  return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/{username}", dependencies=[Depends(get_current_user)])
async def get_user_by_username(username: str, db: Session = Depends(get_db)):
  user = banco.get_user(db, username)
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
  return entidades.User(id=user.id, username=user.username, email=user.email, password="?")

@app.get("/users/{user_id}", dependencies=[Depends(get_current_user)])
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
  user = banco.get_user_by_id(db, user_id)
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
  return entidades.User(id=user.id, username=user.username, email=user.email, password="?")

@app.get("/users", dependencies=[Depends(get_current_user)])
async def get_all_users(db: Session = Depends(get_db)):
  users = banco.get_all_users(db)
  return users

@app.post("/users")
async def create_user(user: entidades.User):
  """ Creates a new user in the database.
  Args:
      user: User object containing user information.
  Returns:
      The created User object.
  Raises:
      HTTPException: If user creation fails.
  """
  try:
      created_user = banco.create_user(user)
      return created_user
  except Exception as e:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error creating user: {str(e)}")

@app.get("/logout", dependencies=[Depends(get_current_user)])
async def logout():
  # In a real scenario, you might store tokens and blacklist them on logout
  # for better security. Here, we just return a success message.
  return {"message": "Successfully logged out"}