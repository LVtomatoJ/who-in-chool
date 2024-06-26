from pydantic import BaseModel


class LoginReq(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    user_id: int


class UserRead(BaseModel):
    id: int
    nick_name: str|None


class WxLoginReq(BaseModel):
    code: str


class SuccessResp(BaseModel):
    message: str
