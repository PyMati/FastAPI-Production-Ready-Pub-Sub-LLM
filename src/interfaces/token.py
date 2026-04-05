from sqlalchemy import select

from models import RefreshToken

from .base_interface import BaseInterface


class TokenInterface(BaseInterface):
    def is_token_blacklisted(self, token: str) -> bool:
        statement = select(RefreshToken).where(RefreshToken.token == token)
        result = self.session.execute(statement).scalars().first()
        return result is not None

    def blacklist_token(self, token: str):
        refresh_token = RefreshToken(token=token)
        self.session.add(refresh_token)
        self.session.commit()
