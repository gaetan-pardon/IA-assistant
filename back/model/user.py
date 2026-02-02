from pydantic import BaseModel, EmailStr, SecretStr

class User(BaseModel):
    id: int
    email: EmailStr
    hashed_password: SecretStr