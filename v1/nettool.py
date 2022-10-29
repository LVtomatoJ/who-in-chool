
import requests

def net_login(bind_id,bind_password):
    try:
        url = rf'https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username'
        r:requests.Response = requests.post(url = url,params = {"username": bind_id, "password": bind_password})
        return {'code':0,"message":"网络请求成功","data":{'body':r.json(),'cookies':r.cookies}}
    except Exception as e:
        return {'code':1,"message":"网络请求失败"}