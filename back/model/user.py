from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    id: int
    email: EmailStr = Field(min_length=5, max_length=255)
    hashed_password: str = Field(min_length=8, max_length=1024)