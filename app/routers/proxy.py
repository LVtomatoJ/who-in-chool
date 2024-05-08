import json
from fastapi import APIRouter

from app.routers.schemas.proxy import (
    DoSignResp,
    LoginResp,
    SchoolListResp,
    SignListResp,
)
from app.routers.utils.proxy import (
    encrypt_password,
    proxy_do_sign,
    proxy_get_school_list,
    proxy_get_sign_list,
    proxy_login,
)


router = APIRouter()


@router.get("/proxy/get_school_list", response_model=SchoolListResp)
def get_school_list():
    school_list = proxy_get_school_list()
    return SchoolListResp(data=school_list)


@router.get("/proxy/login", response_model=LoginResp)
def school_login(phone_number: str, password: str, school_id: str):
    jw_session = proxy_login(
        phone_number, encrypt_password(phone_number, password), school_id
    )
    return LoginResp(jw_session=jw_session)


@router.get("/proxy/sign/list", response_model=SignListResp)
def get_sign_list(jw_session: str, page: int, limit: int = 10):
    sign_list = proxy_get_sign_list(jw_session, page, limit)
    return SignListResp(data=sign_list)


@router.get("/proxy/sign/do", response_model=DoSignResp)
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
    return DoSignResp(message="签到成功")
