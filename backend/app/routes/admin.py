from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.session import SessionModel
from app.security.authorization import require_admin


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# =========================================================
# 1. VIEW ALL USERS
# =========================================================

@router.get("/users")
def get_all_users(
    current_admin=Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Admin can view all registered users.
    """

    users = (
        db.query(User)
        .order_by(User.id.asc())
        .all()
    )

    return users


# =========================================================
# 2. VIEW ALL ACTIVE SESSIONS
# =========================================================

@router.get("/sessions")
def get_all_active_sessions(
    current_admin=Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Admin can view active sessions of ALL users.
    """

    now = datetime.utcnow()

    results = (
        db.query(
            SessionModel,
            User
        )
        .join(
            User,
            SessionModel.user_id == User.id
        )
        .filter(
            SessionModel.expires_at > now
        )
        .order_by(
            SessionModel.last_activity.desc()
        )
        .all()
    )

    sessions = []

    for session, user in results:

        sessions.append({
            "session_id": session.session_id,
            "user_id": user.id,
            "user_name": user.name,
            "user_email": user.email,
            "user_role": user.role,
            "device": session.device,
            "created_at": session.created_at,
            "expires_at": session.expires_at,
            "last_activity": session.last_activity
        })

    return sessions


# =========================================================
# 3. ADMIN TERMINATES ANY USER'S SESSION
# =========================================================

@router.delete("/sessions/{session_id}")
def admin_terminate_session(
    session_id: str,
    current_admin=Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Admin can terminate ANY user's session.
    """

    session = (
        db.query(SessionModel)
        .filter(
            SessionModel.session_id == session_id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    # Delete the selected user's session
    db.delete(session)
    db.commit()

    return {
        "message": "User session terminated successfully",
        "session_id": session_id
    }