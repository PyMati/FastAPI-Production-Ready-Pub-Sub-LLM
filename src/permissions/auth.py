from fastapi import HTTPException, Request, status

from config import config
from enums import RequestStateKeys
from services import JwtService


def is_authenticated(request: Request) -> bool:
    access_token = request.cookies.get(config.ACCESS_COOKIE_NAME)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    try:
        user_id = JwtService.verify_token(access_token)["user_id"]
        setattr(request.state, RequestStateKeys.USER_ID.value, user_id)
        return True
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
