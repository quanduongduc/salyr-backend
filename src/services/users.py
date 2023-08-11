from fastapi import HTTPException, Header, UploadFile
from sqlalchemy.orm import Session
from db.schema import User, UserFavorite
from helpers.constants import S3_AVATAR_FOLDER_PATH
from helpers.http_status import StatusCode
from helpers.s3 import generate_presigned_download_url, upload_file_to_s3
from models.songs_models import SongResponse
from models.user_models import UserCreate, UserResponse, UserUpdate

from services.auth import get_password_hash

def get_current_user(token: str = Header(None)) -> str:
    if token is None:
        raise HTTPException(status_code=401, detail="Bearer token required")

    # In a real-world scenario, you would validate the token and fetch user information
    # For this example, let's assume the token contains the username.
    # Replace this with your actual authentication and user retrieval logic.
    user = "example_user"

    return user


def get_user_by_id(db, id: str):
    user = db.query(User).filter(
        User.id == id).first()

    user_reponse = generate_user_response(user)

    return user_reponse


def generate_user_response(user):
    avatar_url = generate_presigned_download_url(
        key=f'{S3_AVATAR_FOLDER_PATH}{user.id}')

    return UserResponse(
        id=user.id,
        username=user.username,
        alias=user.alias,
        email=user.email,
        created_at=user.created_at,
        last_play=user.last_play,
        playlists=user.playlists,
        avatar_url=avatar_url
    )


def get_favorites(db, id: str) -> SongResponse:
    favorite = db.query(User.favorites).filter(
        User.id == id).first()

    return favorite


def create_user(user_data: UserCreate, db: Session) -> User:
    new_user = User(
        username=user_data.username,
        email=user_data.email,
    )

    hashed_password = get_password_hash(user_data.password)
    new_user.hashed_password = hashed_password

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def update_user(db: Session, user_info: UserUpdate, id : id, avatar_file: UploadFile = None) -> UserResponse:
    db_user = db.query(User).filter(User.id == id).first()
    if db_user:
        for key, value in user_info.dict().items():
            setattr(db_user, key, value)

        if avatar_file:
            # Save the avatar and update the avatar_url in the user model
            key = f'{S3_AVATAR_FOLDER_PATH}{db_user.id}'
            uploade_response = upload_file_to_s3(
                key=key, file=avatar_file)

            if uploade_response['ResponseMetadata']['HTTPStatusCode'] != 200:
                raise HTTPException(
                    status_code=StatusCode.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error uploading avatar")

        db.commit()
        db.refresh(db_user)

        user_response = generate_user_response(db_user)

        return user_response
    else:
        return None


def add_to_favorites(db: Session, user_id: int, song_id: int):
    user = db.query(User.id).filter(User.id == user_id).first()
    if user:
        new_favorite = UserFavorite(user_id=user_id, song_id=song_id)
        db.add(new_favorite)
        db.commit()
        db.refresh(new_favorite)
        return new_favorite
    else:
        return None


def remove_from_favorites(db: Session, user_id: int, song_id: int) -> bool:
    favorite = db.query(UserFavorite).filter(
        UserFavorite.user_id == user_id,
        UserFavorite.song_id == song_id
    ).first()

    if favorite:
        db.delete(favorite)
        db.commit()
        return True
    else:
        return False
