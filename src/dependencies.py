from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from models.models import CurrentUser


def get_current_user(Authorize: AuthJWT = Depends()) -> CurrentUser:
    user_info = Authorize.get_raw_jwt()
    return CurrentUser(
        {
            "user_id": user_info["id"],
            "email": user_info["email"],
            "user_name": user_info["user_name"],
        }
    )
