from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import utilidades
from app import entidades
from app import modelos
from datetime import datetime

DATABASE_URL = "sqlite:///users.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    print("Recriando as tabelas...")
    modelos.Base.metadata.drop_all(engine)
    modelos.Base.metadata.create_all(bind=engine)
    print("Tables criadas")

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

### Users operations ###

class UserDAO:
  def __init__(self, db):
    self.db = db
  
  def get_user(self,username):
    try: 
      user = self.db.query(modelos.UserDB).filter(modelos.UserDB.username == username).first()
      return user
    except Exception as ex:
        raise ValueError(f'Erro ao consultar usuario {username}: {str(ex)}')
     
  def get_user_by_id(self, user_id: int):
    try:
      user = self.db.query(modelos.UserDB).filter(modelos.UserDB.id == user_id).first()
      return user
    except Exception as ex:
        raise ValueError(f"Erro ao consultar usuario: {str(ex)}")

  def create_user(self, user: entidades.User):
    try:
      db = SessionLocal()
      hashed_password = utilidades.hash_password(user.password)
      db_user = modelos.UserDB(username=user.username, email=user.email, password_hash=hashed_password)
      db.add(db_user)
      db.commit()
      db.refresh(db_user)
      return entidades.User(id=db_user.id, username=db_user.username, email=db_user.email, password=user.password)
    except Exception as ex:
      raise ValueError(f"Erro ao criar usuário: {str(ex)}")

  def authenticate_user(self, username: str, password: str):
    try:
      user = self.get_user(username)
      if not user:
        return False
      if not utilidades.verify_password(password, user.password_hash):
        return False
      return user
    except Exception as ex:
      raise ValueError(f"Erro ao autenticar usuário: {str(ex)}")

  def get_all_users(self):
    """Retrieves all users from the database.
    Args:
        db: A database session object.
    Returns:
        A list of User objects representing all users in the database.
    """
    try:
      users = self.db.query(modelos.UserDB).all()
      return [entidades.User(id=user.id, username=user.username, email=user.email, password="?") for user in users]
    except Exception as ex:
      raise ValueError(f"Erro ao recuperar usuários: {str(ex)}")

  def get_image_profile_for_user(self, user_id: int):
    try: 
      image_profile = self.db.query(modelos.ImageProfile).get(user_id)
      if image_profile:
        image_name = image_profile.name
        return image_name
      else:
        return "default.png"
    except Exception as ex:
      raise ValueError(f'Erro ao fazer a busca da imagem {str(ex)}')

  def add_profile_image_to_user(self, user_id: int, filename: str):
    try:
      existing_image = self.get_image_profile_for_user(user_id)
      if existing_image:
          # Update existing image record
          update_image = modelos.ImageProfile(user_id=user_id, name=filename)
          self.db.merge(update_image)
      else:
          # Create a new image record
          new_image = modelos.ImageProfile(user_id=user_id, name=filename)
          self.db.add(new_image)
      self.db.commit()
    except Exception as e:
      raise ValueError(f"Error adding profile image: {str(e)}")

### Notes operations ###

class NotesDAO:
  def __init__(self, db):
    self.db = db

  def create_note(self, user_id: int, description: str) -> entidades.Note:
    try:
      new_note = modelos.NoteDB(description=description, user_id=user_id)
      self.db.add(new_note)
      self.db.commit()
      self.db.refresh(new_note)
      return entidades.Note(id=new_note.id, description=new_note.description)
    except Exception as ex:
      raise ValueError(f"Error creating note: {str(ex)}, status_code=400")

  def get_all_notes_by_user(self, user_id: int) -> list[entidades.Note]:
    try:
      notes = self.db.query(modelos.NoteDB).filter(modelos.NoteDB.user_id == user_id).all()
      return [entidades.Note(id=note.id, description=note.description) for note in notes]
    except Exception as ex:
      raise ValueError(f"Error retrieving notes: {str(ex)}, status_code=500")

  def get_note_by_id(self, note_id: int) -> entidades.Note:
    try:
      note = self.db.query(modelos.NoteDB).filter(modelos.NoteDB.id == note_id).first()
      if not note:
        raise ValueError("Note not found")
      return entidades.Note(id=note.id, description=note.description)
    except Exception as ex:
      raise ValueError(f"Error retrieving note: {str(ex)}, status_code=500")

  def update_note(self, note_id: int, user_id: int, description: str) -> entidades.Note:
    try:
      note = self.db.query(modelos.NoteDB).filter(modelos.NoteDB.id == note_id and modelos.NoteDB.user_id==user_id).first()
      if not note:
        raise ValueError("Note not found")
      note.description = description
      note.edition_date = datetime.utcnow()  # Update edition date
      self.db.commit()
      self.db.refresh(note)
      return entidades.Note(id=note.id, description=note.description)
    except Exception as ex:
      raise ValueError(f"Error updating note: {str(ex)}, status_code=400")

  def delete_note(self, note_id: int, user_id: int) -> None:
    try:
      note = self.db.query(modelos.NoteDB).filter(modelos.NoteDB.id == note_id and modelos.NoteDB.user_id==user_id).first()
      if not note:
        raise ValueError("Note not found")
      self.db.delete(note)
      self.db.commit()
    except Exception as ex:
      raise ValueError(f"Error deleting note: {str(ex)}, status_code=400")