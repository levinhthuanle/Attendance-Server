
from fastapi import FastAPI
from app.api import auth, users, session
from app.db.session import Base
import app.models
from sqlalchemy import create_engine
from app.core.config import settings
from contextlib import asynccontextmanager

def run_migrations():
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1", tags=["User"])
app.include_router(session.router, prefix="/api/v1", tags=["Session"])