from fastapi import APIRouter
from fastapi import Depends, HTTPException
from db.database import get_db
from db.schema import User
from helpers.http_status import StatusCode
from helpers.jwt import generate_tokens
from helpers.utils import JWTBearer
from models.auth_models import AuthResponse, UserLogin
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from models.user_models import UserRequest

from services.auth import authenticate_user, extract_user_info
from services.users import create_user


router = APIRouter()


@router.post("/register")
def register_user(UserBody: UserRequest, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    existing_user = db.query(User).filter(User.username == UserBody.username).first()
    if existing_user:
        raise HTTPException(
            status_code=StatusCode.HTTP_404_NOT_FOUND,
            detail="Username already taken",
        )

    user = create_user(UserBody, db)

    user_info = extract_user_info(user)

    access_token, refresh_token = generate_tokens(user_info, Authorize)
    return {"accessToken": access_token, "refreshToken": refresh_token}


@router.post("/login", response_model=AuthResponse)
def login_user(
    form_data: UserLogin, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=StatusCode.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    user_info = extract_user_info(user)

    access_token, refresh_token = generate_tokens(user_info, Authorize)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh-token/", dependencies=[Depends(JWTBearer())])
def refresh_access_token(Authorize: AuthJWT = Depends(use_cache=False)):
    try:
        Authorize.jwt_refresh_token_required()
        user_info = Authorize.get_raw_jwt()
        access_token, refresh_token = generate_tokens(user_info, Authorize)
    except:
        raise HTTPException(400, "Failed to refresh access token.")
    return {"accessToken": access_token, "refreshToken": refresh_token}
