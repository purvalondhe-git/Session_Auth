import secrets
from datetime import datetime, timedelta

import bcrypt

from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    HTTPException,
    Request,
    Response
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.session import SessionModel
from app.schemas.user import UserRegister, UserLogin, UserResponse
from app.security.authentication import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


SESSION_DURATION_DAYS = 7


# ==========================================
# 1. REGISTER - MODULE 1
# ==========================================

@router.post(
    "/register",
    status_code=201
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    if len(user_data.password) < 6:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 6 characters"
        )

    password_hash = bcrypt.hashpw(
        user_data.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=password_hash,
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Registration successful",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "role": new_user.role,
            "created_at": new_user.created_at
        }
    }


# ==========================================
# 2. LOGIN - MODULE 1 + MODULE 2
# ==========================================

@router.post("/login")
def login(
    user_data: UserLogin,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    password_match = bcrypt.checkpw(
        user_data.password.encode("utf-8"),
        user.password_hash.encode("utf-8")
    )

    if not password_match:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Generate secure random session ID
    session_id = secrets.token_urlsafe(32)

    now = datetime.utcnow()

    expires_at = now + timedelta(
        days=SESSION_DURATION_DAYS
    )

    # Get device/browser information
    device = request.headers.get(
        "user-agent",
        "Unknown Device"
    )

    # Create server-side session
    new_session = SessionModel(
        session_id=session_id,
        user_id=user.id,
        device=device,
        created_at=now,
        expires_at=expires_at,
        last_activity=now
    )

    db.add(new_session)
    db.commit()

    # Store session ID in HTTP-only cookie
    response.set_cookie(
    key="session_id",
    value=session_id,
    max_age=SESSION_DURATION_DAYS * 24 * 60 * 60,
    httponly=True,
    secure=False,
    samesite="lax",
    path="/"
)

    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at
        }

    } 

    


# ==========================================
# 3. GET CURRENT USER - MODULE 2
# ==========================================

@router.get("/me")
def get_me(
    current_user=Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }


# ==========================================
# 4. NORMAL LOGOUT - MODULE 2
# ==========================================

@router.post("/logout")
def logout(
    response: Response,
    session_id: str | None = Cookie(
        default=None,
        alias="session_id"
    ),
    db: Session = Depends(get_db)
):
    if session_id:

        session = (
            db.query(SessionModel)
            .filter(
                SessionModel.session_id == session_id
            )
            .first()
        )

        if session:
            db.delete(session)
            db.commit()

    # Remove cookie from browser
    response.delete_cookie("session_id")

    return {
        "message": "Logged out successfully"
    }

