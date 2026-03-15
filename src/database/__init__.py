from sqlmodel import SQLModel, create_engine

from config import config
from models import Chat, Message, User  # noqa: F401

engine = create_engine(config.DATABASE_URL, echo=True)
SQLModel.metadata.create_all(engine)
