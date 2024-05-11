from typing import TYPE_CHECKING
from sqlmodel import Relationship, SQLModel, Field


from pydantic_extra_types.phone_numbers import PhoneNumber

if TYPE_CHECKING:
    from app.models.message_board import DBMessageBoard


class DBUser(SQLModel, table=True):

    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)
    password: str | None = Field(default=None)
    phone_number: PhoneNumber | None = Field(unique=True)
    open_id: str | None = Field(default=None, unique=True)
    nick_name: str | None = Field(default=None)

    messages: list["DBMessageBoard"] = Relationship(back_populates="user")
