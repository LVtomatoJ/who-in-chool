from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select
from app.models.user import DBUser
from app.routers.schemas.wechat import WxUserInfo
from fastapi import HTTPException
from app.dependencies.wechat.wxa import wxa_client
from wechatpy import WeChatClientException
from jose import jwt

from app.config import settings


SECRET_KEY = settings.token_secret
ALGORITHM = "HS256"


def get_wx_user_info(code: str) -> WxUserInfo:
    try:
        result = wxa_client.code_to_session(code)
        union_id = result.get("unionid")
        open_id = result.get("openid")
        session_key = result.get("session_key")
        return WxUserInfo(
            open_id=open_id,
            session_key=session_key,
            union_id=union_id,
        )
    except WeChatClientException as e:
        raise HTTPException(
            status_code=500,
            detail=e.response.content.decode("utf-8"),
        )


def get_user_by_open_id(
    open_id: str,
    session: Session,
) -> DBUser | None:
    """
    根据 open_id 获取用户
    """
    statement = select(DBUser).where(DBUser.open_id == open_id)
    results = session.exec(statement)
    user: DBUser | None = results.first()
    return user


def get_user_by_user_id(
    user_id: int,
    session: Session,
) -> DBUser | None:
    """
    根据 open_id 获取用户
    """
    statement = select(DBUser).where(DBUser.id == user_id)
    results = session.exec(statement)
    user: DBUser | None = results.first()
    return user


def create_user_by_open_id(open_id: str, session: Session):
    """
    根据 open_id 创建用户
    """
    user: DBUser = DBUser(open_id=open_id)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def create_access_token(data: dict):
    expires_delta = settings.access_token_expires_delta
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
