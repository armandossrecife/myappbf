from fastapi import FastAPI
import uvicorn
from app.routes import auth, users
from app import banco
from app import entidades

app_media = FastAPI()

# Call the create_tables function outside your application code (e.g., in a separate script)
banco.create_tables()
my_user = entidades.User(id=0, username="armando", email="armando@ufpi.edu.br", password="armando")
banco.create_user(my_user)
print(f"Usuário {my_user.username} criado com sucesso!")

app_media.include_router(auth.router)
app_media.include_router(users.router)

if __name__ == "__main__":
  uvicorn.run(app_media, host="0.0.0.0", port=8000)