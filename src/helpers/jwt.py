import jwt
import datetime
from jwt.exceptions import ExpiredSignatureError, DecodeError
from config.config import settings
# Secret key for signing and verifying the JWT


def create_jwt(user_id: int, username: str, expiration_hours: int = 1) -> str:
    """
    Create a JSON Web Token (JWT) with specified user information.

    Args:
        user_id (int): User ID.
        username (str): Username.
        expiration_hours (int, optional): Expiration time in hours. Defaults to 1.

    Returns:
        str: Encoded JWT.
    """
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=expiration_hours)
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALG)
    return token


def decode_jwt(token: str) -> dict:
    """
    Decode and verify a JSON Web Token (JWT).

    Args:
        token (str): Encoded JWT.

    Returns:
        dict: Decoded payload.
    Raises:
        ExpiredSignatureError: If the token has expired.
        DecodeError: If the token is invalid.
    """
    try:
        decoded_payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALG)
        return decoded_payload
    except ExpiredSignatureError:
        raise ExpiredSignatureError("Token has expired.")
    except DecodeError:
        raise DecodeError("Invalid token.")
