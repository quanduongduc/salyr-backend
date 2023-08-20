from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from helpers.exceptions import NotAuthenticated
from models.user_models import CurrentUser


def get_current_user(Authorize: AuthJWT = Depends()) -> CurrentUser:
    user_info = Authorize.get_raw_jwt()
    if not user_info :
        raise NotAuthenticated()
    return CurrentUser(
        user_id=user_info["id"],
        email=user_info["email"],
        username=user_info["username"],
    )
