import json
from fastapi import APIRouter

from app.dependencies.auth import JWTProxySessionDep
from app.dependencies.db import DBSessionDep
from app.models.user import DBUser
from app.routers.schemas.proxy import (
    LoginResp,
    SchoolListResp,
    SignListResp,
)
from app.routers.schemas.common import SuccessResp
from app.routers.utils.common import create_access_token, get_user_by_phone_number
from app.routers.utils.proxy import (
    encrypt_password,
    proxy_do_sign,
    proxy_get_school_list,
    proxy_get_sign_list,
    proxy_login,
    proxy_reset_password,
    proxy_send_code,
)


router = APIRouter(prefix="/proxy", tags=["代理"])


@router.get("/get_school_list", response_model=SchoolListResp)
def get_school_list():
    school_list = proxy_get_school_list()
    return SchoolListResp(data=school_list)


@router.get("/login", response_model=LoginResp)
def school_login(
    session: DBSessionDep, phone_number: str, password: str, school_id: str
):
    e_password = encrypt_password(phone_number, password)
    jw_session = proxy_login(phone_number, e_password, school_id)
    user = get_user_by_phone_number(phone_number, session)
    if not user:
        # 创建用户
        user = DBUser(
            phone_number=phone_number,
            password=e_password,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
    if user.password != e_password:
        # 更新密码
        user.password = e_password
        session.commit()
    token = create_access_token(
        data={"user_id": user.id, "school_id": school_id, "jw_session": jw_session}
    )
    return LoginResp(token=token)


@router.get("/login/send_code", response_model=SuccessResp)
def send_code(phone_number: str):
    proxy_send_code(phone_number)
    return SuccessResp(message="发送成功")


@router.get("/reset_password", response_model=SuccessResp)
def reset_password(session: DBSessionDep, phone_number: str, password: str, code: str):
    proxy_reset_password(phone_number, password, code)
    user = get_user_by_phone_number(phone_number=phone_number, session=session)
    if user:
        user.password = encrypt_password(phone_number, password)
        session.commit()
    return SuccessResp(message="重置成功")


@router.get("/sign/list", response_model=SignListResp)
def get_sign_list(token: JWTProxySessionDep, page: int, limit: int = 10):
    sign_list = proxy_get_sign_list(token.jw_session, page, limit)
    return SignListResp(data=sign_list)


@router.get("/sign/do", response_model=SuccessResp)
def do_sign(
    token: JWTProxySessionDep,
    id: str,
    school_id: str,
    sign_id: str,
    latitude: float,
    longitude: float,
):
    data = {
        "latitude": latitude,
        "longitude": longitude,
        "nationcode": "",
        "country": "",
        "province": "",
        "citycode": "",
        "city": "",
        "adcode": "",
        "district": "",
        "towncode": "",
        "township": "",
        "streetcode": "",
        "street": "",
        "inArea": 1,
        "areaJSON": json.dumps(
            {
                "type": "",
                "circle": {
                    "latitude": "",
                    "longitude": "",
                    "radius": "",
                },
                "id": "",
                "name": "",
            }
        ),
    }
    proxy_do_sign(
        jw_session=token.jw_session,
        data=data,
        id=id,
        signId=sign_id,
        schoolId=school_id,
    )
    return SuccessResp(message="签到成功")
