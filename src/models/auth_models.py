from models.models import ORJSONModel


class UserCreate(ORJSONModel):
    username: str
    password: str

class UserLogin(ORJSONModel):
    username: str
    password: str

class AuthResponse(ORJSONModel):
    access_token: str
    refresh_token: str

class TokenData(ORJSONModel):
    user_id: str
    username: str