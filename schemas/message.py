from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime



class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    sources: Optional[List[str]]
    created_at: datetime
    class Config:
        from_attributes = True