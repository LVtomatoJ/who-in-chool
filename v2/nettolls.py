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


# def doHeat(jwsession: str, data: Document):
#     #          超时：1
#     #          session过期：-10
#     #          其他：101
#     try:

#         # print(type())
#         # data = dict(data)
#         # print(data)
#         # print('====')
#         # print(dataa)
#         url = rf'https://student.wozaixiaoyuan.com/heat/save.json'
#         #headers = {"content-type": "application/x-www-form-urlencoded"}
#         r: requests.Response = requests.post(
#             url=url, headers={'JWSESSION': jwsession}, data=data)
#         data = r.json()
#         code = data['code']
#         if code != 0:
#             if code == -10:
#                 return {'code': '505', 'msg': "绑定过期，重新绑定后重试"}
#             return {'code': '506', 'msg': "请求未知错误", 'data': {'code': code}}
#         return {'code': 0, 'msg': "网络请求成功"}
#     except Exception as e:
#         print(e.args)
#         return {'code': 503, "msg": "网络请求异常"}

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
        url = rf'https://gw.wozaixiaoyuan.com/health/mobile/health/save?batch=400001'
        headers = {"content-type": "application/json",'referer':'https://gw.wozaixiaoyuan.com/h5/mobile/health/index/health/detail?id=400001','JWSESSION': jwsession}
        r: requests.Response = requests.post(
            url=url, headers=headers, json=data)      
        data = r.json()
        print(data)
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

def getSignList_v2(jwsession: str):
    try:
        url = rf'https://gw.wozaixiaoyuan.com/sign/mobile/receive/getMySignLogs?page=1&size=10'
        r = requests.get(url=url, headers={"JWSESSION": jwsession})
        res = r.json()
        code = res['code']
        if code != 0:
            if code == -10:
                return {'code': '505', 'msg': "绑定过期，重新绑定后重试"}
            return {'code': '506', 'msg': "请求未知错误", 'data': {'code': code}}
        return {'code': 0, 'msg': "网络请求成功", 'data': res['data']}
    except Exception as e:
        print(e.args)
        return {'code': 503, "msg": "网络请求异常"}
#已过期
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


def doSign_v2(jwsession: str, data: dict,id:str,schoolId:str,signId:str):
    try:
        url = rf"https://gw.wozaixiaoyuan.com/sign/mobile/receive/doSignByArea"
        data = json.dumps(data)
        r = requests.post(url=url,
                          headers={"JWSESSION": jwsession},
                          params={"id":id,"schoolId":schoolId,"signId":signId},
                          data=data)
        print(r.request.url)
        data = r.json()
        print(data)
        code = data['code']
        if code != 0:
            if code == -10:
                return {'code': '505', 'msg': "绑定过期，重新绑定后重试"}
            return {'code': '506', 'msg': "请求未知错误", 'data': {'code': code}}
        return {'code': 0, 'msg': "网络请求成功"}
    except Exception as e:
        print(e.args)
        return {'code': 503, "msg": "网络请求异常"}
    

# data = {"latitude":34.36367811414931,"longitude":108.72822889539931,"nationcode":"156","country":"中国","province":"陕西省","citycode":"156610400","city":"咸阳市","adcode":"610404","district":"渭城区","towncode":"610404004","township":"渭阳街道","streetcode":"9286619556180057229","street":"铁建路","inArea":1,"areaJSON":"{\"type\":0,\"circle\":{\"latitude\":\"34.3621962451\",\"longitude\":\"108.7292432785\",\"radius\":580},\"id\":\"40002\",\"name\":\"渭城校区\"}"}
# print(doSign('0d0c1b8cc50a4ca39074b3499243ed70',data,'621057320713064495','4','621057320570322944'))

# print(doSign('0d0c1b8cc50a4ca39074b3499243ed70',
#             {"signId": "621057320570322944",
#             "city": "\u54b8\u9633\u5e02", 
#             "longitude": "108.72826633029514", 
#             "id": "621057320713064495", 
#             "country": "\u4e2d\u56fd", 
#             "district": "\u6e2d\u57ce\u533a", 
#             "township": "\u6e2d\u9633\u8857", 
#             "latitude": "34.36141954210069",
#               "province": "\u9655\u897f\u7701"}))

def getOpenid(code: str):
    try:
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        data = {'appid': Miniprogram.appid, 'secret': Miniprogram.secret,
                'js_code': code, 'grant_type': 'authorization_code'}
        r: requests.Response = requests.post(
            url=url, data=data)
        data = r.json()
        if data.get('errcode'):
            return {'code': data['errcode'], 'msg': data['errmsg']}
        else:
            return {'code': 0, 'msg': "获取openid成功", 'data': {'openid': data['openid']}}
    except Exception as e:
        print(e.args)
        return {'code': 503, "msg": "网络请求异常"}



