from typing import Optional

from pydantic import BaseModel
from datetime import datetime

class TicketResponse(BaseModel):
    ticket_id: str
    session_id: str
    reason: str
    status: str
    created_at: datetime
    class Config:
        from_attributes = True