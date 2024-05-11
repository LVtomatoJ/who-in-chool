from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import Relationship, SQLModel, Field


from app.models.user import DBUser


class DBMessageBoard(SQLModel, table=True):

    __tablename__ = "message_board"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    content: str = Field()
    send_time: int = Field()
    school_id: int = Field()

    user: DBUser = Relationship(back_populates="messages")
