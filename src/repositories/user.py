from datetime import datetime, timezone

from sqlalchemy import select

from models import User
from services import PasswordService

from .base_interface import BaseRepository


class UserRepository(BaseRepository):
    async def get_user_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create_user(self, email: str, password: str, gender: str) -> User:
        hashed_password = PasswordService.hash_password(password)
        user = User(email=email, password=hashed_password, gender=gender)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def authenticate_user(self, email: str, password: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user and PasswordService.verify_password(password, user.password):
            user.last_login = datetime.now(timezone.utc)
            await self.session.commit()
            return user
        return None
