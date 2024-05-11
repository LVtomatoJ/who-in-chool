from datetime import datetime
from sqlmodel import Session, select
from app.models.message_board import DBMessageBoard
from app.routers.schemas.message_board import MessageInfo, MessageUserInfo


def handle_get_message_list(
    session: Session, school_id: int, page: int, limit: int = 10
):
    offset = (page - 1) * limit
    statement = (
        select(DBMessageBoard)
        .where(DBMessageBoard.school_id == school_id)
        .order_by(DBMessageBoard.send_time.desc())
        .offset(offset)
        .limit(limit)
    )
    results = session.exec(statement)
    messages = results.all()
    return messages


def formate_one_message(message: DBMessageBoard):
    return MessageInfo(
        id=message.id,
        user_id=message.user_id,
        content=message.content,
        send_time=message.send_time,
        school_id=message.school_id,
        user=MessageUserInfo(
            id=message.user.id,
            nick_name=(
                message.user.nick_name
                if message.user.nick_name
                else "不愿透露姓名的同学"
            ),
        ),
    )


def handle_add_one_message(
    session: Session, user_id: str, school_id: str, content: str
):
    message_board_model: DBMessageBoard = DBMessageBoard(
        user_id=user_id,
        school_id=school_id,
        content=content,
        send_time=datetime.now().timestamp(),
    )
    session.add(message_board_model)
    session.commit()
    session.refresh(message_board_model)
    return message_board_model
