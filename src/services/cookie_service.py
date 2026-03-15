from fastapi import Response

from config import config


class CookieService:
    @staticmethod
    def set_auth_cookies(response: Response, access_token: str, refresh_token: str):
        CookieService.set_cookie(
            response,
            config.ACCESS_COOKIE_NAME,
            access_token,
            config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        CookieService.set_cookie(
            response,
            config.REFRESH_COOKIE_NAME,
            refresh_token,
            config.JWT_REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        )

    @staticmethod
    def set_cookie(response: Response, key: str, value: str, max_age: int):
        response.set_cookie(
            key=key,
            value=value,
            max_age=max_age,
            httponly=config.COOKIE_SECURE,
            secure=config.COOKIE_SECURE,
            samesite="lax",
        )

    @staticmethod
    def delete_cookie(response: Response, key: str):
        response.delete_cookie(key=key)
