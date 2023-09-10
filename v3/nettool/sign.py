import json
import requests

def getSignList(jwsession: str):
    try:
        url = rf'https://gw.wozaixiaoyuan.com/sign/mobile/receive/getMySignLogs?page=1&size=1'
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
# area = getSignList('0d0c1b8cc50a4ca39074b3499243ed70')['data'][0]['areaList'][0]
# area['type'] = area['shape']
# area.pop('shape')

# print(json.dumps(area))



def doSign(jwsession: str, data: dict,id:str,schoolId:str,signId:str):
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
# print(data)
area = {
    "shape":'1',
    'latitude':'34.36367811414931',
    'longitude':'108.72822889539931',
    'radius':'580',
    'id':'40002',
    'name':'渭城校区'

}
# data = {"latitude":34.36367811414931,"longitude":108.72822889539931,"nationcode":"156","country":"中国","province":"陕西省","citycode":"156610400","city":"咸阳市","adcode":"610404","district":"渭城区","towncode":"610404004","township":"渭阳街道","streetcode":"9286619556180057229","street":"铁建路","inArea":1,
#         'areaJSON':json.dumps({"type":area["shape"],"circle":{'latitude':area['latitude'],'longitude':area['longitude'],'radius':area['radius']},'id':area['id'],'name':area['name']})
#         }
# print(doSign('0d0c1b8cc50a4ca39074b3499243ed70',data,'621057320713064495','4','621057320570322944'))
