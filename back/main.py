from fastapi import FastAPI
import uvicorn
from app.routes import auth, users

app_media = FastAPI()

app_media.include_router(auth.router)
app_media.include_router(users.router)

if __name__ == "__main__":
  uvicorn.run(app_media, host="0.0.0.0", port=8000)