from models import RefreshToken

from .base_interface import BaseInterface


class TokenInterface(BaseInterface):
    def blacklist_token(self, token: str):
        refresh_token = RefreshToken(token=token)
        self.session.add(refresh_token)
        self.session.commit()
