from fastapi import APIRouter
from fastapi import Depends, HTTPException
from db.database import get_db
from db.schema.schema import User
from helpers.http_status import StatusCode
from helpers.jwt import generate_tokens
from models.auth_models import AuthResponse, UserLogin
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from models.user_models import UserRequest

from services.auth import authenticate_user
from services.users import create_user


router = APIRouter()


@router.post("/register")
def register_user(UserBody: UserRequest, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    existing_user = db.query(User).filter(User.username == UserBody.user_name).first()
    if existing_user:
        raise HTTPException(
            status_code=StatusCode.HTTP_404_NOT_FOUND,
            detail="Username already taken",
        )
    
    # Create the new user
    user = create_user(UserBody, db)
    
    # Optionally, generate tokens or perform other actions
    access_token, refresh_token = generate_tokens(user, Authorize)
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
    access_token, refresh_token = generate_tokens(user, Authorize)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh-token/")
async def refresh_access_token(Authorize: AuthJWT = Depends(use_cache=False)):
    try:
        Authorize.jwt_refresh_token_required()
        user_info = Authorize.get_raw_jwt()
        access_token, refresh_token = generate_tokens(user_info, Authorize)
    except:
        raise HTTPException(400, "Failed to refresh access token.")
    return {"accessToken": access_token, "refreshToken": refresh_token}
