import sqlalchemy 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
import utilidades
import entidades

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

def create_tables():
    print("Recriando as tabelas...")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(bind=engine)
    print("Tables criadas")

def get_user(db: SessionLocal, username: str):
    return db.query(UserDB).filter(UserDB.username == username).first()

def get_user_by_id(db: SessionLocal, user_id: int):
    return db.query(UserDB).filter(UserDB.id == user_id).first()

def create_user(user: entidades.User):
    db = SessionLocal()
    hashed_password = utilidades.hash_password(user.password)
    db_user = UserDB(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return entidades.User(id=db_user.id, username=db_user.username, email=db_user.email, password=user.password)

def authenticate_user(db: SessionLocal, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not utilidades.verify_password(password, user.password_hash):
        return False
    return user

def get_all_users(db: SessionLocal):
  """Retrieves all users from the database.
  Args:
      db: A database session object.
  Returns:
      A list of User objects representing all users in the database.
  """
  users = db.query(UserDB).all()
  return [entidades.User(id=user.id, username=user.username, email=user.email, password="?") for user in users]


# Call the create_tables function outside your application code (e.g., in a separate script)
create_tables()
my_user = entidades.User(id=0, username="armando", email="armando@ufpi.edu.br", password="armando")
create_user(my_user)
print(f"Usuário {my_user.username} criado com sucesso!")