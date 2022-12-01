import datetime
import json
import default
import requests
from apscheduler.schedulers.background import BackgroundScheduler
access_token=""
appid = default.Miniprogram.appid
secret = default.Miniprogram.secret


class MiniSend():
    def __init__(self,scheduler:BackgroundScheduler) -> None:
        # self.access_token=self.flush_access_token()
        self.access_token=""
        self.flush_access_token()
        scheduler.add_job(self.flush_access_token,trigger='interval', hours=1)
    def flush_access_token(self):
        data = {
        "appid":appid,
        "secret":secret,
        "grant_type":"client_credential"
        }
        res = requests.get(url='https://api.weixin.qq.com/cgi-bin/token',params=data)
        res_json = res.json()
        print(res_json)
        access_token=res_json['access_token']
        self.access_token=access_token
        return access_token
    def demo(self):
        self.access_token=self.access_token+"1"
    def get_access_token(self):
        return self.access_token

    def send_message(self,data:dict):
        url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send'
        data = data
        if self.access_token=="":
            self.flush_access_token()
        res = requests.post(url=url,data=json.dumps(data),params={'access_token':self.access_token})
        print(res.json())


# minisend = MiniSend()
# minisend.flush_access_token()
# minisend.get_access_token()
# data = default.Miniprogram.demo_send_data
# minisend.send_message(data=data)