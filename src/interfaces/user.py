from models import User
from services import PasswordService

from .base_interface import BaseInterface


class UserInterface(BaseInterface):
    def create_user(self, email: str, password: str, gender: str) -> User:
        hashed_password = PasswordService.hash_password(password)
        user = User(email=email, password=hashed_password, gender=gender)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def authenticate_user(self, email: str, password: str) -> User | None:
        user = self.session.query(User).filter(User.email == email).first()
        if user and PasswordService.verify_password(password, user.password):
            return user
        return None
