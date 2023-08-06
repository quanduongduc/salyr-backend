

from fastapi import HTTPException, Header
from fastapi.security import HTTPBearer

reuseable_oauth = HTTPBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


def get_current_user(token: str = Header(None)) -> str:
    if token is None:
        raise HTTPException(status_code=401, detail="Bearer token required")

    # In a real-world scenario, you would validate the token and fetch user information
    # For this example, let's assume the token contains the username.
    # Replace this with your actual authentication and user retrieval logic.
    user = "example_user"

    return user
