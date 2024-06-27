from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import entidades
from app import utilidades
from app import banco
from app import seguranca

router = APIRouter()

# Todo: melhorar o acesso e registro do access_token
@router.post("/login")
async def login(user_login: entidades.UserLogin, db: Session = Depends(banco.get_db)):
  user_dao = banco.UserDAO(db)
  user = user_dao.authenticate_user(user_login.username, user_login.password)
  if not user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
  global access_token
  access_token = utilidades.create_access_token(data={"sub": user.username})
  return {"access_token": access_token, "token_type": "bearer"}

@router.get("/logout", dependencies=[Depends(seguranca.get_current_user)])
async def logout():
# In a real scenario, you might store tokens and blacklist them on logout
  # for better security. Here, we just return a success message.
  return {"message": "Successfully logged out"}  