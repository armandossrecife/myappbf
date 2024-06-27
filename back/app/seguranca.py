from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app import banco
from app import utilidades

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(db: Session = Depends(banco.get_db), token: str = Depends(oauth2_scheme)):
  try: 
    username = utilidades.verify_token(token)
    user_dao = banco.UserDAO(db)
    user = user_dao.get_user(username)
    if not user:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user
  except Exception as ex:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {str(ex)}")