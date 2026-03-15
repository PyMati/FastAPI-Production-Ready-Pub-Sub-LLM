from sqlmodel import Field, SQLModel


class User(SQLModel):
    id: int = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    gender: str
    email: str
    password: str
