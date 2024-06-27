from fastapi import FastAPI
import uvicorn
from app.routes import auth, users, profile, notes
from app import banco
from app import entidades

app_media = FastAPI()

# Call the create_tables function outside your application code (e.g., in a separate script)
banco.create_tables()

# Cria um usuario default
my_user = entidades.User(id=0, username="armando", email="armando@ufpi.edu.br", password="armando")

db = banco.get_db()
user_dao = banco.UserDAO(db)
user_dao.create_user(my_user)
print(f"Usuário {my_user.username} criado com sucesso!")

# Include das rotas da aplicacao
app_media.include_router(auth.router)
app_media.include_router(users.router)
app_media.include_router(profile.router)
app_media.include_router(notes.router)

if __name__ == "__main__":
  uvicorn.run(app_media, host="0.0.0.0", port=8000)