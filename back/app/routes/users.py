from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from app import entidades
from app import banco
from app import seguranca

router = APIRouter()

@router.get("/users/{username}", dependencies=[Depends(seguranca.get_current_user)])
async def get_user_by_username(username: str, db: Session = Depends(banco.get_db)):
  user_dao = banco.UserDAO(db)
  user = user_dao.get_user(username)
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
  return entidades.User(id=user.id, username=user.username, email=user.email, password="?")

@router.get("/users/{user_id}", dependencies=[Depends(seguranca.get_current_user)])
async def get_user_by_id(user_id: int, db: Session = Depends(banco.get_db)):
  user_dao = banco.UserDAO(db)
  user = user_dao.get_user_by_id(user_id)
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
  return entidades.User(id=user.id, username=user.username, email=user.email, password="?")

@router.post("/users")
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
      db = banco.get_db()
      user_dao = banco.UserDAO(db)
      created_user = user_dao.create_user(user)
      return created_user
  except Exception as e:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error creating user: {str(e)}")

'''''
1. User Roles:
- Define roles for your users (e.g., "admin", "editor", "user").
- Store the user's role in the database associated with their user ID.
- In the has_access function:
-- Retrieve the user's role from the database using the user.id.
-- Check if the user's role has the required permission ("list_users" in this case).
  You can use a dictionary or a permission checking library to manage role-based permissions.
'''''
# Replace this with your function to get user role from database
async def get_user_role(user: entidades.User, db: Session = Depends(banco.get_db)) -> str:
    # Implement logic to get user role from database based on user.id
    # ...
    return "user"  # Replace with the actual retrieved role

async def has_access(user: entidades.User = Depends(seguranca.get_current_user), permission: str = "list_users") -> bool:
    user_role = await get_user_role(user)
    allowed_roles = {"list_users": ["admin"]}  # Map permission to allowed roles
    return user_role in allowed_roles.get(permission, [])

@router.get("/users", dependencies=[Depends(seguranca.get_current_user)])
async def get_all_users(user: entidades.User = Depends(seguranca.get_current_user), db: Session = Depends(banco.get_db)):
  # Check user permissions (replace with your access control logic)
  if not has_access(user, "list_users"):  # Replace "has_access" with your permission checking function
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

  # Filter user data
  filtered_users = [
      entidades.User(id=u.id, username=u.username, password="?")
      for u in banco.get_all_users(db)
  ]

  # Optionally, filter further based on logged-in user
  if user.id:
      for filtered_user in filtered_users:
          if filtered_user.id == user.id:
              filtered_user.email = user.email  # Include email only for the current user

  return filtered_users