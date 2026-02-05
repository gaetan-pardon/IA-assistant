from fastapi import Cookie, HTTPException
from model.user import User
from database.database import insertUser, getUserByEmail

from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from dotenv import dotenv_values

config = dotenv_values(".env")

SECRET_KEY = config["SECRET_KEY"]
ALGORITHM = config["ALGORITHM"]
TOKEN_EXPIRE_MINUTES = int(config["TOKEN_EXPIRE_MINUTES"])


def create_access_token(email: str) -> str:
    """Create a JWT access token for the given user ID.
    Args:
        user_id (int): The ID of the user.
    Returns:
        token (str): The encoded JWT token.
    """
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(email),
        "iat": datetime.now(tz=timezone.utc),
        "exp": expire
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email = payload.get("sub")
        if email is None:
            raise ValueError("Token invalide (sub manquant)")

        return email

    except JWTError:
        raise ValueError("Token invalide ou expiré")
    except Exception as e:
        raise ValueError(f"Erreur lors de la vérification du token : {str(e)}")
    

    
async def get_current_user(access_token: str = Cookie(None)):
    if access_token is None:
        raise HTTPException(status_code=401, detail="Non authentifié")

    try:
        email = verify_access_token(access_token)
        user = getUserByEmail(email)
        if user is None:
            raise HTTPException(status_code=401, detail="Utilisateur non trouvé")
        return User(**dict(user))
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))