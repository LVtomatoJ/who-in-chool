from pydantic import BaseModel

from app.models.message_board import DBMessageBoard


class MessageUserInfo(BaseModel):
    id: int
    nick_name: str | None


class MessageInfo(BaseModel):
    id: int
    user_id: int
    content: str
    send_time: float
    school_id: int
    user: MessageUserInfo


class MessageListResp(BaseModel):
    data: list[MessageInfo]
