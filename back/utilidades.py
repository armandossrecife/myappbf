from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt

SECRET_KEY = "your_secret_key"  # Replace with a strong secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

def hash_password(password: str) -> str:
    """Hashes a plain text password using bcrypt with a strong work factor.
    Args:
        password: The plain text password to hash.
    Returns:
        The hashed password as a base64 encoded string.
    """

    # Recommended work factor based on current hardware speeds
    work_factor = 14  # Adjust as needed, higher is more secure but slower
    salt = bcrypt.gensalt(work_factor)
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    # Use base64 encoding for safe storage and transmission
    return hashed_password.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against a hashed password using bcrypt.
    Args:
        plain_password: The plain text password to verify.
        hashed_password: The hashed password to compare against.
    Returns:
        True if the passwords match, False otherwise.
    """
    hashed_password = hashed_password.encode("utf-8")
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password)
    
def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire.timestamp()})
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, credentials_exception=None):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload["sub"]
  except JWTError:
    raise credentials_exception