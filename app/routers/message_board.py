from datetime import datetime
from typing import List
from fastapi import APIRouter

from app.dependencies.auth import JWTProxySessionDep
from app.dependencies.db import DBSessionDep
from app.models.message_board import DBMessageBoard
from app.routers.schemas.message_board import MessageInfo, MessageListResp
from app.routers.utils.message_board import (
    formate_one_message,
    handle_add_one_message,
    handle_get_message_list,
)
from app.routers.schemas.common import SuccessResp


router = APIRouter(prefix="/message_board", tags=["留言板"])


@router.get("/get_message_list", response_model=MessageListResp)
def get_message_list(
    session: DBSessionDep, token: JWTProxySessionDep, page: int, limit: int = 10
):
    message_board_model_list: List[DBMessageBoard] = handle_get_message_list(
        session, token.school_id, page, limit
    )
    message_list = []
    for message_board_model in message_board_model_list:
        formate_msg = formate_one_message(message_board_model)
        message_list.append(formate_msg)
    return MessageListResp(data=message_list)


@router.get("/publish_message", response_model=MessageInfo)
def publish_message(session: DBSessionDep, token: JWTProxySessionDep, content: str):
    message_model:DBMessageBoard = handle_add_one_message(
        session=session,
        user_id=token.user_model.id,
        school_id=token.school_id,
        content=content,
    )
    formate_msg = formate_one_message(message_model)
    return formate_msg
