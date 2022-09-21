from fastapi import FastAPI, Depends

from app.onauth2 import get_current_user
from .config import settings
app = FastAPI()
from .models import Base
from .database import engine
from .routers import user, task
from fastapi.middleware.cors import CORSMiddleware

# Base.metadata.create_all(bind=engine)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# user
app.include_router(user.router)
app.include_router(task.router)
# user

@app.get('/')
def home():
    return {
        'message':'Hello World'
    }