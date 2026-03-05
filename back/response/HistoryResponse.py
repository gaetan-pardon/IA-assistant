from pydantic import BaseModel


class HistoryResponse(BaseModel):
    id: int
    user_id: int
    question: str
    answer: str