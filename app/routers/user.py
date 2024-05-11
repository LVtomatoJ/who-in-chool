from typing import Annotated
from fastapi import APIRouter, Depends

from app.dependencies.auth import JWTUserAuthDep, get_current_user
from app.dependencies.db import DBSessionDep
from app.models.user import DBUser
from app.routers.schemas.common import SuccessResp, UserRead


router = APIRouter()


@router.get("/user", response_model=UserRead)
def get_user(user_model: Annotated[DBUser, Depends(get_current_user)]):
    return user_model


@router.get("/user/change_nick_name", response_model=SuccessResp)
def change_nick_name(session: DBSessionDep, nick_name: str, user_model: JWTUserAuthDep):
    user_model.nick_name = nick_name
    session.add(user_model)
    session.commit()
    session.refresh(user_model)
    return SuccessResp(message="修改成功")
