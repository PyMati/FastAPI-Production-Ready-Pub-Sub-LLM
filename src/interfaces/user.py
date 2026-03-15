from sqlmodel import Session

from models import User
from services import PasswordService


class UserInterface:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, email: str, password: str, gender: str) -> User:
        hashed_password = PasswordService.hash_password(password)
        user = User(email=email, password=hashed_password, gender=gender)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
