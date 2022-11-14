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
        url = rf'https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username'
        r: requests.Response = requests.post(
            url=url, params={"username": bindid, "password": password})
        cookies:RequestsCookieJar = r.cookies
        data = r.json()
        if data['code'] != 0:
            return {'code':405,'msg':data['message']}
        jwsession = cookies.items()[0][1]
        return {'code':0,'msg':"jwsession获取成功",'data':{'jwsession':jwsession}}
    except Exception as e:
        print(e.args)
        return {'code': 503, "msg": "网络请求失败"}



def getSchool(jwsession:str):
    try:
        url='https://gw.wozaixiaoyuan.com/basicinfo/mobile/home/index'
        r: requests.Response = requests.post(
            url=url,
            headers={'JWSESSION':jwsession}
        )
        data = r.json()
        if data['code'] != 0:
            return {'code':406,'msg':"登录失效"}
        school = data['data']['userInfo']['school']
        return {'code':0,'data':{'school':school}}
    except Exception as e:
        print(e.args)
        return {'code': 503, "msg": "网络请求失败"}