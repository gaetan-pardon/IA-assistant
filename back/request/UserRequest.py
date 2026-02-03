from pydantic import BaseModel, EmailStr, Field, SecretStr

class UserRequest(BaseModel):
    email: EmailStr = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=1024)