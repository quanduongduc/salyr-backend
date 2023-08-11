
import bcrypt
from fastapi import Depends
from db.database import get_db
from db.schema import User
from sqlalchemy.orm import Session


def get_password_hash(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)) -> User:
    user : User = db.query(User).filter(User.username == username).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        return user
    return None


def extract_user_info(user: User):
    return {
        "id": user.id,
        "username": user.username,
        'email': user.email
    }
