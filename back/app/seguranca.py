from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app import banco
from app import utilidades

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(db: Session = Depends(banco.get_db), token: str = Depends(oauth2_scheme)):
  username = utilidades.verify_token(token)
  user = banco.get_user(db, username)
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
  return user