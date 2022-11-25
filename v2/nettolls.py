import json
import requests
from requests.cookies import RequestsCookieJar
from tinydb.table import Document
from default import Miniprogram

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
        cookies: RequestsCookieJar = r.cookies
        data = r.json()
        if data['code'] != 0:
            return {'code': 405, 'msg': data['message']}
        jwsession = cookies.items()[0][1]
        return {'code': 0, 'msg': "jwsession获取成功", 'data': {'jwsession': jwsession}}
    except Exception as e:
        print(e.args)
        return {'code': 503, "msg": "网络请求异常"}


def getSchool(jwsession: str):
    try:
        url = 'https://gw.wozaixiaoyuan.com/basicinfo/mobile/home/index'
        r: requests.Response = requests.post(
            url=url,
            headers={'JWSESSION': jwsession}
        )
        data = r.json()
        if data['code'] != 0:
            return {'code': 406, 'msg': "登录失效"}
        school = data['data']['userInfo']['school']
        return {'code': 0, 'data': {'school': school}}
    except Exception as e:
        print(e.args)
        return {'code': 503, "msg": "网络请求异常"}


def doHeat(jwsession: str, data: Document):
    #          超时：1
    #          session过期：-10
    #          其他：101
    try:

        # print(type())
        # data = dict(data)
        # print(data)
        # print('====')
        # print(dataa)
        url = rf'https://student.wozaixiaoyuan.com/heat/save.json'
        #headers = {"content-type": "application/x-www-form-urlencoded"}
        r: requests.Response = requests.post(
            url=url, headers={'JWSESSION': jwsession}, data=data)
        data = r.json()
        code = data['code']
        if code != 0:
            if code == -10:
                return {'code': '505', 'msg': "绑定过期，重新绑定后重试"}
            return {'code': '506', 'msg': "请求未知错误", 'data': {'code': code}}
        return {'code': 0, 'msg': "网络请求成功"}
    except Exception as e:
        print(e.args)
        return {'code': 503, "msg": "网络请求异常"}


def getSignList(jwsession: str):
    try:
        url = rf'https://student.wozaixiaoyuan.com/sign/getSignMessage.json'
        r = requests.post(url=url, headers={"JWSESSION": jwsession}, data={
                          "page": 1, "size": 5})
        res = r.json()
        code = res['code']
        if code != 0:
            if code == -10:
                return {'code': '505', 'msg': "绑定过期，重新绑定后重试"}
            return {'code': '506', 'msg': "请求未知错误", 'data': {'code': code}}
        return {'code': 0, 'msg': "网络请求成功", 'data': {'signlist': res['data']}}
    except Exception as e:
        print(e.args)
        return {'code': 503, "msg": "网络请求异常"}


def doSign(jwsession: str, data: dict):
    try:
        url = rf"https://student.wozaixiaoyuan.com/sign/doSign.json"
        data = json.dumps(data)
        r = requests.post(url=url,
                          headers={"JWSESSION": jwsession},
                          data=data)
        data = r.json()
        code = data['code']
        if code != 0:
            if code == -10:
                return {'code': '505', 'msg': "绑定过期，重新绑定后重试"}
            return {'code': '506', 'msg': "请求未知错误", 'data': {'code': code}}
        return {'code': 0, 'msg': "网络请求成功"}
    except Exception as e:
        print(e.args)
        return {'code': 503, "msg": "网络请求异常"}


def getOpenid(code:str):
    try:
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        data = {'appid':Miniprogram.appid,'secret':Miniprogram.secret,'js_code':code,'grant_type':'authorization_code'}
        r: requests.Response = requests.post(
            url=url,data=data)
        data = r.json()
        if data.get('errcode'):
            return {'code':data['errcode'],'msg':data['errmsg']}
        else:
            return {'code':0,'msg':"获取openid成功",'data':{'openid':data['openid']}}
    except Exception as e:
        print(e.args)
        return {'code': 503, "msg": "网络请求异常"}


# print(getOpenid(code='043ep30w3a8GDZ2o852w3UNxyX1ep30i'))