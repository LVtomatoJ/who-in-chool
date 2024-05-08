from sqlmodel import SQLModel, Field


from pydantic_extra_types.phone_numbers import PhoneNumber


class DBUser(SQLModel, table=True):

    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)
    password: str | None = Field(default=None)
    phone_number: PhoneNumber | None = Field(default=None, unique=True)
    open_id: str | None = Field(default=None, unique=True)
