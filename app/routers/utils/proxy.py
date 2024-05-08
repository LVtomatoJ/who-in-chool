import json
from fastapi import HTTPException
from phonenumbers import PhoneNumber
import requests
from requests.cookies import RequestsCookieJar

from app.routers.schemas.proxy import SchoolInfo


import urllib.parse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import base64


def encrypt(t, e):
    key = e.encode("utf-8")
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = pad(t.encode("utf-8"), AES.block_size)
    ciphertext = cipher.encrypt(plaintext)
    return base64.b64encode(ciphertext).decode("utf-8")


def encrypt_password(phone_number, password):
    a = (phone_number + "0000000000000000")[:16]
    c = urllib.parse.quote(encrypt(password, a))
    return c


def proxy_get_school_list() -> list[SchoolInfo]:
    """
    获取学校列表
    """
    try:
        url = "https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/getSchoolList"
        res = requests.get(url)
        res_json = res.json()
        if res_json["code"] != 0:
            raise HTTPException(status_code=401, detail=res_json["message"])
        return res_json["data"]
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="服务器网络异常")


def proxy_login(phone_number: str, password: str, school_id: str) -> str:
    try:
        url = rf"https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username"
        res = requests.post(
            url=url,
            params={
                "username": phone_number,
                "password": password,
                "schoolId": school_id,
            },
        )
        res_json = res.json()
        if res_json["code"] != 0:
            raise HTTPException(status_code=400, detail=res_json["message"])
        cookies: RequestsCookieJar = res.cookies
        jw_session = cookies.items()[0][1]
        return jw_session
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="服务器网络异常")


def proxy_get_sign_list(jw_session: str, page: int, limit=10):
    try:
        url = f"https://gw.wozaixiaoyuan.com/sign/mobile/receive/getMySignLogs?page={page}&size={limit}"
        res = requests.get(
            url,
            headers={"Cookie": f"JWSESSION={jw_session}"},
        )
        res_json = res.json()
        if res_json["code"] != 0:
            raise HTTPException(status_code=500, detail=res_json["msg"])
        return res_json["data"]
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="服务器网络异常")


def proxy_do_sign(jw_session: str, data: dict, id: str, schoolId: str, signId: str):
    try:
        url = f"https://gw.wozaixiaoyuan.com/sign/mobile/receive/doSignByArea"
        data = json.dumps(data)
        res = requests.post(
            url=url,
            headers={"JWSESSION": jw_session},
            params={"id": id, "schoolId": schoolId, "signId": signId},
            data=data,
        )
        res_json = res.json()
        if res_json["code"] != 0:
            raise HTTPException(status_code=400, detail=res_json["message"])

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="服务器网络异常")
