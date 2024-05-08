from pydantic import BaseModel


class WxUserInfo(BaseModel):
    open_id: str
    session_key: str
    union_id: str | None = None
