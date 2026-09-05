from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.session import SessionModel
from app.schemas.session import SessionResponse
from app.security.authentication import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Sessions"]
)


# =========================================================
# 1. VIEW MY ACTIVE SESSIONS
# =========================================================

@router.get(
    "/sessions",
    response_model=list[SessionResponse]
)
def get_my_sessions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Return only the sessions belonging to the currently
    logged-in user.
    """

    sessions = (
        db.query(SessionModel)
        .filter(
            SessionModel.user_id == current_user.id
        )
        .all()
    )

    return sessions


# =========================================================
# 2. LOGOUT / TERMINATE ONE OF MY SESSIONS
# =========================================================

@router.delete("/sessions/{session_id}")
def logout_session(
    session_id: str,

    response: Response,

    current_session_id: str | None = Cookie(
        default=None,
        alias="session_id"
    ),

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)
):
    """
    A normal user can terminate only their own session.
    """

    session = (
        db.query(SessionModel)
        .filter(
            SessionModel.session_id == session_id,
            SessionModel.user_id == current_user.id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    # Delete the session from database
    db.delete(session)
    db.commit()

    # If the user terminated their current browser session,
    # remove the session cookie from that browser.
    if session_id == current_session_id:
        response.delete_cookie(
            key="session_id"
        )

    return {
        "message": "Session logged out successfully"
    }


# =========================================================
# 3. LOGOUT ALL MY SESSIONS
# =========================================================

@router.post("/logout-all")
def logout_all_sessions(
    response: Response,

    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)
):
    """
    Delete all sessions belonging to the currently
    logged-in user.
    """

    sessions = (
        db.query(SessionModel)
        .filter(
            SessionModel.user_id == current_user.id
        )
        .all()
    )

    for session in sessions:
        db.delete(session)

    db.commit()

    # Remove the current browser's session cookie
    response.delete_cookie(
        key="session_id"
    )

    return {
        "message": "All sessions logged out successfully"
    }