import json
from fastapi import APIRouter

from app.routers.schemas.proxy import (
    LoginResp,
    SchoolListResp,
    SignListResp,
    SuccessResp,
)
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
def school_login(phone_number: str, password: str, school_id: str):
    jw_session = proxy_login(
        phone_number, encrypt_password(phone_number, password), school_id
    )
    return LoginResp(jw_session=jw_session)


@router.get("/login/send_code", response_model=SuccessResp)
def send_code(phone_number: str):
    proxy_send_code(phone_number)
    return SuccessResp(message="发送成功")


@router.get("/reset_password", response_model=SuccessResp)
def reset_password(phone_number: str, password: str, code: str):
    # 重制需要进行两次
    proxy_reset_password(phone_number, encrypt_password(phone_number, password), code)
    proxy_reset_password(phone_number, encrypt_password(phone_number, password), code)
    return SuccessResp(message="重置成功")


@router.get("/sign/list", response_model=SignListResp)
def get_sign_list(jw_session: str, page: int, limit: int = 10):
    sign_list = proxy_get_sign_list(jw_session, page, limit)
    return SignListResp(data=sign_list)


@router.get("/sign/do", response_model=SuccessResp)
def do_sign(
    jw_session: str,
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
        jw_session=jw_session, data=data, id=id, signId=sign_id, schoolId=school_id
    )
    return SuccessResp(message="签到成功")
