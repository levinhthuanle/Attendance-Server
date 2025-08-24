from fastapi import FastAPI
from app.api import auth, users
from app.db.session import Base, engine
import app.models  

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1", tags=["User"])