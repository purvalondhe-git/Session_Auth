from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models.user import User
from app.models.session import SessionModel
from app.routes import auth
from app.routes import sessions
from app.routes import admin


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="FocusFlow API",
    description="Session-Based Authentication and Authorization System",
    version="1.0.0"
)


# --------------------------------------------------
# CORS CONFIGURATION
# --------------------------------------------------
# Allows React frontend to communicate with FastAPI
# Frontend runs on port 5173
# Backend runs on port 8000

app.add_middleware(
    CORSMiddleware,

    # React/Vite frontend URLs
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],

    # Required because authentication uses cookies
    allow_credentials=True,

    # Allow GET, POST, PUT, DELETE, etc.
    allow_methods=["*"],

    # Allow headers such as Content-Type and X-CSRF-Token
    allow_headers=["*"],
)


# --------------------------------------------------
# ROUTES
# --------------------------------------------------

# Authentication routes
app.include_router(auth.router)

# Session management routes
app.include_router(sessions.router)

# Admin routes
app.include_router(admin.router)


# --------------------------------------------------
# HOME ROUTE
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "FocusFlow API is running"
    }