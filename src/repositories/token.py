from sqlalchemy import select

from models import BlacklistedToken

from .base_interface import BaseRepository


class TokenRepository(BaseRepository):
    async def is_token_blacklisted(self, token: str) -> bool:
        result = await self.session.execute(
            select(BlacklistedToken).where(BlacklistedToken.token == token)
        )
        return result.scalar_one_or_none() is not None

    async def blacklist_token(self, token: str):
        refresh_token = BlacklistedToken(token=token)
        await self.session.add(refresh_token)
        await self.session.commit()
