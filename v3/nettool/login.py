import requests
from requests.cookies import RequestsCookieJar


def getJwsession(bindid: str, password: str):
    """获取session

    Args:
        bindid (str):
        password (str):

    Returns:
        dict:{
            code:[
                0:成功
                405:登录请求失败
                503:网络请求失败
            ]
        }
    """
    try:
        url = rf"https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username"
        r: requests.Response = requests.post(
            url=url,
            params={"username": bindid, "password": password, "schoolId": "4"},
        )
        cookies: RequestsCookieJar = r.cookies
        data = r.json()
        if data["code"] != 0:
            return {"code": 405, "msg": data["message"]}
        jwsession = cookies.items()[0][1]
        return {"code": 0, "msg": "jwsession获取成功", "data": {"jwsession": jwsession}}
    except Exception as e:
        print(e.args)
        return {"code": 1, "msg": e.args}


import urllib.parse


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


def encrypt_password(username, password):
    a = (username + "0000000000000000")[:16]
    c = urllib.parse.quote(encrypt(password, a))
    return c


# print(encrypt_password("15389064060", "123456"))

# print(getJwsession("15389064060", f"%252B%252Fivbr9i8XPiuH11Hxf2VQ%253D%253D"))


print(getJwsession("15389064060", encrypt_password("15389064060", "123456")))
