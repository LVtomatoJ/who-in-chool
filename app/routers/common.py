from datetime import timedelta
from typing import Annotated

from sqlmodel import select
from app.models.user import DBUser
from app.routers.schemas.wechat import WxUserInfo
from app.routers.utils.common import (
    create_access_token,
    create_user_by_open_id,
    get_user_by_open_id,
    get_user_by_user_id,
    get_wx_user_info,
)
from fastapi import APIRouter, Depends, HTTPException

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.dependencies.db import DBSessionDep
from app.routers.schemas.common import LoginReq, WxLoginReq

# from app.routers.utils.common import (
#     check_user_by_username_password,
#     create_access_token,
# )

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: DBSessionDep,
) -> Token:
    user_id = form_data.username
    user: DBUser | None = get_user_by_user_id(session=session, user_id=int(user_id))
    if not user:
        raise HTTPException(status_code=403, detail="用户不存在")
    access_token = create_access_token(
        data={"user_id": user_id, "jw_session": "demo", "school_id": "4"}
    )
    return Token(access_token=access_token)


@router.post("/login/wx")
def handle_wx_login(
    form_data: WxLoginReq,
    session: DBSessionDep,
) -> Token:
    code = form_data.code
    wx_info: WxUserInfo = get_wx_user_info(code)
    # 查找openid的用户是否存在
    user: DBUser | None = get_user_by_open_id(wx_info.open_id, session)
    if not user:
        # 如果不存在，则创建用户
        user = create_user_by_open_id(wx_info.open_id, session)
    # 创建jwt token
    access_token = create_access_token({"user_id": user.id})
    return Token(access_token=access_token)


# @router.post("/login/web")
# def login(
#     form_data: LoginReq,
#     session: DBSessionDep,
# ) -> Token:
#     username = form_data.username
#     password = form_data.password
#     user = check_user_by_username_password(session, username, password)
#     if not user:
#         raise HTTPException(
#             status_code=403, detail="登录失败，请检查用户名密码或用户状态"
#         )
#     access_token_expires = timedelta(minutes=30)
#     access_token = create_access_token(
#         data={"username": username}, expires_delta=access_token_expires
#     )
#     return Token(access_token=access_token, token_type="bearer")
