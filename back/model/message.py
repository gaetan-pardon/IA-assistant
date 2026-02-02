from pydantic import BaseModel
from datetime import datetime


class Message(BaseModel):
    prompt: str
    ai_answer: str
    date: datetime