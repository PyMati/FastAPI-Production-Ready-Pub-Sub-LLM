from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from config import config
from models import Chat, Message, User  # noqa: F401

engine = create_engine(config.DATABASE_URL, echo=True)
SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
