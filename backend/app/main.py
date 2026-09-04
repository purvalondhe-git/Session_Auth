from fastapi import FastAPI

from app.database import Base, engine
from app.models.user import User
from app.models.session import SessionModel
from app.routes import auth
from app.routes import sessions
from app.routes import admin

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FocusFlow API",
    description="Session-Based Authentication and Authorization System",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(sessions.router)
app.include_router(admin.router)

@app.get("/")
def home():
    return {
        "message": "FocusFlow API is running"
    }