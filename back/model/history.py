from model.message import Message
from pydantic import BaseModel


class History(BaseModel):
    id: int
    user_id: int
    messages: list[Message]
