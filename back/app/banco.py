import sqlalchemy 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy import ForeignKey
from app import utilidades
from app import entidades
import os

DATABASE_URL = "sqlite:///users.db"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
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

def create_tables():
    print("Recriando as tabelas...")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(bind=engine)
    print("Tables criadas")

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

def get_user(db: SessionLocal, username: str):
    try: 
        user = db.query(UserDB).filter(UserDB.username == username).first()
        return user
    except Exception as ex:
        raise ValueError(f'Erro ao consultar usuario: {username}')
     
def get_user_by_id(db: SessionLocal, user_id: int):
    try:
        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        return user
    except Exception as ex:
        raise ValueError(f"Erro ao consultar usuario: {str(ex)}")

def create_user(user: entidades.User):
    try:
        db = SessionLocal()
        hashed_password = utilidades.hash_password(user.password)
        db_user = UserDB(username=user.username, email=user.email, password_hash=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return entidades.User(id=db_user.id, username=db_user.username, email=db_user.email, password=user.password)
    except Exception as ex:
        raise ValueError(f"Erro ao criar usuário: {str(ex)}")

def authenticate_user(db: SessionLocal, username: str, password: str):
    try:
        user = get_user(db, username)
        if not user:
            return False
        if not utilidades.verify_password(password, user.password_hash):
            return False
        return user
    except Exception as ex:
        raise ValueError(f"Erro ao autenticar usuário: {str(ex)}")

def get_all_users(db: SessionLocal):
  """Retrieves all users from the database.
  Args:
      db: A database session object.
  Returns:
      A list of User objects representing all users in the database.
  """
  try:
    users = db.query(UserDB).all()
    return [entidades.User(id=user.id, username=user.username, email=user.email, password="?") for user in users]
  except Exception as ex:
    raise ValueError(f"Erro ao recuperar usuários: {str(ex)}")

def get_image_profile_for_user(db: SessionLocal, user_id: int):
    try: 
        image_profile = db.query(ImageProfile).get(user_id)
        if image_profile:
            image_name = image_profile.name
            return image_name
        else:
            return "default.png"
    except Exception as ex:
        raise ValueError(f'Erro ao fazer a busca da imagem {str(ex)}')

def add_profile_image_to_user(db: SessionLocal, user_id: int, filename: str):
    try:
        db = SessionLocal()
        existing_image = get_image_profile_for_user(db, user_id)
        if existing_image:
            # Update existing image record
            update_image = ImageProfile(user_id=user_id, name=filename)
            db.merge(update_image)
        else:
            # Create a new image record
            new_image = ImageProfile(user_id=user_id, name=filename)
            db.add(new_image)
        db.commit()
    except Exception as e:
        raise ValueError(f"Error adding profile image: {str(e)}")

# Call the create_tables function outside your application code (e.g., in a separate script)
create_tables()
my_user = entidades.User(id=0, username="armando", email="armando@ufpi.edu.br", password="armando")
create_user(my_user)
print(f"Usuário {my_user.username} criado com sucesso!")