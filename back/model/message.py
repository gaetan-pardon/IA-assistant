from pydantic import BaseModel
from datetime import datetime


class Message(BaseModel):
    id: int
    prompt: str
    ai_answer: str
    date: datetime