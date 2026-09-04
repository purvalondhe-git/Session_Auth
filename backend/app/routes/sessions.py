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


# -----------------------------------
# 1. View active sessions
# -----------------------------------

@router.get(
    "/sessions",
    response_model=list[SessionResponse]
)
def get_my_sessions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    sessions = (
        db.query(SessionModel)
        .filter(
            SessionModel.user_id == current_user.id
        )
        .all()
    )

    return sessions


# -----------------------------------
# 2. Logout one specific session
# -----------------------------------

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

    db.delete(session)
    db.commit()

    if session_id == current_session_id:
        response.delete_cookie("session_id")

    return {
        "message": "Session logged out successfully"
    }

    # -----------------------------------
# 3. Logout all sessions
# -----------------------------------

@router.post("/logout-all")
def logout_all_sessions(
    response: Response,
    current_session_id: str | None = Cookie(
        default=None,
        alias="session_id"
    ),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
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

    response.delete_cookie("session_id")

    return {
        "message": "All sessions logged out successfully"
    }