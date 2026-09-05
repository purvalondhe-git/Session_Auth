from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.session import SessionModel
from app.security.authorization import require_admin


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/users")
def get_all_users(
    current_admin=Depends(require_admin),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()

    return users


@router.get("/sessions")
def get_all_sessions(
    current_admin=Depends(require_admin),
    db: Session = Depends(get_db)
):
    sessions = db.query(SessionModel).all()

    return sessions