from pydantic import BaseModel
from datetime import datetime


class Message(BaseModel):
    id: int
    user_id: int
    prompt: str
    ai_answer: str
    date: datetime
    ancient_message_id: int