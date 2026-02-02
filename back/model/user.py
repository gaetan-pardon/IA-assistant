from pydantic import BaseModel, EmailStr, SecretStr

class User(BaseModel):
    email: EmailStr
    hashed_password: SecretStr