from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

from config import config


class Base(DeclarativeBase):
    pass


engine = create_engine(config.DATABASE_URL, echo=True)


def init_db():
    from models import Chat, Message, RefreshToken, User  # noqa: F401

    Base.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
