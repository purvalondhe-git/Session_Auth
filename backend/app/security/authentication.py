from datetime import datetime

from fastapi import Cookie, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.session import SessionModel
from app.models.user import User


def get_current_user(
    cookie_session_id: str | None = Cookie(
        default=None,
        alias="session_id"
    ),
    db: Session = Depends(get_db)
):
    if not cookie_session_id:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    session = (
        db.query(SessionModel)
        .filter(
            SessionModel.session_id == cookie_session_id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=401,
            detail="Invalid session"
        )

    if session.expires_at < datetime.utcnow():
        db.delete(session)
        db.commit()

        raise HTTPException(
            status_code=401,
            detail="Session expired"
        )

    user = (
        db.query(User)
        .filter(User.id == session.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    session.last_activity = datetime.utcnow()
    db.commit()

    return user