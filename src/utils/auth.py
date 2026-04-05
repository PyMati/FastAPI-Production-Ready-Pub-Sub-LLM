from fastapi.responses import JSONResponse

from config import config
from models import User
from services.cookie_service import CookieService
from services.csrf_service import CSRFService
from services.jwt_service import JwtService


def process_authentication_response(user: User) -> JSONResponse:
    tokens = JwtService.create_tokens(user.id)
    csrf_token = CSRFService.generate_csrf_token()
    json_response = JSONResponse(
        content={
            "id": user.id,
            "email": user.email,
            "gender": user.gender,
        }
    )
    CookieService.set_auth_cookies(
        json_response, tokens["access_token"], tokens["refresh_token"]
    )
    CookieService.set_cookie(
        json_response,
        config.CSRF_TOKEN_NAME,
        csrf_token,
        config.CSRF_COOKIE_EXPIRE_MINUTES * 60,
        False,
    )
    return json_response


def process_refresh_response(user_id: int) -> JSONResponse:
    tokens = JwtService.create_tokens(user_id)["access_token"]
    json_response = JSONResponse(content={"detail": "Token refreshed"})
    CookieService.set_cookie(
        json_response,
        config.ACCESS_COOKIE_NAME,
        tokens,
        config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return json_response
