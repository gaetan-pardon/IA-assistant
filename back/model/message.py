from pydantic import BaseModel
from datetime import datetime


class Message(BaseModel):
    id: int
    role: str
    content: str
    timestamp: datetime