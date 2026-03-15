from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class RefreshToken(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    token: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
