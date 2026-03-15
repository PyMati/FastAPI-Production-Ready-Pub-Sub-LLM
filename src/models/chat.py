import uuid

from sqlmodel import Field, Relationship, SQLModel


class Chat(SQLModel, table=True):
    id: str = Field(default_factory=uuid.uuid4, primary_key=True)

    messages: list["Message"] = Relationship(back_populates="chat")
    is_archived: bool = Field(default=False)


class Message(SQLModel, table=True):
    id: str = Field(default_factory=uuid.uuid4, primary_key=True)
    chat_id: str = Field(foreign_key="chat.id")
    chat: Chat = Relationship(back_populates="messages")
