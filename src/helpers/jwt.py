import time
from typing import Dict
import jwt
import datetime
from fastapi_jwt_auth import AuthJWT
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


def generate_tokens(user_info: Dict, authorize: AuthJWT):
    headers = {
        "typ": "JWT",
        "alg": settings.JWT_ALG
    }
    claim_access = user_info.copy()
    claim_refresh = user_info.copy()
    claim_access['type'] = "access"
    claim_refresh['type'] = "refresh"

    current_timestamp = int(time())
    claim_access['exp'] = current_timestamp + 3600      # seconds
    claim_refresh['exp'] = current_timestamp + 3600*24   # seconds
    access_token = authorize.create_access_token(user_claims=claim_access,
                                                 subject=user_info.get("catid"),
                                                 algorithm="RS256",
                                                 headers=headers)
    refresh_token = authorize.create_refresh_token(user_claims=claim_refresh,
                                                   subject=user_info.get("catid"),
                                                   algorithm="RS256",
                                                   headers=headers)

    return access_token, refresh_token