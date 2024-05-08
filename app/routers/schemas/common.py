from pydantic import BaseModel


class LoginReq(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    user_id: int


class UserRead(BaseModel):
    id: int


class WxLoginReq(BaseModel):
    code: str
