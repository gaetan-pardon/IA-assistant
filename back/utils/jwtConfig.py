from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from dotenv import dotenv_values

config = dotenv_values(".env")

SECRET_KEY = config["SECRET_KEY"]
ALGORITHM = config["ALGORITHM"]
TOKEN_EXPIRE_MINUTES = int(config["TOKEN_EXPIRE_MINUTES"])


def create_access_token(user_id: int) -> str:
    """Create a JWT access token for the given user ID.
    Args:
        user_id (int): The ID of the user.
    Returns:
        str: The encoded JWT token.
    """
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "iat": datetime.now(tz=timezone.utc),
        "exp": expire
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")
        if user_id is None:
            raise ValueError("Token invalide (sub manquant)")

        return int(user_id)

    except JWTError:
        raise ValueError("Token invalide ou expiré")
    except Exception as e:
        raise ValueError(f"Erreur lors de la vérification du token : {str(e)}")