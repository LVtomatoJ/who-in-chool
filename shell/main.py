from urllib import request
from bullet import VerticalPrompt,YesNo,Input,Numbers,Bullet
from bullet import styles
import requests


user = {}
user_id = 0

def print_user_info():
    global user
    print("====用户信息====")
    for i in user.keys():
        print('*'+str(i)+" : "+str(user[i]))


def login():
    cli = VerticalPrompt([Input('输入邮箱 : '),
                      Input('输入密码 : '),])
    result = cli.launch()
    email = result[0][1]
    password = result[1][1]
    url = 'http://127.0.0.1:8000'
    r = requests.get(url=url+"/v1/get_user_by_email",params={'email':email,'password':password})
    data = r.json()
    if(data['code']!=0):
        return False
    global user  
    user = data['data']['user']
    global user_id 
    user_id = data['data']['user_id']
    return True

def menu():
    clildd = Bullet("====菜单====",
              choices = ["查看用户信息", "查看绑定信息", "查看任务信息", "退出程序"],
              **styles.Lime)
    result = clildd.launch()
    if result=="查看用户信息":
        print_user_info()
        return 1
    elif result=="查看绑定信息":
        return 0
    return 0


while user_id==0:
    if(not login()):
        continue
    while menu():
        pass

