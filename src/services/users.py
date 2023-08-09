

from fastapi import HTTPException, Header
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from db.schema.schema import User
from models.user_models import UserRequest

from services.auth import get_password_hash

def get_current_user(token: str = Header(None)) -> str:
    if token is None:
        raise HTTPException(status_code=401, detail="Bearer token required")

    # In a real-world scenario, you would validate the token and fetch user information
    # For this example, let's assume the token contains the username.
    # Replace this with your actual authentication and user retrieval logic.
    user = "example_user"

    return user

def create_user(user_data: UserRequest, db: Session) -> User:
    new_user = User(
        username=user_data.username,
        email=user_data.email,
    )
    
    # Hash the user's password before storing it
    hashed_password = get_password_hash(user_data.password)
    new_user.password = hashed_password
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user