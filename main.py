from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import router
from routers.auth_router import router as auth_router
from database import create_db
from models import Task, User

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"message": "Welcome to Taskmate!"}

app.include_router(router)
app.include_router(auth_router)