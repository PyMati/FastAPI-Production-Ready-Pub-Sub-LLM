from sqlalchemy import select

from models import User
from services import PasswordService

from .base_interface import BaseInterface


class UserInterface(BaseInterface):
    def get_user_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)
        return self.session.execute(statement).scalars().first()

    def create_user(self, email: str, password: str, gender: str) -> User:
        hashed_password = PasswordService.hash_password(password)
        user = User(email=email, password=hashed_password, gender=gender)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def authenticate_user(self, email: str, password: str) -> User | None:
        statement = select(User).where(User.email == email)
        user = self.session.execute(statement).scalars().first()
        if user and PasswordService.verify_password(password, user.password):
            return user
        return None
