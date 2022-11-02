import code
from urllib import request
from bullet import VerticalPrompt,YesNo,Input,Numbers,Bullet
from bullet import styles
import requests

# client = Bullet(**styles.Greece)

# cli = VerticalPrompt(
#     [
#         YesNo("Are you a student? "),
#         Input("Who are you? "),
#         Numbers("How old are you? "),
#         Bullet("What is your favorite programming language? ",
#               choices = ["C++", "Python", "Javascript", "Not here!"],
#               **styles.Greece),
#     ],
#     spacing = 1
# )
user = {}
user_id = 0

def login():
    cli = VerticalPrompt([Input('Input Email : '),
                      Input('Input Password : '),],spacing = 1)
    result = cli.launch()
    email = result[0][1]
    password = result[1][1]
    url = 'http://127.0.0.1:8000'
    r = requests.get(url=url+"/v1/get_user_by_email",params={'email':email,'password':password})
    data = r.json()
    if(data['code']!=0):
        return False
    user = data['data']['user']
    user_id = data['data']['user_id']
    return True

def menu():
    clil = Bullet("====菜单====",
              choices = ["退出登录", "打卡", "用户信息", "退出程序"],
              **styles.Lime)
    resultt = clil.launch()

while user_id==0:
    if(not login()):
        continue
    menu()
    


