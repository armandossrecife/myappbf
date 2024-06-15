from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from app import entidades
from app import utilidades
from app import banco
from app import seguranca
import mimetypes
import os

router = APIRouter()

@router.get("/users/{username}", dependencies=[Depends(seguranca.get_current_user)])
async def get_user_by_username(username: str, db: Session = Depends(banco.get_db)):
  user = banco.get_user(db, username)
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
  return entidades.User(id=user.id, username=user.username, email=user.email, password="?")

@router.get("/users/{user_id}", dependencies=[Depends(seguranca.get_current_user)])
async def get_user_by_id(user_id: int, db: Session = Depends(banco.get_db)):
  user = banco.get_user_by_id(db, user_id)
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
  return entidades.User(id=user.id, username=user.username, email=user.email, password="?")

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

# Todo: check token from current user@router.get("/users/{username}/profile/{filename}", dependencies=[Depends(seguranca.get_current_user)])
@router.get("/users/{username}/profile/{filename}")
async def show_image_profile(filename: str, username: str, db: Session = Depends(banco.get_db)):
    user = banco.get_user(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    try:      
        sanitized_filename = utilidades.validate_filename(filename)
        filepath = os.path.join(utilidades.IMAGES_PATH_PROFILE, sanitized_filename)
        content_type = mimetypes.guess_type(filepath)[0]
        return FileResponse(filepath, media_type=content_type)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail="Image not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error. {str(e)}")

# Todo: check token from current user @router.get("/users/{username}/profile", dependencies=[Depends(seguranca.get_current_user)])
@router.get("/users/{username}/profile")
async def get_user_profile(username: str, db: Session = Depends(banco.get_db)):
    try: 
      user = banco.get_user(db, username)
      if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

      image_profile_name = banco.get_image_profile_for_user(db, user.id) 
      image_url = f"{utilidades.API_URL}/users/{username}/profile/{image_profile_name}"
      image_default = f"{utilidades.API_URL}/users/{username}/profile/default.png"
      content = {
          "message": "User image profile",
          "id": user.id,
          "username": user.username,
          "email": user.email,
          "profile_image_url": image_url if image_profile_name else image_default  # Include image URL if available
      }
      return content
    except Exception as ex:
      raise HTTPException(status_code=500, detail=f"Internal server error. {str(ex)}")

@router.post("/users/{username}/profile", dependencies=[Depends(seguranca.get_current_user)])
async def upload_image_prolife(image: UploadFile, username: str, db: Session = Depends(banco.get_db)):
    user = banco.get_user(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    extension = os.path.splitext(image.filename)[1].lower()
    if extension not in utilidades.ALLOWED_EXTENSIONS:
        return HTTPException(status_code=400, detail=f"Unsupported file extension. Allowed extensions: {', '.join(utilidades.ALLOWED_EXTENSIONS)}")

    try: 
      # Create 'profile' folder if it doesn't exist
      os.makedirs(utilidades.IMAGES_PATH_PROFILE, exist_ok=True)
      filepath = os.path.join(utilidades.IMAGES_PATH_PROFILE, image.filename)
      filename = image.filename

      # Save the image file
      contents = await image.read()
      with open(filepath, "wb") as f:
        f.write(contents)
        image_url = f"{utilidades.API_URL}/users/{username}/profile/{image.filename}"
      banco.add_profile_image_to_user(db, user.id, filename)
      
      content = {"message": f"Image profile uploaded successfully: {image.filename}", 
          "filename":image.filename,
          "id": user.id,
          "username": user.username,
          "email": user.email,
          "profile_image_url": image_url if image.filename else None  # Include image URL if available
          }
      return content

    except Exception as ex:
      raise HTTPException(status_code=500, detail=f"Internal server error. {str(ex)}")

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
      created_user = banco.create_user(user)
      return created_user
  except Exception as e:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error creating user: {str(e)}")