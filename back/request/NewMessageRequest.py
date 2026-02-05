from pydantic import BaseModel, EmailStr, Field

class NewMessageRequest(BaseModel):
    message: str = Field(min_length=1)