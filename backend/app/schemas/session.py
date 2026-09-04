from datetime import datetime
from pydantic import BaseModel


class SessionResponse(BaseModel):
    session_id: str
    device: str
    created_at: datetime
    expires_at: datetime
    last_activity: datetime

    class Config:
        from_attributes = True