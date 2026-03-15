from datetime import datetime, timedelta, timezone

import jwt

from config import config


class JwtService:
    @classmethod
    def create_access_token(cls, user_id: int) -> str:
        expiry = datetime.now(timezone.utc) + timedelta(
            minutes=config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload = {"user_id": user_id, "type": "access", "exp": expiry}
        token = jwt.encode(
            payload, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM
        )
        return token

    @classmethod
    def create_refresh_token(cls, user_id: int) -> str:
        expiry = datetime.now(timezone.utc) + timedelta(
            minutes=config.JWT_REFRESH_TOKEN_EXPIRE_MINUTES
        )
        payload = {"user_id": user_id, "type": "refresh", "exp": expiry}
        token = jwt.encode(
            payload, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM
        )
        return token

    @classmethod
    def create_tokens(cls, user_id: int) -> dict:
        return {
            "access_token": cls.create_access_token(user_id),
            "refresh_token": cls.create_refresh_token(user_id),
        }

    @classmethod
    def decode_token(cls, token: str) -> dict:
        try:
            payload = jwt.decode(
                token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")

    @classmethod
    def verify_token(cls, token: str) -> dict:
        payload = cls.decode_token(token)
        if payload.get("type") != "access":
            raise Exception("Invalid token type")
        return payload
